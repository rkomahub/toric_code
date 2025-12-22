from dataclasses import dataclass # simple immutable data containers

@dataclass(frozen=True)
class Wire:
    """
    Label for a physical qubit living on vertices of the square-lattice.
    (x, y) identifies the lattice cell.
    """
    x: int      # x-coordinate of the lattice cell
    y: int      # y-coordinate of the lattice cell

def mod(i: int, j: int, width: int, height: int) -> Wire:
    """
    Periodic boundary condition: wraps index a into range [0, L-1].
    Implements the torus topology.
    """
    return Wire(i % width, j % height)


def all_wires(width: int, height: int):
    """
    Generate all edge-qubits of an Lx*Ly toric lattice.
    """
    return [Wire(i, j) for i in range(width) for j in range(height)]