# Fig. 8 — Braiding of electric (e) and magnetic (m) anyons
#
# An open Z-string is used to transport ONE magnetic anyon
# around a static electric anyon. The string endpoint traces
# a loop, while the bulk leaves stabilizers unchanged.

import matplotlib.pyplot as plt

from toric.circuits import make_device, make_excitation_qnode
from toric.groups import build_xgroup_sites, build_zgroup_sites
from .common import excitation_plot


# ------------------------------------------------------------
# Lattice and device
# ------------------------------------------------------------
width, height = 6, 4
dev = make_device(width, height)

xgroup_sites = build_xgroup_sites(width, height)
zgroup_sites = build_zgroup_sites(width, height)


# ------------------------------------------------------------
# 1) Create ONE electric anyon (e)
# ------------------------------------------------------------
# A single X creates an electric anyon pair; we focus on
# the one enclosed by the Z-string trajectory.
e_site = [(2, 2)]


# ------------------------------------------------------------
# 2) Create a magnetic anyon pair with a SHORT open Z-string
# ------------------------------------------------------------
# Endpoints of this string are the two m anyons.
z_string = [
    (1, 1), (2, 1)
]


# ------------------------------------------------------------
# 3) Transport ONE magnetic anyon around the electric anyon
# ------------------------------------------------------------
# Extend the Z-string step by step so that ONE endpoint
# encircles the electric anyon at (2,2).
z_string += [
    (2, 2), (2, 3),
    (1, 3), (1, 2),
    (1, 1)
]

# IMPORTANT:
# - This is a SINGLE OPEN STRING
# - One endpoint moves
# - The other endpoint stays fixed
# - The string is NOT a closed loop


# ------------------------------------------------------------
# Apply operators
# ------------------------------------------------------------
qnode = make_excitation_qnode(
    dev,
    width,
    height,
    x_sites=e_site,      # electric anyon
    z_sites=z_string,    # magnetic anyon transport
)

expvals = qnode()

n_x = len(xgroup_sites)
x_expvals = expvals[:n_x]
z_expvals = expvals[n_x:]


# ------------------------------------------------------------
# Plot stabilizers
# ------------------------------------------------------------
fig, ax = excitation_plot(
    x_expvals,
    z_expvals,
    xgroup_sites,
    zgroup_sites,
    width,
    height,
)


# ------------------------------------------------------------
# Visualize electric anyon (static)
# ------------------------------------------------------------
ex, ey = zip(*e_site)
ax.scatter(
    ex, ey,
    color="darkred",
    s=140,
    zorder=6,
    label="electric anyon (e)",
)


# ------------------------------------------------------------
# Visualize magnetic anyon transport (open Z-string)
# ------------------------------------------------------------
zx, zy = zip(*z_string)
ax.plot(
    zx, zy,
    color="firebrick",
    linewidth=6,
    zorder=5,
    label="Z-string (m transport)",
)
ax.scatter(
    zx, zy,
    color="firebrick",
    s=80,
    zorder=6,
)


# ------------------------------------------------------------
# Final touches
# ------------------------------------------------------------
plt.title("Fig. 8: Braiding of electric (e) and magnetic (m) anyons")
plt.legend(loc="lower left")
plt.savefig("fig10.png", dpi=200, bbox_inches="tight")
plt.show()