from SoccerGameEnv import SoccerGameEnv
from arguments import get_variable_args
import time
from stable_baselines3 import A2C, PPO
from stable_baselines3.common.env_checker import check_env

if __name__ == '__main__':
    args = get_variable_args()

    env = SoccerGameEnv(args)
    # check_env(env)
    # t1 = time.time()
    # model = A2C("MultiInputPolicy", env, verbose=1).learn(total_timesteps=500)
    model = PPO("MultiInputPolicy", env, verbose=1)
    model.learn(args.total_timestep)
    model.save("ppo_rsge")

    # print("GUI: {}".format(time.time() - t1))
    env.close()
