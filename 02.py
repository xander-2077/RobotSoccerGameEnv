from CoppeliaSim import sim
import sys
from robomaster import robot
from multi_robomaster import multi_robot


def group_task(robot_group):
    x = 0.1
    y = 0.1
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


def main():
    sim.simxFinish(-1)
    clientID = sim.simxStart("127.0.0.1", 19991, True, True, 5000, 5)
    if clientID != -1:
        print("Connection successful!")
    else:
        print("Connection not successful!")
        sys.exit("Could not connect")

    single_robot()
    # multiple_robot()


def single_robot():
    # single EP robot
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")
    ep_robot.chassis.drive_speed(0.2, 0, 0)


def multiple_robot():
    robots_sn_list = ['3JKDH2T00159G8', '3JKCJC400302GS']

    multi_robots = multi_robot.MultiEP()
    multi_robots.initialize()
    # multi_robots._MultiRobotBase_robots_list

    number = multi_robots.number_id_by_sn(robots_sn_list, [1, robots_sn_list[0]], [2, robots_sn_list[1]])
    print("The number of robot is: {0}".format(number))

    robot_1 = multi_robots.build_group([1])
    robot_2 = multi_robots.build_group([2])
    robot_all = multi_robots.build_group([1, 2])

    multi_robots.run([robot_1, group_task])
    multi_robots.run([robot_2, group_task])
    multi_robots.run([robot_all, group_task])

    print("Game over")
    multi_robots.close()


if __name__ == '__main__':
    main()
