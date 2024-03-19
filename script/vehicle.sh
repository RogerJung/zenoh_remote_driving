#!/bin/bash

source ./install/setup.bash

VEHICLE_IP=10.10.0.71
OPERATOR_IP=10.10.0.72

# Control
ros2 run remote_control remote_control -l tcp/${VEHICLE_IP}:8001
