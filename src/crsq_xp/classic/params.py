"""
params
"""

import math


class Params:
    """parameters for wave function integration
            :param n1: number of bits for each dimension
            :param dimension: dimension of the system
            :param L: length of the system
            :param psixmax: max value of the wave function x
            :param psikmax: max value of the wave function k
            :param dt: time step
            :param interval_time: interval time for saving data
            :param total_time: total time for simulation
            :param signed: whether to use signed coordinates
            :param trotter_order: order of the Trotter decomposition
            :param WM: window radius in momentum space
            :param x0: initial x coordinate of the wave function center
            :param y0: initial y coordinate of the wave function center
            :param z0: initial z coordinate of the wave function center
            :param qn: principal quantum number for the initial wave function
            :param ql: azimuthal quantum number for the initial wave function
            :param qm: magnetic quantum number for the initial wave function
            :param pole_mitigation: method for pole mitigation in the potential
            :param eps: epsilon parameter for pole mitigation
            :param plot_type: type of plot for visualization ("2d" or "3d")
            :param clean_report_dir: whether to clean the report directory before running the simulation
            :param use_saved_data: whether to use saved data if available
            :param use_fixed_point: whether to use fixed point arithmetic for the wave function
            :param save_psi2: whether to save the wave function after applying the potential operator
            :param frac_bits: number of fractional bits for fixed point representation (if use_fixed_point is True)
            :param dpi: DPI for figures. specify None for default.
    """

    def __init__(
        self,
        n1: int,
        dimension: int,
        L: float,
        psixmax: float,
        psikmax: float,
        dt: float,
        interval_time: float,
        total_time: float,
        signed: bool,
        trotter_order: int,
        WM: float,
        x0: float = 0,
        y0: float = 0,
        z0: float = 0,
        qn: int = 0,
        ql: int = 0,
        qm: int = 0,
        pole_mitigation: str = "r0lim",
        eps: float = 0,
        plot_type: str="3d",
        clean_report_dir: bool = False,
        use_saved_data: bool = False,
        use_fixed_point: bool = False,
        save_psi2: bool = False,
        frac_bits: int = -1,
        dpi: int|None = None
        ):
        self._n1 = n1
        self._frac_bits = frac_bits
        self._dimension = dimension
        self._L = L
        self._psixmax = psixmax
        self._psikmax = psikmax
        self._x0 = x0
        self._y0 = y0
        self._z0 = z0
        self._dt = dt
        self._interval_time = interval_time
        self._total_time = total_time
        self._signed = signed
        self._n = n1 * dimension
        M = 1 << n1
        self._M = M
        dq = L / M
        self._dq = dq
        self._dp = 2 * math.pi / L
        self._trotter_order = trotter_order
        self._WM = WM
        self._qn = qn
        self._ql = ql
        self._qm = qm
        self._pole_mitigation = pole_mitigation
        self._eps = eps
        self._plot_type = plot_type
        self._clean_report_dir = clean_report_dir
        self._use_saved_data = use_saved_data
        self._use_fixed_point = use_fixed_point
        self._save_psi2 = save_psi2
        self._dpi = dpi

    @property
    def n1(self):
        return self._n1

    @property
    def frac_bits(self):
        return self._frac_bits

    @property
    def qn(self):
        return self._qn
    
    @property
    def ql(self):
        return self._ql

    @property
    def qm(self):
        return self._qm
    
    @property
    def pole_mitigation(self):
        return self._pole_mitigation

    @property
    def eps(self) -> float:
        return self._eps

    @property
    def dimension(self):
        return self._dimension

    @property
    def L(self):
        return self._L
    
    @property
    def psixmax(self):
        return self._psixmax
    
    @property
    def psikmax(self):
        return self._psikmax
    
    @property
    def x0(self):
        return self._x0
    
    @property
    def y0(self):
        return self._y0

    @property
    def dq(self):
        return self._dq

    @property
    def dp(self):
        return self._dp

    @property
    def dt(self):
        return self._dt

    @property
    def total_time(self):
        return self._total_time
    
    @property
    def interval_time(self):
        return self._interval_time

    @property
    def M(self) -> int:
        return self._M

    @property
    def WM(self) -> int:
        return self._WM

    @property
    def trotter_order(self) -> int:
        return self._trotter_order

    @property
    def signed(self) -> bool:
        return self._signed
    
    @property
    def plot_type(self) -> str:
        return self._plot_type
    
    @property
    def clean_report_dir(self) -> bool:
        return self._clean_report_dir
    
    @property
    def use_saved_data(self) -> bool:
        return self._use_saved_data
    
    @property
    def use_fixed_point(self) -> bool:
        return self._use_fixed_point
    
    @property
    def save_psi2(self) -> bool:
        return self._save_psi2

    @property
    def dpi(self):
        return self._dpi
