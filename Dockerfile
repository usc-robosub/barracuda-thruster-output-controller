# Base image for ROS Noetic on Ubuntu 20.04 Focal
FROM ros:noetic-ros-base-focal

COPY . /opt/barracuda-thruster-output-server

# Set working directory
WORKDIR /opt

# Install dependencies for the IMU sensor and update other tools
RUN apt-get update && rm -rf /var/lib/apt/lists/*

# Source the workspace on container start
CMD ["/bin/bash", "/opt/barracuda-thruster-output-server/entrypoint.sh"]