# Multidisciplinary Design Optimization (MDO) Aerospace Framework

## Abstract
This repository contains a custom-built Multidisciplinary Design Optimization (MDO) framework engineered to evaluate aerostructural coupling in aircraft wing design. Built entirely in Python, the project bridges the gap between aerodynamic load distribution and structural deflection, utilizing a partitioned approach to simulate aeroelastic static equilibrium without relying on black-box commercial software.

## Core Architecture

The framework is modular, separating the underlying physics engines into distinct sub-systems before linking them via a coupling matrix.

### 1. Structural Finite Element Analysis (FEA) Engine
*   **Module:** `structural_fea.py`
*   **Physics Implemented:** Calculates nodal displacements of a spatial wing beam under aerodynamic loading. The solver defines elemental properties (Young's Modulus, Cross-Sectional Area, Moment of Inertia), calculates local stiffness matrices, and transforms them into a global coordinate system.
*   **Visualization:** Integrates Matplotlib to generate a physical, real-time visual representation of the wing's deformation curve.

### 2. The Aerostructural Interface (Active Development)
*   **Module:** `aero_struct_bridge.py`
*   **Physics Implemented:** Acts as the aeroelastic translator. This module maps distributed aerodynamic lift (generated via VLM or equivalent aero engines) into discrete point loads corresponding to the structural nodes. 
*   **The Feedback Loop:** Executes a convergence loop where structural displacement alters aerodynamic geometry, iterating until the system reaches static aeroelastic equilibrium.

### 3. Aerodynamic Engine
*   **Module:** `wing_optimizer.py`
*   **Physics Implemented:** Handles core aerodynamic lift and drag coefficient calculations across the wing span.

## Computational Methodologies Demonstrated
*   **Matrix Algebra & Numerical Methods:** Extensive use of `numpy` for solving highly coupled linear systems (`K * U = F`).
*   **Partitioned MDO Logic:** Demonstrates advanced software architecture by keeping physics solvers isolated and relying on a master interface script to pass load/displacement data.
*   **Data Visualization:** Programmatic generation of structural deflection graphs to validate mathematical models against expected physical realities.

## Technical Stack
*   **Language:** Python 3.x
*   **Libraries:** NumPy (Matrix Operations), Matplotlib (Data Visualization)

---
*Note: This repository is maintained as a private portfolio of computational physics research and aerospace engineering development.*
