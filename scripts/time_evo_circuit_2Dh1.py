import os, argparse

from crsq_xp.circuits import time_evo_2Dh1

from crsq.blocks.time_evolution.spec import (
    SUZUKI_TROTTER_QROM,
    SUZUKI_TROTTER_ARITHMETIC,
)

import logging

logger = logging.getLogger("crsq_xp.scripts")


def run_experiment(driver: time_evo_2Dh1.Driver2D):

    driver.draw_circuits()
    if driver.use_saved_data:
        logger.info("skip running the simulator")
    else:
        driver.run_circuit()
    driver.draw_graph()
    logger.info("done")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="time_evo_circuit_2Dh1", description="Time evolution of H atom 2D model"
    )
    parser.add_argument("--gpu", help="Use GPU (default)", action="store_true")
    parser.add_argument("--cpu", help="Use CPU", action="store_true")
    parser.add_argument(
        "--cuStateVec", help="Use cuStateVec (default)", action="store_true"
    )
    parser.add_argument("--stateVec", help="Use stateVector", action="store_true")
    parser.add_argument(
        "--double", help="Use double precision (default)", action="store_true"
    )
    parser.add_argument("--single", help="Use single precision", action="store_true")
    parser.add_argument("--bits", type=int, default=5)
    parser.add_argument(
        "--trotter-order", type=int, default=1,
        help="Order of the Trotter decomposition (default: 1)"
    )
    parser.add_argument("--signed", help="Use signed coordinates (default)", action="store_true")
    parser.add_argument("--unsigned", help="Use unsigned coordinates", action="store_true")
    parser.add_argument("--qnum-n", type=int, required=True)
    parser.add_argument("--qnum-m", type=int, required=True)
    parser.add_argument("--length", type=float, default=16.0)
    parser.add_argument(
        "--psixmax", type=float, default=0.2, help="max value of the wave function x"
    )
    parser.add_argument(
        "--psikmax", type=float, default=0.2, help="max value of the wave function k"
    )
    parser.add_argument("--delta-t", type=float, required=True)
    parser.add_argument("--num-elec", type=int, default=1)
    parser.add_argument("--num-nucl", type=int, default=1)
    parser.add_argument("--dpi", type=int, default=None, help="DPI for output images (default=None)")
    parser.add_argument("--plot-type", type=str, default="3d-3qp", choices=["2d", "3d", "3d-re", "3d-3", "3d-3qp"])
    parser.add_argument(
        "--use-saved-data",
        help="skip calculation and use logged data",
        action="store_true",
    )
    parser.add_argument("--save-psi2", help="save psi before and after Hp", action="store_true")
    parser.add_argument(
        "--pole", type=str, default="r0lim", choices=["r0lim", "r0", "r0new", "rofs"],
        help="Pole mitigation method for the potential"
    )
    parser.add_argument(
        "--eps", type=float, default=0.25, help="Epsilon for pole mitigation (for r0lim and rofs)"
    )
    args = parser.parse_args()

    if args.gpu or not args.cpu:
        device = "GPU"
    else:
        device = "CPU"

    if args.cuStateVec or not args.stateVec:
        stateVec_type = "cuStateVec"
        enable_cuStateVec = True
    else:
        stateVec_type = "statevector"
        enable_cuStateVec = False

    if args.double or not args.single:
        precision = "double"
    else:
        precision = "single"

    if args.signed or not args.unsigned:
        slabel = "signed"
        signed_flag = True
    else:
        slabel="unsigned"
        signed_flag = False

    if args.use_saved_data:
        use_saved_data = True
    else:
        use_saved_data = False

    dim = 2
    qn = args.qnum_n
    qm = args.qnum_m
    delta_t = args.delta_t

    trotter_order = args.trotter_order
    total_time = args.num_elec * args.num_nucl * delta_t
    interval_time = args.num_elec * delta_t
    pole_path= f"{args.pole}_{args.eps:.3f}"
    tag = f"{device}_{stateVec_type}_{precision}/n{qn}_m{qm}_TO{trotter_order}_{pole_path}/{args.bits}b_L{args.length}_T{total_time}_iT{interval_time}_dt{delta_t}"

    outdir = "onedrive.lnk/circuits2D/" + tag
    os.makedirs(outdir, exist_ok=True)
    logfilename = outdir + "/circuit_2D.log"
    if os.path.exists(logfilename):
        os.truncate(logfilename, 0)
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s [%(name)s] %(message)s",
        filename=logfilename,
        encoding="utf-8",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.getLogger("crsq").setLevel(logging.INFO)
    logging.getLogger("crsq_xp").setLevel(logging.INFO)
    logger.setLevel(logging.INFO)
    print("Log file: ", logfilename)

    logger.info("Device : %s", device)
    logger.info("enable_cuStateVec : %s", enable_cuStateVec)
    logger.info("Precision : %s", precision)
    logger.info("n1 : %d", args.bits)
    logger.info("signed : %d", signed_flag)
    logger.info("L: %f", args.length)
    logger.info("delta_t: %f", args.delta_t)
    logger.info("num nucl iters : %d", args.num_nucl)
    logger.info("num elec iters : %d", args.num_elec)
    logger.info("qn : %d", args.qnum_n)
    logger.info("qm : %d", args.qnum_m)
    logger.info("trotter order : %d", trotter_order)
    logger.info("pole mitigation : %s", args.pole)
    logger.info("eps for pole mitigation : %f", args.eps)
    logger.info("use saved data : %s", use_saved_data)
    logger.info("outdir : %s", outdir)

    driver = time_evo_2Dh1.Driver2D(
        outdir=outdir,
        device=device,
        enable_cuStateVec=enable_cuStateVec,
        dim=dim,
        length=args.length,
        psixmax=args.psixmax,
        psikmax=args.psikmax,
        qn=args.qnum_n,
        qm=args.qnum_m,
        trotter_order=trotter_order,
        pole_mitigation=args.pole,
        eps=args.eps,
        delta_t=delta_t,
        precision=precision,
        n1=args.bits,
        signed=signed_flag,
        num_nucl_iters=args.num_nucl,
        num_elec_iters=args.num_elec,
        plot_type=args.plot_type,
        dpi=args.dpi,
        use_saved_data=use_saved_data,
        save_psi2=args.save_psi2
    )
    try:
        run_experiment(driver)
    except ValueError as e:
        logger.error("ValueError: %s", e)
        print("ValueError: ", e)
