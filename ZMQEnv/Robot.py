from robomaster import robot
from robomaster.led import EFFECT_ON, EFFECT_OFF
import numpy as np
import math
import random
import time


class EP_Robot:
    def __init__(self, _sim):
        self.sim = _sim
        self.eprobot = robot.Robot()
        self.eprobot.initialize(conn_type="sta")
        self.eprobot.set_robot_mode('chassis_lead')
        self.chassis = self.eprobot.chassis
        self.eprobot.led.set_led(r=0, g=0, b=230, effect=EFFECT_ON)

        self.hdl = self.sim.getObject("/EP")

    def move(self, x, y, z, timeout=0.5):
        self.chassis.drive_speed(x=x, y=y, z=z, timeout=timeout)
        # time.sleep(t_interval)  # TODO

    def get_pos(self):
        return self.sim.getObjectPosition(self.hdl, self.sim.handle_world)[:-1]

    def get_ori(self, form='rad'):
        angle_3d = np.array(self.sim.getObjectOrientation(self.hdl, self.sim.handle_world))
        if form == 'rad':
            return -angle_3d[1] - math.pi / 2 if angle_3d[0] < 0 else math.pi / 2 + angle_3d[1]
        elif form == 'ang':
            return (-angle_3d[1] - math.pi / 2 if angle_3d[0] < 0 else math.pi / 2 + angle_3d[1]) * 180 / math.pi

    def random_initial_robot(self):
        self.sim.setObjectPosition(self.hdl, self.sim.handle_world, (0, random.uniform(-1, 1), 0))
        self.sim.setObjectOrientation(self.hdl, self.sim.handle_world, (math.pi / 2, 0, 0))

    def close(self):
        self.eprobot.chassis.stop()
        self.eprobot.led.set_led(effect=EFFECT_OFF)
        self.eprobot.close()
