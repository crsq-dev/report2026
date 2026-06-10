#!/bin/sh -e

# PSI(0,0)
# python compare_energy_h2D.py --bits 6 --signed --double --qn 0 --qm 0 --etot -2 --ek 2 --ep -4 --length 10 --delta-t 0.001 --interval-time 0.2 --total-time 3.2
# python compare_energy_h2D.py --bits 7 --signed --double --qn 0 --qm 0 --length 10 --delta-t 0.0005 --interval-time 0.2 --total-time 3.2
# python compare_energy_h2D.py --bits 8 --signed --double --qn 0 --qm 0 --length 10 --delta-t 0.0001 --interval-time 0.2 --total-time 3.2
# python compare_energy_h2D.py --bits 9 --signed --double --qn 0 --qm 0 --length 10 --delta-t 0.00005 --interval-time 0.2 --total-time 3.2

# python compare_energy_h2D.py --bits 6 --signed --double --qn 0 --qm 0 --length 12 --delta-t 0.005 --interval-time 0.2 --total-time 3.2
# python compare_energy_h2D.py --bits 7 --signed --double --qn 0 --qm 0 --length 12 --delta-t 0.001 --interval-time 0.2 --total-time 3.2
# python compare_energy_h2D.py --bits 8 --signed --double --qn 0 --qm 0 --length 12 --delta-t 0.0001 --interval-time 0.2 --total-time 3.2
# python compare_energy_h2D.py --bits 9 --signed --double --qn 0 --qm 0 --length 12 --delta-t 0.00005 --interval-time 0.2 --total-time 3.2

# PSI(1,0)
# python compare_energy_h2D.py --bits 6 --signed --double --qn 1 --qm 0 --length 26 --delta-t 0.01 --interval-time 0.2 --total-time 16
# python compare_energy_h2D.py --bits 7 --signed --double --qn 1 --qm 0 --length 26 --delta-t 0.005 --interval-time 0.2 --total-time 16
# python compare_energy_h2D.py --bits 8 --signed --double --qn 1 --qm 0 --length 26 --delta-t 0.001 --interval-time 0.2 --total-time 16
# python compare_energy_h2D.py --bits 9 --signed --double --qn 1 --qm 0 --length 26 --delta-t 0.0001 --interval-time 0.2 --total-time 16

# python compare_energy_h2D.py --bits 6 --signed --double --qn 1 --qm 0 --length 32 --delta-t 0.01 --interval-time 0.2 --total-time 16
# python compare_energy_h2D.py --bits 7 --signed --double --qn 1 --qm 0 --length 32 --delta-t 0.005 --interval-time 0.2 --total-time 16
# python compare_energy_h2D.py --bits 8 --signed --double --qn 1 --qm 0 --length 32 --delta-t 0.001 --interval-time 0.2 --total-time 16
# python compare_energy_h2D.py --bits 9 --signed --double --qn 1 --qm 0 --length 32 --delta-t 0.0005 --interval-time 0.2 --total-time 16

# PSI(1,1)
# python compare_energy_h2D.py --bits 6 --signed --double --qn 1 --qm 1 --length 26 --delta-t 0.01 --interval-time 0.2 --total-time 16
# python compare_energy_h2D.py --bits 7 --signed --double --qn 1 --qm 1 --length 26 --delta-t 0.005 --interval-time 0.2 --total-time 16
# python compare_energy_h2D.py --bits 8 --signed --double --qn 1 --qm 1 --length 26 --delta-t 0.001 --interval-time 0.2 --total-time 16
# python compare_energy_h2D.py --bits 9 --signed --double --qn 1 --qm 1 --length 26 --delta-t 0.0001 --interval-time 0.2 --total-time 16

# python compare_energy_h2D.py --bits 8 --signed --double --qn 1 --qm 1 --length 26 --delta-t 0.001 --interval-time 0.2 --total-time 32

# python compare_energy_h2D.py --bits 6 --signed --double --qn 1 --qm 1 --length 26 --delta-t 0.01 --interval-time 0.5 --total-time 64
# python compare_energy_h2D.py --bits 7 --signed --double --qn 1 --qm 1 --length 26 --delta-t 0.005 --interval-time 0.5 --total-time 64
# python compare_energy_h2D.py --bits 8 --signed --double --qn 1 --qm 1 --length 26 --delta-t 0.001 --interval-time 0.5 --total-time 64
# python compare_energy_h2D.py --bits 9 --signed --double --qn 1 --qm 1 --length 26 --delta-t 0.0001 --interval-time 0.5 --total-time 64

