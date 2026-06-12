import logging, os
from pathlib import Path
from typing import Callable, Tuple
import numpy

def setup_logging(filename: str):
    os.makedirs("onedrive.lnk/count_gates", exist_ok=True)
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s [%(name)s] %(message)s",
        filename=f"onedrive.lnk/count_gates/{filename}.log",
        encoding="utf-8",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.getLogger("crsq").setLevel(logging.INFO)

    logger = logging.getLogger("TEV")
    logger.setLevel(logging.INFO)

from crsq.blocks import (
    wave_function,
    hamiltonian,
    discretization,
    rfqhamiltonian,
    hamiltonian2,
    energy_initialization,
    antisymmetrization,
)
from crsq.models import hydrogen1d, hydrogen2d, hydrogen3d

from crsq.utils import circuit_tools as ctools

from qiskit import QuantumCircuit


def rfunc_for_rfq(r):
    return r


# def count_gate_rfq(dim, n):
#     dq = 1 / 2 ** (n - 1)
#     tb = radial_func_qrom.RadialFuncQrom(n, dq, rfunc_for_rfq, verbose=False)
#     qc = ctools.decompose_circuit_to_privmities(tb.circuit)
#     ops = qc.count_ops()
#     ops2 = ctools.merge_controled_gates(ops)
#     print(f"n:{n}  rfq count_ops:{ops2}")
#     return qc


# count_gates_and_save_as_csv(5, 8, count_gate_rfq, "rfqrom")
def rfunc_for_rfqh(r):
    return 1 / (r + 0.5)


def print_summary(dim: int, n: int, qc: QuantumCircuit, label: str):
    ops = qc.count_ops()
    ops2 = ctools.merge_controled_gates(ops)
    width = qc.width()
    print(f"{label} {dim}D n1={n} width: {width}, count_ops:{ops2}")


def make_ham_spec(dim, wfr_spec):
    if dim == 1:
        pos = 0
    elif dim == 2:
        pos = (0, 0)
    elif dim == 3:
        pos = (0, 0, 0)
    ham_spec = hamiltonian.HamiltonianSpec(
        wfr_spec, nuclei_data=[{"charge": 1, "pos": pos}]
    )
    return ham_spec


def make_wfr_spec(dim, n, n_frac_bits=0):
    M=1 << n
    L=32
    dq = L / M
    iq = numpy.linspace(0, M - 1, M)
    itox = iq*dq
    jtoy = iq*dq
    wfr_spec = wave_function.WaveFunctionRegisterSpec(
        dimension=dim,
        num_coordinate_bits=n,
        space_length=32,
        num_electrons=1,
        num_moving_nuclei=0,
        num_stationary_nuclei=1,
        num_frac_bits=n_frac_bits,
        i_to_x=itox,
        j_to_y=jtoy
    )
    return wfr_spec


