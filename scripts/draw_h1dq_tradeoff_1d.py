import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from typing import Tuple
import pandas as pd

import cupy
import numpy
import os, argparse, logging, math

logger = logging.getLogger("crsq-explore.scripts")

OUTDIR1="onedrive.lnk/dq_tradeoff"
OUTDIR2="onedrive.lnk/dq_tradeoff2"

LABELS1 = ["(A1)", "(A2)", "(A3)"]
LABELS2 = ["(a)", "(b)", "(c)"]

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

class EvalDq1d:
    def __init__(self, psi1d, labels, outdir):
        self._psi1d = psi1d
        fig, axs = plt.subplots(1, 3, figsize=(15, 4), layout='constrained')
        self._df = pd.DataFrame()
        self._fig = fig
        self._axs = axs
        self._colors = ['blue', 'orange', 'green', 'red']
        self._labels = labels
        self._outdir = outdir
        os.makedirs(outdir, exist_ok=True)
    
    def calcS(self, L, m):
        dq = L / m
        x = numpy.linspace(-L/2, L/2-dq, m)
        psi = self._psi1d(x)
        psidag= numpy.conjugate(psi)
        s = numpy.sum(psi*psidag)*dq
        return s

    def evalOneL(self, L: float, M: int):
        """ L: length
            nb: bits per coordinate
        """
        Sd = self.calcS(L, M)
        S1 = self.calcS(L, M*1024)
        S2 = 1 - S1
        Err1 = numpy.abs(Sd-S1)
        Err2 = S2
        return (Err1, Err2)

    def drawS1(self, ax, nb, col, npqd, nperr1, nperr2):
        ax.plot(npqd, nperr1, color=col, label=f"nb={nb}, |Sd-S1|", marker="o")
        # ax.plot(npqd, nperr2, label=f"nb={nb}, S2", marker="+")
        self._df[f"dq"] = npqd
        self._df[f"S1Sd({nb})"] = nperr1

    def drawS2(self, ax, nb, col, npqd, nperr1, nperr2):
        # ax.plot(npqd, nperr1, label=f"nb={nb}, |Sd-S1|", marker="x")
        ax.plot(npqd, nperr2, color=col, label=f"nb={nb}, S2", marker="x")
        # self._df[f"dq"] = npqd
        # self._df[f"S1Sd({nb})"] = nperr1

    def drawSsum(self, ax, nb, col, npdq, nperr1, nperr2, dr):
        sdiff = nperr1 + nperr2
        ax.plot(npdq, sdiff, color=col, label=f"nb={nb}, |Sd-S1|+S2")
        # plot the point that will be used as minimum
        y = find_y_for(npdq, sdiff, dr)
        ax.plot(dr, y, color=col, marker="o")
        self._df[f"Sdiff({nb})"] = sdiff
    
    def drawPsi(self, xr, yr, sr, nbs):
        ax: Axes = self._axs[0]
        ax.set_title(f"{self._labels[0]} Re(Ψ1D)")
        ax.set_xlabel("x")
        x = numpy.linspace(xr[0], xr[1], 201)
        ax.set_ylim(yr[0], yr[1])
        ax.grid(True)
        psi_vals = self._psi1d(x)
        ax.plot(x, psi_vals, label=f"Re(Ψ1D)")
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
        dq0 = 0.02
        scales = numpy.geomspace(1, 20, 40)
        dqList= []
        err1List = []
        err2List = []
        for scale in scales:
            dq = dq0 * scale
            L = dq * M
            err1, err2 = self.evalOneL(L, M)
            dqList.append(dq)
            err1List.append(err1)
            err2List.append(err2)
        npdq = numpy.array(dqList)
        nperr1 = numpy.array(err1List)
        nperr2 = numpy.array(err2List)
        return (npdq, nperr1, nperr2)

    def evalAndDraw(self, nb, col):
        dq, err1, err2 = self.evalLRange(nb)
        ax = self._axs[1]
        ax.set_title(f"{self._labels[1]} |Sd-S1| and S2")
        ax.set_xlabel("δr")
        ax.set_ylim(0, 0.002)
        ax.grid(True)
        self.drawS1(ax, nb, col, dq, err1, err2)
        self.drawS2(ax, nb, col, dq, err1, err2)
        ax.legend()

    def evalAndDrawS2(self, nb, col, dr):
        dq, err1, err2 = self.evalLRange(nb)
        ax = self._axs[2]
        ax.set_xlabel("δr")
        ax.set_ylim(0, 0.004)
        ax.grid(True)
        ax.set_title(f"{self._labels[2]} |Sd-S1| + S2")
        self.drawSsum(ax, nb, col, dq, err1, err2, dr)
        ax.legend()

    def plot(self):
        fig = self._fig
        fig.suptitle("1D δr analysis for Ψ1D_1")
        fig.savefig(f"{outdir}/eval1d_dq.png", dpi=300)
        self._df.to_csv(f"{outdir}/eval1d_dq.csv")

def psi1d_1(x):
    return math.sqrt(2)*numpy.exp(-numpy.abs(x))*x


for labels, outdir in zip([LABELS1, LABELS2], [OUTDIR1, OUTDIR2]):
    evaldq1d = EvalDq1d(psi1d_1, labels, outdir)

    drs = [0.23, 0.13, 0.078, 0.045]
    evaldq1d.drawPsi([-15,15], [-0.75, 0.75], drs, range(6,10))
    for nb, col in zip(range(6, 10), evaldq1d._colors):
        evaldq1d.evalAndDraw(nb, col)
    for nb, col, dr in zip(range(6, 10), evaldq1d._colors, drs):
        evaldq1d.evalAndDrawS2(nb, col, dr)
    evaldq1d.plot()

