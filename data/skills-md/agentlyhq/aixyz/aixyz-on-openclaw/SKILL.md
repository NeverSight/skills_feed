---
name: aixyz-on-openclaw
description: >-
  Step-by-step guide for openclaw users to build, deploy, and monetise an AI agent with aixyz.
  Covers everything from zero: installing Bun, scaffolding an agent, choosing a deployment option,
  getting a crypto wallet, funding it for on-chain registration, and marketing your agent once it is live.
license: MIT
metadata:
  framework: aixyz
  runtime: bun
  audience: openclaw
---

# aixyz for openclaw Users

This guide is written for openclaw users who want to ship a live, paid AI agent using aixyz. You do **not** need prior coding experience or knowledge of crypto infrastructure — every step is explained from scratch.

> **Quick reference:** The general aixyz skill lives at [skills.sh/agentlyhq/aixyz](https://skills.sh/agentlyhq/aixyz).
> Consult it for full CLI flags and advanced topics. This guide focuses on the path that matters most to openclaw users.

---

## What You Are Building

An **AI agent** that:

1. Runs on the internet at a public URL
2. Accepts work requests from other agents (A2A protocol) and from AI clients like Claude Desktop (MCP protocol)
3. Gets paid per request in crypto via the x402 micropayment protocol
4. Is discoverable on-chain via the ERC-8004 registry

---

## Step 1 — Install Bun

aixyz requires **Bun** (not Node). If you already have Bun ≥ 1.3, skip this step.

```bash
# macOS / Linux
curl -fsSL https://bun.sh/install | bash

# Windows (PowerShell, requires WSL or Windows 10+)
powershell -c "irm bun.sh/install.ps1 | iex"
```

Verify:

```bash
bun --version   # should print 1.3 or higher
```

> **Why Bun?** The aixyz build pipeline uses Bun's native build API and plugin system — this is a hard architectural requirement, not a preference. The CLI (`@aixyz/cli`) cannot run on Node. Bun also includes a built-in test runner, which means no extra test framework is needed. Curious about the full rationale? Read [Why Bun](https://aixyz.sh/getting-started/why-bun).

---

## Step 2 — Scaffold Your Agent

```bash
# Create a new agent project (uses all defaults)
bunx create-aixyz-app my-agent --yes

cd my-agent
```

This creates:

```
my-agent/
  aixyz.config.ts   ← agent name, description, payment config
  app/
    agent.ts        ← your AI agent logic
    tools/          ← tool files (optional)
  package.json
  .env.local        ← API keys (never commit this file)
```

Open `.env.local` and add your LLM provider's API key. The default scaffold uses `@ai-sdk/openai`, so add:

```
OPENAI_API_KEY=sk-...
```

If you prefer a different provider (Anthropic, Google, Amazon Bedrock, etc.), swap the `@ai-sdk/*` adapter in `package.json` and `app/agent.ts`, then set the corresponding env var instead. See [ai-sdk.dev](https://ai-sdk.dev) for the full list of providers.

Run locally to test:

```bash
bun run dev
# Agent is now live at http://localhost:3000
```

> **Testing with an AI agent client?** Install the `use-agently` skill so your AI agent can call your local agent in dev mode:
>
> ```bash
> npx skills add https://github.com/agentlyhq/use-agently --skill use-agently
> ```
>
> This skill lets any AI agent discover and call your locally running agent at `http://localhost:3000`.
> While testing locally, set `"scheme": "free"` so callers are not charged (see [Step 7](#step-7--set-up-payments)).
> Before going to production, switch to `"scheme": "exact"` so your agent earns from every request.

---

## Step 3 — Deploy to the Internet

Your agent needs a **public HTTPS URL** so other agents and clients can reach it. If you already have a preferred hosting platform, use it. If you are starting fresh, here are our recommendations.

### Option A — Vercel (recommended, no server knowledge needed)

Vercel gives you a free HTTPS URL with zero configuration. It is the easiest path.

1. Push your project to a GitHub repository
2. Go to [vercel.com](https://vercel.com) → **Add New Project** → import your repo
3. Set the **Build Command** to `bun run build` and the **Output Directory** to `.vercel/output`
4. Add your LLM provider API key (e.g., `OPENAI_API_KEY`) in the Vercel dashboard under **Settings → Environment Variables**
5. Click **Deploy** — Vercel gives you a URL like `https://my-agent.vercel.app`

Vercel auto-deploys on every push. Your agent is serverless and scales automatically.

### Option B — Railway / Render / Fly.io (persistent server)

Use these if your agent needs to hold state between requests or run background jobs.

| Platform                       | Free tier          | Notes                                |
| ------------------------------ | ------------------ | ------------------------------------ |
| [Railway](https://railway.app) | 5 USD/month credit | Easiest Docker-free deploy           |
| [Render](https://render.com)   | Generous free tier | Sleeps after inactivity              |
| [Fly.io](https://fly.io)       | Free allowance     | More control, steeper learning curve |

For all three: push your repo, connect the platform, set your LLM provider API key (e.g., `OPENAI_API_KEY`) as an environment variable, and follow their deploy wizard. They all detect Bun automatically.

### Option C — Cloud Platform Ingress or Local Tunnel (advanced)

**If you are already running OpenClaw on a cloud platform** (AWS, GCP, Azure, DigitalOcean, etc.), the simplest path is to expose the agent through that same platform:

- **AWS** — use an Application Load Balancer or API Gateway in front of the process
- **GCP** — use Cloud Run (zero-config container deploy) or a load balancer
- **Azure** — use Azure Container Apps or App Service
- **DigitalOcean** — use App Platform or a Droplet with nginx as a reverse proxy

> 🔒 **Least-privilege rule:** When exposing the agent process, only open the port the agent listens on (default `3000`). Do **not** grant the process broader network, IAM, or filesystem access than it needs to serve HTTP requests.

**If you just need a quick tunnel for local testing**, use ngrok:

```bash
# ngrok — creates a public HTTPS URL that forwards to localhost:3000
npx ngrok http 3000
```

> ⚠️ **Security warning:** Local tunnels are fine for short-lived testing but should **never** be used for a production agent. Anyone who discovers the URL can send requests to your machine. Always use a proper hosting provider for live traffic.

---

## Step 4 — Get a Crypto Wallet

You need a wallet to:

- **Receive payments** from callers of your agent
- **Pay gas fees** when registering on ERC-8004

### Option A — Use `use-agently` (simplest, recommended for openclaw users)

`use-agently` is the simplest wallet for the aixyz ecosystem. It is designed for the circular economy of agents paying agents.

When prompted during `aixyz erc-8004 register`, select **"Generate a new wallet"** and the CLI will create one for you and display the private key.

> 🔐 **Private key security — read this carefully:**
>
> - **Never share your private key with anyone.** Anyone who has it controls your funds.
> - **Never commit it to git** or paste it in public channels (Discord, Slack, GitHub, etc.).
> - Write it down offline and store it somewhere safe (e.g., a password manager).
> - For a production agent that earns significant income, consider a hardware wallet (Ledger, Trezor).

### Option B — MetaMask (browser extension)

1. Install [MetaMask](https://metamask.io) in your browser
2. Create a new wallet — MetaMask gives you a **seed phrase** (12 words); write it down somewhere safe, never share it
3. Copy your wallet address (starts with `0x…`)

### Option C — Any EVM-compatible wallet

Any wallet that supports Ethereum-compatible networks works: Coinbase Wallet, Rabby, Frame, etc.

> **Your wallet address is your "bank account number."** You share it publicly. Your **private key / seed phrase is your password** — never share it, never commit it to code.

---

## Step 5 — Get Crypto for Registration

Registering on ERC-8004 costs a small gas fee (a fraction of a dollar). You need the native coin of your chosen network.

| Network          | Coin needed | Where to get it                                                                                |
| ---------------- | ----------- | ---------------------------------------------------------------------------------------------- |
| Ethereum mainnet | ETH         | [Coinbase](https://coinbase.com), [Binance](https://binance.com), [Kraken](https://kraken.com) |
| BNB Smart Chain  | BNB         | [Binance](https://binance.com)                                                                 |
| Base             | ETH         | [Coinbase](https://coinbase.com) (Base is a Coinbase L2)                                       |
| Polygon          | POL         | [Coinbase](https://coinbase.com), [Binance](https://binance.com)                               |

**Recommended network: Base.** The x402 payment facilitator is primarily deployed on Base, so your agent will receive payments most reliably there. Base also has very low gas fees — registration typically costs a few cents. Ethereum mainnet gas varies widely and is usually not worth it for getting started. Gas prices on all networks can fluctuate; the amounts above are rough guides only.

**Steps to fund your wallet:**

1. Create an account on any exchange above (identity verification required)
2. Buy a small amount of the relevant coin (a few dollars is enough for registration)
3. Withdraw to your wallet address
4. Wait for the transaction to confirm (~1–5 minutes)

> **No crypto yet?** You can still build and run your agent locally and on Vercel without registration. Register once you are ready to be publicly discoverable.

---

## Step 6 — Register on ERC-8004

ERC-8004 is an on-chain registry that makes your agent **discoverable** by other agents, platforms, and users. It is like a DNS entry but for AI agents.

Once your agent is deployed (Step 3) and you have a funded wallet (Steps 4–5), run:

```bash
# Interactive mode (will prompt you for each setting)
aixyz erc-8004 register

# Non-interactive mode (all values as flags)
aixyz erc-8004 register \
  --url https://my-agent.vercel.app \
  --chain base \
  --broadcast
```

The CLI will ask for (or accept as flags):

| Prompt             | Flag            | What to enter                                      |
| ------------------ | --------------- | -------------------------------------------------- |
| Agent URL          | `--url`         | Your deployed URL from Step 3                      |
| Chain              | `--chain`       | `base` (recommended), `ethereum`, `bsc`, `polygon` |
| Wallet private key | `--private-key` | The key from your wallet (never share this)        |
| Trust mechanisms   | `--trust`       | Accept the default                                 |
| Broadcast          | `--broadcast`   | Pass this flag to actually submit on-chain         |

See all flags:

```bash
aixyz erc-8004 register --help
```

After registration, your agent appears in the ERC-8004 registry and becomes discoverable by the ecosystem.

---

## Step 7 — Set Up Payments

Add an `accepts` export to `app/agent.ts` so callers are charged per request:

```ts
import type { Accepts } from "aixyz/accepts";

// During local testing — callers are not charged
export const accepts: Accepts = { scheme: "free" };

// Production — callers pay $0.005 per request
// export const accepts: Accepts = { scheme: "exact", price: "$0.005" };
```

> **Testing tip:** Use `"scheme": "free"` while developing and testing locally (install the [`use-agently`](#step-2--scaffold-your-agent) skill to call your local agent from an AI client).
> **Before going to production**, switch to `"scheme": "exact"` with a `price` so your agent earns from every request.

Set the wallet address that receives payments in `aixyz.config.ts`:

```ts
export default {
  name: "my-agent",
  // ...
  x402: {
    payTo: "0xYourWalletAddress", // ← paste your address from Step 4
  },
} satisfies AixyzConfig;
```

Or pass it at scaffold time:

```bash
bunx create-aixyz-app my-agent --yes --pay-to 0xYourWalletAddress
```

> Payments flow directly to your wallet — no platform takes a cut.

---

## Step 8 — Go Live Checklist

Before announcing your agent, verify:

- [ ] `bun run dev` works locally and the agent responds correctly
- [ ] Agent is deployed to a public URL (Vercel or similar)
- [ ] LLM provider API key (e.g., `OPENAI_API_KEY`) and any other secrets are set as environment variables on the platform, **not** committed to your repo
- [ ] `aixyz.config.ts` has the correct `name`, `description`, and `payTo` address
- [ ] ERC-8004 registration is complete and the registry shows your agent URL
- [ ] `accepts` export is set so your agent earns from requests

---

## Step 9 — Market Your Agent

> **Registration is only half the work.** Getting on-chain doesn't automatically bring users. You need to actively promote your agent.

### Make it discoverable

- Write a clear, specific `description` in `aixyz.config.ts` — this appears in the A2A agent card and on-chain registry
- Add an `app/icon.png` — a good icon makes your agent stand out in listings
- Post your agent URL and ERC-8004 agent ID in the openclaw community

### Reach potential callers

- Share your `/.well-known/agent-card.json` URL — it is the standard entry point for agent-to-agent discovery
- Add your agent to relevant directories and marketplaces (check [aixyz.sh](https://aixyz.sh) for current listings)
- Write a short demo showing what your agent does and how much it costs — post on X/Twitter, Farcaster, or Discord communities

### Think about pricing

- Too expensive → no callers; too cheap → not worth running
- Start with `$0.001`–`$0.01` per request and adjust based on demand
- Monitor your wallet — incoming transactions tell you who is using your agent and how often

### Keep improving

- Add more tools to make your agent more useful
- Respond to issues and feedback
- Update your on-chain registration if your URL changes: `aixyz erc-8004 update --help`

---

## Troubleshooting

### "command not found: bun"

Restart your terminal after installing Bun, or run `source ~/.bashrc` (Linux) / `source ~/.zshrc` (macOS).

### "API key is not set" / "OPENAI_API_KEY is not set"

Add your LLM provider's API key to `.env.local` (local dev) or to your platform's environment variable settings (production).

### "Transaction failed" during ERC-8004 registration

Your wallet does not have enough gas. Add a few more dollars of the relevant coin and retry.

### Agent is deployed but not responding

Check that your platform's build command is `bun run build` and that all environment variables are set. Check the platform's deploy logs for errors.

### Payment not arriving

Verify your `payTo` address in `aixyz.config.ts` is correct and that you rebuilt and redeployed after changing it.

---

## Further Reading

- [aixyz docs](https://aixyz.sh) — full documentation
- [General aixyz skill](https://skills.sh/agentlyhq/aixyz) — CLI reference for advanced usage
- [ERC-8004 protocol](https://aixyz.sh/protocols/erc-8004) — on-chain identity deep dive
- [x402 payments](https://aixyz.sh/getting-started/payments) — payment protocol details
- [Examples](https://github.com/AgentlyHQ/aixyz/tree/main/examples) — working agents to learn from
