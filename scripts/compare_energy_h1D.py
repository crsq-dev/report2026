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
    trotter_order: int,
    precision: str,
    qnum_n: int,
    length: float,
    window: float,
    delta_t: float,
    num_elec: int,
    num_nucl: int,
):
    basedir = "onedrive.lnk"

    file_suffix = []

    hk_df = pd.DataFrame()
    hp_df = pd.DataFrame()
    htot_df = pd.DataFrame()

    analytic_filename = f"{basedir}/analytic1D/1D_{bits}b_{signed_label}/N{qnum_n}_L{length}_X0.0_WM{window}/dt{delta_t}/{num_nucl}n.{num_elec}e/energy_trace.csv"
    if os.path.exists(analytic_filename):
        logger.info(f"analytic file found: {analytic_filename}")
        analytic_df = pd.read_csv(analytic_filename)
        file_suffix.append(" analytic_discretized")
        key = "analytic_discretized"
        hk_df["t"] = analytic_df["t"]
        hp_df["t"] = analytic_df["t"]
        htot_df["t"] = analytic_df["t"]
        hk_df[key] = analytic_df["Hk"]
        hp_df[key] = analytic_df["Hp"]
        htot_df[key] = analytic_df["Htot"]
        htot_df["analytic"] = -1 / (2 * qnum_n**2)
        for k in ["k", "p", "tot"]:
            analytic_df[f"E{k} analytic_discretized"] = analytic_df[f"H{k}"]
    else:
        raise ValueError(f"analytic file not found: {analytic_filename}")

    classic_filename = f"{basedir}/classic1D/1D_{bits}b_{signed_label}_TO{trotter_order}/N{qnum_n}odd_L{length}_X0.0_WM{window}/dt{delta_t}/{num_nucl}n.{num_elec}e/energy_trace.csv"
    if os.path.exists(classic_filename):
        logger.info(f"classic file found: {classic_filename}")
        classic_df = pd.read_csv(classic_filename)
        file_suffix.append(" classic")
        key = "classic"
        sdf = classic_df
        hk_df[key] = sdf["Hk"]
        hp_df[key] = sdf["Hp"]
        htot_df[key] = sdf["Htot"]
    else:
        raise ValueError(f"classic file not found: {classic_filename}")

    classic_fixed_filename = f"{basedir}/classic1D/1D_{bits}b_{signed_label}_fixed_TO{trotter_order}/N{qnum_n}odd_L{length}_X0.0_WM{window}/dt{delta_t}/{num_nucl}n.{num_elec}e/energy_trace.csv"
    if os.path.exists(classic_fixed_filename):
        logger.info(f"classic fixed point file found: {classic_fixed_filename}")
        classic_fixed_df = pd.read_csv(classic_fixed_filename)
        file_suffix.append(" classic_fixed")
        key = "classic_fixed"
        sdf = classic_fixed_df
        hk_df[key] = sdf["Hk"]
        hp_df[key] = sdf["Hp"]
        htot_df[key] = sdf["Htot"]
    else:
        logger.warning(f"classic fixed file not found: {classic_filename}")
        classic_fixed_df = None

    stqr_filename = f"{basedir}/circuits1D/GPU_cuStateVec_{precision}_{bits}b{slabel}/N{qnum_n}odd_L{length}_X0.0/dt{delta_t:.3f}/{num_nucl}n.{num_elec}e/STQR/energy_trace.csv"
    if os.path.exists(stqr_filename):
        logger.info(f"stqr file found: {stqr_filename}")
        stqr_df = pd.read_csv(stqr_filename)
        file_suffix.append(" look-up")
        key = "look-up"
        sdf = stqr_df
        hk_df[key] = sdf["Hk"]
        hp_df[key] = sdf["Hp"]
        htot_df[key] = sdf["Htot"]
    else:
        logger.warning(f"stqr file not found: {stqr_filename}")
        stqr_df = None

    star_filename = f"{basedir}/circuits1D/GPU_cuStateVec_{precision}_{bits}b{slabel}/N{qnum_n}odd_L{length}_X0.0/dt{delta_t:.3f}/{num_nucl}n.{num_elec}e/STAR/energy_trace.csv"
    if os.path.exists(star_filename):
        logger.info(f"star file found: {star_filename}")
        star_df = pd.read_csv(star_filename)
        file_suffix.append(" arithmetic")
        key = "arithmetic"
        sdf = star_df
        hk_df[key] = sdf["Hk"]
        hp_df[key] = sdf["Hp"]
        htot_df[key] = sdf["Htot"]
    else:
        logger.warning(f"star file not found: {star_filename}")
        star_df = None
    # merge the dataframes

    analytic_df["Ek classic"] = classic_df["Hk"]
    analytic_df["Ep classic"] = classic_df["Hp"]
    analytic_df["Etot classic"] = classic_df["Htot"]

    if classic_fixed_df is not None:
        analytic_df["Ek classic_fixed"] = classic_fixed_df["Hk"]
        analytic_df["Ep classic_fixed"] = classic_fixed_df["Hp"]
        analytic_df["Etot classic_fixed"] = classic_fixed_df["Htot"]

    if stqr_df is not None:
        analytic_df["Ek look-up"] = stqr_df["Hk"]
        analytic_df["Ep look-up"] = stqr_df["Hp"]
        analytic_df["Etot look-up"] = stqr_df["Htot"]

    if star_df is not None:
        analytic_df["Ek arithmetic"] = star_df["Hk"]
        analytic_df["Ep arithmetic"] = star_df["Hp"]
        analytic_df["Etot arithmetic"] = star_df["Htot"]

    compare_csv_dirname = f"{basedir}/compare1D/1D_{bits}b_{signed_label}/N{qnum_n}odd_L{length}_X0.0_WM{window}/dt{delta_t}/{num_nucl}n.{num_elec}e"
    os.makedirs(compare_csv_dirname, exist_ok=True)
    compare_csv_filename = f"{compare_csv_dirname}/compare_energy_trace.csv"
    analytic_df.to_csv(compare_csv_filename, index=False)

    fig, ax = plt.subplots(2, 2, figsize=(12, 8), layout="constrained")
    fig.suptitle(
        f"Energy comparison of H atom 1D model\nn=1, nb={bits}, L={length}, dt={delta_t}"
    )

    colors = {
        "analytic": "blue",
        "analytic_discretized": "green",
        "classic": "orange",
        "classic_fixed": "brown",
        "look-up": "magenta",
        "arithmetic": "red",
    }

    markers = {
        "analytic_discretized": ".",
        "look-up": "+",
        "classic": "o",
        "classic_fixed": "*",
        "analytic": ".",
        "arithmetic": "x",
    }

    # Combined energy plots
    dashed = {"Ek": (5, 5), "Ep": (2, 2), "Etot": (None, None)}
    for k in ["Ek", "Etot", "Ep"]:
        for s in file_suffix:
            y = f"{k}{s}"
            sk = s[1:]
            analytic_df.plot(
                x="t",
                y=y,
                ax=ax[0, 0],
                dashes=dashed[k],
                title="(A) Energy conservation",
                color=colors[sk],
                grid=True,
            )

    y = "analytic"
    htot_df.plot(
        ax=ax[0, 1],
        x="t",
        y=y,
        marker=markers[y],
        color=colors[y],
        title="(B) Total Energy Etot",
        grid=True,
    )
    y = "analytic_discretized"
    htot_df.plot(ax=ax[0, 1], x="t", y=y, marker=markers[y], color=colors[y], grid=True)
    y = "classic"
    htot_df.plot(ax=ax[0, 1], x="t", y=y, marker=markers[y], color=colors[y], grid=True)
    if classic_fixed_df is not None:
        y = "classic_fixed"
        htot_df.plot(
            ax=ax[0, 1], x="t", y=y, marker=markers[y], color=colors[y], grid=True
        )
    if stqr_df is not None:
        y = "look-up"
        htot_df.plot(
            ax=ax[0, 1], x="t", y=y, marker=markers[y], color=colors[y], grid=True
        )
    if star_df is not None:
        y = "arithmetic"
        htot_df.plot(
            ax=ax[0, 1], x="t", y=y, marker=markers[y], color=colors[y], grid=True
        )

    y = "analytic_discretized"
    hk_df.plot(
        ax=ax[1, 0],
        x="t",
        y=y,
        marker=markers[y],
        color=colors[y],
        title="(C) Kinetic Energy Ek",
        grid=True,
    )
    y = "classic"
    hk_df.plot(ax=ax[1, 0], x="t", y=y, marker=markers[y], color=colors[y], grid=True)
    if classic_fixed_df is not None:
        y = "classic_fixed"
        hk_df.plot(
            ax=ax[1, 0], x="t", y=y, marker=markers[y], color=colors[y], grid=True
        )
    if stqr_df is not None:
        y = "look-up"
        hk_df.plot(
            ax=ax[1, 0], x="t", y=y, marker=markers[y], color=colors[y], grid=True
        )
    if star_df is not None:
        y = "arithmetic"
        hk_df.plot(
            ax=ax[1, 0], x="t", y=y, marker=markers[y], color=colors[y], grid=True
        )

    y = "analytic_discretized"
    hp_df.plot(
        ax=ax[1, 1],
        x="t",
        y=y,
        marker=markers[y],
        color=colors[y],
        title="(D) Potential Energy Ep",
        grid=True,
    )
    y = "classic"
    hp_df.plot(ax=ax[1, 1], x="t", y=y, marker=markers[y], color=colors[y], grid=True)
    if classic_fixed_df is not None:
        y = "classic_fixed"
        hp_df.plot(
            ax=ax[1, 1], x="t", y=y, marker=markers[y], color=colors[y], grid=True
        )
    if stqr_df is not None:
        y = "look-up"
        hp_df.plot(
            ax=ax[1, 1], x="t", y=y, marker=markers[y], color=colors[y], grid=True
        )
    if star_df is not None:
        y = "arithmetic"
        hp_df.plot(
            ax=ax[1, 1], x="t", y=y, marker=markers[y], color=colors[y], grid=True
        )

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
    parser.add_argument(
        "--trotter-order",
        type=int,
        default=1,
        help="Trotter order for the simulation (default=1)",
    )
    parser.add_argument("--single", help="Use single precision", action="store_true")
    parser.add_argument(
        "--qn",
        type=int,
        default=1,
        help="Quntum number for the wave function (default=1)",
    )
    parser.add_argument(
        "--length",
        type=float,
        default=16.0,
        help="Length of the 1D grid (default=16.0)",
    )
    parser.add_argument("--x0", type=float, required=True, help="atom position")
    parser.add_argument(
        "--delta-t", type=float, default=0.001, help="Time step (default=0.001)"
    )
    parser.add_argument("--num-elec", type=int, default=1)
    parser.add_argument("--num-nucl", type=int, default=1)
    parser.add_argument(
        "--window-radius", type=int, help="P-space window radius (default=2^(bits-1))"
    )

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
        trotter_order=args.trotter_order,
        precision=precision,
        qnum_n=args.qn,
        length=args.length,
        window=args.window_radius,
        delta_t=args.delta_t,
        num_elec=args.num_elec,
        num_nucl=args.num_nucl,
    )
