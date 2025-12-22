import pennylane as qml
from toric.circuits import make_device
from toric.state_prep import state_prep
from toric.loops import horizontal_Z_loop, vertical_X_loop
from toric.lattice import mod

width, height = 6, 4
dev = make_device(width, height)

y0 = 2   # where the Z-loop lives
x0 = 1   # choose an x that crosses it once

@qml.qnode(dev, diff_method=None)
def measure_Xloop_on_ground():
    state_prep(width, height)
    return qml.expval(vertical_X_loop(x0, width, height))

@qml.qnode(dev, diff_method=None)
def measure_Xloop_after_Zloop():
    state_prep(width, height)

    # Apply a non-contractible Z loop around x direction
    for x in range(width):
        qml.PauliZ(mod(x, y0, width, height))

    # Measure the intersecting X loop (should flip)
    return qml.expval(vertical_X_loop(x0, width, height))

print("X-loop on GS:", measure_Xloop_on_ground())
print("X-loop after Z-loop:", measure_Xloop_after_Zloop())
