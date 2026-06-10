#!/bin/sh -e

NN=63
L=15
#USE_SAVED_DATA=--use-saved-data

python time_evo_circuit_1Dh1.py --STQR --bits 6 --length $L --x0 0 --odd --qn 1 --delta-t 0.01 --num-elec 20 --num-nucl 63 $USE_SAVED_DATA
# python time_evo_circuit_1Dh1.py --STQR --bits 7 --length $L --x0 0 --odd --qn 1 --delta-t 0.01 --num-elec 20 --num-nucl 63 $USE_SAVED_DATA
# python time_evo_circuit_1Dh1.py --STQR --bits 8 --length $L --x0 0 --odd --qn 1 --delta-t 0.005 --num-elec 40 --num-nucl 63 $USE_SAVED_DATA
# python time_evo_circuit_1Dh1.py --STQR --bits 9 --length $L --x0 0 --odd --qn 1 --delta-t 0.001 --num-elec 200 --num-nucl 63 $USE_SAVED_DATA

# python time_evo_circuit_1Dh1.py --STQR --bits 7 --length $L --x0 0 --odd --qn 1 --delta-t 0.01 --num-elec 20 --num-nucl 32 $USE_SAVED_DATA

