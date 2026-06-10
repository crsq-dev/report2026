#!/bin/sh -e
L=10
TT=3.2
IT=0.2
QN=0
QM=0
PXM=1.2
PKM=0.5
USD=--use-saved-data

# python time_evo_classic_2Dh1.py --bits 6 --length $L --psixmax $PXM --psikmax $PKM --qnum-n $QN --qnum-m $QM --delta-t 0.001 --interval-time $IT --total-time $TT
# python time_evo_classic_2Dh1.py --bits 7 --length $L --psixmax $PXM --psikmax $PKM --qnum-n $QN --qnum-m $QM --delta-t 0.0005 --interval-time $IT --total-time $TT
# python time_evo_classic_2Dh1.py --bits 8 --length $L --psixmax $PXM --psikmax $PKM --qnum-n $QN --qnum-m $QM --delta-t 0.0001 --interval-time $IT --total-time $TT
# python time_evo_classic_2Dh1.py --bits 9 --length $L --psixmax $PXM --psikmax $PKM --qnum-n $QN --qnum-m $QM --delta-t 0.00005 --interval-time $IT --total-time $TT

# for debugging
IT=0.001
TT=0.004
# python time_evo_classic_2Dh1.py --bits 6 --length $L --psixmax $PXM --psikmax $PKM --qnum-n $QN --qnum-m $QM --delta-t 0.001 --interval-time $IT --total-time $TT --save-psi2


L=12
TT=3.2
IT=0.2
QN=0
QM=0
PXM=1.2
PKM=0.5

# python time_evo_classic_2Dh1.py --bits 6 --length $L --psixmax $PXM --psikmax $PKM --qnum-n $QN --qnum-m $QM --delta-t 0.005 --interval-time $IT --total-time $TT
# python time_evo_classic_2Dh1.py --bits 7 --length $L --psixmax $PXM --psikmax $PKM --qnum-n $QN --qnum-m $QM --delta-t 0.001 --interval-time $IT --total-time $TT
# python time_evo_classic_2Dh1.py --bits 8 --length $L --psixmax $PXM --psikmax $PKM --qnum-n $QN --qnum-m $QM --delta-t 0.0001 --interval-time $IT --total-time $TT
# python time_evo_classic_2Dh1.py --bits 9 --length $L --psixmax $PXM --psikmax $PKM --qnum-n $QN --qnum-m $QM --delta-t 0.00005 --interval-time $IT --total-time $TT

# for debugging
IT=0.005
TT=0.02
# python time_evo_classic_2Dh1.py --bits 6 --length $L --psixmax $PXM --psikmax $PKM --qnum-n $QN --qnum-m $QM --delta-t 0.005 --interval-time $IT --total-time $TT --save-psi2


L=26
TT=16
IT=0.2
QN=1
QM=0
PXM=0.4
PKM=2.2
# python time_evo_classic_2Dh1.py --bits 6 --length $L --psixmax $PXM --psikmax $PKM --qnum-n $QN --qnum-m $QM --delta-t 0.01 --interval-time $IT --total-time $TT
# python time_evo_classic_2Dh1.py --bits 7 --length $L --psixmax $PXM --psikmax $PKM --qnum-n $QN --qnum-m $QM  --delta-t 0.005 --interval-time $IT --total-time $TT
# python time_evo_classic_2Dh1.py --bits 8 --length $L --psixmax $PXM --psikmax $PKM --qnum-n $QN --qnum-m $QM  --delta-t 0.001 --interval-time $IT --total-time $TT
# python time_evo_classic_2Dh1.py --bits 9 --length $L --psixmax $PXM --psikmax $PKM --qnum-n $QN --qnum-m $QM --delta-t 0.0001 --interval-time $IT --total-time $TT

