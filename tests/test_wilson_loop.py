from toric.circuits import make_device, make_excitation_qnode
from toric.loops import horizontal_Z_loop
import pennylane as qml

width, height = 6, 4
dev = make_device(width, height)

# Ground state (no loop applied)
@qml.qnode(dev, diff_method=None)
def ground_state():
    from toric.state_prep import state_prep
    state_prep(width, height)
    return qml.expval(horizontal_Z_loop(y=2, width=width, height=height))

# Ground state with non-contractible loop applied
z_loop = [(x, 2) for x in range(width)]
excited = make_excitation_qnode(dev, width, height, z_sites=z_loop)

print("Wilson loop (original GS):", ground_state())
print("Wilson loop (looped GS):", excited()[-1])  # last measurement
