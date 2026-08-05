import numpy as np
import multiprocessing # Added for parallel core execution

# IMPORTING FROM YOUR OTHER FILES
from structural_fea import generate_global_stiffness_matrix, plot_deformation
from wing_optimizer import calculate_initial_lift, optimize_and_render_wing

def map_lift_to_nodes(aero_lift_distribution, num_struct_nodes):

    # 1. LOAD MAPPING

    nodal_force_vector = np.zeros(num_struct_nodes * 2)
    panels_per_node = len(aero_lift_distribution) // num_struct_nodes
    clean_aero_lift = [float(x) for x in aero_lift_distribution]
    
    for i in range(num_struct_nodes):
        start_idx = i * panels_per_node
        end_idx = start_idx + panels_per_node
        nodal_lift = sum(clean_aero_lift[start_idx:end_idx])
        vertical_dof = i * 2 + 1 
        nodal_force_vector[vertical_dof] = nodal_lift
        
    return nodal_force_vector

def aeroelastic_loop(initial_lift, global_stiffness_matrix, num_nodes):

    # 2. AEROELASTIC LOOP INITIALIZATION

    converged = False
    iteration = 0
    max_iter = 15      
    tolerance = 1e-4   
    
    current_lift = initial_lift
    prev_displacement = np.zeros(num_nodes * 2) 
    
    print("\n--- INITIATING AEROELASTIC COUPLING LOOP ---")
    
    # 3. ITERATIVE SOLVE & DEFORMATION TRACKING

    while not converged and iteration < max_iter:
        
        applied_forces = map_lift_to_nodes(current_lift, num_nodes)
        
        # --- ARMOR PLATING FAILSAFE ---
        # If the structural module accidentally passes a tuple (Matrix, Old_Vector),
        # this intercepts it, strips the junk, and keeps only the pure matrix.

        if isinstance(global_stiffness_matrix, tuple):
            global_stiffness_matrix = global_stiffness_matrix[0]
            
        # Force strict NumPy float matrices to prevent CasADi or sequence errors
        safe_K_matrix = np.array(global_stiffness_matrix, dtype=float)
        safe_forces = np.array(applied_forces, dtype=float)
        # ------------------------------
        
        # Step B: Solve the fundamental FEA matrix equation (K * U = F)

        current_displacement = np.linalg.solve(safe_K_matrix, safe_forces)

        # 4. EQUILIBRIUM CHECK (CONVERGENCE)

        max_diff = np.max(np.abs(current_displacement - prev_displacement))
        print(f"Iteration {iteration}: Max Displacement Delta = {max_diff:.6f}m")

        if max_diff < tolerance:
            converged = True
            print(">>> AEROELASTIC EQUILIBRIUM ACHIEVED <<<")
            break

        prev_displacement = current_displacement
        iteration += 1

    return current_displacement, safe_forces


if __name__ == "__main__":
    # 5. MASTER EXECUTION BLOCK

    # Safety lock required for Windows multiprocessing
    multiprocessing.freeze_support()

    print("--- BOOTING MDO FRAMEWORK ---")

    NUM_ELEMENTS = 5
    NUM_NODES = NUM_ELEMENTS + 1

    raw_K_matrix = generate_global_stiffness_matrix(num_elements=NUM_ELEMENTS)
    mock_initial_lift = calculate_initial_lift(num_panels=50)

    final_displacement, final_forces = aeroelastic_loop(
        initial_lift=mock_initial_lift,
        global_stiffness_matrix=raw_K_matrix,
        num_nodes=NUM_NODES
    )

    print("--- MDO SIMULATION COMPLETE ---")

    print("--- MDO SIMULATION COMPLETE ---")

    # --- PARALLEL MULTIPROCESSING TRIGGER ---
    print("\nLaunching 2D and 3D Engines Simultaneously...")
    
    # 1. Spawns the 2D graph on CPU Core 1
    graph_process = multiprocessing.Process(
        target=plot_deformation, 
        args=(final_displacement, NUM_NODES)
    )
    graph_process.start()

    # 2. While Core 1 handles the 2D graph, the Main Core runs the 3D model
    optimize_and_render_wing()

    # 3. Tells the program not to shut down until you manually close the 2D graph
    graph_process.join()