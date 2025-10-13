#!/bin/bash

#CONTAINER_NAME="py-v"
CONTAINER_NAME="go-v"

docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}" | head -n 1

while true; do
    docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}" | grep "$CONTAINER_NAME"
    sleep 2
done
