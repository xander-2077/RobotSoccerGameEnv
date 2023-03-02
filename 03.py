# -*-coding:utf-8-*-
# author: Xander
# 4 EP robots act the same actions
import time

from CoppeliaSim import sim
import sys
from multi_robomaster import multi_robot
from robomaster import led

ROBOT_NUM = 4
DISTANCE_BY_SITE = 0.3


def reset_task(robot_group):
    """初始自由模式 & 关掉所有灯效"""
    robot_group.led.set_led(led.COMP_ALL, 255, 1, 1, led.EFFECT_OFF)
    robot_group.set_group_robots_mode(multi_robot.FREE_MODE)
    robot_group.led.set_led(led.COMP_ALL, 1, 255, 1, led.EFFECT_FLASH)


def group_task(robot_group):
    x = 0.3
    y = 0.3
    z = 90
    # 前进 0.3米
    robot_group.chassis.move(-x, 0, 0, 2, 180).wait_for_completed()
    # 后退 0.3米
    robot_group.chassis.move(x, 0, 0, 2, 180).wait_for_completed()
    # 左移 0.3米
    robot_group.chassis.move(0, -y, 0, 2, 180).wait_for_completed()
    # 右移 0.3米
    robot_group.chassis.move(0, y, 0, 2, 180).wait_for_completed()
    # 左转 90度
    robot_group.chassis.move(0, 0, z, 2, 180).wait_for_completed()
    # 右转 90度
    robot_group.chassis.move(0, 0, -z, 2, 180).wait_for_completed()


if __name__ == '__main__':
    # CoppeliaSim Start
    sim.simxFinish(-1)
    clientID = sim.simxStart("127.0.0.1", 19991, True, True, 5000, 5)
    if clientID != -1:
        print("Connection successful!")
    else:
        print("Connection not successful!")
        sys.exit("Could not connect")

    # res, EP_A0_handle = sim.simxGetObjectHandle(clientID, "/EP_A0", sim.simx_opmode_oneshot_wait)
    # res, position = sim.simxGetObjectPosition(clientID, EP_A0_handle, -1, sim.simx_opmode_streaming)
    # while sim.simxGetConnectionId(clientID) != -1:
    #     res, position = sim.simxGetObjectPosition(clientID, EP_A0_handle, -1, sim.simx_opmode_buffer)
    #     if res == sim.simx_return_ok:
    #         print(position)
    #     time.sleep(0.5)


    # Init Config
    robots_sn_list = ['3JKDH2T00159G8', '3JKCJC400302GS', '3JKCJC400301ZP', '3JKCJC400301UD']

    multi_robots = multi_robot.MultiEP()
    multi_robots.initialize()

    # Modified
    number = multi_robots.number_id_by_sn(robots_sn_list, [1, robots_sn_list[0]], [2, robots_sn_list[1]],
                                          [3, robots_sn_list[2]], [4, robots_sn_list[3]])
    print("The number of robot is: {0}".format(number))

    robot_group_all = multi_robots.build_group([1, 2, 3, 4])
    # robot_group_1 = multi_robots.build_group([1, 2])
    # robot_group_2 = multi_robots.build_group([3, 4])
    # robot_group_3 = multi_robots.build_group([1, 3])
    # robot_group_4 = multi_robots.build_group([4])
    # robot_group_5 = multi_robots.build_group([1, 2, 3])

    multi_robots.run([robot_group_all, group_task])

    print("Game over")
    multi_robots.close()
