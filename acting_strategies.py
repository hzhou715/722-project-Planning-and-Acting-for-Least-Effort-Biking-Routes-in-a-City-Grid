# acting_strategies.py
# Execute a plan from sas_plan using SimpleGridWrapper
# Supports Run-Lookahead and Run-Lazy-Lookahead strategies

from simple_grid_wrapper import SimpleGridWrapper
import time
import sys

def load_plan(path="sas_plan"):
    actions = []
    with open(path, "r") as f:
        for line in f:
            if line.startswith(";") or not line.strip():
                continue
            tokens = line.strip("()\n").split()
            if tokens[0] == "move":
                from_cell, to_cell = tokens[1], tokens[2]
                actions.append((from_cell, to_cell))
    return actions

def cell_name_to_coord(name):
    x, y = int(name[1:3]), int(name[3:5])
    return (x, y)

def simulate_step(env, to_cell):
    next_pos = cell_name_to_coord(to_cell)
    env.agent_pos = next_pos
    cost = env.terrain[next_pos]
    print(f" → moved to {next_pos}, cost {cost}")
    env.render()
    time.sleep(0.3)
    return cost

def run_lazy_lookahead(env, plan):
    print("Running Run-Lazy-Lookahead")
    total_cost = 0
    steps = 0
    for _, to_cell in plan:
        cost = simulate_step(env, to_cell)
        total_cost += cost
        steps += 1
    print(f"Total steps: {steps}, Total cost: {total_cost}")

def run_lookahead(env, plan):
    print("Running Run-Lookahead")
    total_cost = 0
    steps = 0
    for _, to_cell in plan:
        print("→ Checking next action (lookahead)...")
        cost = simulate_step(env, to_cell)
        total_cost += cost
        steps += 1
    print(f"Total steps: {steps}, Total cost: {total_cost}")

def report_environment(env):
    print("=" * 40)
    print("📋 Environment Report")
    print(f"Grid size: {env.size}x{env.size}")
    print(f"Agent start position: {env.agent_pos}")
    print(f"Goal position: {env.goal_pos}")
    print("Terrain cost matrix (8x8):")
    print(env.terrain[:8, :8])
    print("=" * 40 + "\n")

if __name__ == "__main__":
    strategy = sys.argv[1] if len(sys.argv) > 1 else "lazy"
    #env = SimpleGridWrapper(seed=42)
    env = SimpleGridWrapper(seed=42, start=(0, 0), goal=(7, 7))

    plan = load_plan("sas_plan")

    print("Initial position:", env.agent_pos)
    report_environment(env)
    env.render()
    time.sleep(1)

    if strategy == "lookahead":
        run_lookahead(env, plan)
    else:
        run_lazy_lookahead(env, plan)
