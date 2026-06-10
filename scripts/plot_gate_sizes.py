import pandas as pd
import matplotlib.pyplot as plt

plot_frac_bits = False

dirname="onedrive.lnk/count_gates"
def csvfilename(label, dmin, dmax, nmin, nmax):
    filename=f"{dirname}/hamiltonian-gatecount-{label}-d{dmin}-{dmax}-n{nmin}-{nmax}.csv"
    return filename

def read_data(values, label, dmin, dmax, nmin, nmax):
    path = csvfilename(label,dmin,dmax,nmin,nmax)
    print(f"Reading data from {path}")
    df = pd.read_csv(path)
    if not label in values:
        values[label] = [{},{},{}]
    for row in df.itertuples():
        series_set = values[label][row.dim-1]
        for k in ['width', 'cX', 't+tdg']:
            if k not in series_set:
                series_set[k] = []
        values[label][row.dim-1]['width'].append(row.width)
        cX = 0
        if hasattr(row, 'cx'):
            cX += row.cx
        if hasattr(row, 'cp'):
            cX += row.cp
        if hasattr(row, 'cu'):
            cX += row.cu
        if hasattr(row, 'cry'):
            cX += row.cry
        values[label][row.dim-1]['cX'].append(cX)
        td = 0
        if hasattr(row, 't'):
            td += row.t
        if hasattr(row, 'tdg'):
            td += row.tdg
        values[label][row.dim-1]['t+tdg'].append(td)

values={}
read_data(values, "embed", 1,3,5,7)
read_data(values, "embed", 1,2,8,10)
read_data(values, "embed", 3,3,8,8)
read_data(values, "arith-elec-potential", 1,3,5,8)
read_data(values, "arith-elec-potential", 1,2,9,10)
#read_data(values, "arith-elec-potential", 3,3,8,10)
if plot_frac_bits:
    read_data(values, "arith-elec-potential-fracbits", 2,3,5,7)
    read_data(values, "arith-elec-potential-fracbits", 2,2,8,10)
read_data(values, "ucrz", 1,3,5,7)
read_data(values, "ucrz", 1,2,8,10)
read_data(values, "ucrz", 3,3,8,9)

print(values)

LN = 27
plot_limit_line = True

if plot_frac_bits:
    keys1 = ["arith-elec-potential", "arith-elec-potential-fracbits", "ucrz", "embed"]
else:
    keys1 = ["arith-elec-potential", "ucrz", "embed"]

labels1= {
    "arith-elec-potential": "Hep:arithmetic",
    "arith-elec-potential-fracbits": "Hep:arithmetic (frac)",
    "ucrz": "Hep:UCRZ",
    "embed": "state preparation"
}

titles1 = [
    ["1D", "2D", "3D"],
    ["", "", ""]
]

titles2 = [
    ["(a) qubits(1D)", "(b) qubits(2D)", "(c) qubits(3D)"],
    ["(d) 2 qubit gates(1D)", "(e) 2 qubit gates(2D)", "(f) 2 qubit gates(3D)"]
]

revision = 2

def draw_charts(revision):

    if revision == 1:
        titles = titles1
        filename = "hamiltonian-gatecount.png"
    elif revision == 2:
        titles = titles2
        filename = "hamiltonian-gatecount-revision2.png"

    fig, axs = plt.subplots(2,3, figsize=(10,6), layout="constrained")
    for dim in [1,2,3]:
        ax:plt.Axes = axs[0][dim-1]
        ax.grid()
        ax.set_title(titles[0][dim-1])
        ax.set_xlim(4.5, 10.5)
        ax.set_ylim(0, 150)
        lengthlist=[]
        for label in keys1:
            if label not in values:
                print(f"Label {label} not found in values")
                continue
            if 'width' not in values[label][dim-1]:
                print(f"'width' not found in values for label {label} and dimension {dim}")
                continue
            series = values[label][dim-1]['width']
            bitcount = range(5, 5+len(series))
            lengthlist.append(5+len(series)-1)
            ax.plot(bitcount, series, label=labels1[label], marker="o")
        if plot_limit_line:
            limy = [LN]*2
            limx = [5, 10]
            ax.plot(limx, limy, label=f"limit({LN})", color='red')
    axs[0][0].legend()
    axs[0][0].set_ylabel("qubits")

    if plot_frac_bits:
        keys2 = ["arith-elec-potential", "arith-elec-potential-fracbits", "ucrz"]
    else:
        keys2 = ["arith-elec-potential", "ucrz"]
    labels2= {
        # "embed": "state preparation",
        "arith-elec-potential": "Hep:arithmetic x 1e+3",
        "arith-elec-potential-fracbits": "Hep:arithmetic (frac) x 1e+3",
        "ucrz": "Hep:UCRZ x 1e+3"
    }

    GN=1.0e+7
    for dim in [1,2,3]:
        ax:plt.Axes = axs[1][dim-1]
        ax.grid()
        ax.set_title(titles[1][dim-1])
        ax.set_xlabel("bits/dim")
        ax.set_yscale("log")
        ax.set_xlim(4.5, 10.5)
        ax.set_ylim(1e+3, 1e+10)
        for label in keys2:
            if not 'cX' in values[label][dim-1]:
                print(f"'cX' not found in values for label {label} and dimension {dim}")
                continue
            series = values[label][dim-1]['cX']
            seriesx = [x * 1e+3 for x in series]  # scale by 1e+3
            bitcount = range(5, 5+len(series))
            lengthlist.append(5+len(series))
            print(series)
            ax.plot(bitcount, seriesx, label=labels2[label], marker="o")
        if plot_limit_line:
            limy = [GN]*2
            limx = [5, 10]
            ax.plot(limx, limy, label=f"limit(1e+7)", color='red')
        axs[1][0].set_ylabel("2 qubit gates")
    axs[1][0].legend()
    figfile = f"{dirname}/{filename}"
    fig.savefig(figfile)
    print(f"Figure saved to {figfile}")

# revisions = [1, 2]
revisions = [2]

for revision in revisions:
    draw_charts(revision)


# for dim in [1,2,3]:
#     ax:plt.Axes = axs[2][dim-1]
#     ax.grid()
#     ax.set_xlabel("bits/dim")
#     ax.set_yscale("log")
#     ax.set_xlim(4.5, 10.5)
#     ax.set_ylim(1, 10**9)
#     for label in values.keys():
#         series = values[label][dim-1]['t+tdg']
#         bitcount = range(5, 5+len(series))
#         lengthlist.append(5+len(series))
#         print(series)
#         ax.plot(bitcount, series, label=label, marker="o")
#     axs[2][0].set_ylabel("t gates")

