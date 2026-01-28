---
name: gemini-research-browser-use
description: Use Chrome DevTools Protocol to allow the AI to "ask Gemini" or "research with Gemini" directly. This uses the user's logged-in Chrome session, bypassing API limits and leveraging the web interface's reasoning capabilities.
---

# Gemini Research Browser Use

## Overview

Perform research or queries using Google Gemini via Chrome DevTools Protocol (CDP). This method reuses the user's **existing Chrome login session** to interact with the Gemini web interface (`https://gemini.google.com/`).

## Prerequisites

1. **Python + websockets**
   Verify:
   ```bash
   python3 --version
   python3 -m pip show websockets
   ```
   Install if missing:
   ```bash
   python3 -m pip install websockets
   ```

2. **Google Chrome**
   Verify:
   ```bash
   "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --version
   ```

3. **CDP Port Availability**
   Verify Chrome is listening (after launch in Step 2):
   ```bash
   curl -s http://localhost:9222/json | python3 -m json.tool
   ```

4. **Non-default user data directory (required by Chrome)**
   Chrome CDP **requires** a non-default profile path. Use a cloned profile so you keep login state.
   ```bash
   rm -rf /tmp/chrome-gemini-profile
   rsync -a "$HOME/Library/Application Support/Google/Chrome/" /tmp/chrome-gemini-profile/
   ```

## Method Comparison

| Method | Pros | Cons | Recommended |
|--------|------|------|-------------|
| **Chrome Remote Debugging (CDP)** | Uses existing login, full automation, reliable | Requires Chrome restart with debugging flag | ✅ **Yes** |
| `browser-use --browser real` | Simple CLI | Opens new session without login | ❌ No |
| `browser_subagent` | Visual feedback | Rate limited, may fail | ❌ No |

---

## ✅ Recommended Method: Chrome Remote Debugging (CDP)

This is the **most reliable method** that uses your system Chrome with existing Google login.

### Prerequisites

1. **Python 3** with `websockets` library
2. **Google Chrome** installed at `/Applications/Google Chrome.app/`
3. **User logged into Google** in Chrome

### Step 1: Install websockets (if needed)

```bash
pip3 install websockets
# Or in virtual environment:
python3 -m venv .venv && ./.venv/bin/pip install websockets
```

### Step 2: Launch Chrome with Remote Debugging (Non-default profile)

**Important**: Close any existing Chrome windows first, or use a different debugging port.

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --remote-debugging-port=9222 \
  --user-data-dir="/tmp/chrome-gemini-profile" \
  "https://gemini.google.com/" &
```

**Parameters explained:**
- `--remote-debugging-port=9222`: Enables CDP on port 9222
- `--user-data-dir`: Points to your existing Chrome profile (with login session)
- The URL opens Gemini directly

### Step 3: Verify Connection (CDP)

```bash
curl -s http://localhost:9222/json | python3 -m json.tool
```

Look for the Gemini page entry:
```json
{
  "title": "Google Gemini",
  "url": "https://gemini.google.com/app",
  "webSocketDebuggerUrl": "ws://localhost:9222/devtools/page/XXXXXXXX"
}
```

**Note**: If URL shows `/app` instead of just `/`, it means you're **logged in**.

### Step 4: Send Query to Gemini

Save this as `gemini_query.py` or run inline:

```python
import asyncio
import websockets
import json
import subprocess
import sys

