#!/usr/bin/env bash

source docker/config_bash

docker run -d -p 8181:8181 -p 2181:2181 -p 2888:2888 -p 3888:3888 \
    -e S3_BUCKET="quixey-${QENV}" \
    -e S3_PREFIX="zk-exhibitor" \
    -e HOSTNAME=$(hostname) \
    orca.quixey.com/docker-zk-exhibitor

