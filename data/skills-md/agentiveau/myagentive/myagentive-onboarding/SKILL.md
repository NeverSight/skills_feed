---
name: myagentive-onboarding
description: Onboard new MyAgentive users, explain capabilities, and help set up integrations. Use when welcoming new users, explaining what MyAgentive can do, checking integration status, or helping configure API keys and services.
---

# MyAgentive Onboarding

Use this skill when onboarding new users, explaining MyAgentive capabilities, or helping users set up integrations.

## What is MyAgentive?

MyAgentive is your personal AI agent that runs on your machine (or a cloud server) and can perform real tasks autonomously. Unlike chatbots that only provide information, MyAgentive can:

- Create and deploy websites
- Post to social media
- Generate images, audio, and video
- Transcribe audio/video content
- Make phone calls and send SMS
- Read and send emails
- Create and edit documents (Word, Excel, PowerPoint, PDF)
- Control your Android phone remotely
- Manage your online presence
- Automate repetitive tasks

## Capability Categories

### 1. Communication
| Capability | Skill | Setup Required |
|------------|-------|----------------|
| Phone calls with AI voice | `twilio-phone` | Twilio + ElevenLabs |
| SMS messages | `twilio-phone` | Twilio |
| Email (read/send) | `email-himalaya` | himalaya CLI |
| Telegram notifications | Core | Already configured |

### 2. Content Creation
| Capability | Skill | Setup Required |
|------------|-------|----------------|
| Image generation | `gemini-imagen` | Gemini API key |
| Audio/video transcription | `deepgram-transcription` | Deepgram API key |
| Voice synthesis | `twilio-phone` | ElevenLabs API key |

### 3. Social Media
| Capability | Skill | Setup Required |
|------------|-------|----------------|
| LinkedIn posts | `social-media-poster` | LinkedIn API |
| Twitter/X posts | `social-media-poster` | Twitter API |

### 4. Documents
| Capability | Skill | Setup Required |
|------------|-------|----------------|
| Word documents (.docx) | `docx` | None |
| Excel spreadsheets (.xlsx) | `xlsx` | None |
| PowerPoint presentations (.pptx) | `pptx` | None |
| PDF manipulation | `pdf` | None |

### 5. Device Control
| Capability | Skill | Setup Required |
|------------|-------|----------------|
| Android phone control | `android-use` | ADB + USB connection |

### 6. Web Hosting (External)
| Capability | Provider | Setup Required |
|------------|----------|----------------|
| Static websites | Cloudflare Pages | Cloudflare account |
| Serverless functions | Cloudflare Workers | Cloudflare account |
| Custom domains | Cloudflare DNS | Cloudflare account |

---

## Quick Start: Check Integration Status

To see what is configured, check the config file:

```bash
# List configured API keys (values hidden)
grep -E "_KEY|_TOKEN|_SECRET|_SID" ~/.myagentive/config | cut -d'=' -f1

# Or use the validation script
python .claude/skills/myagentive/scripts/check_config.py
```

---

## Integration Setup Guides

### Already Configured (Core)

These are set up during initial MyAgentive installation:

| Integration | Variables | Status |
|-------------|-----------|--------|
| Telegram | `TELEGRAM_BOT_TOKEN`, `TELEGRAM_USER_ID` | Required |
| Web Interface | `WEB_PASSWORD`, `PORT` | Required |

---

### Deepgram (Transcription)

**Free Credit:** $200 for new accounts

**What it enables:**
- Transcribe voice messages in Telegram
- Convert audio files to text
- Transcribe video files
- Multiple language support

**Setup:**
1. Sign up: https://console.deepgram.com/signup
2. Go to API Keys > Create new key
3. Add to config:
   ```bash
   echo "DEEPGRAM_API_KEY=your_key" >> ~/.myagentive/config
   ```

**Skill:** `deepgram-transcription`

---

### Gemini (Image Generation)

**Free Tier:** Limited requests per minute

**What it enables:**
- Generate images from text descriptions
- Multiple quality levels (fast, balanced, ultra)

