from typing import Callable, Dict
import cupy
import math, cmath
import logging

from crsq.reports.h1d2report import H1D2Report
from .params import Params
from crsq.reports import H1D3Report

logger = logging.getLogger("crsq_xp.classic")

class Analytic3D:
    def __init__(
        self,
        par: Params,
        basedir: str,
        psifunc3: Callable[[float, float, float], complex],
        vfunc3: Dict[str, Callable[[float, float, float], float]],
    ):
        self._par = par
        self._basedir = basedir
        self._psifunc3 = psifunc3
        self._vfunc3 = vfunc3
        # self._plot_type = "3d-3"
        self._colormap_name = "cmr.guppy"
        # self._colormap_name = "cmr.redshift"
        s = par.psixmax
        self._zmin = 0
        self._zmax = s
        self._vmin = -s
        self._vmax = s
        km = par.psikmax
        self._kzmin = 0
        self._kzmax = km
        self._kvmin = -km
        self._kvmax = km
        self._E = psifunc3.eigen_value
        logger.info("energy eigen value = %f", self._E)
        cycle_time = -2 * math.pi / self._E
        logger.info("cycle_time = %f", cycle_time)
        rootdq = math.sqrt(par.dq)
        logger.info("rootdq = %f", rootdq)
        # value of initial wave function
        M = par.M
        # discretized coordinate values
        if par.signed:
            iq = cupy.mod(cupy.linspace(-M // 2, M // 2 - 1, M), M) - (M // 2)
        else:
            iq = cupy.linspace(0, M - 1, M)
        self._xq = iq[:, None, None]
        self._yq = iq[None, :, None]
        self._zq = iq[None, None, :]

        dq = par.dq
        self._x = self._xq * dq
        self._y = self._yq * dq
        self._z = self._zq * dq
        # discretized wave number values

        kq = cupy.mod(cupy.linspace(-M // 2, M // 2 - 1, M), M) - (M // 2)
        kq2 = cupy.square(kq)
        self._kxv2 = kq2[:, None, None]
        self._kyv2 = kq2[None, :, None]
        self._kzv2 = kq2[None, None, :]
        
        self._kv2 = self._kxv2 + self._kyv2 + self._kzv2
        np_x = cupy.asnumpy(self._x)
        np_y = cupy.asnumpy(self._y)
        np_z = cupy.asnumpy(self._z)
        np_psi0 = math.pow(dq,3/2) * psifunc3(np_x, np_y, np_z)
        psi0 = cupy.asarray(np_psi0)
        norm = math.sqrt(cupy.sum(cupy.square(cupy.abs(psi0))))
        logger.info("sqrt(Σ|ψ|^2) = %f should be 1.0", norm)
        # normalize psi0
        psi0 = psi0 / norm
        self._psi0 = psi0

    def _shift_phase(self, t: float):
        phase_shift = -1j * self._E * t
        operator = cmath.exp(-1j * self._E * t)
        logger.info("phase_shift(%f) = %f", t, abs(phase_shift))
        self._psiq = operator * self._psi0
        self._psip = cupy.fft.fftn(self._psiq, norm="ortho")

    def run_calculation(self):
        par = self._par
        title = f"H 3D analytic L={par.L} n={par.qn} l={par.ql} m={par.qm} nb={par.n1} dt={par.dt}"
        T_total = par.total_time
        T_interval = par.interval_time
        self.num_elec_iters = int(T_interval / par.dt + 0.5)
        self.num_nucl_iters = int(T_total / T_interval + 0.5)
        self._report = H1D3Report(
            outdir=self._basedir,
            plot_type=par.plot_type,
            title=title,
            psifunc_label=self._psifunc3.label,
            num_coordinate_bits=par.n1,
            zmin=self._zmin,
            zmax=self._zmax,
            vmin=self._vmin,
            vmax=self._vmax,
            kzmin=self._kzmin,
            kzmax=self._kzmax,
            kvmin=self._kvmin,
            kvmax=self._kvmax,
            space_length=par.L,
            hp_func=self._vfunc3,
            delta_t=par.dt,
            num_elec_iters=self.num_elec_iters,
            num_nucl_iters=self.num_nucl_iters,
            colormap_name=self._colormap_name,
            signed=par._signed
        )
        if par.use_saved_data:
            return
        for nucl_it in range(self.num_nucl_iters+1):
            t = nucl_it * T_interval
            self._shift_phase(t)
            np_psi_q0 = cupy.asnumpy(self._psi0)
            np_psi_q = cupy.asnumpy(self._psiq)
            np_psi_p = cupy.asnumpy(self._psip)
            self._report.add_data_sample("q", t, np_psi_q)
            self._report.add_data_sample("p", t, np_psi_p)
            self._report.record_energy(t, np_psi_q, np_psi_p, np_psi_q0)

    def generate_animation_frames(self):
        par = self._par
        T_interval = par.interval_time

        self._report.open_report(clean=par.clean_report_dir)
        psi_q0 = None
        for nucl_it in range(self.num_nucl_iters + 1):
            t = T_interval * nucl_it
            psi_q = self._report.read_data_sample("q", t)
            psi_p = self._report.read_data_sample("p", t)
            if psi_q0 is None:
                psi_q0 = psi_q  # save initial wave function for autocorrelation
            self._report.produce_frame(t, psi_q, psi_p)
            t += T_interval
        self._report.generate_report()
