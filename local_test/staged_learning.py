from stable_baselines3 import PPO, A2C
from stable_baselines3.common.env_util import make_vec_env
from gym_env import SnakeGameEnv
from feature_extractor import CustomCNN
import json
import os

model_name = "ppo_snake4.8d_staged"
log_dir = "logs"
config_dir = f"param_configs/{model_name}"

param_list = []

for filename in sorted(os.listdir(config_dir)):
    with open(os.path.join(config_dir, filename), "r") as f:
        param_list.append(json.load(f))

policy_kwargs = dict(
    features_extractor_class=CustomCNN,
    features_extractor_kwargs=dict(features_dim=256),
    # net_arch=dict(pi=[128, 64], vf=[256, 256, 128])
)

model = None
for i, params in enumerate(param_list):
    vec_env = make_vec_env(lambda: SnakeGameEnv(**params), n_envs=32)
    # model.set_env(vec_env)

    if not model:
        model = PPO('CnnPolicy', vec_env, policy_kwargs=policy_kwargs, verbose=True, device='cuda', tensorboard_log=log_dir, n_steps=128, batch_size=2048, learning_rate=0.00025)
        # model = A2C('CnnPolicy', vec_env, policy_kwargs=policy_kwargs, verbose=True, device='cuda', tensorboard_log=log_dir, n_steps=128, learning_rate=0.0003)

    num_repeats = 40
    for j in range(num_repeats):
        model.learn(200000, progress_bar=True, tb_log_name=f"{model_name}_small_arch_long_{i}", reset_num_timesteps=False)
        model.save(f'{model_name}_small_arch_long_{i}.zip')