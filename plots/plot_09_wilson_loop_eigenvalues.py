# plots/plot_09_wilson_loop_eigenvalues.py

import pennylane as qml

from toric.circuits import make_device
from toric.state_prep import state_prep
from toric.lattice import mod

width, height = 6, 4
dev = make_device(width, height)

def Wz_x():
    # horizontal Z Wilson loop
    return qml.prod(*[
        qml.PauliZ(mod(x, 1, width, height))
        for x in range(width)
    ])

def Wz_y():
    # vertical Z Wilson loop
    return qml.prod(*[
        qml.PauliZ(mod(1, y, width, height))
        for y in range(height)
    ])

@qml.qnode(dev, diff_method=None)
def measure_wilson_loops(x_sites):
    state_prep(width, height)

    # apply X logical operators
    for (i, j) in x_sites:
        qml.PauliX(mod(i, j, width, height))

    return (
        qml.expval(Wz_x()),
        qml.expval(Wz_y()),
    )

horizontal_loop = [(x, 1) for x in range(width)]
vertical_loop   = [(1, y) for y in range(height)]

states = {
    "|G>": [],
    "X_x|G>": horizontal_loop,
    "X_y|G>": vertical_loop,
    "X_x X_y|G>": horizontal_loop + vertical_loop,
}

print("\n=== Z-type Wilson loop eigenvalues ===\n")

for name, ops in states.items():
    Wx, Wy = measure_wilson_loops(ops)
    print(f"{name:12s}: ({Wx:+.1f}, {Wy:+.1f})")
