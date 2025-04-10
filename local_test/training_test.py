from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from gym_env import SnakeGameEnv
from feature_extractor import CustomCNN
import json


log_dir = "logs"
config_dir = "param_configs"

with open(f"{config_dir}/ppo_snake4.1/c.json", "r") as f:
    game_params = json.load(f)


policy_kwargs = dict(
    features_extractor_class=CustomCNN,
    features_extractor_kwargs=dict(features_dim=256)
)

vec_env = make_vec_env(lambda: SnakeGameEnv(**game_params), n_envs=32)
# env = SnakeGameEnv(num_snakes=1, num_teams=1)



# model = PPO('MultiInputPolicy', vec_env, verbose=True, device='cuda', tensorboard_log=log_dir, n_steps=128, batch_size=2048, learning_rate=0.0003)
model = PPO('CnnPolicy', vec_env, policy_kwargs=policy_kwargs, verbose=True, device='cuda', tensorboard_log=log_dir, n_steps=128, batch_size=2048, learning_rate=0.0003)
# model = PPO.load("ppo_snake3.4.zip", env=vec_env, device="cuda", tensorboard_log=log_dir, n_steps=128, batch_size=2048, learning_rate=0.0003)


for i in range(20):
    model.learn(100000, progress_bar=True, tb_log_name="ppo_snake4.1_single", reset_num_timesteps=False)
    model.save('ppo_snake4.1_single.zip')