async def query_gemini(query_text, wait_seconds=30):
    # Get the Gemini page WebSocket URL
    result = subprocess.run(
        ["curl", "-s", "http://localhost:9222/json"],
        capture_output=True, text=True
    )
    pages = json.loads(result.stdout)
    
    # Find Gemini page
    gemini_page = None
    for page in pages:
        if page.get("type") == "page" and "gemini.google.com" in page.get("url", ""):
            gemini_page = page
            break
    
    if not gemini_page:
        print("Error: Gemini page not found. Make sure Chrome is open with Gemini.")
        return None
    
    ws_url = gemini_page["webSocketDebuggerUrl"]
    print(f"Connecting to: {ws_url}")
    
    async with websockets.connect(ws_url) as ws:
        # Step 1: Input the query
        input_js = f'''
        const editor = document.querySelector('div[contenteditable="true"]');
        if(editor) {{
            editor.focus();
            document.execCommand('insertText', false, `{query_text}`);
            editor.dispatchEvent(new Event('input', {{bubbles: true}}));
            'success';
        }} else {{
            'editor not found';
        }}
        '''
        
        await ws.send(json.dumps({
            "id": 1,
            "method": "Runtime.evaluate",
            "params": {"expression": input_js}
        }))
        response = await ws.recv()
        result = json.loads(response)
        print(f"Input result: {result.get('result', {}).get('result', {}).get('value', 'unknown')}")
        
        # Step 2: Click send button
        await asyncio.sleep(1)
        click_js = '''
        const btn = document.querySelector('button[aria-label="傳送訊息"]');
        if(btn) { btn.click(); 'clicked'; } else { 'button not found'; }
        '''
        
        await ws.send(json.dumps({
            "id": 2,
            "method": "Runtime.evaluate",
            "params": {"expression": click_js}
        }))
        response = await ws.recv()
        result = json.loads(response)
        print(f"Click result: {result.get('result', {}).get('result', {}).get('value', 'unknown')}")
        
        # Step 3: Wait for response
        print(f"Waiting {wait_seconds} seconds for Gemini to respond...")
        await asyncio.sleep(wait_seconds)
        
        # Step 4: Extract the response
        extract_js = '''
        const markdownEls = document.querySelectorAll('.markdown');
        if(markdownEls.length > 0) {
            markdownEls[markdownEls.length - 1].innerText;
        } else {
            'No response found';
        }
        '''
        
        await ws.send(json.dumps({
            "id": 3,
            "method": "Runtime.evaluate",
            "params": {"expression": extract_js}
        }))
        response = await ws.recv()
        result = json.loads(response)
        content = result.get('result', {}).get('result', {}).get('value', 'No content')
        
        return content

# Main execution
if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "範例問題：請用繁體中文回答什麼是區塊鏈？"
    result = asyncio.run(query_gemini(query, wait_seconds=30))
    print("\n" + "="*50)
    print("GEMINI RESPONSE:")
    print("="*50)
    print(result)
```

### Step 5: Run the Query

```bash
python3 gemini_query.py "範例問題：你的查詢問題"
```

Or inline for simple queries:

```bash
python3 << 'EOF'
import asyncio
import websockets
import json

async def send_to_gemini():
    # Get WebSocket URL
    import subprocess
    result = subprocess.run(["curl", "-s", "http://localhost:9222/json"], capture_output=True, text=True)
    pages = json.loads(result.stdout)
    ws_url = next(p["webSocketDebuggerUrl"] for p in pages if "gemini.google.com" in p.get("url", ""))
    
    async with websockets.connect(ws_url) as ws:
        # Input query
        await ws.send(json.dumps({
            "id": 1,
            "method": "Runtime.evaluate",
            "params": {"expression": '''
                const editor = document.querySelector('div[contenteditable="true"]');
                editor.focus();
                document.execCommand('insertText', false, '範例問題：請分析比特幣未來的價格走勢');
                editor.dispatchEvent(new Event('input', {bubbles: true}));
            '''}
        }))
        await ws.recv()
        
        # Click send
        await asyncio.sleep(1)
        await ws.send(json.dumps({
            "id": 2,
            "method": "Runtime.evaluate",
            "params": {"expression": '''document.querySelector('button[aria-label="傳送訊息"]').click()'''}
        }))
        await ws.recv()
        
        # Wait and extract
        await asyncio.sleep(30)
        await ws.send(json.dumps({
            "id": 3,
            "method": "Runtime.evaluate",
            "params": {"expression": '''
                document.querySelectorAll('.markdown')[document.querySelectorAll('.markdown').length - 1].innerText
            '''}
        }))
        response = await ws.recv()
        print(json.loads(response)['result']['result']['value'])

