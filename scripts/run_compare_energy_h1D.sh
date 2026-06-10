#!/bin/sh -e

python compare_energy_h1D.py --bits 6 --signed --double --qn 1 --length 24 --x0 0 --delta-t 0.05 --num-elec 4 --num-nucl 63 --window-radius 32
python compare_energy_h1D.py --bits 7 --signed --double --qn 1 --length 24 --x0 0 --delta-t 0.01 --num-elec 20 --num-nucl 63 --window-radius 64
python compare_energy_h1D.py --bits 8 --signed --double --qn 1 --length 24 --x0 0 --delta-t 0.005 --num-elec 40 --num-nucl 63 --window-radius 128
python compare_energy_h1D.py --bits 9 --signed --double --qn 1 --length 24 --x0 0 --delta-t 0.001 --num-elec 200 --num-nucl 63 --window-radius 256

python compare_energy_h1D.py --bits 7 --signed --double --qn 1 --length 24 --x0 0 --delta-t 0.01 --num-elec 20 --num-nucl 32 --window-radius 64

python compare_energy_h1D.py --bits 6 --signed --double --qn 1 --length 15 --x0 0 --delta-t 0.010 --num-elec 20 --num-nucl 63 --window-radius 32
python compare_energy_h1D.py --bits 7 --signed --double --qn 1 --length 17 --x0 0 --delta-t 0.010 --num-elec 20 --num-nucl 63 --window-radius 64
python compare_energy_h1D.py --bits 8 --signed --double --qn 1 --length 20 --x0 0 --delta-t 0.001 --num-elec 200 --num-nucl 63 --window-radius 128
python compare_energy_h1D.py --bits 9 --signed --double --qn 1 --length 23 --x0 0 --delta-t 0.001 --num-elec 200 --num-nucl 63 --window-radius 256
