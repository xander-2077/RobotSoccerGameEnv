from CoppeliaSim import sim
import sys
import time
import numpy as np
import matplotlib.pyplot as mlp


def main():
    sim.simxFinish(-1)
    clientID = sim.simxStart("127.0.0.1", 19997, True, True, 5000, 5)
    if clientID != -1:
        print("Connection successful!")
    else:
        print("Connection not successful!")
        sys.exit("Could not connect")

    # res, objs = sim.simxGetObjects(clientID, sim.sim_handle_all, sim.simx_opmode_blocking)
    # # if res == sim.simx_return_ok:
    # #     print('Number of objects in the scene: ', len(objs))
    _, leftmotor_handle = sim.simxGetObjectHandle(clientID, "/pioneer/leftMotor", sim.simx_opmode_oneshot_wait)
    # print("_: ", _, "\nleft motor handle: ", leftmotor_handle)
    # _, rightmotor_handle = sim.simxGetObjectHandle(clientID, "/pioneer/rightMotor",
    #                                                        sim.simx_opmode_oneshot_wait)
    # print("_: ", _, "\nright motor handle: ", rightmotor_handle)

    sim.simxSetJointTargetVelocity(clientID, leftmotor_handle, 0.2, sim.simx_opmode_streaming)
    # sim.simxSetJointTargetVelocity(clientID, rightmotor_handle, 0.2, sim.simx_opmode_streaming)

    # sensor_handle = []
    # for i in range(16):
    #     _, handle = sim.simxGetObjectHandle(clientID, "/pioneer/ultrasonicSensor[" + str(i) + "]",
    #                                         sim.simx_opmode_oneshot_wait)
    #     print("handle", i, ":", handle)
    #     sensor_handle.append(handle)

    # for i in range(16):
    #     returnCode, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = sim.simxReadProximitySensor(
    #                                                                                                     clientID,
    #                                                                                                     sensor_handle[i],
    #                                                                                                     sim.simx_opmode_streaming)

    # # Camera
    # _, cam1_handle = sim.simxGetObjectHandle(clientID, "/cam1", sim.simx_opmode_oneshot_wait)
    # _, resolution, image = sim.simxGetVisionSensorImage(clientID, cam1_handle, 0, sim.simx_opmode_streaming)
    # while sim.simxGetConnectionId(clientID) != -1:
    #     _, resolution, image = sim.simxGetVisionSensorImage(clientID, cam1_handle, 0, sim.simx_opmode_buffer)
    #     if _ == sim.simx_return_ok:
    #         print(resolution)
    #         im = np.array(image).astype(np.uint8)
    #         # print(im.shape)
    #         im.resize([resolution[0], resolution[1], 3])
    #         # print(im.shape)
    #         mlp.imshow(im)
    #         mlp.show()
    #     time.sleep(0.5)

    time.sleep(3)

    stop = sim.simxStopSimulation(clientID, sim.simx_opmode_blocking)
    time.sleep(4)  # 需要反应时间
    start = sim.simxStartSimulation(clientID, sim.simx_opmode_blocking)

    # # https://blog.csdn.net/weixin_41754912/article/details/82353012
    # lastCmdTime = vrep.simxGetLastCmdTime(clientID)  # 记录当前时间
    # vrep.simxSynchronousTrigger(clientID)  # 让仿真走一步
    # # 开始仿真
    # while vrep.simxGetConnectionId(clientID) != -1：
    # currCmdTime = vrep.simxGetLastCmdTime(clientID)  # 记录当前时间
    # dt = currCmdTime - lastCmdTime  # 记录时间间隔，用于控制
    #     # 读取当前的状态值，之后都用buffer形式读取
    #     for i in range(jointNum):
    #          _, jpos = vrep.simxGetJointPosition(clientID, jointHandle[i], vrep.simx_opmode_buffer)
    #         print(round(jpos * RAD2DEG, 2))
    #         jointConfig[i] = jpos
    #
    #     # 控制命令需要同时方式，故暂停通信，用于存储所有控制命令一起发送
    #     vrep.simxPauseCommunication(clientID, True)
    #     for i in range(jointNum):
    #         vrep.simxSetJointTargetPosition(clientID, jointHandle[i], 120 / RAD2DEG, vrep.simx_opmode_oneshot)
    #     vrep.simxPauseCommunication(clientID, False)
    # lastCmdTime = currCmdTime  # 记录当前时间
    # vrep.simxSynchronousTrigger(clientID)  # 进行下一步
    # vrep.simxGetPingTime(clientID)  # 使得该仿真步走完



    # sim.simxGetPingTime(clientID)
    # sim.simxFinish(clientID)


if __name__ == '__main__':
    main()
