#!/bin/sh -e

L=24
NN=63
#USE_SAVED_DATA=--use-saved-data
#python time_evo_circuit_1Dh1.py --STAR --bits 6 --length $L --x0 0 --odd --qn 1 --delta-t 0.05 --num-elec 4 --num-nucl $NN $USE_SAVED_DATA


L=24
NN=32
# python time_evo_circuit_1Dh1.py --STAR --bits 7 --length $L --x0 0 --odd --qn 1 --delta-t 0.01 --num-elec 20 --num-nucl $NN $USE_SAVED_DATA

# opt

USE_SAVED_DATA=--use-saved-data
python time_evo_circuit_1Dh1.py --STAR --bits 6 --length 15 --x0 0 --odd --qn 1 --trotter-order 1 --delta-t 0.010 --num-elec 20 --num-nucl 63 $USE_SAVED_DATA
#python time_evo_circuit_1Dh1.py --STAR --bits 6 --length 15 --x0 0 --odd --qn 1 --delta-t 0.010 --num-elec 20 --num-nucl 2 $USE_SAVED_DATA
# python time_evo_circuit_1Dh1.py --STAR --bits 7 --length 17 --x0 0 --odd --qn 1 --delta-t 0.010 --num-elec 20 --num-nucl 63 $USE_SAVED_DATA
