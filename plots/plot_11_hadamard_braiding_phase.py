import pennylane as qml
from toric.lattice import Wire, mod, all_wires
from toric.state_prep import state_prep

# ----------------------------
# Geometry / device
# ----------------------------
width, height = 6, 4
data_wires = all_wires(width, height)
anc = Wire(-1, -1)
dev = qml.device("lightning.qubit", wires=data_wires + [anc])


def loop(z_loop):
    """Closed Z-string (Wilson loop)"""
    for (i, j) in z_loop:
        qml.PauliZ(mod(i, j, width, height))


@qml.qnode(dev, diff_method=None)
def hadamard_test(x_prep, z_prep, z_loop):
    state_prep(width, height)

    for (i, j) in x_prep:
        qml.PauliX(mod(i, j, width, height))
    for (i, j) in z_prep:
        qml.PauliZ(mod(i, j, width, height))

    qml.Hadamard(anc)
    qml.ctrl(loop, control=anc)(z_loop)
    qml.Hadamard(anc)

    return qml.expval(qml.PauliZ(anc))

# ----------------------------
# Tutorial-style geometry
# ----------------------------

# create one e pair
x_prep = [(1, 1), (2, 1)] 

# create one m pair
z_prep = [(1, 3)]

# CLOSED loop enclosing the e anyon
z_loop = [(2, 3), (2, 2), (2, 1), (3, 1), (3, 2), (2, 3)]

val = hadamard_test(x_prep, z_prep, z_loop)
print("Braiding phase m around e:", val) # (x around z)