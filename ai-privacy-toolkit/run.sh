#!/bin/bash
# AI Privacy Toolkit - One-line launch

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🔒 AI Privacy Toolkit${NC}"
echo ""

# Check Ollama
if curl -s --max-time 3 http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Ollama connected${NC}"
    curl -s http://localhost:11434/api/tags | python3 -c "import sys,json; m=json.load(sys.stdin)['models']; print('   Models:', ', '.join([x['name'] for x in m[:5]]))"
else
    echo -e "${YELLOW}⚠️ Ollama not running. Starting...${NC}"
    echo "   Run: brew services start ollama  OR  ollama serve"
fi

# Install deps
echo ""
echo "📦 Checking dependencies..."
cd "$(dirname "$0")"
pip3 install -q fastapi uvicorn python-multipart httpx 2>/dev/null

# Launch
echo -e "${GREEN}🚀 Starting server...${NC}"
echo "   URL: http://localhost:8000"
echo "   API: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload