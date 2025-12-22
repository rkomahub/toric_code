import pennylane as qml
from .lattice import mod

def horizontal_Z_loop(y, width, height):
    # Product of Z along a horizontal non-contractible loop
    return qml.prod(
        *[qml.PauliZ(mod(x, y, width, height)) for x in range(width)])

def vertical_X_loop(x0, width, height):
    # Product of X along a vertical non-contractible loop
    return qml.prod(*[qml.PauliX(mod(x0, y, width, height)) for y in range(height)])

def controlled_horizontal_Z_loop(ctrl, y, width, height):
    # Controlled-Z string wrapping horizontally
    for x in range(width):
        qml.ctrl(qml.PauliZ, control=ctrl)(mod(x, y, width, height))