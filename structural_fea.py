import math
import numpy as np
import matplotlib.pyplot as plt

def generate_global_stiffness_matrix(num_elements=5, L=1.5, E=69e9, radius=0.126):

    # 1. MATERIAL & GEOMETRY DEFINITIONS

    A=math.pi*(radius**2)           # Cross-sectional area in square meters (m^2)
    num_nodes=num_elements+1        # Total connection points (nodes) in the mesh
    elements_length=L/num_elements  # Length of each section (element) in meters


    print(f"--- FEA MESH GENERATED ---")
    print(f"Nodes: {num_nodes}, Elements: {num_elements}, Element Length: {elements_length}m")

    # 2. LOCAL STIFFNESS MATRIX GENERATION

    k_element=(E*A)/elements_length                                # Calculate the exact stiffness constant (k) for one individual element
    local_stiffness_matrix=k_element*np.array([[1,-1],[-1,1]])     # 2x2 mathematical grid


    print("\n--- FEA MESH & STIFFNESS GENERATED ---")
    print(f"Calculated Spar Area: {A:.4f} m^2")
    print(f"Elemental Stiffness (k): {k_element:.2e} N/m")

    # 3. GLOBAL STIFFNESS MATRIX ASSEMBLY

    total_dofs=num_nodes*2
    global_stiffness_matrix=np.zeros((total_dofs,total_dofs))   # empty square matrix

    for i in range(num_elements):
        # Map axial stiffness to the vertical DOF (odd indices)
        idx1=i*2+1
        idx2=(i+1)*2+1
        global_stiffness_matrix[idx1,idx1]+=local_stiffness_matrix[0,0]
        global_stiffness_matrix[idx1,idx2]+=local_stiffness_matrix[0,1]
        global_stiffness_matrix[idx2,idx1]+=local_stiffness_matrix[1,0]
        global_stiffness_matrix[idx2,idx2]+=local_stiffness_matrix[1,1]


        # Torsional stability for the twist DOFs
        twist1=i*2
        twist2=(i+1)*2
        global_stiffness_matrix[twist1,twist1]+=k_element*0.1
        global_stiffness_matrix[twist2,twist2]+=k_element*0.1

    print("\n--- GLOBAL STIFFNESS MATRIX ASSEMBLED ---")
    print(f"Global Matrix Size: {total_dofs}x{total_dofs}")

    # 4. BOUNDARY CONDITIONS

    # Set the entire first row and first column to 0, and the top-left corner to 1 (Fixed root)
    global_stiffness_matrix[0,:]=0
    global_stiffness_matrix[:,0]=0
    global_stiffness_matrix[0,0]=1.0

    global_stiffness_matrix[1,:]=0
    global_stiffness_matrix[:,1]=0
    global_stiffness_matrix[1,1]=1.0

    return global_stiffness_matrix, num_nodes


def plot_deformation(displacement_vector, num_nodes, L=1.5):

    # 5. VISUALIZATION

    elements_length=L/(num_nodes-1)
    node_positions_x=np.array([i*elements_length for i in range(num_nodes)])    # Define the original x-positions
    scale_factor=50000.0                                                        # Define visual magnification

    # Extract only vertical DOFs for plotting
    vertical_displacements=displacement_vector[1::2]
    scaled_displacements_y=vertical_displacements*scale_factor                    # Stretches the calculated bending results

    plt.figure(figsize=(10,6))     # Define graph size

    # Plot 1: Baseline Spar (dotted gray line at y=0)
    plt.plot(node_positions_x, np.zeros(num_nodes), 'k--', label='Undeformed Spar (Reference)', alpha=0.5)

    # Plot 2: Deformed Shape (Blue solid line with markers at nodes)
    plt.plot(node_positions_x, scaled_displacements_y, 'b-o', linewidth=2, label=f'Deformed Shape (Scaled {scale_factor:.0e}x)')

    # Chart Formatting
    
    plt.title("Structural FEA Simulation: Linear Elastic Cantilever Deflection")
    plt.xlabel("Position Along Wing Span (meters)")
    plt.ylabel(f"Exaggerated Bending (Scaled meters)")
    plt.legend()
    plt.grid(True)  # Added measuring grid
    plt.show()