#!/bin/bash

export ROS_MASTER_URI=http://192.168.15.21:11311
export ROS_IP=192.168.15.21
export ROS_USERNAME=192.168.15.21
echo "##### ENVVAR UPDATED! #####"

cd /home/chip/catkin_ws/src/kerberus
git pull
echo "##### REPOSITORY UPDATED! #####"

source /opt/ros/indigo/setup.bash
source /home/chip/catkin_ws/devel/setup.bash

echo "##### ENV SOURCED! #####"

echo "##### SATARTING ROS... #####"
# running sensor nodes
roslaunch kerberus_robot sonar.launch
