#!/bin/bash

VEHICLE_IP=10.10.0.71

while true; do

    ffmpeg -hwaccel cuda -f v4l2 -input_format mjpeg -framerate 30 -video_size 1920x1080 -i /dev/video0 -tune zero_latency -f mpegts tcp://${VEHICLE_IP}:8003?connect
    # ffmpeg -i /dev/video0 -vf scale=1920:1080 -tune zero_latency -f mpegts tcp://${VEHICLE_IP}:8003?connect

    # Check whether "ffmpeg" execute success or not.
    if [ $? -eq 0 ]; then
        echo "FFmpeg success..."
        break
    else
        echo "FFmpeg error, restarting..."
        sleep 1  # Retry
    fi
done
