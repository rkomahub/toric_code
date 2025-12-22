import pennylane as qml
from .lattice import Wire, mod

def star_wires(x: int, y: int, Lx: int, Ly: int):
    """The 4 edge-qubits touching the vertex (x,y)."""
    return [
        Wire(x, y, "h"),                 # right-going horizontal
        Wire(mod(x - 1, Lx), y, "h"),     # left-going horizontal (wraps)
        Wire(x, y, "v"),                 # up-going vertical
        Wire(x, mod(y - 1, Ly), "v"),     # down-going vertical (wraps)
    ]

def plaquette_wires(x: int, y: int, Lx: int, Ly: int):
    """The 4 edge-qubits around the plaquette with lower-left corner (x,y)."""
    return [
        Wire(x, y, "h"),                 # bottom edge
        Wire(x, mod(y + 1, Ly), "h"),     # top edge
        Wire(x, y, "v"),                 # left edge
        Wire(mod(x + 1, Lx), y, "v"),     # right edge
    ]

def A_star(x: int, y: int, Lx: int, Ly: int):
    """Star stabilizer A_{x,y} = product of X on the 4 star edges."""
    return qml.prod(*[qml.PauliX(w) for w in star_wires(x, y, Lx, Ly)])

def B_plaquette(x: int, y: int, Lx: int, Ly: int):
    """Plaquette stabilizer B_{x,y} = product of Z on the 4 plaquette edges."""
    return qml.prod(*[qml.PauliZ(w) for w in plaquette_wires(x, y, Lx, Ly)])

def all_stabilizers(Lx: int, Ly: int):
    """Lists of all star and plaquette stabilizers."""
    A = [A_star(x, y, Lx, Ly) for x in range(Lx) for y in range(Ly)]
    B = [B_plaquette(x, y, Lx, Ly) for x in range(Lx) for y in range(Ly)]
    return A, B