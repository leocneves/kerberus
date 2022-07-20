#!/bin/bash

export ROS_MASTER_URI=http://192.168.15.3:11311
export ROS_IP=192.168.15.3
export ROS_USERNAME=192.168.15.3
echo "##### ENV VAR UPDATED! #####"

#sh -c "echo nameserver 8.8.8.8 > /etc/resolv.conf"

echo "######### ARRUMA DNS ############"

cd /home/pi/catkin_ws/src/kerberus
git pull

echo "##### REPOSITORY UPDATED! #####"

source /opt/ros/melodic/setup.bash
source /home/pi/catkin_ws/devel/setup.bash

echo "##### ENV SOURCED! #####"

chmod 777 /dev/ttyACM0

echo "##### PERMISSIONS ADDED! #####"

echo "##### STARTING ROS... #####"
# running sensor nodes
roslaunch kerberus_robot sonar.launch
