import pennylane as qml
from itertools import product

from .lattice import Wire, mod

def build_zgroup_sites(width, height):
    zgroup_sites = []

    for x, y in product(range(width // 2), range(height)):
        x0 = 2 * x + (y + 1) % 2
        sites = [
            (x0, y),
            (x0 + 1, y),
            (x0 + 1, y + 1),
            (x0, y + 1),
        ]
        zgroup_sites.append(sites)

    return zgroup_sites

def build_zgroup_ops(zgroup_sites, width, height):
    zgroup_ops = []

    for sites in zgroup_sites:
        op = qml.prod(
            *(qml.PauliZ(mod(i, j, width, height)) for (i, j) in sites)
        )
        zgroup_ops.append(op)

    return zgroup_ops

def build_xgroup_sites(width, height):
    xgroup_sites = []

    for x, y in product(range(width // 2), range(height)):
        x0 = 2 * x + y % 2
        sites = [
            (x0 + 1, y + 1),
            (x0,     y + 1),
            (x0,     y),
            (x0 + 1, y),
        ]

        # special reordering (same as guide)
        if x == width // 2 - 1 and y == 1:
            sites = sites[1:] + sites[:1]

        xgroup_sites.append(sites)

    return xgroup_sites

def build_xgroup_ops(xgroup_sites, width, height):
    xgroup_ops = []

    for sites in xgroup_sites:
        op = qml.prod(
            *(qml.PauliX(mod(i, j, width, height)) for (i, j) in sites)
        )
        xgroup_ops.append(op)

    return xgroup_ops