# python compare_energy_h2D.py --bits 6 --signed --double --qn 1 --qm 1 --length 32 --delta-t 0.01 --interval-time 0.2 --total-time 16
# python compare_energy_h2D.py --bits 7 --signed --double --qn 1 --qm 1 --length 32 --delta-t 0.005 --interval-time 0.2 --total-time 16
# python compare_energy_h2D.py --bits 8 --signed --double --qn 1 --qm 1 --length 32 --delta-t 0.001 --interval-time 0.2 --total-time 16
# python compare_energy_h2D.py --bits 9 --signed --double --qn 1 --qm 1 --length 32 --delta-t 0.0005 --interval-time 0.2 --total-time 16

#python compare_energy_h2D.py --bits 9 --signed --double --qn 1 --qm 1 --length 32 --delta-t 0.0005 --interval-time 0.2 --total-time 32

# python compare_energy_h2D.py --bits 6 --signed --double --qn 1 --qm 1 --length 32 --delta-t 0.01 --interval-time 0.5 --total-time 64
# python compare_energy_h2D.py --bits 7 --signed --double --qn 1 --qm 1 --length 32 --delta-t 0.005 --interval-time 0.5 --total-time 64
# python compare_energy_h2D.py --bits 8 --signed --double --qn 1 --qm 1 --length 32 --delta-t 0.001 --interval-time 0.5 --total-time 64
# python compare_energy_h2D.py --bits 9 --signed --double --qn 1 --qm 1 --length 32 --delta-t 0.0005 --interval-time 0.5 --total-time 64

# optimal

for TO in 1 2; do
    python compare_energy_h2D.py --bits 6 --signed --double --length 5 --qn 0 --qm 0 --trotter-order $TO --etot -2 --ek 2 --ep -4 --ew 0.3 --delta-t 0.00100 --interval-time 0.2 --total-time 4.0
    python compare_energy_h2D.py --bits 7 --signed --double --length 5 --qn 0 --qm 0 --trotter-order $TO --etot -2 --ek 2 --ep -4 --ew 0.3 --delta-t 0.00010 --interval-time 0.2 --total-time 4.0
    python compare_energy_h2D.py --bits 8 --signed --double --length 6 --qn 0 --qm 0 --trotter-order $TO --etot -2 --ek 2 --ep -4 --ew 0.3 --delta-t 0.00010 --interval-time 0.2 --total-time 4.0
    python compare_energy_h2D.py --bits 9 --signed --double --length 7 --qn 0 --qm 0 --trotter-order $TO --etot -2 --ek 2 --ep -4 --ew 0.3 --delta-t 0.00005 --interval-time 0.2 --total-time 4.0

    python compare_energy_h2D.py --bits 6 --signed --double --length 18 --qn 1 --qm 0 --trotter-order $TO --etot -0.22 --ek 0.22 --ep -0.44 --ew 0.03 --delta-t 0.0100 --interval-time 0.5 --total-time 30
    python compare_energy_h2D.py --bits 7 --signed --double --length 21 --qn 1 --qm 0 --trotter-order $TO --etot -0.22 --ek 0.22 --ep -0.44 --ew 0.03 --delta-t 0.0050 --interval-time 0.5 --total-time 30
    python compare_energy_h2D.py --bits 8 --signed --double --length 24 --qn 1 --qm 0 --trotter-order $TO --etot -0.22 --ek 0.22 --ep -0.44 --ew 0.03 --delta-t 0.0010 --interval-time 0.5 --total-time 30
    python compare_energy_h2D.py --bits 9 --signed --double --length 27 --qn 1 --qm 0 --trotter-order $TO --etot -0.22 --ek 0.22 --ep -0.44 --ew 0.03 --delta-t 0.0005 --interval-time 0.5 --total-time 30

    TT=30
    python compare_energy_h2D.py --bits 6 --signed --double --length 25 --qn 1 --qm 1 --trotter-order $TO --etot -0.22 --ek 0.22 --ep -0.44 --ew 0.03 --delta-t 0.0100 --interval-time 0.5 --total-time $TT
    python compare_energy_h2D.py --bits 7 --signed --double --length 30 --qn 1 --qm 1 --trotter-order $TO --etot -0.22 --ek 0.22 --ep -0.44 --ew 0.03 --delta-t 0.0100 --interval-time 0.5 --total-time $TT
    python compare_energy_h2D.py --bits 8 --signed --double --length 34 --qn 1 --qm 1 --trotter-order $TO --etot -0.22 --ek 0.22 --ep -0.44 --ew 0.03 --delta-t 0.0050 --interval-time 0.5 --total-time $TT
    python compare_energy_h2D.py --bits 9 --signed --double --length 39 --qn 1 --qm 1 --trotter-order $TO --etot -0.22 --ek 0.22 --ep -0.44 --ew 0.03 --delta-t 0.0010 --interval-time 0.5 --total-time $TT
done
