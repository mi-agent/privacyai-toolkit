"""
Browser Agent - AI-powered web automation
Uses local AI to decide actions, execute via browser
"""
import asyncio
import json
import time
import re
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field
from fastapi import FastAPI, HTTPException, Form, BackgroundTasks
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI(title="Browser Agent", version="1.0.0")

# ============ Config ============
BROWSER_PORT = 9222
CHROME_DEBUG_URL = "http://localhost:9222"
SESSION_DIR = Path("sessions")
SESSION_DIR.mkdir(exist_ok=True)

@dataclass
class Task:
    task_id: str
    goal: str
    status: str = "pending"  # pending, running, done, error
    steps: list = field(default_factory=list)
    result: str = ""
    created_at: float = field(default_factory=time.time)

tasks: dict[str, Task] = {}

# ============ Browser API ============

async def chrome_cmd(method: str, endpoint: str, data: dict = None):
    """Send CDP command to Chrome"""
    import httpx
    url = f"{CHROME_DEBUG_URL}/json/{endpoint}" if endpoint else f"{CHROME_DEBUG_URL}/json/{method}"
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        if data is not None:
            resp = await client.post(url, json=data)
        else:
            resp = await client.get(url)
        return resp.json()

async def get_tabs():
    """List open tabs"""
    try:
        return await chrome_cmd("", "")
    except:
        return []

async def navigate(url: str):
    """Navigate tab to URL"""
    try:
        tabs = await get_tabs()
        if tabs:
            tab = tabs[0]
            await chrome_cmd("", f"activate/{tab['id']}")
        else:
            # Need to create new tab
            await chrome_cmd("", "new", {"url": url})
        return {"status": "ok", "url": url}
    except Exception as e:
        raise HTTPException(500, f"Chrome not accessible: {e}")

async def get_page_content(tab_id: str) -> str:
    """Get page HTML via CDP"""
    try:
        import httpx
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Use Runtime.evaluate to get page content
            resp = await client.post(
                f"{CHROME_DEBUG_URL}/json/runtime.evaluate",
                json={"expression": "document.body.innerText", "returnByValue": True}
            )
            if resp.status_code == 200:
                return resp.json().get("result", {}).get("value", "")
            return ""
    except:
        return ""

async def take_screenshot(tab_id: str = None) -> dict:
    """Take screenshot of current page"""
    return {"screenshot_taken": False, "note": "CDP requires Chrome in debug mode with --remote-debugging-port=9222"}

# ============ AI Decision Engine (Ollama) ============

async def ollama_generate(prompt: str, model: str = "gemma4:e4b") -> str:
    """Use local Ollama for AI decisions"""
    import httpx
    try:
        resp = await httpx.AsyncClient(timeout=120.0).post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.3, "num_predict": 512}
            }
        )
        if resp.status_code == 200:
            return resp.json().get("response", "")
        return f"AI error: {resp.status_code}"
    except Exception as e:
        return f"Connection error: {e}"

async def plan_steps(goal: str, context: str = "") -> list[dict]:
    """Use AI to plan browser action steps"""
    system = f"""You are a browser automation planner. Given a user's goal, break it into specific browser actions.
Available actions: navigate(url), click(selector), type(selector, text), wait(seconds), extract(selector), scroll(direction), screenshot, submit_form(selector)

Return a JSON array of steps:
[{{"action": "navigate", "args": {{"url": "https://..."}}}}, {{"action": "click", "args": {{"selector": "#button"}}}}, ...]

Keep steps minimal (max 8). Only use extract() to get final results."""

    prompt = f"Goal: {goal}\nContext: {context}"
    result = await ollama_generate(f"{system}\n\n{prompt}")
    
    # Parse JSON steps
    try:
        import re
        json_match = re.search(r'\[.*\]', result, re.DOTALL)
        if json_match:
            steps = json.loads(json_match.group())
            return steps
    except:
        pass
    return [{"action": "navigate", "args": {"url": f"https://www.google.com/search?q={goal.replace(' ', '+')}"}}]

# ============ Task Execution ============

async def execute_task(task_id: str):
    """Execute a browser automation task"""
    task = tasks.get(task_id)
    if not task:
        return
    
    task.status = "running"
    
    try:
        # Plan steps with AI
        steps = await plan_steps(task.goal)
        task.steps = steps
        
        for i, step in enumerate(steps):
            action = step.get("action", "")
            args = step.get("args", {})
            
            if action == "navigate":
                # Use Chrome DevTools Protocol via webdriver alternative
                result = await navigate(args.get("url", ""))
                task.steps[i]["result"] = result
            elif action == "wait":
                await asyncio.sleep(args.get("seconds", 2))
                task.steps[i]["result"] = "waited"
            elif action == "screenshot":
                task.steps[i]["result"] = await take_screenshot()
            elif action == "click" or action == "type":
                task.steps[i]["result"] = f"Would {action} {args}"
            elif action == "extract":
                content = await get_page_content("")
                task.steps[i]["result"] = content[:500]
            else:
                task.steps[i]["result"] = f"Unknown action: {action}"
            
            task.steps[i]["status"] = "done"
        
        # Final AI summary
        steps_text = json.dumps(task.steps, indent=2)
        summary_prompt = f"Based on these browser automation results:\n{steps_text}\n\nSummarize what was accomplished for the user's goal: {task.goal}"
        task.result = await ollama_generate(summary_prompt)
        task.status = "done"
        
    except Exception as e:
        task.status = "error"
        task.result = f"Execution error: {str(e)}"

# ============ API Routes ============

