#!/bin/bash


/usr/bin/screen -S robot_main_process -ADm bash -l -c '/home/pi/catkin_ws/src/my_dynamixel_workbench_tutorial/src/robot_main_program_launcher.sh'
#tmux new -s robot_main_process "/home/pi/catkin_ws/src/my_dynamixel_workbench_tutorial/src/robot_main_program_launcher.sh"