#!/bin/sh -e

# trotter order 別に nb=6 で dt を振り、reff=0.25δrでt=1の期間tevした時のエネルギーの解析解との差をプロットする。

TO=1
# for EPS in 1.000 0.707 0.500 0.353 0.250 0.176 0.125; do
EPS=0.250
for DT in 0.1 0.01 0.001 0.0001 1e-4 1e-5 ; do
    python sdt_error.py --bits 6 --trotter-order $TO --length 5 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --pole rofs --eps $EPS --delta-t $DT --interval-time 0.1 --total-time 1.0
done

TO=2
EPS=0.250
for DT in 0.1 0.01 0.001 0.0001 1e-4 1e-5 ; do
    python sdt_error.py --bits 6 --trotter-order $TO --length 5 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --pole rofs --eps $EPS --delta-t $DT --interval-time 0.1 --total-time 1.0
done
