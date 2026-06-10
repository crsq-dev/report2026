import os, argparse, logging
from crsq_xp.classic import params, reference2d
from crsq.models import hydrogen2d

logger = logging.getLogger("crsq-explore.scripts")


def run_simulation(par: params.Params, basedir: str):
    if par.signed:
        Qx0 = 0
        Qy0 = 0
    else:
        Qx0 = par.L / 2
        Qy0 = par.L / 2
    psifunc2 = hydrogen2d.PsiH2D(Qx0=Qx0, Qy0=Qy0, dq=par.dq, n=par.qn, m=par.qm)
    vfunc2_2 = hydrogen2d.VHAtom2(Qx0=Qx0, Qy0=Qy0, dq=par.dq, r0=par.dq/2, Z=1)
    vfunc2_4 = hydrogen2d.VHAtom2(Qx0=Qx0, Qy0=Qy0, dq=par.dq, r0=par.dq/4, Z=1)
    vfunc2_8 = hydrogen2d.VHAtom2(Qx0=Qx0, Qy0=Qy0, dq=par.dq, r0=par.dq/8, Z=1)
    vfunc2_r0 = hydrogen2d.VHAtom2(Qx0=Qx0, Qy0=Qy0, dq=par.dq, r0=psifunc2.r0, Z=1)
    vfunc2_r0_new = hydrogen2d.VHAtom2(Qx0=Qx0, Qy0=Qy0, dq=par.dq, r0=psifunc2.r0_new, Z=1)
    vfuncs = {
        "Hp_2": vfunc2_2,
        "Hp_4": vfunc2_4,
        "Hp_8": vfunc2_8,
        "Hp_r0": vfunc2_r0,
        "Hp_r0_new": vfunc2_r0_new,
    }
    st = reference2d.Analytic2D(par, basedir, psifunc2=psifunc2, vfunc2=vfuncs)
    st.run_calculation()
    st.generate_animation_frames()


def run():
    parser = argparse.ArgumentParser(
        prog="time_evo_reference_2Dh1",
        description="Time evolution of a hydrogen atom in 2D",
    )
    parser.add_argument("--bits", type=int, default=5)
    parser.add_argument(
        "--signed", help="Use signed coordinates (default)", action="store_true"
    )
    parser.add_argument(
        "--unsigned", help="Use unsigned coordinates", action="store_true"
    )
    parser.add_argument(
        "--qnum-n", type=int, required=True, help="Principal quantum number"
    )
    parser.add_argument(
        "--qnum-m", type=int, required=True, help="Azimuthal quantum number"
    )
    parser.add_argument(
        "--length", type=float, default=16.0, help="Length of the 2D grid"
    )
    parser.add_argument(
        "--psixmax", type=float, default=0.2, help="max value of the wave function in x-space"
    )
    parser.add_argument(
        "--psikmax", type=float, default=0.2, help="max value of the wave function in k-space"
    )
    parser.add_argument("--delta-t", type=float, default=0.001)
    parser.add_argument("--interval-time", type=float, default=0.1)
    parser.add_argument("--total-time", type=float, default=30.0)
    parser.add_argument(
        "--plot-type",
        type=str,
        default="3d-3qp",
        choices=["none", "2d", "3d", "3d-re", "3d-qp", "3d-3", "3d-3qp"]
    )

    parser.add_argument("--clean", action="store_true", help="Clean report directory before running")

    parser.add_argument(
        "--use-saved-data",
        help="skip calculation and use logged data",
        action="store_true",
    )
    args = parser.parse_args()

    if args.signed or not args.unsigned:
        slabel = "signed"
        signed_flag = True
    else:
        slabel = "unsigned"
        signed_flag = False
    if args.use_saved_data:
        use_saved_data = True
    else:
        use_saved_data = False

    configpath = f"{args.bits}b_{slabel}_L{args.length}_n{args.qnum_n}_m{args.qnum_m}/dt{args.delta_t}_T{args.total_time}"
    outdir = "onedrive.lnk/analytic2D/" + configpath
    os.makedirs(outdir, exist_ok=True)
    logfilename = outdir + "/analytic_2Dh1.log"
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

    # 6 bit coordinates, 1D, length=16 a.u. (bohr), time step 1.0e-3 a.u., p-space window radius 64 grids
    par = params.Params(
        n1=args.bits,
        dimension=2,
        L=args.length,
        psixmax=args.psixmax,
        psikmax=args.psikmax,
        dt=args.delta_t,
        interval_time=args.interval_time,
        total_time=args.total_time,
        signed=signed_flag,
        WM=16,
        trotter_order=2,
        qn=args.qnum_n,
        qm=args.qnum_m,
        pole_mitigation="none",
        eps=0,
        plot_type=args.plot_type,
        clean_report_dir=args.clean,
        use_saved_data=use_saved_data,
    )

    run_simulation(par, outdir)


if __name__ == "__main__":
    run()
