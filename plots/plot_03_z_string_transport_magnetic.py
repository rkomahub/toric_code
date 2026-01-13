# Fig 3: Z-string transporting a magnetic anyon pair

import matplotlib.pyplot as plt

from toric.circuits import make_device, make_excitation_qnode
from toric.groups import build_xgroup_sites, build_zgroup_sites
from .common import excitation_plot

width, height = 6, 4
dev = make_device(width, height)

# ---- Straight Z string ----
z_string = [(1, 2), (2, 2), (3, 2), (4, 2)]
# ---------------------------

qnode = make_excitation_qnode(
    dev,
    width,
    height,
    x_sites=[],
    z_sites=z_string,
)

expvals = qnode()

n_x = len(build_xgroup_sites(width, height))
x_expvals = expvals[:n_x]
z_expvals = expvals[n_x:]

# Pretty printing
fmt = lambda arr: [f"{v:+.3f}" for v in arr]
print("Z string (straight):", z_string)
print("X-group expvals:", fmt(x_expvals))
print("Z-group expvals:", fmt(z_expvals))

# Plot stabilizer excitations
fig, ax = excitation_plot(
    x_expvals,
    z_expvals,
    build_xgroup_sites(width, height),
    build_zgroup_sites(width, height),
    width,
    height,
)

# Draw Z-string path (Z ops = blue)
xs, ys = zip(*z_string)
ax.plot(xs, ys, color="steelblue", linewidth=6, zorder=4)
ax.scatter(xs, ys, color="steelblue", s=80, zorder=5)

plt.title("Fig 3: Z-string transporting a magnetic anyon pair")
plt.show()