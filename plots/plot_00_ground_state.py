# Graph 0: Ground state (no excitations)

import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

from toric.circuits import make_device, make_excitation_qnode
from toric.groups import build_xgroup_sites, build_zgroup_sites
from .common import excitation_plot

# Lattice size
width, height = 6, 4

# Build device
dev = make_device(width, height)

# Ground state = no perturbations
ground_qnode = make_excitation_qnode(
    dev,
    width,
    height,
    x_sites=[],
    z_sites=[],
)

# Run circuit
expvals = ground_qnode()

# Split expectation values
n_x = len(build_xgroup_sites(width, height))
x_expvals = expvals[:n_x]
z_expvals = expvals[n_x:]

# Print expectation values
print("X-group expvals:", x_expvals)
print("Z-group expvals:", z_expvals)

# Plot
fig, ax = excitation_plot(
    x_expvals,
    z_expvals,
    build_xgroup_sites(width, height),
    build_zgroup_sites(width, height),
    width,
    height,
)

plt.title("Ground state of the toric code (no excitations)")
plt.show()