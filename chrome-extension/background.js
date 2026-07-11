// Privacy Shield - Background Service Worker
// Right-click menu for quick text cleaning

chrome.runtime.onInstalled.addListener(() => {
  // Create context menu
  chrome.contextMenus.create({
    id: "cleanPrivacy",
    title: "🛡️ Clean Privacy (AI)",
    contexts: ["selection"]
  });
  chrome.contextMenus.create({
    id: "checkPrivacy",
    title: "🔍 Check Privacy Risk",
    contexts: ["selection"]
  });
  chrome.contextMenus.create({
    id: "summarize",
    title: "📝 AI Summarize",
    contexts: ["selection"]
  });
});

// Handle context menu clicks
chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  const selectedText = info.selectionText;
  if (!selectedText) return;
  
  const taskId = info.menuItemId;
  
  try {
    // Call local Privacy Toolkit API
    const apiMap = {
      cleanPrivacy: { endpoint: "/api/privacy/clean", field: "cleaned" },
      checkPrivacy: { endpoint: "/api/privacy/check", field: "analysis" },
      summarize: { endpoint: "/api/summarize", field: "summary" }
    };
    
    const api = apiMap[taskId];
    if (!api) return;
    
    // Try local first, then show result
    let result = "";
    try {
      const formData = new FormData();
      formData.append("text", selectedText);
      
      const resp = await fetch("http://localhost:8000" + api.endpoint, {
        method: "POST",
        body: formData
      });
      
      if (resp.ok) {
        const data = await resp.json();
        result = data[api.field] || JSON.stringify(data);
      } else {
        result = "[Local API not running]\n\nStart: open ~/Projects/ai-privacy-toolkit/run.sh\n\nSelected text:\n" + selectedText.substring(0, 100) + "...";
      }
    } catch {
      result = "[Privacy Shield Ready]\n\nStart local API:\n1. cd ~/Projects/ai-privacy-toolkit\n2. bash run.sh\n\nThen select text and try again.\n\nSelected text:\n" + selectedText.substring(0, 200) + "...";
    }
    
    // Show result in notification
    chrome.notifications.create({
      type: "basic",
      iconUrl: "icon.png",
      title: taskId === "cleanPrivacy" ? "Privacy Cleaned" : 
             taskId === "checkPrivacy" ? "Privacy Check" : "Summary",
      message: result.substring(0, 300) + (result.length > 300 ? "..." : "")
    });
    
    // Copy result to clipboard
    await navigator.clipboard.writeText(result);
    
  } catch (err) {
    console.error("Privacy Shield error:", err);
  }
});

// Listen for messages from popup
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type === "getStatus") {
    // Check if local API is running
    fetch("http://localhost:8000/api/health", { mode: "no-cors" })
      .then(() => sendResponse({ api: "online" }))
      .catch(() => sendResponse({ api: "offline" }));
    return true;
  }
  
  if (msg.type === "process") {
    // Quick process from popup
    const formData = new FormData();
    formData.append("text", msg.text);
    
    fetch("http://localhost:8000" + msg.endpoint, { method: "POST", body: formData })
      .then(r => r.json())
      .then(data => sendResponse({ success: true, data }))
      .catch(err => sendResponse({ success: false, error: err.message }));
    return true;
  }
});