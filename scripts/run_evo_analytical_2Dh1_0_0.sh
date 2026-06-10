#!/bin/sh -e

#USE_SAVED_DATA=--use-saved-data

# optimal L, deltat
# PSI(0,0)
python time_evo_analytic_2Dh1.py --bits 6 --length 5 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --delta-t 0.00100 --interval-time 0.2 --total-time 4.0
python time_evo_analytic_2Dh1.py --bits 7 --length 5 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --delta-t 0.00010 --interval-time 0.2 --total-time 4.0
python time_evo_analytic_2Dh1.py --bits 8 --length 6 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --delta-t 0.00010 --interval-time 0.2 --total-time 4.0
python time_evo_analytic_2Dh1.py --bits 9 --length 7 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --delta-t 0.00005 --interval-time 0.2 --total-time 4.0

# PSI(1,0)
# python time_evo_analytic_2Dh1.py --bits 6 --length 18 --psixmax 0.4 --psikmax 2.2 --qnum-n 1 --qnum-m 0 --delta-t 0.0100 --interval-time 0.5 --total-time 16
# python time_evo_analytic_2Dh1.py --bits 7 --length 21 --psixmax 0.4 --psikmax 2.2 --qnum-n 1 --qnum-m 0 --delta-t 0.0050 --interval-time 0.5 --total-time 16
# python time_evo_analytic_2Dh1.py --bits 8 --length 24 --psixmax 0.4 --psikmax 2.2 --qnum-n 1 --qnum-m 0 --delta-t 0.0010 --interval-time 0.5 --total-time 16
# python time_evo_analytic_2Dh1.py --bits 9 --length 27 --psixmax 0.4 --psikmax 2.2 --qnum-n 1 --qnum-m 0 --delta-t 0.0005 --interval-time 0.5 --total-time 16

# # PSI(1,1)
# for TT in 16 30; do
#     python time_evo_analytic_2Dh1.py --bits 6 --length 25 --psixmax 0.2 --psikmax 1.0 --qnum-n 1 --qnum-m 1 --delta-t 0.0100 --interval-time 0.5 --total-time $TT
#     python time_evo_analytic_2Dh1.py --bits 7 --length 30 --psixmax 0.2 --psikmax 1.0 --qnum-n 1 --qnum-m 1 --delta-t 0.0100 --interval-time 0.5 --total-time $TT
#     python time_evo_analytic_2Dh1.py --bits 8 --length 34 --psixmax 0.2 --psikmax 1.0 --qnum-n 1 --qnum-m 1 --delta-t 0.0050 --interval-time 0.5 --total-time $TT
#     python time_evo_analytic_2Dh1.py --bits 9 --length 39 --psixmax 0.2 --psikmax 1.0 --qnum-n 1 --qnum-m 1 --delta-t 0.0010 --interval-time 0.5 --total-time $TT
# done
