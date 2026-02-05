---
name: berrypay
description: Manage Nano (XNO) cryptocurrency wallet operations using BerryPay CLI. Use for checking balance, sending/receiving XNO, creating payment charges with webhooks, generating QR codes, and processing payments with automatic sweeping.
---

# BerryPay CLI - AI Agent Skill Guide

BerryPay is a Nano (XNO) cryptocurrency wallet CLI designed for AI agents. It provides passwordless operation, JSON output for parsing, and a payment processor for accepting payments with automatic sweeping.

## Quick Reference

| Task | Command |
|------|---------|
| Check balance | `berrypay balance` |
| Get address | `berrypay address` |
| Send XNO | `berrypay send <address> <amount> --yes` |
| Receive pending | `berrypay receive` |
| Create charge | `berrypay charge create <amount> --webhook <url>` |
| Check charge | `berrypay charge status <id>` |
| List charges | `berrypay charge list` |

---

## Installation & Setup

### Install globally
```bash
npm install -g berrypay
```

### Initialize wallet (first time only)
```bash
berrypay init
```
This creates a new wallet with a random seed stored in `~/.berrypay/config.json`.

### Or use environment variable (recommended for agents)
```bash
export BERRYPAY_SEED=<64-character-hex-seed>
```
When `BERRYPAY_SEED` is set, it overrides the config file. This is the recommended approach for AI agents.

### Import existing seed
```bash
berrypay import <64-character-hex-seed>
```

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `BERRYPAY_SEED` | 64-char hex seed (overrides config) | - |
| `BERRYPAY_RPC_URL` | Nano RPC node URL | `https://uk1.public.xnopay.com/proxy` |
| `BERRYPAY_WS_URL` | WebSocket URL for confirmations | `wss://uk1.public.xnopay.com/ws` |

---

## Core Wallet Commands

### Get Wallet Address
```bash
berrypay address
```

**Output:**
```json
{
  "address": "nano_1abc...",
  "index": 0
}
```

**With QR code (for sharing/display):**
```bash
berrypay address --qr
```
Displays QR code in terminal.

**Save QR code as PNG image:**
```bash
berrypay address --qr --output /path/to/qr.png
```
Creates a 400x400 PNG image of the QR code. Useful for sending via Telegram or other messaging.

### Check Balance
```bash
berrypay balance
```

**Output:**
```json
{
  "address": "nano_1abc...",
  "balance": "1.5",
  "balanceRaw": "1500000000000000000000000000000",
  "pending": "0.0",
  "pendingRaw": "0"
}
```

**Note:** This command auto-receives any pending funds before showing balance.

**JSON-only output (for parsing):**
```bash
berrypay balance --json
```

### Send XNO
```bash
berrypay send <recipient_address> <amount> --yes
```

**Parameters:**
- `<recipient_address>`: Nano address starting with `nano_`
- `<amount>`: Amount in XNO (e.g., `0.1`, `1.5`, `100`)
- `--yes` or `-y`: Skip confirmation prompt (required for automation)

**Example:**
```bash
berrypay send nano_1abc123... 0.5 --yes
```

**Output:**
```json
{
  "hash": "ABC123...",
  "to": "nano_1abc...",
  "amount": "0.5",
  "amountRaw": "500000000000000000000000000000"
}
```

**Note:** Auto-receives pending funds before sending to ensure full balance is available.

### Receive Pending Funds
```bash
berrypay receive
```

Receives all pending incoming transactions. Called automatically by `balance` and `send`, but can be run manually.

**Output:**
```json
{
  "received": 2,
  "blocks": [
    {"hash": "ABC...", "amount": "0.1"},
    {"hash": "DEF...", "amount": "0.05"}
  ]
}
```

### Watch for Incoming Payments (Real-time)
```bash
berrypay watch
```

Monitors the wallet address via WebSocket and auto-receives incoming payments. Runs continuously until Ctrl+C.

---

## Payment Processor (Charges)

The payment processor creates ephemeral addresses for each payment request, monitors for payments, and automatically sweeps funds to the main wallet.

### Flow
```
1. Create charge → Ephemeral address generated
2. Customer/payer sends XNO to ephemeral address
3. Listener detects payment via WebSocket
4. Auto-receive → Funds received to ephemeral address
5. Auto-sweep → Funds sent to main wallet (index 0)
6. Webhook called → Your server notified
7. Listener auto-stops when no active charges remain
```

### Create a Charge
```bash
berrypay charge create <amount> [options]
```

**Parameters:**
- `<amount>`: Amount in XNO to request

