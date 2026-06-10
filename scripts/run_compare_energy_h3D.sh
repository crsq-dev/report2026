#!/bin/sh -e

# PSI(1,0,0)
TO=2
python compare_energy_h3D.py --bits 6 --signed --double --trotter-order $TO --qn 1 --ql 0 --qm 0 --etot -0.5 --ek 0.5 --ep -1 --ew 0.5 --length 12 --delta-t 0.005 --interval-time 0.2 --total-time 12.6
python compare_energy_h3D.py --bits 7 --signed --double --trotter-order $TO --qn 1 --ql 0 --qm 0 --etot -0.5 --ek 0.5 --ep -1 --ew 0.5 --length 13 --delta-t 0.001 --interval-time 0.2 --total-time 12.6
python compare_energy_h3D.py --bits 8 --signed --double --trotter-order $TO --qn 1 --ql 0 --qm 0 --etot -0.5 --ek 0.5 --ep -1 --ew 0.5 --length 13 --delta-t 0.0005 --interval-time 0.2 --total-time 12.6

