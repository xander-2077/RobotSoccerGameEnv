import gym
from gym import spaces
import numpy as np
import logging
import time
from CoppeliaSim import sim

import sys
sys.path.append("../..")
from GymEnv.EPRobot import EP_Robot

logging.basicConfig(level=logging.INFO)
gym.logger.set_level(40)
PI = 3.141592654


class SoccerGameEnv(gym.Env):
    def __init__(self, args):
        super().__init__()

        self.args = args
        self.GUI = self.args.gui
        self._max_episode_steps = self.args.max_episode_step
        self.current_step = 0
        self.total_steps = 0
        self.alpha = 10
        self.distance = [0., 0.]

        self.robot = None
        self.ball_handle = None
        self.clientID = None

        # self.observation_space = spaces.Dict(
        #     {
        #         'robot': spaces.Box(low=-5.,
        #                             high=5.,
        #                             shape=(3,),
        #                             dtype=np.float16),  # TODO: change low & high
        #         'ball': spaces.Box(low=-5.,
        #                            high=5.,
        #                            shape=(2,),
        #                            dtype=np.float16)
        #     })
        self.observation_space = spaces.Box(low=-5., high=5., shape=(5,), dtype=np.float16)
        self.action_space = spaces.Box(
            low=np.array([-1, -1, -1]),
            high=np.array([1, 1, 1]),
            dtype=np.float32
        )

        # Initialize
        sim.simxFinish(-1)
        while True:
            self.clientID = sim.simxStart("127.0.0.1", 19997, True, True, 5000, 5)
            if self.clientID != -1:
                # turn on or off visualization interface
                logging.info('Scene connect successfully')
                break
            else:
                time.sleep(0.2)

        sim.simxStartSimulation(self.clientID, sim.simx_opmode_blocking)
        sim.simxSetBooleanParameter(self.clientID, sim.sim_boolparam_display_enabled, self.GUI, sim.simx_opmode_oneshot)
        self.init_sim()

    def init_sim(self):
        # get the handle of ball
        _, self.ball_handle = sim.simxGetObjectHandle(self.clientID, "/ball", sim.simx_opmode_oneshot_wait)
        if _ != sim.simx_return_ok:
            logging.warning("Cannot get ball handle!")
        sim.simxGetObjectPosition(self.clientID, self.ball_handle, -1, sim.simx_opmode_streaming)

        self.robot = EP_Robot(self.clientID, self.ball_handle)

    def _get_obs(self):
        # return {"robot": np.hstack((self.robot.get_pos(), self.robot.get_ori())).astype('float16'),
        #         "ball": np.array(
        #             sim.simxGetObjectPosition(self.clientID, self.ball_handle, -1, sim.simx_opmode_buffer)[1],
        #             dtype='float16')[:-1]
        #         }
        return np.concatenate((np.hstack((self.robot.get_pos(), self.robot.get_ori())).astype('float16'),
                               np.array(sim.simxGetObjectPosition(self.clientID, self.ball_handle, -1,
                                                                  sim.simx_opmode_buffer)[1],
                                        dtype='float16')[:-1]))

    def _get_info(self):
        # Check if collision
        # _, __ = sim.simxCheckCollision(self.clientID, self.robot.clientID, self.ball_handle,
        #                                sim.simx_opmode_streaming)
        # _, have_collision = sim.simxCheckCollision(self.clientID, self.robot.clientID, self.ball_handle,
        #                                            sim.simx_opmode_buffer)

        _, distance = sim.simxCheckDistance(self.clientID, self.robot.handle, self.ball_handle,
                                            sim.simx_opmode_buffer)
        _, linear_velocity, angular_velocity = sim.simxGetObjectVelocity(self.clientID, self.robot.handle,
                                                                         sim.simx_opmode_buffer)
        return {"distance": distance, "linear_velocity": linear_velocity, "angular_velocity": angular_velocity}

    def step(self, action):
        sim.simxSetBooleanParameter(self.clientID, sim.sim_boolparam_display_enabled, self.GUI, sim.simx_opmode_oneshot)

        # Pass action to CoppeliaSim
        self.robot.move(action[0] * 3.5, action[1] * 3.5, action[2] * 600)
        self.current_step += 1
        self.total_steps += 1

        # Retrieve obs & info
        observation = self._get_obs()
        info = self._get_info()
        done = False
        if observation[3] < -4.125 or self.current_step >= self._max_episode_steps:  # or observation['robot']:
            done = True

        # Calculate Reward
        reward = 100 if done else -1
        self.distance[1] = info["distance"]
        reward += self.alpha * (self.distance[0] - self.distance[1])
        if not (-3.575 < observation[1] < 1.55 and -3.7 < observation[0] < -0.3):
            reward += -1

        print("-----------------------------")
        # print("total step: {} / {}".format(self.current_step, self.))
        print("current step: {}".format(self.current_step))
        print("obs: {}".format(observation))
        print("info: {}".format(info))
        print("done: {}".format(done))
        print("reward: {}".format(reward))

        return observation, reward, done, info

    def reset(self):
        # sim.simxStopSimulation(self.clientID, sim.simx_opmode_blocking)
        # time.sleep(4)
        # sim.simxStartSimulation(self.clientID, sim.simx_opmode_blocking)
        # self.init_sim()

        if self.args.random_initial_state:
            self.robot.random_initial_robot()
        else:
            sim.simxSetObjectPosition(self.clientID, self.ball_handle, -1, (-1.925, -1., 0.11), sim.simx_opmode_oneshot)
            sim.simxSetObjectPosition(self.clientID, self.robot.handle, -1, (-1.925, 1, 0.0674),
                                      sim.simx_opmode_oneshot)

        sim.simxSetObjectOrientation(self.clientID, self.robot.handle, -1, (-PI / 2, 0, -PI / 2),
                                     sim.simx_opmode_oneshot)

        self.current_step = 0
        _, self.distance[0] = sim.simxCheckDistance(self.clientID, self.robot.clientID, self.ball_handle,
                                                    sim.simx_opmode_buffer)
        return self._get_obs()

    def close(self):
        sim.simxStopSimulation(self.clientID, sim.simx_opmode_blocking)
        sim.simxFinish(self.clientID)

    def render(self, mode="human"):
        return None
