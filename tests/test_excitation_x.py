from toric.circuits import make_device, make_excitation_qnode
from toric.diagnostics import print_info
from toric.plots import excitation_plot
from toric.groups import build_xgroup_sites, build_zgroup_sites
import matplotlib.pyplot as plt

width, height = 6, 4
E0 = -24  # for width=6, height=4
dev = make_device(width, height)

# apply one X at site (1,2)
circuit = make_excitation_qnode(dev, width, height, x_sites=[(1, 2)])
vals = circuit()

n_x = (width // 2) * height
x_vals = vals[:n_x]
z_vals = vals[n_x:]

print("X-groups:", [round(v, 6) for v in x_vals])
print("Z-groups:", [round(v, 6) for v in z_vals])
print_info(x_vals, z_vals, E0)

xgroup_sites = build_xgroup_sites(width, height)
zgroup_sites = build_zgroup_sites(width, height)

fig, ax = excitation_plot(
    x_vals,
    z_vals,
    xgroup_sites,
    zgroup_sites,
    width,
    height
)

# Mark where we applied the Pauli operator
ax.scatter(1, 2, color="maroon", s=100)

plt.show()