// Content script - runs on every page
// Provides in-page privacy tools

(function() {
  // Inject floating button
  const btn = document.createElement('div');
  btn.id = 'privacy-shield-btn';
  btn.innerHTML = '🛡️';
  btn.title = 'Privacy Shield - Select text first';
  btn.style.cssText = `
    position: fixed; bottom: 20px; right: 20px; z-index: 999999;
    width: 48px; height: 48px; border-radius: 50%;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white; font-size: 20px; display: flex; align-items: center; justify-content: center;
    cursor: pointer; box-shadow: 0 4px 20px rgba(99,102,241,0.4);
    user-select: none; transition: transform 0.2s;
  `;
  document.body.appendChild(btn);
  
  btn.addEventListener('click', () => {
    const selection = window.getSelection().toString().trim();
    if (!selection) {
      alert('Privacy Shield: Select some text first, then click this button.');
      return;
    }
    
    // Show mini panel
    const panel = document.createElement('div');
    panel.style.cssText = `
      position: fixed; bottom: 80px; right: 20px; z-index: 999999;
      background: #0f172a; border: 1px solid #334155; border-radius: 12px;
      padding: 16px; min-width: 280px; color: #f1f5f9; font-family: system-ui;
      box-shadow: 0 8px 40px rgba(0,0,0,0.5);
    `;
    panel.innerHTML = `
      <div style="font-weight:600;margin-bottom:12px;">🛡️ Privacy Shield</div>
      <div style="font-size:0.8rem;color:#94a3af;margin-bottom:12px;max-height:80px;overflow:hidden;">
        Selected: ${selection.substring(0, 100)}${selection.length > 100 ? '...' : ''}
      </div>
      <div style="display:flex;flex-direction:column;gap:8px;">
        <button id="ps-clean" style="background:#6366f1;color:white;border:none;padding:10px;border-radius:8px;cursor:pointer;font-size:0.85rem;">
          🧹 Clean PII
        </button>
        <button id="ps-check" style="background:#0f172a;color:#f1f5f9;border:1px solid #334155;padding:10px;border-radius:8px;cursor:pointer;font-size:0.85rem;">
          🔍 Check Privacy
        </button>
        <button id="ps-summarize" style="background:#0f172a;color:#f1f5f9;border:1px solid #334155;padding:10px;border-radius:8px;cursor:pointer;font-size:0.85rem;">
          📝 Summarize
        </button>
      </div>
      <div id="ps-result" style="margin-top:12px;font-size:0.8rem;color:#22c55e;min-height:20px;"></div>
    `;
    
    document.body.appendChild(panel);
    
    const closePanel = () => { if (panel.parentNode) panel.remove(); };
    btn.addEventListener('click', closePanel, { once: true });
    setTimeout(closePanel, 10000);
    
    const process = (endpoint, field, btnId) => {
      const btn = panel.querySelector('#' + btnId);
      const origText = btn.textContent;
      btn.textContent = '⏳...';
      btn.disabled = true;
      
      const formData = new FormData();
      formData.append("text", selection);
      
      fetch("http://localhost:8000" + endpoint, { method: "POST", body: formData })
        .then(r => r.json())
        .then(data => {
          const result = data[field] || JSON.stringify(data);
          panel.querySelector('#ps-result').textContent = result.substring(0, 200) + '...';
          // Copy to clipboard
          navigator.clipboard.writeText(result);
          btn.textContent = '✅ Done! (copied)';
        })
        .catch(() => {
          btn.textContent = '❌ API offline';
          panel.querySelector('#ps-result').textContent = 'Start Privacy Toolkit: cd ~/Projects/ai-privacy-toolkit && python3 -m uvicorn app.main:app --port 8000';
        });
      
      setTimeout(() => { btn.textContent = origText; btn.disabled = false; }, 3000);
    };
    
    panel.querySelector('#ps-clean').onclick = () => process('/api/privacy/clean', 'cleaned', 'ps-clean');
    panel.querySelector('#ps-check').onclick = () => process('/api/privacy/check', 'analysis', 'ps-check');
    panel.querySelector('#ps-summarize').onclick = () => process('/api/summarize', 'summary', 'ps-summarize');
  });
})();