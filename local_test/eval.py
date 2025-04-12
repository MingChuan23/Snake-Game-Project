from stable_baselines3.common.evaluation import evaluate_policy
from gym_env import SnakeGameEnv
from stable_baselines3 import PPO
import torch
import json
from stable_baselines3.common.monitor import Monitor
from feature_extractor import CustomCNN

# action_map = {
#     0: 'stay',
#     1: 'left',
#     2: 'right'
# }

action_map = {
            0: 'up',
            1: 'down',
            2: 'left',
            3: 'right'
        }

with open("param_configs/eval.json", "r") as f:
    game_params = json.load(f)

# Load the trained model
model = PPO.load("models/ppo_snake4.3e_1.zip")

# Create a new environment instance for evaluation
env = Monitor(SnakeGameEnv(**game_params))

# Evaluate the model
# rew, std = evaluate_policy(model, env, n_eval_episodes=50, render=False, return_episode_rewards=False, warn=True, deterministic=False)


# For getting the explicit actions probabilities, could be good for data and reporting
num_episodes = 5
all_action_probs = []

for _ in range(num_episodes):
    obs, _ = env.reset()
    done = False

    while not done:
        with torch.no_grad():
            tensor_obs, _ = model.policy.obs_to_tensor(obs)
            action_dist = model.policy.get_distribution(tensor_obs)
            action_probs = torch.exp(action_dist.distribution.logits)[0].tolist()
            all_action_probs.append(action_probs)

        paired_probs = [(action_map[i], round(prob, ndigits=3)) for i, prob in enumerate(action_probs)]
        print(f"Action Dist: {paired_probs}")
        env.render()
        action, _ = model.predict(obs, deterministic=False)
        print(f"Action: {action_map[int(action)]}")
        obs, reward, done,_, info = env.step(int(action))
        if done:
            print(info)
            input("Press Enter to continue...")



# print(f"Mean Reward: {rew:.2f}, Std Reward: {std:.2f}")