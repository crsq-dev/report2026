#!/bin/sh -e

#USE_SAVED_DATA=--use-saved-data

# optimal L, deltat
# # PSI(1,1)
TT=30
python time_evo_analytic_2Dh1.py --bits 6 --length 25 --psixmax 0.2 --psikmax 1.0 --qnum-n 1 --qnum-m 1 --delta-t 0.0100 --interval-time 0.5 --total-time $TT
python time_evo_analytic_2Dh1.py --bits 7 --length 30 --psixmax 0.2 --psikmax 1.0 --qnum-n 1 --qnum-m 1 --delta-t 0.0100 --interval-time 0.5 --total-time $TT
python time_evo_analytic_2Dh1.py --bits 8 --length 34 --psixmax 0.2 --psikmax 1.0 --qnum-n 1 --qnum-m 1 --delta-t 0.0050 --interval-time 0.5 --total-time $TT
python time_evo_analytic_2Dh1.py --bits 9 --length 39 --psixmax 0.2 --psikmax 1.0 --qnum-n 1 --qnum-m 1 --delta-t 0.0010 --interval-time 0.5 --total-time $TT