QN=1
QM=1
PXM=0.2
PKM=1.0
# python time_evo_classic_2Dh1.py --bits 6 --length $L --psixmax $PXM --psikmax $PKM --qnum-n $QN --qnum-m $QM --delta-t 0.01 --interval-time $IT --total-time $TT
# python time_evo_classic_2Dh1.py --bits 7 --length $L --psixmax $PXM --psikmax $PKM --qnum-n $QN --qnum-m $QM  --delta-t 0.005 --interval-time $IT --total-time $TT
# python time_evo_classic_2Dh1.py --bits 8 --length $L --psixmax $PXM --psikmax $PKM --qnum-n $QN --qnum-m $QM  --delta-t 0.001 --interval-time $IT --total-time $TT
# python time_evo_classic_2Dh1.py --bits 9 --length $L --psixmax $PXM --psikmax $PKM --qnum-n $QN --qnum-m $QM --delta-t 0.0001 --interval-time $IT --total-time $TT

IT=0.5
TT=64
# python time_evo_classic_2Dh1.py --bits 6 --length $L --psixmax $PXM --psikmax $PKM --qnum-n $QN --qnum-m $QM --delta-t 0.01 --interval-time $IT --total-time $TT
# python time_evo_classic_2Dh1.py --bits 7 --length $L --psixmax $PXM --psikmax $PKM --qnum-n $QN --qnum-m $QM  --delta-t 0.005 --interval-time $IT --total-time $TT
# python time_evo_classic_2Dh1.py --bits 8 --length $L --psixmax $PXM --psikmax $PKM --qnum-n $QN --qnum-m $QM  --delta-t 0.001 --interval-time $IT --total-time $TT
# python time_evo_classic_2Dh1.py --bits 9 --length $L --psixmax $PXM --psikmax $PKM --qnum-n $QN --qnum-m $QM --delta-t 0.0001 --interval-time $IT --total-time $TT

L=32
TT=16
IT=0.2
QN=1
QM=0
PXM=0.4
PKM=2.2
# python time_evo_classic_2Dh1.py --bits 6 --length $L --psixmax $PXM --psikmax $PKM --qnum-n $QN --qnum-m $QM --delta-t 0.01 --interval-time $IT --total-time $TT
# python time_evo_classic_2Dh1.py --bits 7 --length $L --psixmax $PXM --psikmax $PKM --qnum-n $QN --qnum-m $QM  --delta-t 0.005 --interval-time $IT --total-time $TT
# python time_evo_classic_2Dh1.py --bits 8 --length $L --psixmax $PXM --psikmax $PKM --qnum-n $QN --qnum-m $QM  --delta-t 0.001 --interval-time $IT --total-time $TT
# python time_evo_classic_2Dh1.py --bits 9 --length $L --psixmax $PXM --psikmax $PKM --qnum-n $QN --qnum-m $QM --delta-t 0.0005 --interval-time $IT --total-time $TT

QN=1
QM=1
PXM=0.2
PKM=1.0
# python time_evo_classic_2Dh1.py --bits 6 --length $L --psixmax $PXM --psikmax $PKM --qnum-n $QN --qnum-m $QM --delta-t 0.01 --interval-time $IT --total-time $TT
# python time_evo_classic_2Dh1.py --bits 7 --length $L --psixmax $PXM --psikmax $PKM --qnum-n $QN --qnum-m $QM  --delta-t 0.005 --interval-time $IT --total-time $TT
# python time_evo_classic_2Dh1.py --bits 8 --length $L --psixmax $PXM --psikmax $PKM --qnum-n $QN --qnum-m $QM  --delta-t 0.001 --interval-time $IT --total-time $TT
# python time_evo_classic_2Dh1.py --bits 9 --length $L --psixmax $PXM --psikmax $PKM --qnum-n $QN --qnum-m $QM --delta-t 0.0005 --interval-time $IT --total-time $TT

