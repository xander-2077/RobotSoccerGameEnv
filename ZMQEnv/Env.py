from coppeliasim_zmqremoteapi_client import *
import gym
import numpy as np
import math
import time
import logging
from Robot import EP_Robot

logging.basicConfig(level=logging.INFO)
gym.logger.set_level(40)


class SoccerGameEnv(gym.Env):
    def __init__(self, args):
        super().__init__()

        self.args = args
        self._max_episode_steps = self.args.max_episode_step
        self.a0 = 10  # reward for close to target
        self.a1 = 1  # reward for close to goal

        self.distance = [0., 0.]
        self.goal_distance = [0., 0.]
        self.current_step = 0
        self.total_steps = 0
        self.current_episode = 0

        self.observation_space = gym.spaces.Box(low=-np.inf, high=np.inf, shape=(11,), dtype=np.float32)
        self.action_space = gym.spaces.Box(low=-1.0, high=1.0, shape=(3,), dtype=np.float32)

        # defaults are host='localhost', port=23000)
        self.client = RemoteAPIClient()
        self.sim = self.client.getObject('sim')
        # self.client.setStepping(True)  # sync mode
        # self.sim.setFloatParam(self.sim.floatparam_simulation_time_step, 0.05)
        self.sim.startSimulation()
        self.sim.setBoolParam(self.sim.boolparam_display_enabled, self.args.gui)

        self.target_hdl = self.sim.getObject("/ball")
        self.robot = EP_Robot(self.sim)

    def step(self, action):
        self.current_step += 1
        self.total_steps += 1

        if self.current_step > 1:
            self.distance[0] = self.distance[1]
            self.goal_distance[0] = self.goal_distance[1]

        # Pass action to CoppeliaSim
        self.robot.move(action[0] * 3.5, action[1] * 3.5, action[2] * 600)

        # Retrieve obs & info
        observation = self._get_obs()
        info = self._get_info()
        self.distance[1] = info["distance"]
        self.goal_distance[1] = info["goal_distance"]

        # Calculate Reward and judge if end
        # int result,list collidingObjectHandles=sim.checkCollision(int entity1Handle,int entity2Handle)
        if observation[4] < -4.075:
            reward = 100
            done = True
            print("----------------------------------------")
            print(f"total step: {self.total_steps}")
            print(f"current episode: {self.current_episode}")
            print(f"current step: {self.current_step}")
            print(f"obs: {observation}")
            print(f"info: {info}")
            print(f"done: {done}")
            print(f"reward: {reward}")
            return observation, reward, done, info
        else:
            reward = -1
            reward += self.a0 * (self.distance[0] - self.distance[1])
            reward += self.a1 * (self.goal_distance[0] - self.goal_distance[1])
            if not (-3.575 < observation[1] < 1.55 and -3.7 < observation[0] < -0.3):
                reward += -1

            done = False
            # if self.current_step >= self._max_episode_steps:
            #     done = True

            if self.current_step % 10 == 0:
                print("----------------------------------------")
                print(f"total step: {self.total_steps}")
                print(f"current episode: {self.current_episode}")
                print(f"current step: {self.current_step}")
                print(f"obs: {observation}")
                print(f"info: {info}")
                print(f"done: {done}")
                print(f"reward: {reward}")

            # Decide frequency
            time.sleep(1 / self.args.decide_freq)
            # for _ in range(10):
            #     self.client.step()

            return observation, reward, done, info

    def reset(self):
        self.current_episode += 1
        if self.current_episode % 100 == 0:
            # self.robot.close()
            self.sim.stopSimulation()
            time.sleep(5)
            self.sim.startSimulation()
            time.sleep(1)
            self.sim.setBoolParam(self.sim.boolparam_display_enabled, self.args.gui)
            self.target_hdl = self.sim.getObject("/ball")
            self.robot = EP_Robot(self.sim)
        elif self.args.random_initial_state:
            self.robot.random_initial_robot()
            self.sim.setObjectPosition(self.target_hdl, self.sim.handle_world, (-1.925, -1., 0.11))
        else:
            self.sim.setObjectPosition(self.target_hdl, self.sim.handle_world, (-1.925, -1., 0.11))
            self.sim.setObjectPosition(self.robot.hdl, self.sim.handle_world, (-1.925, 1, 0.0674))
            self.sim.setObjectOrientation(self.robot.hdl, self.sim.handle_world, (-math.pi / 2, 0, -math.pi / 2))

        self.current_step = 0
        self.distance[0] = self.sim.checkDistance(self.robot.hdl, self.target_hdl)[1][6]
        self.goal_distance[0] = self.sim.getObjectPosition(self.target_hdl, self.sim.handle_world)[1] + 4.075

        return self._get_obs()

    def render(self, mode="human"):
        pass

    def close(self):
        self.robot.close()
        self.sim.stopSimulation()

    def _get_obs(self):
        # robot position: 2
        # robot orientation: 1
        # target position: 2
        # robot linear velocity: 2
        # robot angular velocity: 3
        # distance: 1
        linear_velocity, angular_velocity = self.sim.getObjectVelocity(self.robot.hdl)
        observation = np.concatenate((np.hstack((self.robot.get_pos(), self.robot.get_ori())),
                                      np.array(self.sim.getObjectPosition(self.target_hdl, self.sim.handle_world)[:-1]),
                                      np.array(linear_velocity[:-1]),
                                      np.array(angular_velocity),
                                      np.array(self.sim.checkDistance(self.robot.hdl, self.target_hdl)[1][6]).reshape(
                                          (1,))
                                      ), axis=0, dtype='float32')
        return observation

    def _get_info(self):
        goal_distance = self.sim.getObjectPosition(self.target_hdl, self.sim.handle_world)[1] + 4.075
        distance = self.sim.checkDistance(self.robot.hdl, self.target_hdl)[1][6]
        return {"goal_distance": goal_distance, "distance": distance}
