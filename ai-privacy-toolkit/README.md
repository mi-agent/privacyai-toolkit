# AI Privacy Toolkit

> 🔒 Privacy-first AI tools that run 100% locally. Zero API costs, zero data leakage.

![Privacy](https://img.shields.io/badge/Privacy-100%25%20Local-green)
![AI](https://img.shields.io/badge/AI-Ollama%20powered-blue)
![Cost](https://img.shields.io/badge/Cost-$0-yellow)

## Why This Exists

Every privacy tool on the market sends your data to third-party servers. This toolkit uses local AI (Ollama) to process everything locally — your data never leaves your machine.

## Features

| Tool | What It Does | Use Case |
|------|-------------|----------|
| 🧹 **Privacy Cleaner** | Remove all PII from text | Share documents safely |
| 📝 **AI Summarizer** | Summarize in 3 lengths | Read faster, work less |
| 📄 **Smart Redactor** | Redact specific data types | Selective information removal |
| 📧 **Email Generator** | Generate professional emails | Speed up communication |
| 🔍 **Privacy Checker** | Score your text's privacy risk | Audit before sharing |
| ⚡ **Batch Processor** | Process 20 texts at once | Bulk operations |

## Quick Start

```bash
# 1. Make sure Ollama is running
ollama serve

# 2. Run the toolkit
bash run.sh

# 3. Open http://localhost:8000
```

## Tech Stack

- **Backend**: FastAPI + Python 3.9
- **AI**: Ollama (gemma4:e4b or any local model)
- **Frontend**: Vanilla HTML/JS (zero frontend deps)
- **Cost**: $0 total (uses local GPU/CPU)

## API

Full API docs at `http://localhost:8000/docs` or REST:

```bash
# Clean privacy
curl -X POST http://localhost:8000/api/privacy/clean \
  -F "text=Contact john@example.com or call 555-1234"

# Summarize
curl -X POST http://localhost:8000/api/summarize \
  -F "text=Your long text here..." \
  -F "length=medium"

# Privacy check
curl -X POST http://localhost:8000/api/privacy/check \
  -F "text=Text to analyze"
```

## Monetization Path

1. **Deploy to Render/Railway** (free tier) → Pro tier for heavy users
2. **White-label** to businesses with custom branding
3. **API access tiers** — free 100 req/day, paid unlimited
4. **Affiliate** — partner with VPN/privacy tools

## License

MIT — Free forever.