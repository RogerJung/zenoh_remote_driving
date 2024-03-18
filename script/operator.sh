#!/bin/bash

source ./install/setup.bash
source ./external/autoware_manual_control/install/setup.bash

RUST_LOG=error ./external/zenoh-plugin-ros2dds/target/release/zenoh-bridge-ros2dds -e tcp/10.10.0.71:8001 &
ros2 run autoware_manual_control keyboard_control
