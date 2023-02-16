from CoppeliaSim import sim

while True:
    clientId = sim.simxStart("127.0.0.1", 19992, True, True, 5000, 5)  # 建立和服务器的连接
    if clientId != -1:  # 连接成功
        print('Robot1 connect successfully')
        break