#!/bin/bash
IMAGE_NAME="my_portscanner"
if [[ "$(docker images -q $IMAGE_NAME 2> /dev/null)" == "" ]]; then
  docker buildx build -t my_portscanner .
fi
docker run --rm my_portscanner localhost
