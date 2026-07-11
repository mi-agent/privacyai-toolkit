// Popup JS
const API_BASE = "http://localhost:8000";
const resultEl = document.getElementById("result");
const copiedEl = document.getElementById("copied");
const inputEl = document.getElementById("inputText");
const apiStatus = document.getElementById("apiStatus");

// Check API status on load
(async () => {
  try {
    const r = await fetch(API_BASE + "/api/health", { mode: "no-cors" });
    apiStatus.className = "status";
    apiStatus.innerHTML = 'API: <span>Online ✅</span>';
  } catch {
    apiStatus.className = "status offline";
    apiStatus.innerHTML = 'API: <span>Offline (run Privacy Toolkit)</span>';
  }
})();

async function process(endpoint, field) {
  const text = inputEl.value.trim();
  if (!text) {
    resultEl.textContent = "Please enter some text first.";
    return;
  }
  
  resultEl.textContent = "Processing...";
  resultEl.className = "result";
  
  try {
    const formData = new FormData();
    formData.append("text", text);
    const resp = await fetch(API_BASE + endpoint, { method: "POST", body: formData });
    const data = await resp.json();
    const result = data[field] || JSON.stringify(data);
    resultEl.textContent = result;
    resultEl.className = "result success";
    
    await navigator.clipboard.writeText(result);
    copiedEl.style.display = "block";
    setTimeout(() => { copiedEl.style.display = "none"; }, 2000);
  } catch (e) {
    resultEl.textContent = "Error: Make sure Privacy Toolkit is running at localhost:8000\n\nStart: cd ~/Projects/ai-privacy-toolkit && python3 -m uvicorn app.main:app --port 8000";
    resultEl.className = "result";
  }
}

document.getElementById("btnClean").onclick = () => process("/api/privacy/clean", "cleaned");
document.getElementById("btnCheck").onclick = () => process("/api/privacy/check", "analysis");
document.getElementById("btnSummarize").onclick = () => process("/api/summarize", "summary");
document.getElementById("btnRedact").onclick = () => process("/api/redact", "redacted");