#!/bin/bash


source /home/pi/.bashrc

echo "Robot main program awaking..."

# echo "Run roscore..."
# roscore &


echo "waiting for roscore to run."
sleep 20


CATKIN_WS_PATH="/home/pi/catkin_ws"

cd $CATKIN_WS_PATH
pwd

echo "setup catkin_ws"
source devel/setup.bash

MAIN_SCRIPT_NAME="main.py"
PACKAGE_NAME="my_dynamixel_workbench_tutorial"

echo "Launch Main script"
rosrun $PACKAGE_NAME $MAIN_SCRIPT_NAME

