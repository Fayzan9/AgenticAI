#!/bin/bash
# Build the agent executor container image

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMAGE_NAME="${CONTAINER_IMAGE:-agent-executor:latest}"

echo "Building container image: $IMAGE_NAME"

cd "$SCRIPT_DIR"

podman build -t "$IMAGE_NAME" .

echo ""
echo "✅ Build complete: $IMAGE_NAME"
echo ""
echo "Verify with: podman images | grep agent-executor"
echo "Run test with: podman run --rm $IMAGE_NAME"
