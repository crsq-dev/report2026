"""
Suzuki Trotter / split operator wave function integrator
"""

import math
from typing import Callable

import cupy
import cupy.fft as fft

import logging

logger = logging.getLogger("crsq_xp.classic")

from . import params

from crsq.reports import H1D1Report
from crsq.error import sdbound

class SuzukiTrotter1:
    """
    Suzuki-Trotter integrator.
    1D model.
    """

    def __init__(
        self,
        par: params.Params,
        basedir: str,
        psifunc: Callable[[float], complex],
        vfunc: Callable[[float], float] = None
    ):
        self._par = par
        self._basedir = basedir
        self._report_large_psi = True
        self._show_logpsip_frame = True
        self._enable_qspace_evolution = True
        self._enable_pspace_evolution = True
        logger.info("n1 = %d", par.n1)
        logger.info("signed = %s", par._signed)
        logger.info("L = %f", par.L)
        logger.info("WM = %f", par.WM)
        logger.info("dq = %f", par.dq)
        logger.info("dt = %f", par.dt)
        logger.info("qn = %d", par.qn)
        M = par.M
        # window width for p-space plots. wave number range is -WM ~ WM
        # discretized coordinate values
        if par._signed:
            self._xq = cupy.mod(cupy.linspace(-M // 2, M // 2 - 1, M), M) - (M // 2)
        else:
            self._xq = cupy.linspace(0, M - 1, M)
        # discretized wave number values
        self._kv = cupy.concatenate(
            [cupy.linspace(0, M // 2 - 1, M // 2), cupy.linspace(-M // 2, -1, M // 2)]
        )
        # value of q
        logger.info("dq = %f", par.dq)
        self._x = self._xq * par.dq
        self._psifunc = psifunc
        self._E = psifunc.eigen_value
        logger.info("Energy eigen value = %f", self._E)
        cycle_time = -2 * math.pi / self._E
        logger.info("cycle_time = %f", cycle_time)
        rootdq = math.sqrt(par.dq)
        # value of initial wave function
        npqv = cupy.asnumpy(self._x)
        np_psi0 = rootdq * psifunc(npqv)
        psi0 = cupy.asarray(np_psi0)
        norm = math.sqrt(cupy.sum(cupy.square(cupy.abs(psi0))))
        logger.info(f"sqrt(Σ|ψ|^2) = {norm} should be 1.0")
        # normalize psi0
        psi0 = psi0 / norm
        self._psi5q = psi0
        if vfunc is not None:
            # varray は各格子点でのポテンシャルの値
            self._varray = vfunc(self._x)
        else:
            self._varray = cupy.zeros(par.M)
        # value of exp(-iVδt/hbar)
        hbar = 1
        dt = par.dt
        self._expvdt = cupy.exp((-1j * dt / hbar) * self._varray)
        self._expvdthalf = cupy.exp((-1j * dt / (2 * hbar)) * self._varray)
        dtheta_q = (-dt / hbar) * self._varray
        for idx in range(par.M // 2 - 6, par.M // 2 + 6):
            logger.info(
                f"qv[{idx}]={self._x[idx]} psi0_r[{idx}] = {psi0[idx]} varray[{idx}] = {self._varray[idx]} dtheta_q[{idx}]={dtheta_q[idx]}"
            )
        # value of T(k)
        dp = 2 * math.pi / par.L
        logger.info("dp = %f", dp)
        me = 1
        self._pv = self._kv * dp
        self._tarray = cupy.square(self._pv) / (2.0 * me)
        # value of exp(-iTδt/hbar)
        self._exptdt = cupy.exp((-1j * dt / hbar) * self._tarray)
        dtheta_p = (-dt / hbar) * self._tarray
        # check.
        for idx in range(0, 6):
            logger.info(
                f"pv[{idx}]={self._pv[idx]} tarray[{idx}] = {self._tarray[idx]} dtheta_p[{idx}]={dtheta_p[idx]}"
            )
        self._hk_trace = []
        self._hp_trace = []
        self._trace_time = []
        if par.use_fixed_point:
            label = "classic_fixed"
        else:
            label= "classic"
        title = f"H 1D {label} L={par.L} n=1 nb={par.n1} dt={par.dt}"
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
            signed=par._signed
        )

    def _do_1st_step(self):
        self._psi1q = self._psi5q
        self._apply_vhalf()
        self._apply_t()
    
    def _do_last_step(self):
        self._psi1q = self._psi5q
        self._apply_v()
        self._apply_t()
        self._psi1q = self._psi5q
        self._apply_vhalf()
        self._psi5q = self._psi2q

    def _do_step(self):
        self._psi1q = self._psi5q
        self._apply_v()
        self._apply_t()

    def _apply_v(self):
        if self._enable_qspace_evolution:
            self._psi2q = self._expvdt * self._psi1q
        else:
            self._psi2q = self._psi1q

    def _apply_vhalf(self):
        if self._enable_qspace_evolution:
            self._psi2q = self._expvdthalf * self._psi1q
        else:
            self._psi2q = self._psi1q

    def _apply_t(self):
        self._psi3p = fft.fft(self._psi2q, norm="ortho")
        if self._enable_pspace_evolution:
            self._psi4p = self._exptdt * self._psi3p
        else:
            self._psi4p = self._psi3p
        self._psi5q = fft.ifft(self._psi4p, norm="ortho")

    def hp_func(self, q: float) -> float:
        x0 = self._par.x0
        dq = self._par.dq
        r = cupy.abs(q - x0)
        if r == 0:
            invr = 2 / dq
        else:
            invr = 1 / r
        return -1 * invr

    def run_simulation(self):
        par = self._par
        T_interval = par.interval_time
        t = 0
        for _nucl_it in range(self.num_nucl_iters):
            for _elec_it in range(self.num_elec_iters):
                if self._par.trotter_order == 1:
                    self._do_step()
                elif _nucl_it == 0 and _elec_it == 0:
                    self._do_1st_step()
                elif _nucl_it == self.num_nucl_iters - 1 and _elec_it == self.num_elec_iters - 1:
                    self._do_last_step()
                else:
                    self._do_step()
            t += T_interval
            psi_q = cupy.asnumpy(self._psi5q)
            psi_p = cupy.asnumpy(self._psi4p)
            self._add_psi_to_report(t, psi_q, psi_p)

    def _add_psi_to_report(self, t: float, psi_q, psi_p):
        svdim = self._par.M  # dimension of the state vector
        self._report.add_q_state_vector_file(t, svdim, psi_q)
        self._report.add_p_state_vector_file(t, svdim, psi_p)

    def generate_animation_frames(self):
        par = self._par
        T_interval = par.interval_time

        self._report.open_report()
        t = 0
        for _nucl_it in range(self.num_nucl_iters):
            t += T_interval
            bit_range = (0, self._par.n1)
            psi_q = self._report.read_q_state_vector_file(t, bit_range)
            psi_p = self._report.read_p_state_vector_file(t, bit_range)
            self._report.add_wave_function_plot(t, psi_q, psi_p)
            self._report.record_energy(t, psi_q, psi_p)
        self._report.generate_report()

    def print_large_psi_indexes(self, psi_t_psi):
        thresh = 0.2
        s = f"ps_t_psi[i]>{thresh} :"
        for i in range(0, len(psi_t_psi)):
            if psi_t_psi[i] > thresh:
                s += f" {i}({bin(i)})"
        print(s)

    @property
    def qv(self):
        return self._x

    @property
    def psi1q(self):
        return self._psi1q

    @property
    def psi2q(self):
        return self._psi2q

    @property
    def psi3p(self):
        return self._psi3p

    @property
    def psi4p(self):
        return self._psi4p

    @property
    def psi5q(self):
        return self._psi5q
