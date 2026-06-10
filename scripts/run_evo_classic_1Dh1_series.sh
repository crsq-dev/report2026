#!/bin/sh -e
L=16
TT=12.6
# python time_evo_classic_h1.py --bits 6 --length $L --x0 0 --delta-t 0.01 --interval-time 0.2 --total-time $TT --window-radius 32
# python time_evo_classic_h1.py --bits 7 --length $L --x0 0 --delta-t 0.005 --interval-time 0.2 --total-time $TT  --window-radius 64
# python time_evo_classic_h1.py --bits 8 --length $L --x0 0 --delta-t 0.001 --interval-time 0.2 --total-time $TT  --window-radius 128
# python time_evo_classic_h1.py --bits 9 --length $L --x0 0 --delta-t 0.0005 --interval-time 0.2 --total-time $TT  --window-radius 256
# python time_evo_classic_h1.py --bits 10 --length $L --x0 0 --delta-t 0.0001 --interval-time 0.2 --total-time $TT  --window-radius 512

# python time_evo_classic_h1.py --bits 7 --length $L --x0 0 --delta-t 0.005 --interval-time 0.2 --total-time 6.4  --window-radius 64

L=24
TT=12.6
# python time_evo_classic_h1.py --bits 6 --length $L --x0 0 --delta-t 0.05 --interval-time 0.2 --total-time $TT --window-radius 32
# python time_evo_classic_h1.py --bits 7 --length $L --x0 0 --delta-t 0.01 --interval-time 0.2 --total-time $TT  --window-radius 64
# python time_evo_classic_h1.py --bits 8 --length $L --x0 0 --delta-t 0.005 --interval-time 0.2 --total-time $TT  --window-radius 128
# python time_evo_classic_h1.py --bits 9 --length $L --x0 0 --delta-t 0.001 --interval-time 0.2 --total-time $TT  --window-radius 256

# python time_evo_classic_h1.py --bits 7 --length $L --x0 0 --delta-t 0.01 --interval-time 0.2 --total-time 6.4  --window-radius 64

for TO in 1 2; do
    # optimal
    # python time_evo_classic_h1.py --bits 6 --trotter-order $TO --length 15 --x0 0 --delta-t 0.010 --interval-time 0.2 --total-time 12.6 --window-radius 32
    # python time_evo_classic_h1.py --bits 7 --trotter-order $TO --length 17 --x0 0 --delta-t 0.010 --interval-time 0.2 --total-time 12.6 --window-radius 64
    # python time_evo_classic_h1.py --bits 8 --trotter-order $TO --length 20 --x0 0 --delta-t 0.001 --interval-time 0.2 --total-time 12.6 --window-radius 128
    # python time_evo_classic_h1.py --bits 9 --trotter-order $TO --length 23 --x0 0 --delta-t 0.001 --interval-time 0.2 --total-time 12.6 --window-radius 256
    # for comparison with arithmetic gates
    python time_evo_classic_h1.py --bits 6 --trotter-order $TO --fixed-point --length 15 --x0 0 --delta-t 0.010 --interval-time 0.2 --total-time 12.6 --window-radius 32
done



# suboptimal examples
# L = 0.8 x optimal
#python time_evo_classic_h1.py --bits 6 --length 11 --x0 0 --delta-t 0.01 --interval-time 0.2 --total-time 12.6 --window-radius 32

# L = 1.2 x optimal
#python time_evo_classic_h1.py --bits 6 --length 17 --x0 0 --delta-t 0.01 --interval-time 0.2 --total-time 12.6 --window-radius 32

# dt = 2 x optimal
# python time_evo_classic_h1.py --bits 6 --length 15 --x0 0 --delta-t 0.02 --interval-time 0.2 --total-time 12.6 --window-radius 32