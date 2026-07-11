# PrivacyAI Toolkit - Zero-API-Cost AI Business System

> **Build a profitable AI product with $0 in API costs.** Self-hosted, privacy-first, runs entirely on your hardware.

## 🎯 What Is This?

A complete, production-ready AI toolkit that you can deploy in 60 seconds and monetize immediately. No OpenAI keys, no monthly bills, no data sent to third parties.

## ✨ What's Included

### 6 AI Tools (All Free, All Private)
- 🧹 **Privacy Cleaner** — Remove names, emails, phones, SSNs, addresses from any text in one click
- 📝 **AI Summarizer** — Short, medium, or detailed summaries at 3 quality levels  
- 📧 **Email Generator** — Professional emails from simple context (4 tones)
- 🔍 **Privacy Checker** — Scan any text for privacy risks with severity scoring
- 🛡️ **Smart Redactor** — Selectively redact by data type
- 🔄 **Batch Processor** — Process up to 20 texts at once

### Full Tech Stack
```
Frontend:  React-ready SPA + Chrome Extension
Backend:   FastAPI + Uvicorn
AI Engine: Ollama (llama3.2, gemma4, mistral — your choice)
Storage:   SQLite (logs) + file system
Hosting:   Docker, Render, Railway, VPS — any platform
Cost:      $0/month forever
```

## 🚀 Quick Start

### Option 1: One-Command Deploy
```bash
# Install Ollama (if not already)
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2

# Run the toolkit
cd ai-privacy-toolkit
pip install -r requirements.txt
uvicorn app.main:app --port 8000

# Open http://localhost:8000
```

### Option 2: Docker
```bash
docker run -p 8000:8000 \
  -e OLLAMA_URL=http://host.docker.internal:11434 \
  privacyai/toolkit
```

## 💰 How to Make Money

| Strategy | Revenue Potential | Effort |
|----------|------------------|--------|
| Self-host for businesses | $99/one-time | Medium |
| Resell as "Pro" SaaS | $9/mo per user | Low |
| White-label for enterprises | $299-999/project | High |
| Chrome extension premium | $3 one-time | Low |
| Commercial license resale | $29/license | Low |
| Affiliate links | Passive | Minimal |

## 📁 Project Structure

```
ai-privacy-toolkit/     ← FastAPI backend + landing pages
browser-agent/           ← Chrome DevTools Protocol automation
chrome-extension/        ← Browser extension (Chrome Web Store ready)
digital-product/         ← Gumroad-ready product bundle
ai-tools-guide/          ← Content/marketing site (GitHub Pages)
dashboard.py             ← Unified monitoring dashboard
control.sh               ← Service management script
```

## 🔧 Configuration

### Environment Variables
```bash
OLLAMA_URL=http://localhost:11434          # Your Ollama instance
OLLAMA_MODEL=gemma4:e4b                    # Default model
PORT=8000                                  # Server port
LOG_LEVEL=info
```

### Switching AI Models
```bash
# Any Ollama model works
ollama pull llama3.2
ollama pull mistral
ollama pull gemma4:e4b

# Set via env
export OLLAMA_MODEL=llama3.2
```

## 🌐 Deployment Options

### Render (Free Tier)
1. Fork this repo to GitHub
2. Sign up at [render.com](https://render.com)
3. Connect GitHub → New Web Service → Select repo
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Railway
1. Push to GitHub
2. Connect at [railway.app](https://railway.app)
3. Railway auto-detects FastAPI

### VPS (Ubuntu/Debian)
```bash
# SSH into your VPS
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2
pip install fastapi uvicorn httpx python-multipart
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📊 Dashboard

Monitor all services from one dashboard:
```bash
python ~/Projects/dashboard.py
# Opens http://localhost:8888
```

Shows: Privacy Toolkit health, Browser Agent status, Ollama models, uptime.

## 📦 Chrome Extension

1. Open `chrome://extensions/`
2. Enable Developer Mode
3. Load Unpacked → select `chrome-extension/`
4. Click the 🛡️ icon in toolbar

Features: Right-click context menu, in-page floating button, popup with all tools.

## 📄 API Reference

See `digital-product/docs/api-guide.md` for full API docs.

Key endpoints:
- `POST /api/privacy/clean` — Remove PII
- `POST /api/summarize` — Summarize text  
- `POST /api/email/generate` — Generate emails
- `POST /api/privacy/check` — Check privacy risks
- `GET /api/health` — Health check

## 🛡️ Privacy Guarantees

- **Zero data collection** — Nothing sent to any server except your own Ollama
- **No telemetry** — No analytics, no tracking, no cookies
- **Local processing** — All AI inference runs on YOUR hardware
- **Open source** — Audit the code yourself
- **No API keys needed** — No vendor lock-in

## 📄 License

- **Personal/Non-commercial**: MIT License (free)
- **Commercial use**: Purchase commercial license (see `digital-product/COMMERCIAL_LICENSE.md`)

## 🙏 Credits

Built with [Ollama](https://ollama.com), [FastAPI](https://fastapi.tiangolo.com), and a lot of ☕

---

*Version 1.0 | Built with zero external API costs | 2025*