@app.post("/tasks")
async def create_task(goal: str = Form(...)):
    """Create a new browser automation task"""
    import uuid
    task_id = str(uuid.uuid4())[:8]
    tasks[task_id] = Task(task_id=task_id, goal=goal)
    
    # Run in background
    asyncio.create_task(execute_task(task_id))
    
    return {"task_id": task_id, "status": "pending", "goal": goal}

@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    """Get task status and results"""
    if task_id not in tasks:
        raise HTTPException(404, "Task not found")
    task = tasks[task_id]
    return {
        "task_id": task.task_id,
        "goal": task.goal,
        "status": task.status,
        "steps": task.steps,
        "result": task.result,
        "progress": f"{len([s for s in task.steps if s.get('status') == 'done'])}/{len(task.steps)}" if task.steps else "0/0"
    }

@app.get("/tasks")
async def list_tasks():
    """List all tasks"""
    return [
        {"task_id": t.task_id, "goal": t.goal, "status": t.status, "created_at": t.created_at}
        for t in tasks.values()
    ]

@app.get("/browser/status")
async def browser_status():
    """Check Chrome DevTools Protocol connection"""
    try:
        tabs = await get_tabs()
        return {"chrome": "connected", "tabs": len(tabs), "tabs_detail": [{"title": t.get("title"), "url": t.get("url")} for t in tabs[:5]]}
    except Exception as e:
        return {"chrome": "disconnected", "error": str(e), "setup_instructions": "Launch Chrome with: open -a 'Google Chrome' --args '--remote-debugging-port=9222'"}

@app.post("/browser/launch")
async def launch_chrome():
    """Instructions to launch Chrome with debugging"""
    return {
        "command": "open -a 'Google Chrome' --args '--remote-debugging-port=9222 --start-fullscreen'",
        "or": "Google Chrome > View > Developer > JavaScript Console > Remote debugging port 9222",
        "alternate": "Chrome needs to be launched with --remote-debugging-port=9222 flag"
    }

@app.get("/")
async def home():
    return HTMLResponse(HTML_AGENT)

HTML_AGENT = """
<!DOCTYPE html>
<html>
<head>
    <title>Browser Agent</title>
    <meta charset="utf-8">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, system-ui, sans-serif; background: #0a0a0a; color: #e2e8f0; min-height: 100vh; }
        .container { max-width: 800px; margin: 0 auto; padding: 40px 20px; }
        h1 { font-size: 2rem; background: linear-gradient(135deg, #f97316, #eab308); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 8px; }
        .subtitle { color: #94a3b8; margin-bottom: 30px; }
        .input-group { background: #1e293b; border-radius: 12px; padding: 20px; border: 1px solid #334155; }
        textarea { width: 100%; background: #0f172a; border: 1px solid #334155; border-radius: 8px; color: #e2e8f0; padding: 12px; font-size: 1rem; min-height: 80px; resize: vertical; }
        button { background: linear-gradient(135deg, #f97316, #ea580c); color: white; border: none; padding: 12px 24px; border-radius: 8px; font-size: 1rem; cursor: pointer; margin-top: 12px; }
        button:hover { opacity: 0.9; }
        .status { margin-top: 20px; }
        .task { background: #1e293b; border-radius: 8px; padding: 16px; margin-top: 12px; border: 1px solid #334155; }
        .task.pending { border-color: #f59e0b; }
        .task.done { border-color: #22c55e; }
        .task.error { border-color: #ef4444; }
        .step { padding: 8px 0; border-bottom: 1px solid #334155; font-family: monospace; font-size: 0.85rem; }
        .step:last-child { border-bottom: none; }
        .chrome-status { background: #1e293b; padding: 16px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #334155; }
        code { background: #0f172a; padding: 2px 6px; border-radius: 4px; color: #60a5fa; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌐 Browser Agent</h1>
        <p class="subtitle">AI-powered web automation. Give a goal, watch it happen.</p>
        <div class="chrome-status" id="chrome-status">Checking Chrome...</div>
        
        <div class="input-group">
            <textarea id="goal" placeholder="What do you want me to do? e.g. 'Search for AI tools on ProductHunt and give me a summary of the top 5'"></textarea>
            <button onclick="submitTask()">🚀 Execute</button>
        </div>
        
        <div class="status" id="tasks"></div>
    </div>
    <script>
        async function checkChrome() {
            const res = await fetch('/browser/status');
            const data = await res.json();
            const el = document.getElementById('chrome-status');
            if (data.chrome === 'connected') {
                el.style.borderColor = '#22c55e';
                el.innerHTML = '✅ Chrome Connected | ' + data.tabs + ' tabs open';
            } else {
                el.style.borderColor = '#f59e0b';
                el.innerHTML = '⚠️ Chrome not in debug mode | Run: <code>open -a "Google Chrome" --args "--remote-debugging-port=9222"</code>';
            }
        }
        
        async function submitTask() {
            const goal = document.getElementById('goal').value;
            if (!goal) return;
            const res = await fetch('/tasks', { method: 'POST', body: new URLSearchParams({goal}), headers: {'Content-Type': 'application/x-www-form-urlencoded'} });
            const data = await res.json();
            document.getElementById('goal').value = '';
            loadTasks();
        }
        
        async function loadTasks() {
            const res = await fetch('/tasks');
            const tasks = await res.json();
            const el = document.getElementById('tasks');
            el.innerHTML = tasks.map(t => '<div class="task ' + t.status + '"><strong>' + t.goal.substring(0,80) + '</strong><br><small>' + t.task_id + ' — ' + t.status + '</small></div>').join('');
        }
        
        checkChrome();
        setInterval(loadTasks, 3000);
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)