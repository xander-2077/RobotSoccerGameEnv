import os
import time
import sys
import threading
from queue import Queue
import logging
from CoppeliaSim import sim
from robomaster import robot


def main():
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="sta")
    ep_chassis = ep_robot.chassis

    print("control active!")




if __name__ == '__main__':
    main()
