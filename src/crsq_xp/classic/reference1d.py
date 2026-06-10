from typing import Callable, Dict
import cupy
import math, cmath
import logging
from .params import Params
from crsq.reports import H1D1Report, H1D2Report

logger = logging.getLogger("crsq_xp.classic")


class Analytic1D:
    def __init__(self, par: Params, basedir: str, psifunc: Callable[[float], complex]):
        self._par = par
        self._basedir = basedir
        self._psifunc = psifunc
        M = par.M
        if par._signed:
            self._xv = cupy.concatenate(
                [
                    cupy.linspace(0, M // 2 - 1, M // 2),
                    cupy.linspace(-M // 2, -1, M // 2),
                ]
            )
        else:
            self._xv = cupy.linspace(0, M - 1, M)
        # discretized wave number values
        self._kv = cupy.concatenate(
            [cupy.linspace(0, M // 2 - 1, M // 2), cupy.linspace(-M // 2, -1, M // 2)]
        )
        # value of q
        logger.info("dq = %f", par.dq)
        self._qv = self._xv * par.dq
        self._psifunc = psifunc
        self._E = psifunc.eigen_value
        logger.info("Energy eigen value = %f", self._E)
        cycle_time = -2 * math.pi / self._E
        logger.info("cycle_time = %f", cycle_time)
        rootdq = math.sqrt(par.dq)
        logger.info("rootdq = %f", rootdq)
        # value of initial wave function
        npqv = cupy.asnumpy(self._qv)
        np_psi0 = rootdq * psifunc(npqv)
        psi0 = cupy.asarray(np_psi0)
        norm = math.sqrt(cupy.sum(cupy.square(cupy.abs(psi0))))
        logger.info(f"sqrt(Σ|ψ|^2) = {norm} should be 1.0")
        # normalize psi0
        psi0 = psi0 / norm
        self._psi0 = psi0
        title = f"H 1D analytic L={par.L} n=1 nb={par.n1} dt={par.dt}"
        T_total = par.total_time
        T_interval = par.interval_time
        self.num_elec_iters = int(T_interval / par.dt + 0.5)
        self.num_nucl_iters = int(T_total / T_interval + 0.5)
        self._report = H1D1Report(
            outdir=self._basedir,
            title=title,
            psifunc_label=self._psifunc.label,
            num_coordinate_bits=par.n1,
            psi_axis_scale=par.psixmax,
            space_length=par.L,
            window_radius=par.WM,
            hp_func=self.hp_func,
            delta_t=par.dt,
            num_elec_iters=self.num_elec_iters,
            num_nucl_iters=self.num_nucl_iters,
            signed=par._signed,
            dpi=par.dpi
        )

    def hp_func(self, q: float) -> float:
        x0 = self._par.x0
        dq = self._par.dq
        r = cupy.abs(q - x0)
        if r == 0:
            invr = 2 / dq
        else:
            invr = 1 / r
        return -1 * invr

    def _do_step(self, t: float):
        time_shift = cmath.exp(-1j * self._E * t)
        logger.info("time_shift(%f) = %f", t, abs(time_shift))
        self._psiq = time_shift * self._psi0
        self._psip = cupy.fft.fft(self._psiq, norm="ortho")

    def run_calculation(self):
        par = self._par
        T_interval = par.interval_time
        t = 0
        for _nucl_it in range(self.num_nucl_iters + 1):
            self._do_step(t)
            self._add_psi_to_report(t, self._psiq, self._psip)
            t += T_interval

    def _add_psi_to_report(self, t: float, psi_q, psi_p):
        svdim = self._par.M  # dimension of the state vector
        self._report.add_q_state_vector_file(t, svdim, psi_q)
        self._report.add_p_state_vector_file(t, svdim, psi_p)

    def generate_animation_frames(self):
        par = self._par
        T_interval = par.interval_time

        self._report.open_report()
        # t = 0 は画像フレームは作るがenergyは記録しない
        t = 0
        for _nucl_it in range(self.num_nucl_iters + 1):
            bit_range = (0, self._par.n1)
            psi_q = self._report.read_q_state_vector_file(t, bit_range)
            psi_p = self._report.read_p_state_vector_file(t, bit_range)
            self._report.add_wave_function_plot(t, psi_q, psi_p)
            if t > 0:
                self._report.record_energy(t, psi_q, psi_p)
            t += T_interval
        self._report.generate_report()

