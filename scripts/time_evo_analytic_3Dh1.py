import os, argparse, logging
from crsq_xp.classic import params, reference3d
from crsq.models import hydrogen3d

logger = logging.getLogger("crsq-explore.scripts")


def run_simulation(par: params.Params, basedir: str):
    if par.signed:
        Qx0 = 0
        Qy0 = 0
        Qz0 = 0
    else:
        Qx0 = par.L / 2
        Qy0 = par.L / 2
        Qz0 = par.L / 2
    psifunc3 = hydrogen3d.PsiH3D(Qx0=Qx0, Qy0=Qy0, Qz0=Qz0, n=par.qn, l=par.ql, m=par.qm)

    vfunc3_1_5 = hydrogen3d.VHAtom3(Qx0=Qx0, Qy0=Qy0, Qz0=Qz0, dq=par.dq, reff=par.dq/1.5, Z=1)
    vfunc3_3 = hydrogen3d.VHAtom3(Qx0=Qx0, Qy0=Qy0, Qz0=Qz0, dq=par.dq, reff=par.dq/3, Z=1)
    vfunc3_6 = hydrogen3d.VHAtom3(Qx0=Qx0, Qy0=Qy0, Qz0=Qz0, dq=par.dq, reff=par.dq/6, Z=1)

    # 微小量近似をせず、円形領域で積分する式
    # vfunc2_r0 = hydrogen3d.VHAtom3(Qx0=Qx0, Qy0=Qy0, dq=par.dq, r0=psifunc3.r0, Z=1)
    # 微小量近似をせず、四角形領域で積分する式
    # vfunc2_r0_new = hydrogen3d.VHAtom3(Qx0=Qx0, Qy0=Qy0, dq=par.dq, r0=psifunc3.r0_new, Z=1)
    vfuncs = {
        "Hp_15": vfunc3_1_5,
        "Hp_3": vfunc3_3,
        "Hp_6": vfunc3_6,
        # "Hp_r0": vfunc2_r0,
        # "Hp_r0_new": vfunc2_r0_new,
    }
    st = reference3d.Analytic3D(par, basedir, psifunc3=psifunc3, vfunc3=vfuncs)
    st.run_calculation()
    st.generate_animation_frames()


def run():
    parser = argparse.ArgumentParser(
        prog="time_evo_reference_3Dh1",
        description="Time evolution of a hydrogen atom in 3D",
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
        "--qnum-l", type=int, required=True, help="Azimuthal quantum number"
    )
    parser.add_argument(
        "--qnum-m", type=int, required=True, help="Magnetic quantum number"
    )
    parser.add_argument(
        "--length", type=float, default=16.0, help="Length of the 3D grid"
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

    configpath = f"{args.bits}b_{slabel}_L{args.length}_n{args.qnum_n}_l{args.qnum_l}_m{args.qnum_m}/dt{args.delta_t}_T{args.total_time}"
    outdir = "onedrive.lnk/analytic3D/" + configpath
    os.makedirs(outdir, exist_ok=True)
    logfilename = outdir + "/analytic_3Dh1.log"
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
        dimension=3,
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
        ql=args.qnum_l,
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