asyncio.run(send_to_gemini())
EOF
```

---

## Alternative Method: browser-use CLI

This method is simpler but **does not use your existing Chrome login**. You'll need to log in manually each time.

### Prerequisites

```bash
# Create virtual environment
python3 -m venv .venv

# Install browser-use
./.venv/bin/pip install browser-use
```

### Workflow

#### 1) Open Gemini

```bash
./.venv/bin/browser-use --browser real open "https://gemini.google.com/"
```

#### 2) Get Page State

```bash
./.venv/bin/browser-use --browser real state
```

Look for:
- The input textbox: `contenteditable=true role=textbox`
- The send button: `aria-label=傳送訊息`

#### 3) Input Text via JavaScript eval

```bash
./.venv/bin/browser-use --browser real eval "const editor = document.querySelector('div[contenteditable=\"true\"]'); editor.focus(); document.execCommand('insertText', false, 'YOUR QUERY HERE'); editor.dispatchEvent(new Event('input', {bubbles: true}));"
```

#### 4) Click Send Button

```bash
# Get current state to find button index
./.venv/bin/browser-use --browser real state

# Click the send button (replace INDEX with actual number)
./.venv/bin/browser-use --browser real click INDEX
```

#### 5) Close Session

```bash
./.venv/bin/browser-use close
```

---

## Troubleshooting

### Chrome Remote Debugging Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| `curl: (7) Failed to connect` | Chrome not running with debugging | Restart Chrome with `--remote-debugging-port=9222` |
| WebSocket connection refused | Page ID changed | Re-fetch `/json` to get new WebSocket URL |
| "editor not found" | Page not fully loaded | Wait a few seconds before running script |
| "button not found" | Send button not visible | Check if text was actually input first |
| Login page instead of app | Wrong user-data-dir path | Verify path: `"$HOME/Library/Application Support/Google/Chrome"` |
| `DevTools remote debugging requires a non-default data directory` | Chrome disallows default profile for CDP | Launch with a cloned profile: `/tmp/chrome-gemini-profile` |
| `curl` shows connection refused even though Chrome is running | CDP not listening due to profile path | Ensure `--user-data-dir` is **not** default and the port is free |
| `No Gemini page found via CDP` | Gemini not loaded or not logged in | Open `https://gemini.google.com/` in the launched Chrome and wait for `/app` |

### browser-use Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| Not logged in | browser-use creates isolated session | Use Chrome Remote Debugging method instead |
| `Unknown key: "請"` error | CLI doesn't support Unicode | Use `eval` with JavaScript `execCommand` |
| Click doesn't work | Element index changed | Re-run `state` before each click |

---

## Best Practices

