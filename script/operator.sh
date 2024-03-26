#!/bin/bash

source ./install/setup.bash
source ./external/autoware_manual_control/install/setup.bash
source ${HOME}/autoware/install/setup.bash

VEHICLE_IP=10.10.0.71
OPERATOR_IP=10.10.0.72

# Init. tmux
tmux kill-server

# Autoware & Lidar
export ROS_DOMAIN_ID=1
tmux new -s bridge_autoware -d
tmux send-keys -t bridge_autoware "RUST_LOG=info ./external/zenoh-plugin-ros2dds/target/release/zenoh-bridge-ros2dds -e tcp/${VEHICLE_IP}:8001" ENTER
ros2 run remote_lidar remote_lidar &

# Control
export ROS_DOMAIN_ID=2
tmux new -s bridge_control -d
tmux send-keys -t bridge_control "export ROS_DOMAIN_ID=2 && RUST_LOG=info ./external/zenoh-plugin-ros2dds/target/release/zenoh-bridge-ros2dds -e tcp/${VEHICLE_IP}:8002" ENTER
export ROS_DOMAIN_ID=2 && sleep 2 && ros2 run g923_control g923_control
