import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import pandas as pd
import cupy
import numpy
from crsq.models.hydrogen3d import PsiH3D
import os, argparse, logging

logger = logging.getLogger("crsq-explore.scripts")

OUTDIR="onedrive.lnk/dq_tradeoff/3d"
os.makedirs(OUTDIR, exist_ok=True)

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

class EvalDq3d:
    def __init__(self, psi3d, dq0, label, suffix, scale=0.01):
        self._psi3d = psi3d
        self._dq0 = dq0
        self._label = label
        self._suffix = suffix
        self._scale = scale
        fig, axs = plt.subplots(1, 3, figsize=(15, 4), layout='constrained')
        fig.suptitle(f"3D δr analysis for Ψ3D_{suffix}")
        axs[0].set_title(f"({label}1) Re(Ψ3D_{suffix}(x,0,0))")
        axs[1].set_title(f"({label}2) |Sd-S1| and S2")
        axs[2].set_title(f"({label}3) |Sd-S1| + S2")
        self._df = pd.DataFrame()
        self._fig = fig
        self._axs = axs
        self._colors = ['blue', 'orange', 'green', 'red']
    
    def psi3d(self, x, y, z):
        npx = cupy.asnumpy(x)
        npy = cupy.asnumpy(y)
        npz = cupy.asnumpy(z)
        psi = self._psi3d(npx, npy, npz)
        return cupy.asarray(psi)
    
    def calcS(self, L, m):
        dq = L / m
        logger.info(f"calcS: L={L:.2f}, m={m}, dq={dq:.4f}")
        q = cupy.linspace(-L/2, L/2-dq, m)
        x = q[:, None, None]
        y = q[None, :, None]
        z = q[None, None, :]
        s = 0.0
        y = q[:, None]
        z = q[None, :]
        for i in range(m):
            logger.info(f"calcS: i={i}/{m}")
            xi = q[i]
            x = xi
            psi_slice = self.psi3d(x,y,z)
            s += cupy.sum(cupy.abs(psi_slice)**2)
        return s.item() * dq**3

    def evalOneL(self, L: float, M: int):
        """ :param L: length
            :param nb: bits per coordinate
            :return: (Err1, Err2) where Err1 = |Sd-S1|, Err2 = S2
        """
        logger.info(f"evalOneL: L={L:.2f}, M={M}")
        Sd = self.calcS(L, M) #scalar
        S1 = self.calcS(L, M*8) #scalar ほんとは16
        S2 = 1.0 - S1
        logger.info(f"Sd={Sd:.6f}, S1={S1:.6f}, S2={S2:.6f}")
        Err1 = Sd-S1 #scalar
        Err2 = S2 #scalar
        return (Err1, Err2)

    def drawS1S2(self, ax: Axes, nb, col, dqlist, err1List, err2List):
        ax.set_xlabel("δr")
        ax.set_ylim(0, self._scale)
        ax.grid(True)
        ax.plot(dqlist, err1List, color=col, label=f"nb={nb}, |Sd-S1|", marker="o")
        ax.plot(dqlist, err2List, color=col, label=f"nb={nb}, S2", marker="x")
        ax.legend()
        self._df[f"δr"] = dqlist
        self._df[f"S1Sd({nb})"] = err1List

    def drawSsum(self, ax: Axes, nb, col, dqlist, err1List, err2List, dr):
        nperr1 = numpy.array(err1List)
        nperr2 = numpy.array(err2List)
        ax.set_xlabel("δr")
        ax.set_ylim(0, self._scale)
        sdiff = nperr1 + nperr2
        ax.plot(dqlist, sdiff, color=col, label=f"nb={nb}, |Sd-S1|+S2")
        # plot the point that will be used as minimum
        y = find_y_for(dqlist, sdiff, dr)
        ax.plot(dr, y, color=col, marker="o")
        ax.legend()
        ax.grid(True)
        self._df[f"Sdiff({nb})"] = sdiff
    
    def drawPsi(self, xr, yr, sr, nbs):
        label = self._label
        ax: Axes = self._axs[0]
        ax.set_title(f"({label}1) Re(Ψ3D_{self._suffix}(x,0,0))")
        ax.set_xlabel("x")
        x = cupy.linspace(xr[0], xr[1], 201)
        ax.set_ylim(yr[0], yr[1])
        ax.grid(True)
        psiVals = self._psi3d(x, 0, 0)
        npX = cupy.asnumpy(x)
        npPsiVals = cupy.asnumpy(cupy.real(psiVals))
        ax.plot(npX, npPsiVals, label=f"Re(Ψ3D_{self._suffix}(x,0,0))")
        for s,nb,col in zip(sr, nbs, self._colors):
            # put vertical line at x = +- s
            L = s * (1 << nb)
            HL=L/2
            ax.axvline(x= HL, color=col, label=f"nb={nb}, x=\u00b1{HL:.1f}")
            ax.axvline(x=-HL, color=col)
        ax.legend()

    def evalLRange(self, nb):
        """ eval L range.
            :param nb: bits per coordinate
            :return: (npdq, nperr1, nperr2) where npdq is the array of δr values, nperr1 is the array of |Sd-S1| values, nperr2 is the array of S2 values
        """
        M = 1 << nb
        # step ratio for increasing L. step_ratio**10 = 10.
        npscales = numpy.geomspace(2.0, 40.0, 20) # もとは40
        dqList= []
        err1List = []
        err2List = []
        for scale in npscales:
            logger.info(f"scale={scale:.2f}")
            dq = self._dq0 * scale
            L = dq * M
            err1, err2 = self.evalOneL(L, M)
            dqList.append(dq)
            err1List.append(err1)
            err2List.append(err2)
        return (dqList, err1List, err2List)

    def evalAndDraw(self, nb, col, dr):
        logger.info(f"evalAndDraw: nb={nb}, dr={dr}")
        dqList, err1List, err2List = self.evalLRange(nb)
        ax = self._axs[1]
        self.drawS1S2(ax, nb, col, dqList, err1List, err2List)
        ax = self._axs[2]
        self.drawSsum(ax, nb, col, dqList, err1List, err2List, dr)

    def plot(self):
        fig = self._fig
        fig.savefig(f"{OUTDIR}/eval3d_dq_geom_{self._suffix}.png")
        self._df.to_csv(f"{OUTDIR}/eval3d_geom_{self._suffix}.csv")

