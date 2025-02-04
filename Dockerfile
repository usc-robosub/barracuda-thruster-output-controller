FROM ros:noetic-ros-base-focal

RUN sudo apt-get update \
    && sudo apt-get install -y --no-install-recommends git vim wget zstd \
    ros-noetic-rosserial-server \
    ros-noetic-rosserial-python \
    ros-noetic-rosserial-arduino \
    ros-noetic-rosserial-server \
    && rm -rf /var/lib/apt/lists/* \
    && echo "source /opt/ros/noetic/setup.bash" >> /root/.bashrc
    # && echo "[ -f /opt/barracuda-dvl/catkin_ws/devel/setup.bash ] && source /opt/barracuda-dvl/catkin_ws/devel/setup.bash" >> /root/.bashrc \ 
    # && echo "cd /opt/barracuda-dvl/catkin_ws" >> /root/.bashrc

COPY . /opt/barracuda-serial-server/

# Set working directory
WORKDIR /opt

# Source the workspace on container start
CMD ["/bin/bash", "/opt/barracuda-serial-server/entrypoint.sh"]