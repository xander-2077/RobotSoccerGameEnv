import sys
sys.path.append("../..")
from GymEnv.SoccerGameEnv import SoccerGameEnv
from GymEnv.arguments import get_variable_args

if __name__ == '__main__':
    args = get_variable_args()
    env = SoccerGameEnv(args)

