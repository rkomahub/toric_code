# Graph 2: Electric anyon pair (single Z flips two X-groups)

import numpy as np
import matplotlib.pyplot as plt

from toric.circuits import make_device, make_excitation_qnode
from toric.groups import build_xgroup_sites, build_zgroup_sites
from .common import excitation_plot

width, height = 6, 4
dev = make_device(width, height)

# ---- choose a site to flip with Z ----
single_z = [(1, 2)]   # feel free to move it later
# -------------------------------------

qnode = make_excitation_qnode(
    dev,
    width,
    height,
    x_sites=[],
    z_sites=single_z,
)

expvals = qnode()

n_x = len(build_xgroup_sites(width, height))
x_expvals = expvals[:n_x]
z_expvals = expvals[n_x:]

# Pretty printing (3 decimals)
fmt = lambda arr: [f"{v:+.3f}" for v in arr]
print("Applied Z at:", single_z)
print("X-group expvals:", fmt(x_expvals))
print("Z-group expvals:", fmt(z_expvals))

# Plot
fig, ax = excitation_plot(
    x_expvals,
    z_expvals,
    build_xgroup_sites(width, height),
    build_zgroup_sites(width, height),
    width,
    height,
)

# Mark the physical location of the applied Z
ax.scatter(*zip(*single_z), color="steelblue", s=120, zorder=5)

plt.title("Fig 2: Electric anyon pair from a single Z")
plt.show()