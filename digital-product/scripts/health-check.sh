#!/bin/bash
# Health check - run via cron or monitoring service
# Exit 0 = healthy, Exit 1 = unhealthy

URL="${1:-http://localhost:8000/api/health}"
EXPECTED_MODEL="${2:-gemma4}"

response=$(curl -sf --max-time 5 "$URL" 2>/dev/null)

if [ -z "$response" ]; then
    echo "[FAIL] No response from $URL"
    exit 1
fi

status=$(echo "$response" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
ollama=$(echo "$response" | grep -o '"ollama":"[^"]*"' | cut -d'"' -f4)

if [ "$status" = "online" ] && [ "$ollama" = "connected" ]; then
    echo "[OK] PrivacyAI Toolkit healthy"
    models=$(echo "$response" | grep -o '"models":\[[^]]*\]' | cut -d':' -f2 | tr -d '[]" ')
    echo "  Models: $models"
    exit 0
else
    echo "[WARN] Status: $status | Ollama: $ollama"
    exit 1
fi