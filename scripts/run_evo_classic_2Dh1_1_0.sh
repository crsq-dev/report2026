#!/bin/sh -e
# optimal L, deltat

# PSI(1,0)
TO=2
TT=30
for PO in rofs r0lim ; do
    for EPS in 1.000 0.707 0.500 0.353 0.250 0.176 0.125; do
        python time_evo_classic_2Dh1.py --bits 6 --trotter-order $TO --length 18 --psixmax 0.4 --psikmax 2.2 --qnum-n 1 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.0100 --interval-time 0.5 --total-time $TT &
        python time_evo_classic_2Dh1.py --bits 7 --trotter-order $TO --length 21 --psixmax 0.4 --psikmax 2.2 --qnum-n 1 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.0050 --interval-time 0.5 --total-time $TT &
        python time_evo_classic_2Dh1.py --bits 8 --trotter-order $TO --length 24 --psixmax 0.4 --psikmax 2.2 --qnum-n 1 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.0010 --interval-time 0.5 --total-time $TT &
        python time_evo_classic_2Dh1.py --bits 9 --trotter-order $TO --length 27 --psixmax 0.4 --psikmax 2.2 --qnum-n 1 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.0005 --interval-time 0.5 --total-time $TT
    done
done

PO=rofs
EPS=0.250
TT=30
# python time_evo_classic_2Dh1.py --bits 6 --trotter-order $TO --length 18 --psixmax 0.4 --psikmax 2.2 --qnum-n 1 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.0100 --interval-time 0.5 --total-time $TT &
# python time_evo_classic_2Dh1.py --bits 7 --trotter-order $TO --length 21 --psixmax 0.4 --psikmax 2.2 --qnum-n 1 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.0050 --interval-time 0.5 --total-time $TT &
# python time_evo_classic_2Dh1.py --bits 8 --trotter-order $TO --length 24 --psixmax 0.4 --psikmax 2.2 --qnum-n 1 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.0010 --interval-time 0.5 --total-time $TT &
# python time_evo_classic_2Dh1.py --bits 9 --trotter-order $TO --length 27 --psixmax 0.4 --psikmax 2.2 --qnum-n 1 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.0005 --interval-time 0.5 --total-time $TT
