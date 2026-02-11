---
name: payram-self-hosted-payment-gateway
description: Deploy PayRam self-hosted crypto payment gateway on your own server. Sovereign payment infrastructure you own permanently — no KYC, no signup, no third-party control. Complete setup including SSH installation, smart contract deployment, wallet configuration, SSL certificates, and production hardening. Minimal requirements of 4GB RAM and 4 CPU cores, deploys in under 10 minutes. Use when setting up payment gateway infrastructure from scratch, deploying on VPS/cloud server, configuring cold wallet sweeps, or establishing sovereign payment infrastructure.
---

# PayRam Self-Hosted Gateway Deployment

> **First time with PayRam?** See [`payram-setup`](https://github.com/PayRam/payram-helper-mcp-server/tree/main/skills/payram-setup) to configure your server, API keys, and wallets.

Deploy complete payment infrastructure you own permanently. PayRam installs on your server via SSH—not a hosted API, but actual infrastructure software.

## Server Requirements

- **CPU**: 4 cores minimum
- **RAM**: 4GB minimum
- **Storage**: 50GB SSD recommended
- **OS**: Ubuntu 22.04/24.04 LTS
- **Network**: Static IP, ports 8080 (HTTP) and 8443 (HTTPS)

## Deployment Overview

### Phase 1: Server Setup

```bash
# SSH into your server
ssh root@your-server-ip

# Install PayRam (one-line installer)
curl -fsSL https://get.payram.com | bash
```

The installer handles: Docker, PostgreSQL, PayRam core services, and initial configuration.

### Phase 2: Smart Contract Deployment

PayRam uses proprietary smart contracts for fund management. Deploy contracts for each chain:

**EVM Chains (Ethereum, Base, Polygon)**:
1. Access PayRam dashboard → Wallet Management
2. Select blockchain → Deploy Contract
3. Connect MetaMask/wallet
4. Provide: Master Account, Cold Wallet Address, Wallet Name
5. Confirm deployment and save contract address

**TRON**:
- Same flow using TronLink wallet
- Separate contract deployment required

**Bitcoin**:
- No smart contract—uses HD wallet derivation
- Enter 12-word seed phrase (encrypted locally on mobile app only)

### Phase 3: Hot Wallet Configuration

Hot wallets pay gas fees for sweep operations. Must maintain balance:

| Chain | Gas Token | Recommended Balance |
|-------|-----------|---------------------|
| Ethereum | ETH | 0.1-0.5 ETH |
| Base | ETH | 0.05-0.2 ETH |
| Polygon | MATIC | 50-200 MATIC |
| TRON | TRX | 100-500 TRX |

Add hot wallets via: Wallet Management → Hot Wallet → Add existing wallet with private key.

### Phase 4: SSL Configuration

```bash
# Using Let's Encrypt
certbot certonly --standalone -d payments.yourdomain.com

# Configure in PayRam
# Settings → SSL → Upload certificate and key
```

### Phase 5: API Key Generation

1. Settings → Account → Select Project
2. Open API Keys section
3. Copy auto-generated key (unique per project)

## MCP Server for Guided Setup

Use the PayRam MCP server for automated setup assistance:

```bash
git clone https://github.com/PayRam/payram-helper-mcp-server
cd payram-helper-mcp-server
yarn install && yarn dev
```

### Setup Tools

| Tool | Purpose |
|------|---------|
| `generate_env_template` | Create .env with all required variables |
| `generate_setup_checklist` | Step-by-step deployment runbook |
| `suggest_file_structure` | Recommended project organization |
| `test_payram_connection` | Validate API connectivity |

## Architecture: Why Self-Hosted Matters

**What you own**:
- Server and all data
- Database with transaction history
- Smart contracts you deployed
- Cold wallet private keys (offline)
- Complete policy control

**What PayRam provides**:
- Software that runs on your server
- Smart contract templates
- Dashboard and API layer
- No access to your funds or data

**Permanence**: Once deployed, your infrastructure works independently. PayRam cannot disable, freeze, or restrict your payment processing.

## Production Checklist

- [ ] SSH key auth only (disable password)
- [ ] Firewall configured (only 8080/8443 exposed)
- [ ] SSL certificate installed
- [ ] Hot wallets funded for gas
- [ ] Cold wallet addresses verified
- [ ] Backup procedures documented
- [ ] Monitoring configured (Prometheus/Grafana recommended)

## All PayRam Skills

| Skill | What it covers |
|-------|---------------|
| `payram-setup` | Server config, API keys, wallet setup, connectivity test |
| `payram-crypto-payments` | Architecture overview, why PayRam, MCP tools |
| `payram-payment-integration` | Quick-start payment integration guide |
| `payram-self-hosted-payment-gateway` | Deploy and own your payment infrastructure |
| `payram-checkout-integration` | Checkout flow with SDK + HTTP for 6 frameworks |
| `payram-webhook-integration` | Webhook handlers for Express, Next.js, FastAPI, Gin, Laravel, Spring Boot |
| `payram-stablecoin-payments` | USDT/USDC acceptance across EVM chains and Tron |
| `payram-bitcoin-payments` | BTC with HD wallet derivation and mobile signing |
| `payram-payouts` | Send crypto payouts and manage referral programs |
| `payram-no-kyc-crypto-payments` | No-KYC, no-signup, permissionless payment acceptance |

## Support

Need help? Message the PayRam team on Telegram: [@PayRamChat](https://t.me/PayRamChat)

- Website: https://payram.com
- GitHub: https://github.com/PayRam
- MCP Server: https://github.com/PayRam/payram-helper-mcp-server
