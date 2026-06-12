import os, argparse, logging
from crsq_xp.classic import cu_suzuki_trotter2, params
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
    # vfunc2 = hydrogen2d.VHAtom2(Qx0=Qx0, Qy0=Qy0, dq=par.dq, r0=par.dq/2, Z=1)
    # vfunc2 = hydrogen2d.VHAtom2(Qx0=Qx0, Qy0=Qy0, dq=par.dq, r0=par.dq/4, Z=1)
    # vfunc2 = hydrogen2d.VHAtom2(Qx0=Qx0, Qy0=Qy0, dq=par.dq, r0=psifunc2.r0, Z=1)
    # vfunc2 = hydrogen2d.VHAtom2(Qx0=Qx0, Qy0=Qy0, dq=par.dq, r0=psifunc2.r0_new, Z=1)
    if par.pole_mitigation == "rofs":
        vfunc2 = hydrogen2d.VHAtom2(Qx0=Qx0, Qy0=Qy0, dq=par.dq, r0=0, Z=1, eps=par.eps, frac_bits=par.frac_bits)
    else:
        vfunc2 = hydrogen2d.VHAtom2(Qx0=Qx0, Qy0=Qy0, dq=par.dq, r0=psifunc2.r0_for_pole(par.pole_mitigation, par.eps), Z=1, frac_bits=par.frac_bits)
    st = cu_suzuki_trotter2.SuzukiTrotter2(
        par, basedir, psifunc2=psifunc2, vfunc2=vfunc2
    )
    st.run_simulation()
    st.generate_animation_frames()


def run():
    parser = argparse.ArgumentParser(
        prog="time_evo_classic_2Dh1",
        description="Time evolution of a hydrogen atom in 1D",
    )
    parser.add_argument("--bits", type=int, default=6)
    parser.add_argument("--frac-bits", type=int, default=-1)
    parser.add_argument(
        "--trotter-order", type=int, default=1,
        help="Order of the Trotter decomposition (default: 1)"
    )
    parser.add_argument(
        "--qnum-n", type=int, required=True, help="Principal quantum number"
    )
    parser.add_argument(
        "--qnum-m", type=int, required=True, help="Azimuthal quantum number"
    )
    parser.add_argument(
        "--pole", type=str, default="r0lim", choices=["r0lim", "r0", "r0new", "rofs"],
        help="Pole mitigation method for the potential"
    )
    parser.add_argument(
        "--eps", type=float, default=0.25, help="Epsilon for pole mitigation (for r0lim and rofs)"
    )
    parser.add_argument(
        "--length", type=float, default=16.0, help="Length of the 2D grid"
    )
    parser.add_argument(
        "--psixmax", type=float, default=0.2, help="max value of the wave function x"
    )
    parser.add_argument(
        "--psikmax", type=float, default=0.2, help="max value of the wave function k"
    )
    parser.add_argument("--delta-t", type=float, default=0.001)
    parser.add_argument("--interval-time", type=float, default=0.1)
    parser.add_argument("--total-time", type=float, default=30.0)
    parser.add_argument(
        "--plot-type",
        type=str,
        default="3d-3qp",
        choices=["none", "2d", "3d", "3d-re", "3d-qp", "3d-3", "3d-3qp"],
    )
    parser.add_argument("--clean", action="store_true", help="Clean report directory before running")
    parser.add_argument("--window-radius", type=int, default=16)
    parser.add_argument("--save-psi2", help="save psi before and after Hp", action="store_true")

    args = parser.parse_args()

    signed_flag = True

    pole_path= f"{args.pole}_{args.eps:.3f}"
    if args.frac_bits >= 0:
        frac_spec = "_frac" + str(args.frac_bits)
    else:
        frac_spec = ""

    configpath = f"n{args.qnum_n}_m{args.qnum_m}_TO{args.trotter_order}_{pole_path}/{args.bits}b{frac_spec}_L{args.length}_T{args.total_time}_iT{args.interval_time}_dt{args.delta_t}"
    outdir = "onedrive.lnk/classic2D/" + configpath
    os.makedirs(outdir, exist_ok=True)
    logfilename = outdir + "/classic_2Dh1.log"
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
        WM=args.window_radius,
        trotter_order=args.trotter_order,
        qn=args.qnum_n,
        qm=args.qnum_m,
        pole_mitigation=args.pole,
        eps=args.eps,
        plot_type=args.plot_type,
        clean_report_dir=args.clean,
        save_psi2=args.save_psi2,
        frac_bits=args.frac_bits
    )

    run_simulation(par, outdir)


if __name__ == "__main__":
    run()
