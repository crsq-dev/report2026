#!/bin/sh -e

# optimal
#USE_SAVED=--use-saved-data
USE_SAVED=

for TO in 1 2 ; do
    python time_evo_circuit_2Dh1.py --bits 6 --length 5 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --trotter-order $TO --delta-t 0.001 --num-elec 200 --num-nucl 20 $USE_SAVED
done

TO=2
# python time_evo_circuit_2Dh1.py --bits 6 --length 5 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --trotter-order $TO --save-psi2 --delta-t 0.001 --num-elec 2 --num-nucl 4 $USE_SAVED

