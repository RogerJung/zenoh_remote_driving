#!/usr/bin/bash

source $HOME/autoware/install/setup.bash

ros2 topic pub /initialpose geometry_msgs/msg/PoseWithCovarianceStamped "{ \
  header: { \
    stamp: { sec: 1714578814, nanosec: 208498609 }, \
    frame_id: 'map' \
  }, \
  pose: { \
    pose: { \
      position: { x: 3776.230224609375, y: 73698.3671875, z: 19.557 }, \
      orientation: { x: 0.0, y: 0.0, z: -1, w: 0.25 } \
    }, \
    covariance: [ \
      1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, \
      0.0, 0.0, 0.01, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.01, 0.0, 0.0, \
      0.0, 0.0, 0.0, 0.0, 0.01, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.2 \
    ] \
   } \
}" -1
