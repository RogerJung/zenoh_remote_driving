#!/bin/bash

source $HOME/autoware/install/setup.bash

ros2 service call /api/operation_mode/change_to_autonomous autoware_adapi_v1_msgs/srv/ChangeOperationMode {}

