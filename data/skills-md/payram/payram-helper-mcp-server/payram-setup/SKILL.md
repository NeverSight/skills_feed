---
name: payram-setup
description: Deploy and configure your PayRam self-hosted crypto payment gateway server. Install on VPS, set up PostgreSQL database, configure root account, node details, wallets, and hot wallets. Complete deployment and onboarding in under 10 minutes. No signup required — fully self-hosted. Use when deploying PayRam for the first time, setting up server infrastructure, or configuring the PayRam dashboard.
---

# PayRam Setup

> **This is the deployment and onboarding guide for PayRam.** Deploy the PayRam server on your VPS and configure the dashboard before integrating payments into your application.

## What is PayRam?

PayRam is a self-hosted crypto payment gateway. You deploy it on your own server — no signup, no KYC, no third-party custody. Accept USDT, USDC, Bitcoin, and ETH across Ethereum, Base, Polygon, and Tron.

---

## Part 1: Deploy PayRam Server

### Prerequisites

**Server Requirements:**
- **CPU**: 4 cores
- **RAM**: 4 GB
- **Storage**: 50 GB SSD
- **OS**: Ubuntu 22.04
- **Ports**: 80, 443, 8080, 8443, 5432

**Database Requirements:**
- **Engine**: PostgreSQL
- **vCPUs**: 2 CPU cores
- **Memory**: 8 GB
- **Storage**: 50 GB SSD

**Recommended VPS Providers:** AWS, Google Cloud, Azure, Hetzner, Hostinger

### Quick Setup (Recommended - 10 Minutes)

1. **Connect to your VPS via SSH**

2. **Choose network** (mainnet or testnet)

3. **Run the installation script:**
```bash
curl -fsSL https://raw.githubusercontent.com/PayRam/payram-server/main/install.sh | bash
```

4. **Follow the interactive prompts:**
   - Enter PostgreSQL connection details
   - Set encryption keys
   - Configure domain/IP address
   - Choose SSL certificate options

5. **Wait for installation to complete** (~5-10 minutes)

