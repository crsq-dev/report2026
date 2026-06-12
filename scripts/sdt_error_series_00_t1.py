""" Run trotter_error for n=0, m=0
"""

import crsq_xp.sderror.trotter_err as trotter_err
import numpy
import matplotlib.pyplot as plt
import logging, os

logger = logging.getLogger("crsq_xp")
basedir="onedrive.lnk/parameters/evaluator"

qn=0
qm=0
En = -2.0
nblist = [6,9]
L = [5,7]
# nblist = [6,7,8,9]
# L = [5,5,6,7]
# nblist = [6]
# L = [5]
t=1.0

for nb, L in zip(nblist,L):
    eva = trotter_err.Evaluator(basedir, nb=nb, qn=qn, qm=qm, En=En, L=L, t=t)
    eva.set_ylim(1e-3, 1e+2)
    # specify log of trotter rounds.
    lo=1
    hi=5
    oct=4
    log_nt = numpy.linspace(lo,hi,(hi-lo)*oct+1)
    eva.run(log_nt) #Trotter order = 1
    eva.save_fig()
