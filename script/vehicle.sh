#!/bin/bash

source ./install/setup.bash

# Control
ros2 run remote_control remote_control -l tcp/10.10.0.71:8001
