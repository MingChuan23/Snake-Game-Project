import numpy as np
import gymnasium as gym
from snake_game import Env, SnakeState
import cv2
import itertools

# Epsiode length
# MAX_STEPS = 1000

# # Initial game settings
# INIT_HP = 100
# INIT_TAIL_SIZE = 4
# MAX_FRUITS = 1
# PERSPECTIVE = 'third'

# # Rewards
# reward_map = {
#     SnakeState.OK: -0.4,
#     SnakeState.ATE: 20,
#     SnakeState.DED: -40,
#     SnakeState.WON: 1
# }


# Allows rewards to be converted from the json strings to enum values
def parse_enum(enum, str_dict:dict):
    return {enum[key.split('.')[-1]]: value for key, value in str_dict.items()}

class SnakeGameEnv(gym.Env):
    def __init__(self, max_steps=1000, init_hp=100, init_tail_size=4, num_fruits=1, gs=10, perspective='third', num_snakes=1, num_teams=1, render_mode='human', rewards={}):
        super(SnakeGameEnv, self).__init__()
        self.env = Env(gs=gs, num_fruits=num_fruits, num_snakes=num_snakes, num_teams=num_teams, init_hp=init_hp, init_tail_size=init_tail_size, perspective=perspective)
        
        if perspective == 'third':
            self.action_map = {
                0: 'up',
                1: 'down',
                2: 'left',
                3: 'right'
            }
        elif perspective == 'first':
            self.action_map = {
                0: 'stay',
                1: 'left',
                2: 'right'
            }

        self.reward_map = parse_enum(SnakeState, rewards)
        self.max_steps = max_steps
        self.num_snakes = num_snakes
        self.numteams = num_teams
        self.scale = 4
        self.render_mode = render_mode
        self.gs = gs

        self.action_space = gym.spaces.Discrete(len(self.action_map.keys()))

        # FOR MULTIINPUT
        # n = 5 * self.num_snakes  # 5 features per snake, add more if needed
        # self.observation_space = gym.spaces.Dict(
        #     {
        #         'image': gym.spaces.Box(
        #             low=0, high=255, shape=(self.gs*self.scale, self.gs*self.scale, 3),
        #             dtype=np.uint8),
        #         'vector': gym.spaces.Box(
        #             low=0, high=100, shape=(n,),
        #             dtype=np.int16)
        #     }
        # ) 

        # FOR CNN
        self.observation_space = gym.spaces.Box(
                    low=0, high=255, shape=(self.gs*self.scale, self.gs*self.scale, 3),
                    dtype=np.uint8)

    def _get_obs(self):
        # FOR MULTIINPUT

        # snakes = [(snake.hp, snake.direction.to_int(), snake.colour.value, snake.head.x, snake.head.y) for snake in self.env.snakes]
        # snakes = list(itertools.chain(*snakes)) + [0, 0, 0] * (self.num_snakes - len(snakes))
        # return {
        #     'image': cv2.resize(self.env.to_image(), (self.gs*self.scale, self.gs*self.scale), interpolation=cv2.INTER_NEAREST),
        #     # 'image': np.expand_dims(self.env.to_image().astype('float32'), -1),
        #     'vector': snakes
        # }

        # FOR CNN
        return cv2.resize(self.env.to_image(), (self.gs*self.scale, self.gs*self.scale), interpolation=cv2.INTER_NEAREST)

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

        is_terminal = snake_condition in [SnakeState.DED, SnakeState.WON] 
        truncated = self.env.time_steps > self.max_steps

        return self._get_obs(), reward, is_terminal, truncated, self._get_info()
    
    def render(self):
        im = self.env.to_image(gradation=True)
        if self.render_mode == 'human':
            cv2.imshow('Snake Game', cv2.resize(im, (640, 640), interpolation=cv2.INTER_NEAREST))
            # print(self._get_obs()['vector'])
            cv2.waitKey(0)
        elif self.render_mode == 'rgb_array':
            return cv2.resize(im, (640, 640), interpolation=cv2.INTER_NEAREST)
        elif self.render_mode == 'ansi':
            print(self.env.to_string())

    def close(self):
        cv2.destroyAllWindows()

