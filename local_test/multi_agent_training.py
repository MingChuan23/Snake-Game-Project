from multi_snake_env import SnakeMultiEnv


env = SnakeMultiEnv(
    num_snakes=2,
    num_teams=2,
    max_steps=1000,
    init_hp=100,
    init_tail_size=4,
    num_fruits=1,
    gs=10,
    perspective='third',
    render_mode='human',
    rewards={
        "SnakeState.OK": -1.43,
        "SnakeState.ATE": 37.37,
        "SnakeState.DED": -68.2,
        "SnakeState.WON": 100
    }
)
