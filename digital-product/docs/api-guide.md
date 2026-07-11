# Complete API Documentation

## Base URL
```
http://localhost:8000/api/
```

## Authentication
No authentication required for local use.
For deployed versions: pass `X-API-Key` header.

---

## POST /api/privacy/clean
Remove all personally identifiable information from text.

**Request:**
```
POST /api/privacy/clean
Content-Type: multipart/form-data

text: "John Smith, email: john@example.com, SSN: 123-45-6789"
```

**Response:**
```json
{
  "cleaned": "[REDACTED] [EMAIL] [SSN]",
  "items_removed": 3,
  "privacy_score": "100%"
}
```

---

## POST /api/summarize
Summarize text using AI.

**Request:**
```
POST /api/summarize
Content-Type: multipart/form-data

text: "Long text to summarize..."
length: "medium"  # short | medium | long
```

**Response:**
```json
{
  "summary": "Concise summary of the input...",
  "word_count_original": 500,
  "word_count_summary": 45,
  "compression_ratio": "91%"
}
```

---

## POST /api/email/generate
Generate professional emails from context.

**Request:**
```
POST /api/email/generate
Content-Type: multipart/form-data

context: "Follow up with client about proposal from last week"
tone: "professional"  # professional | friendly | urgent | formal
```

**Response:**
```json
{
  "email": "Subject: Following Up - Project Proposal\n\nDear [Client Name],\n\nI hope...",
  "tone": "professional",
  "estimated_read_time": "30 seconds"
}
```

---

## POST /api/privacy/check
Analyze text for privacy risks.

**Request:**
```
POST /api/privacy/check
Content-Type: multipart/form-data

text: "User report: John Smith works at Acme Corp. Contact: john@acme.com"
```

**Response:**
```json
{
  "pii_found": [
    {"type": "name", "value": "John Smith", "severity": "high"},
    {"type": "email", "value": "john@acme.com", "severity": "high"},
    {"type": "company", "value": "Acme Corp", "severity": "medium"}
  ],
  "risk_score": "85%",
  "recommendations": [
    "Remove all 3 identified PII items",
    "Consider anonymizing company name if not essential"
  ]
}
```

---

## GET /api/health
Check system health.

**Response:**
```json
{
  "status": "online",
  "ollama": "connected",
  "models": ["gemma4:e4b", "gemma4:e2b"],
  "free_ai": true
}
```

---

## Rate Limits
- Free tier: 50 requests/day
- Pro: 5,000 requests/day
- Enterprise: Unlimited

---

## Error Codes
- `400` - Bad request (missing required fields)
- `408` - Request timeout (AI model took too long)
- `422` - Validation error (invalid input)
- `500` - Internal server error
- `503` - Ollama not running

---

## Examples

### cURL
```bash
# Clean PII
curl -X POST http://localhost:8000/api/privacy/clean \
  -F "text=My name is John and my SSN is 123-45-6789"

# Summarize
curl -X POST http://localhost:8000/api/summarize \
  -F "text=The quick brown fox..." \
  -F "length=short"
```

### Python
```python
import requests

# Clean PII
resp = requests.post("http://localhost:8000/api/privacy/clean", 
                     data={"text": "John's email: john@example.com"})
print(resp.json()["cleaned"])
```

### JavaScript
```javascript
const formData = new FormData();
formData.append("text", "Sensitive data here...");

const res = await fetch("http://localhost:8000/api/privacy/clean", {
  method: "POST",
  body: formData
});
const data = await res.json();
console.log(data.cleaned);
```