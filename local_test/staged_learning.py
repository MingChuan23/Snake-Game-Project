from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from gym_env import SnakeGameEnv
import json
import os

model_name = "ppo_snake4.2"
log_dir = "logs"
config_dir = f"param_configs/{model_name}"

param_list = []

for filename in os.listdir(config_dir):
    with open(os.path.join(config_dir, filename), "r") as f:
        param_list.append(json.load(f))

model = None
for i, params in enumerate(param_list):
    vec_env = make_vec_env(lambda: SnakeGameEnv(**params), n_envs=32)

    if not model:
        model = PPO('CnnPolicy', vec_env, verbose=True, device='cuda', tensorboard_log=log_dir, n_steps=128, batch_size=2048, learning_rate=0.0003)

    num_repeats = 5 if i < len(param_list) - 1 else 10
    for j in range(num_repeats):
        model.learn(50000, progress_bar=True, tb_log_name=f"{model_name}_{i}b", reset_num_timesteps=False)
        model.save(f'{model_name}_{i}b.zip')