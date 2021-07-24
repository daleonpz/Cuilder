#!/bin/bash

DEVICE_NAME="msp430fr2433"
IMAGE_NAME="git.infra.cospace.de:4567/toolchains/toolchain-msp430/build-docker:latest"

LOCAL_WORKING_DIR="$(pwd)"
DOCKER_WORKING_DIR="/usr/$(basename ${LOCAL_WORKING_DIR})"

COMMAND_TO_RUN_ON_DOCKER=(sh -c "rake clean DEVICE=${DEVICE_NAME} && rake DEVICE=${DEVICE_NAME} ")

echo "###############################"

echo -e "Working Directory: \r\n\t ${LOCAL_WORKING_DIR}"
echo -e "Executing: \r\n\t ${COMMAND_TO_RUN_ON_DOCKER}"

echo "###############################"


sudo docker run \
    --rm \
    -v $LOCAL_WORKING_DIR:$DOCKER_WORKING_DIR\
    -w $DOCKER_WORKING_DIR\
    --name my_container $IMAGE_NAME  \
    "${COMMAND_TO_RUN_ON_DOCKER[@]}"
