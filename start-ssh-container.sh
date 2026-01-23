#!/usr/bin/env bash
set -euo pipefail

CONTAINER_NAME="oeleo-ssh"
IMAGE="linuxserver/openssh-server:latest"
PORT="2222"

if ! docker info >/dev/null 2>&1; then
  echo "Docker engine is not running. Start Docker Desktop and try again."
  exit 1
fi

if docker ps -a --format '{{.Names}}' | grep -qx "$CONTAINER_NAME"; then
  echo "Starting existing container $CONTAINER_NAME..."
  docker start "$CONTAINER_NAME" >/dev/null
else
  echo "Creating and starting container $CONTAINER_NAME..."
  docker run -d --name "$CONTAINER_NAME" -p "$PORT:$PORT" \
    -e USER_NAME=oeleo \
    -e USER_PASSWORD=oeleo \
    -e PASSWORD_ACCESS=true \
    "$IMAGE" >/dev/null
fi

echo "SSH test container is running on localhost:$PORT"
