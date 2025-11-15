# simple_grid_wrapper.py
# Wraps the SimpleGrid-v0 environment and extracts agent, goal, terrain, and wall info

import gymnasium as gym
import numpy as np
import gym_simplegrid  # Ensure it's installed with: pip install gym-simplegrid
'''
class SimpleGridWrapper:
    def __init__(self, seed=42):
        self.seed = seed
        self.size = 8  # Fixed for "8x8" map
        self.env = gym.make("SimpleGrid-v0", obstacle_map="8x8")
        self.obs, _ = self.env.reset(seed=seed, options={})      
        self.blocked = self._get_walls()      
        self.agent_pos = tuple(self.env.unwrapped.agent_xy)
        self.goal_pos = tuple(self.env.unwrapped.goal_xy)
        self.terrain = self._generate_terrain()
        self.walls = self._get_walls()  # Changed from 'blocked' to 'walls' for consistency
        #self.blocked[4, 3] = True  # e.g. block cell used in step 3
'''
class SimpleGridWrapper:
    def __init__(self, seed=42, start=(0, 0), goal=(7, 7)):
        self.seed = seed
        self.env = gym.make("SimpleGrid-v0", obstacle_map="8x8")
        self.size = 8  # fixed map
        self.obs, _ = self.env.reset(seed=seed, options={
            "start_loc": start,
            "goal_loc": goal
        })

        self.agent_pos = tuple(self.env.unwrapped.agent_xy)
        self.goal_pos = tuple(self.env.unwrapped.goal_xy)

        self.terrain = self._generate_terrain()
        self.walls = self._get_walls()  # optional

    def _generate_terrain(self):
        """Generate random terrain costs for each cell"""
        rng = np.random.default_rng(self.seed)
        # Generate terrain costs between 1 and 5 for each cell
        terrain = rng.integers(1, 6, size=(self.size, self.size))
        return terrain

    def _get_walls(self):
        """Extract wall positions from the environment"""
        walls = np.zeros((self.size, self.size), dtype=bool)
        
        # Access the obstacle map from the environment
        # SimpleGrid uses different attributes depending on the version
        if hasattr(self.env.unwrapped, 'obstacle_map'):
            # Get obstacles from the environment's obstacle map
            obstacle_map = self.env.unwrapped.obstacle_map
            for i in range(self.size):
                for j in range(self.size):
                    # Check if position (i,j) is an obstacle
                    if obstacle_map is not None and obstacle_map[i, j]:
                        walls[i, j] = True
        elif hasattr(self.env.unwrapped, 'grid'):
            # Alternative: check grid directly if available
            grid = self.env.unwrapped.grid
            for i in range(self.size):
                for j in range(self.size):
                    # Wall cells typically have a specific value
                    if grid[i, j] == 1:  # Assuming 1 represents walls
                        walls[i, j] = True
        
        return walls

    def get_state(self):
        """Return the current state as a dictionary"""
        return {
            "agent": self.agent_pos,
            "goal": self.goal_pos,
            "terrain": self.terrain,
            "walls": self.walls,
            "size": self.size
        }

    def step(self, action):
        """Execute an action in the environment"""
        obs, reward, terminated, truncated, info = self.env.step(action)
        # Update agent position after step
        self.agent_pos = tuple(self.env.unwrapped.agent_xy)
        return obs, reward, terminated, truncated, info

    def reset(self, seed=None):
        """Reset the environment"""
        if seed is not None:
            self.seed = seed
        self.obs, info = self.env.reset(seed=self.seed, options={})
        self.agent_pos = tuple(self.env.unwrapped.agent_xy)
        self.goal_pos = tuple(self.env.unwrapped.goal_xy)
        self.terrain = self._generate_terrain()
        self.walls = self._get_walls()
        return self.obs, info

    def render(self):
        """Render the environment"""
        return self.env.render()

    def close(self):
        """Close the environment"""
        self.env.close()


if __name__ == "__main__":
    # Test the wrapper
    wrapper = SimpleGridWrapper(seed=42)
    state = wrapper.get_state()
    print(f"Agent position: {state['agent']}")
    print(f"Goal position: {state['goal']}")
    print(f"Grid size: {state['size']}")
    print(f"Terrain shape: {state['terrain'].shape}")
    print(f"Walls shape: {state['walls'].shape}")
    print("\nTerrain costs (sample 8x8):")
    print(state['terrain'][:8, :8])