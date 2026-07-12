#!/bin/bash
# ~/Library/LaunchAgents/com.zerocostearn.server.plist
# Auto-start all Zero Cost Earn services on login

cat > "$HOME/Library/LaunchAgents/com.zerocostearn.server.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.zerocostearn.server</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-c</string>
        <string>
            sleep 3
            cd ~/Projects/ai-privacy-toolkit && ~/.hermes/hermes-agent/venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 >> ~/.zero-cost-earn/privacy.log 2>&1 &
            cd ~/Projects/browser-agent && ~/.hermes/hermes-agent/venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 >> ~/.zero-cost-earn/agent.log 2>&1 &
            cd ~/Projects && python3 dashboard.py >> ~/.zero-cost-earn/dashboard.log 2>&1 &
            echo "Zero Cost Earn services started at $(date)" >> ~/.zero-cost-earn/launch.log
        </string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/com.zerocostearn.server.out.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/com.zerocostearn.server.err.log</string>
</dict>
</plist>
EOF

mkdir -p ~/.zero-cost-earn

# Load the service
launchctl unload ~/Library/LaunchAgents/com.zerocostearn.server.plist 2>/dev/null
launchctl load ~/Library/LaunchAgents/com.zerocostearn.server.plist 2>/dev/null

echo "Service installed and loaded!"
echo "Services will auto-start on every login."
echo ""
echo "Manual commands:"
echo "  launchctl start com.zerocostearn.server  # Start now"
echo "  launchctl stop com.zerocostearn.server   # Stop"
echo "  launchctl unload ~/Library/LaunchAgents/com.zerocostearn.server.plist  # Remove"