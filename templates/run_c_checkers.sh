#!/bin/bash

IMAGE_NAME="git.infra.cospace.de:4567/guidelines/code-quality-control/build-docker:latest"

LOCAL_WORKING_DIR="$(pwd)"
DOCKER_WORKING_DIR="/usr/$(basename "${LOCAL_WORKING_DIR}")"

echo "${LOCAL_WORKING_DIR}"

COMMAND_TO_RUN_ON_DOCKER=(sh -c "\
    bash /usr/checkers/00-style-analysis.sh     -I src/ -I include/  && \
    bash /usr/checkers/01-code-complexity.sh    -I src/ -I include/  && \
    bash /usr/checkers/02-static-analysis.sh    -I src/ -I include/")

sudo docker run \
    --rm \
    -v "${LOCAL_WORKING_DIR}":"${DOCKER_WORKING_DIR}"\
    -w "${DOCKER_WORKING_DIR}"\
    --name my_container "${IMAGE_NAME}"  \
    "${COMMAND_TO_RUN_ON_DOCKER[@]}"
