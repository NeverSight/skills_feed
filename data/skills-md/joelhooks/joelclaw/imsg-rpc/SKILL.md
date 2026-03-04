---
name: imsg-rpc
displayName: imsg-rpc Socket Daemon
description: Set up, maintain, and debug the imsg-rpc Unix socket daemon that gives the gateway iMessage access via JSON-RPC. Covers FDA setup, code signing, launchd service, and the imsg source repo.
version: 1.1.0
author: joelclaw
tags: [imessage, gateway, imsg, launchd, fda, rpc]
---

# imsg-rpc Skill

Manages the `com.joel.imsg-rpc` launchd service that bridges the gateway daemon to iMessage via a Unix socket.

## Architecture (ADR-0121)

```
gateway daemon (bun, no FDA)
    ↕ JSON-RPC over /tmp/imsg.sock
imsg-rpc (com.joel.imsg-rpc launchd agent, has FDA)
    ↕ SQLite reads
~/Library/Messages/chat.db
```

- **Source**: `~/Code/steipete/imsg` (we own it — modify freely)
- **Build binary**: `~/Code/steipete/imsg/bin/imsg`
- **Launch binary**: `/Applications/imsg-rpc.app/Contents/MacOS/imsg`
- **Socket**: `/tmp/imsg.sock`
- **launchd plist**: `~/Library/LaunchAgents/com.joel.imsg-rpc.plist`
- **Logs**: `/tmp/joelclaw/imsg-rpc.{log,err}`
- **Gateway channel**: `packages/gateway/src/channels/imessage.ts`

## Status Check

```bash
launchctl print gui/$(id -u)/com.joel.imsg-rpc | rg "state =|pid =|runs =|last exit code"
lsof -p "$(launchctl print gui/$(id -u)/com.joel.imsg-rpc | awk '/pid =/{print $3; exit}')" | rg "imsg.sock|chat.db"
lsof -nP -U | rg "imsg.sock|com.joel.gateway|/tmp/imsg.sock"  # gateway socket peer
tail -10 /tmp/joelclaw/gateway.log | rg imessage
```

Healthy state: PID present, exit code 0, gateway shows `watch.subscribe OK`.

## Restart

```bash
launchctl unload ~/Library/LaunchAgents/com.joel.imsg-rpc.plist
launchctl load ~/Library/LaunchAgents/com.joel.imsg-rpc.plist
```

## Rebuild imsg

Always use `build-local.sh` — NOT `make build` — so signing stays stable and `/Applications/imsg-rpc.app` stays in sync with source builds:

```bash
cd ~/Code/steipete/imsg && ./build-local.sh
```

`build-local.sh` now:
- builds `bin/imsg`
- signs with `imsg Local Signing`
- refreshes/signs `/Applications/imsg-rpc.app` via `scripts/install-rpc-app.sh`

## FDA Setup (new machine)

The `imsg` binary needs Full Disk Access. macOS requires a verifiable code signature to accept it.

### 1. Create local signing cert (once per machine)

```bash
cat > /tmp/imsg-ext.cnf << 'EOF'
[req]
distinguished_name = req_distinguished_name
x509_extensions = v3_req
[req_distinguished_name]
[v3_req]
keyUsage = critical, digitalSignature
extendedKeyUsage = critical, codeSigning
basicConstraints = CA:FALSE
EOF

openssl req -x509 -newkey rsa:2048 \
  -keyout /tmp/imsg-key.pem -out /tmp/imsg-cert.pem \
  -days 3650 -nodes \
  -subj "/CN=imsg Local Signing/O=Joel Hooks" \
  -config /tmp/imsg-ext.cnf -extensions v3_req

openssl pkcs12 -export \
  -out /tmp/imsg-sign.p12 \
  -inkey /tmp/imsg-key.pem -in /tmp/imsg-cert.pem \
  -passout pass:imsg123 -name "imsg Local Signing" \
  -keypbe PBE-SHA1-3DES -certpbe PBE-SHA1-3DES -macalg sha1

security import /tmp/imsg-sign.p12 \
  -k ~/Library/Keychains/login.keychain-db \
  -P imsg123 -T /usr/bin/codesign

security add-trusted-cert -d -r trustRoot \
  -k ~/Library/Keychains/login.keychain-db /tmp/imsg-cert.pem

security find-identity -v -p codesigning  # should show "imsg Local Signing"
```

