# 🔒 Authoritative Legend (Toric Code — this repository)

This legend defines the **unique interpretation** of all graphical elements in plots.
Anything that contradicts this legend is **wrong by definition**.

---

## 1️⃣ Stabilizers and anyons (SQUARES)

Squares represent **stabilizer measurements**.

A **dark square** means the stabilizer eigenvalue is **−1** → an **anyon is present**.  
A **light square** means eigenvalue **+1** → no anyon.

| Square color              | Stabilizer group     | Operator | Geometry  | Anyon                  |
| ------------------------- | -------------------- | -------- | --------- | ---------------------- |
| Lavender (light blue)     | Z-group satisfied    | ∏ Z      | Star      | none                   |
| **Steelblue (dark blue)** | **Z-group violated** | ∏ Z      | Star      | **Electric anyon (e)** |
| Mistyrose (light red)     | X-group satisfied    | ∏ X      | Plaquette | none                   |
| **Firebrick (dark red)**  | **X-group violated** | ∏ X      | Plaquette | **Magnetic anyon (m)** |

📌 **Rule (Kitaev convention):**

> **Z-group violations = electric anyons (e)**  
> **X-group violations = magnetic anyons (m)**

---

## 2️⃣ Local operators (DOTS)

Dots mark **where a single-qubit Pauli operator is applied**.

They are **not excitations**.

| Dot color   | Operator applied | Meaning                   |
| ----------- | ---------------- | ------------------------- |
| 🔴 Red dot  | Pauli-X          | Local X error / operation |
| 🔵 Blue dot | Pauli-Z          | Local Z error / operation |

📌 **Rule:**

> Dots show **operator support**, not anyons.

---

## 3️⃣ String operators (LINES)

Lines represent **string operators**, i.e. products of Pauli operators along a connected path of edges.

The **interior of a string is unobservable**; only endpoints matter.

| Line color   | String type  | Operator | Stabilizer violated | Anyon created    |
| ------------ | ------------ | -------- | ------------------- | ---------------- |
| 🔴 Red line  | **X-string** | ∏ X      | Z-group (stars)     | **Electric (e)** |
| 🔵 Blue line | **Z-string** | ∏ Z      | X-group (plaquettes)| **Magnetic (m)** |

📌 **Rule:**

> A string creates anyons of the **stabilizer type it anticommutes with**.

📌 **Important:**

> **String color ≠ anyon color.**  
> They are expected to be different.

---

## 4️⃣ String endpoints (ANYONS)

Every **open string** has **exactly two endpoints**.

| Endpoint square      | Stabilizer violated | Anyon            |
| -------------------- | ------------------- | ---------------- |
| **Steelblue square** | Z-group (stars)     | **Electric (e)** |
| **Firebrick square** | X-group (plaquettes)| **Magnetic (m)** |

📌 **Rule:**

> Open strings always create anyons **in pairs**.

---

## 5️⃣ Closed loops

| Loop type                     | Effect                                         |
| ----------------------------- | ---------------------------------------------- |
| Closed, contractible loop     | No excitations                                 |
| Closed, non-contractible loop | Logical operator (changes ground-state sector) |

📌 **Rule:**

> Closed **contractible** loops are physically invisible.

---

## 6️⃣ Boundaries and topology

| Graphical element      | Meaning           |
| ---------------------- | ----------------- |
| Dotted horizontal line | Periodic boundary |
| Dashed vertical line   | Periodic boundary |

This represents a **torus topology**.

---

## 7️⃣ One-line sanity check (use this forever)

* **Single X or X-string** → **Z-group flips (stars)** → **electric anyons (e)**
* **Single Z or Z-string** → **X-group flips (plaquettes)** → **magnetic anyons (m)**

If a figure violates this, the **label is wrong**, not the physics.