#!/bin/bash

export ROS_MASTER_URI=http://192.168.15.37:11311
export ROS_IP=192.168.15.37
export ROS_USERNAME=192.168.15.37
echo "##### ENV VAR UPDATED! #####"

cd /home/ubuntu/catkin_ws/src/kerberus
git pull
echo "##### REPOSITORY UPDATED! #####"

source /opt/ros/kinetic/setup.bash
source /home/ubuntu/catkin_ws/devel/setup.bash

echo "##### ENV SOURCED! #####"

chmod 777 /dev/ttyACM0

echo "##### PERMISSIONS ADDED! #####"

echo "##### STARTING ROS... #####"
# running sensor nodes
roslaunch kerberus_robot sonar.launch