**Setup:**
1. Get API key: https://aistudio.google.com/apikey
2. Add to config:
   ```bash
   echo "GEMINI_API_KEY=your_key" >> ~/.myagentive/config
   ```

**Skill:** `gemini-imagen`

---

### ElevenLabs (Voice Synthesis)

**Free Tier:** 10,000 characters/month

**What it enables:**
- Natural AI voices for phone calls
- Multiple voice options and accents
- Text-to-speech conversion

**Setup:**
1. Sign up: https://elevenlabs.io
2. Go to Profile > API Keys
3. Add to config:
   ```bash
   echo "ELEVENLABS_API_KEY=your_key" >> ~/.myagentive/config
   ```

**Skill:** `twilio-phone`

---

### Twilio (Phone & SMS)

**What it enables:**
- Make phone calls with AI voices
- Send SMS messages
- Receive call/SMS notifications

**Setup:**
1. Sign up: https://www.twilio.com
2. Get a phone number
3. Install CLI: `brew tap twilio/brew && brew install twilio`
4. Login: `twilio login`
5. Optionally add to config for reference:
   ```bash
   echo "TWILIO_PHONE_NUMBER=+1234567890" >> ~/.myagentive/config
   ```

**Note:** Twilio uses CLI authentication, not environment variables.

**Skill:** `twilio-phone`

---

### LinkedIn (Social Media)

**What it enables:**
- Post updates to your profile
- Share articles and content
- Post to company pages

**Requirement:** LinkedIn Company Page

**Setup:**
1. Create app: https://www.linkedin.com/developers/apps
2. Request "Share on LinkedIn" permission
3. Get Client ID, Client Secret from app settings
4. Generate access token using OAuth flow:
   ```bash
   cd .claude/skills/social-media-poster
   source venv/bin/activate
   python scripts/get_token.py
   ```
5. Add to config:
   ```bash
   echo "LINKEDIN_CLIENT_ID=your_id" >> ~/.myagentive/config
   echo "LINKEDIN_CLIENT_SECRET=your_secret" >> ~/.myagentive/config
   echo "LINKEDIN_ACCESS_TOKEN=your_token" >> ~/.myagentive/config
   ```

**Note:** Tokens expire after ~60 days. Re-run `get_token.py` to refresh.

**Skill:** `social-media-poster`

---

### Twitter/X (Social Media)

**Free Tier:** 1,500 tweets/month

**What it enables:**
- Post tweets
- Schedule content
- Share media

**Setup:**
1. Apply for developer access: https://developer.x.com
2. Create app with Read+Write permissions
3. Generate all tokens (API Key, Secret, Access Token, Access Token Secret, Bearer Token)
4. Add to config:
   ```bash
   echo "TWITTER_API_KEY=your_key" >> ~/.myagentive/config
   echo "TWITTER_API_SECRET=your_secret" >> ~/.myagentive/config
   echo "TWITTER_ACCESS_TOKEN=your_token" >> ~/.myagentive/config
   echo "TWITTER_ACCESS_TOKEN_SECRET=your_secret" >> ~/.myagentive/config
   echo "TWITTER_BEARER_TOKEN=your_bearer" >> ~/.myagentive/config
   ```

**Important:** After changing permissions, regenerate all tokens.

**Skill:** `social-media-poster`

---

### Email (himalaya)

**What it enables:**
- Read emails from any account
- Send emails
- Search and manage mailboxes

**Setup:**
1. Install himalaya: `brew install himalaya`
2. Configure accounts in `~/.config/himalaya/config.toml`
3. For Gmail, create an App Password:
   - Go to: https://myaccount.google.com/apppasswords
   - Store in macOS Keychain:
     ```bash
     security add-generic-password -s himalaya-gmail -a "you@gmail.com" -w "your-app-password"
     ```

**Skill:** `email-himalaya`

---

### Android Device Control

**What it enables:**
- Tap buttons and navigate apps
- Type text
- Take screenshots
- Automate phone tasks

