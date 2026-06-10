from crsq.reports.h1d2report import H1D2ShowPsi
import matplotlib.pyplot as plt

basedir = "onedrive.lnk/analytic2D"

pxm = 1.2
kpm = 1.2
psi00 = H1D2ShowPsi(
    basedir + "/6b_signed_L5.0_n0_m0/dt0.001_T3.2/frames",
    6,
    0,
    pxm,
    -pxm,
    pxm,
    0,
    kpm,
    -kpm,
    kpm,
    5,
)
pxm = 0.4
kpm = 1.2
psi10 = H1D2ShowPsi(
    basedir + "/6b_signed_L18.0_n1_m0/dt0.01_T16.0/frames",
    6,
    0,
    pxm,
    -pxm,
    pxm,
    0,
    kpm,
    -kpm,
    kpm,
    18,
)

pxm = 0.2
kpm = 2.0
psi11 = H1D2ShowPsi(
    basedir + "/6b_signed_L26.0_n1_m1/dt0.05_T30.0/frames",
    6,
    0,
    pxm,
    -pxm,
    pxm,
    0,
    kpm,
    -kpm,
    kpm,
    26,
)

fig, axs = plt.subplots(
    1, 3, subplot_kw={"projection": "3d"}, figsize=(16, 5), layout="constrained"
)
psi00.plot(axs[0], 0, "(A) Re(Ψ2D_0_0)")
psi10.plot(axs[1], 0, "(B) Re(Ψ2D_1_0)")
psi11.plot(axs[2], 0, "(C) Re(Ψ2D_1_1)")

fig.savefig("onedrive.lnk/diagrams/psi0_h2d_opt.png")

### backup

basedir = "onedrive.lnk/analytic2D"

pxm = 1.2
kpm = 1.2
psi00 = H1D2ShowPsi(
    basedir + "/6b_signed_L5.0_n0_m0/dt0.001_T3.2/frames",
    6,
    0,
    pxm,
    -pxm,
    pxm,
    0,
    kpm,
    -kpm,
    kpm,
    12,
)
pxm = 0.4
kpm = 1.2
psi10 = H1D2ShowPsi(
    basedir + "/6b_signed_L32.0_n1_m0/dt0.01_T16.0/frames",
    6,
    0,
    pxm,
    -pxm,
    pxm,
    0,
    kpm,
    -kpm,
    kpm,
    32,
)

pxm = 0.2
kpm = 2.0
psi11 = H1D2ShowPsi(
    basedir + "/6b_signed_L32.0_n1_m1/dt0.01_T16.0/frames",
    6,
    0,
    pxm,
    -pxm,
    pxm,
    0,
    kpm,
    -kpm,
    kpm,
    32,
)

fig, axs = plt.subplots(
    1, 3, subplot_kw={"projection": "3d"}, figsize=(16, 5), layout="constrained"
)
psi00.plot(axs[0], 0, "(A) Re(Ψ2D_0_0)")
psi10.plot(axs[1], 0, "(B) Re(Ψ2D_1_0)")
psi11.plot(axs[2], 0, "(C) Re(Ψ2D_1_1)")

fig.savefig("onedrive.lnk/diagrams/psi0_h2d.png")
