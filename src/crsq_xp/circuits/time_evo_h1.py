import numpy

from crsq.blocks.antisymmetrization import AntisymmetrizationSpec
from crsq.blocks.discretization import DiscretizationSpec
from crsq.blocks.energy_initialization import EnergyConfigurationSpec
from crsq.blocks.hamiltonian import HamiltonianSpec
from crsq.blocks.rfqhamiltonian import RfqPotentialSpec
from crsq.blocks.time_evolution.spec import (
    TimeEvolutionSpec,
    SUZUKI_TROTTER_ARITHMETIC,
    SUZUKI_TROTTER_QROM,
)
from crsq.blocks.wave_function import WaveFunctionRegisterSpec
from crsq.blocks.time_evolution.suzuki_trotter import SuzukiTrotterMethodBlock
from crsq.models import hydrogen1d
from crsq.reports import H1D1Report
import crsq.utils.statevector as svec
from crsq.utils.qfthelper import BitReverser

from qiskit_aer import AerSimulator
from qiskit import transpile
from qiskit.quantum_info import Statevector

import logging

logger = logging.getLogger(__name__)


class Driver1D:

    def hp_func(self, q: float) -> float:
        r = numpy.abs(q - self.x0)
        if r == 0:
            invr = 2 / self.dq
        else:
            invr = 1 / r
        return -1 * invr

    def elec_proton_potential_func(self, r: float) -> float:
        if r == 0:
            r = self.dq / 2
        qq = -1 * 1
        return qq / r

    def elec_elec_potential_func(self, r: float) -> float:
        if r == 0:
            r = self.dq / 2
        qq = -1 * -1
        return qq / r

    def __init__(
        self,
        outdir="output/default",
        device="GPU",
        enable_cuStateVec=True,
        precision="single",
        delta_t=0.001,
        n1=6,
        signed=False,
        parity="odd",
        qn=1,
        length=16,
        psimax=0.5,
        window_radius=32,
        trotter_order=1,
        x0=8,
        num_elec_iters=1,
        num_nucl_iters=1,
        st_method=SUZUKI_TROTTER_ARITHMETIC,
        st_method_label="arithmetic",
        use_saved_data=False,
        dpi=None,
    ):
        self.outdir = outdir
        self.device = device
        self.enable_cuStateVec = enable_cuStateVec
        self.precision = precision
        self.dim = 1  # 1 dimension
        self.n1 = n1  # bits per coordinate
        self.M = 1 << n1
        self.WM = window_radius
        self.trotter_order = trotter_order
        self.L = length  # 16 bohr
        self.psimax = psimax
        self.x0 = x0
        self.dq = self.L / self.M
        self.eta = 1  # num of electrons
        self.Ln = 0  # moving nucleus
        self.Ls = 1  # stationary nucleus
        self.num_nucl_iters = num_nucl_iters
        self.num_elec_iters = num_elec_iters
        self._dpi = dpi
        self.st_method = st_method
        self.st_method_label = st_method_label
        self.signed = signed
        self.parity = parity
        self.qn = qn
        self.antisym_method = 3  # binary coded antisymmetrization method
        logger.info(f"Parameters.signed: {self.signed}")

        # atom position in discretized coords.
        M = int(self.M)
        xq0 = int(x0 // self.dq)
        xqmin = xq0 - M // 2
        xqmax = xq0 + M // 2
        logger.info(f"xqmin={xqmin}, xqmax={xqmax}")

        if not self.signed:
            # series of x coordinates.
            self.xq = numpy.linspace(0, M - 1, M)
            xqpbc = numpy.mod(self.xq - xq0 + M // 2, M) - M // 2 + xq0
        else:
            # series of x coordinates.
            self.xq = numpy.mod(numpy.linspace(-M // 2, M // 2 - 1, M), M) - M // 2
            xqpbc = numpy.mod(self.xq - xq0 + M // 2, M) - M // 2 + xq0

        self.x = self.xq * self.dq
        logger.info("atom pos x0=%f", self.x0)

        self.wfr_spec = WaveFunctionRegisterSpec(
            self.dim, self.n1, self.L, self.eta, self.Ln, self.Ls, i_to_x=self.x
        )

        self.xpbc = xqpbc * self.dq
        for i in range(4):
            logger.info(f"xpbc[{i}]={self.xpbc[i]}")
        logger.info(f"x0 = {self.x0}")

        self._make_ene_spec()

        self.delta_t = delta_t  # a.u.
        self.disc_spec = DiscretizationSpec(self.delta_t)
        self.asy_spec = AntisymmetrizationSpec(self.wfr_spec, self.antisym_method)
        self.nuclei_data = [{"mass": 1680, "charge": 1, "pos": int(self.x0 / self.dq)}]

        self._bit_reverser = BitReverser(self.n1)

        if self.st_method == SUZUKI_TROTTER_QROM:
            self.rfq_spec = RfqPotentialSpec(
                self.wfr_spec,
                self.elec_elec_potential_func,
                self.elec_proton_potential_func,
                use_symmetry=False,
                use_transpose=False,
                use_gray_code=True,
            )
        else:
            self.rfq_spec = None

        self.ham_spec = HamiltonianSpec(self.wfr_spec, nuclei_data=self.nuclei_data)

        self.evo_spec = TimeEvolutionSpec(
            self.ham_spec,
            self.disc_spec,
            self.num_nucl_iters,
            self.num_elec_iters,
            self.st_method,
            self.trotter_order,
            self.rfq_spec,
            save_q_state_vector=True,
            save_p_state_vector=True,
        )

        self.use_saved_data = use_saved_data
        self.stm_block = None

        self.report = H1D1Report(
            outdir,
            title=f"H 1D {self.st_method_label} L={self.L} n={self.qn} nb={self.n1} dt={self.delta_t:.3f}",
            psifunc_label=self.psifunc_label,
            num_coordinate_bits=self.n1,
            psi_axis_scale=self.psimax,
            space_length=self.L,
            window_radius=self.WM,
            hp_func=self.hp_func,
            delta_t=delta_t,
            num_elec_iters=self.num_elec_iters,
            num_nucl_iters=self.num_nucl_iters,
            signed=self.signed,
            dpi=self._dpi,
        )

    def _make_ene_spec(self):
        qn = self.qn
        parity = self.parity
        self.psifunc = hydrogen1d.PsiH1D_Loudon(self.x0, qn, parity == "odd")
        self.psifunc_label = self.psifunc.label
        self.psix = self.psifunc(self.xpbc)
        ini_electrons = [self.psix]
        ini_configs = [ini_electrons]
        initial_electron_orbitals = ini_configs

        initial_nucleus_orbitals = [[]]
        self.ene_spec = EnergyConfigurationSpec(
            [1], initial_electron_orbitals, initial_nucleus_orbitals
        )

    def draw_circuits(self):

        evo_spec_for_draw = TimeEvolutionSpec(
            self.ham_spec,
            self.disc_spec,
            self.num_nucl_iters,
            self.num_elec_iters,
            self.st_method,
            self.trotter_order,
            self.rfq_spec,
            save_q_state_vector=False,
            use_for_loop_gate=True,
        )

        # don't use motion block gates for drawing the circuit
        stm_block = SuzukiTrotterMethodBlock(
            evo_spec_for_draw,
            self.ene_spec,
            self.asy_spec,
            use_motion_block_gates=True,  # to make the diagram symmetric with the ucrz version
        )

        logger.info("draw the circuit")
        self.report.add_circuit_diagram(stm_block.circuit, "circuit")

        # draw the circuit

        if self.st_method == SUZUKI_TROTTER_QROM:
            emb = stm_block.build_electron_motion_block(sim_time=0)
            self.report.add_circuit_diagram(emb.circuit, "elec_motion")

            epbq = emb.build_elec_potential_block_qrom(1.0)
            self.report.add_circuit_diagram(epbq.circuit, "elec_potential_qrom")

            ekbq = emb.build_elec_kinetic_block()
            self.report.add_circuit_diagram(ekbq.circuit, "elec_kinetic")
        else:
            emb = stm_block.build_electron_motion_block(sim_time=0)
            self.report.add_circuit_diagram(emb.circuit, "elec_motion")

            epot = emb.build_elec_potential_block_arithmetic()
            self.report.add_circuit_diagram(epot.circuit, "elec_potential_arithmetic")

            ekbq = emb.build_elec_kinetic_block()
            self.report.add_circuit_diagram(ekbq.circuit, "elec_kinetic")

    def run_circuit(self):
        # run the simulator
        logger.info("run the simulator")

        backend = AerSimulator(
            method="statevector",
            device=self.device,
            cuStateVec_enable=self.enable_cuStateVec,
            precision=self.precision,
        )
        backend.set_options(max_parallel_threads=0)

        # use motion block gates for simulation
        self.stm_block = SuzukiTrotterMethodBlock(
            self.evo_spec,
            self.ene_spec,
            self.asy_spec,
            use_motion_block_gates=True,
        )

        if self.use_saved_data:
            logger.info("Skipping simulation, using saved data")
            return

        circ = self.stm_block.circuit
        logger.info("transpile START")
        transpiled = transpile(circ, backend)
        total_global_phase = transpiled.global_phase
        logger.info("accumulated global phase of the circuit: %f", total_global_phase)
        logger.info("transpile END, run START")
        result = backend.run(transpiled).result()
        if not result.success:
            logger.error("simulation failed")
            raise ValueError("simulation failed")
            return
        logger.info("run END")
        dt = self.disc_spec.delta_t
        for nucl_it in range(self.num_nucl_iters + 1):
            # phase = total_global_phase * (_nucl_it + 1)/self.num_nucl_iters
            phase = total_global_phase
            t = dt * self.evo_spec.num_elec_per_atom_iterations * nucl_it
            self._save_result_state_vectors(result, t, phase)

    def _save_result_state_vectors(self, result, t, global_phase):
        logger.info("global phase at t=%f: %f", t, global_phase)
        q_state_label = self.evo_spec.make_state_vector_label(t)
        qsv: Statevector = result.data()[q_state_label]
        phase_adjusted_qdata = qsv.data * numpy.exp(-1j * global_phase)
        self.report.add_q_state_vector_file(t, qsv.dim, phase_adjusted_qdata)
        p_state_label = self.evo_spec.make_state_vector_label(t, "qft")
        psv: Statevector = result.data()[p_state_label]
        phase_adjusted_pdata = psv.data * numpy.exp(-1j * global_phase)
        reordered_data = self._reverse_electron_bits(phase_adjusted_pdata)
        self.report.add_p_state_vector_file(t, psv.dim, reordered_data)

    def _reverse_electron_bits(self, data):
        n1 = self.wfr_spec.num_coordinate_bits
        M = 1 << n1
        result = numpy.zeros(M, dtype=numpy.complex128)
        for i in range(M):
            j = self._bit_reverser.reverse_bits(i)
            result[j] = data[i]
        return result

    def draw_graph(self):
        """draw the graph based on the results file."""
        self.report.open_report()

        dt = self.disc_spec.delta_t
        for nucl_it in range(self.num_nucl_iters + 1):
            t = dt * self.evo_spec.num_elec_per_atom_iterations * nucl_it
            self._add_plot_from_file(t)

        self.report.generate_report()

    def _add_plot_from_file(self, time):
        qc = self.stm_block.circuit
        bit_range = svec.get_bit_range_for_reg(qc, "xq0")
        q_data = self.report.read_q_state_vector_file(time, bit_range)
        p_data = self.report.read_p_state_vector_file(time, bit_range)
        self.report.add_wave_function_plot(time, q_data, p_data)
        self.report.record_energy(time, q_data, p_data)
