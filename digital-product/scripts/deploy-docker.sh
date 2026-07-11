#!/bin/bash
# Docker deployment script
# Run this to deploy to any server with Docker

set -e

IMAGE_NAME="${1:-privacyai/toolkit}"
PORT="${2:-8000}"
OLLAMA_URL="${3:-http://host.docker.internal:11434}"

echo "Deploying PrivacyAI Toolkit..."
echo "  Image: $IMAGE_NAME"
echo "  Port: $PORT"
echo "  Ollama: $OLLAMA_URL"
echo ""

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "Docker not found. Installing..."
    curl -fsSL https://get.docker.com | sh
fi

# Pull or build
docker pull "$IMAGE_NAME" 2>/dev/null || {
    echo "Building image locally..."
    docker build -t "$IMAGE_NAME" .
}

# Stop old container
docker stop privacyai 2>/dev/null || true
docker rm privacyai 2>/dev/null || true

# Run
docker run -d \
    --name privacyai \
    -p "${PORT}:8000" \
    -e "OLLAMA_URL=${OLLAMA_URL}" \
    -e "OLLAMA_MODEL=gemma4:e4b" \
    --restart unless-stopped \
    "$IMAGE_NAME"

echo ""
echo "Deployed! http://localhost:$PORT"
echo ""
echo "View logs: docker logs -f privacyai"
echo "Stop:      docker stop privacyai"