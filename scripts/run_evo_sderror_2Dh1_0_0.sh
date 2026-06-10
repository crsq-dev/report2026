#!/bin/sh -e


# optimal L, deltat
# PSI(0,0)
#PO=rofs
PO=r0lim
TO=2
# for EPS in 1.000 0.707 0.500 0.353 0.250 0.176 0.125; do
#     python time_evo_sderror_2Dh1.py --bits 6 --trotter-order $TO --length 5 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.00100 --interval-time 0.2 --total-time 4.0 &
#     python time_evo_sderror_2Dh1.py --bits 7 --trotter-order $TO --length 5 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.00050 --interval-time 0.2 --total-time 4.0 &
#     python time_evo_sderror_2Dh1.py --bits 8 --trotter-order $TO --length 6 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.00010 --interval-time 0.2 --total-time 4.0 &
#     python time_evo_sderror_2Dh1.py --bits 9 --trotter-order $TO --length 7 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.00005 --interval-time 0.2 --total-time 4.0
# done

PO=rofs
EPS=0.250
python time_evo_sderror_2Dh1.py --bits 6 --trotter-order $TO --length 5 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.00100 --interval-time 0.2 --total-time 4.0
# python time_evo_sderror_2Dh1.py --bits 7 --trotter-order $TO --length 5 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.00010 --interval-time 0.2 --total-time 4.0
# python time_evo_sderror_2Dh1.py --bits 8 --trotter-order $TO --length 6 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.00010 --interval-time 0.2 --total-time 4.0
# python time_evo_sderror_2Dh1.py --bits 9 --trotter-order $TO --length 7 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.00005 --interval-time 0.2 --total-time 4.0

