---
name: ai-sdr-agent
description: Create an instant AI SDR (Sales Development Representative) agent for any website using HeyGen LiveAvatar. Use this when the user wants to create an AI sales rep, AI SDR, or AI avatar that can talk about a specific website or business.
user-invocable: true
argument-hint: "[website-url]"
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# AI SDR Agent Setup

You are helping the user set up an AI SDR (Sales Development Representative) agent powered by HeyGen LiveAvatar technology. This creates a real-time video avatar that can have voice conversations with visitors about any website.

## Required Information (BOTH are required)

1. **LiveAvatar API Key** (REQUIRED) - Get your free API key from https://app.liveavatar.com/developers (sign in with your HeyGen account)
2. **Website URL** (REQUIRED) - The website the AI SDR should represent. This is NOT optional - you must get both pieces of information from the user before proceeding.

Parse any provided arguments: $ARGUMENTS

**IMPORTANT**: Do not proceed with setup until you have BOTH the API key AND the website URL from the user. Ask for both if not provided.

## Setup Steps

### Step 1: Check for existing project or clone it

```bash
# Check if we're already in the project
if [ -f "package.json" ] && grep -q "liveavatar" package.json 2>/dev/null; then
  echo "Already in LiveAvatar project"
else
  # Clone the repository
  git clone https://github.com/eNNNo/liveavatar-ai-sdr.git ai-sdr-agent
  cd ai-sdr-agent
fi
```

### Step 2: Install dependencies

```bash
npm install
```

### Step 3: Configure API key

Create `.env.local` with the user's API key:

```bash
cat > .env.local << 'EOF'
LIVEAVATAR_API_KEY=<USER_API_KEY>
EOF
```

Replace `<USER_API_KEY>` with the actual key provided by the user.

### Step 4: (Optional) Configure auto-start

If the user wants to skip the onboarding form, also add these to `.env.local`:

```
NEXT_PUBLIC_AUTO_START=true
NEXT_PUBLIC_WEBSITE_URL=<WEBSITE_URL>
NEXT_PUBLIC_USER_NAME=Visitor
```

### Step 5: Start the application

```bash
npm run dev
```

### Step 6: Tell the user

- App is running at **http://localhost:3001**
- Open this URL in browser to create/talk to their AI SDR
- If auto-start is configured, it will immediately start the avatar session
- Session duration: 2 minutes per conversation
- They can create new sessions for different websites

## Error Messages

| Error | Meaning | Solution |
|-------|---------|----------|
| Invalid API key | The LiveAvatar API key is wrong | Check key at https://app.liveavatar.com/developers |
| Website unreachable | Can't fetch the URL | Verify URL is correct and publicly accessible |
| Avatar expired | Default avatar needs renewal | Select different avatar or renew HeyGen subscription |
| Context creation failed | API limit or server issue | Wait and retry, or check HeyGen account status |

## Example Interaction

**User**: "Create an AI SDR for shopify.com using API key abc123"

**You should**:
1. Clone/setup the project
2. Create `.env.local` with `LIVEAVATAR_API_KEY=abc123`
3. Run `npm install && npm run dev`
4. Tell user to open http://localhost:3001 and enter "shopify.com" in the form
