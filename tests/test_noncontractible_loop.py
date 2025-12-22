from toric.circuits import make_device, make_excitation_qnode
from toric.diagnostics import print_info

width, height = 6, 4
E0 = -24

dev = make_device(width, height)

# Non-contractible Z loop (wraps around x direction)
z_loop = [(x, 2) for x in range(width)]

circuit = make_excitation_qnode(dev, width, height, z_sites=z_loop)
vals = circuit()

n_x = (width // 2) * height
x_vals = vals[:n_x]
z_vals = vals[n_x:]

print_info(x_vals, z_vals, E0)
