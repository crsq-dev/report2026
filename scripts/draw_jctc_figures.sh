#!/bin/bash -ex

# wave function initial value 1D
python time_evo_analytic_1Dh1.py --bits 6 --length 15 --x0 0 --delta-t 0.010 --interval-time 0.2 --total-time 0.01 --window-radius 32 --dpi 300

# wave function initial value 2D
python draw_classic2d_frame.py --bits 6 --qnum-n 0 --qnum-m 0 --length 5 --psixmax 1.2 --psikmax 0.5 --delta-t 0.001 --interval-time 0.2 --total-time 4.0 --plot-type 3d-qp --time 0.0 --dpi 300
python draw_classic2d_frame.py --bits 6 --qnum-n 1 --qnum-m 0 --length 18 --psixmax 0.4 --psikmax 2.2 --delta-t 0.01 --interval-time 0.5 --total-time 30 --plot-type 3d-qp --time 0.0 --dpi 300
python draw_classic2d_frame.py --bits 6 --qnum-n 1 --qnum-m 1 --length 25 --psixmax 0.2 --psikmax 1.0 --delta-t 0.01 --interval-time 0.5 --total-time 30 --plot-type 3d-qp --time 0.0 --dpi 300

# circuit diagram 1D arithmetic.
USE_SAVED_DATA=--use-saved-data
python time_evo_circuit_1Dh1.py --STAR --bits 6 --length 15 --x0 0 --odd --qn 1 --trotter-order 1 --delta-t 0.010 --num-elec 20 --num-nucl 63 $USE_SAVED_DATA --dpi 300

TO=1
python time_evo_circuit_2Dh1.py --bits 6 --length 5 --psixmax 1.2 --psikmax 0.5 --qnum-n 0 --qnum-m 0 --trotter-order $TO --delta-t 0.001 --num-elec 200 --num-nucl 20 $USE_SAVED_DATA --dpi 300
