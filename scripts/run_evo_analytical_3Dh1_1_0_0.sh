#!/bin/sh -e

#USE_SAVED_DATA=--use-saved-data

# PSI(1,0,0)
python time_evo_analytic_3Dh1.py --bits 6 --length 12 --psixmax 0.6 --psikmax 1.2 --qnum-n 1 --qnum-l 0 --qnum-m 0 --delta-t 0.00500 --interval-time 0.2 --total-time 12.6
python time_evo_analytic_3Dh1.py --bits 7 --length 13 --psixmax 0.6 --psikmax 1.2 --qnum-n 1 --qnum-l 0 --qnum-m 0 --delta-t 0.00100 --interval-time 0.2 --total-time 12.6
python time_evo_analytic_3Dh1.py --bits 8 --length 13 --psixmax 0.6 --psikmax 1.2 --qnum-n 1 --qnum-l 0 --qnum-m 0 --delta-t 0.00050 --interval-time 0.2 --total-time 12.6
