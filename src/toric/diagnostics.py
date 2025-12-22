import numpy as np

def occupation_numbers(expvals):
    return [0.5 * (1 - np.round(v)) for v in expvals]

def energy(x_expvals, z_expvals):
    return -sum(x_expvals) - sum(z_expvals)

def print_info(x_expvals, z_expvals, E0):
    E = energy(x_expvals, z_expvals)
    print("Total energy:", round(E, 6))
    print("Energy above ground state:", round(E - E0, 6))
    print("X-group occupation numbers:", occupation_numbers(x_expvals))
    print("Z-group occupation numbers:", occupation_numbers(z_expvals))