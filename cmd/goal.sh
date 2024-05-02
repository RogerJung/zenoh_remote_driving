#!/usr/bin/bash

source $HOME/autoware/install/setup.bash

ros2 topic pub /planning/mission_planning/goal geometry_msgs/msg/PoseStamped "{ \
  header: { \
    stamp: { sec: 1714579977, nanosec: 133644277 }, \
    frame_id: 'map' \
  }, \
  pose: { \
    position: { x: 3781.310791015625, y: 73715.515625, z: 0.0 }, \
    orientation: { x: 0.0, y: 0.0, z: -0.52, w: 0.85 } \
  } \
}" -1

