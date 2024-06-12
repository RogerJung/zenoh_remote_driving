#!/bin/bash

source ${HOME}/repos/F1EIGHT/install/setup.bash

# Init. tmux
tmux kill-server

# FFMPEG
tmux new -s bridge_ffmpeg -d
tmux send-keys -t bridge_ffmpeg "taskset --cpu-list 0-2 bash $HOME/zenoh_remote_driving/script/ffmpeg.sh" ENTER

# Autoware
export ROS_DOMAIN_ID=1
tmux new -s bridge_autoware -d
tmux send-keys -t bridge_autoware "RUST_LOG=info ./external/zenoh-plugin-ros2dds/target/release/zenoh-bridge-ros2dds -l tcp/${VEHICLE_IP}:8001" ENTER
tmux new -s autoware -d
tmux send-keys -t autoware "taskset --cpu-list 3-11 ros2 launch autoware_launch planning_simulator.launch.xml map_path:=$HOME/autoware_map/test/ vehicle_model:=sample_vehicle sensor_model:=sample_sensor_kit" ENTER