IT=0.5
TT=64
# python time_evo_classic_2Dh1.py --bits 6 --length $L --psixmax $PXM --psikmax $PKM --qnum-n $QN --qnum-m $QM --delta-t 0.01 --interval-time $IT --total-time $TT
# python time_evo_classic_2Dh1.py --bits 7 --length $L --psixmax $PXM --psikmax $PKM --qnum-n $QN --qnum-m $QM  --delta-t 0.005 --interval-time $IT --total-time $TT
# python time_evo_classic_2Dh1.py --bits 8 --length $L --psixmax $PXM --psikmax $PKM --qnum-n $QN --qnum-m $QM  --delta-t 0.001 --interval-time $IT --total-time $TT
# python time_evo_classic_2Dh1.py --bits 9 --length $L --psixmax $PXM --psikmax $PKM --qnum-n $QN --qnum-m $QM --delta-t 0.0005 --interval-time $IT --total-time $TT


# optimal L, deltat
# PSI(0,0)
# for EPS in 1.000 0.707 0.500 0.353 0.250 0.176 0.125; do
#     python time_evo_classic_2Dh1.py --bits 6 --length 5 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.00100 --interval-time 0.2 --total-time 4.0
#     python time_evo_classic_2Dh1.py --bits 7 --length 5 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.00050 --interval-time 0.2 --total-time 4.0
#     python time_evo_classic_2Dh1.py --bits 8 --length 6 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.00010 --interval-time 0.2 --total-time 3.2
#     python time_evo_classic_2Dh1.py --bits 9 --length 7 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.00005 --interval-time 0.2 --total-time 3.2
# done
# EPS=0.250
# python time_evo_classic_2Dh1.py --bits 6 --length 5 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.00100 --interval-time 0.2 --total-time 4.0
# python time_evo_classic_2Dh1.py --bits 7 --length 5 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.00010 --interval-time 0.2 --total-time 4.0
# python time_evo_classic_2Dh1.py --bits 8 --length 6 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.00010 --interval-time 0.2 --total-time 4.0
# python time_evo_classic_2Dh1.py --bits 9 --length 7 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.00005 --interval-time 0.2 --total-time 4.0

# PSI(1,0)
PO=rofs
TO=2
for EPS in 1.000 0.707 0.500 0.353 0.250 0.176 0.125; do
    python time_evo_classic_2Dh1.py --bits 6 --trotter-order $TO --length 18 --psixmax 0.4 --psikmax 2.2 --qnum-n 1 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.0100 --interval-time 0.5 --total-time 16 &
    python time_evo_classic_2Dh1.py --bits 7 --trotter-order $TO --length 21 --psixmax 0.4 --psikmax 2.2 --qnum-n 1 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.0050 --interval-time 0.5 --total-time 16 &
    python time_evo_classic_2Dh1.py --bits 8 --trotter-order $TO --length 24 --psixmax 0.4 --psikmax 2.2 --qnum-n 1 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.0010 --interval-time 0.5 --total-time 16 &
    python time_evo_classic_2Dh1.py --bits 9 --trotter-order $TO --length 27 --psixmax 0.4 --psikmax 2.2 --qnum-n 1 --qnum-m 0 --pole $PO --eps $EPS --delta-t 0.0005 --interval-time 0.5 --total-time 16
done


# PSI(1,1)
# for TT in 16 30; do
#     python time_evo_classic_2Dh1.py --bits 6 --length 25 --psixmax 0.2 --psikmax 1.0 --qnum-n 1 --qnum-m 1 --pole $PO --eps $EPS --delta-t 0.0100 --interval-time 0.5 --total-time $TT
#     python time_evo_classic_2Dh1.py --bits 7 --length 30 --psixmax 0.2 --psikmax 1.0 --qnum-n 1 --qnum-m 1 --pole $PO --eps $EPS --delta-t 0.0100 --interval-time 0.5 --total-time $TT
#     python time_evo_classic_2Dh1.py --bits 8 --length 34 --psixmax 0.2 --psikmax 1.0 --qnum-n 1 --qnum-m 1 --pole $PO --eps $EPS --delta-t 0.0050 --interval-time 0.5 --total-time $TT
#     python time_evo_classic_2Dh1.py --bits 9 --length 39 --psixmax 0.2 --psikmax 1.0 --qnum-n 1 --qnum-m 1 --pole $PO --eps $EPS --delta-t 0.0010 --interval-time 0.5 --total-time $TT
# done