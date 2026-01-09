# Fig 8: Distinct ground states from non-contractible X-loops
# Logical operators change the global wavefunction
# while leaving all local stabilizers invariant.

import numpy as np

import pennylane as qml
from toric.circuits import make_device
from toric.lattice import all_wires, mod
from toric.state_prep import state_prep


width, height = 6, 4
dev = make_device(width, height)

wires = all_wires(width, height)


@qml.qnode(dev, diff_method=None)
def probs(x_sites):
    """
    Prepare ground state, apply optional X-loop(s),
    and return full probability distribution.
    """
    state_prep(width, height)

    for (i, j) in x_sites:
        qml.PauliX(mod(i, j, width, height))

    return qml.probs(wires=wires)


# --- define non-contractible loops ---
horizontal_loop = [(x, 1) for x in range(width)]
vertical_loop   = [(1, y) for y in range(height)]

# --- compute probabilities ---
P0 = probs([])                                   # |G>
Px = probs(horizontal_loop)                      # X_x |G>
Py = probs(vertical_loop)                        # X_y |G>
Pxy = probs(horizontal_loop + vertical_loop)     # X_x X_y |G>

overlap = np.dot(np.sqrt(P0), np.sqrt(Px))
print("Bhattacharyya overlap:", overlap)

# Note:
# Ground states related by logical X-loops may have
# identical computational-basis probabilities,
# despite being distinct quantum states.

def compare(name1, P1, name2, P2):
    diff = np.max(np.abs(P1 - P2))
    print(f"{name1} vs {name2}:")
    print(f"  max |ΔP| = {diff:.6e}")
    print()

print("\n=== Ground-state probability comparisons ===\n")
compare("|G>", P0, "X_x|G>", Px)
compare("|G>", P0, "X_y|G>", Py)
compare("|G>", P0, "X_x X_y|G>", Pxy)
compare("X_x|G>", Px, "X_y|G>", Py)
compare("X_x|G>", Px, "X_x X_y|G>", Pxy)
compare("X_y|G>", Py, "X_x X_y|G>", Pxy)