import aerosandbox as asb
import aerosandbox as np
import math
# Initialize the optimization environment
opti=asb.Opti()

# 2. DESIGN VARIABLES

wingspan=opti.variable(init_guess=2.0, lower_bound=0.5, upper_bound=4.0)
chord=opti.variable(init_guess=0.5, lower_bound=0.1, upper_bound=1.5)

# 3. PHYSICS CONSTRAINTS

wing_area=wingspan*chord
opti.subject_to(wing_area==1.5)

# 4. AERODYNAMIC CALCULATIONS

# The algorithm calculates Aspect Ratio dynamically as it changes the wingspan
aspect_ratio=(wingspan**2)/wing_area
C_L=0.5   # Lift Coefficient (constant for steady flight)
e=0.9     # Oswald efficiency number (aerodynamic efficiency of the wing shape)

# Induced Drag Formula
induced_drag=(C_L**2)/(math.pi*e*aspect_ratio)    

# 5. THE OBJECTIVE FUNCTION

# commanding the solver to find the geometry that makes this number as small as mathematically possible
opti.minimize(induced_drag)

# 6. EXECUTING THE SOLVER

sol=opti.solve()

# 7. THE OUTPUT

print("\n--- OPTIMIZED WING GEOMETRY ---")
print(f"Calculated Wingspan: {sol.value(wingspan):.2f} meters")
print(f"Calculated Chord: {sol.value(chord):.2f} meters")
print(f"Final Aspect Ratio: {sol.value(aspect_ratio):.2f}")
print(f"Minimum Induced Drag: {sol.value(induced_drag):.4f}")

input("\nPress Enter to launch 3D render...")

# 8. THE 3D GEOMETRY

# We use the optimized numbers to generate a physical Wing object
optimized_wing=asb.Wing(
    name="Optimized Wing",
    symmetric=True,     # This mirrors the right side to create a full wing
    xsecs=[
                # Cross-section 1: The center of the wing (Root)
                asb.WingXSec(
                    xyz_le=[0,0,0],
                    chord=sol.value(chord),
                    airfoil=asb.Airfoil("naca2412")
                ),
                # Cross-section 2: The tip of the wing
                asb.WingXSec(
                    xyz_le=[0,sol.value(wingspan)/2,0],
                    chord=sol.value(chord),
                    airfoil=asb.Airfoil("naca2412")
                )  
    ]
)

# 9. ASSEMBLE AND VISUALIZE

# Package the wing into an Airplane object
airplane=asb.Airplane(
    name="MDO_Drone",
    wings=[optimized_wing]
)

# Launch the 3D viewer
print("Generating 3D model...")
airplane.draw(show=True)

import trimesh

# 10. EXPORT TO MANUFACTURING (THE ROBUST WAY)

print("\nExtracting raw mathematical mesh...")
# We extract the raw 3D coordinates (points) and triangles (faces) directly from the engine
points, faces = airplane.mesh_body(method='tri')

# We feed those raw matrices into Trimesh to construct a physical 3D object
print("Compiling geometry...")
mesh = trimesh.Trimesh(vertices=points, faces=faces)

# Export the final STL
print("Exporting STL file for 3D printing...")
mesh.export("optimized_wing.stl")
print("Done! Check your folder.")