**Options:**
| Option | Description |
|--------|-------------|
| `-t, --timeout <minutes>` | Timeout in minutes (default: 30) |
| `-w, --webhook <url>` | URL to POST when payment completes |
| `-m, --metadata <json>` | JSON metadata included in webhook |
| `--qr` | Display QR code in terminal |
| `-o, --output <path>` | Save QR code as PNG image |

**Example - Basic charge:**
```bash
berrypay charge create 0.1
```

**Example - With webhook and metadata:**
```bash
berrypay charge create 1.5 \
  --webhook http://localhost:3000/api/payment-callback \
  --metadata '{"orderId": "order_123", "userId": "user_456"}'
```

**Example - With QR code image:**
```bash
berrypay charge create 0.5 --qr --output /tmp/payment-qr.png
```

**Output:**
```json
{
  "id": "chg_abc123def456...",
  "address": "nano_3ephemeral...",
  "amount": "0.5",
  "amountRaw": "500000000000000000000000000000",
  "expiresAt": "2026-01-30T12:30:00.000Z",
  "webhookUrl": "http://localhost:3000/callback",
  "metadata": {"orderId": "order_123"}
}
```

**Important:** Creating a charge automatically starts the background listener if not already running.

### Check Charge Status
```bash
berrypay charge status <charge_id>
```

**Example:**
```bash
berrypay charge status chg_abc123def456
```

**Output:**
```json
{
  "id": "chg_abc123def456",
  "address": "nano_3ephemeral...",
  "status": "completed",
  "required": "0.5",
  "requiredRaw": "500000000000000000000000000000",
  "onChainBalance": "0.5",
  "onChainPending": "0.0",
  "isPaid": true,
  "remaining": "0.0",
  "swept": true,
  "sweepHash": "XYZ789..."
}
```

**Status values:**
| Status | Description |
|--------|-------------|
| `pending` | Waiting for payment |
| `partial` | Some payment received, not complete |
| `completed` | Full payment received |
| `swept` | Funds transferred to main wallet |
| `expired` | Timeout reached without full payment |

**Note:** Running `charge status` will:
1. Check blockchain for actual balance/pending
2. Auto-receive any pending blocks
3. Auto-sweep if fully paid (unless `--no-sweep` flag)

### List All Charges
```bash
berrypay charge list
```

**Filter by status:**
```bash
berrypay charge list --status pending
berrypay charge list --status completed
berrypay charge list --status swept
```

**Output:**
```json
{
  "charges": [
    {"id": "chg_abc...", "status": "swept", "amount": "0.5", "received": "0.5"},
    {"id": "chg_def...", "status": "pending", "amount": "1.0", "received": "0.0"}
  ]
}
```

### Manually Sweep a Charge
```bash
berrypay charge sweep <charge_id>
```

Forces immediate sweep of funds from charge's ephemeral address to main wallet.

**Verbose mode (for debugging):**
```bash
berrypay charge sweep <charge_id> --verbose
```

### Listener Management

**Check if listener is running:**
```bash
berrypay charge listener
```

**Output:**
```json
{
  "running": true,
  "pid": 12345
}
```

**Manually stop listener:**
```bash
berrypay charge stop
```

**Manually start listener (usually not needed):**
```bash
berrypay charge listen
```
Note: Listener auto-starts on `charge create` and auto-stops when no active charges remain.

### Clean Up Old Charges
```bash
berrypay charge cleanup
```

Removes swept charges from history to free up storage.

---

## Webhook Payload

When a charge is completed and swept, BerryPay POSTs to your webhook URL:

**Request:**
```http
POST /your-webhook-endpoint HTTP/1.1
Content-Type: application/json

{
  "event": "charge.completed",
  "charge": {
    "id": "chg_abc123def456",
    "address": "nano_3ephemeral...",
    "amountNano": "0.5",
    "amountRaw": "500000000000000000000000000000",
    "receivedNano": "0.5",
    "receivedRaw": "500000000000000000000000000000",
    "status": "swept",
    "sweepTxHash": "ABC123...",
    "sweptAmountNano": "0.5",
    "sweptAmountRaw": "500000000000000000000000000000",
    "completedAt": "2026-01-30T12:15:00.000Z",
    "sweptAt": "2026-01-30T12:15:05.000Z",
    "metadata": {
      "orderId": "order_123",
      "userId": "user_456"
    }
  },
  "timestamp": "2026-01-30T12:15:05.000Z"
}
```

**Your webhook should return HTTP 200 to confirm receipt.**

---

## Storage Locations

