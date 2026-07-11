# Chrome Extension Setup

## Quick Install (Developer Mode)

1. Open Chrome → `chrome://extensions/`
2. Enable "Developer mode" (top right)
3. Click "Load unpacked"
4. Select the `~/Projects/chrome-extension/` folder
5. Click the Privacy Shield icon in toolbar
6. Start using!

## Features

- **Right-click menu** on any selected text
- **In-page floating button** for quick access
- **Popup** with all 4 tools
- **Auto-copy** results to clipboard

## Requirements

Privacy Toolkit must be running at `localhost:8000`:

```bash
cd ~/Projects/ai-privacy-toolkit
python3 -m uvicorn app.main:app --port 8000
```

## Publishing to Chrome Web Store

1. Package: `chrome://extensions/` → Pack extension
2. Create developer account: https://chrome.google.com/webstore/devconsole
3. Pay $5 one-time fee
4. Upload .crx package
5. Submit for review (usually 1-3 days)

## Revenue

- **Free tier**: 50 uses/day
- **Premium**: $3 one-time (remove ads, unlimited)
- **Enterprise**: White-label license $99

## Icon

Replace `icon.png` with a 128x128 PNG icon (shield + AI design)