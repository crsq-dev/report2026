#!/bin/bash -e

# script to store data and images used in the paper to the published data directory
SRC_ROOT=onedrive.lnk
DEST_ROOT=report2026_data
mkdir -p $DEST_ROOT

FILES=(
    analytic1D/1D_6b_signed/N1_L15.0_X0.0_WM32/dt0.01/0n.20e/images300dpi/t_00.000.png
    analytic1D/1D_6b_signed/N1_L15.0_X0.0_WM32/dt0.01/0n.20e/frames/state_vector_0.000_p.csv
    analytic1D/1D_6b_signed/N1_L15.0_X0.0_WM32/dt0.01/0n.20e/frames/state_vector_0.000_q.csv
    classic2D/n0_m0_TO2_r0lim_0.250/6b_L5.0_T4.0_iT0.2_dt0.001/images300dpi/t_00.000_3d-qp.png
    classic2D/n0_m0_TO2_r0lim_0.250/6b_L5.0_T4.0_iT0.2_dt0.001/frames/00.000.p.csv
    classic2D/n0_m0_TO2_r0lim_0.250/6b_L5.0_T4.0_iT0.2_dt0.001/frames/00.000.q.csv
    classic2D/n1_m0_TO2_r0lim_0.250/6b_L18.0_T30.0_iT0.5_dt0.01/images300dpi/t_00.000_3d-qp.png
    classic2D/n1_m0_TO2_r0lim_0.250/6b_L18.0_T30.0_iT0.5_dt0.01/frames/00.000.p.csv
    classic2D/n1_m0_TO2_r0lim_0.250/6b_L18.0_T30.0_iT0.5_dt0.01/frames/00.000.q.csv
    classic2D/n1_m1_TO2_r0lim_0.250/6b_L25.0_T30.0_iT0.5_dt0.01/images300dpi/t_00.000_3d-qp.png
    classic2D/n1_m1_TO2_r0lim_0.250/6b_L25.0_T30.0_iT0.5_dt0.01/frames/00.000.p.csv
    classic2D/n1_m1_TO2_r0lim_0.250/6b_L25.0_T30.0_iT0.5_dt0.01/frames/00.000.q.csv
    count_gates/hamiltonian-gatecount-revision2.png
    count_gates/hamiltonian-gatecount-arith-elec-potential-d1-2-n9-10.csv
    count_gates/hamiltonian-gatecount-arith-elec-potential-d1-3-n5-8.csv
    count_gates/hamiltonian-gatecount-embed-d1-2-n8-10.csv
    count_gates/hamiltonian-gatecount-embed-d1-3-n5-7.csv
    count_gates/hamiltonian-gatecount-embed-d3-3-n8-8.csv
    count_gates/hamiltonian-gatecount-ucrz-d1-2-n8-10.csv
    count_gates/hamiltonian-gatecount-ucrz-d1-3-n5-7.csv
    count_gates/hamiltonian-gatecount-ucrz-d3-3-n8-9.csv
    compare2D/compare_energy_h2D_TO2_r0lim_0_0.png
    compare2D/compare_energy_h2D_TO2_r0lim_1_0.png
    compare2D/compare_energy_h2D_TO2_rofs_0_0.png
    compare2D/compare_energy_h2D_TO2_rofs_1_0.png
    dq_tradeoff2/eval1d_dq.png
    dq_tradeoff2/eval1d_dq.csv
    dq_tradeoff2/eval2d_dq_geom_0_0.png
    dq_tradeoff2/eval2d_geom_0_0.csv
    dq_tradeoff2/eval2d_dq_geom_1_0.png
    dq_tradeoff2/eval2d_geom_1_0.csv
    parameters/evaluator/graphs/t1.0/trotter_err_n0_m0_6b_t1.0.png
    parameters/evaluator/graphs/t1.0/trotter_err_n0_m0_6b_t1.0.csv
    parameters/evaluator/graphs/t1.0/trotter_err_n0_m0_9b_t1.0.png
    parameters/evaluator/graphs/t1.0/trotter_err_n0_m0_9b_t1.0.csv
    parameters/evaluator/graphs/t1.0/trotter_err_n1_m0_6b_t1.0.png
    parameters/evaluator/graphs/t1.0/trotter_err_n1_m0_6b_t1.0.csv
    parameters/evaluator/graphs/t1.0/trotter_err_n1_m0_9b_t1.0.png
    parameters/evaluator/graphs/t1.0/trotter_err_n1_m0_9b_t1.0.csv
    parameters/evaluator/graphs/t1.0/trotter_err_n1_m1_6b_t1.0.png
    parameters/evaluator/graphs/t1.0/trotter_err_n1_m1_6b_t1.0.csv
    parameters/evaluator/graphs/t1.0/trotter_err_n1_m1_9b_t1.0.png
    parameters/evaluator/graphs/t1.0/trotter_err_n1_m1_9b_t1.0.csv
    compare3D/compare_energy_h3D_TO2_r0lim_1_0_0.png
    parameters/evaluator/graphs/t30/trotter_err_n0_m0_6b_t30.png
    parameters/evaluator/graphs/t30/trotter_err_n0_m0_6b_t30.csv
    parameters/evaluator/graphs/t30/trotter_err_n0_m0_9b_t30.png
    parameters/evaluator/graphs/t30/trotter_err_n0_m0_9b_t30.csv
    parameters/evaluator/graphs/t30/trotter_err_n1_m0_6b_t30.png
    parameters/evaluator/graphs/t30/trotter_err_n1_m0_6b_t30.csv
    parameters/evaluator/graphs/t30/trotter_err_n1_m0_9b_t30.png
    parameters/evaluator/graphs/t30/trotter_err_n1_m0_9b_t30.csv
    parameters/evaluator/graphs/t30/trotter_err_n1_m1_6b_t30.png
    parameters/evaluator/graphs/t30/trotter_err_n1_m1_6b_t30.csv
    parameters/evaluator/graphs/t30/trotter_err_n1_m1_9b_t30.png
    parameters/evaluator/graphs/t30/trotter_err_n1_m1_9b_t30.csv
    )

