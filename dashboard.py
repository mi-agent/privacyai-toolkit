#!/usr/bin/env python3
"""Zero Cost Earn - Unified Dashboard Server"""
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import json
import urllib.request
import urllib.error

PORT = 8888

HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Zero Cost Earn Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, system-ui, sans-serif; background: #0a0a0f; color: #e2e8f0; min-height: 100vh; }
        .container { max-width: 1100px; margin: 0 auto; padding: 30px 20px; }
        h1 { font-size: 2.2rem; background: linear-gradient(135deg, #60a5fa, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 6px; }
        .subtitle { color: #64748b; margin-bottom: 30px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; }
        .card { background: #111827; border: 1px solid #1f2937; border-radius: 12px; padding: 20px; }
        .card h2 { font-size: 1.1rem; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }
        .status-dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }
        .online { background: #22c55e; box-shadow: 0 0 8px #22c55e; }
        .offline { background: #ef4444; }
        .url { font-family: monospace; color: #60a5fa; font-size: 0.85rem; padding: 6px 12px; background: #0f172a; border-radius: 6px; display: inline-block; margin-top: 8px; text-decoration: none; }
        .models { margin-top: 8px; }
        .model { background: #1e293b; padding: 4px 10px; border-radius: 6px; font-size: 0.8rem; display: inline-block; margin: 2px; }
        footer { margin-top: 40px; padding-top: 20px; border-top: 1px solid #1f2937; text-align: center; color: #475569; font-size: 0.85rem; }
        table { width: 100%; font-size: 0.85rem; }
        td { padding: 4px 0; }
        .sticky-bar { position: fixed; bottom: 0; left: 0; right: 0; background: #111827; border-top: 1px solid #1f2937; padding: 12px 20px; display: flex; justify-content: center; gap: 20px; }
        .sticky-bar a { color: #60a5fa; text-decoration: none; font-size: 0.9rem; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Zero Cost Earn Dashboard</h1>
        <p class="subtitle">All running services and project status</p>
        <div class="grid">
            <div class="card">
                <h2><span id="s1" class="status-dot offline"></span> AI Privacy Toolkit</h2>
                <p style="color:#64748b;font-size:0.9rem;margin-bottom:8px;">6 privacy AI tools - 100% local, $0 cost</p>
                <a href="http://localhost:8000" class="url">localhost:8000</a>
            </div>
            <div class="card">
                <h2><span id="s2" class="status-dot offline"></span> Browser Agent</h2>
                <p style="color:#64748b;font-size:0.9rem;margin-bottom:8px;">AI-powered web automation</p>
                <div style="color:#64748b;font-size:0.85rem;">Chrome: <span id="chrome-tabs">-</span> tabs</div>
                <a href="http://localhost:8001" class="url">localhost:8001</a>
            </div>
            <div class="card">
                <h2><span id="s3" class="status-dot offline"></span> Ollama AI Engine</h2>
                <p style="color:#64748b;font-size:0.9rem;margin-bottom:8px;">Free local LLM inference</p>
                <div class="models" id="models"></div>
            </div>
            <div class="card">
                <h2>Project Status</h2>
                <table>
                    <tr><td style="color:#64748b;">AI Privacy Toolkit</td><td style="text-align:right;color:#22c55e;">Live</td></tr>
                    <tr><td style="color:#64748b;">Browser Agent</td><td style="text-align:right;color:#22c55e;">Live</td></tr>
                    <tr><td style="color:#64748b;">AI Tools Guide</td><td style="text-align:right;color:#22c55e;">Ready</td></tr>
                </table>
            </div>
            <div class="card">
                <h2>Revenue Streams</h2>
                <table>
                    <tr><td style="color:#64748b;">Privacy Toolkit API</td><td style="text-align:right;color:#f59e0b;">Next</td></tr>
                    <tr><td style="color:#64748b;">Content + Affiliate</td><td style="text-align:right;color:#f59e0b;">Next</td></tr>
                    <tr><td style="color:#64748b;">Browser Agent SaaS</td><td style="text-align:right;color:#64748b;">Planning</td></tr>
                </table>
            </div>
            <div class="card">
                <h2>Projects</h2>
                <p style="color:#22c55e;font-family:monospace;font-size:0.8rem;">~/Projects/ai-privacy-toolkit</p>
                <p style="color:#22c55e;font-family:monospace;font-size:0.8rem;">~/Projects/browser-agent</p>
                <p style="color:#22c55e;font-family:monospace;font-size:0.8rem;">~/Projects/ai-tools-guide</p>
            </div>
        </div>
        <footer>Zero Cost Earn | Auto-restart via launchd (coming soon)</footer>
    </div>
    <div class="sticky-bar">
        <a href="http://localhost:8000">Privacy Toolkit</a>
        <a href="http://localhost:8001">Browser Agent</a>
        <a href="http://localhost:8888">Dashboard</a>
    </div>
    <script>
        async function refresh() {
            try {
                const r = await fetch('/api/status');
                const d = await r.json();
                if (d.privacy_toolkit && d.privacy_toolkit.status === 'online')
                    document.getElementById('s1').className = 'status-dot online';
                if (d.browser_agent && d.browser_agent.chrome === 'connected') {
                    document.getElementById('s2').className = 'status-dot online';
                    document.getElementById('chrome-tabs').textContent = d.browser_agent.tabs;
                }
                if (d.ollama_models && d.ollama_models.length > 0) {
                    document.getElementById('s3').className = 'status-dot online';
                    document.getElementById('models').innerHTML = d.ollama_models.map(m => '<span class="model">' + m + '</span>').join('');
                }
            } catch(e) {}
        }
        refresh();
        setInterval(refresh, 10000);
    </script>
</body>
</html>
"""

class Dashboard(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/status':
            def get_health(port, path):
                try:
                    with urllib.request.urlopen(f"http://localhost:{port}{path}", timeout=3) as r:
                        return json.loads(r.read())
                except:
                    return {"status": "offline"}
            privacy = get_health(8000, "/api/health")
            agent = get_health(8001, "/browser/status")
            try:
                with urllib.request.urlopen("http://localhost:11434/api/tags", timeout=3) as r:
                    ollama = json.loads(r.read())
                    models = [m["name"] for m in ollama.get("models", [])]
            except:
                models = []
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "privacy_toolkit": privacy,
                "browser_agent": agent,
                "ollama_models": models
            }, indent=2).encode())
        elif self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(HTML.encode())
        else:
            super().do_GET()

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    server = HTTPServer(('0.0.0.0', PORT), Dashboard)
    print(f"Dashboard: http://localhost:{PORT}")
    server.serve_forever()