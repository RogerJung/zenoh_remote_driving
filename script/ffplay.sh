#!/bin/bash

VEHICLE_IP=10.10.0.71
PORT=8080

# 设置 ffplay 命令
ffplay_command="ffplay -fflags nobuffer -flags low_delay -f mpegts tcp://${VEHICLE_IP}:${PORT}?connect"

# 无限循环
while :
do
    # 尝试执行 ffplay 命令
    $ffplay_command

    sleep 1
done
