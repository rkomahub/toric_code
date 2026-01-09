# Fig 3: X-string transporting a magnetic anyon pair

import matplotlib.pyplot as plt

from toric.circuits import make_device, make_excitation_qnode
from toric.groups import build_xgroup_sites, build_zgroup_sites
from .common import excitation_plot

width, height = 6, 4
dev = make_device(width, height)

# ---- X string path (operator) ----
x_string = [(1, 2), (2, 2), (3, 2), (4, 2)]
# ---------------------------------

qnode = make_excitation_qnode(
    dev,
    width,
    height,
    x_sites=x_string,
    z_sites=[],
)

expvals = qnode()

n_x = len(build_xgroup_sites(width, height))
x_expvals = expvals[:n_x]
z_expvals = expvals[n_x:]

# Pretty printing
fmt = lambda arr: [f"{v:+.3f}" for v in arr]
print("X string:", x_string)
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

# Draw X-string path (tutorial convention: X ops = red)
xs, ys = zip(*x_string)
ax.plot(xs, ys, color="firebrick", linewidth=6, zorder=4)
ax.scatter(xs, ys, color="firebrick", s=80, zorder=5)

plt.title("Fig 3: X-string transporting a magnetic anyon pair")
plt.show()