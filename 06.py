import time
import threading
from CoppeliaSim import sim
import sys
from multi_robomaster import multi_robot
import logging
logging.basicConfig(level=logging.INFO)
logging.info()


def Init_sim(port):
    sim.simxFinish(-1)
    clientID = sim.simxStart("127.0.0.1", port, True, True, 5000, 5)
    if clientID != -1:
        print("Connection successful!")
    else:
        print("Connection not successful!")
        sys.exit("Could not connect")
    return clientID


def main():
    clientID = Init_sim(19991)

    # Init Config
    robots_sn_list = ['3JKDH2T00159G8', '3JKCJC400302GS', '3JKCJC400301ZP', '3JKCJC400301UD']
    multi_robots = multi_robot.MultiEP()
    multi_robots.initialize()
    # Modified
    number = multi_robots.number_id_by_sn(robots_sn_list, [1, robots_sn_list[0]], [2, robots_sn_list[1]],
                                          [3, robots_sn_list[2]], [4, robots_sn_list[3]])
    print("The number of robot is: {0}".format(number))
    ep_robot = []
    for i in range(4):
        ep_robot[i] = multi_robots.build_group([i+1])

    # Init info receive
    robot_handle = []
    for i in range(4):
        _, robot_handle[i] = sim.simxGetObjectHandle(clientID, "/EP_"+str(i), sim.simx_opmode_oneshot_wait)
        if _ != sim.simx_return_ok:
            raise Exception("handle error")
    _, ball_handle = sim.simxGetObjectHandle(clientID, "/ball", sim.simx_opmode_oneshot_wait)
    if _ != sim.simx_return_ok:
        raise Exception("handle error")

    robot_pos = []
    robot_ang = []
    for i in range(4):
        _, robot_pos[i] = sim.simxGetObjectPosition(clientID, "/EP_"+str(i), -1, sim.simx_opmode_streaming)
        _, robot_ang[i] = sim.simxGetObjectOrientation(clientID, "/EP_"+str(i), -1, sim.simx_opmode_streaming)


























if __name__ == '__main__':
    main()
