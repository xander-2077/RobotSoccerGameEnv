import os
import threading
from CoppeliaSim import sim


def robot_start(index):
    os.system('/home/xander/Documents/RobotSoccerGameEnv/venv/bin/python '
              '/home/xander/Documents/RobotSoccerGameEnv/multirobots_individual/EP_' + str(index) + '.py')


if __name__ == '__main__':
    while True:
        clientId = sim.simxStart("127.0.0.1", 19991, True, True, 5000, 5)  # 建立和服务器的连接
        if clientId != -1:  # 连接成功
            print('Scene connect successfully')
            break

    for i in range(4):
        robot = threading.Thread(target=robot_start, args=(i, ))
        print("num: ", i)
        robot.setDaemon(True)
        robot.start()