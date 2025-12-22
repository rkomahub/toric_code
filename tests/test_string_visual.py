import matplotlib.pyplot as plt

from toric.circuits import make_device, make_excitation_qnode
from toric.groups import build_xgroup_sites, build_zgroup_sites
from toric.plots import excitation_plot

width, height = 6, 4
dev = make_device(width, height)

# A Z-string (path) that moves the excitation
z_string = [(1, 2)]

# Build the circuit: ground state + Z-string
circuit = make_excitation_qnode(dev, width, height, z_sites=z_string)
vals = circuit()

# Split expvals into X-groups and Z-groups
n_x = (width // 2) * height
x_vals = vals[:n_x]
z_vals = vals[n_x:]

# Geometry of groups (for plotting)
xgroup_sites = build_xgroup_sites(width, height)
zgroup_sites = build_zgroup_sites(width, height)

# Plot colored stabilizers (dark = excitation)
fig, ax = excitation_plot(
    x_vals, z_vals,
    xgroup_sites, zgroup_sites,
    width, height
)

# Overlay the string path (thick line)
xs, ys = zip(*z_string)
ax.plot(xs, ys, color="blue", linewidth=4, linestyle="--")

# Mark endpoints explicitly
ax.scatter(xs[0], ys[0], color="black", s=150, zorder=3)
ax.scatter(xs[-1], ys[-1], color="black", s=150, zorder=3)

plt.savefig("string_excitation.png", dpi=200, bbox_inches="tight")
plt.close()