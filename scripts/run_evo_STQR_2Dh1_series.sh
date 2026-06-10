#!/bin/sh -e


# optimal


USE_SAVED_DATA=
TO=2
python time_evo_circuit_2Dh1.py --bits 6 --length 5 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --trotter-order $TO --delta-t 0.001 --num-elec 200 --num-nucl 20 $USE_SAVED
python time_evo_circuit_2Dh1.py --bits 6 --length 18 --psixmax 0.4 --psikmax 2.2 --qnum-n 1 --qnum-m 0 --trotter-order $TO --delta-t 0.01 --num-elec 50 --num-nucl 60 $USE_SAVED
python time_evo_circuit_2Dh1.py --bits 6 --length 25 --psixmax 0.2 --psikmax 1.0 --qnum-n 1 --qnum-m 1 --trotter-order $TO --delta-t 0.01 --num-elec 50 --num-nucl 60 $USE_SAVED
