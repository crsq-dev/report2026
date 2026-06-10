from typing import List
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging

logger = logging.getLogger("crsq_xp.scripts")
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

def make_chart(pole:str, title: str, n: int, m: int, files: List, eps_list):
    basedir = "onedrive.lnk"
    outdir = f"{basedir}/compare2D"
    trotter_order = 2
    fig, ax = plt.subplots(figsize=(6, 8))
    hk_lines = []
    hp_lines = []
    htot_lines = []
    ent_mean_dfs = []
    for ent in files:
        bits, length, delta_t, interval_time, total_time = ent
        mean_dfs = []
        sigma_dfs = []
        for eps in eps_list:
            filename = f"{basedir}/classic2D/n{n}_m{m}_TO{trotter_order}_{pole}_{eps:.3f}/{bits}b_L{length}_T{total_time:.1f}_iT{interval_time}_dt{delta_t}/energy_trace.csv"
            logger.info(f"Reading file: {filename}")
            raw_df = pd.read_csv(filename)
            mean_df = raw_df.mean().to_frame().T
            sigma_df = raw_df.std().to_frame().T
            a = 1.0 / eps
            mean_df["a"] = a
            sigma_df["a"] = a
            mean_dfs.append(mean_df)
            sigma_dfs.append(sigma_df)
        tot_mean_df = pd.concat(mean_dfs)
        tot_sigma_df = pd.concat(sigma_dfs)
        ent_mean_dfs.append(tot_mean_df)
        # print("tot_sigma_df\n", tot_sigma_df)
        ebc = ax.errorbar(
            tot_mean_df["a"],
            tot_mean_df["Hk+Hp"],
            tot_sigma_df["Hk+Hp"],
            label=f"{bits}b",
            fmt="o-"
        )
        htot_lines.append(ebc)
        ebc = ax.errorbar(
            tot_mean_df["a"],
            tot_mean_df["Hk"],
            tot_sigma_df["Hk"],
            label=f"{bits}b",
            fmt="*-"
        )
        hk_lines.append(ebc)
        ebc = ax.errorbar(
            tot_mean_df["a"],
            tot_mean_df["Hp"],
            tot_sigma_df["Hp"],
            label=f"{bits}b",
            fmt="*-"
        )
        hp_lines.append(ebc)
    hk_legend = ax.legend(handles=hk_lines, loc="upper left", title="Hk")
    hp_legend = ax.legend(handles=hp_lines, loc="lower left", title="Hp")
    htot_legend = ax.legend(handles=htot_lines, loc="upper center", title="Hk+Hp")
    # Combine legends
    ax.add_artist(hk_legend)
    ax.add_artist(hp_legend)
    ax.add_artist(htot_legend)

    an_x = 2.5
    an_hk_y = ent_mean_dfs[0]["Hk"].iloc[1]
    an_hp_y = ent_mean_dfs[0]["Hp"].iloc[1]
    an_htot_y = ent_mean_dfs[0]["Hk+Hp"].iloc[6]

    ax.text(an_x, an_hk_y, "Hk", bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10})
    ax.text(an_x, an_hp_y, "Hp", bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10})
    ax.text(an_x, an_htot_y, "Hk+Hp", bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10})

    ax.grid(True)
    ax.set_title(f"Hk+Hp vs a for Ψ2D_{n},{m}, V(r)={title}")
    ax.set_xlabel("a")
    # ax.set_xscale("log")
    ax.set_ylabel("energy")
    figfile = f"{outdir}/compare_energy_h2D_TO{trotter_order}_{pole}_{n}_{m}.png"
    logger.info(f"Saving figure to {figfile}")
    fig.savefig(figfile, dpi=300, bbox_inches="tight")


eps = [ 0.125, 0.176, 0.250, 0.353, 0.500, 0.707, 1.000]

files0_0 = [
    #nb, L, T, dt
    [6, 5.0, 0.001, 0.2, 4.0],
    [7, 5.0, 0.0001, 0.2, 4.0],
    [8, 6.0, 0.0001, 0.2, 4.0],
    [9, 7.0, 5e-05, 0.2, 4.0]
]

files1_0 = [
    #nb, L, T, dt
    [6, 18.0, 0.01, 0.5, 30.0],
    [7, 21.0, 0.005, 0.5, 30.0],
    [8, 24.0, 0.001, 0.5, 30.0],
    [9, 27.0, 0.0005, 0.5, 30.0]
]

if __name__ == "__main__":
    # Compare energies for the two sets of files

    make_chart("rofs", "-1/\u221a(r**2 + (δr/a)**2)", 0, 0, files0_0, eps)
    make_chart("rofs", "-1/\u221a(r**2 + (δr/a)**2)", 1, 0, files1_0, eps)
    make_chart("r0lim","-1/r;-1/(δr/a)",  0, 0, files0_0, eps)
    make_chart("r0lim","-1/r;-1/(δr/a)",  1, 0, files1_0, eps)