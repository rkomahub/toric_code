import pennylane as qml
from toric.circuits import make_device
from toric.state_prep import state_prep
from toric.loops import controlled_horizontal_Z_loop
from toric.lattice import all_wires, Wire, mod

width, height = 6, 4

# System wires (same Wire objects as everywhere else)
system_wires = all_wires(width, height)

# Add ancilla wire (must be hashable, non-iterable)
ancilla = "ancilla"

dev = qml.device(
    "lightning.qubit",
    wires=[ancilla] + system_wires
)

@qml.qnode(dev, diff_method=None)
def hadamard_test(loop_applied=False):
    # Prepare system ground state
    state_prep(width, height)

    # Optionally change topological sector
    if loop_applied:
    # Apply an X-loop that crosses the controlled Z-loop once
        x0 = 1
        for y in range(height):
            qml.PauliX(mod(x0, y, width, height))  # non-contractible X loop

    # Ancilla Hadamard
    qml.Hadamard("ancilla")

    # Controlled loop operator
    controlled_horizontal_Z_loop("ancilla", y=2, width=width, height=height)

    # Final Hadamard
    qml.Hadamard("ancilla")

    # Measure ancilla
    return qml.expval(qml.PauliZ("ancilla"))

print("Hadamard test on GS:", hadamard_test(loop_applied=False))
print("Hadamard test after Z-loop:", hadamard_test(loop_applied=True))