**Setup:**
1. Install ADB: `brew install android-platform-tools`
2. Enable Developer mode on Android (tap Build Number 7 times)
3. Enable USB debugging in Developer options
4. Connect phone via USB and authorise
5. Verify: `adb devices -l`
6. Optional (for vision-based detection):
   ```bash
   echo "OPENAI_API_KEY=your_key" >> ~/.myagentive/config
   ```

**Skill:** `android-use`

---

### Cloudflare (Web Hosting)

**Free Tier:** Generous limits for Pages, Workers, DNS

**What it enables:**
- Deploy static websites (Cloudflare Pages)
- Create serverless functions (Workers)
- Manage DNS and custom domains

**Setup:**
1. Sign up: https://dash.cloudflare.com/sign-up
2. Create API Token: https://dash.cloudflare.com/profile/api-tokens
3. Permissions needed:
   - Account > Cloudflare Pages: Edit
   - Account > Workers Scripts: Edit
   - Zone > DNS: Edit
4. Add to config:
   ```bash
   echo "CLOUDFLARE_API_TOKEN=your_token" >> ~/.myagentive/config
   echo "CLOUDFLARE_ACCOUNT_ID=your_account_id" >> ~/.myagentive/config
   ```

---

### Google Analytics & Search Console

**What it enables:**
- Track website visitors
- Monitor search performance
- SEO insights

**Setup (Analytics):**
1. Create property: https://analytics.google.com
2. Get Measurement ID (G-XXXXXXXXXX)
3. Add to config:
   ```bash
   echo "GOOGLE_ANALYTICS_ID=G-XXXXXXXXXX" >> ~/.myagentive/config
   ```

**Setup (Search Console):**
1. Add site: https://search.google.com/search-console
2. Verify ownership
3. For API access, create GCP Service Account with Search Console access

---

### GCP Service Account

**What it enables:**
- Access Google APIs (Sheets, Drive, Calendar)
- Cloud Storage
- BigQuery, Vision, Speech, Translation APIs

**Setup:**
1. Create project: https://console.cloud.google.com
2. Create Service Account (IAM & Admin > Service Accounts)
3. Download JSON key file
4. Save to secure location and set:
   ```bash
   echo "GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json" >> ~/.myagentive/config
   echo "GCP_PROJECT_ID=your-project-id" >> ~/.myagentive/config
   ```

---

## Recommended Setup Order

### Essential (Start Here)
1. **Deepgram** - $200 free credit, enables voice message transcription
2. **Gemini** - Free tier, enables image generation

### Communication
3. **ElevenLabs** - Natural AI voices
4. **Twilio** - Phone calls and SMS
5. **Email (himalaya)** - Email access

### Social Media
6. **Twitter/X** - Social presence
7. **LinkedIn** - Professional presence

### Web Hosting
8. **Cloudflare** - Website deployment

### Advanced
9. **Android Control** - Phone automation
10. **GCP Service Account** - Google Workspace automation

---

## Document Skills (No Setup Required)

These skills work out of the box:

| Skill | Description |
|-------|-------------|
| `docx` | Create, edit, and read Word documents |
| `xlsx` | Create, edit, and analyse Excel spreadsheets |
| `pptx` | Create and edit PowerPoint presentations |
| `pdf` | Extract text, merge, split, and fill PDF forms |

---

## How to Add an Integration

Simply ask:
- "Set up Deepgram integration"
- "Help me configure Twitter"
- "I want to add ElevenLabs"

I will guide you through the process step by step.

---

## Security Notes

- All API keys are stored in `~/.myagentive/config`
- This file is only readable by your user account
- Never share your API keys publicly
- You can revoke any API key from the provider's dashboard
- Keys are never displayed in full in responses

---

## Need Help?

Ask me:
- "What can you do?" - Overview of capabilities
- "What integrations are available?" - List all integrations
- "Check my integration status" - See what is configured
- "Help me set up [integration name]" - Step-by-step setup guide
