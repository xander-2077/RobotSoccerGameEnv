# For playground_tof_ep scene

from CoppeliaSim import sim
import sys
import time
from robomaster import robot
import numpy as np
import matplotlib.pyplot as plt


def sub_data_handler(sub_info):
    distance = sub_info
    print("tof1:{0}  tof2:{1}  tof3:{2}  tof4:{3}".format(distance[0], distance[1], distance[2], distance[3]))


def main():
    sim.simxFinish(-1)
    clientID = sim.simxStart("127.0.0.1", 19999, True, True, 5000, 5)
    if clientID != -1:
        print("Connection successful!")
    else:
        print("Connection not successful!")
        sys.exit("Could not connect")

    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")

    ep_chassis = ep_robot.chassis
    ep_chassis.drive_speed(x=0.2, y=0.1, z=0, timeout=5)
    # time.sleep(3)

    ep_sensor = ep_robot.sensor
    ep_sensor.sub_distance(freq=20, callback=sub_data_handler)
    time.sleep(60)
    ep_sensor.unsub_distance()
    ep_robot.close()


if __name__ == '__main__':
    main()

