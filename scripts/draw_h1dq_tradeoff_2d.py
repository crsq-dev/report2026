import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from typing import Tuple
import pandas as pd

import cupy
import numpy
import os, argparse, logging, math

logger = logging.getLogger("crsq-explore.scripts")

def find_y_for(xs: list[float], ys: list[float], x):
    # return y for x on the curve (xs[i], ys[i])
    # using linear interpolation
    # assume xs is sorted
    for i in range(1, len(xs)):
        if xs[i] >= x:
            x0 = xs[i-1]
            x1 = xs[i]
            y0 = ys[i-1]
            y1 = ys[i]
            # linear interpolation
            y = y0 + (y1 - y0) * (x - x0) / (x1 - x0)
            return y
    return None    

def psi2d_0_0(x,y):
    r = numpy.sqrt(x*x+y*y)
    return math.sqrt(8/math.pi)*numpy.exp(-2*r)

def psi2d_1_0(x,y):
    r = numpy.sqrt(x*x+y*y)
    return math.sqrt(8/(27*math.pi))*(1-(4/3)*r)*numpy.exp(-(2/3)*r)

def psi2d_1_1(x,y):
    r = numpy.sqrt(x*x+y*y)
    cr = x + 1j*y
    psi = (8/(9*math.sqrt(3*math.pi)))*cr*numpy.exp(-(2/3)*r)
    # psi = (8/(9*math.sqrt(3*math.pi)))*r*numpy.exp(-(2/3)*r)
    return psi

class EvalDq2d:
    def __init__(self, psi2d, dq0, outdir, labels, suffix, scale=0.01):
        self._psi2d = psi2d
        self._dq0 = dq0
        self._outdir = outdir
        os.makedirs(outdir, exist_ok=True)
        self._labels = labels
        self._suffix = suffix
        self._scale = scale
        fig, axs = plt.subplots(1, 3, figsize=(15, 4), layout='constrained')
        fig.suptitle(f"2D δr analysis for Ψ2D_{suffix}")
        axs[0].set_title(f"({self._labels[0]}) Re(Ψ2D_{suffix}(x,0))")
        axs[1].set_title(f"({self._labels[1]}) |Sd-S1| and S2")
        axs[2].set_title(f"({self._labels[2]}) |Sd-S1| + S2")
        self._df = pd.DataFrame()
        self._fig = fig
        self._axs = axs
        self._colors = ['blue', 'orange', 'green', 'red']
    
    def calcS(self, L, m):
        dq = L / m
        q = numpy.linspace(-L/2, L/2-dq, m)
        x, y = numpy.meshgrid(q, q)
        psi = self._psi2d(x,y)
        psidag= numpy.conjugate(psi)
        s = numpy.sum(numpy.real(psi*psidag))*dq*dq
        return s

    def evalOneL(self, L: float, M: int):
        """ L: length
            nb: bits per coordinate
        """
        Sd = self.calcS(L, M)
        S1 = self.calcS(L, M*16)
        S2 = 1 - S1
        print(f"evalOneL: L={L:.2f}, M={M}, Sd={Sd:.6f}, S1={S1:.6f}, S2={S2:.6f}")
        Err1 = numpy.abs(Sd-S1)
        Err2 = S2
        return (Err1, Err2)

    def drawS1S2(self, ax: Axes, nb, col, npqd, nperr1, nperr2):
        ax.set_xlabel("δr")
        ax.set_ylim(0, self._scale)
        ax.grid(True)
        ax.plot(npqd, nperr1, color=col, label=f"nb={nb}, |Sd-S1|", marker="o")
        ax.plot(npqd, nperr2, color=col, label=f"nb={nb}, S2", marker="x")
        ax.legend()
        self._df[f"δr"] = npqd
        self._df[f"S1Sd({nb})"] = nperr1

    def drawSsum(self, ax: Axes, nb, col, npdq, nperr1, nperr2, dr):
        ax.set_xlabel("δr")
        ax.set_ylim(0, self._scale)
        sdiff = nperr1 + nperr2
        ax.plot(npdq, sdiff, color=col, label=f"nb={nb}, |Sd-S1|+S2")
        # plot the point that will be used as minimum
        y = find_y_for(npdq, sdiff, dr)
        ax.plot(dr, y, color=col, marker="o")
        ax.legend()
        ax.grid(True)
        self._df[f"Sdiff({nb})"] = sdiff
    
    def drawPsi(self, xr, yr, sr, nbs):
        ax: Axes = self._axs[0]
        ax.set_xlabel("x")
        x = numpy.linspace(xr[0], xr[1], 201)
        ax.set_ylim(yr[0], yr[1])
        ax.grid(True)
        psi_vals = numpy.real(self._psi2d(x, 0))
        ax.plot(x, psi_vals, label=f"Re(Ψ2D_{self._suffix}(x,0))")
        for s,nb,col in zip(sr, nbs, self._colors):
            # put vertical line at x = +- s
            L = s * (1 << nb)
            HL=L/2
            ax.axvline(x= HL, color=col, label=f"nb={nb}, x=\u00b1{HL:.1f}")
            ax.axvline(x=-HL, color=col)
        ax.legend()

    def evalLRange(self, nb):
        """ eval L range.
            nb: bits per coordinate
        """
        M = 1 << nb
        # step ratio for increasing L. step_ratio**10 = 10.
        scales = numpy.geomspace(1, 40, 40)
        dqList= []
        err1List = []
        err2List = []
        for scale in scales:
            dq = self._dq0 * scale
            L = dq * M
            err1, err2 = self.evalOneL(L, M)
            dqList.append(dq)
            err1List.append(err1)
            err2List.append(err2)
        npdq = numpy.array(dqList)
        nperr1 = numpy.array(err1List)
        nperr2 = numpy.array(err2List)
        return (npdq, nperr1, nperr2)

    def evalAndDraw(self, nb, col, dr):
        dq, err1, err2 = self.evalLRange(nb)
        ax = self._axs[1]
        self.drawS1S2(ax, nb, col, dq, err1, err2)
        ax = self._axs[2]
        self.drawSsum(ax, nb, col, dq, err1, err2, dr)

    def plot(self):
        fig = self._fig
        fig.savefig(f"{outdir}/eval2d_dq_geom_{self._suffix}.png", dpi=300)
        self._df.to_csv(f"{outdir}/eval2d_geom_{self._suffix}.csv")

