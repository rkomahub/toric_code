import pennylane as qml

from toric.lattice import Wire, mod, all_wires
from toric.groups import build_zgroup_sites
from toric.state_prep import state_prep

# ------------------------------------------------------------
# Geometry / device
# ------------------------------------------------------------
width, height = 6, 4

data_wires = all_wires(width, height)
anc = Wire(-1, -1)                       # ancilla wire
dev = qml.device("lightning.qubit", wires=data_wires + [anc])

# ------------------------------------------------------------
# Magnetic anyon pair (open X-string)
# ------------------------------------------------------------
x_string_m = [(1, 1), (2, 1)]   # same as before

# ------------------------------------------------------------
# Choose a CLOSED Z-loop = plaquette stabilizer
# with ODD overlap with x_string_m
# ------------------------------------------------------------
zgroup_sites = build_zgroup_sites(width, height)

def overlap(a, b):
    return len(set(a).intersection(set(b)))

k = None
for idx, plaq in enumerate(zgroup_sites):
    if overlap(plaq, x_string_m) == 1:
        k = idx
        break

assert k is not None, "No plaquette with odd overlap found"

z_loop = zgroup_sites[k]

print("Using plaquette:", z_loop)
print("Overlap with X-string:", set(z_loop).intersection(set(x_string_m)))

# ------------------------------------------------------------
# Closed Z-loop operator (UNITARY)
# ------------------------------------------------------------
def Z_loop_operator():
    for (i, j) in z_loop:
        qml.PauliZ(mod(i, j, width, height))

# ------------------------------------------------------------
# Hadamard test
# ------------------------------------------------------------
@qml.qnode(dev, diff_method=None)
def hadamard_test():
    # 1. prepare |psi> = X_string |G>
    state_prep(width, height)
    for (i, j) in x_string_m:
        qml.PauliX(mod(i, j, width, height))

    # ancilla |0>
    qml.Hadamard(anc)

    # 3. controlled-U (U = closed Z-loop)
    qml.ctrl(Z_loop_operator, control=anc)()

    # 4. second Hadamard
    qml.Hadamard(anc)

    # 5. measure Z on ancilla
    return qml.expval(qml.PauliZ(anc))

# ------------------------------------------------------------
# Run
# ------------------------------------------------------------
val = hadamard_test()
print("Hadamard-test result ⟨Z_anc⟩ =", f"{val:+.6f}")