from toric.circuits import make_device, make_ground_state_qnode

width, height = 6, 4

dev = make_device(width, height)
circuit = make_ground_state_qnode(dev, width, height)

vals = circuit()
print([round(v, 6) for v in vals])