from SoccerGameEnv import SoccerGameEnv
import time
from stable_baselines3 import A2C
from stable_baselines3.common.env_checker import check_env

if __name__ == '__main__':
    env = SoccerGameEnv()
    # check_env(env)
    t1 = time.time()
    model = A2C("MultiInputPolicy", env, verbose=1).learn(total_timesteps=500)
    # print("GUI: {}".format(time.time() - t1))
    env.close()
