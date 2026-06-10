#!/bin/sh -e

#USE_SAVED_DATA=--use-saved-data


# optimal L, deltat

TT=30
python time_evo_analytic_2Dh1.py --bits 6 --length 18 --psixmax 0.4 --psikmax 2.2 --qnum-n 1 --qnum-m 0 --delta-t 0.0100 --interval-time 0.5 --total-time $TT
python time_evo_analytic_2Dh1.py --bits 7 --length 21 --psixmax 0.4 --psikmax 2.2 --qnum-n 1 --qnum-m 0 --delta-t 0.0050 --interval-time 0.5 --total-time $TT
python time_evo_analytic_2Dh1.py --bits 8 --length 24 --psixmax 0.4 --psikmax 2.2 --qnum-n 1 --qnum-m 0 --delta-t 0.0010 --interval-time 0.5 --total-time $TT
python time_evo_analytic_2Dh1.py --bits 9 --length 27 --psixmax 0.4 --psikmax 2.2 --qnum-n 1 --qnum-m 0 --delta-t 0.0005 --interval-time 0.5 --total-time $TT
