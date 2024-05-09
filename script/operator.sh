#!/bin/bash

source ./install/setup.bash
source ./external/autoware_manual_control/install/setup.bash
source ${HOME}/autoware/install/setup.bash

VEHICLE_IP=192.168.225.72
OPERATOR_IP=192.168.225.73

# Init. tmux
tmux kill-server


# FFPLAY
tmux new -s bridge_ffplay -d
tmux send-keys -t bridge_ffplay "bash ./script/ffplay.sh" ENTER

# Autoware & Lidar
tmux new -s bridge_autoware -d
tmux send-keys -t bridge_autoware "RUST_LOG=info ./external/zenoh-plugin-ros2dds/target/release/zenoh-bridge-ros2dds -e tcp/${VEHICLE_IP}:8001" ENTER
ros2 run remote_lidar remote_lidar &

# Control
sleep 2 && ros2 run g923_control g923_control
