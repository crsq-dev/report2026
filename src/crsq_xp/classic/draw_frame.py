from typing import Callable
import crsq_xp.classic.params as params
from crsq.reports import H1D1Report, H1D2Report
import cupy

class DrawFrame1d:
    def __init__(
        self,
        par: params.Params,
        basedir: str,
        psifunc: Callable[[float], complex],
        vfunc: Callable[[float], float]
    ):
        self._par = par
        self._basedir = basedir
        self._psifunc = psifunc
        self._vfunc = vfunc
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
        T_total = par.total_time
        T_interval = par.interval_time
        self.num_elec_iters = int(T_interval / par.dt + 0.5)
        self.num_nucl_iters = int(T_total / T_interval + 0.5)

    def hp_func(self, q: float) -> float:
        x0 = self._par.x0
        dq = self._par.dq
        r = cupy.abs(q - x0)
        if r == 0:
            invr = 2 / dq
        else:
            invr = 1 / r
        return -1 * invr

    def draw_frame(self, t: float):
        """draw a single frame."""
        par = self._par
        title = f"H 1D classical L={par.L} n={par.qn} m={par.qm} dt{par.dt}"
        self._report = H1D1Report(
            outdir=self._basedir,
            plot_type=par.plot_type,
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
            signed=par.signed
        )

        self._report.open_report(clean=False)
        bit_range = (0, self._par.n1)
        psi_q = self._report.read_q_state_vector_file(t, bit_range)
        psi_p = self._report.read_p_state_vector_file(t, bit_range)
        self._report.draw_single_frame(t, psi_q, psi_p)

class DrawFrame2d:
    def __init__(
        self,
        par: params.Params,
        basedir: str,
        psifunc2: Callable[[float, float], complex],
        vfunc2: Callable[[float, float], float]
    ):
        self._par = par
        self._basedir = basedir
        self._psifunc2 = psifunc2
        self._vfunc2 = vfunc2
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
        T_total = par.total_time
        T_interval = par.interval_time
        self.num_elec_iters = int(T_interval / par.dt + 0.5)
        self.num_nucl_iters = int(T_total / T_interval + 0.5)

    def draw_frame(self, t: float):
        """draw a single frame."""
        par = self._par
        title = f"H 2D classical L={par.L} n={par.qn} m={par.qm} nb={par.n1} dt{par.dt}"
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
            signed=par.signed,
            dpi=par.dpi
        )

        self._report.open_report(clean=False)

        psi_q = self._report.read_data_sample("q", t)
        psi_p = self._report.read_data_sample("p", t)
        self._report.produce_frame(t, psi_q, psi_p)

        # report.generate_report() is not called.

