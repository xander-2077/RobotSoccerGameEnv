from CoppeliaSim import sim
import sys
import numpy as np
import matplotlib.pyplot as mlp


def main():
    sim.simxFinish(-1)
    clientID = sim.simxStart("127.0.0.1", 19999, True, True, 5000, 5)
    if clientID != -1:
        print("Connection successful!")
    else:
        print("Connection not successful!")
        sys.exit("Could not connect")

    res, objs = sim.simxGetObjects(clientID, sim.sim_handle_all, sim.simx_opmode_blocking)
    # if res == sim.simx_return_ok:
    #     print('Number of objects in the scene: ', len(objs))
    errorcode, leftmotor_handle = sim.simxGetObjectHandle(clientID, "/pioneer/leftMotor", sim.simx_opmode_oneshot_wait)
    print("errorcode: ", errorcode, "\nleft motor handle: ", leftmotor_handle)
    errorcode, rightmotor_handle = sim.simxGetObjectHandle(clientID, "/pioneer/rightMotor",
                                                           sim.simx_opmode_oneshot_wait)
    print("errorcode: ", errorcode, "\nright motor handle: ", rightmotor_handle)

    sim.simxSetJointTargetVelocity(clientID, leftmotor_handle, 0.2, sim.simx_opmode_streaming)
    # sim.simxSetJointTargetVelocity(clientID, rightmotor_handle, 0.2, sim.simx_opmode_streaming)

    sensor_handle = []
    for i in range(16):
        errorcode, handle = sim.simxGetObjectHandle(clientID, "/pioneer/ultrasonicSensor[" + str(i) + "]",
                                                    sim.simx_opmode_oneshot_wait)
        print("errorcode:", errorcode, " ", "handle", i, ":", handle)
        sensor_handle.append(handle)

    # for i in range(16):
    #     returnCode, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = sim.simxReadProximitySensor(
    #                                                                                                     clientID,
    #                                                                                                     sensor_handle[i],
    #                                                                                                     sim.simx_opmode_streaming)

    errorcode, cam1_handle = sim.simxGetObjectHandle(clientID, "/cam1", sim.simx_opmode_oneshot_wait)
    print(errorcode)
    errorcode, resolution, image = sim.simxGetVisionSensorImage(clientID, cam1_handle, 0, sim.simx_opmode_streaming)
    print(errorcode)
    errorcode, resolution, image = sim.simxGetVisionSensorImage(clientID, cam1_handle, 0, sim.simx_opmode_buffer)
    print(resolution)
    # print(image)
    # time.sleep(5)
    im = np.array(image, dtype=np.uint8)
    print(im.shape)
    im.resize([resolution[0], resolution[1], 3])
    print(im.shape)
    mlp.imshow(im)
    mlp.show()
    # sim.simxGetPingTime(clientID)
    # sim.simxFinish(clientID)


if __name__ == '__main__':
    main()
