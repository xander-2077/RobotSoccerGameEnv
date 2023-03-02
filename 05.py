# for robot arm and gripper

from CoppeliaSim import sim
import sys
import time
from robomaster import robot


def main():
    sim.simxFinish(-1)
    clientID = sim.simxStart("127.0.0.1", 19991, True, True, 5000, 5)
    if clientID != -1:
        print("Connection successful!")
    else:
        print("Connection not successful!")
        sys.exit("Could not connect")

    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")

    ep_arm = ep_robot.robotic_arm
    # 向前移动20毫米
    ep_arm.move(x=40, y=0).wait_for_completed()
    time.sleep(1)
    # 向后移动20毫米
    ep_arm.move(x=-40, y=0).wait_for_completed()
    time.sleep(1)
    # 向上移动20毫米
    ep_arm.move(x=0, y=40).wait_for_completed()
    time.sleep(1)
    # 向下移动20毫米
    ep_arm.move(x=0, y=-40).wait_for_completed()
    time.sleep(1)

    ep_gripper = ep_robot.gripper
    # 闭合机械爪
    ep_gripper.close(power=50)
    time.sleep(1)
    ep_gripper.pause()
    # 张开机械爪
    ep_gripper.open(power=50)
    time.sleep(1)
    ep_gripper.pause()




    ep_robot.close()


if __name__ == '__main__':
    main()