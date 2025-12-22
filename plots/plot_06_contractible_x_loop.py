# Fig 6: Contractible X-loop (using same design as previous figures)

import matplotlib.pyplot as plt

from toric.circuits import make_device, make_excitation_qnode
from toric.groups import build_xgroup_sites, build_zgroup_sites
from .common import excitation_plot

width, height = 6, 4
dev = make_device(width, height)

# --- Contractible X loop ---
x_loop = [
    (1, 1), (2, 1), (3, 1), (4, 1),
    (4, 2), (4, 3),
    (3, 3), (2, 3), (1, 3),
    (1, 2), (1, 1)
]

qnode = make_excitation_qnode(
    dev,
    width,
    height,
    x_sites=x_loop,
    z_sites=[],
)

expvals = qnode()

n_x = len(build_xgroup_sites(width, height))
x_expvals = expvals[:n_x]
z_expvals = expvals[n_x:]

# pretty printing
fmt = lambda arr: [f"{v:+.3f}" for v in arr]
print("X loop (contractible):", x_loop)
print("X-group expvals:", fmt(x_expvals))
print("Z-group expvals:", fmt(z_expvals))

# --- SAME plotting pipeline as Figs. 0–5 ---
fig, ax = excitation_plot(
    x_expvals,
    z_expvals,
    build_xgroup_sites(width, height),
    build_zgroup_sites(width, height),
    width,
    height,
)

# overlay the X-loop (X operator = red)
xs, ys = zip(*x_loop)
ax.plot(xs, ys, color="firebrick", linewidth=6, zorder=5)
ax.scatter(xs, ys, color="firebrick", s=80, zorder=6)

plt.title("Fig 6: Contractible X-loop (same visual language)")
plt.show()