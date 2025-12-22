import pennylane as qml

from .lattice import all_wires, mod
from .groups import (
    build_zgroup_sites,
    build_zgroup_ops,
    build_xgroup_sites,
    build_xgroup_ops,
)
from .state_prep import state_prep


def make_device(width: int, height: int, backend: str = "lightning.qubit"):
    """
    Create a PennyLane device whose wires are the edge-qubits of the toric lattice.
    """
    wires = all_wires(width, height)
    return qml.device(backend, wires=wires)

def build_groups(width, height):
    z_sites = build_zgroup_sites(width, height)
    x_sites = build_xgroup_sites(width, height)

    z_ops = build_zgroup_ops(z_sites, width, height)
    x_ops = build_xgroup_ops(x_sites, width, height)

    return x_sites, z_sites, x_ops, z_ops

def make_group_measurement_qnode(dev, width, height):
    x_sites, z_sites, x_ops, z_ops = build_groups(width, height)
    """
    Returns a QNode that (for now) starts in |0...0> and measures <A_i>, <B_j>.
    This is just a sanity check that our stabilizer objects and wire labels work.
    """

    @qml.qnode(dev) # decorator turn it into a quantum circuit that runs on the device dev
    def circuit():
        # No gates yet: default state is |0...0>
        # Later we'll add state prep / projection.
        return [qml.expval(op) for op in (x_ops + z_ops)]

    return circuit

def make_ground_state_qnode(dev, width, height):
    x_ops = build_xgroup_ops(
        build_xgroup_sites(width, height),
        width,
        height,
    )

    @qml.qnode(dev, diff_method=None)
    def circuit():
        state_prep(width, height)
        return [qml.expval(op) for op in x_ops]

    return circuit

def make_full_measurement_qnode(dev, width, height):
    x_sites, z_sites, x_ops, z_ops = build_groups(width, height)

    @qml.qnode(dev, diff_method=None)
    def circuit():
        state_prep(width, height)
        return [qml.expval(op) for op in (x_ops + z_ops)]

    return circuit

def make_excitation_qnode(dev, width, height, x_sites=None, z_sites=None):
    x_sites = x_sites or []
    z_sites = z_sites or []

    x_sites_g, z_sites_g, x_ops, z_ops = build_groups(width, height)

    @qml.qnode(dev, diff_method=None)
    def circuit():
        state_prep(width, height)

        # apply perturbations
        for (i, j) in x_sites:
            qml.PauliX(mod(i, j, width, height))
        for (i, j) in z_sites:
            qml.PauliZ(mod(i, j, width, height))

        return [qml.expval(op) for op in (x_ops + z_ops)]

    return circuit