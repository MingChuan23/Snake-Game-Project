from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from gym_env import SnakeGameEnv
from feature_extractor import CustomCNN
import json
import os


log_dir = "logs"
config_dir = "param_configs/ga_params"

param_list = []

# for filename in sorted(os.listdir(f"{config_dir}")):
#     with open(os.path.join(config_dir, filename), "r") as f:
#         param_list.append(json.load(f))

with open(f"{config_dir}/d.json", "r") as f:
    game_params = json.load(f)

policy_kwargs = dict(
    features_extractor_class=CustomCNN,
    features_extractor_kwargs=dict(features_dim=256),
    net_arch=dict(pi=[128, 64], vf=[256, 256, 128])
)

# env = SnakeGameEnv(num_snakes=1, num_teams=1)
# model = PPO('MultiInputPolicy', vec_env, verbose=True, device='cuda', tensorboard_log=log_dir, n_steps=128, batch_size=2048, learning_rate=0.0003)
# model = PPO.load("ppo_snake4.5_2.zip", env=vec_env, device="cuda", tensorboard_log=log_dir, n_steps=128, batch_size=2048, learning_rate=0.0003)
# print(model.get_parameters()['policy'].keys())
# for index, config in enumerate(param_list):
vec_env = make_vec_env(lambda: SnakeGameEnv(**game_params), n_envs=32)
model = PPO('CnnPolicy', vec_env, policy_kwargs=policy_kwargs,verbose=False, device='cuda', tensorboard_log=log_dir, n_steps=128, batch_size=2048, learning_rate=0.0003)

for i in range(40):
    model.learn(100000, progress_bar=True, tb_log_name=f"ppo_snake4.8_d", reset_num_timesteps=False)
    model.save(f'ppo_snake4.8_d.zip')