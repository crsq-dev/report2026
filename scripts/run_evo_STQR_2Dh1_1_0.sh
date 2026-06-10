#!/bin/sh -e

TT=3.2
IT=0.2
QN=0
QM=0
L=10
PXM=1.2
PKM=0.5
# USE_SAVED_DATA=--use-saved-data

# python time_evo_circuit_2Dh1.py --bits 6 --qnum-n $QN --qnum-m $QM --length $L --psixmax $PXM --psikmax $PKM --delta-t 0.001 --num-elec 200 --num-nucl 16 $USE_SAVED_DATA

# python time_evo_circuit_2Dh1.py --bits 6 --qnum-n $QN --qnum-m $QM --length $L --psixmax $PXM --psikmax $PKM --delta-t 0.001 --num-elec 50 --num-nucl 64 $USE_SAVED_DATA

# for debugging
IT=0.005
TT=0.02
# python time_evo_circuit_2Dh1.py --bits 6 --qnum-n $QN --qnum-m $QM --length $L --psixmax $PXM --psikmax $PKM --delta-t 0.001 --num-elec 1 --num-nucl 4 $USE_SAVED_DATA --save-psi2


TT=3.2
IT=0.2
QN=0
QM=0
L=12
PXM=1.2
PKM=0.5

# python time_evo_circuit_2Dh1.py --bits 6 --qnum-n $QN --qnum-m $QM --length $L --psixmax $PXM --psikmax $PKM --delta-t 0.005 --num-elec 40 --num-nucl 16 $USE_SAVED_DATA

# for debugging
IT=0.005
TT=0.02
# python time_evo_circuit_2Dh1.py --bits 6 --qnum-n $QN --qnum-m $QM --length $L --psixmax $PXM --psikmax $PKM --delta-t 0.005 --num-elec 1 --num-nucl 4 $USE_SAVED_DATA --save-psi2

# 7bit model has 28 bits! cant run.
#python time_evo_circuit_2Dh1.py --bits 7 --qnum-n $QN --qnum-m $QM --length $L --psixmax $PXM --psikmax $PKM --delta-t 0.0005 --num-elec 400 --num-nucl 32 $USE_SAVED_DATA
#python time_evo_circuit_2Dh1.py --bits 8 --qnum-n $QN --qnum-m $QM --length $L --psixmax $PXM --psikmax $PKM --delta-t 0.0001 --num-elec 2000 --num-nucl 32 $USE_SAVED_DATA


L=26
TT=16
IT=0.2
QN=1
QM=0
PXM=0.4
PKM=2.2
# python time_evo_circuit_2Dh1.py --bits 6 --qnum-n $QN --qnum-m $QM --length $L --psixmax $PXM --psikmax $PKM --delta-t 0.01 --num-elec 20 --num-nucl 80 $USE_SAVED_DATA

L=26
TT=15
IT=0.2
QN=1
QM=1
PXM=0.2
PKM=0.4
# python time_evo_circuit_2Dh1.py --bits 6 --qnum-n $QN --qnum-m $QM --length $L --psixmax $PXM --psikmax $PKM --delta-t 0.01 --num-elec 20 --num-nucl 80 $USE_SAVED_DATA

L=32
TT=16
IT=0.2
QN=1
QM=0
PXM=0.4
PKM=2.2
# python time_evo_circuit_2Dh1.py --bits 6 --qnum-n $QN --qnum-m $QM --length $L --psixmax $PXM --psikmax $PKM --delta-t 0.01 --num-elec 20 --num-nucl 80 $USE_SAVED_DATA


L=32
TT=15
IT=0.2
QN=1
QM=1
PXM=0.2
PKM=1.0
# python time_evo_circuit_2Dh1.py --bits 6 --qnum-n $QN --qnum-m $QM --length $L --psixmax $PXM --psikmax $PKM --delta-t 0.01 --num-elec 20 --num-nucl 80 $USE_SAVED_DATA

# optimal
#USE_SAVED=--use-saved-data
USE_SAVED=

for TO in 1 2; do
    python time_evo_circuit_2Dh1.py --bits 6 --length 18 --psixmax 0.4 --psikmax 2.2 --qnum-n 1 --qnum-m 0 --trotter-order $TO --delta-t 0.01 --num-elec 50 --num-nucl 60 $USE_SAVED
done