### 2. Build and sign

```bash
cd ~/Code/steipete/imsg && ./build-local.sh
```

### 3. Grant FDA in System Settings

```bash
open "x-apple.systempreferences:com.apple.preference.security?Privacy_AllFiles"
```

- Click **+**
- Press **⌘⇧G**, paste `/Applications/imsg-rpc.app`, Enter
- Toggle **ON**

### 4. Load service

```bash
launchctl load ~/Library/LaunchAgents/com.joel.imsg-rpc.plist
```

Verify: `tail -f /tmp/joelclaw/gateway.log | grep imessage` — should show `watch.subscribe OK`.

## Troubleshooting

### `permissionDenied` in imsg-rpc.log

FDA is missing or csreq mismatch. Check:

```bash
sqlite3 /Library/Application\ Support/com.apple.TCC/TCC.db \
  "SELECT client, auth_value FROM access WHERE client LIKE '%imsg%';"
# auth_value 2 = allowed, 0 = denied

/usr/bin/log show --last 10m --style compact \
  --predicate 'process == "tccd" && (eventMessage CONTAINS "com.steipete.imsg" || eventMessage CONTAINS "kTCCServiceSystemPolicyAllFiles")' \
  | tail -80
```

If denied (0): go to System Settings → Full Disk Access → toggle imsg ON.
If missing: redo FDA setup step 3.
If `tccd` shows `AUTHREQ_RESULT ... authValue=2` for `/Applications/imsg-rpc.app/Contents/MacOS/imsg`, FDA is granted.

### Socket exists but gateway can't subscribe

imsg-rpc crashed after accepting. Check `/tmp/joelclaw/imsg-rpc.err`. Restart service.

### `connect ENOENT /tmp/imsg.sock` but launchd says running

The daemon process can stay alive while the Unix socket path is unlinked. Gateway cannot connect until the socket path is recreated.

```bash
launchctl kickstart -k gui/$(id -u)/com.joel.imsg-rpc
ls -l /tmp/imsg.sock
```

Gateway now attempts this heal automatically on repeated ENOENT, but manual kickstart is the fastest recovery during incidents.

### FDA toggle didn't help after rebuild

You likely rebuilt without refreshing the app bundle. Re-run:

```bash
cd ~/Code/steipete/imsg && ./build-local.sh
```

### imsg-rpc keeps restarting (exit code 1)

Likely FDA denial. Run from terminal to test:

```bash
/Applications/imsg-rpc.app/Contents/MacOS/imsg chats --limit 1
```

If that works but launchd still fails → FDA entry is for wrong path or wrong signature.

## JSON-RPC Protocol Reference

The gateway uses these methods over `/tmp/imsg.sock`:

```json
// Subscribe to incoming messages
{"jsonrpc":"2.0","method":"watch.subscribe","params":{"participants":["handle"]},"id":1}

// Send a message
{"jsonrpc":"2.0","method":"send","params":{"to":"handle","text":"..."},"id":2}

// Inbound notification format
{"jsonrpc":"2.0","method":"message","params":{"subscription":1,"message":{...}}}
```

## Files

| Path | Purpose |
|------|---------|
| `~/Code/steipete/imsg/` | imsg source (we own) |
| `~/Code/steipete/imsg/bin/imsg` | built binary |
| `/Applications/imsg-rpc.app` | FDA target app bundle for launchd process |
| `~/Code/steipete/imsg/build-local.sh` | build + sign + app sync |
| `~/Code/steipete/imsg/scripts/install-rpc-app.sh` | creates/signs `/Applications/imsg-rpc.app` |
| `~/Library/LaunchAgents/com.joel.imsg-rpc.plist` | launchd service (not in git) |
| `packages/gateway/src/channels/imessage.ts` | gateway socket client |
| `apps/web/content/adrs/0121-imsg-rpc-socket-daemon.md` | ADR |
