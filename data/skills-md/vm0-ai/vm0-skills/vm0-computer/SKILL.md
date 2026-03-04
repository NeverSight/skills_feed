---
name: vm0-computer
description: Access the user's local computer files via WebDAV through the VM0 Computer Connector. Use when you need to read, write, or list files on the user's local machine from within a VM0 sandbox.
vm0_secrets:
  - COMPUTER_CONNECTOR_BRIDGE_TOKEN
  - COMPUTER_CONNECTOR_DOMAIN
---

# VM0 Computer Connector

Access the user's local filesystem from a VM0 sandbox over a secure WebDAV tunnel established by the VM0 Computer Connector.

---

## When to Use

Use this skill when you need to:

- List files and directories on the user's local machine
- Read files from the user's computer into the sandbox
- Write or update files on the user's local machine
- Transfer outputs back to the user's local filesystem

---

## How to Use

### Setup

> **Note on Proxy Persistence:** VM0 sandboxes are stateless environments. The proxy process and `/tmp/proxy.mjs` file will be cleared between sessions. This is expected behavior - you'll need to reinstall `ws` and recreate the proxy each time you start a new sandbox session.

Write the proxy script to `/tmp/proxy.mjs`:

```javascript
import { WebSocket, WebSocketServer } from "ws";
import http from "http";
import https from "https";

const TOKEN = process.env.COMPUTER_CONNECTOR_BRIDGE_TOKEN;
const DOMAIN = process.env.COMPUTER_CONNECTOR_DOMAIN;

// Chrome CDP WebSocket proxy: ws://127.0.0.1:9222 → wss://chrome.{DOMAIN}
const wss = new WebSocketServer({ host: "127.0.0.1", port: 9222 });
wss.on("connection", (local) => {
  const remote = new WebSocket(`wss://chrome.${DOMAIN}`, {
    headers: { "x-vm0-token": TOKEN },
  });
  local.on("message", (msg) => remote.send(msg));
  remote.on("message", (msg) => local.send(msg));
  local.on("close", () => remote.close());
  remote.on("close", () => local.close());
});

// WebDAV HTTP proxy: http://127.0.0.1:8080 → https://webdav.{DOMAIN}
http.createServer((req, res) => {
  const upstream = https.request(
    `https://webdav.${DOMAIN}${req.url}`,
    { method: req.method, headers: { ...req.headers, "x-vm0-token": TOKEN, host: `webdav.${DOMAIN}` } },
    (proxyRes) => { res.writeHead(proxyRes.statusCode, proxyRes.headers); proxyRes.pipe(res); }
  );
  req.pipe(upstream);
}).listen(8080, "127.0.0.1");

console.log("WebDAV proxy: http://127.0.0.1:8080");
console.log("CDP proxy:    ws://127.0.0.1:9222");
```

### Run

```bash
cd /tmp && npm install ws && node /tmp/proxy.mjs &
```

The proxy runs in the background. Tools can now connect to `http://127.0.0.1:8080` (WebDAV) and `ws://127.0.0.1:9222` (Chrome CDP) without any additional headers.

> **Important:** Wrap curl commands that use `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.

### 1. List Files in a Directory

Use `PROPFIND` to list the contents of a directory (depth 1):

```bash
bash -c 'curl -s -X PROPFIND "http://127.0.0.1:8080"'
```

List a subdirectory:

```bash
curl -s -X PROPFIND "http://127.0.0.1:8080/reports/" --header "Depth: 1"
```

### 2. Download a File from the Local Machine

```bash
curl -s -o /tmp/myfile.pdf "http://127.0.0.1:8080/myfile.pdf"
```

Read a text file directly:

```bash
curl -s "http://127.0.0.1:8080/notes.txt"
```

### 3. Upload a File to the Local Machine

Write a local sandbox file to remote:

```bash
curl -s -X PUT "http://127.0.0.1:8080/output-report.txt" --header "Content-Type: text/plain" --data-binary @/home/user/output-report.txt
```

Upload from stdin (inline content):

```bash
curl -s -X PUT "http://127.0.0.1:8080/result.json" --header "Content-Type: application/json" -d '{"status": "done"}'
```

### 4. Delete a File

```bash
curl -s -X DELETE "http://127.0.0.1:8080/old-file.txt"
```

### 5. Create a Directory

```bash
curl -s -X MKCOL "http://127.0.0.1:8080/new-folder/"
```

### 6. Move (Rename) a File

```bash
curl -s -X MOVE "http://127.0.0.1:8080/old-name.txt" --header "Destination: http://127.0.0.1:8080/new-name.txt"
```

Move to a subdirectory:

```bash
curl -s -X MOVE "http://127.0.0.1:8080/report.pdf" --header "Destination: http://127.0.0.1:8080/archive/report.pdf"
```

### 7. Search File Contents

WebDAV does not support full-text search natively. Use PROPFIND with `Depth: infinity` to list all files recursively, then download and search:

```bash
# List all files recursively
curl -s -X PROPFIND "http://127.0.0.1:8080/" --header "Depth: infinity" | grep -o '<D:href>[^<]*</D:href>' | sed 's/<[^>]*>//g'
```

Search for a keyword across all text files:

```bash
for f in $(curl -s -X PROPFIND "http://127.0.0.1:8080/" --header "Depth: infinity" | grep -o '<D:href>[^<]*</D:href>' | sed 's/<[^>]*>//g' | grep '\.txt$'); do
  content=$(curl -s "http://127.0.0.1:8080${f}")
  echo "$content" | grep -q "keyword" && echo "Found in: $f"
done
```

---

## Troubleshooting

### SSL Certificate Error (`ERR_TLS_CERT_ALTNAME_INVALID`)

**Issue:** The first connection attempt may fail with `ERR_TLS_CERT_ALTNAME_INVALID` or similar SSL certificate errors.

**Cause:** The ngrok tunnel needs a few minutes to provision and propagate SSL certificates after the Computer Connector starts.

**Solution:**
1. **Wait 2-3 minutes** after starting the Computer Connector for SSL certificates to be fully provisioned
2. The proxy will automatically work once certificates are ready - no code changes needed
3. Test with a simple curl command: `curl -s "http://127.0.0.1:8080/"`

**Note:** Do NOT add `rejectUnauthorized: false` to the proxy code as a workaround. This weakens security and is unnecessary - simply wait for proper certificate provisioning.
