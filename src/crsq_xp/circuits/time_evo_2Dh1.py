# This module does not use cupy.
import numpy as np
import numpy.typing as npt

from crsq.blocks.antisymmetrization import AntisymmetrizationSpec
from crsq.blocks.discretization import DiscretizationSpec
from crsq.blocks.energy_initialization import EnergyConfigurationSpec
from crsq.blocks.hamiltonian import HamiltonianSpec
from crsq.blocks.time_evolution.spec import TimeEvolutionSpec, SUZUKI_TROTTER_QROM
from crsq.blocks.wave_function import WaveFunctionRegisterSpec
from crsq.blocks.time_evolution.suzuki_trotter import SuzukiTrotterMethodBlock
from crsq.blocks.rfqhamiltonian import RfqPotentialSpec

from crsq.utils.sparse_statevector import SparseStatevector
from crsq.models import hydrogen2d

from qiskit_aer import AerSimulator
from qiskit import transpile
from crsq.utils.qfthelper import BitReverser
import crsq.utils.sparse_statevector as ssvec
from crsq.reports import H1D2Report

import logging

logger = logging.getLogger(__name__)


# build the simulator
class Driver2D:

    def __init__(
        self,
        outdir,
        device,
        enable_cuStateVec,
        dim,
        length,
        psixmax,
        psikmax,
        qn,
        qm,
        trotter_order,
        delta_t,
        pole_mitigation="r0lim",
        eps=0.25,
        precision="single",
        n1=5,
        signed=False,
        num_nucl_iters=1,
        num_elec_iters=2,
        plot_type="3d-3qp",
        use_saved_data=False,
        save_psi2=False,
        dpi=None,
    ):
        self.outdir = outdir
        self.device = device
        self.enable_cuStateVec = enable_cuStateVec
        self.precision = precision
        self.dim = dim  # 1 dimension
        self.qn = qn
        self.qm = qm
        self.trotter_order = trotter_order
        self.pole_mitigation = pole_mitigation
        self.eps = eps
        self.n1 = n1  # bits per coordinate
        self.signed = signed
        self.M = 1 << n1
        self.L = length  # bohrs
        self.psixmax = psixmax
        self.psikmax = psikmax
        self.delta_t = delta_t
        self.dq = self.L / self.M
        self.eta = 1  # num of electrons
        self.Ln = 0  # moving nucleus
        self.Ls = 1  # stationary nucleus
        self.num_nucl_iters = num_nucl_iters
        self.num_elec_iters = num_elec_iters
        # QROM optimization switches
        self.use_symmetry = False
        self.use_transpose = False
        self.use_gray_code = True
        self.save_state_vector_per_qrom = save_psi2
        self.save_state_vector_per_atom_iteration = True
        self.antisym_method = 3  # binary coded antisymmetrization method
        self.plot_type = plot_type
        self.use_saved_data = use_saved_data
        self._dpi = dpi

        M = self.M
        if self.signed:
            iq = np.mod(np.linspace(-M // 2, M // 2 - 1, M), M) - (M // 2)
        else:
            # unsigned index
            iq = np.linspace(0, M - 1, M)
        self.xq, self.yq = np.meshgrid(iq, iq)
        dq = self.dq
        self.x = self.xq * dq
        self.y = self.yq * dq

        i_to_x = iq * dq

        self.wfr_spec = WaveFunctionRegisterSpec(
            self.dim,
            self.n1,
            self.L,
            self.eta,
            self.Ln,
            self.Ls,
            i_to_x=i_to_x,
            j_to_y=i_to_x,
        )

        self.disc_spec = DiscretizationSpec(self.delta_t)
        self.asy_spec = AntisymmetrizationSpec(self.wfr_spec, self.antisym_method)

        if self.signed:
            self.Qx0 = 0
            self.Qy0 = 0
        else:
            self.Qx0 = self.L / 2
            self.Qy0 = self.L / 2

        self.nuclei_data = [
            {
                "mass": 1680,
                "charge": 1,
                "pos": (int(self.Qx0 / self.dq), int(self.Qy0 / self.dq)),
            }
        ]

        self._bit_reverser = BitReverser(self.n1)

        self.ham_spec = HamiltonianSpec(self.wfr_spec, nuclei_data=self.nuclei_data)
        self.stm_block = None

        self._make_ene_spec()

        logger.info("dq: %f", self.dq)

        # report は self.init で作成
        # self.run_circuit の中では add でデータをファイルに補間。レポート生成はしない
        # self.draw_graph の中では open_report, add_plot, generate_report でファイル生成
        s = self.psixmax
        ks = self.psikmax
        psifunc2 = hydrogen2d.PsiH2D(Qx0=self.Qx0, Qy0=self.Qy0, dq=self.dq, n=self.qn, m=self.qm)
        if self.pole_mitigation == "rofs":
            self.vfunc2 = hydrogen2d.VHAtom2(Qx0=self.Qx0, Qy0=self.Qy0, dq=self.dq, r0=0, Z=1, eps=self.eps)
            self.elec_nuc_potential_func = self.Hen_rofs
        else:
            self.vfunc2 = hydrogen2d.VHAtom2(Qx0=self.Qx0, Qy0=self.Qy0, dq=self.dq, r0=psifunc2.r0_for_pole(self.pole_mitigation, self.eps), Z=1)
            self.elec_nuc_potential_func = self.Hen_r0lim
        self.report = H1D2Report(
            outdir,
            self.plot_type,
            title=f"H 2D look-up L={self.L} n={self.qn} m={self.qm} nb={self.n1} dt={self.delta_t:.3f}",
            psifunc_label=self.psifunc2d.label,
            num_coordinate_bits=self.n1,
            zmin=0,
            zmax=s,
            vmin=-s,
            vmax=s,
            kzmin=0,
            kzmax=ks,
            kvmin=-ks,
            kvmax=ks,
            space_length=self.L,
            hp_func=self.vfunc2,
            delta_t=self.delta_t,
            num_elec_iters=self.num_elec_iters,
            num_nucl_iters=self.num_nucl_iters,
            signed=self.signed,
            dpi=self._dpi,
        )

    def _make_ene_spec(self):
        """make EnergyConfigurationSpec"""

        # quantum numbers
        qn = self.qn
        qm = self.qm
        self.psifunc2d = hydrogen2d.PsiH2D(self.Qx0, self.Qy0, self.dq, qn, qm)
        logger.info("psifunc2d = %s", self.psifunc2d.label)
        logger.info("Energy eigen value = %f", self.psifunc2d.eigen_value)
        psixy = self.dq * self.psifunc2d(self.x, self.y)
        M = self.M
        if self.signed:
            CM = 0
        else:
            CM = M // 2
        for i in range(-2,3):
            si = (CM + i + M) % M
            for j in range(-2, 3):
                sj = (CM + j + M) % M
                logger.info(
                    "psixy[%d,%d]=psixy(%f,%f)=(%f,%f)",
                    i,
                    j,
                    self.x[si, sj],
                    self.y[si, sj],
                    psixy[si, sj].real,
                    psixy[si, sj].imag,
                )
        ini_electrons = [psixy]
        ini_configs = [ini_electrons]
        initial_electron_orbitals = ini_configs

        initial_nucleus_orbitals = [[]]
        self.ene_spec = EnergyConfigurationSpec(
            [1], initial_electron_orbitals, initial_nucleus_orbitals
        )

    def Hen_r0lim(self, r: float) -> float:
        """Ha1 potential function for r0lim pole mitigation"""
        if r == 0:
            r0 = self.dq * self.eps
            return -1 / r0
        return -1 / r

    def Hen_rofs(self, r: float) -> float:
        """Ha2 potential function for rofs pole mitigation"""
        return -1 / np.sqrt(r * r + (self.dq * self.eps)**2)

    def elec_elec_potential(self, r: float) -> float:
        if r == 0:
            return 2 / self.dq
        return 1 / r

    def draw_circuits(self):

        # psix = np.zeros(M)
        # psiy = np.zeros(M)

        logger.info(
            "use_symmetry: %s , use_transpose: %s",
            self.use_symmetry,
            self.use_transpose,
        )
        rfq_spec = RfqPotentialSpec(
            self.wfr_spec,
            self.elec_elec_potential,
            self.elec_nuc_potential_func,
            use_symmetry=self.use_symmetry,
            use_transpose=self.use_transpose,
            use_gray_code=self.use_gray_code,
            save_state_vector_per_qrom=False,
        )

        evo_spec = TimeEvolutionSpec(
            self.ham_spec,
            self.disc_spec,
            self.num_nucl_iters,
            self.num_elec_iters,
            method=SUZUKI_TROTTER_QROM,
            trotter_order=self.trotter_order,
            rfq_spec=rfq_spec,
            save_q_state_vector=False,  # False when we are just drawing
            use_for_loop_gate=True,
        )

        logger.info("Build SuzukiTrotterMethodBlock to draw the circuit")
        stm_block = SuzukiTrotterMethodBlock(
            evo_spec, self.ene_spec, self.asy_spec, use_motion_block_gates=True
        )

        self.report.add_circuit_diagram(stm_block.circuit, "circuit")

        emb = stm_block.build_electron_motion_block(sim_time=0)
        self.report.add_circuit_diagram(emb.circuit, "elec_motion")

        weight = 1.0
        epbq = emb.build_elec_potential_block_qrom(weight)
        self.report.add_circuit_diagram(epbq.circuit, "elec_potential_qrom")

    def _make_evo_spec_for_running(self):
        rfq_spec = RfqPotentialSpec(
            self.wfr_spec,
            self.elec_elec_potential,
            self.elec_nuc_potential_func,
            use_symmetry=self.use_symmetry,
            use_transpose=self.use_transpose,
            use_gray_code=self.use_gray_code,
            save_state_vector_per_qrom=self.save_state_vector_per_qrom,
        )

        evo_spec = TimeEvolutionSpec(
            self.ham_spec,
            self.disc_spec,
            self.num_nucl_iters,
            self.num_elec_iters,
            method=SUZUKI_TROTTER_QROM,
            trotter_order=self.trotter_order,
            rfq_spec=rfq_spec,
            save_q_state_vector=self.save_state_vector_per_atom_iteration,  # True when we are running
            save_p_state_vector=True,
        )
        return evo_spec

    def run_circuit(self):
        # run the simulator
        logger.info("run the simulator")

        backend = AerSimulator(
            method="statevector",
            device=self.device,
            cuStateVec_enable=self.enable_cuStateVec,
            precision=self.precision,
        )
        num_threads = 0
        backend.set_options(max_parallel_threads=num_threads)

        evo_spec = self._make_evo_spec_for_running()

        stm = SuzukiTrotterMethodBlock(
            evo_spec, self.ene_spec, self.asy_spec, use_motion_block_gates=True
        )

        circ = stm.circuit
        logger.info("transpile START")
        transpiled = transpile(circ, backend)
        total_global_phase = transpiled.global_phase
        logger.info("accumulated global phase of the circuit: %f", total_global_phase)
        logger.info("transpile END, run START")
        results = backend.run(transpiled).result()
        logger.info("run END")
        dt = self.delta_t
        for nucl_it in range(self.num_nucl_iters + 1):
            t = dt * evo_spec.num_elec_per_atom_iterations * nucl_it
            self._save_result_state_vectors(circ, results, t, evo_spec, total_global_phase)

    def _save_result_state_vectors(
        self, circuit, results, t, evo_spec: TimeEvolutionSpec, global_phase: float
    ):
        state_label_prefix_to_file_suffix = {"sv": "q"}
        if evo_spec.rfq_spec.should_save_state_vector_per_qrom:
            state_label_prefix_to_file_suffix["qrom0"] = "qrom0"
            state_label_prefix_to_file_suffix["qrom1"] = "qrom1"
        if evo_spec.should_save_p_state_vector:
            state_label_prefix_to_file_suffix["qft"] = "p"
        for prefix, suffix in state_label_prefix_to_file_suffix.items():
            label = evo_spec.make_state_vector_label(t, prefix)
            logger.info("looking for state vector with label %s", label)
            if label in results.data():
                sv = results.data()[label]
                ssv = ssvec.sv_to_sparse(sv)
                phase_adjusted_ssv = SparseStatevector(ssv.num_bits, ssv.keys, ssv.values * np.exp(-1j * global_phase))
                data2d = self._make_2d_data_from_ssv(circuit, phase_adjusted_ssv)
                # store data on files.
                if label[:3] == "qft":
                    logger.info("reversing bits for state vector %s", label)
                    revdata2d = self._reverse_electron_bits2d(data2d)
                    self.report.add_data_sample(suffix, t, revdata2d)
                else:
                    self.report.add_data_sample(suffix, t, data2d)
            else:
                logger.warning("state vector %s was not found", label)

    def _make_2d_data_from_ssv(self, circuit, ssv):
        np_data2d = ssvec.extract_dist2d(circuit, ssv, "yq0", "xq0")
        return np_data2d

    def _reverse_electron_bits2d(
        self, data2d: npt.NDArray[np.complex128]
    ) -> npt.NDArray[np.complex128]:
        result = np.zeros(data2d.shape, dtype=np.complex128)
        for i in range(data2d.shape[0]):
            ri = self._bit_reverser.reverse_bits(i)
            for j in range(data2d.shape[1]):
                rj = self._bit_reverser.reverse_bits(j)
                result[ri, rj] = data2d[i, j]
        return result

    def draw_graph(self):
        """draw the graph based on the results file."""
        self.report.open_report()
        dt = self.delta_t
        evo_spec = self._make_evo_spec_for_running()
        for nucl_it in range(self.num_nucl_iters + 1):
            t = dt * evo_spec.num_elec_per_atom_iterations * nucl_it
            self._add_plots_from_file(t, evo_spec)

        self.report.generate_report()

    def _add_plots_from_file(self, time, evo_spec: TimeEvolutionSpec):
        q_data = self.report.read_data_sample("q", time)
        if time == 0:
            self._q0_data = q_data
        if evo_spec.should_save_p_state_vector:
            p_data = self.report.read_data_sample("p", time)
        else:
            p_data = None
        self.report.produce_frame(time, q_data, p_data)
        self.report.record_energy(time, q_data, p_data, self._q0_data)
