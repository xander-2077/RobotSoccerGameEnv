import time
import logging
import numpy as np
from CoppeliaSim import sim
from robomaster import robot

PI = 3.141592654
global clientID
logging.basicConfig(level=logging.INFO)


def get_target_position(target_handle):
    """
    Remember to initialize with sim.simx_opmode_streaming.
    """
    return np.array(sim.simxGetObjectPosition(clientID, target_handle, -1, sim.simx_opmode_buffer)[1])[:-1]


class EP_ROBOT:

    def __init__(self, robot_name):
        self._robot = robot.Robot()
        self._robot.initialize(conn_type="sta")
        self.chassis = self._robot.chassis
        _, self.handle = sim.simxGetObjectHandle(clientID, robot_name, sim.simx_opmode_oneshot_wait)
        if _ != sim.simx_return_ok:
            logging.warning("Cannot get robot handle!")
        _, __ = sim.simxGetObjectPosition(clientID, self.handle, -1, sim.simx_opmode_streaming)
        _, __ = sim.simxGetObjectOrientation(clientID, self.handle, -1, sim.simx_opmode_streaming)

    def get_position(self):
        while all(np.array(sim.simxGetObjectPosition(clientID, self.handle, -1, sim.simx_opmode_buffer)[1])[:-1] == [0., 0.]):
            pass
        return np.array(sim.simxGetObjectPosition(clientID, self.handle, -1, sim.simx_opmode_buffer)[1])[:-1]

    def get_orientation(self, form='rad'):
        angle_3d = np.array(sim.simxGetObjectOrientation(clientID, self.handle, -1, sim.simx_opmode_buffer)[1])
        if form == 'rad':
            return -angle_3d[1] - PI / 2 if angle_3d[0] > 0 else PI / 2 + angle_3d[1]
        elif form == 'ang':
            return (-angle_3d[1] - PI / 2 if angle_3d[0] > 0 else PI / 2 + angle_3d[1]) * 180 / PI
        else:
            logging.warning("Wrong parameter!")

    def ep_move2point(self, target_pos):
        relative_pos = target_pos - self.get_position()
        logging.info("distance: {}".format(relative_pos))
        robot_ang = self.get_orientation('ang')
        logging.info("robot angle: {}".format(robot_ang))
        target_ang = np.arctan2(relative_pos[1], relative_pos[0]) * 180 / PI
        logging.info("target angle: {}".format(target_ang))
        delta_ang = target_ang - robot_ang
        logging.info("delta angle: {}".format(delta_ang))

        self.chassis.move(z=delta_ang, z_speed=60).wait_for_completed()
        self.chassis.move(x=np.linalg.norm(relative_pos, ord=2)).wait_for_completed()


if __name__ == '__main__':

    sim.simxFinish(-1)
    while True:
        clientID = sim.simxStart("127.0.0.1", 19991, True, True, 5000, 5)
        if clientID != -1:
            logging.info('Scene connect successfully')
            break
        else:
            time.sleep(0.2)

    # stop = sim.simxStopSimulation(clientID, sim.simx_opmode_blocking)
    # time.sleep(4)
    # start = sim.simxStartSimulation(clientID, sim.simx_opmode_blocking)

    # https://blog.csdn.net/weixin_41754912/article/details/82353012
    # 设置仿真步长，为了保持API端与V-rep端相同步长
    t_step = 0.005  # 定义仿真步长
    sim.simxSetFloatingParameter(clientID, sim.sim_floatparam_simulation_time_step, t_step, sim.simx_opmode_oneshot)
    # 打开同步模式
    sim.simxSynchronous(clientID, True)
    sim.simxStartSimulation(clientID, sim.simx_opmode_oneshot)

    # Get handle and Initialization
    ep_robot = EP_ROBOT("/EP")

    ret, ball_handle = sim.simxGetObjectHandle(clientID, "/ball", sim.simx_opmode_oneshot_wait)
    logging.info("ball handle return: {}".format(ret))
    _, __ = sim.simxGetObjectPosition(clientID, ball_handle, -1, sim.simx_opmode_streaming)
    # _, __ = sim.simxGetObjectOrientation(clientID, ball_handle, -1, sim.simx_opmode_streaming)

    while sim.simxGetConnectionId(clientID) != -1:
        # robot_pos = np.array(sim.simxGetObjectPosition(clientID, robot_handle, -1, sim.simx_opmode_buffer)[1])

        while all(get_target_position(ball_handle) == [0., 0.]):
            pass
        ball_pos = get_target_position(ball_handle)

        ep_robot.ep_move2point(ball_pos)

        # relative_pos = ball_pos - ep_robot.get_position()
        # logging.info("distance: {}".format(relative_pos))
        #
        # robot_ang = ep_robot.get_orientation('ang')
        # logging.info("robot angle: {}".format(robot_ang))
        # target_ang = np.arctan2(relative_pos[1], relative_pos[0]) * 180 / PI
        # logging.info("target angle: {}".format(target_ang))
        # delta_ang = target_ang - robot_ang
        # logging.info("delta angle: {}".format(delta_ang))
        #
        # ep_robot.chassis.move(z=delta_ang, z_speed=60).wait_for_completed()
        # ep_robot.chassis.move(x=np.linalg.norm(relative_pos, ord=2)).wait_for_completed()

        break
