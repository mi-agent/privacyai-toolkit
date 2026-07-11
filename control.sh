#!/bin/bash
# Zero Cost Earn - Master Control Panel
# All projects in one place

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
PYTHON=~/.hermes/hermes-agent/venv/bin/python
PID_DIR="$HOME/.zero-cost-earn"
mkdir -p "$PID_DIR"

cd ~/Projects

status() {
    echo -e "${YELLOW}=== Zero Cost Earn — Status${NC}"
    echo ""
    # Check ports
    for port in 8000 8001; do
        if lsof -i :$port > /dev/null 2>&1; then
            echo -e "  Port $port: ${GREEN}✅ Running${NC}"
        else
            echo -e "  Port $port: ${RED}❌ Stopped${NC}"
        fi
    done
    echo ""
    # Ollama
    if curl -s --max-time 2 http://localhost:11434/api/tags > /dev/null; then
        echo -e "  Ollama: ${GREEN}✅ Connected${NC}"
        curl -s http://localhost:11434/api/tags | python3 -c "import sys,json; models=json.load(sys.stdin)['models']; [print(f'    • {m[\"name\"]} ({m[\"size\"]//1024**3}GB)') for m in models[:5]]" 2>/dev/null
    else
        echo -e "  Ollama: ${RED}❌ Not running (run: ollama serve)${NC}"
    fi
    echo ""
    # Projects
    echo "  Projects:"
    for proj in ai-privacy-toolkit browser-agent ai-tools-guide; do
        if [ -d "$HOME/Projects/$proj" ]; then
            echo -e "    ✅ $proj"
        fi
    done
}

start() {
    echo -e "${GREEN}🚀 Starting all services...${NC}"
    
    # Ollama check
    if ! curl -s --max-time 2 http://localhost:11434/api/tags > /dev/null; then
        echo -e "${YELLOW}⚠️ Ollama not running. Starting...${NC}"
        nohup ollama serve > "$PID_DIR/ollama.log" 2>&1 &
        sleep 2
    fi
    
    # Privacy Toolkit
    if ! lsof -i :8000 > /dev/null; then
        cd ~/Projects/ai-privacy-toolkit
        nohup $PYTHON -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > "$PID_DIR/privacy.log" 2>&1 &
        echo $! > "$PID_DIR/privacy.pid"
        echo -e "  ✅ AI Privacy Toolkit → http://localhost:8000"
    fi
    
    # Browser Agent
    if ! lsof -i :8001 > /dev/null; then
        cd ~/Projects/browser-agent
        nohup $PYTHON -m uvicorn app.main:app --host 0.0.0.0 --port 8001 > "$PID_DIR/agent.log" 2>&1 &
        echo $! > "$PID_DIR/agent.pid"
        echo -e "  ✅ Browser Agent → http://localhost:8001"
    fi
    
    sleep 2
    status
}

stop() {
    echo -e "${YELLOW}🛑 Stopping all services...${NC}"
    kill $(cat "$PID_DIR"/*.pid 2>/dev/null) 2>/dev/null
    rm -f "$PID_DIR"/*.pid
    echo -e "${GREEN}✅ All stopped${NC}"
}

logs() {
    echo -e "${YELLOW}=== Recent Logs ===${NC}"
    for log in "$PID_DIR"/*.log; do
        [ -f "$log" ] || continue
        name=$(basename "$log" .log)
        echo -e "${GREEN}--- $name ---${NC}"
        tail -10 "$log"
    done
}

case "${1:-status}" in
    start) start ;;
    stop) stop ;;
    status) status ;;
    logs) logs ;;
    restart) stop; sleep 1; start ;;
    *) echo "Usage: $0 {start|stop|status|restart|logs}" ;;
esac