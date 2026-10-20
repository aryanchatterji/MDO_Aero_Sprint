# Multidisciplinary Design Optimization (MDO) Aerospace Framework

## Abstract
This repository contains a custom-built Multidisciplinary Design Optimization (MDO) framework engineered to evaluate aerostructural coupling in aircraft wing design. Built entirely in Python, the project bridges the gap between aerodynamic load distribution and structural deflection, utilizing a partitioned approach to simulate aeroelastic static equilibrium without relying on black-box commercial software.

Crucially, this architecture deprecates static CAD exports (e.g., `.stl` files) in favor of a fully dynamic, programmatic physics engine. The geometry, structural matrix, and fluid-structure interactions are calculated and visualized in real-time purely through mathematics.

## Execution Instructions (How to Run)

**CRITICAL: Do not execute the component physics modules (`structural_fea.py` or `wing_optimizer.py`) individually.** 

To execute the complete multidisciplinary aerostructural pipeline and generate the geometry, you must run the master controller file:

`python aero_struct_bridge.py`

**What to expect upon execution:**
This master file utilizes Python's `multiprocessing` library to safely allocate the parallel physics engines across different CPU cores. Running this script will simultaneously:
1. Spawn the 2D structural FEA deformation graph (via Matplotlib)[cite: 8, 10].
2. Process the aerodynamic VLM constraints and launch the fully interactive 3D aerostructural model (via AeroSandbox)[cite: 8, 11].

## Core Architecture

The framework is highly modular, separating the underlying physics engines into distinct sub-systems before linking them via a mathematical coupling matrix.

### 1. Structural Finite Element Analysis (FEA) Engine
*   **Module:** `structural_fea.py`
*   **Physics Implemented:** Calculates nodal displacements of a spatial wing beam under aerodynamic loading. The solver calculates local stiffness matrices and transforms them into a global coordinate system. It relies on a custom implementation of Hooke's Law in matrix form ($[K]\{U\} = \{F\}$), injecting torsional stability protocols and rigid boundary conditions.
*   **Data Visualization:** Integrates Matplotlib to generate a physical, real-time visual representation of the wing's deformation curve against a baseline undeformed state.

### 2. Aerodynamic Optimization Engine
*   **Module:** `wing_optimizer.py`
*   **Physics Implemented:** Handles core aerodynamic lift and drag calculations. It acts as a programmatic fluid dynamics solver that dynamically bounds and optimizes wing geometry (Wingspan, Chord, Aspect Ratio) to minimize induced drag constraints ($C_{D_i} = \frac{C_L^2}{\pi e AR}$).
*   **3D Visualization:** Utilizes AeroSandbox to instantly wrap a mathematically optimized NACA 2412 airfoil around the calculated geometry, launching a fully interactive 3D rendering of the final drone configuration directly from the execution state.

### 3. The Master Controller & Aerostructural Interface
*   **Module:** `aero_struct_bridge.py`
*   **Physics Implemented:** Acts as the aeroelastic translator. This module rigorously sanitizes data payloads between libraries and maps distributed aerodynamic lift into discrete point loads corresponding to the structural nodes. 
*   **The Feedback Loop:** Executes a convergence `while` loop where structural displacement alters aerodynamic forces, mathematically forcing the two engines to interact until the displacement delta falls below a strict tolerance (static aeroelastic equilibrium).
*   **Parallel Processing:** Bypasses UI thread-blocking by utilizing Python's `multiprocessing` library to allocate the 2D matrix visualizations and the 3D AeroSandbox rendering to separate CPU cores, allowing simultaneous, non-blocking execution.

## Computational Methodologies Demonstrated
*   **Matrix Algebra & Numerical Methods:** Extensive use of pure `numpy` data structures for solving highly coupled linear systems while preventing data contamination from external calculus libraries.
*   **Partitioned MDO Logic:** Demonstrates advanced software architecture by keeping physics solvers isolated and relying on a master interface script to pass load/displacement data.
*   **Algorithmic Independence:** Validates theoretical aerospace models strictly through custom matrices and iteration loops, entirely replacing the need for external, commercially licensed simulation platforms.

## Technical Stack
*   **Language:** Python 3.x
*   **Libraries:** NumPy (Matrix Operations), Matplotlib (Data Visualization), AeroSandbox (Fluid Optimization & 3D Rendering), Multiprocessing (Parallel CPU Execution).

---
*Note: This repository is maintained as a public portfolio of computational physics research and aerospace engineering development.*
