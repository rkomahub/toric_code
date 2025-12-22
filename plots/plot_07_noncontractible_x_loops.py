# plots/plot_07_noncontractible_x_loops.py

import matplotlib.pyplot as plt

from toric.circuits import make_device, make_excitation_qnode
from toric.groups import build_xgroup_sites, build_zgroup_sites
from .common import excitation_plot

width, height = 6, 4
dev = make_device(width, height)

xgroup_sites = build_xgroup_sites(width, height)
zgroup_sites = build_zgroup_sites(width, height)

# --- Fig 7: two NON-CONTRACTIBLE X-loops on the torus ---
# Match the tutorial’s choice (a loop around x at fixed y, and around y at fixed x).
horizontal_loop = [(x, 1) for x in range(width)]   # wraps horizontally
vertical_loop   = [(1, y) for y in range(height)]  # wraps vertically

x_sites = horizontal_loop + vertical_loop

qnode = make_excitation_qnode(dev, width, height, x_sites=x_sites, z_sites=[])
expvals = qnode()

n_x = len(xgroup_sites)
x_expvals = expvals[:n_x]
z_expvals = expvals[n_x:]

fmt = lambda arr: [f"{v:+.3f}" for v in arr]
print("Horizontal X-loop:", horizontal_loop)
print("Vertical X-loop:", vertical_loop)
print("X-group expvals:", fmt(x_expvals))
print("Z-group expvals:", fmt(z_expvals))

# --- plot stabilizers + overlay the two loops ---
fig, ax = excitation_plot(
    x_expvals, z_expvals,
    xgroup_sites, zgroup_sites,
    width, height,
)

# overlay loops (same visual language: red path + dots)
hx, hy = zip(*(horizontal_loop + [horizontal_loop[0]]))
vx, vy = zip(*(vertical_loop + [vertical_loop[0]]))

ax.plot(hx, hy, color="firebrick", linewidth=6, zorder=5)
ax.scatter(hx, hy, color="firebrick", s=80, zorder=6)

ax.plot(vx, vy, color="firebrick", linewidth=6, zorder=5)
ax.scatter(vx, vy, color="firebrick", s=80, zorder=6)

plt.title("Fig 7: Crossed non-contractible X-loops on the torus")
plt.savefig("fig7.png", dpi=200, bbox_inches="tight")
plt.show()