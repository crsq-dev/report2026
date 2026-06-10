import os, argparse

from crsq_xp.circuits import time_evo_h1

from crsq.blocks.time_evolution.spec import (
    SUZUKI_TROTTER_ARITHMETIC,
    SUZUKI_TROTTER_QROM,
)

import logging

logger = logging.getLogger("crsq_xp.scripts")


def run_experiment(driver: time_evo_h1.Driver1D):

    driver.draw_circuits()
    driver.run_circuit() # will skip simulation if use_saved_data is True
    driver.draw_graph()
    logger.info("done")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="time_evo_circuit_1Dh1", description="Time evolution of H atom"
    )
    parser.add_argument("--gpu", help="Use GPU (default)", action="store_true")
    parser.add_argument("--cpu", help="Use CPU", action="store_true")
    parser.add_argument("--cuStateVec", help="Use cuStateVec (default)", action="store_true")
    parser.add_argument("--stateVec", help="Use stateVector", action="store_true")
    parser.add_argument("--STAR", help="Use arithmetic gates for potential (default)", action="store_true")
    parser.add_argument("--STQR", help="Use QROM gates for potential", action="store_true")
    parser.add_argument("--double", help="Use double precision (default)", action="store_true")
    parser.add_argument("--single", help="Use single precision", action="store_true")
    parser.add_argument("--bits", type=int, required=True, help="Number of bits for the coordinate")
    parser.add_argument("--signed", help="Use signed coordinates (default)", action="store_true")
    parser.add_argument("--unsigned", help="Use unsigned coordinates", action="store_true")
    parser.add_argument("--trotter-order", help="Order of Trotter decomposition", type=int, default=1)
    parser.add_argument("--length", type=float, required=True, help="simulation space length")
    parser.add_argument("--psimax", type=float, default=0.6, help="max value of the wave function (default=0.6)")
    parser.add_argument("--window-radius", type=int, help="P-space window radius (default=2^(bits-1))")
    parser.add_argument("--x0", type=float, required=True, help="atom position")
    parser.add_argument("--odd", help="Odd parity wave function (default)", action="store_true")
    parser.add_argument("--even", help="Even parity wave function", action="store_true")
    parser.add_argument("--qn", type=int, help="Quntum number for the wave function", required=True)
    parser.add_argument("--delta-t", type=float, required=True)
    parser.add_argument("--num-elec", type=int, required=True, help="Number of electron iterations")
    parser.add_argument("--num-nucl", type=int, required=True, help="Number of nucleus iterations")
    parser.add_argument("--dpi", type=int, default=None, help="DPI for output figures (default=None)")
    parser.add_argument("--use-saved-data", help="skip calculation and use logged data", action="store_true")
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
    
    if args.STAR or not args.STQR:
        st_method = SUZUKI_TROTTER_ARITHMETIC
        st_method_label = 'arithmetic'
    else:
        st_method = SUZUKI_TROTTER_QROM
        st_method_label = 'look-up'

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

    if args.window_radius is not None:
        window_radius = args.window_radius
    else:
        window_radius = 1 << (args.bits-1)

    if args.odd or not args.even:
        parity = 'odd'
    else:
        parity = 'even'
    
    if args.use_saved_data:
        use_saved_data = True
    else:
        use_saved_data = False

    tag = f"{device}_{stateVec_type}_{precision}_{args.bits}b{slabel}_TO{args.trotter_order}/N{args.qn}{parity}_L{args.length}_X{args.x0}/dt{args.delta_t:.3f}/{args.num_nucl}n.{args.num_elec}e/{st_method}"

    outdir = "onedrive.lnk/circuits1D/" + tag
    os.makedirs(outdir, exist_ok=True)
    logfilename = outdir + f"/time_evo_h1_{st_method}.log"
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

    logger.info(f"Device : {device}")
    logger.info(f"enable_cuStateVec : {stateVec_type}")
    logger.info(f"ST method : {st_method}")
    logger.info(f"Precision : {precision}")
    logger.info(f"Bits: {args.bits}")
    logger.info(f"Signed : {signed_flag}")
    logger.info(f"Order of Trotter decomposition : {args.trotter_order}")
    logger.info(f"length : {args.length}")
    logger.info(f"window radius : {window_radius}")
    logger.info(f"x0 : {args.x0}")
    logger.info(f"parity : {parity}")
    logger.info(f"qn : {args.qn}")
    logger.info(f"trotter_order : {args.trotter_order}")
    logger.info(f"delta_t : {args.delta_t}")
    logger.info(f"num elec iters : {args.num_elec}")
    logger.info(f"num nucl iters : {args.num_nucl}")
    logger.info(f"use saved data : {args.use_saved_data}")
    logger.info(f"Tag : {tag}")

    driver = time_evo_h1.Driver1D(
        outdir,
        device=device,
        enable_cuStateVec=enable_cuStateVec,
        precision=precision,
        delta_t=args.delta_t,
        n1=args.bits,
        signed=signed_flag,
        parity=parity,
        qn=args.qn,
        length=args.length,
        psimax=args.psimax,
        window_radius=window_radius,
        trotter_order=args.trotter_order,
        x0=args.x0,
        num_elec_iters=args.num_elec,
        num_nucl_iters=args.num_nucl,
        st_method=st_method,
        st_method_label=st_method_label,
        dpi=args.dpi,
        use_saved_data=use_saved_data,
    )
    run_experiment(driver)
