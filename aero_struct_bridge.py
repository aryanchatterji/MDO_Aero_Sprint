import numpy as np

# IMPORTING FROM YOUR OTHER FILES
from structural_fea import generate_global_stiffness_matrix, plot_deformation
from wing_optimizer import calculate_initial_lift, optimize_and_render_wing
def map_lift_to_nodes(aero_lift_distribution, num_struct_nodes):
    # 1. LOAD MAPPING
    """
    Translates continuous aerodynamic pressure into discrete point loads for the FEA solver.
    """
    nodal_force_vector = np.zeros(num_struct_nodes * 2)
    panels_per_node = len(aero_lift_distribution) // num_struct_nodes
    
    for i in range(num_struct_nodes):
        start_idx = i * panels_per_node
        end_idx = start_idx + panels_per_node
        
        nodal_lift = np.sum(aero_lift_distribution[start_idx:end_idx])
        vertical_dof = i * 2 + 1 
        nodal_force_vector[vertical_dof] = nodal_lift
        
    return nodal_force_vector

def aeroelastic_loop(initial_lift, global_stiffness_matrix, num_nodes):
    # 2. AEROELASTIC LOOP INITIALIZATION
    """
    Forces the aerodynamic and structural engines to interact iteratively 
    until static equilibrium is reached.
    """
    converged = False
    iteration = 0
    max_iter = 15      # Failsafe to prevent an infinite computational loop
    tolerance = 1e-4   # The physical threshold (in meters) to define "equilibrium"
    
    current_lift = initial_lift
    prev_displacement = np.zeros(num_nodes * 2) # Starting state: zero bending
    
    print("\n--- INITIATING AEROELASTIC COUPLING LOOP ---")
    
    # 3. ITERATIVE SOLVE & DEFORMATION TRACKING
    while not converged and iteration < max_iter:
        
        # Step A: Translate fluid physics to solid physics
        applied_forces = map_lift_to_nodes(current_lift, num_nodes)
        
        # Step B: Solve the fundamental FEA matrix equation (K * U = F)
        current_displacement = np.linalg.solve(global_stiffness_matrix, applied_forces)

        # 4. EQUILIBRIUM CHECK (CONVERGENCE)
        # Find the largest difference in bending between this iteration and the last
        max_diff = np.max(np.abs(current_displacement - prev_displacement))
        print(f"Iteration {iteration}: Max Displacement Delta = {max_diff:.6f}m")

        if max_diff < tolerance:
            converged = True
            print(">>> AEROELASTIC EQUILIBRIUM ACHIEVED <<<")
            break

        prev_displacement = current_displacement
        iteration += 1

    return current_displacement, applied_forces


if __name__ == "__main__":
    # 5. MASTER EXECUTION BLOCK
    print("--- BOOTING MDO FRAMEWORK ---")

    # Define the resolution of your wing structure
    NUM_ELEMENTS = 5
    NUM_NODES = NUM_ELEMENTS + 1

    # Generate the structural stiffness matrix (K) from your FEA engine
    global_K_matrix = generate_global_stiffness_matrix(num_elements=NUM_ELEMENTS)

    # Get the initial lift data from your Aerodynamic engine
    mock_initial_lift = calculate_initial_lift(num_panels=50)

    # Execute the coupling loop
    final_displacement, final_forces = aeroelastic_loop(
        initial_lift=mock_initial_lift,
        global_stiffness_matrix=global_K_matrix,
        num_nodes=NUM_NODES
    )

    print("--- MDO SIMULATION COMPLETE ---")

    # 6. VISUALIZATIONS (2D THEN 3D)
    print("Plotting 2D Structural Deformation...")
    plot_deformation(final_displacement, num_nodes=NUM_NODES)
    
    print("\nLaunching 3D Aerodynamic Model...")
    optimize_and_render_wing()
                                                        