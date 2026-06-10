import logging
import os, argparse
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

logger = logging.getLogger("crsq_xp.scripts")
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def compare_energy(
    bits: int,
    signed_label: bool,
    precision: str,
    qnum_n: int,
    qnum_l: int,
    qnum_m: int,
    trotter_order: int,
    etot: float,
    ek: float,
    ep: float,
    ew: float,
    length: float,
    delta_t: float,
    interval_time: float,
    total_time: float,
):
    basedir = "onedrive.lnk"

    file_suffix = []

    hk_df = pd.DataFrame()
    hp_df = pd.DataFrame()
    htot_df = pd.DataFrame()
    autocorr_df = pd.DataFrame()

    analytic_filename = f"{basedir}/analytic3D/{bits}b_{signed_label}_L{length}_n{qnum_n}_l{qnum_l}_m{qnum_m}/dt{delta_t}_T{total_time}/energy_trace.csv"
    if os.path.exists(analytic_filename):
        logger.info(f"analytic file found: {analytic_filename}")
        analytic_df = pd.read_csv(analytic_filename)
        file_suffix.append(" analytic_discretized")
        key = "analytic_discretized"
        # "t"カラムはみな同じ
        hk_df["t"] = analytic_df["t"]
        hp_df["t"] = analytic_df["t"]
        htot_df["t"] = analytic_df["t"]
        autocorr_df["t"] = analytic_df["t"]
        hk_df[key] = analytic_df["Hk"]
        hp_df[key] = analytic_df["Hp_3"]
        htot_df[key] = analytic_df["Hk+Hp_3"]
        autocorr_df[key + ".re"] = analytic_df["autocorr.re"]
        autocorr_df[key + ".im"] = analytic_df["autocorr.im"]
        # true energy value
        En = -1 / (2 * qnum_n**2)
        htot_df["analytic"] = En
        autocorr = np.exp(- 1j* En * analytic_df["t"])
        autocorr_df["analytic.re"] = np.real(autocorr)
        autocorr_df["analytic.im"] = np.imag(autocorr)
        for k, kk in [ ("Ek","Hk"), ("Ep", "Hp_3"), ("Etot", "Hk+Hp_3")]:
            analytic_df[f"{k} analytic_discretized"] = analytic_df[kk]
    else:
        raise ValueError(f"analytic file not found: {analytic_filename}")

    pole="r0lim_0.333"
    classic_filename = f"{basedir}/classic3D/n{qnum_n}_l{qnum_l}_m{qnum_m}_TO{trotter_order}_{pole}/{bits}b_L{length}_T{total_time}_iT{interval_time}_dt{delta_t}/energy_trace.csv"
    if os.path.exists(classic_filename):
        logger.info(f"classic file found: {classic_filename}")
        classic_df = pd.read_csv(classic_filename)
        file_suffix.append(" classic")
        key = "classic"
        sdf = classic_df
        hk_df[key] = sdf["Hk"]
        hp_df[key] = sdf["Hp"]
        htot_df[key] = sdf["Hk+Hp"]
        autocorr_df[key + ".re"] = sdf["autocorr.re"]
        autocorr_df[key + ".im"] = sdf["autocorr.im"]
    else:
        raise ValueError(f"classic file not found: {classic_filename}")

    num_elec = int(interval_time / delta_t + 0.5)
    num_nucl = int(total_time / interval_time + 0.5)
    stqr_filename = f"{basedir}/circuits3D/GPU_cuStateVec_{precision}/n{qnum_n}_l{qnum_l}_m{qnum_m}_TO{trotter_order}_{pole}/{bits}b_L{length}_T{total_time}_iT{interval_time}_dt{delta_t}/energy_trace.csv"
    if os.path.exists(stqr_filename):
        logger.info(f"stqr file found: {stqr_filename}")
        stqr_df = pd.read_csv(stqr_filename)
        file_suffix.append(" look-up")
        key = "look-up"
        sdf = stqr_df
        hk_df[key] = sdf["Hk"]
        hp_df[key] = sdf["Hp"]
        htot_df[key] = sdf["Hk+Hp"]
        autocorr_df[key + ".re"] = sdf["autocorr.re"]
        autocorr_df[key + ".im"] = sdf["autocorr.im"]
    else:
        logger.warning(f"stqr file not found: {stqr_filename}")
        stqr_df = None

    # merge the dataframes

    analytic_df["Ek classic"] = classic_df["Hk"]
    analytic_df["Ep classic"] = classic_df["Hp"]
    analytic_df["Etot classic"] = classic_df["Hk+Hp"]

    if stqr_df is not None:
        autocorr_df["look-up.re"] = stqr_df["autocorr.re"]
        autocorr_df["look-up.im"] = stqr_df["autocorr.im"]
        analytic_df["Ek look-up"] = stqr_df["Hk"]
        analytic_df["Ep look-up"] = stqr_df["Hp"]
        analytic_df["Etot look-up"] = stqr_df["Hk+Hp"]

    compare_csv_dirname = f"{basedir}/compare3D/{bits}b{slabel}_L{length}_TO{trotter_order}/n{qnum_n}_l{qnum_l}_m{qnum_m}/dt{delta_t}/{num_nucl}n.{num_elec}e"
    os.makedirs(compare_csv_dirname, exist_ok=True)
    compare_csv_filename = f"{compare_csv_dirname}/compare_energy_trace.csv"
    analytic_df.to_csv(compare_csv_filename, index=False)
    autocorr_filename = f"{compare_csv_dirname}/autocorr_trace.csv"
    autocorr_df.to_csv(autocorr_filename, index=False)

    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle(
        f"Energy comparison of H atom 2D model n={qnum_n},m={qnum_m}\n{bits} bits, L={length} a.u., dt={delta_t}"
    )

    colors = {
        "analytic": "blue",
        "analytic_discretized": "green",
        "classic": "orange",
        "look-up": "magenta"
    }

    dashed = {
        "Ek analytic_discretized": (5, 5),
        "Ek classic": (5, 5),
        "Ek look-up": (0, 5, 5, 0),
        "Ep analytic_discretized": (2, 2),
        "Ep classic": (2, 2),
        "Ep look-up": (0, 2, 2, 0),
        "Etot analytic_discretized": (None, None),
        "Etot classic": (None, None),
        "Etot look-up": (None, None)
    }

    markers = {
        "analytic_discretized": ".",
        "look-up": "+",
        "classic": "o",
        "analytic": "."
    }


    ax = axs[0,1]
    ax.set_ylim(ek-ew, ek+ew)
    y = "analytic_discretized"
    hk_df.plot(
        ax=ax,
        x="t",
        y=y,
        marker=markers[y],
        color=colors[y],
        title="(C) Kinetic Energy Ek",
        grid=True,
    )
    y="classic"
    hk_df.plot(ax=ax, x="t", y=y, marker=markers[y], color=colors[y], grid=True)
    if stqr_df is not None:
        y="look-up"
        hk_df.plot(ax=ax, x="t", y=y, marker=markers[y], color=colors[y], grid=True)

    ax = axs[1,1]
    ax.set_ylim(ep-ew, ep+ew)
    y = "analytic_discretized"
    hp_df.plot(
        ax=ax,
        x="t",
        y=y,
        marker=markers[y],
        color=colors[y],
        title="(D) Potential Energy Ep",
        grid=True,
    )
    y="classic"
    hp_df.plot(ax=ax, x="t", y=y, marker=markers[y], color=colors[y], grid=True)
    if stqr_df is not None:
        y="look-up"
        hp_df.plot(ax=ax, x="t", y=y, marker=markers[y], color=colors[y], grid=True)

    ax = axs[0,0]
    ax.set_ylim(etot-ew, etot+ew)
    y = "analytic"
    htot_df.plot(
        ax=ax,
        x="t",
        y=y,
        marker=markers[y],
        color=colors[y],
        title="(A) Total Energy Etot",
        grid=True,
    )
    y = "analytic_discretized"
    htot_df.plot(
        ax=ax,
        x="t",
        y=y,
        marker=markers[y],
        color=colors[y],
        title="(A) Total Energy Etot",
        grid=True,
    )
    y = "classic"
    htot_df.plot(ax=ax, x="t", y=y, marker=markers[y], color=colors[y], grid=True)
    if stqr_df is not None:
        y = "look-up"
        htot_df.plot(ax=ax, x="t", y=y, marker=markers[y], color=colors[y], grid=True)

    ax = axs[0, 0]
    for k in ["Ek", "Etot", "Ep"]:
        for s in file_suffix:
            y = f"{k}{s}"
            sk = s[1:]
            # print(f"y = {y} s={s}")
            # analytic_df.plot(
            #     x="t",
            #     y=y,
            #     ax=ax,
            #     dashes=dashed[y],
            #     title="(A) Combined plots",
            #     color=colors[sk],
            #     # marker=markers[sk],
            #     grid=True,
            # )
    
    ax = axs[1, 0]
    ax.set_ylim(-1,1)
    for s in [" analytic"] + file_suffix:
        sk = s[1:]
        # print(f"sk = [{sk}]")
        # xd = autocorr_df["t"]
        # yd = autocorr_df[sk]
        # for y in yd:
        #     print(f"y = {y.real} + i * {y.imag}")
        # ax.plot(xd, yd, label=sk)
        autocorr_df.plot(
            x="t",
            y=sk + ".re",
            ax=ax,
            dashes=dashed[y],
            title="(B) Autocorrelation",
            color=colors[sk],
            marker=markers[sk],
            grid=True,
        )
    ax.legend()
    ax.set_xlabel("Time (a.u.)")
    ax.set_ylabel("<ψ(0)|ψ(t)>")
    fig.tight_layout()
    fig.savefig(f"{compare_csv_dirname}/compare_energy_trace.png")
    plt.close(fig)
    logger.info(f"Compare energy trace saved to {compare_csv_filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="comp_energy_h1", description="Compare energy of H atom 1D model"
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
        "--double", help="Use double precision (default)", action="store_true"
    )
    parser.add_argument("--single", help="Use single precision", action="store_true")
    parser.add_argument(
        "--qn",
        type=int,
        default=1,
        help="Quntum number for the wave function (default=1)",
    )
    parser.add_argument(
        "--ql",
        type=int,
        default=0,
        help="Azithumal Quntum number for the wave function (default=0)",
    )
    parser.add_argument(
        "--qm",
        type=int,
        default=0,
        help="Magnetic Quntum number for the wave function (default=0)",
    )
    parser.add_argument(
        "--etot",
        type=float,
        help="Total energy of the system",
    )
    parser.add_argument(
        "--ek",
        type=float,
        help="Kinetic energy of the system",
    )
    parser.add_argument(
        "--ep",
        type=float,
        help="Potential energy of the system",
    )
    parser.add_argument(
        "--trotter-order",
        type=int,
        default=1,
        help="Trotter order (default=1)",
    )
    parser.add_argument(
        "--ew",
        type=float,
        help="y-axis width"
    )
    parser.add_argument(
        "--length",
        type=float,
        default=16.0,
        help="Length of the 1D grid (default=16.0)",
    )
    parser.add_argument(
        "--delta-t", type=float, default=0.001, help="Time step (default=0.001)"
    )
    parser.add_argument("--interval-time", type=float, default=0.1)
    parser.add_argument("--total-time", type=float, default=30.0)

    parser.add_argument

    args = parser.parse_args()

    if args.double or not args.single:
        precision = "double"
    else:
        precision = "single"

    if args.signed or not args.unsigned:
        slabel = "signed"
        signed_flag = True
    else:
        slabel = "unsigned"
        signed_flag = False

    compare_energy(
        bits=args.bits,
        signed_label=slabel,
        precision=precision,
        qnum_n=args.qn,
        qnum_l=args.ql,
        qnum_m=args.qm,
        trotter_order=args.trotter_order,
        etot=args.etot,
        ek=args.ek,
        ep=args.ep,
        ew=args.ew,
        length=args.length,
        delta_t=args.delta_t,
        interval_time=args.interval_time,
        total_time=args.total_time,
    )
