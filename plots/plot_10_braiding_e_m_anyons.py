# Braiding sanity check (auto-pick):
# - Create an m-pair with an open X-string.
# - Find a contractible closed Z-loop (plaquette stabilizer) with odd overlap.
# - Verify: (i) Z-loop alone creates no excitations, (ii) overlap is odd, (iii) anyons unchanged.
#
# NOTE: In toric code, the mutual braiding is encoded in operator algebra (odd intersection).
# Stabilizer plots show anyon locations, not the global braiding phase.

import numpy as np
import matplotlib.pyplot as plt
import pennylane as qml

from toric.circuits import make_device
from toric.groups import build_xgroup_sites, build_zgroup_sites
from toric.lattice import mod
from toric.state_prep import state_prep
from plots.common import excitation_plot  # keep consistent with your project layout


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def overlap_sites(a, b):
    return sorted(set(a).intersection(set(b)))

def find_odd_overlap_plaquette(zgroup_sites, x_string):
    # Prefer overlap=1 (simplest braiding witness)
    for idx, plaq in enumerate(zgroup_sites):
        if len(overlap_sites(plaq, x_string)) == 1:
            return idx
    # Fallback: any odd overlap
    for idx, plaq in enumerate(zgroup_sites):
        if len(overlap_sites(plaq, x_string)) % 2 == 1 and len(overlap_sites(plaq, x_string)) > 0:
            return idx
    return None

def build_stabilizer_ops(xgroup_sites, zgroup_sites, width, height):
    x_ops = [
        qml.prod(*(qml.PauliX(mod(i, j, width, height)) for (i, j) in sites))
        for sites in xgroup_sites
    ]
    z_ops = [
        qml.prod(*(qml.PauliZ(mod(i, j, width, height)) for (i, j) in sites))
        for sites in zgroup_sites
    ]
    return x_ops, z_ops

def count_violations(x_expvals, z_expvals):
    return sum(v < 0 for v in x_expvals), sum(v < 0 for v in z_expvals)

def polygon_edges(poly):
    # Close polygon boundary for plotting
    return poly + [poly[0]]


# ------------------------------------------------------------
# Lattice / device
# ------------------------------------------------------------
width, height = 6, 4
dev = make_device(width, height)

xgroup_sites = build_xgroup_sites(width, height)  # X-group stabilizers (stars)
zgroup_sites = build_zgroup_sites(width, height)  # Z-group stabilizers (plaquettes)
n_x = len(xgroup_sites)

# Pick a simple open X-string that definitely creates an m-pair
# (You can change this later; script will adapt.)
x_string_m = [(1, 1), (2, 1)]

# Auto-find a plaquette Z-loop with odd overlap (ideally 1) with that X-string
k = find_odd_overlap_plaquette(zgroup_sites, x_string_m)
assert k is not None, "No plaquette with odd overlap found. Try a different x_string_m."

z_loop_sites = zgroup_sites[k]
ov = overlap_sites(z_loop_sites, x_string_m)

print("\n=== Auto-picked braiding ingredients ===")
print("X-string (open, creates m-pair):", x_string_m)
print("Chosen plaquette index k:", k)
print("Z-loop sites (plaquette stabilizer):", z_loop_sites)
print("Overlap sites:", ov, " (count =", len(ov), ")")
print("Odd overlap? ", (len(ov) % 2 == 1))

# ------------------------------------------------------------
# QNode: measure all stabilizers
# ------------------------------------------------------------
x_ops, z_ops = build_stabilizer_ops(xgroup_sites, zgroup_sites, width, height)

@qml.qnode(dev, diff_method=None)
def measure_all(x_sites, z_sites):
    state_prep(width, height)

    for (i, j) in x_sites:
        qml.PauliX(mod(i, j, width, height))
    for (i, j) in z_sites:
        qml.PauliZ(mod(i, j, width, height))

    return [qml.expval(op) for op in (x_ops + z_ops)]

# Cases:
# A) ground state
# B) m-pair only (open X-string)
# C) Z-loop only (plaquette stabilizer, must be invisible)
# D) m-pair + Z-loop (should have same anyons as B)
exp_A = measure_all([], [])
exp_B = measure_all(x_string_m, [])
exp_C = measure_all([], z_loop_sites)
exp_D = measure_all(x_string_m, z_loop_sites)

def split(expvals):
    return expvals[:n_x], expvals[n_x:]

xA, zA = split(exp_A)
xB, zB = split(exp_B)
xC, zC = split(exp_C)
xD, zD = split(exp_D)

print("\n=== Stabilizer sanity checks ===")
print("Ground (A):          #X-viol, #Z-viol =", count_violations(xA, zA))
print("m-pair only (B):     #X-viol, #Z-viol =", count_violations(xB, zB), "  (expect 0,2)")
print("Z-loop only (C):     #X-viol, #Z-viol =", count_violations(xC, zC), "  (expect 0,0)")
print("m-pair + Z-loop (D): #X-viol, #Z-viol =", count_violations(xD, zD), "  (expect 0,2)")

# Hard assertions (these are the ones that should always hold)
assert count_violations(xC, zC) == (0, 0), "Z-loop is not excitation-free (not a true stabilizer loop)."
assert count_violations(xB, zB) == (0, 2), "Open X-string did not create exactly an m-pair."
assert count_violations(xD, zD) == (0, 2), "Adding the Z-loop changed local anyon content (should not)."
assert (len(ov) % 2 == 1), "Overlap is not odd; adjust x_string_m or loop selection."

print("\nAll checks passed: you have a contractible Z-loop with odd intersection with the m-string.\n"
      "This encodes the mutual braiding phase (-1) at the operator-algebra level.\n")

# ------------------------------------------------------------
# Plot (use case D: m-pair + Z-loop)
# ------------------------------------------------------------
fig, ax = excitation_plot(
    xD, zD,
    xgroup_sites, zgroup_sites,
    width, height
)

# Draw open X-string (red)
mx, my = zip(*x_string_m)
ax.plot(mx, my, color="firebrick", linewidth=6, zorder=5)
ax.scatter(mx, my, color="firebrick", s=80, zorder=6)

# Draw the plaquette boundary as a closed blue loop (ordered as given; close it)
loop_poly = polygon_edges(z_loop_sites)
lx, ly = zip(*loop_poly)
ax.plot(lx, ly, color="steelblue", linewidth=4, zorder=4, alpha=0.8)
ax.scatter(lx, ly, color="steelblue", s=60, zorder=5, alpha=0.8)

plt.title("Braiding witness: contractible Z-loop with odd intersection with an open X-string")
plt.show()