#!/usr/bin/bash
source /opt/ros/noetic/setup.bash

# Build catkin_ws
cd barracuda-serial-server/catkin_ws
catkin_make
source devel/setup.bash

# Start interactive shell session in /opt/barracuda-camera directory
cd ..
exec /bin/bash