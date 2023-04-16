from Env import SoccerGameEnv
from argument import get_variable_args
import time


if __name__ == '__main__':
    args = get_variable_args()

    env = SoccerGameEnv(args)

    # env.step([0.1, 0.2, 0.5])
    # env._get_info()
    # env.robot.get_pos()
    # env.robot.chassis.drive_speed(z=-60)
    # while True:
    #     env.robot.get_ori('ang')
    #     time.sleep(0.5)

    env.close()
