""" draw a single frame from the h2 dataset.
"""

import os, argparse, logging
from crsq_xp.classic import params, draw_frame
from crsq.models import hydrogen2d

logger = logging.getLogger("crsq-explore.scripts")

def draw(par: params.Params, out_dir: str,  t: float):
    if par.signed:
        Qx0 = 0
        Qy0 = 0
    else:
        Qx0 = par.L / 2
        Qy0 = par.L / 2
    psifunc2 = hydrogen2d.PsiH2D(Qx0=Qx0, Qy0=Qy0, dq=par.dq, n=par.qn, m=par.qm)
    # vfunc2_2 = hydrogen2d.VHAtom2(Qx0=Qx0, Qy0=Qy0, dq=par.dq, r0=par.dq/2, Z=1)
    vfunc2_4 = hydrogen2d.VHAtom2(Qx0=Qx0, Qy0=Qy0, dq=par.dq, r0=par.dq/4, Z=1)
    drawer = draw_frame.DrawFrame2d(par, out_dir, psifunc2, vfunc2_4)
    drawer.draw_frame(t)


def run():
    parser = argparse.ArgumentParser(
        prog="draw_classic2d_frame",
        description="Draw a single frame from the classic2d dataset",
    )
    parser.add_argument("--bits", type=int, default=6)
    parser.add_argument(
        "--signed", help="Use signed coordinates (default)", action="store_true"
    )
    parser.add_argument(
        "--unsigned", help="Use unsigned coordinates", action="store_true"
    )
    parser.add_argument(
        "--trotter-order", type=int, default=2, help="Trotter order (default=2)"
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
        choices=["2d", "3d", "3d-re", "3d-qp", "3d-3", "3d-3qp"],
    )
    parser.add_argument("--window-radius", type=int, default=16)
    parser.add_argument("--time", type=float, help="frame time")
    parser.add_argument("--dpi", type=int, default=None, help="DPI of the output image")

    args = parser.parse_args()
    if args.signed or not args.unsigned:
        slabel = "signed"
        signed_flag = True
    else:
        slabel = "unsigned"
        signed_flag = False

    configpath = f"n{args.qnum_n}_m{args.qnum_m}_TO{args.trotter_order}_r0lim_0.250/{args.bits}b_L{args.length}_T{args.total_time}_iT{args.interval_time}_dt{args.delta_t}"
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
        trotter_order=args.trotter_order,
        WM=args.window_radius,
        qn=args.qnum_n,
        qm=args.qnum_m,
        plot_type=args.plot_type,
        dpi=args.dpi,

    )

    draw(par, outdir, args.time)

if __name__ == "__main__":
    run()
