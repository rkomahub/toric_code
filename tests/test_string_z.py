from toric.circuits import make_device, make_excitation_qnode
from toric.diagnostics import print_info

width, height = 6, 4
E0 = -24
dev = make_device(width, height)

# Z string (path 1)
z_string = [(1, 2), (2, 2), (3, 2)]

# Z string (path 2) same endspoints
"""
Expected: identical occupation numbers and energy as path 1
(homotopy invariance)
"""
# z_string = [(1, 2), (1, 1), (2, 1), (3, 2)]

# Z string (contractible closed loop -> no quasiparticle excitation)
"""
Expected: all occupation numbers zero, ground-state energy
The loop created particles, moved them, and annihilated them.
"""
# z_loop = [(1, 2), (2, 2), (2, 3), (1, 3), (1, 2)]


circuit = make_excitation_qnode(dev, width, height, z_sites=z_string)
vals = circuit()

n_x = (width // 2) * height
x_vals = vals[:n_x]
z_vals = vals[n_x:]

print("X-groups:", [round(v, 6) for v in x_vals])
print("Z-groups:", [round(v, 6) for v in z_vals])

print_info(x_vals, z_vals, E0)