def build_circuit_embed1d(
    wfr_spec: wave_function.WaveFunctionRegisterSpec,
) -> QuantumCircuit:
    M = 1 << wfr_spec.num_coordinate_bits
    xq = numpy.linspace(0, M - 1, M)
    xqpbc = numpy.mod(xq - M // 2, M) - M // 2
    xpbc = xqpbc * wfr_spec.delta_q
    psifunc = hydrogen1d.PsiH1D_Loudon(0, 1, True)
    psix = psifunc(xpbc)
    ini_electrons = [psix]
    ini_configs = [ini_electrons]
    initial_electron_orbitals = ini_configs
    initial_nucleus_orbitals = [[]]
    ene_spec = energy_initialization.EnergyConfigurationSpec(
        [1], initial_electron_orbitals, initial_nucleus_orbitals
    )
    asy_spec = antisymmetrization.AntisymmetrizationSpec(wfr_spec, 3)
    sd_block = energy_initialization.SlaterDeterminantPreparationBlock(
        ene_spec, asy_spec, 0
    )
    return sd_block.circuit


def build_circuit_embed2d(
    wfr_spec: wave_function.WaveFunctionRegisterSpec,
) -> QuantumCircuit:
    M = 1 << wfr_spec.num_coordinate_bits
    # unsigned index
    xq = numpy.linspace(0, M - 1, M)
    yq = numpy.linspace(0, M - 1, M)
    # signed index
    dq = wfr_spec.delta_q
    x = xq * dq
    y = yq * dq
    gx, gy = numpy.meshgrid(x, y)
    # quantum numbers
    qn = 1
    qm = 0
    x0 = 0
    y0 = 0
    psifunc2d = hydrogen2d.PsiH2D(x0, y0, dq, qn, qm)
    psixy = dq * psifunc2d(gx, gy)
    ini_electrons = [psixy]
    ini_configs = [ini_electrons]
    initial_electron_orbitals = ini_configs

    initial_nucleus_orbitals = [[]]
    ene_spec = energy_initialization.EnergyConfigurationSpec(
        [1], initial_electron_orbitals, initial_nucleus_orbitals
    )
    asy_spec = antisymmetrization.AntisymmetrizationSpec(wfr_spec, 3)
    sd_block = energy_initialization.SlaterDeterminantPreparationBlock(
        ene_spec, asy_spec, 0
    )
    return sd_block.circuit


def build_circuit_embed3d(
    wfr_spec: wave_function.WaveFunctionRegisterSpec,
) -> QuantumCircuit:
    M = 1 << wfr_spec.num_coordinate_bits
    # unsigned index
    xq = numpy.linspace(0, M - 1, M)
    yq = numpy.linspace(0, M - 1, M)
    zq = numpy.linspace(0, M - 1, M)
    # signed index
    dq = wfr_spec.delta_q
    x = xq * dq
    y = yq * dq
    z = zq * dq
    gx, gy, gz = numpy.meshgrid(x, y, z)
    # quantum numbers
    x0 = 0
    y0 = 0
    z0 = 0
    qn = 1
    ql = 0
    qm = 0
    psifunc2d = hydrogen3d.PsiH3D(x0, y0, z0, qn, ql, qm)
    psixyz = dq * psifunc2d(gx, gy, gz)
    ini_electrons = [psixyz]
    ini_configs = [ini_electrons]
    initial_electron_orbitals = ini_configs

    initial_nucleus_orbitals = [[]]
    ene_spec = energy_initialization.EnergyConfigurationSpec(
        [1], initial_electron_orbitals, initial_nucleus_orbitals
    )
    asy_spec = antisymmetrization.AntisymmetrizationSpec(wfr_spec, 3)
    sd_block = energy_initialization.SlaterDeterminantPreparationBlock(
        ene_spec, asy_spec, 0
    )
    return sd_block.circuit


def build_circuit_embed(dim, n) -> QuantumCircuit:
    wfr_spec = make_wfr_spec(dim, n)
    if dim == 1:
        circ = build_circuit_embed1d(wfr_spec)
    elif dim == 2:
        circ = build_circuit_embed2d(wfr_spec)
    elif dim == 3:
        circ = build_circuit_embed3d(wfr_spec)
    return (circ, "Initial state embedding")


def build_circuit_arithmetic(dim, n) -> QuantumCircuit:
    # wfr_spec = make_wfr_spec(dim, n, 0)
    wfr_spec = make_wfr_spec(dim, n, n-1)
    ham_spec = make_ham_spec(dim, wfr_spec)
    delta_t = 1e-3
    disc_spec = discretization.DiscretizationSpec(delta_t)
    epb = hamiltonian.ArithElectronPotentialBlock(ham_spec, disc_spec, 1.0)
    return (epb.circuit, "Arithmetic Hamiltonian")

def build_circuit_arithmetic_with_frac_bits(dim, n) -> QuantumCircuit:
    wfr_spec = make_wfr_spec(dim, n, n-1)
    ham_spec = make_ham_spec(dim, wfr_spec)
    delta_t = 1e-3
    disc_spec = discretization.DiscretizationSpec(delta_t)
    epb = hamiltonian.ArithElectronPotentialBlock(ham_spec, disc_spec, 1.0)
    return (epb.circuit, "Arithmetic Hamiltonian")


def build_circuit_rfq(
    dim: int, n: int, label, use_symmetry, use_transpose, use_gray_code
) -> QuantumCircuit:
    wfr_spec = make_wfr_spec(dim, n)
    ham_spec = make_ham_spec(dim, wfr_spec)
    rfunc = rfunc_for_rfqh
    rfq_spec = rfqhamiltonian.RfqPotentialSpec(
        wfr_spec,
        rfunc,
        rfunc,
        use_symmetry=use_symmetry,
        use_transpose=use_transpose,
        use_gray_code=use_gray_code,
    )
    delta_t = 1e-3
    disc_spec = discretization.DiscretizationSpec(delta_t)
    repb = rfqhamiltonian.RfqElectronPotentialBlock(rfq_spec, ham_spec, disc_spec, 1.0)
    return (repb.circuit, label)


def build_circuit_vsqrom_newton(dim: int, n: int) -> QuantumCircuit:
    wfr_spec = make_wfr_spec(dim, n)
    ham2 = hamiltonian2.InverseSquareRoot(wfr_spec)
    return (ham2.circuit, "VSQROM + Newton-Raphson")


def count_gates_and_save_as_csv(
    dmin: int,
    dmax: int,
    n1min,
    n1max,
    build_circuit_func: Callable[[int, int], Tuple[QuantumCircuit, str]],
    label,
):
    outdir = "onedrive.lnk/count_gates"
    filename = (
        f"{outdir}/hamiltonian-gatecount-{label}-d{dmin}-{dmax}-n{n1min}-{n1max}.csv"
    )
    if Path(filename).is_file():
        print("CSV file exists. skipping : ", filename)
        return
    else:
        print("Starting for ", filename)
    setup_logging(f"hamiltonian-gatecount-{label}-d{dmin}-{dmax}-n{n1min}-{n1max}")
    oplist = []
    for d in range(dmin, dmax + 1):
        for n in range(n1min, n1max + 1):
            hlqc, title = build_circuit_func(d, n)
            circ_diagram_filename = f"{outdir}/circuit-{label}-{d}D-{n}bits.png"
            hlqc.draw(output="mpl", filename=circ_diagram_filename, scale=0.6, fold=100)
            gate_list = [
                "circuit",
                "adder",
                "subtractor",
                "square",
                "sqrt",
                "divide",
                "UMA",
                "MAJ",
                "ucrz",
                "ccx",
                "mcphase"
            ]
            qc = ctools.decompose_circuit_to_privmities(hlqc, gate_list)
            print_summary(d, n, qc, title)
            width = qc.width()
            odict = qc.count_ops()
            odict2 = ctools.merge_controled_gates(odict)
            odict2["dim"] = d
            odict2["n"] = n
            odict2["width"] = width
            oplist.append(odict2)
    cols0 = [
        "dim",
        "n",
        "width",
        "mcx",
        "ccx",
        "cswap",
        "cx",
        "crx",
        "cry",
        "crz",
        "cp",
        "cu",
        "x",
        "h",
        "t",
        "tdg",
        "rx",
        "ry",
        "rz",
        "u",
        "p",
    ]
    cols = [col for col in cols0 if col in oplist[0]]
    with open(filename, "w") as f:
        f.write(",".join(cols) + "\n")
        for op in oplist:
            f.write(",".join([str(op[col]) for col in cols]) + "\n")


# count_gate_arithmetic_elec_potential(5)


def build_circuit_sawtooth_qrom(dim, n) -> QuantumCircuit:
    return build_circuit_rfq(dim, n, "Sawtooth", False, False, False)


def build_circuit_sym_qrom(dim, n) -> QuantumCircuit:
    return build_circuit_rfq(dim, n, "Symmetry RFQROM", True, False, False)


def build_circuit_sym_trans_qrom(dim, n) -> QuantumCircuit:
    return build_circuit_rfq(dim, n, "Symmetry Transpose RFQROM", True, True, False)


def build_circuit_ucrz(dim, n) -> QuantumCircuit:
    return build_circuit_rfq(dim, n, "UCRZ", False, False, True)


dmin = 1
dmax = 2

nmin = 8
nmax = 8

calc_embed = True
calc_arith = True
calc_ucrz = True

calc_vsqrom = False 
calc_sawtooth = False
calc_4fold = False
calc_8fold = False

calc_3d_large = False

calc_frac_bits = False

if calc_frac_bits:
    count_gates_and_save_as_csv(
        2, 3, 5, 7, build_circuit_arithmetic_with_frac_bits, "arith-elec-potential-fracbits"
    )
    count_gates_and_save_as_csv(2, 2, 8, 10, build_circuit_arithmetic_with_frac_bits, "arith-elec-potential-fracbits")

if calc_embed:
    count_gates_and_save_as_csv(1, 3, 5, 7, build_circuit_embed, "embed")
    count_gates_and_save_as_csv(1, 2, 8, 10, build_circuit_embed, "embed")
    count_gates_and_save_as_csv(3, 3, 8, 8, build_circuit_embed, "embed")

if calc_arith:
    count_gates_and_save_as_csv(
        1, 3, 5, 8, build_circuit_arithmetic, "arith-elec-potential"
    )
    
    count_gates_and_save_as_csv(
       1, 2, 9, 10, build_circuit_arithmetic, "arith-elec-potential"
    )

if calc_3d_large:
    count_gates_and_save_as_csv(3, 3, 9, 10, build_circuit_arithmetic, "arith-elec-potential")
    count_gates_and_save_as_csv(3, 3, 8, 8, build_circuit_embed, "embed")

if calc_ucrz:
    count_gates_and_save_as_csv(1, 3, 5, 7, build_circuit_ucrz, "ucrz")
    count_gates_and_save_as_csv(3, 3, 8, 9, build_circuit_ucrz, "ucrz")
    count_gates_and_save_as_csv(1, 2, 8, 10, build_circuit_ucrz, "ucrz")

if calc_vsqrom:
    count_gates_and_save_as_csv(
        dmin, dmax, nmin, nmax, build_circuit_vsqrom_newton, "vsqrom-newton"
    )

if calc_sawtooth:
    count_gates_and_save_as_csv(
        dmin, dmax, nmin, nmax, build_circuit_sawtooth_qrom, "sawtooth-qrom"
    )

if calc_4fold:
    count_gates_and_save_as_csv(
        dmin, dmax, nmin, nmax, build_circuit_sym_qrom, "rfqrom-sym"
    )

if calc_8fold:
    count_gates_and_save_as_csv(
        dmin, dmax, nmin, nmax, build_circuit_sym_trans_qrom, "rfqrom-sym-trans"
    )
