#!/usr/bin/python

import os

import traceback

import rospy

from dynamixel_servomotor_controller import *
from xl_config import *
from getch import Getch


import socket
import time


#from time import sleep

PORT = 8001
CONNECTION_LOST_TIMEOUT = 5.0

PROTOCOL_VERSION = 2.0


DXL_ID = 2
BAUDRATE = 57600
DEVICENAME = '/dev/ttyUSB0'

def main():
    print "Start node."


    # --- ros setting -----------
    rospy.init_node("robot_controller")

    timer = rospy.Rate(10)
    # end ros setting -------


    # --- socket settgin --------
    server_socket = socket.socket()
    server_socket.bind(('', PORT))
    print 'Launch tcp socket.'
    # end socket setting ------







    motor_controller = DynamixelServomotorController(device_name = DEVICENAME, protocol_version = PROTOCOL_VERSION,\
                    baudrate = BAUDRATE, motor_config = XLConfig())
    motor_controller.current_id = DXL_ID


    #motor_controller.set_operating_mode(XLConfig.OPERATING_MODE_POSITION_CONTROL_MODE)
    motor_controller.set_operating_mode(XLConfig.OPERATING_MODE_VELOCITY_CONTROL_MODE)

    print "torque_enable: "
    motor_controller.set_torque_enable(1)

    print "id: " + str(motor_controller.id())
    print "baudrate: " + str(motor_controller.baudrate())
    print "torque_enable: " + str(motor_controller.torque_enable())
    
    
    


    # sw = False

    is_connected = False
    client_socket = None

    last_request_time = time.time()

    # --- node main loop -----------------------------
    while not rospy.is_shutdown():
        # sw ^= True

        # motor_controller.set_led(int(sw))
        
        try:
            if is_connected:
                # check last request time.
                if time.time() - last_request_time > CONNECTION_LOST_TIMEOUT:
                    print ("[ERROR] long no request. last_request_time: %f; now: %f" % (last_request_time, time.time()))
                    raise Exception


                request_msg = client_socket.recv(1024)

                # --- something to receive ----------------
                if request_msg != "":

                    # lines = request_msg.split("\n")
                    # for line in lines:
                        
                    if request_msg == "ping":
                        client_socket.send("pong\n")

                    elif request_msg.startswith("speed"):
                        args = request_msg.split(" ")
                        try:
                            speed = float(args[1])
                            print "speed: " + str(speed)
                            motor_controller.set_goal_velocity(speed)

                        except:
                            print "[ERROR] cannot set the motor speed"
                            traceback.print_exc()
                        finally:
                            client_socket.send("ACK\n")
                    
                    elif request_msg.startswith("shutdown"):
                        print "shutdown received"
                        try:
                            os.system("sudo shutdown now")
                        except:
                            print "[ERROR] cannot shutdown"
                            traceback.print_exc()
                        finally:
                            client_socket.send("ACK\n")

                    elif request_msg.startswith("reboot"):
                        print "reboot received"
                        try:
                            os.system("sudo reboot")
                        except:
                            print "[ERROR] cannot reboot"
                            traceback.print_exc()
                        finally:
                            client_socket.send("ACK\n")
                        

                    last_request_time = time.time()
                # end something receive --------------------


            else:
                print "Waiting for connection..."
                # wait one connection
                server_socket.listen(1)
                client_socket, client_address = server_socket.accept()
                print "connected!"
                is_connected = True
                last_request_time = time.time()

        except Exception as e:
            print("[ERROR] message:{0}".format(e.message))
            traceback.print_exc()
            print "[ERROR] connection lost. retrying..."
            is_connected = False
            motor_controller.set_goal_velocity(0.0)
            if client_socket is not None:
                client_socket.close()
                client_socket = None



        # print "cmd << ",
        # cmd = raw_input()

        # isAccepted = True
        # if(cmd == "exit"):
        #     print "program is now to end..."
        #     break
        # else: 
        #     try:
        #         speed = float(cmd)
        #         print "speed: " + str(speed)
        #         motor_controller.set_goal_velocity(speed)
        #     except:
        #         isAccepted = False
        
        
        # if not isAccepted:
        #     print "[Error] command parse error!"

        # print "OK"

        # print "loop"
        
        # motor_controller.set_goal_velocity(speed)
        # print "max_position: " +  str(motor_controller.max_position_limit())
        # print "min_position: " +  str(motor_controller.min_position_limit())

        # speed += dir
        # if speed > max_speed:
        #     speed = max_speed
        #     dir *= -1

        # if speed < -max_speed:
        #     speed = -max_speed
        #     dir *= -1

        # print str(speed)

        timer.sleep()
    # end node main loop --------------------

    motor_controller.set_led(0)
    motor_controller.set_goal_velocity(0.0)
    motor_controller.end()
    
    server_socket.close()

    
if __name__ == "__main__":
    main()