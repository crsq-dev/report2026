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

from crsq.reports import H1D2Report
from crsq.error import sdbound


class SuzukiTrotter2:
    """
    Suzuki-Trotter integrator (2D model).
    """

    def __init__(
        self,
        par: params.Params,
        basedir: str,
        psifunc2: Callable[[float, float], complex],
        vfunc2: Callable[[float, float], float] = None,
        run_data: sdbound.RunData = None
    ):
        cupy.set_printoptions(precision=3)
        self._par = par
        self._basedir = basedir
        self._psifunc2 = psifunc2
        self._vfunc2 = vfunc2
        self._run_data = run_data
        self._colormap_name = "cmr.guppy"
        sx = par.psixmax
        self._zmin = 0
        self._zmax = sx
        self._vmin = -sx
        self._vmax = sx
        sk = par.psikmax
        self._kzmin = 0
        self._kzmax = sk
        self._kvmin = -sk
        self._kvmax = sk
        M = par.M
        logger.info("n1 = %d", par.n1)
        logger.info("signed = %s", par._signed)
        logger.info("L = %f", par.L)
        logger.info("dq = %f", par.dq)
        logger.info("dt = %f", par.dt)
        logger.info("psifunc2 = %s", psifunc2.label)
        self._E = psifunc2.eigen_value
        logger.info("Energy eigen value = %f", self._E)
        cycle_time = -2 * math.pi / self._E
        logger.info("cycle_time = %f", cycle_time)
        logger.info("pole mitigation = %s", par.pole_mitigation)
        logger.info("eps = %f", par.eps)
        # discretized coordinate values
        if par.signed:
            iq = cupy.mod(cupy.linspace(-M // 2, M // 2 - 1, M), M) - (M // 2)
        else:
            iq = cupy.linspace(0, M - 1, M)
        self._xq, self._yq = cupy.meshgrid(iq, iq)
        dq = par.dq
        self._x = self._xq * dq
        self._y = self._yq * dq
        # discretized wave number values
        kq = cupy.mod(cupy.linspace(-M // 2, M // 2 - 1, M), M) - (M // 2)
        kq2 = cupy.square(kq)
        self._kxv2, self._kyv2 = cupy.meshgrid(kq2, kq2)
        self._kv2 = self._kxv2 + self._kyv2
        # value of psi
        np_x = cupy.asnumpy(self._x)
        logger.info("np_x[0] = %s", str(np_x[0]))
        np_y = cupy.asnumpy(self._y)
        np_psi0 = dq * psifunc2(np_x, np_y)
        logger.info("np_psi0[0] = %s", str(np_psi0[0]))
        psi0 = cupy.asarray(np_psi0)
        norm = math.sqrt(cupy.sum(cupy.square(cupy.abs(psi0))))
        logger.info("sqrt(Σ|ψ|**2) = %f should be 1.0", norm)
        # normalize np_psi0
        psi0 = psi0 / norm
        self._psi5q = psi0
        # value of V
        if vfunc2 is not None:
            self._varray = vfunc2(self._x, self._y)
        else:
            self._varray = cupy.zeros((par.M, par.M))
        # value of exp(-iVδt)
        self._expvdt = cupy.exp(-1j * par.dt * self._varray)
        self._expvdthalf = cupy.exp(-1j * par.dt / 2 * self._varray)
        theta00=self._varray[0,0]
        logger.info("varray at center: (%f,%f)", theta00.real, theta00.imag )
        # value of T(k)
        dp = 2 * math.pi / par.L
        me = 1
        self._pv2 = self._kv2 * (dp * dp)
        self._tarray = self._pv2 / (2 * me)
        # value of exp(-iTδt)
        self._exptdt = cupy.exp(-1j * par.dt * self._tarray)

        T_total = par.total_time
        T_interval = par.interval_time
        self.num_elec_iters = int(T_interval / par.dt + 0.5)
        self.num_nucl_iters = int(T_total / T_interval + 0.5)

        if self._run_data is not None:
            rd = self._run_data
            rd.set_psi0_rs(np_psi0)
            psi0p = fft.fft2(psi0, norm="ortho")
            rd.set_psi0_ks(cupy.asnumpy(psi0p))
            rd.set_dh1_rs(cupy.asnumpy(self._varray))
            rd.set_dh2_ks(cupy.asnumpy(self._tarray))

    def _do_step_to1(self):
        # logger.info("SuzukiTrotter._do_step_to1 V, T")
        self._psi1q = self._psi5q
        self._apply_v() # psi1q -> psi2q
        self._apply_t() # psi2q -> psi3p -> psi4p -> psi5q
    
    def _do_step_to2a(self):
        # logger.info("SuzukiTrotter._do_step_to2a V/2, T")
        self._psi1q = self._psi5q
        self._apply_vhalf()
        self._apply_t()

    def _do_step_to2b(self):
        # logger.info("SuzukiTrotter._do_step_to2b V/2")
        self._psi1q = self._psi5q
        self._apply_vhalf()
        self._psi5q = self._psi2q

    def _apply_v(self):
        self._psi2q = self._expvdt * self._psi1q
    
    def _apply_vhalf(self):
        self._psi2q = self._expvdthalf * self._psi1q

    def _apply_t(self):
        self._psi3p = fft.fft2(self._psi2q, norm="ortho")
        self._psi4p = self._exptdt * self._psi3p
        self._psi5q = fft.ifft2(self._psi4p, norm="ortho")

    def run_simulation(self):
        par = self._par
        title = f"H 2D classical L={par.L} n={par.qn} m={par.qm} nb={par.n1} dt{par.dt}"
        T_interval = par.interval_time
        self._report = H1D2Report(
            outdir=self._basedir,
            plot_type=par.plot_type,
            title=title,
            psifunc_label=self._psifunc2.label,
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
            hp_func=self._vfunc2,
            delta_t=par.dt,
            num_elec_iters=self.num_elec_iters,
            num_nucl_iters=self.num_nucl_iters,
            colormap_name=self._colormap_name,
            signed=par.signed
        )
        par = self._par
        # record the initial p and q
        psi1q_0 = self._psi5q
        np_psi1q_0 = cupy.asnumpy(psi1q_0)
        self._report.add_data_sample("q", 0, np_psi1q_0)
        np_psi3p_0 = cupy.asnumpy(fft.fft2(psi1q_0, norm="ortho"))
        self._report.add_data_sample("p", 0, np_psi3p_0)

        for nucl_it in range(self.num_nucl_iters):
            t = T_interval * nucl_it
            if par.trotter_order == 1:
                for _elec_it in range(self.num_elec_iters):
                    self._do_step_to1()
            else:
                self._do_step_to2a()
                if par.save_psi2:
                    np_psi1_q = cupy.asnumpy(self._psi1q)
                    np_psi2_q = cupy.asnumpy(self._psi2q)
                    self._report.add_data_sample("qrom0", t, np_psi1_q)
                    self._report.add_data_sample("qrom1", t, np_psi2_q)
                for _elec_it in range(self.num_elec_iters - 1):
                    self._do_step_to1()
                self._do_step_to2b()
            t = T_interval * (nucl_it+1)
            np_psi_q = cupy.asnumpy(self._psi5q)
            np_psi_p = cupy.asnumpy(self._psi4p)
            self._report.add_data_sample("q", t, np_psi_q)
            self._report.add_data_sample("p", t, np_psi_p)
            if par.save_psi2:
                np_psi1_q = cupy.asnumpy(self._psi1q)
                np_psi2_q = cupy.asnumpy(self._psi2q)
                self._report.add_data_sample("qrom0", t, np_psi1_q)
                self._report.add_data_sample("qrom1", t, np_psi2_q)
        if self._run_data is not None:
            rd = self._run_data
            rd.set_psin_rs(cupy.asnumpy(self._psi5q))
            rd.set_psin_ks(cupy.asnumpy(self._psi4p))

    def set_color_map(self, colormap_name: str):
        self._colormap_name = colormap_name

    def set_zlim(self, zmin: float, zmax: float):
        self._zmin = zmin
        self._zmax = zmax

    def set_vlim(self, vmin: float, vmax: float):
        self._vmin = vmin
        self._vmax = vmax

    def generate_animation_frames(self):
        par = self._par
        T_interval = par.interval_time

        self._report.open_report(clean=par.clean_report_dir)
        psi_q0 = None
        for nucl_it in range(self.num_nucl_iters + 1):
            t = T_interval * nucl_it
            psi_q = self._report.read_data_sample("q", t)
            if psi_q0 is None:
                psi_q0 = psi_q # save initial wave function for autocorrelation
            psi_p = self._report.read_data_sample("p", t)
            self._report.produce_frame(t, psi_q, psi_p)
            self._report.record_energy(t, psi_q, psi_p, psi_q0)
        self._report.generate_report()

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
