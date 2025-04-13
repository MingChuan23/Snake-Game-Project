import json
import pygad
from tqdm import tqdm
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3 import PPO
from gym_env import SnakeGameEnv
from feature_extractor import CustomCNN

config_dir = "param_configs"
with open(f"{config_dir}/4.7_single.json", "r") as f:
    game_params = json.load(f)


policy_kwargs = dict(
    features_extractor_class=CustomCNN,
    features_extractor_kwargs=dict(features_dim=256),
)

def fitness_func(ga_instance, solution, solution_idx):
    rewards = {
        "SnakeState.OK": solution[0],
        "SnakeState.ATE": solution[1], 
        "SnakeState.DED": solution[2],   
    }

    game_params['rewards'] = rewards
    game_params['use_dist'] = solution[3] 
    # Create the environment with the current reward parameters
    vec_env = make_vec_env(lambda: SnakeGameEnv(**game_params), n_envs=32)

    # Train PPO on the environment for a few timesteps to evaluate performance
    model = PPO('CnnPolicy', vec_env, policy_kwargs=policy_kwargs,verbose=True, device='cuda', n_steps=128, batch_size=2048, learning_rate=0.0003)
    model.learn(total_timesteps=500000, progress_bar=True)  # Adjust timesteps as needed

    # After training, evaluate the model (mean reward in a set of episodes)
    env = Monitor(SnakeGameEnv(**game_params))
    mean_reward, std = evaluate_policy(model, env, n_eval_episodes=30, render=False, return_episode_rewards=False, warn=False, deterministic=False)
    
    # The fitness is the mean reward; higher mean reward is better
    return mean_reward

num_generations = 20
with tqdm(total=num_generations) as pbar:
    ga_instance = pygad.GA(
        num_generations=20,       # Number of generations
        sol_per_pop=10,           # Number of solutions in the population
        num_parents_mating=5,     # Number of parents to mate
        fitness_func=fitness_func,
        num_genes=4,
        gene_space=[              # Define the reward weight parameters (values can vary)
            {'low': -3, 'high': -1},  # Range for OK reward
            {'low': 10, 'high': 100},  # Range for ATE reward
            {'low': -100, 'high': -10},   # Range for DED reward
            {'low': 20, 'high': 40},   # Range for distance reward

        ],
        crossover_type="uniform",  # Crossover method
        mutation_type="random",    # Mutation method
        mutation_percent_genes=10, # Mutation rate
    )

    ga_instance.run()

solution, solution_fitness, solution_idx  = ga_instance.best_solution()
print("Best solution: ", solution)
print("Fitness: ", solution_fitness)

with open("best_solution.txt", "w") as f:
    f.write(f"{solution}")