The script automatically:
- Installs dependencies
- Sets up Docker containers
- Configures database connections
- Generates SSL certificates (if using Let's Encrypt)
- Starts PayRam services

### Advanced Setup (Docker)

For manual Docker deployment with custom configurations:

1. **Clone the repository:**
```bash
git clone https://github.com/PayRam/payram-server.git
cd payram-server
```

2. **Configure environment variables:**
```bash
cp .env.example .env
nano .env  # Edit with your database, encryption keys, domain
```

3. **Start with Docker Compose:**
```bash
docker compose up -d
```

4. **Verify services are running:**
```bash
docker compose ps
```

For detailed Docker setup instructions, see the PayRam deployment documentation.

---

## Part 2: Onboard Your PayRam Instance

After the server is installed and running, complete the onboarding configuration through the dashboard.

### Step 1: Create Root Account

1. **Navigate to signup page:**
   - Open `http://<your-ip-address>/signup` in your browser
   - Replace `<your-ip-address>` with your server's IP or domain

2. **Set root email:**
   - Enter your admin email (you'll use this to log in)
   - This becomes your root/administrator account

3. **Set root password:**
   - Create a strong password and store it securely
   - You can change it later in dashboard settings

4. **Create your first project:**
   - Enter a project name (e.g., "My E-commerce Store")
   - Projects represent different products/websites using PayRam

### Step 2: Configure Node Details

After logging in, configure blockchain node connections:

1. **Go to Settings → Node Details**

2. **For each chain you want to support:**
   - Enter RPC endpoint URLs (public or private)
   - Recommended: Use dedicated node providers for production
   - Example providers: Alchemy, Infura, QuickNode, GetBlock

3. **Test connections** to verify nodes are accessible

**Supported Chains:**
- Ethereum (Mainnet/Testnet)
- Base (Mainnet/Testnet)
- Polygon (Mainnet/Testnet)
- Tron (Mainnet/Testnet)
- Bitcoin (Mainnet/Testnet)

### Step 3: Configure Wallets

Set up your wallet infrastructure:

1. **Go to Settings → Wallets**

2. **For each chain, configure:**
   - **Sweep Contract Address** (deploy once per chain)
   - **Cold Wallet Address** (where funds are swept to)
   - **Hot Wallet** (for gas fees and instant payouts)

3. **Deploy sweep contracts** using the provided scripts in the dashboard

4. **Fund hot wallets** with native tokens:
   - ETH for Ethereum/Base
   - MATIC for Polygon
   - TRX for Tron
   - BTC for Bitcoin

### Step 4: Set Up Hot Wallets

Configure hot wallets for paying gas fees:

1. **Go to Settings → Hot Wallets**

2. **For each chain:**
   - Generate a hot wallet or import an existing one
   - Fund it with enough native tokens for gas
   - Set auto-refill thresholds (optional)

**Recommended Hot Wallet Balances:**
- Ethereum: 0.5-1 ETH
- Base: 0.1-0.5 ETH
- Polygon: 100-500 MATIC
- Tron: 1000-5000 TRX

### Step 5: Configure Funds Sweeping

Set up automatic fund sweeping to your cold wallet:

1. **Go to Settings → Sweeping Configuration**

2. **Configure sweep rules:**
   - Minimum balance threshold before sweep
   - Sweep schedule (e.g., every 6 hours)
   - Gas price limits

3. **Enable auto-sweep** for each chain

4. **Test sweep** with a small payment to verify everything works

### Step 6: Generate API Keys

Create API keys for your application:

1. **Go to Settings → API Keys**

2. **Generate a new API key** for your project

3. **Copy and securely store:**
   - `PAYRAM_API_KEY` (for authentication)
   - `PAYRAM_BASE_URL` (your server's URL)

4. **Use these in your application's `.env` file**

---

## Part 3: Test Your Setup

After completing deployment and onboarding, verify everything works:

### Test Payment Link

1. **Go to Payment Links in the dashboard**
2. **Create a test payment** (e.g., $1 USD)
3. **Complete the checkout flow**
4. **Verify payment appears** in dashboard
5. **Check funds swept** to cold wallet

### Verify API Access

Test your API key works:

```bash
curl -X POST https://your-server.com/api/v1/payment \
  -H "API-Key: your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "customerEmail": "test@example.com",
    "customerId": "test-123",
    "amountInUSD": 1
  }'
```

Expected response:
```json
{
  "reference_id": "ref_...",
  "url": "https://your-server.com/checkout/...",
  "host": "your-server.com"
}
```

---

## Troubleshooting Setup Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Can't access dashboard | Firewall blocking ports | Open ports 80, 443, 8080, 8443 |
| Database connection error | Wrong credentials | Check PostgreSQL connection string in `.env` |
| SSL certificate error | Domain not configured | Use HTTP for testing, or configure Let's Encrypt |
| Node RPC failing | Invalid endpoint | Verify RPC URL and API key with provider |
| Sweep not working | Hot wallet empty | Fund hot wallet with native tokens |
| API 401 error | Wrong API key | Regenerate in Settings → API Keys |

---

---

## Next Steps

After your PayRam server is deployed and configured, start integrating it into your application:

- **Integrate payments into your app** → `payram-payment-integration`
- **Complete checkout implementation** → `payram-checkout-integration`
- **Handle webhooks** → `payram-webhook-integration`
- **Send payouts** → `payram-payouts`
- **Learn about stablecoin payments** → `payram-stablecoin-payments`

---

## MCP Server Tools

For automated setup assistance, use the PayRam MCP server:

| Tool | Purpose |
|------|---------|
| `generate_env_template` | Create .env with all required variables |
| `generate_setup_checklist` | Step-by-step deployment runbook |
| `test_payram_connection` | Validate API connectivity |

---

## All PayRam Skills

| Skill | What it covers |
|-------|---------------|
| `payram-setup` | Deploy PayRam server, configure dashboard, wallets, and hot wallets |
| `payram-crypto-payments` | Architecture overview, why PayRam, MCP tools |
| `payram-payment-integration` | Integrate payments into your application code |
| `payram-self-hosted-payment-gateway` | Deep dive into PayRam infrastructure and deployment |
| `payram-checkout-integration` | Build complete checkout flows in 6 frameworks |
| `payram-webhook-integration` | Handle payment webhooks in Express, Next.js, FastAPI, etc. |
| `payram-stablecoin-payments` | Accept USDT/USDC across EVM chains and Tron |
| `payram-bitcoin-payments` | Bitcoin payments with HD wallets and mobile signing |
| `payram-payouts` | Send crypto payouts and manage referral programs |
| `payram-no-kyc-crypto-payments` | No-KYC, no-signup, permissionless payment acceptance |

---

Need help? Message the PayRam team on Telegram: [@PayRamChat](https://t.me/PayRamChat)

- Website: https://payram.com
- GitHub: https://github.com/PayRam
- MCP Server: https://github.com/PayRam/payram-helper-mcp-server
