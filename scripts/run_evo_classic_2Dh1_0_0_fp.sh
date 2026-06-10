#!/bin/sh -e


# test for evaluating fixed point.
TO=1
TT=4.0
PO=r0lim
EPS=0.250
for FP in 0 2 4 6 8; do
    python time_evo_classic_2Dh1.py --bits 6 --frac-bits $FP --trotter-order $TO --length 5 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.00100 --interval-time 0.2 --total-time 4.0
    python time_evo_classic_2Dh1.py --bits 8 --frac-bits $FP --trotter-order $TO --length 6 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.00010 --interval-time 0.2 --total-time 4.0
done

# optimal L, deltat

# PSI(0,0)
TO=2
TT=4.0
# for PO in rofs r0lim ; do
#     for EPS in 1.000 0.707 0.500 0.353 0.250 0.176 0.125; do
#         python time_evo_classic_2Dh1.py --bits 6 --trotter-order $TO --length 5 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.00100 --interval-time 0.2 --total-time 4.0 &
#         python time_evo_classic_2Dh1.py --bits 7 --trotter-order $TO --length 5 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.00010 --interval-time 0.2 --total-time 4.0 &
#         python time_evo_classic_2Dh1.py --bits 8 --trotter-order $TO --length 6 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.00010 --interval-time 0.2 --total-time 4.0 &
#         python time_evo_classic_2Dh1.py --bits 9 --trotter-order $TO --length 7 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.00005 --interval-time 0.2 --total-time 4.0
#     done
# done

# Short runs for debugging
# EPS=0.250
# python time_evo_classic_2Dh1.py --bits 6 --trotter-order $TO --save-psi2 --length 5 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.00100 --interval-time 0.002 --total-time 0.008


PO=rofs
EPS=0.250
# python time_evo_classic_2Dh1.py --bits 6 --trotter-order $TO --length 5 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.00100 --interval-time 0.2 --total-time 4.0
# python time_evo_classic_2Dh1.py --bits 7 --trotter-order $TO --length 5 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.00010 --interval-time 0.2 --total-time 4.0
# python time_evo_classic_2Dh1.py --bits 8 --trotter-order $TO --length 6 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.00010 --interval-time 0.2 --total-time 4.0
# python time_evo_classic_2Dh1.py --bits 9 --trotter-order $TO --length 7 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.00005 --interval-time 0.2 --total-time 4.0

