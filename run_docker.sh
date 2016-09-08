#!/usr/bin/env bash

DEFAULT_QENV='dev'
DEFAULT_LOG_DIR='/var/log/docker/zookeeper'
: ${QENV:=$DEFAULT_QENV}
: ${LOG_DIR:=$DEFAULT_LOG_DIR}

docker run -d -p 8181:8181 -p 2181:2181 -p 2888:2888 -p 3888:3888 \
    -e S3_BUCKET="quixey-${QENV}" \
    -e S3_PREFIX="zk-exhibitor" \
    -e HOSTNAME=$(hostname) \
    orca.quixey.com/docker-zk-exhibitor

