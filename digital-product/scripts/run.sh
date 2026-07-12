#!/bin/bash
# PrivacyAI Toolkit - Production Launcher
# Single command to start everything

set -e

PYTHON="${HOME}/.hermes/hermes-agent/venv/bin/python"
APP_DIR="${HOME}/Projects/ai-privacy-toolkit"
LOG_DIR="${HOME}/.zero-cost-earn"
PORT="${PORT:-8000}"

mkdir -p "$LOG_DIR"
cd "$APP_DIR"

echo "Starting PrivacyAI Toolkit on port $PORT..."
echo "Dashboard: http://localhost:$PORT"
echo "Tools:     http://localhost:$PORT/tools"
echo "Pricing:   http://localhost:$PORT/pricing"
echo ""

exec "$PYTHON" -m uvicorn app.main:app \
    --host 0.0.0.0 \
    --port "$PORT" \
    --access-log \
    2>&1 | tee -a "$LOG_DIR/privacy.log"