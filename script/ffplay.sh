#!/bin/bash

VEHICLE_IP=10.10.0.71
PORT=8080

ffplay_command="ffplay -fflags nobuffer -flags low_delay -f mpegts tcp://${VEHICLE_IP}:${PORT}?connect"

while :
do
    $ffplay_command

    sleep 1
done
