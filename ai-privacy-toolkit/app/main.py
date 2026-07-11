"""
AI Privacy Toolkit - Main Application
Using Ollama for free local AI processing
"""
import os
import json
import asyncio
import httpx
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI(title="AI Privacy Toolkit", version="1.0.0")

# Config
STATIC_DIR = Path(__file__).parent / "app" / "static"
TEMPLATES_DIR = Path(__file__).parent / "app" / "templates"
STATIC_DIR.mkdir(parents=True, exist_ok=True)
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma4:e4b")

# ============ Health & Config ============

LANDING_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PrivacyAI Toolkit - Free Privacy-First AI Tools</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#030712;--surface:#0f172a;--border:#1e293b;--text:#f1f5f9;--muted:#94a3b8;--accent:#6366f1;--accent2:#8b5cf6;--green:#22c55e;--yellow:#f59e0b;--red:#ef4444}
body{font-family:-apple-system,system-ui,sans-serif;background:var(--bg);color:var(--text);line-height:1.7}
.wrap{max-width:860px;margin:0 auto;padding:0 20px}
nav{display:flex;justify-content:space-between;align-items:center;padding:24px 0;border-bottom:1px solid var(--border);margin-bottom:60px}
.logo{font-size:1.3rem;font-weight:700;background:linear-gradient(135deg,var(--accent),var(--accent2));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
nav a{color:var(--text);text-decoration:none;font-size:0.9rem;padding:8px 16px;border-radius:8px}
nav .cta{background:var(--accent)}
.hero{text-align:center;padding:60px 0 80px}
.hero h1{font-size:3rem;font-weight:800;line-height:1.1;margin-bottom:20px}
.hero h1 .g{background:linear-gradient(135deg,var(--accent),#a855f7,#ec4899);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.hero p{font-size:1.2rem;color:var(--muted);max-width:560px;margin:0 auto 30px}
.hero .btns{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}
.btn{padding:14px 28px;border-radius:10px;text-decoration:none;font-weight:600;transition:transform .2s,box-shadow .2s}
.btn-p{background:linear-gradient(135deg,var(--accent),var(--accent2));color:white;box-shadow:0 4px 20px rgba(99,102,241,.3)}
.btn-p:hover{transform:translateY(-2px);box-shadow:0 6px 30px rgba(99,102,241,.4)}
.btn-s{background:var(--surface);border:1px solid var(--border);color:var(--text)}
.features{padding:40px 0}
.features h2{text-align:center;font-size:2rem;margin-bottom:40px}
.feat-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}
.feat{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:24px}
.feat h4{font-size:1rem;margin-bottom:8px}
.feat p{color:var(--muted);font-size:0.9rem}
.stats{background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:40px;margin:40px 0;display:flex;justify-content:space-around;text-align:center;flex-wrap:wrap;gap:20px}
.stats .s{font-size:2.5rem;font-weight:800;background:linear-gradient(135deg,var(--accent),var(--accent2));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.stats .l{color:var(--muted);font-size:0.9rem}
.pricing{padding:40px 0}
.pricing h2{text-align:center;font-size:2rem;margin-bottom:40px}
.p-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.plan{background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:32px 24px;position:relative}
.plan.f{box-shadow:0 0 40px rgba(99,102,241,.12)}
.plan .badge{position:absolute;top:-12px;left:50%;transform:translateX(-50%);background:var(--accent);color:white;font-size:.75rem;padding:4px 16px;border-radius:99px;white-space:nowrap}
.plan h3{font-size:.85rem;color:var(--muted);text-transform:uppercase;letter-spacing:.05em;margin-bottom:8px}
.plan .price{font-size:2.5rem;font-weight:800;margin-bottom:4px}
.plan .price span{font-size:1rem;color:var(--muted);font-weight:400}
.plan .per{color:var(--muted);font-size:.9rem;margin-bottom:24px}
.plan ul{list-style:none;margin-bottom:24px}
.plan ul li{padding:8px 0;font-size:.9rem;color:var(--muted);border-bottom:1px solid var(--border)}
.plan ul li:last-child{border-bottom:none}
.plan ul li::before{content:"✓ ";color:var(--green)}
.plan .gbtn{display:block;text-align:center;background:var(--accent);color:white;padding:12px;border-radius:10px;text-decoration:none;font-weight:600}
.plan .gbtn:hover{opacity:.9}
.plan.f .gbtn{background:linear-gradient(135deg,var(--accent),var(--accent2))}
.plan.free{border-color:var(--green)}
.plan.free h3{color:var(--green)}
.plan.free .gbtn{background:var(--surface);border:1px solid var(--green);color:var(--green)}
.how{background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:32px;margin:40px 0}
.how h3{font-size:1.3rem;margin-bottom:16px}
.how pre{background:#030712;padding:16px;border-radius:10px;font-family:monospace;font-size:.85rem;color:var(--green);margin:8px 0;overflow-x:auto}
footer{border-top:1px solid var(--border);padding:32px 0;text-align:center;color:var(--muted);font-size:.85rem}
footer a{color:var(--accent);text-decoration:none}
@media(max-width:640px){
.hero h1{font-size:2rem}
.pricing-grid,.feat-grid{grid-template-columns:1fr}
.stats{flex-direction:column}
}
</style>
</head>
<body>
<div class="wrap">
<nav>
<div class="logo">PrivacyAI Toolkit</div>
<div>
<a href="/tools">Tools</a>
<a href="/pricing">Pricing</a>
<a href="/tools" class="cta">Try Free</a>
</div>
</nav>

<section class="hero">
<h1>AI That <span class="g">Never Sees</span><br>Your Private Data</h1>
<p>Privacy-first AI tools that run entirely on your server. No API keys, no data sent to third parties, no subscriptions. Just privacy, guaranteed by architecture.</p>
<div class="btns">
<a href="/tools" class="btn btn-p">Try Free Tools</a>
<a href="/pricing" class="btn btn-s">View Pricing</a>
</div>
</section>

<section class="features">
<h2>6 Tools, 100% Private</h2>
<div class="feat-grid">
<div class="feat"><h4>Privacy Cleaner</h4><p>Remove all PII from documents instantly. Names, emails, phones, addresses, SSNs gone in one click.</p></div>
<div class="feat"><h4>AI Summarizer</h4><p>Summarize any text to short, medium, or long form. Perfect for processing reports and long documents.</p></div>
<div class="feat"><h4>Smart Redactor</h4><p>Selectively redact specific data types. Remove emails only, or names only, or financial data.</p></div>
<div class="feat"><h4>Email Generator</h4><p>Generate professional emails from simple context. Multiple tones: professional, friendly, urgent.</p></div>
<div class="feat"><h4>Privacy Checker</h4><p>Scan any text for privacy risks and get a score with specific recommendations.</p></div>
<div class="feat"><h4>Batch Processor</h4><p>Process up to 20 texts at once. Bulk clean, summarize, or analyze documents.</p></div>
</div>
</section>

<div class="stats">
<div><div class="s">$0</div><div class="l">API costs per month</div></div>
<div><div class="s">100%</div><div class="l">Data never leaves your server</div></div>
<div><div class="s">6</div><div class="l">Powerful AI tools</div></div>
</div>

<section class="how">
<h3>Deploy in 60 Seconds</h3>
<p style="color:var(--muted);margin-bottom:12px;">One Docker command to self-host everything.</p>
<pre>$ docker run -p 8000:8000 \\
  -e OLLAMA_URL=http://your-ollama:11434 \\
  privacyai/toolkit</pre>
<p style="color:var(--muted);font-size:.85rem;margin-top:8px;">Available on Docker Hub, GitHub Container Registry, and Render</p>
</section>

<section class="pricing" id="pricing">
<h2>Simple Pricing</h2>
<div class="p-grid">
<div class="plan free">
<h3>Free</h3>
<div class="price">$0 <span>/mo</span></div>
<div class="per">Forever free</div>
<ul>
<li>50 requests/day</li>
<li>All 6 tools</li>
<li>Self-hosted only</li>
<li>Community support</li>
</ul>
<a href="https://github.com" class="gbtn">Deploy Free</a>
</div>
<div class="plan f">
<span class="badge">MOST POPULAR</span>
<h3>Pro</h3>
<div class="price">$9 <span>/mo</span></div>
<div class="per">or $89/year (save 17%)</div>
<ul>
<li>5,000 requests/day</li>
<li>Priority AI speed</li>
<li>All 6 tools</li>
<li>API access</li>
<li>Email support</li>
<li>Usage dashboard</li>
</ul>
<a href="#" class="gbtn" onclick="alert('Coming soon! Join waitlist: privacyai@example.com')">Join Waitlist</a>
</div>
<div class="plan">
<h3>Team</h3>
<div class="price">$29 <span>/mo</span></div>
<div class="per">per team (up to 10 users)</div>
<ul>
<li>Unlimited requests</li>
<li>API access</li>
<li>Team management</li>
<li>SLA guarantee</li>
<li>Dedicated support</li>
</ul>
<a href="#" class="gbtn" onclick="alert('Coming soon! Contact: privacyai@example.com')">Contact Sales</a>
</div>
</div>
</section>

<footer>
<p>PrivacyAI Toolkit &middot; <a href="https://github.com">GitHub</a> &middot; Open Source</p>
<p style="margin-top:8px;">Built with Ollama &middot; Zero API costs &middot; 100% private by design</p>
</footer>
</div>
</body>
</html>
"""

TOOLS_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PrivacyAI - Free Tools</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#030712;--surface:#0f172a;--border:#1e293b;--text:#f1f5f9;--muted:#94a3b8;--accent:#6366f1;--accent2:#8b5cf6;--green:#22c55e;--red:#ef4444;--yellow:#f59e0b}
body{font-family:-apple-system,system-ui,sans-serif;background:var(--bg);color:var(--text);line-height:1.7}
.wrap{max-width:860px;margin:0 auto;padding:0 20px}
nav{display:flex;justify-content:space-between;align-items:center;padding:20px 0;border-bottom:1px solid var(--border);margin-bottom:40px}
.logo{font-size:1.2rem;font-weight:700;background:linear-gradient(135deg,var(--accent),var(--accent2));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
nav a{color:var(--text);text-decoration:none;font-size:.9rem}
nav a:hover{color:var(--accent)}
.nav-status{font-size:.8rem;color:var(--muted)}
.nav-status span{color:var(--green)}
h1{font-size:1.8rem;margin-bottom:8px}
.subtitle{color:var(--muted);margin-bottom:32px;font-size:.95rem}
.tabs{display:flex;gap:8px;margin-bottom:24px;flex-wrap:wrap}
.tab{padding:10px 20px;border-radius:8px;border:1px solid var(--border);background:var(--surface);cursor:pointer;font-size:.9rem;color:var(--muted);transition:all .2s}
.tab:hover{border-color:var(--accent)}
.tab.active{background:var(--accent);border-color:var(--accent);color:white}
.tool-panel{display:none}
.tool-panel.active{display:block}
.input-area{margin-bottom:16px}
textarea{width:100%;height:120px;background:var(--surface);border:1px solid var(--border);border-radius:10px;color:var(--text);padding:14px;font-size:.9rem;resize:vertical;font-family:inherit;line-height:1.6}
textarea:focus{outline:none;border-color:var(--accent)}
.btn-row{display:flex;gap:10px;margin-bottom:16px;flex-wrap:wrap}
button{padding:10px 20px;border-radius:8px;border:none;font-size:.9rem;font-weight:600;cursor:pointer;transition:opacity .2s}
.btn-primary{background:var(--accent);color:white}
.btn-primary:hover{opacity:.9}
.btn-secondary{background:var(--surface);color:var(--text);border:1px solid var(--border)}
.result-area{margin-top:20px}
.result{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:16px;min-height:80px;font-size:.9rem;white-space:pre-wrap;word-break:break-word;max-height:400px;overflow-y:auto}
.result.error{border-color:var(--red);color:var(--red)}
.result.success{border-color:var(--green);color:var(--green)}
.result-label{font-size:.8rem;color:var(--muted);margin-bottom:8px}
.copy-btn{float:right;font-size:.75rem;padding:4px 10px;background:var(--border);color:var(--muted);border:none;border-radius:4px;cursor:pointer}
.copy-btn:hover{color:var(--text)}
footer{border-top:1px solid var(--border);padding:24px 0;text-align:center;color:var(--muted);font-size:.8rem;margin-top:60px}
footer a{color:var(--accent);text-decoration:none}
</style>
</head>
<body>
<div class="wrap">
<nav>
<div class="logo">PrivacyAI</div>
<div>
<span class="nav-status">AI: <span id="aiStatus">Checking...</span></span>
<a href="/" style="margin-left:16px">Home</a>
<a href="/pricing" style="margin-left:12px">Pricing</a>
</div>
</nav>

<h1>Free Privacy AI Tools</h1>
<p class="subtitle">All processing happens on your server. No data sent anywhere.</p>

<div class="tabs">
<button class="tab active" data-panel="clean">Privacy Cleaner</button>
<button class="tab" data-panel="summarize">Summarizer</button>
<button class="tab" data-panel="email">Email Generator</button>
<button class="tab" data-panel="check">Privacy Checker</button>
</div>

<!-- Clean -->
<div class="tool-panel active" id="panel-clean">
<p style="color:var(--muted);font-size:.9rem;margin-bottom:12px;">Removes all personally identifiable information from text. Names, emails, phone numbers, addresses, SSNs, IPs.</p>
<div class="input-area"><textarea id="clean-input" placeholder="Paste text containing private information...&#10;&#10;Example: John Smith lives at 123 Main St, email: john.smith@gmail.com, phone: 555-123-4567"></textarea></div>
<div class="btn-row">
<button class="btn-primary" onclick="runClean()">Clean PII</button>
<button class="btn-secondary" onclick="document.getElementById('clean-input').value='';document.getElementById('clean-output').textContent=''">Clear</button>
</div>
<div class="result-area">
<div class="result-label">Cleaned Result <button class="copy-btn" onclick="copyResult('clean-output')">Copy</button></div>
<div class="result" id="clean-output">Results appear here...</div>
</div>
</div>

<!-- Summarize -->
<div class="tool-panel" id="panel-summarize">
<p style="color:var(--muted);font-size:.9rem;margin-bottom:12px;">Summarize any text into short, medium, or detailed summaries using AI.</p>
<div class="input-area"><textarea id="sum-input" placeholder="Paste text to summarize..."></textarea></div>
<div class="btn-row">
<button class="btn-primary" onclick="runSummarize()">Summarize</button>
<select id="sum-length" style="padding:10px;border-radius:8px;border:1px solid var(--border);background:var(--surface);color:var(--text)">
<option value="short">Short summary</option>
<option value="medium" selected>Medium summary</option>
<option value="long">Detailed summary</option>
</select>
</div>
<div class="result-area">
<div class="result-label">Summary <button class="copy-btn" onclick="copyResult('sum-output')">Copy</button></div>
<div class="result" id="sum-output">Results appear here...</div>
</div>
</div>

<!-- Email -->
<div class="tool-panel" id="panel-email">
<p style="color:var(--muted);font-size:.9rem;margin-bottom:12px;">Generate professional emails from simple context.</p>
<div class="input-area"><textarea id="email-input" placeholder="Describe the email you need...&#10;&#10;Example: Follow up with client about proposal, friendly tone, mention the meeting next Tuesday"></textarea></div>
<div class="btn-row">
<button class="btn-primary" onclick="runEmail()">Generate Email</button>
<select id="email-tone" style="padding:10px;border-radius:8px;border:1px solid var(--border);background:var(--surface);color:var(--text)">
<option value="professional">Professional</option>
<option value="friendly">Friendly</option>
<option value="urgent">Urgent</option>
<option value="formal">Formal</option>
</select>
</div>
<div class="result-area">
<div class="result-label">Generated Email <button class="copy-btn" onclick="copyResult('email-output')">Copy</button></div>
<div class="result" id="email-output">Results appear here...</div>
</div>
</div>

<!-- Check -->
<div class="tool-panel" id="panel-check">
<p style="color:var(--muted);font-size:.9rem;margin-bottom:12px;">Scan text for privacy risks and get a detailed analysis.</p>
<div class="input-area"><textarea id="check-input" placeholder="Paste text to check for privacy risks..."></textarea></div>
<div class="btn-row">
<button class="btn-primary" onclick="runCheck()">Check Privacy</button>
</div>
<div class="result-area">
<div class="result-label">Analysis <button class="copy-btn" onclick="copyResult('check-output')">Copy</button></div>
<div class="result" id="check-output">Results appear here...</div>
</div>
</div>

<footer>
<p>PrivacyAI Toolkit &middot; <a href="/">Home</a> &middot; <a href="/pricing">Pricing</a></p>
</footer>
</div>

<script>
const API = '';

// Check AI status
(async()=>{
  try{
    const r = await fetch('/api/health');
    const d = await r.json();
    document.getElementById('aiStatus').textContent = d.ollama==='connected' ? 'Online' : 'Offline';
    document.getElementById('aiStatus').style.color = d.ollama==='connected' ? '#22c55e' : '#ef4444';
  }catch{
    document.getElementById('aiStatus').textContent = 'Offline';
    document.getElementById('aiStatus').style.color = '#ef4444';
  }
})();

// Tabs
document.querySelectorAll('.tab').forEach(t=>{
  t.onclick=()=>{
    document.querySelectorAll('.tab').forEach(x=>x.classList.remove('active'));
    document.querySelectorAll('.tool-panel').forEach(x=>x.classList.remove('active'));
    t.classList.add('active');
    document.getElementById('panel-'+t.dataset.panel).classList.add('active');
  };
});

async function apiCall(endpoint, formData) {
  const r = await fetch(endpoint, {method:'POST', body:formData});
  if(!r.ok) throw new Error('API error: '+r.status);
  return r.json();
}

async function runClean(){
  const inp=document.getElementById('clean-input').value;
  if(!inp.trim()){alert('Enter text first');return;}
  const el=document.getElementById('clean-output');
  el.textContent='Processing...';el.className='result';
  try{
    const fd=new FormData();fd.append('text',inp);
    const d=await apiCall('/api/privacy/clean',fd);
    el.textContent=d.cleaned||JSON.stringify(d);
    el.className='result success';
  }catch(e){el.textContent='Error: '+e.message;el.className='result error';}
}

async function runSummarize(){
  const inp=document.getElementById('sum-input').value;
  if(!inp.trim()){alert('Enter text first');return;}
  const el=document.getElementById('sum-output');
  el.textContent='Processing...';el.className='result';
  try{
    const fd=new FormData();fd.append('text',inp);fd.append('length',document.getElementById('sum-length').value);
    const d=await apiCall('/api/summarize',fd);
    el.textContent=d.summary||JSON.stringify(d);
    el.className='result success';
  }catch(e){el.textContent='Error: '+e.message;el.className='result error';}
}

async function runEmail(){
  const inp=document.getElementById('email-input').value;
  if(!inp.trim()){alert('Enter context first');return;}
  const el=document.getElementById('email-output');
  el.textContent='Generating...';el.className='result';
  try{
    const fd=new FormData();fd.append('context',inp);fd.append('tone',document.getElementById('email-tone').value);
    const d=await apiCall('/api/email/generate',fd);
    el.textContent=d.email||JSON.stringify(d);
    el.className='result success';
  }catch(e){el.textContent='Error: '+e.message;el.className='result error';}
}

async function runCheck(){
  const inp=document.getElementById('check-input').value;
  if(!inp.trim()){alert('Enter text first');return;}
  const el=document.getElementById('check-output');
  el.textContent='Analyzing...';el.className='result';
  try{
    const fd=new FormData();fd.append('text',inp);
    const d=await apiCall('/api/privacy/check',fd);
    const items=d.pii_found||d.analysis||JSON.stringify(d,null,2);
    el.textContent=typeof items==='string'?items:JSON.stringify(items,null,2);
    el.className='result success';
  }catch(e){el.textContent='Error: '+e.message;el.className='result error';}
}

function copyResult(id){
  const text=document.getElementById(id).textContent;
  navigator.clipboard.writeText(text);
  const btn=document.querySelector(`#${id}`).previousElementSibling.querySelector('.copy-btn');
  btn.textContent='Copied!';btn.style.color='#22c55e';
  setTimeout(()=>{btn.textContent='Copy';btn.style.color='';},1500);
}
</script>
</body>
</html>
"""

@app.get("/")
async def landing():
    return HTMLResponse(LANDING_HTML)

@app.get("/tools")
async def tools():
    return HTMLResponse(TOOLS_HTML)

@app.get("/pricing")
async def pricing():
    return HTMLResponse(LANDING_HTML.split('<section class="pricing"')[1].join('<section class="pricing"'))

@app.get("/api/health")
async def health():
    """Check Ollama status"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(f"{OLLAMA_URL}/api/tags")
            models = resp.json().get("models", []) if resp.status_code == 200 else []
            return {
                "status": "online",
                "ollama": "connected",
                "models": [m["name"] for m in models],
                "free_ai": True
            }
    except Exception as e:
        return {
            "status": "degraded",
            "ollama": "disconnected",
            "error": str(e),
            "free_ai": True
        }

@app.get("/api/config")
async def config():
    return {
        "model": OLLAMA_MODEL,
        "ollama_url": OLLAMA_URL,
        "free_mode": True,
        "features": [
            "privacy-cleaner",
            "ai-summarizer", 
            "text-redactor",
            "email-generator",
            "content-translator"
        ]
    }

# ============ AI Core (Ollama) ============

async def ollama_chat(prompt: str, system: str = "", model: str = None) -> str:
    """Call Ollama for free AI inference"""
    model = model or OLLAMA_MODEL
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.7, "num_predict": 2048}
    }
    if system:
        payload["system"] = system
    
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(
                f"{OLLAMA_URL}/api/generate",
                json=payload
            )
            if resp.status_code == 200:
                return resp.json().get("response", "")
            raise HTTPException(status_code=500, detail=f"Ollama error: {resp.text}")
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="AI timeout, try smaller input")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI error: {str(e)}")

# ============ Feature: Privacy Cleaner ============

@app.post("/api/privacy/clean")
async def clean_privacy(text: str = Form(...)):
    """Remove PII, emails, phones, IPs from text using AI"""
    system = """You are a privacy expert. Remove ALL personally identifiable information from the text:
- Names (real and usernames)
- Email addresses
- Phone numbers  
- Physical addresses
- IP addresses
- Account numbers, SSN-like numbers
- Dates of birth
Return ONLY the cleaned text, nothing else. Preserve the meaning and structure."""
    
    result = await ollama_chat(text, system=system)
    return {"cleaned": result, "original_length": len(text)}

# ============ Feature: AI Summarizer ============

@app.post("/api/summarize")
async def summarize(text: str = Form(...), length: str = Form("medium")):
    """Summarize text using AI"""
    length_map = {
        "short": "2-3 sentences",
        "medium": "1 paragraph", 
        "long": "2-3 paragraphs"
    }
    system = f"Summarize the following text in {length_map.get(length, '1 paragraph')}. Be clear and factual."
    
    result = await ollama_chat(text, system=system)
    return {"summary": result, "mode": length}

# ============ Feature: Text Redactor ============

@app.post("/api/redact")
async def redact(text: str = Form(...), what: str = Form("all")):
    """Redact specific categories from text"""
    categories = {
        "all": "everything identifiable",
        "emails": "email addresses only",
        "phones": "phone numbers only",
        "names": "names and usernames only",
        "addresses": "physical addresses only",
        "financial": "account numbers, card numbers, monetary values"
    }
    system = f"Redact {categories.get(what, 'all')} from the text. Replace them with [REDACTED]. Keep formatting."
    
    result = await ollama_chat(text, system=system)
    return {"redacted": result, "category": what}

# ============ Feature: Email Generator ============

@app.post("/api/email/generate")
async def generate_email(
    context: str = Form(...),
    tone: str = Form("professional"),
    action: str = Form("inform")
):
    """Generate professional emails using AI"""
    system = f"""Write a {tone} email with the goal to {action}. 
Context: {context}
Format:
- Subject line
- Body (clear, concise, action-oriented)
Sign it professionally."""
    
    result = await ollama_chat(context, system=system)
    return {"email": result, "tone": tone, "action": action}

# ============ Feature: Privacy Checker ============

@app.post("/api/privacy/check")
async def check_privacy(text: str = Form(...)):
    """Analyze what privacy risks exist in text"""
    system = """Analyze this text for privacy risks. Identify ALL potential PII:
- Emails, phones, addresses
- Names and usernames
- IP addresses, URLs with tokens
- Account numbers
- Any other identifying data

Return a JSON with: {"risks": [{"type": "...", "found": "...", "severity": "high/medium/low"}], "score": 0-100, "recommendation": "..."}"""

    result = await ollama_chat(text, system=system)
    
    # Try to parse as JSON
    try:
        # Try to extract JSON from response
        import re
        json_match = re.search(r'\{.*\}', result, re.DOTALL)
        if json_match:
            risks = json.loads(json_match.group())
        else:
            risks = {"raw_analysis": result}
    except:
        risks = {"raw_analysis": result}
    
    return {"analysis": risks, "original_length": len(text)}

# ============ Feature: Batch Processing ============

@app.post("/api/batch/process")
async def batch_process(
    texts: list[str] = Form(...),
    operation: str = Form("summarize")
):
    """Process multiple texts"""
    results = []
    for i, text in enumerate(texts[:20]):  # Max 20
        try:
            if operation == "summarize":
                result = await ollama_chat(f"Summarize in 1 sentence: {text[:2000]}")
            elif operation == "clean":
                result = await ollama_chat(
                    text,
                    system="Remove all PII. Return only cleaned text."
                )
            else:
                result = await ollama_chat(text[:2000])
            results.append({"index": i, "result": result, "success": True})
        except Exception as e:
            results.append({"index": i, "error": str(e), "success": False})
    
    return {"results": results, "total": len(texts)}

# ============ Frontend ============

@app.get("/")
async def home():
    """Serve the main page"""
    html_path = TEMPLATES_DIR / "index.html"
    if html_path.exists():
        return HTMLResponse(html_path.read_text())
    return HTMLResponse(HTML_FALLBACK)

@app.get("/tools/{tool}")
async def tool_page(tool: str):
    """Dynamic tool pages"""
    html_path = TEMPLATES_DIR / f"{tool}.html"
    if html_path.exists():
        return HTMLResponse(html_path.read_text())
    raise HTTPException(404, "Tool not found")

# ============ Startup ============

HTML_FALLBACK = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Privacy Toolkit</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, system-ui, sans-serif; background: #0f172a; color: #e2e8f0; min-height: 100vh; }
        .container { max-width: 900px; margin: 0 auto; padding: 40px 20px; }
        h1 { font-size: 2.5rem; background: linear-gradient(135deg, #60a5fa, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 8px; }
        .subtitle { color: #94a3b8; margin-bottom: 40px; }
        .tools-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 16px; }
        .tool-card { background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 24px; cursor: pointer; transition: all 0.2s; }
        .tool-card:hover { border-color: #60a5fa; transform: translateY(-2px); }
        .tool-card h3 { color: #60a5fa; margin-bottom: 8px; }
        .tool-card p { font-size: 0.875rem; color: #94a3b8; line-height: 1.5; }
        .badge { display: inline-block; background: #065f46; color: #6ee7b7; font-size: 0.7rem; padding: 2px 8px; border-radius: 99px; margin-left: 8px; }
        .status { background: #1e293b; padding: 16px; border-radius: 8px; margin-bottom: 30px; border: 1px solid #334155; }
        .status.online { border-color: #22c55e; }
        .status.offline { border-color: #ef4444; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔒 AI Privacy Toolkit</h1>
        <p class="subtitle">Free AI-powered privacy tools. Your data never leaves your server.</p>
        <div id="status" class="status"></div>
        <div class="tools-grid">
            <div class="tool-card" onclick="showTool('clean')">
                <h3>🧹 Privacy Cleaner <span class="badge">POPULAR</span></h3>
                <p>Remove all PII from text using AI — names, emails, phones, addresses in one click.</p>
            </div>
            <div class="tool-card" onclick="showTool('summarize')">
                <h3>📝 AI Summarizer</h3>
                <p>Summarize any text to short, medium, or long length with one click.</p>
            </div>
            <div class="tool-card" onclick="showTool('redact')">
                <h3>📄 Smart Redactor</h3>
                <p>Redact specific categories — emails only, names only, financial data, etc.</p>
            </div>
            <div class="tool-card" onclick="showTool('email')">
                <h3>📧 Email Generator</h3>
                <p>Generate professional emails from context — professional, friendly, urgent tones.</p>
            </div>
            <div class="tool-card" onclick="showTool('check')">
                <h3>🔍 Privacy Checker <span class="badge">NEW</span></h3>
                <p>Scan text for privacy risks and get a score with recommendations.</p>
            </div>
            <div class="tool-card" onclick="showTool('batch')">
                <h3>⚡ Batch Processor</h3>
                <p>Process up to 20 texts at once — summarize or clean in bulk.</p>
            </div>
        </div>
        <div id="tool-area" style="margin-top:30px;"></div>
    </div>
    <script>
        async function checkStatus() {
            const res = await fetch('/api/health');
            const data = await res.json();
            const status = document.getElementById('status');
            if (data.ollama === 'connected') {
                status.className = 'status online';
                status.innerHTML = '✅ AI Engine Online | Model: ' + data.models.join(', ');
            } else {
                status.className = 'status offline';
                status.innerHTML = '⚠️ AI Engine Offline | ' + (data.error || '');
            }
        }
        function showTool(name) {
            document.getElementById('tool-area').innerHTML = '<p style="color:#94a3b8">Loading tool: ' + name + '...</p>';
        }
        checkStatus();
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)