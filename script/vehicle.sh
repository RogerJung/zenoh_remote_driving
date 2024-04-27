#!/bin/bash

source ${HOME}/repos/F1EIGHT/install/setup.bash
source ./install/setup.bash
source /opt/ros/humble/setup.bash

VEHICLE_IP=10.10.0.71
OPERATOR_IP=10.10.0.73

# Init. tmux
tmux kill-server

# FFMPEG
tmux new -s bridge_ffmpeg -d
tmux send-keys -t bridge_ffmpeg "bash $HOME/zenoh_remote_driving/script/ffmpeg.sh" ENTER

# Autoware
export ROS_DOMAIN_ID=1
tmux new -s bridge_autoware -d
tmux send-keys -t bridge_autoware "RUST_LOG=info ./external/zenoh-plugin-ros2dds/target/release/zenoh-bridge-ros2dds -l tcp/${VEHICLE_IP}:8001" ENTER
tmux new -s autoware -d
tmux send-keys -t autoware "ros2 launch autoware_launch autoware.launch.xml map_path:=${HOME}/autoware_map/sample-map-planning vehicle_model:=sample_vehicle sensor_model:=sample_sensor_kit" ENTER

# while true
# do
#     ros2 bag play rosbag2_2024_03_24-17_07_09/
# done

# Control
export ROS_DOMAIN_ID=2
ros2 run remote_control remote_control -l tcp/${VEHICLE_IP}:8002
