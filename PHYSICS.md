# Toric Code Physics Contract

This repository implements a toric-code–like stabilizer model on a periodic square lattice (a torus). Qubits live on **edges**, stabilizers live on **stars** and **plaquettes**, and open string operators create **pairs of anyonic excitations at endpoints only**.

This document states the non-negotiable rules the code must satisfy.

---

## 0. Objects and where they live

### Lattice and wires

* A physical qubit is addressed by a **Wire** with coordinates `Wire(x, y)`.
* Periodic boundary conditions are enforced by:

  * `mod(i, j, width, height) -> Wire(i % width, j % height)`

**Contract:** Any indexing of qubits must pass through `mod(...)` (or be equivalent) to respect the torus.

---

## 1. Stabilizers in this code

The stabilizers are built in `groups.py`:

### Star stabilizers (electric sector)

* Built by: `build_zgroup_sites(width, height)`
* Operator: `build_zgroup_ops(...)` produces products of **PauliZ** on 4 edges.

So in the code:

* **Z-group operators are star stabilizers**
  \[
  A_s = \prod_{e \in \text{star}(s)} Z_e
  \]

**Contract:** A violation of a Z-group operator (expectation value negative, ideally (-1)) represents an **electric anyon (e)**.

### Plaquette stabilizers (magnetic sector)

* Built by: `build_xgroup_sites(width, height)`
* Operator: `build_xgroup_ops(...)` produces products of **PauliX** on 4 edges.

So in the code:

* **X-group operators are plaquette stabilizers**
  \[
  B_p = \prod_{e \in \partial p} X_e
  \]

**Contract:** A violation of an X-group operator represents a **magnetic anyon (m)**.

> Note: This matches the Kitaev toric code convention: stars are Z-type (electric), plaquettes are X-type (magnetic).

---

## 2. Excitations and what a plot means

In `excitation_plot(...)`:

* Z-group (stars):

  * `steelblue` if `z_expval < 0` (excited)
  * `lavender` if `z_expval > 0` (ground)
* X-group (plaquettes):

  * `firebrick` if `x_expval < 0` (excited)
  * `mistyrose` if `x_expval > 0` (ground)

**Contract:**

* A *dark* square/patch means the stabilizer eigenvalue is **(-1)** (or expval < 0) → an anyon is present.
* A *light* square/patch means eigenvalue **(+1)** (or expval > 0) → no anyon.

**Crucial:** colored polygons represent **stabilizer measurements**, not operator support.

---

## 3. String operators and which anyons they create

The excitation circuit applies local Paulis in `make_excitation_qnode`:

* `x_sites` applies **PauliX** on selected edge-qubits.
* `z_sites` applies **PauliZ** on selected edge-qubits.

### X-string (product of X along a path)

If you apply an open string:
\[
W^X(\gamma) = \prod_{e\in\gamma} X_e
\]
then:

* It **commutes** with all plaquette stabilizers (B_p).
* It **anticommutes** with **star** stabilizers (A_s) only at the **endpoints**.

**Contract:** An open X-string creates exactly **two electric anyons (e)**:

* **Z-group** shows exactly **two violations** (two expvals < 0)
* **X-group** remains all +1 (all expvals > 0)

### Z-string (product of Z along a path)

If you apply an open string:
\[
W^Z(\gamma) = \prod_{e\in\gamma} Z_e
\]
then:

* It **commutes** with all star stabilizers (A_s).
* It **anticommutes** with **plaquette** stabilizers (B_p) only at the **endpoints**.

**Contract:** An open Z-string creates exactly **two magnetic anyons (m)**:

* **X-group** shows exactly **two violations**
* **Z-group** remains all +1

---

## 4. Endpoint-only rule (no “extra pairs” along the string)

**Contract:** For a *connected* open string of uniform Pauli type (all X or all Z),

* excitations may appear **only at endpoints**,
* never in the interior.

If you observe interior excitations, one of these is true:

* the “string” is not actually connected (has breaks),
* the operator type is mixed (X and Z interleaved),
* the coordinate→edge mapping is inconsistent with the stabilizer geometry,
* or you are plotting operator support and stabilizers in a visually confusing way.

---

## 5. Homotopy invariance

Two strings with the **same endpoints** and the **same Pauli type** but different interior routes are physically equivalent on a torus up to multiplication by stabilizers.

**Contract:** Changing the route of a string without changing its endpoints must not change:

* which stabilizers are violated,
* how many violations exist (should remain 2),
* the endpoint locations of the anyons.

This is exactly what you were testing in “homotopic string” figures.

---

## 6. Closed loops

### Contractible loop

A closed, contractible loop of X or Z operators should create **no anyons**:

* all stabilizers remain +1.

### Non-contractible loop (around the torus)

A closed, non-contractible loop acts as a **logical operator**:

* it should still create **no local anyons**,
* but it changes the **topological sector** (logical state).

(The current `state_prep` chooses a particular stabilizer-defined state; adding logical-loop tests is a good next verification.)

---

## 7. Ground-state preparation contract (the `state_prep`)

The `state_prep(width, height)` constructs a stabilizer-like state by iterating over **Z-group sites** and applying:

* `H` on the first qubit of the group
* CNOTs from that control to the other three edges
* and it explicitly **skips the last Z-group**, matching the guide.

**Contract:** After `state_prep`, measuring the Z-group stabilizers (except the skipped dependency) should yield **+1** (up to numerical tolerance). The `make_ground_state_qnode` is already a partial check of this.

---

## 8. Naming and documentation (to prevent future confusion)

**Contract:** In documentation and figure captions, prefer **geometry** over Pauli letters:

* Z-group = **stars** = **electric sector (e anyons)**
* X-group = **plaquettes** = **magnetic sector (m anyons)**

When describing strings:

* **X-string creates e anyons** (violates stars → Z-group)
* **Z-string creates m anyons** (violates plaquettes → X-group)

Colors are allowed to be arbitrary, but captions must follow physics.

---

# Quick “sanity checklist” for any run

For an open connected string:

* **Z-string (z_sites nonempty):**

  * X-group: exactly 2 negative expvals
  * Z-group: 0 negative expvals

* **X-string (x_sites nonempty):**

  * Z-group: exactly 2 negative expvals
  * X-group: 0 negative expvals

If not, the run violates the contract.
