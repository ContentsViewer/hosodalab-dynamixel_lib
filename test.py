#!/usr/bin/python

# import os




import rospy

from dynamixel_servomotor_controller import *
from xl_config import *


#from time import sleep


PROTOCOL_VERSION = 2.0


DXL_ID = 2
BAUDRATE = 57600
DEVICENAME = '/dev/ttyUSB0'

def main():
    print "start node."
    rospy.init_node("servomotor_controller")

    timer = rospy.Rate(1)




    motor_controller = DynamixelServomotorController(device_name = DEVICENAME, protocol_version = PROTOCOL_VERSION,\
                    baudrate = BAUDRATE, motor_config = XLConfig())
    motor_controller.current_id = DXL_ID


    motor_controller.set_operating_mode(XLConfig.OPERATING_MODE_VELOCITY_CONTROL_MODE)
    motor_controller.set_torque_enable(1)



    speed = 0.0


    sw = False

    while not rospy.is_shutdown():
        sw ^= True

        motor_controller.set_led(int(sw))
        
        motor_controller.set_goal_velocity(0.5)

        timer.sleep()

    motor_controller.set_led(0)
    motor_controller.set_goal_velocity(0.0)
    motor_controller.end()

    
if __name__ == "__main__":
    main()