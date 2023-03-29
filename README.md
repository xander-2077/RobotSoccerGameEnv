# Robot Soccer Game Environment

## Installation

### Install CoppeliaSim

Refer to `Installation` and `Build` part of [robomaster_sim](https://github.com/jeguzzi/robomaster_sim).
CoppeliaSim Edu 4.4.0 is recommended.

### Install Python Packages

Refer to [Robomaster SDK](https://github.com/jeguzzi/robomaster_ros#robomaster-sdk). A virtual environment `venv` is 
recommended (Anaconda is not recommended). We modified a few code, so you could just pull this repo.

## Running

1. Start CoppeliaSim like
```shell
./CoppeliaSim_Edu_V4_4_0_rev0_Ubuntu20_04/coppeliasim.sh
```
2. Open simulation scene `soccer_game.simscene.xml`.
3. IP alias
```shell
sudo ifconfig lo:0 127.0.1.1/8 up
sudo ifconfig lo:1 127.0.1.2/8 up
sudo ifconfig lo:2 127.0.1.3/8 up
```
4. Modify the child script of robot in lua
```lua
function sysCall_init()
    local index = sim.getNameSuffix(nil)
    -- (index, IP/IP mask, serial number)
    handle = simRobomaster.create_ep(index, "127.0.0.1/8", "3JKDH2T00159G8")
end
```
5. Add to the child script of ball
```lua
simRemoteApi.start(19999)
```
6. Press PLAY in CoppeliaSim.
7. Try this to test if everything in CoppeliaSim is fine.
```lua
simRobomaster.set_target_twist(0, {x=0.2, y=-0.1, theta=0.1});
simRobomaster.set_target_twist(1, {y=0.2, theta=-0.1});
simRobomaster.set_target_twist(2, {x=0.2, y=-0.12});
simRobomaster.set_target_twist(3, {x=0.2, y=0.1})

simRobomaster.move_arm(0, 1, 1, true)

simRobomaster.open_gripper(int robot_handle, bool wait=true)
simRobomaster.close_gripper(int robot_handle, bool wait=true)
simRobomaster.set_gripper_target(int handle, string state, float power=0.5)
```
8. Run the python script `simpleTest.py` in CoppeliaSim folder to test if everything is fine.

## CoppeliaSim remote API
https://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsPython.htm

## Robomaster API
https://robomaster-dev.readthedocs.io/zh_CN/latest/index.html