OUTDIR1="onedrive.lnk/dq_tradeoff"
OUTDIR2="onedrive.lnk/dq_tradeoff2"

LABELSB1 = ["B1", "B2", "B3"]
LABELSB2 = ["d", "e", "f"]

LABELSC1 = ["C1", "C2", "C3"]
LABELSC2 = ["g", "h", "i"]

LABELSD1 = ["D1", "D2", "D3"]
LABELSD2 = ["j", "k", "l"]


for labels, outdir in zip([LABELSB1, LABELSB2], [OUTDIR1, OUTDIR2]):
    evaldq2d00 = EvalDq2d(psi2d_0_0, 0.01, outdir, labels, "0_0", 0.02)
    drs = [0.078, 0.039, 0.0234, 0.0137]
    evaldq2d00.drawPsi([-5,5], [-0.5, 2.0], drs, range(6,10))
    for nb, col, dr in zip(range(6, 10), evaldq2d00._colors, drs):
        evaldq2d00.evalAndDraw(nb, col, dr)
    evaldq2d00.plot()


for labels, outdir in zip([LABELSC1, LABELSC2], [OUTDIR1, OUTDIR2]):
    evaldq2d10 = EvalDq2d(psi2d_1_0, 0.01, outdir, labels, "1_0", 0.02)
    drs = [0.30, 0.164, 0.0937, 0.0527]
    evaldq2d10.drawPsi([-20,20],[-0.2, 0.4], drs, range(6,10))
    for nb, col, dr in zip(range(6, 10), evaldq2d10._colors, drs):
        evaldq2d10.evalAndDraw(nb, col, dr)
    evaldq2d10.plot()

for labels, outdir in zip([LABELSD1, LABELSD2], [OUTDIR1, OUTDIR2]):
    evaldq2d11 = EvalDq2d(psi2d_1_1, 0.02, outdir, labels, "1_1", 0.005)
    drs = [0.39, 0.234, 0.133, 0.076]
    evaldq2d11.drawPsi([-20,20],[-0.3, 0.3], drs, range(6,10))
    for nb, col, dr in zip(range(6, 10), evaldq2d11._colors, drs):
        evaldq2d11.evalAndDraw(nb, col, dr)
    evaldq2d11.plot()