for p in "${FILES[@]}"; do
    d=$(dirname $p)
    mkdir -p $DEST_ROOT/$d
    if [ ! -f $DEST_ROOT/$p ]; then
        cp -v $SRC_ROOT/$p $DEST_ROOT/$d
    fi
done


EPS2DFILES=(
    classic2D/n0_m0_TO2_rofs_0.250/6b_L5.0_T4.0_iT0.2_dt0.001/energy_trace.csv
    classic2D/n0_m0_TO2_rofs_0.250/7b_L5.0_T4.0_iT0.2_dt0.0001/energy_trace.csv
    classic2D/n0_m0_TO2_rofs_0.250/8b_L6.0_T4.0_iT0.2_dt0.0001/energy_trace.csv
    classic2D/n0_m0_TO2_rofs_0.250/9b_L7.0_T4.0_iT0.2_dt5e-05/energy_trace.csv
    classic2D/n1_m0_TO2_rofs_0.250/6b_L18.0_T30.0_iT0.5_dt0.01/energy_trace.csv
    classic2D/n1_m0_TO2_rofs_0.250/7b_L21.0_T30.0_iT0.5_dt0.005/energy_trace.csv
    classic2D/n1_m0_TO2_rofs_0.250/8b_L24.0_T30.0_iT0.5_dt0.001/energy_trace.csv
    classic2D/n1_m0_TO2_rofs_0.250/8b_L24.0_T30.0_iT0.5_dt0.001/energy_trace.csv
    classic2D/n1_m0_TO2_rofs_0.250/9b_L27.0_T30.0_iT0.5_dt0.0005/energy_trace.csv
    classic2D/n0_m0_TO2_r0lim_0.250/6b_L5.0_T4.0_iT0.2_dt0.001/energy_trace.csv
    classic2D/n0_m0_TO2_r0lim_0.250/7b_L5.0_T4.0_iT0.2_dt0.0001/energy_trace.csv
    classic2D/n0_m0_TO2_r0lim_0.250/8b_L6.0_T4.0_iT0.2_dt0.0001/energy_trace.csv
    classic2D/n0_m0_TO2_r0lim_0.250/9b_L7.0_T4.0_iT0.2_dt5e-05/energy_trace.csv
    classic2D/n1_m0_TO2_r0lim_0.250/6b_L18.0_T30.0_iT0.5_dt0.01/energy_trace.csv
    classic2D/n1_m0_TO2_r0lim_0.250/7b_L21.0_T30.0_iT0.5_dt0.005/energy_trace.csv
    classic2D/n1_m0_TO2_r0lim_0.250/8b_L24.0_T30.0_iT0.5_dt0.001/energy_trace.csv
    classic2D/n1_m0_TO2_r0lim_0.250/9b_L27.0_T30.0_iT0.5_dt0.0005/energy_trace.csv
)
EPS2D=(0.125 0.176 0.250 0.353 0.500 0.707 1.000)

for p in "${EPS2DFILES[@]}"; do
    for e in "${EPS2D[@]}"; do
        pp=$(echo $p | sed "s/0.250/$e/")
        d=$(dirname $pp)
        mkdir -p $DEST_ROOT/$d
        if [ ! -f $DEST_ROOT/$pp ]; then
            cp -v $SRC_ROOT/$pp $DEST_ROOT/$d
        fi
    done
done

EPS3DFILES=(
    classic3D/n1_l0_m0_TO2_r0lim_0.250/6b_L12.0_T12.6_iT0.2_dt0.005/energy_trace.csv
    classic3D/n1_l0_m0_TO2_r0lim_0.250/7b_L13.0_T12.6_iT0.2_dt0.001/energy_trace.csv
    classic3D/n1_l0_m0_TO2_r0lim_0.250/8b_L13.0_T12.6_iT0.2_dt0.0005/energy_trace.csv
)

EPS3D=(0.200 0.250 0.333 0.500 1.000)

for p in "${EPS3DFILES[@]}"; do
    for e in "${EPS3D[@]}"; do
        pp=$(echo $p | sed "s/0.250/$e/")
        d=$(dirname $pp)
        mkdir -p $DEST_ROOT/$d
        if [ ! -f $DEST_ROOT/$pp ]; then
            cp -v $SRC_ROOT/$pp $DEST_ROOT/$d
        fi
    done
done
