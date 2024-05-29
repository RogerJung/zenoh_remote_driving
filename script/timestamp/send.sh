#!/bin/bash

source env.sh
while true; do

    ffmpeg -f v4l2 -input_format mjpeg -framerate 30 \
        -video_size 1920x1080 \
        -i /dev/video0 -tune zero_latency \
        -vf "drawtext=text='%{localtime\:%Y-%m-%d %H\\\\\:%M\\\\\:%S}.%{eif\:(1000 * (t - floor(t)))\:d}':x=10:y=10:fontcolor=white: fontsize=38: box=1: boxcolor=black@0.5" \
        -f mpegts tcp://${VEHICLE_IP}:8003?connect

    # Check whether "ffmpeg" execute success or not.
    if [ $? -eq 0 ]; then
        echo "FFmpeg success..."
        break
    else
        echo "FFmpeg error, restarting..."
        sleep 1  # Retry
    fi
done
