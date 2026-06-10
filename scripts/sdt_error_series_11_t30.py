"""Run trotter_error"""

import crsq_xp.sderror.trotter_err as trotter_err
import numpy
import matplotlib.pyplot as plt
import logging, os

logger = logging.getLogger("crsq_xp")
basedir="onedrive.lnk/parameters/evaluator"

qn = 1
qm = 1
En = -2 / 9
nb = [6, 7, 8, 9]
L = [25, 30, 34, 39]
t=30
lo=2
hi=6
oct=4

for nb, L in zip(nb, L):
    eva = trotter_err.Evaluator(basedir, nb=nb, qn=qn, qm=qm, En=En, L=L, t=t)
    eva.set_ylim(1e-4, 1e1)
    # specify log of trotter rounds.
    log_nt = numpy.linspace(lo,hi,(hi-lo)*oct+1)
    eva.run(log_nt)  # Trotter order = 1
    eva.save_fig()