X0 = 0
Y0 = 0
Z0 = 0

def psi3d_1_0_0(x,y,z):
    npx = cupy.asnumpy(x)
    npy = cupy.asnumpy(y)
    npz = cupy.asnumpy(z)
    psi = PsiH3D(X0, Y0, Z0, 1, 0, 0)
    return cupy.asarray(psi(npx, npy, npz))

def psi3d_2_0_0(x,y,z):
    npx = cupy.asnumpy(x)
    npy = cupy.asnumpy(y)
    npz = cupy.asnumpy(z)
    psi = PsiH3D(X0, Y0, Z0, 2, 0, 0)
    return cupy.asarray(psi(npx, npy, npz))

def psi3d_2_1_0(x,y,z):
    npx = cupy.asnumpy(x)
    npy = cupy.asnumpy(y)
    npz = cupy.asnumpy(z)
    psi = PsiH3D(X0, Y0, Z0, 2, 1, 0)
    return cupy.asarray(psi(npx, npy, npz))

def psi3d_2_1_1(x,y,z):
    npx = cupy.asnumpy(x)
    npy = cupy.asnumpy(y)
    npz = cupy.asnumpy(z)
    psi = PsiH3D(X0, Y0, Z0, 2, 1, 1)
    return cupy.asarray(psi(npx, npy, npz))

def draw_graphs():
    psi3d = PsiH3D(X0, Y0, Z0, 1, 0, 0)
    evaldq3d100 = EvalDq3d(psi3d, 0.01, "C", "1_0_0", 0.02)
    # drs = [0.078, 0.039, 0.0234, 0.0137]
    drs = [0.078, 0.039, 0.0234]
    #drs = [0.078]
    evaldq3d100.drawPsi([-5,5], [-0.5, 1.0], drs, range(6,8)) #ほんとはrange(6,10)
    for nb, col, dr in zip(range(6, 8), evaldq3d100._colors, drs):
        evaldq3d100.evalAndDraw(nb, col, dr)
    evaldq3d100.plot()

def draw_graphs_from_files(evaldq, drs):
    """ read results from csv files and draw graphs."""
    evaldq.drawPsi([-8,8], [-0.5, 0.75], drs, range(6, 9)) #ほんとはrange(6,10)
    for nb, col, dr in zip(range(6, 9), evaldq._colors, drs):
        df = pd.read_csv(f"{OUTDIR}/eval3d_geom_{evaldq._suffix}_nb{nb}.csv")
        dqList = df["δr"].tolist()
        err1List = df[f"S1Sd({nb})"].tolist()
        err2List = df[f"Sdiff({nb})"].tolist()
        ax = evaldq._axs[1]
        evaldq.drawS1S2(ax, nb, col, dqList, err1List, err2List)
        ax = evaldq._axs[2]
        evaldq.drawSsum(ax, nb, col, dqList, err1List, err2List, dr)
    evaldq.plot()

def eval_one_nb(evaldq, drs, nb):
    """ evaluate for one nb and save results to csv"""
    dqList, err1List, err2List = evaldq.evalLRange(nb)
    df = pd.DataFrame({
        "δr": dqList,
        f"S1Sd({nb})": err1List,
        f"Sdiff({nb})": err2List,
    })
    df.to_csv(f"{OUTDIR}/eval3d_geom_{evaldq._suffix}_nb{nb}.csv", index=False)

def run_main():
    parser = argparse.ArgumentParser(
        prog="draw_h1dq_tradeoff_3d",
        description="Draw tradeoff between δr and error in 3D hydrogen atom model.",
    )
    parser.add_argument("--draw-graph", action="store_true", help="Draw the graphs")
    parser.add_argument("--eval", type=int, default=0, help="Evaluate the errors for given nb. Usage: --eval 6")

    args = parser.parse_args()

    evaldq = EvalDq3d(psi3d_1_0_0, 0.01, "C", "1_0_0", 0.01)
    drs = [0.180, 0.100, 0.050]

    logfilename = f"{OUTDIR}/draw_h1dq_tradeoff_3d_{args.eval}.log"
    logging.basicConfig(filename=logfilename, level=logging.INFO, format='%(asctime)s %(message)s')

    if args.draw_graph:
        draw_graphs_from_files(evaldq, drs)
    elif args.eval > 0:
        eval_one_nb(evaldq, drs, args.eval)

if __name__ == "__main__":
    run_main()
