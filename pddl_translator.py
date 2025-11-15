# pddl_translator.py
# Converts SimpleGridWrapper output to a PDDL problem file with action costs

from simple_grid_wrapper import SimpleGridWrapper
import os

def pos_to_cellname(r, c):
    """Convert position (row, col) to cell name"""
    return f"c{r:02d}{c:02d}"

def generate_problem_file(state, domain_name="grid-costs", problem_name="grid5",
                          output_path="grid5_problem.pddl"):
    """Generate a PDDL problem file from the grid state"""
    
    # Extract state information
    size = state["terrain"].shape[0]
    agent = pos_to_cellname(*state["agent"])
    goal = pos_to_cellname(*state["goal"])
    terrain = state["terrain"]
    walls = state["walls"]

    with open(output_path, "w") as f:
        # Problem definition
        f.write(f"(define (problem {problem_name})\n")
        f.write(f"  (:domain {domain_name})\n")
        
        # Objects (cells)
        f.write("  (:objects\n")
        for r in range(size):
            for c in range(size):
                f.write(f"    {pos_to_cellname(r,c)} - cell\n")
        f.write("  )\n\n")

        # Initial state
        f.write("  (:init\n")
        f.write(f"    (at {agent})\n")
        
        # Set move costs and adjacencies for each cell
        for r in range(size):
            for c in range(size):
                name = pos_to_cellname(r, c)
                # Only set move cost if the cell is not a wall
                if not walls[r, c]:
                    f.write(f"    (= (move-cost {name}) {terrain[r,c]})\n")
                else:
                    # Walls have infinite cost (or we can skip them)
                    f.write(f"    (= (move-cost {name}) 9999)\n")  # High cost for walls
                
                # Define adjacencies (only between non-wall cells)
                for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < size and 0 <= nc < size:
                        # Only add adjacency if neither cell is a wall
                        if not walls[r, c] and not walls[nr, nc]:
                            neighbor = pos_to_cellname(nr, nc)
                            f.write(f"    (adj {name} {neighbor})\n")
        
        # Set total cost to 0 initially (if using metric)
        f.write("    (= (total-cost) 0)\n")
        f.write("  )\n\n")
        
        # Goal
        f.write(f"  (:goal (at {goal}))\n")
        
        # Metric (minimize total cost)
        f.write("  (:metric minimize (total-cost))\n")
        f.write(")\n")
    
    print(f"✅ PDDL problem written to {output_path}")
    return output_path

def parse_plan(plan_file):
    """Parse a plan file and extract the sequence of moves"""
    if not os.path.exists(plan_file):
        print(f"❌ Plan file {plan_file} not found")
        return []
    
    moves = []
    with open(plan_file, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if line.startswith(';') or not line:
                continue
            # Parse move actions (format: (move from to))
            if line.startswith('(move'):
                parts = line.replace('(', '').replace(')', '').split()
                if len(parts) == 3:
                    _, from_cell, to_cell = parts
                    moves.append((from_cell, to_cell))
    
    return moves

def cellname_to_pos(cellname):
    """Convert cell name back to position (row, col)"""
    # Assuming format cRRCC where RR is row and CC is column
    if cellname.startswith('c') and len(cellname) == 5:
        row = int(cellname[1:3])
        col = int(cellname[3:5])
        return (row, col)
    else:
        raise ValueError(f"Invalid cell name format: {cellname}")


if __name__ == "__main__":
    # Create environment and get state
    #env = SimpleGridWrapper(seed=42)
    env = SimpleGridWrapper(seed=42, start=(0, 0), goal=(7, 7))

    state = env.get_state()
    
    # Generate PDDL problem file
    problem_file = generate_problem_file(state, output_path="grid_problem.pddl")
    
    print(f"\nGrid Information:")
    print(f"  Agent starts at: {state['agent']}")
    print(f"  Goal is at: {state['goal']}")
    print(f"  Grid size: {state['size']}x{state['size']}")
    
    # Show a sample of terrain costs
    print(f"\nSample terrain costs (top-left 4x4):")
    for r in range(min(4, state['size'])):
        row_str = ""
        for c in range(min(4, state['size'])):
            if state['walls'][r, c]:
                row_str += " W "
            else:
                row_str += f" {state['terrain'][r, c]} "
        print(row_str)