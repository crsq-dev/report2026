#!/bin/sh -e
# optimal L, deltat

# PSI(1,0,0)
TO=1
TT=4.0
for PO in r0lim ; do
    # for EPS in 0.3333333333; do
    for EPS in 1 0.5 0.3333333333 0.25 0.2; do
        python time_evo_classic_3Dh1.py  --bits 6 --trotter-order $TO --length 12 --psixmax 0.6 --psikmax 1.2 --qnum-n 1 --qnum-l 0 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.00500 --interval-time 0.2 --total-time 12.6
        python time_evo_classic_3Dh1.py  --bits 7 --trotter-order $TO --length 13 --psixmax 0.6 --psikmax 1.2 --qnum-n 1 --qnum-l 0 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.00100 --interval-time 0.2 --total-time 12.6
        python time_evo_classic_3Dh1.py  --bits 8 --trotter-order $TO --length 13 --psixmax 0.6 --psikmax 1.2 --qnum-n 1 --qnum-l 0 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.00050 --interval-time 0.2 --total-time 12.6
    done
done

# Short runs for debugging
# EPS=0.250
# python time_evo_classic_2Dh1.py  --bits 6 --trotter-order $TO --save-psi2 --length 5 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.00100 --interval-time 0.002 --total-time 0.008


PO=rofs
EPS=0.250
# python time_evo_classic_2Dh1.py  --bits 6 --trotter-order $TO --length 5 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.00100 --interval-time 0.2 --total-time 4.0
# python time_evo_classic_2Dh1.py  --bits 7 --trotter-order $TO --length 5 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.00010 --interval-time 0.2 --total-time 4.0
# python time_evo_classic_2Dh1.py  --bits 8 --trotter-order $TO --length 6 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.00010 --interval-time 0.2 --total-time 4.0
# python time_evo_classic_2Dh1.py  --bits 9 --trotter-order $TO --length 7 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.00005 --interval-time 0.2 --total-time 4.0

