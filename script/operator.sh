#!/bin/bash

source ./install/setup.bash
source ./external/autoware_manual_control/install/setup.bash

VEHICLE_IP=10.10.0.71
OPERATOR_IP=10.10.0.72

# Control
RUST_LOG=error ./external/zenoh-plugin-ros2dds/target/release/zenoh-bridge-ros2dds -e tcp/${VEHICLE_IP}:8001 &

sleep 2 && ros2 run autoware_manual_control keyboard_control
