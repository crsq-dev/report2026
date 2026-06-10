"""State dependent Trotter error analyzer"""

import cmath
import math
import os
import numpy
import numpy.typing as npt
import pandas as pd
import matplotlib.pyplot as plt

from crsq_xp.classic import cu_suzuki_trotter2, params
from crsq.models import hydrogen2d
from crsq.error import sdbound

import logging

logger = logging.getLogger(__name__)


class Evaluator:
    """Evalutor for Trotter order 1.
    Evaluates observed trotter error and error bound for given range of parameters
    """

    def __init__(
        self, basedir: str, nb: int, qn: int, qm: int, En: float, L: int, t: float
    ):
        """
        Args:
            :param nb: number of bits
            :param qn: quantum number n
            :param qm: quantum number m
            :param En: energy level
            :param L: system size
            :param t: time
        """
        self._nb = nb
        self._qn = qn
        self._qm = qm
        self._En = En
        self._L = L
        self._t = t
        # Index 0 corresponds to trotter order 1, index 1 to order 2.
        self._xi = [[], []]
        self._bd = [[], []]
        self._ymin = 1e-4
        self._ymax = 1e+4
        self._basedir = basedir
        self._outdir = f"{self._basedir}/graphs/t{self._t}"
        os.makedirs(self._outdir, exist_ok=True)
        logfilename = basedir + f"/evaluator.n{qn}.m{qm}.log"
        # delete the old log file if exists
        if os.path.exists(logfilename):
            os.remove(logfilename)
        logging.basicConfig(
            format="%(asctime)s %(levelname)-8s [%(name)s] %(message)s",
            filename=logfilename,
            encoding="utf-8",
            level=logging.INFO,
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    
    def set_ylim(self, ymin, ymax):
        self._ymin = ymin
        self._ymax = ymax

    def run(self, log_nt: list[float]):
        """log_nt: list of log_nT. the value of nT = 10**log_nT"""
        self._csv_filename = f"{self._outdir}/trotter_err_n{self._qn}_m{self._qm}_{self._nb}b_t{self._t}.csv"
        if os.path.exists(self._csv_filename):
            self._read_data()
        else:
            self._calc_data(log_nt)

    def _calc_data(self, log_nt: list[float]):
        self._nT = [10**logn for logn in log_nt]
        self._dt = [self._t / nT for nT in self._nT]
        for nT, dt in zip(self._nT, self._dt):
            print("nt: ", nT, ", dt: ", dt)
            self._eval(int(nT), dt)
        self._save_data()

    def _save_data(self):
        print(f"Writing data to '{self._csv_filename}'")
        csvdata = {}
        csvdata["xi1"] = self.xi1
        csvdata["xi2"] = self.xi2
        csvdata["bd1"] = self.bd1
        csvdata["bd2"] = self.bd2
        nt = self.nT
        df = pd.DataFrame(index=nt, data=csvdata)
        df.to_csv(self._csv_filename, index=True, index_label="nT", header=True)

    def _read_data(self):
        print(f"Reading data from '{self._csv_filename}'")
        df = pd.read_csv(self._csv_filename)
        print("df:", df)
        self._nT = df["nT"]
        self._xi = [df["xi1"], df["xi2"]]
        self._bd = [df["bd1"], df["bd2"]]

    def _eval(self, nT, dt):
        for trotter_order in [1, 2]:
            self._make_dirs(nT, trotter_order)
            self._make_params(dt, trotter_order)
            self._make_simulator()
            self._st.run_simulation()
            self._st.generate_animation_frames()
            xi, bd = self._analyze_data(trotter_order)
            index = trotter_order - 1
            self._xi[index].append(xi)
            self._bd[index].append(bd)

    def _make_dirs(self, nT, trotter_order):
        self._datadir = f"{self._basedir}/n{self._qn}_m{self._qm}_{self._nb}b_TO{trotter_order}_L{self._L}_t{self._t}/nT{nT:06d}"
        os.makedirs(self._datadir, exist_ok=True)

    def _make_params(self, dt, trotter_order):
        logger.info("Making parameters for nbit: %d, trotter_order: %d, dt: %f", self._nb, trotter_order, dt)
        self._par = params.Params(
            n1=self._nb,
            dimension=2,
            L=self._L,
            psixmax=1,
            psikmax=1,
            dt=dt,
            interval_time=self._t,
            total_time=self._t,
            signed=True,
            WM=1,
            trotter_order=trotter_order,
            qn=self._qn,
            qm=self._qm,
            pole_mitigation="r0lim",
            eps=0.25, # Δ1=eps*dq
            plot_type="3d-3qp",
            clean_report_dir=False,
            save_psi2=False,
        )

    def _make_simulator(self):
        par = self._par
        if par.signed:
            Qx0 = 0
            Qy0 = 0
        else:
            Qx0 = par.L / 2
            Qy0 = par.L / 2
        psifunc2 = hydrogen2d.PsiH2D(Qx0=Qx0, Qy0=Qy0, dq=par.dq, n=par.qn, m=par.qm)
        if par.pole_mitigation == "rofs":
            vfunc2 = hydrogen2d.VHAtom2(
                Qx0=Qx0, Qy0=Qy0, dq=par.dq, r0=0, Z=1, eps=par.eps
            )
        else:
            vfunc2 = hydrogen2d.VHAtom2(
                Qx0=Qx0,
                Qy0=Qy0,
                dq=par.dq,
                r0=psifunc2.r0_for_pole(par.pole_mitigation, par.eps),
                Z=1,
            )
        rd = sdbound.RunData()
        self._rd = rd
        rd.set_h(self._En)
        rd.set_t(par.total_time)
        rd.set_N(int(par.total_time / par.dt))
        self._st = cu_suzuki_trotter2.SuzukiTrotter2(
            par, self._datadir, psifunc2=psifunc2, vfunc2=vfunc2, run_data=rd
        )

    def _analyze_data(self, trotter_order):
        # observed error
        rd = self._rd
        par = self._par
        xi = sdbound.sderror(rd)
        logger.info(
            f"trotter_order: {par.trotter_order}, trotter_steps: {rd.N}, total_time: {rd.t}"
        )
        logger.info(f"Observed error: {xi}")
        psi0_rs_norm = numpy.linalg.norm(rd.psi0_rs)
        psi0_ks_norm = numpy.linalg.norm(rd.psi0_ks)
        logger.info(f"|psi0_rs| = {psi0_rs_norm}, |psi0_ks| = {psi0_ks_norm}")
        # Search for minimum predicted bound. sbound1 and sbound2a will return a
        # bound for rd and alpha alpha is known to have a minimum. The location
        # is not known but there is a single minimum. We assume that the minimum
        # is located at alhpa > 0.1. We search for the alpha that gives the
        # mininum. We search for either sbound1 or sbound2a depending on the
        # trotter order. we move the value of alpha up from 0.1 and see if the
        # bound is decreasing. If the bound starts to increase, we stop and take
        # the minimum value as the bound.
        bdmin = 1e10
        alpha = 0.1
        ratio = 10**(1/4)
        count = 0
        while True:
            N = par.total_time / par.dt
            if trotter_order == 1:
                bound = sdbound.sdbound1(rd, alpha)
            elif trotter_order == 2:
                bound = sdbound.sdbound2a(rd, alpha)
            else:
                raise ValueError("trotter_order must be 1 or 2")
            if bound < bdmin:
                bdmin = bound
            else:
                break
            alpha *= ratio
            count += 1
        logger.info(f"minimum found at alpha: {alpha}, count: {count}, bdmin: {bdmin}")
        return (xi, bdmin)
    
    def save_fig(self):
        nT=self._nT
        xi1=self._xi[0]
        bd1=self._bd[0]
        xi2=self._xi[1]
        bd2=self._bd[1]
        ymin=self._ymin
        ymax=self._ymax
        xmin=self._nT[0]/2
        xmax=self._nT[len(self._nT)-1]*2
        nTpmin = 2**(self._nb+2)*self._t/(self._L*math.pi)
        nTkmin = 2**(2*self._nb)*math.pi*self._t/(self._L**2)

        fig, ax = plt.subplots(1, 1, figsize=(4,4), layout="constrained", dpi=300)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.grid(True)
        ax.set_title(f"$\\xi_N$ vs $B_N$ ($\\Psi^{{\\mathrm{{2D}} }}_{{ {self._qn},{self._qm}}}$ {self._nb}bits, t={self._t} a.u.)")
        ax.set_xlabel("$n_T$ (trotter rounds)")
        ax.set_ylabel("err")
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(ymin, ymax)
        ax.plot(nT, bd1, marker=".", label="$B_N^{(1)}$", color="blue")
        ax.plot(nT, bd2, marker="+", label="$B_N^{(2)}$", color="orange", linestyle="dashed")
        ax.plot(nT, xi1, marker="o", label="$\\xi_N^{(1)}$", color="blue")
        ax.plot(nT, xi2, marker="*", label="$\\xi_N^{(2)}$", color="orange", linestyle="dashed")
        ax.vlines([nTpmin], ymin=ymin, ymax=ymax, colors="g", label="$n_{Tp,\\mathrm{min}}$", linestyles="dashed")
        ax.vlines([nTkmin], ymin=ymin, ymax=ymax, colors="r", label="$n_{Tk,\\mathrm{min}}$")
        ax.legend(loc="upper right")
        filename = f"{self._outdir}/trotter_err_n{self._qn}_m{self._qm}_{self._nb}b_t{self._t}.png"
        fig.savefig(filename)
        plt.show()
    
    @property
    def nT(self):
        return self._nT

    @property
    def dt(self):
        return self._dt

    @property
    def xi1(self):
        return self._xi[0]

    @property
    def xi2(self):
        return self._xi[1]

    @property
    def bd1(self):
        return self._bd[0]

    @property
    def bd2(self):
        return self._bd[1]
