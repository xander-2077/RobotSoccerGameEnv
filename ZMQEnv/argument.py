import argparse


def get_variable_args():
    parser = argparse.ArgumentParser()
    # the environment setting
    # parser.add_argument('--gui', default=True, action='store_false')
    parser.add_argument('--gui', default=False, action='store_true')
    parser.add_argument('--random_initial_state', default=True, action='store_true')
    parser.add_argument('--max_episode_step', type=int, default=100, help="max length of one episode")
    parser.add_argument('--total_timestep', type=int, default=1e6)
    parser.add_argument('--decide_freq', type=int, default=2)
    parser.add_argument('--load_trained_model', default=False, action='store_true')
    parser.add_argument('--alg', type=str, default='ppo')
    parser.add_argument('--cuda', default=False, action='store_true')
    parser.add_argument('--save_dir', type=str, default='../trained_model')

    args = parser.parse_args()
    return args
