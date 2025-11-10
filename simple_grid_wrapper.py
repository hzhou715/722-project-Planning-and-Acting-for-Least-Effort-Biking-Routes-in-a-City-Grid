# simple_grid_wrapper.py
import gymnasium as gym
import numpy as np
import gym_simplegrid  # requires: pip install -e .

class SimpleGridWrapper:
    def __init__(self, size=5, seed=42):
        self.env = gym.make("SimpleGrid-v0", size=size)
        self.obs, _ = self.env.reset(seed=seed)
        self.size = size
        self.agent_pos = tuple(self.env.agent_pos)
        self.goal_pos = tuple(self.env.goal_pos)
        self.seed = seed
        self.terrain = self._generate_terrain()
        self.blocked = self._get_walls()

    def _generate_terrain(self):
        rng = np.random.default_rng(self.seed)
        return rng.integers(1, 10, size=(self.size, self.size))

    def _get_walls(self):
        walls = np.zeros((self.size, self.size), dtype=bool)
        for r in range(self.size):
            for c in range(self.size):
                tile = self.env.grid.get(c, r)
                if tile and getattr(tile, 'type', None) == "wall":
                    walls[r, c] = True
        return walls

    def get_state(self):
        return {
            "agent": self.agent_pos,
            "goal": self.goal_pos,
            "terrain": self.terrain,
            "walls": self.blocked
        }

    def render(self):
        self.env.render()
