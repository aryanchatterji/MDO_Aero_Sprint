import math
import numpy as np

# 1. MATERIAL & GEOMETRY DEFINITIONS

E=69e9           # Young's Modulus in Pascals (Pa)
radius = 0.126   # Radius of the internal tubular spar in meters

A=math.pi*(radius**2)  # Cross-sectional area in square meters (m^2)
L=1.5                  # Total length of the wing in meters (m)

# 2. FINITE ELEMENT MESHING

num_elements=5  # Number of discrete sections to create
num_nodes=num_elements+1   #Total connection points (nodes) in the mesh
elements_length=L/num_elements   # Length of each section (element) in meters

print(f"--- FEA MESH GENERATED ---")
print(f"Nodes: {num_nodes}, Elements: {num_elements}, Element Length: {elements_length}m")

# 3. LOCAL STIFFNESS MATRIX GENERATION

k_element=(E*A)/elements_length   #Calculate the exact stiffness constant (k) for one individual element
local_stiffness_matrix=k_element*np.array([[1, -1], [-1, 1]])                                               # 2x2 mathematical grid
print("\n--- FEA MESH & STIFFNESS GENERATED ---")
print(f"Calculated Spar Area: {A:.4f} m^2")
print(f"Elemental Stiffness (k): {k_element:.2e} N/m")
print(f"Local Matrix:\n{local_stiffness_matrix}")

# 4. GLOBAL STIFFNESS MATRIX ASSEMBLY

global_stiffness_matrix=np.zeros((num_nodes,num_nodes))  #empty square matrix (6x6)

for i in range(num_elements):
    global_stiffness_matrix[i:i+2,i:i+2]+=local_stiffness_matrix  # Add the 2x2 local matrix into the overlapping positions in the global matrix

print("\n--- GLOBAL STIFFNESS MATRIX ASSEMBLED ---")
print(f"Global Matrix Size: {num_nodes}x{num_nodes}")
print(global_stiffness_matrix) 

# 5. BOUNDARY CONDITIONS & AERODYNAMIC LOADS

force_vector=np.zeros(num_nodes)  # A blank vector to hold the force values for each node
total_lift=500.0                  # Total lift force in Newtons (N)
nodal_force=total_lift/num_elements  # Distribute the total lift evenly across all elements
force_vector[1:]=nodal_force         # Apply the distributed force to all nodes except the root (node 0)

# Set the entire first row and first column to 0, and the top-left corner to 1
global_stiffness_matrix[0,:]=0
global_stiffness_matrix[:,0]=0
global_stiffness_matrix[0,0]=1.0 

force_vector[0]=0    # The root node is fixed, so it has no force applied

print("\n--- BOUNDARY CONDITIONS APPLIED ---")
print(f"Force Vector (N):\n{force_vector}")

# 6. SOLVING FOR DISPLACEMENT

displacement_vector=np.linalg.solve(global_stiffness_matrix,force_vector)

print("\n--- STRUCTURAL DEFORMATION RESULTS ---")

# Iterate through the vector to print the final position of each node
for i in range(num_nodes):
    disp_mm=displacement_vector[i]*1000.0   #meters to millimeters conversion
    print(f"Node {i} (Distance: {i * elements_length:.2f}m) -> Bending: {disp_mm:.4f} mm")


import matplotlib.pyplot as plt
# 7. VISUALIZATION

node_positions_x=np.array([i*elements_length for i in range(num_nodes)]) # Define the original x-positions of the nodes along the wing length
scale_factor=50000.0                                                     # Defines visual magnification
scaled_displacements_y=displacement_vector*scale_factor                  # Stretches the calculated bending results so they become visible               
plt.figure(figsize=(10,6))                                               # Define graph size

# Plot 1: Baseline Spar
# Plotted a dotted gray line at y=0, representing the original, unbent wing position
plt.plot(node_positions_x, np.zeros(num_nodes),'k--', label='Undeformed Spar (Reference)', alpha=0.5)

# Plot 2: Deformed Shape
# Plotted the new curved line based on FEA results (Blue solid line with markers at nodes)
plt.plot(node_positions_x, scaled_displacements_y, 'b-o', linewidth=2, label=f'Deformed Shape(Scaled {scale_factor:.0e}x)')

# Chart Formatting
plt.title("Structural FEA Simulation: Linear Elastic Cantilever Deflection")
plt.xlabel("Position Along Wing Span (meters)")
plt.ylabel(f"Exaggerated Bending (Scaled meters)")
plt.legend()
plt.grid(True)  # Added measuring grid


plt.show()