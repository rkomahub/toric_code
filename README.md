# 🧲 Toric Code in PennyLane

**A step-by-step implementation of the toric code, its ground states, excitations, and anyonic braiding**

---

## Overview

This project is a **pedagogical and modular implementation of the toric code** using

[PennyLane](https://pennylane.ai/) as a quantum simulation framework.

The toric code is a paradigmatic model of **topological order**, featuring:

- a degenerate ground-state manifold
- electric ($e$) and magnetic ($m$) anyonic excitations
- string operators and homotopy invariance
- non-trivial braiding statistics revealed via a Hadamard test

The goal of this repository is not just to *simulate* the toric code, but to make its
**physics transparent, visual, and reproducible**.

---

## Features

✅ Explicit preparation of the toric-code ground state

✅ Measurement of all stabilizers (X-groups and Z-groups)

✅ Creation and transport of $e$ and $m$ anyons via string operators

✅ Contractible and non-contractible loops on the torus

✅ Ground-state degeneracy and Wilson loops

✅ Braiding of $e$ and $m$ anyons

✅ Extraction of the braiding phase using the **Hadamard test**

✅ High-quality lattice visualizations with matplotlib

---

## Repository Structure

```bash
toric_code/
├── src/
│   └── toric/              # Core toric-code package
│       ├── circuits.py
│       ├── state_prep.py
│       ├── lattice.py
│       ├── groups.py
│       ├── stabilizers.py
│       ├── loops.py
│       ├── diagnostics.py
│       └── plot_groups.py
│
├── plots/                  # Executable plotting scripts
│   ├── plot_00_ground_state.py
│   ├── plot_01_electric_anyons.py
│   ├── plot_02_magnetic_anyons.py
│   ├── ...
│   └── plot_11_hadamard_braiding_phase.py
│
├── tests/                  # Pytest test suite
│
├── pyproject.toml
├── README.md
└── figures / outputs
```

---

## Installation (Recommended Workflow)

### 1. Clone the repository

```bash
gitclone https://github.com/your-username/toric-code.git
cd toric-code
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the project in editable mode

```bash
pip install -e .
```

This is required so that the `toric` package (located in `src/`) is correctly

discoverable by Python.

---

## Running the Examples

All plots are executable as Python modules from the project root.

Example: **ground state**

```bash
python3 -m plots.plot_00_ground_state
```

Each script:

- prepares a quantum state
- measures stabilizers
- visualizes the lattice and excitations

---

## Plotting Backend (Important)

This project uses `plt.show()` for interactive visualization.

If you are on Linux / WSL and want figures to open in windows, you must install

the **system Tk backend**:

```bash
sudo apt install python3-tk
```

Then, in each plotting script, matplotlib uses the `TkAgg` backend.

If you prefer file output instead, simply replace `plt.show()` with:

```python
plt.savefig("figure.png", dpi=200, bbox_inches="tight")
```

---

## Physics Background

- Qubits live on the edges of a square lattice embedded on a torus
- X-type and Z-type stabilizers commute and define the Hamiltonian
- Violated stabilizers correspond to **anyonic excitations**
- String operators create, move, and annihilate anyons
- Only the **homotopy class** of a string matters, not its geometry
- Braiding an $e$ around an $m$ produces a non-trivial phase

The Hadamard test is used to extract this phase directly from the quantum circuit.

---

## Testing

A full pytest suite verifies:

- correct ground-state preparation
- correct stabilizer eigenvalues
- string operator behavior
- non-contractible loops
- braiding and phase detection

---

## Dependencies

- Python ≥ 3.10
- PennyLane
- PennyLane-Lightning
- NumPy
- Matplotlib

All Python dependencies are listed in `pyproject.toml`.

---

## Final Note

The toric code is not just a quantum error-correcting code — it is a **topological theory disguised as a circuit**. Enjoy bending space, dragging anyons around holes, and watching global phases emerge from local moves.