import pennylane as qml

from .groups import (
    build_xgroup_sites,
    build_xgroup_ops,
)
from .lattice import Wire, mod

def state_prep(width, height):
    xgroup_sites = build_xgroup_sites(width, height)

    # IMPORTANT: skip the last X-group (same as the guide)
    for sites in xgroup_sites[:-1]:
        control = mod(*sites[0], width, height)
        qml.Hadamard(control)

        for (i, j) in sites[1:]:
            qml.CNOT(wires=[control, mod(i, j, width, height)])