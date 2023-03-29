from robomaster import robot as rmrobot
import numpy as np
import time
import logging
from CoppeliaSim import sim

logging.basicConfig(level=logging.INFO)
PI = 3.141592654


class EP_Robot:
    def __init__(self, clientID, ball_handle):
        self.clientID = clientID
        self.ball_handle = ball_handle
        self._robot = rmrobot.Robot()
        self._robot.initialize(conn_type="sta")
        self.chassis = self._robot.chassis
        _, self.handle = sim.simxGetObjectHandle(clientID, "/EP", sim.simx_opmode_oneshot_wait)
        if _ != sim.simx_return_ok:
            logging.warning("Cannot get robot handle!")

        # set the position and orientation of robot in random
        # self.random_set_robot_position()

        # Initialize to get position and orientation of robot
        sim.simxGetObjectPosition(self.clientID, self.handle, -1, sim.simx_opmode_streaming)
        sim.simxGetObjectOrientation(self.clientID, self.handle, -1, sim.simx_opmode_streaming)
        # 检测机器人与球的距离
        sim.simxCheckDistance(self.clientID, self.handle, self.ball_handle, sim.simx_opmode_streaming)
        # 检测机器人移动速度
        sim.simxGetObjectVelocity(self.clientID, self.handle, sim.simx_opmode_streaming)

    def move(self, x, y, z, t_interval=0.5):
        self.chassis.drive_speed(x=x, y=y, z=z, timeout=t_interval)
        time.sleep(t_interval)  # TODO: need to change

    # def random_set_robot_position(self):
    #     sim.simxSetObjectPosition(self.clientID, self.handle, self.handle, (0, random.uniform(-1, 1), 0), sim.simx_opmode_oneshot)
    #     sim.simxSetObjectOrientation(self.clientID, self.handle, self.handle, (PI / 2, 0, 0), sim.simx_opmode_oneshot)

    def get_pos(self):
        while all(
                np.array(sim.simxGetObjectPosition(self.clientID, self.handle, -1, sim.simx_opmode_buffer)[1])[:-1] == [
                    0., 0.]):
            pass
        return np.array(sim.simxGetObjectPosition(self.clientID, self.handle, -1, sim.simx_opmode_buffer)[1])[:-1]

    def get_ori(self, form='rad'):
        angle_3d = np.array(sim.simxGetObjectOrientation(self.clientID, self.handle, -1, sim.simx_opmode_buffer)[1])
        if form == 'rad':
            return -angle_3d[1] - PI / 2 if angle_3d[0] < 0 else PI / 2 + angle_3d[1]
        elif form == 'ang':
            return (-angle_3d[1] - PI / 2 if angle_3d[0] < 0 else PI / 2 + angle_3d[1]) * 180 / PI
        else:
            logging.warning("Wrong parameter!")

    def set_pos_and_ori(self):
        pass
