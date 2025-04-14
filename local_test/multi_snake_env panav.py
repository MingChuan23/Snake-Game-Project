import numpy as np
import gymnasium as gym
import cv2
from snake_game import Env, SnakeState
from pettingzoo.utils.env import ParallelEnv


def parse_enum(enum, str_dict: dict):
    return {enum[key.split('.')[-1]]: value for key, value in str_dict.items()}


class SnakeMultiEnv(ParallelEnv):
    def __init__(
        self,
        max_steps=1000,
        init_hp=100,
        init_tail_size=4,
        num_fruits=1,
        gs=10,
        perspective='third',
        num_snakes=2,
        num_teams=1,
        render_mode='human',
        rewards=None
    ):
        super().__init__()
        self.env = Env(grid_size=gs, num_fruits=num_fruits, num_snakes=2,
                       num_teams=2, init_hp=init_hp, init_tail_size=init_tail_size,
                       perspective=perspective)

        self.perspective = perspective
        if self.perspective == 'third':
            self.action_map = {
                0: 'up',
                1: 'down',
                2: 'left',
                3: 'right'
            }
        else:
            self.action_map = {
                0: 'stay',
                1: 'left',
                2: 'right'
            }

        self.num_snakes = num_snakes
        self.agents = [f"snake_{i}" for i in range(self.num_snakes)]
        self.possible_agents = self.agents[:]

        self.reward_map = parse_enum(SnakeState, rewards or {
            "SnakeState.OK": -0.4,
            "SnakeState.ATE": 20,
            "SnakeState.DED": -40,
            "SnakeState.WON": 1
        })

        self.max_steps = max_steps
        self.scale = 4
        self.render_mode = render_mode
        self.gs = gs
        self.t = 0

        self.action_spaces = {
            agent: gym.spaces.Discrete(len(self.action_map)) for agent in self.agents
        }

        self.observation_spaces = {
            agent: gym.spaces.Box(
                low=0,
                high=255,
                shape=(self.gs * self.scale, self.gs * self.scale, 3),
                dtype=np.uint8
            ) for agent in self.agents
        }

    def _get_obs(self):
        return cv2.resize(
            self.env.to_image(),
            (self.gs * self.scale, self.gs * self.scale),
            interpolation=cv2.INTER_NEAREST
        )

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        self.env.reset()
        self.agents = self.possible_agents[:]
        self.t = 0

        obs = {agent: self._get_obs() for agent in self.agents}
        infos = {agent: {} for agent in self.agents}
        return obs, infos

    def step(self, actions):
        if not self.agents:
            return {}, {}, {}, {}, {}

        self.t += 1

        action_list = [self.action_map[actions[agent]] for agent in self.agents]
        snake_conditions, _, _ = self.env.update(action_list)

        obs = {agent: self._get_obs() for agent in self.agents}
        rewards = {
            agent: self.reward_map.get(cond, 0) / 100
            for agent, cond in zip(self.agents, snake_conditions)
        }
        terminations = {
            agent: cond in [SnakeState.DED, SnakeState.WON]
            for agent, cond in zip(self.agents, snake_conditions)
        }
        truncations = {agent: self.t > self.max_steps for agent in self.agents}
        infos = {agent: {} for agent in self.agents}

        # Remove dead agents
        self.agents = [agent for agent in self.agents if not terminations[agent]]

        return obs, rewards, terminations, truncations, infos

    def render(self):
        im = self.env.to_image(gradation=True)
        if self.render_mode == 'human':
            cv2.imshow('Snake Game', cv2.resize(im, (640, 640), interpolation=cv2.INTER_NEAREST))
            cv2.waitKey(1)
        elif self.render_mode == 'rgb_array':
            return cv2.resize(im, (640, 640), interpolation=cv2.INTER_NEAREST)
        elif self.render_mode == 'ansi':
            print(self.env.to_string())

    def close(self):
        cv2.destroyAllWindows()
