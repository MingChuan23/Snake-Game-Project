import numpy as np
import gymnasium as gym
from snake_game import Env, SnakeState, INIT_TAIL_SIZE
import cv2
import itertools


MAX_STEPS = 50
INIT_HP = 20

reward_map = {
    SnakeState.OK: -1,
    SnakeState.ATE: 5,
    SnakeState.DED: -1000,
    SnakeState.WON: 1
}

class SnakeGameEnv(gym.Env):
    def __init__(self, gs=10, num_fruits=10, num_snakes=1, num_teams=1, render_mode='human'):
        super(SnakeGameEnv, self).__init__()
        self.env = Env(gs, num_fruits, num_snakes, num_teams, init_hp=INIT_HP)
        self.action_map = {
            0: 'stay',
            1: 'left',
            2: 'right'
        }
        self.num_snakes = num_snakes
        self.numteams = num_teams
        self.scale = 64
        self.render_mode = render_mode

        self.action_space = gym.spaces.Discrete(len(self.action_map.keys()))

        n = 5 * self.num_snakes  # 4 features per snake, add more if needed
        self.observation_space = gym.spaces.Dict(
            {
                'image': gym.spaces.Box(
                    low=0, high=255, shape=(self.env.gs*self.scale, self.env.gs*self.scale, 3),
                    dtype=np.uint8),
                'vector': gym.spaces.Box(
                    low=0, high=255, shape=(n,),
                    dtype=np.int16)
            }
        ) 

    def _get_obs(self):
        snakes = [(snake.hp, snake.direction.to_int(), snake.colour.value, snake.head.x, snake.head.y) for snake in self.env.snakes]
        snakes = list(itertools.chain(*snakes)) + [0, 0, 0] * (self.num_snakes - len(snakes))
        return {
            'image': cv2.resize(self.env.to_image(), (640, 640), interpolation=cv2.INTER_NEAREST),
            'vector': snakes
        }

    def _get_info(self):
        return {}
        
    def reset(self, *, seed = None):
        super().reset(seed=seed)

        self.env.reset()
        return self._get_obs(), self._get_info()
    
    def step(self, action):
        actions = [action]
        if self.num_snakes > 1:  #TODO: Add fixed agent move selection, currently random
            for i in range(1, self.num_snakes):
                actions.append(self.action_space.sample())

        snake_condition, hp, tail_size = self.env.update([self.action_map[a] for a in actions])

        reward = reward_map[snake_condition]  / 100

        is_terminal = snake_condition in [SnakeState.DED, SnakeState.WON] #or self.env.time_steps > MAX_STEPS
        truncated = self.env.time_steps > MAX_STEPS

        return self._get_obs(), reward, is_terminal, truncated, self._get_info()
    
    def render(self):
        im = self.env.to_image(gradation=True)
        if self.render_mode == 'human':
            cv2.imshow('Snake Game', cv2.resize(im, (640, 640), interpolation=cv2.INTER_NEAREST))
            cv2.waitKey(500)
        elif self.render_mode == 'rgb_array':
            return cv2.resize(im, (640, 640), interpolation=cv2.INTER_NEAREST)
        elif self.render_mode == 'ansi':
            print(self.env.to_string())

    def close(self):
        cv2.destroyAllWindows()

