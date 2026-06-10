#!/bin/sh -e


# optimal
#USE_SAVED=--use-saved-data
USE_SAVED=

for TO in 1 2; do
    python time_evo_circuit_2Dh1.py --bits 6 --length 25 --psixmax 0.2 --psikmax 1.0 --qnum-n 1 --qnum-m 1 --trotter-order $TO --delta-t 0.01 --num-elec 50 --num-nucl 60 $USE_SAVED
done

