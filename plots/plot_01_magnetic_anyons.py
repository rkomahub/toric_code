# Graph 1: Magnetic anyon pair (single X flips two Z-groups)

import numpy as np
import matplotlib.pyplot as plt

from toric.circuits import make_device, make_excitation_qnode
from toric.groups import build_xgroup_sites, build_zgroup_sites
from .common import excitation_plot

width, height = 6, 4
dev = make_device(width, height)

# ---- choose a site to flip with X ----
single_x = [(1, 2)]   # you can change this later
# -------------------------------------

qnode = make_excitation_qnode(
    dev,
    width,
    height,
    x_sites=single_x,
    z_sites=[],
)

expvals = qnode()

n_x = len(build_xgroup_sites(width, height))
x_expvals = expvals[:n_x]
z_expvals = expvals[n_x:]
# Pretty printing (round to 3 decimals)
x_pretty = [round(v, 3) for v in x_expvals]
z_pretty = [round(v, 3) for v in z_expvals]

print("Applied X at:", single_x)
print("X-group expvals:", x_pretty)
print("Z-group expvals:", z_pretty)

# Plot
fig, ax = excitation_plot(
    x_expvals,
    z_expvals,
    build_xgroup_sites(width, height),
    build_zgroup_sites(width, height),
    width,
    height,
)

# Mark the physical location of the applied X
ax.scatter(*zip(*single_x), color="firebrick", s=120, zorder=5)

plt.title("Fig 1: Magnetic anyon pair from a single X")
plt.show()
