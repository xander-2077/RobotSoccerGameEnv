import os
import time
import sys
import threading
from queue import Queue
import logging
from CoppeliaSim import sim


class PosThread(threading.Thread):
    def __init__(self, args):
        threading.Thread.__init__(self)
        self.args = args

    def run(self):
        os.system(self.args[0]+" "+self.args[1])


class ControlThread(threading.Thread):
    def __init__(self, args):
        threading.Thread.__init__(self)
        self.args = args

    def run(self):
        os.system(self.args[0]+" "+self.args[1])


# def pos_th():
#     os.system('/home/xander/Documents/RobotSoccerGameEnv/venv/bin/python '
#               '/home/xander/Documents/RobotSoccerGameEnv/pos_control/position.py')
#
#
# def control_th():
#     os.system('/home/xander/Documents/RobotSoccerGameEnv/venv/bin/python '
#               '/home/xander/Documents/RobotSoccerGameEnv/pos_control/control.py')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    sim.simxFinish(-1)
    while True:
        clientID = sim.simxStart("127.0.0.1", 19991, True, True, 5000, 5)  # 建立和服务器的连接
        if clientID != -1:  # 连接成功
            logging.info('Scene connect successfully')
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

    # get handle and initialization
    _, robot_handle = sim.simxGetObjectHandle(clientID, "/EP", sim.simx_opmode_oneshot_wait)
    logging.info("robot handle return: ", _)
    _, ball_handle = sim.simxGetObjectHandle(clientID, "/ball", sim.simx_opmode_oneshot_wait)
    logging.info("ball handle return: ", _)
    _, __ = sim.simxGetObjectPosition(clientID, robot_handle, -1, sim.simx_opmode_streaming)
    _, __ = sim.simxGetObjectOrientation(clientID, robot_handle, -1, sim.simx_opmode_streaming)
    _, __ = sim.simxGetObjectPosition(clientID, ball_handle, -1, sim.simx_opmode_streaming)
    _, __ = sim.simxGetObjectOrientation(clientID, ball_handle, -1, sim.simx_opmode_streaming)

    robot_pos = Queue(10)
    robot_ang = Queue(10)
    ball_pos = Queue(10)
    ball_ang = Queue(10)

    





    # pos_thread = threading.Thread(target=pos_th, args=(), name="pos_thread")
    # control_thread = threading.Thread(target=control_th, args=(), name="control_thread")

    # pos_thread.start()
    # control_thread.start()

    python_exec_path = '/home/xander/Documents/RobotSoccerGameEnv/venv/bin/python'
    pos_path = '/home/xander/Documents/RobotSoccerGameEnv/pos_control/position.py'
    control_path = '/home/xander/Documents/RobotSoccerGameEnv/pos_control/control.py'

    pos_th = PosThread((python_exec_path, pos_path))
    control_th = ControlThread((python_exec_path, control_path))

    pos_th.start()
    control_th.start()

    pos_th.join()
    control_th.join()

