# Fig 6: Contractible X-loop (no excitations)

import matplotlib.pyplot as plt
from collections import Counter
import numpy as np

from toric.circuits import make_device, make_excitation_qnode
from toric.groups import build_xgroup_sites, build_zgroup_sites
from .common import excitation_plot

def order_loop(points):
    """
    Order boundary vertices cyclically for plotting.
    """
    pts = np.array(points)
    center = pts.mean(axis=0)
    angles = np.arctan2(pts[:,1] - center[1], pts[:,0] - center[0])
    order = np.argsort(angles)
    return [tuple(pts[i]) for i in order]

def extract_boundary(vertices):
    """
    Given a list of vertices acted on by a product of stabilizers,
    return the boundary vertices (appear exactly once).
    """
    counts = Counter(vertices)
    boundary = [v for v, c in counts.items() if c == 1]
    return boundary

width, height = 6, 4
dev = make_device(width, height)

xgroup_sites = build_xgroup_sites(width, height)
zgroup_sites = build_zgroup_sites(width, height)

# --- CENTRAL 2×2 BLOCK OF X-GROUPS (contractible region) ---
block_indices = [4, 5, 8, 9]  # central for 6x4

# Apply all X operators from these plaquette stabilizers
x_sites = []
for k in block_indices:
    x_sites.extend(xgroup_sites[k])

# --- extract the boundary loop ---
boundary = extract_boundary(x_sites)

# order boundary vertices cyclically
boundary = order_loop(boundary)

# close loop for plotting
boundary_loop = boundary + [boundary[0]]

# --- run circuit ---
qnode = make_excitation_qnode(
    dev,
    width,
    height,
    x_sites=x_sites,
    z_sites=[],
)
expvals = qnode()

n_x = len(xgroup_sites)
x_expvals = expvals[:n_x]
z_expvals = expvals[n_x:]

assert all(v > 0 for v in x_expvals), "X-group excitation detected!"
assert all(v > 0 for v in z_expvals), "Z-group excitation detected!"

# pretty printing
fmt = lambda arr: [f"{v:+.3f}" for v in arr]
print("Applied X-groups:", block_indices)
print("X-group expvals:", fmt(x_expvals))
print("Z-group expvals:", fmt(z_expvals))

# --- plot ---
fig, ax = excitation_plot(
    x_expvals,
    z_expvals,
    xgroup_sites,
    zgroup_sites,
    width,
    height,
)

# draw the X-loop (X operator = red)
xs, ys = zip(*boundary_loop)
ax.plot(xs, ys, color="firebrick", linewidth=6, zorder=5)
ax.scatter(xs, ys, color="firebrick", s=80, zorder=6)

plt.title("Fig 6: Contractible X-loop (no excitations)")
plt.savefig("fig6.png", dpi=200, bbox_inches="tight")
plt.show()