from toric.circuits import make_device, make_full_measurement_qnode

width, height = 6, 4

dev = make_device(width, height)
circuit = make_full_measurement_qnode(dev, width, height)

vals = circuit()

n_x = (width // 2) * height
x_vals = vals[:n_x]
z_vals = vals[n_x:]

print("X-groups:", [round(v, 6) for v in x_vals])
print("Z-groups:", [round(v, 6) for v in z_vals])

E0 = -sum(x_vals) - sum(z_vals)
print("Ground-state energy:", round(E0, 6))