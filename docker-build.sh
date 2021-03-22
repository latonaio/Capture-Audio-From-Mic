#!/usr/bin/env bash

PUSH=$1
DATE="$(date "+%Y%m%d%H%M")"
REPOSITORY_NAME="latonaio"
IMAGE_NAME="capture-audio-from-mic"

DOCKER_BUILDKIT=1 docker build --secret id=ssh,src=$HOME/.ssh/bitbucket/id_rsa -f . -t ${REPOSITORY_NAME}/${IMAGE_NAME}:"${DATE}" .
docker tag ${REPOSITORY_NAME}/${IMAGE_NAME}:"${DATE}" ${REPOSITORY_NAME}/${IMAGE_NAME}:latest

if [[ $PUSH == "push" ]]; then
    docker push ${REPOSITORY_NAME}/${IMAGE_NAME}:"${DATE}"
    docker push ${REPOSITORY_NAME}/${IMAGE_NAME}:latest
fi