1. **Always use Chrome Remote Debugging** for queries requiring authentication
2. **Wait 30+ seconds** for complex queries (Gemini's "Deep Think" mode takes longer)
3. **Check for `.markdown` elements** to verify response is complete
4. **Use inline Python** for one-off queries; use the full script for automation
5. **Close Chrome debugging session** when done to avoid port conflicts
6. **Keep profile cloned** in `/tmp/chrome-gemini-profile` to avoid CDP blocking the default profile

---

## Complete Example: Crypto Price Analysis

### 完整工作流程

```bash
# Step 1: 準備 Chrome 設定檔副本 (避免 CDP 預設目錄限制)
rm -rf /tmp/chrome-gemini-profile
rsync -a "$HOME/Library/Application Support/Google/Chrome/" /tmp/chrome-gemini-profile/

# Step 2: 啟動 Chrome 遠端除錯模式
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --remote-debugging-port=9222 \
  --user-data-dir="/tmp/chrome-gemini-profile" \
  "https://gemini.google.com/" > /dev/null 2>&1 &

# Step 3: 等待頁面載入並驗證連接
sleep 8
curl -s http://localhost:9222/json | python3 -c "import sys, json; pages = json.load(sys.stdin); gemini = [p for p in pages if p.get('type') == 'page' and 'gemini.google.com' in p.get('url', '')]; print(f\"找到 Gemini 頁面: {gemini[0]['url'] if gemini else '未找到'}\")"
```

### 方法 1: 完整查詢腳本 (query_gemini.py)

將以下內容儲存為 `query_gemini.py`:

```python
import asyncio
import websockets
import json
import subprocess
import sys

async def query_gemini(query_text, wait_seconds=60):
    # Get the Gemini page WebSocket URL
    result = subprocess.run(
        ["curl", "-s", "http://localhost:9222/json"],
        capture_output=True, text=True
    )
    pages = json.loads(result.stdout)
    
    # Find Gemini page
    gemini_page = None
    for page in pages:
        if page.get("type") == "page" and "gemini.google.com" in page.get("url", ""):
            gemini_page = page
            break
    
    if not gemini_page:
        print("錯誤:找不到 Gemini 頁面。請確保 Chrome 已開啟 Gemini。")
        return None
    
    ws_url = gemini_page["webSocketDebuggerUrl"]
    print(f"正在連接到: {ws_url}")
    
    async with websockets.connect(ws_url) as ws:
        # Step 1: Input the query
        input_js = f'''
        const editor = document.querySelector('div[contenteditable="true"]');
        if(editor) {{
            editor.focus();
            document.execCommand('insertText', false, `{query_text}`);
            editor.dispatchEvent(new Event('input', {{bubbles: true}}));
            'success';
        }} else {{
            'editor not found';
        }}
        '''
        
        await ws.send(json.dumps({
            "id": 1,
            "method": "Runtime.evaluate",
            "params": {"expression": input_js}
        }))
        response = await ws.recv()
        result = json.loads(response)
        print(f"輸入結果: {result.get('result', {}).get('result', {}).get('value', 'unknown')}")
        
        # Step 2: Click send button
        await asyncio.sleep(1)
        click_js = '''
        const btn = document.querySelector('button[aria-label="傳送訊息"]');
        if(btn) { btn.click(); 'clicked'; } else { 'button not found'; }
        '''
        
        await ws.send(json.dumps({
            "id": 2,
            "method": "Runtime.evaluate",
            "params": {"expression": click_js}
        }))
        response = await ws.recv()
        result = json.loads(response)
        print(f"點擊結果: {result.get('result', {}).get('result', {}).get('value', 'unknown')}")
        
        # Step 3: Wait for response
        print(f"等待 {wait_seconds} 秒讓 Gemini 回應...")
        await asyncio.sleep(wait_seconds)
        
        # Step 4: Extract the response - try to get complete content
        extract_js = '''
        const markdownEls = document.querySelectorAll('.markdown');
        if(markdownEls.length > 0) {
            const lastMarkdown = markdownEls[markdownEls.length - 1];
            // Get all text content including nested elements
            lastMarkdown.innerText || lastMarkdown.textContent || 'Empty response';
        } else {
            'No response found';
        }
        '''
        
        await ws.send(json.dumps({
            "id": 3,
            "method": "Runtime.evaluate",
            "params": {"expression": extract_js}
        }))
        response = await ws.recv()
        result = json.loads(response)
        content = result.get('result', {}).get('result', {}).get('value', 'No content')
        
        return content

# Main execution
if __name__ == "__main__":
    query = """範例問題：請詳細分析 BTC、ETH 的價格預測走勢。
需包含相關專業指標，並用繁體中文回答。"""
    
    result = asyncio.run(query_gemini(query, wait_seconds=60))
    print("\n" + "="*50)
    print("GEMINI 回應:")
    print("="*50)
    print(result)
```

**執行方式:**

```bash
python3 query_gemini.py
```

### 方法 2: 獲取已存在的回應 (get_gemini_response.py)

如果 Gemini 頁面已經有回應,可以使用此腳本直接提取:

```python
import asyncio
import websockets
import json
import subprocess

async def get_all_gemini_content():
    # Get the Gemini page WebSocket URL
    result = subprocess.run(
        ["curl", "-s", "http://localhost:9222/json"],
        capture_output=True, text=True
    )
    pages = json.loads(result.stdout)
    
    # Find Gemini page
    gemini_page = None
    for page in pages:
        if page.get("type") == "page" and "gemini.google.com" in page.get("url", ""):
            gemini_page = page
            break
    
    if not gemini_page:
        print("錯誤:找不到 Gemini 頁面。")
        return None
    
    ws_url = gemini_page["webSocketDebuggerUrl"]
    print(f"正在連接到: {ws_url}\n")
    
    async with websockets.connect(ws_url) as ws:
        # Extract all markdown content from the page
        extract_js = '''
        (function() {
            const markdownEls = document.querySelectorAll('.markdown');
            console.log('Found markdown elements:', markdownEls.length);
            
            if(markdownEls.length === 0) {
                return 'No markdown elements found';
            }
            
            // Get the last two markdown elements (user query and AI response)
            const responses = [];
            const startIdx = Math.max(0, markdownEls.length - 2);
            
            for(let i = startIdx; i < markdownEls.length; i++) {
                const text = markdownEls[i].innerText || markdownEls[i].textContent || '';
                if(text.trim()) {
                    responses.push(`[回應 ${i+1}]:\\n${text}`);
                }
            }
            
            return responses.join('\\n\\n' + '='.repeat(80) + '\\n\\n');
        })()
        '''
        
        await ws.send(json.dumps({
            "id": 1,
            "method": "Runtime.evaluate",
            "params": {"expression": extract_js, "returnByValue": True}
        }))
        response = await ws.recv()
        result = json.loads(response)
        content = result.get('result', {}).get('result', {}).get('value', 'No content')
        
        return content

# Main execution
if __name__ == "__main__":
    result = asyncio.run(get_all_gemini_content())
    print("="*80)
    print("GEMINI 對話內容:")
    print("="*80)
    print(result)
```

**執行方式:**

```bash
python3 get_gemini_response.py
```

### 實際使用範例

```bash
# 完整流程
rm -rf /tmp/chrome-gemini-profile && \
rsync -a "$HOME/Library/Application Support/Google/Chrome/" /tmp/chrome-gemini-profile/ && \
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --remote-debugging-port=9222 \
  --user-data-dir="/tmp/chrome-gemini-profile" \
  "https://gemini.google.com/" > /dev/null 2>&1 &

# 等待並執行查詢
sleep 8 && python3 query_gemini.py
```

### 清理資源

完成查詢後,建議清理臨時文件和資源:

```bash
# 1. 關閉 Chrome 除錯會話
pkill -9 "Google Chrome"

# 2. 清理臨時設定檔 (可選,釋放磁碟空間)
rm -rf /tmp/chrome-gemini-profile

# 3. 清理測試過程中生成的臨時腳本和輸出文件
rm -f query_gemini.py get_gemini_response.py get_all_gemini_content.py
rm -f gemini_response.txt gemini_full_response.txt
```

**最佳實踐:**

1. **每次使用後關閉 Chrome** - 避免佔用 9222 端口
2. **定期清理臨時設定檔** - `/tmp/chrome-gemini-profile` 可能佔用數百 MB
3. **保持工作目錄整潔** - 刪除測試腳本,將常用腳本整合到專案中
4. **使用完整腳本** - 將上述 `query_gemini.py` 儲存為專案文件,而非每次重新建立

---

## 注意事項

1. **等待時間調整** - 複雜查詢(如深度分析)建議 `wait_seconds=60` 或更長
2. **回應截斷問題** - 如果回應很長,可能需要多次提取或使用 `get_all_gemini_content.py` 方法
3. **登入狀態** - 確保 Chrome 設定檔中已登入 Google 帳號
4. **網路穩定性** - CDP 連接需要穩定的網路環境
5. **並發限制** - 避免同時開啟多個 Chrome 除錯會話在同一端口
