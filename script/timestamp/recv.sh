#!/bin/bash


ffmpeg -fflags nobuffer -flags low_delay \
    -f mpegts -i tcp://${VEHICLE_IP}:8080?connect \
    -vf "drawtext=text='%{localtime\:%Y-%m-%d %H\\\\\:%M\\\\\:%S}.%{eif\:(1000 * (t - floor(t)))\:d}': fontcolor=white: fontsize=24: box=1: boxcolor=black@0.5: x=w-tw-10: y=10" \
    output.mp4
