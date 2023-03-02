import os
import time
import sys
import threading
from queue import Queue
from CoppeliaSim import sim


def robot_start(index):
    os.system('/home/xander/Documents/RobotSoccerGameEnv/venv/bin/python '
              '/home/xander/Documents/RobotSoccerGameEnv/multirobots_individual/EP_' + str(index) + '.py')


if __name__ == '__main__':
    sim.simxFinish(-1)
    while True:
        clientID = sim.simxStart("127.0.0.1", 19991, True, True, 5000, 5)  # 建立和服务器的连接
        if clientID != -1:  # 连接成功
            print('Scene connect successfully')
            break
        else:
            time.sleep(0.2)

    # https://blog.csdn.net/weixin_41754912/article/details/82353012
    # 设置仿真步长，为了保持API端与V-rep端相同步长
    tstep = 0.005  # 定义仿真步长
    sim.simxSetFloatingParameter(clientID, sim.sim_floatparam_simulation_time_step, tstep, sim.simx_opmode_oneshot)
    # 然后打开同步模式
    sim.simxSynchronous(clientID, True)
    sim.simxStartSimulation(clientID, sim.simx_opmode_oneshot)

    # # Restart simulation
    # stop = sim.simxStopSimulation(clientID, sim.simx_opmode_blocking)
    # time.sleep(4)  # 需要反应时间
    # start = sim.simxStartSimulation(clientID, sim.simx_opmode_blocking)

    for i in range(4):
        robot = threading.Thread(target=robot_start, args=(i, ))
        print("num: ", i)
        robot.setDaemon(True)
        robot.start()