| File | Purpose |
|------|---------|
| `~/.berrypay/config.json` | Wallet seed and settings |
| `~/.berrypay/charges.json` | Charge history and state |
| `~/.berrypay/listener.pid` | Background listener PID |

---

## Common Agent Workflows

### Workflow 1: Accept Payment for a Service

```bash
# 1. Create charge with webhook
berrypay charge create 0.1 \
  --webhook http://localhost:3000/api/payment-complete \
  --metadata '{"jobId": "job_abc123"}'

# 2. Parse the output to get charge address
# 3. Share the address with the payer
# 4. Your webhook will be called when payment completes
# 5. Funds are automatically in your main wallet
```

### Workflow 2: Check if Payment Received

```bash
# Check charge status (also triggers sweep if paid)
berrypay charge status chg_abc123def456

# Parse JSON output, check "isPaid" field
```

### Workflow 3: Send Payment to Another Agent

```bash
# 1. Check balance
berrypay balance

# 2. Send payment (--yes to skip confirmation)
berrypay send nano_1recipient... 0.5 --yes

# 3. Parse output to get transaction hash
```

### Workflow 4: Generate Payment QR for User

```bash
# Create charge with QR image
berrypay charge create 1.0 \
  --qr \
  --output /tmp/payment_qr.png \
  --webhook http://localhost:3000/callback

# The QR image at /tmp/payment_qr.png can be sent to user via Telegram, etc.
```

### Workflow 5: Programmatic Integration (Node.js)

```typescript
import { BerryPayWallet, PaymentProcessor } from 'berrypay';

// Create wallet from environment
const wallet = new BerryPayWallet({
  seed: process.env.BERRYPAY_SEED
});

// Check balance
const { balance, pending } = await wallet.getBalance();
console.log(`Balance: ${BerryPayWallet.rawToNano(balance)} XNO`);

// Send payment
const result = await wallet.send(
  'nano_1recipient...',
  BerryPayWallet.nanoToRaw('0.5')
);
console.log(`Sent! Hash: ${result.hash}`);

// Payment processor
const processor = new PaymentProcessor({
  wallet,
  autoSweep: true
});

processor.on('charge:completed', (charge) => {
  console.log(`Payment received for ${charge.id}`);
});

processor.on('charge:swept', ({ charge, hash }) => {
  console.log(`Swept to main wallet: ${hash}`);
});

await processor.start();

// Create charge
const charge = await processor.createCharge({
  amountNano: '1.0',
  webhookUrl: 'http://localhost:3000/callback',
  metadata: { orderId: '123' }
});

console.log(`Pay to: ${charge.address}`);
```

---

## Error Handling

All commands output JSON with error information on failure:

```json
{
  "error": "Insufficient balance. Have: 0.05 XNO"
}
```

**Common errors:**
| Error | Cause | Solution |
|-------|-------|----------|
| "No wallet found" | Wallet not initialized | Run `berrypay init` or set `BERRYPAY_SEED` |
| "Insufficient balance" | Not enough XNO | Check balance, wait for pending |
| "Invalid Nano address" | Bad recipient address | Verify address starts with `nano_` |
| "Account not opened" | Sending from empty account | Receive some XNO first |
| "Charge not found" | Invalid charge ID | Check `charge list` for valid IDs |

---

## Tips for AI Agents

1. **Always use `--yes` flag** when sending to skip interactive prompts
2. **Parse JSON output** - all commands output JSON for easy parsing
3. **Use webhooks** for charge notifications instead of polling
4. **Store charge IDs** - needed for status checks and sweeping
5. **Use environment variables** - `BERRYPAY_SEED` for secure seed management
6. **Auto-receive is enabled** - `balance` and `send` auto-receive pending funds
7. **Listener auto-manages** - starts on charge create, stops when done
8. **QR images** - use `--output` to save QR codes for sharing with users

---

## Unit Conversions

| Unit | Value |
|------|-------|
| 1 XNO (Nano) | 10^30 raw |
| 1 raw | Smallest unit |

**In code:**
```typescript
BerryPayWallet.nanoToRaw('1.5')  // "1500000000000000000000000000000"
BerryPayWallet.rawToNano('1500000000000000000000000000000')  // "1.5"
```

---

## Network Information

- **Currency:** Nano (XNO)
- **Transaction fees:** Zero (feeless)
- **Confirmation time:** ~0.5 seconds
- **Default RPC:** `https://uk1.public.xnopay.com/proxy`
- **Default WebSocket:** `wss://uk1.public.xnopay.com/ws`
- **Representative:** `nano_1xnopay1bfmyx5eit8ut4gg1j488kt8bjukijerbn37jh3wdm81y6mxjg8qj`
