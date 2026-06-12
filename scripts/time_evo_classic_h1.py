import os, argparse, logging
from crsq_xp.classic import cu_suzuki_trotter1, params
from crsq.models import hydrogen1d

logger = logging.getLogger("crsq_xp.scripts")


def run_simulation(par: params.Params, basedir: str):
    # par = params.Params(n1=13, dimension=1, L=64, dt=1.0e-3, WM=4096)
    # delta_q0=par.dq / 2
    Q0 = par.x0
    logger.info("Q0=%f", Q0)
    odd_flag = True
    use_palma = False
    if use_palma:
        psifunc = hydrogen1d.PsiH1D_Palma(Q0=Q0, N=par.qn)
    else:
        psifunc = hydrogen1d.PsiH1D_Loudon(Q0=Q0, N=par.qn, odd=odd_flag)
    if par.use_fixed_point:
        vfunc = hydrogen1d.VHAtomDiscrete(Q0, par.dq, par.n1, 1)
    else:
        vfunc = hydrogen1d.VHAtom(Q0=Q0, dq=par.dq, Z=1)
    st = cu_suzuki_trotter1.SuzukiTrotter1(par, basedir, psifunc=psifunc, vfunc=vfunc)
    st.run_simulation()
    st.generate_animation_frames()


def run():
    parser = argparse.ArgumentParser(
        prog="time_evo_classic_h1",
        description="Time evolution of a hydrogen atom in 1D",
    )
    parser.add_argument(
        "--bits",
        type=int,
        default=6,
        help="Number of bits for the coordinate (default=6)",
    )
    parser.add_argument(
        "--signed", help="Use signed coordinates (default)", action="store_true"
    )
    parser.add_argument(
        "--unsigned", help="Use unsigned coordinates", action="store_true"
    )
    parser.add_argument(
        "--fixed-point", help="Use fixed point arithmetic", action="store_true"
    )
    parser.add_argument(
        "--length",
        type=float,
        default=16.0,
        help="Length of the 1D grid (default=16.0)",
    )
    parser.add_argument(
        "--psimax",
        type=float,
        default=0.6,
        help="max value of the wave function (default=0.6)",
    )
    parser.add_argument("--x0", type=float, required=True, help="atom position")
    parser.add_argument(
        "--qn",
        type=int,
        default=1,
        help="Quntum number for the wave function (default=1)",
    )
    parser.add_argument(
        "--delta-t", type=float, default=0.001, help="Time step (default=0.001)"
    )
    parser.add_argument(
        "--window-radius", type=int, help="P-space window radius (default=2^(bits-1))"
    )
    parser.add_argument(
        "--trotter-order",
        type=int,
        default=1,
        help="Order of Trotter decomposition (default=1)"
    )
    parser.add_argument(
        "--total-time", type=float, default=30.0, help="Total time (default=30.0)"
    )
    parser.add_argument(
        "--interval-time", type=float, default=0.1, help="Interval time (default=0.1)"
    )

    args = parser.parse_args()

    if args.signed or not args.unsigned:
        slabel = "signed"
        signed_flag = True
    else:
        slabel = "unsigned"
        signed_flag = False

    if args.window_radius is not None:
        window_radius = args.window_radius
    else:
        window_radius = 2 ** (args.bits - 1)

    num_elec = int((args.interval_time / args.delta_t) + 0.5)
    num_nucl = int((args.total_time / args.interval_time) + 0.5)

    parity = "odd"
    if args.fixed_point:
        fp_label = "_fixed"
    else:
        fp_label = ""
    configpath = f"1D_{args.bits}b_{slabel}{fp_label}_TO{args.trotter_order}/N{args.qn}{parity}_L{args.length}_X{args.x0}_WM{window_radius}/dt{args.delta_t}/{num_nucl}n.{num_elec}e"
    outdir = "onedrive.lnk/classic1D/" + configpath
    os.makedirs(outdir, exist_ok=True)
    logfilename = outdir + "/classic_h1.log"
    if os.path.exists(logfilename):
        os.truncate(logfilename, 0)
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s [%(name)s] %(message)s",
        filename=logfilename,
        encoding="utf-8",
        level=logging.WARNING,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.getLogger("crsq").setLevel(logging.INFO)
    logging.getLogger("crsq_xp").setLevel(logging.INFO)
    logger.setLevel(logging.INFO)
    print("Log file: ", logfilename)

    logger.info(f"Bits: {args.bits}")
    logger.info(f"Signed : {signed_flag}")
    logger.info(f"length : {args.length}")
    logger.info(f"window radius : {window_radius}")
    logger.info(f"Trotter order : {args.trotter_order}")
    logger.info(f"x0 : {args.x0}")
    logger.info(f"parity : {parity}")
    logger.info(f"qn : {args.qn}")
    logger.info(f"delta_t : {args.delta_t}")
    logger.info(f"num elec iters : {num_elec}")
    logger.info(f"num nucl iters : {num_nucl}")

    # 6 bit coordinates, 1D, length=16 a.u. (bohr), time step 1.0e-3 a.u., p-space window radius 64 grids
    par = params.Params(
        n1=args.bits,
        dimension=1,
        L=args.length,
        psixmax=args.psimax,
        psikmax=args.psimax,
        x0=args.x0,
        dt=args.delta_t,
        interval_time=args.interval_time,
        total_time=args.total_time,
        signed=signed_flag,
        use_fixed_point=args.fixed_point,
        WM=window_radius,
        qn=args.qn,
        trotter_order=args.trotter_order
    )
    run_simulation(par, outdir)


if __name__ == "__main__":
    run()
