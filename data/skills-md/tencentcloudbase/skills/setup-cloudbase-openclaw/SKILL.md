---
name: setup-cloudbase-openclaw
description: Configure Moltbot/OpenClaw for CloudBase full-stack development. Checks ~/.openclaw/ or ~/.clawdbot/ config, finds workspace directory, updates AGENTS.md, and configures mcporter with CloudBase MCP. Guides users to get environment ID and API keys.
---

# Setup CloudBase for OpenClaw/Moltbot

This skill guides you through configuring your OpenClaw/Moltbot installation for CloudBase full-stack development.

## Prerequisites

Before starting, ensure you have:
- A Tencent Cloud account with CloudBase enabled
- Access to your CloudBase environment ID and credentials

## Quick Setup Overview

| Step | Action | Purpose |
|------|--------|---------|
| 1 | Check installation dirs | Find where OpenClaw/Moltbot is installed |
| 2 | Locate workspace | Identify the agent workspace directory |
| 3 | Configure MCP | Set up CloudBase MCP with credentials |
| 4 | Update AGENTS.md | Add CloudBase development rules |
| 5 | Install skills | Install CloudBase-related skills |
| 6 | Copy app template (optional) | Copy CloudBase React template to workspace |
| 7 | Apply changes | Use /new to start a new session |

---

## Step 1: Check Installation Directories

First, identify which directory your installation uses:

```bash
# Check for OpenClaw directory
ls -la ~/.openclaw/

# Or check for Moltbot directory
ls -la ~/.clawdbot/

# Or check for standard moltbot config
ls -la ~/.moltbot/
```

**What to look for:**
- Configuration file: `moltbot.json` or `config.json`
- Workspace path defined in the config
- Existing `skills/` directory

**Run the setup script to auto-detect:**

```bash
bash <(curl -s https://raw.githubusercontent.com/tencentcloudbase/skills/main/scripts/detect-setup.sh)
```

Or use the Node.js version:

```bash
npx @cloudbase/setup-openclaw detect
```

---

## Step 2: Locate Workspace Directory

The workspace is where your agent reads/writes files and where AGENTS.md lives.

Find it in your config:

```bash
# Read config and find workspace
cat ~/.openclaw/moltbot.json | grep '"workspace"'
# or
cat ~/.clawdbot/moltbot.json | grep '"workspace"'
# or
cat ~/.moltbot/moltbot.json | grep '"workspace"'
```

**Common default workspaces:**
- `~/clawd/` - Default for many installations
- `~/.openclaw/workspace/` - OpenClaw default
- Custom path specified in your config

**Note this path** — you'll need it for Step 4.

---

## Step 3: Configure CloudBase MCP

### 3.1 Get Your CloudBase Credentials

You need three values:

1. **Environment ID (EnvId)** - Your CloudBase environment identifier
2. **SecretId** - Tencent Cloud API Secret ID
3. **SecretKey** - Tencent Cloud API Secret Key

**How to get them:**

1. **EnvId**: Go to [CloudBase Console](https://tcb.cloud.tencent.com)
   - Select your environment
   - Copy the Environment ID from the top-left corner

2. **SecretId & SecretKey**: Go to [CAM API Key Management](https://console.cloud.tencent.com/cam/capi)
   - Create a new API key or use existing
   - Copy both SecretId and SecretKey

### 3.2 Create or Update mcporter Config

In your **workspace directory**, create or update `config/mcporter.json`:

```bash
# First, create the config directory if it doesn't exist
mkdir -p <workspace>/config

# Then create the mcporter.json file
nano <workspace>/config/mcporter.json
```

**Add the following configuration:**

```json
{
  "mcpServers": {
    "cloudbase-mcp": {
      "description": "CloudBase MCP",
      "command": "npx",
      "args": ["@cloudbase/cloudbase-mcp@latest"],
      "env": {
        "TENCENTCLOUD_SECRETID": "your_secret_id_here",
        "TENCENTCLOUD_SECRETKEY": "your_secret_key_here",
        "CLOUDBASE_ENV_ID": "your_env_id_here"
      }
    }
  }
}
```

**用户必须提供**以下三项并替换占位符，MCP 才能正常调用云开发：

**如何获取：**
- **TENCENTCLOUD_SECRETID / TENCENTCLOUD_SECRETKEY**：登录 [腾讯云控制台](https://console.cloud.tencent.com) → 访问管理 [API 密钥](https://console.cloud.tencent.com/cam/capi) → 创建或查看密钥，得到 SecretId 与 SecretKey。
- **CLOUDBASE_ENV_ID**：登录 [云开发控制台](https://tcb.cloud.tencent.com/dev) → 选择环境 → 在「概览」或「设置」中查看「环境 ID」（形如 `xxx-xxxxx`）。

### 3.3 Verify MCP Configuration

Test that mcporter can load the configuration:

```bash
cd <workspace>
npx mcporter list
```

You should see `cloudbase-mcp` in the list of available MCP servers.

---

## Step 4: Update AGENTS.md

Add CloudBase development rules to your workspace's AGENTS.md.

**If AGENTS.md doesn't exist, create it:**

```bash
nano <workspace>/AGENTS.md
```

**Add the following CloudBase section:**

```markdown
## CloudBase Development

When working with CloudBase projects, the agent MUST:

1. **Read skills first** - Before writing any code, read the relevant CloudBase skills:
   - `cloudbase-guidelines` - Essential development guidelines
   - `web-development` - For web apps with static hosting
   - `miniprogram-development` - For WeChat mini programs
   - `cloud-functions` - For cloud function development
   - `auth-web-cloudbase` - For web authentication
   - `cloudbase-document-database-web-sdk` - For document database operations

2. **Use MCP, not CLI** - All CloudBase operations must go through CloudBase MCP tools:
   - Environment queries via MCP
   - Database configuration via MCP
   - Cloud function deployment via MCP
   - Do NOT use the CloudBase CLI (it requires interactive login)

3. **Prefer SDK + security rules** - If the requirement can be satisfied with the document database SDK and security rules alone, do NOT introduce cloud functions.

4. **Deploy to subdirectory (mandatory)** - When deploying web apps to static hosting, you MUST use a subdirectory path (e.g., `/my-app/`), not the root, unless the user explicitly asks otherwise.

5. **Auto-deploy web apps** - After completing a web application, automatically deploy it to CloudBase static hosting using MCP tools.
```

---

## Step 5: Install CloudBase Skills

Install the CloudBase skills package to make all CloudBase-related skills available:

```bash
# Option 1: Install to workspace skills (single workspace)
cd <workspace>
npx skills add tencentcloudbase/skills -y

# Option 2: Install to shared skills (all agents on this machine)
npx skills add tencentcloudbase/skills -y --workdir ~/.openclaw/skills
# or
npx skills add tencentcloudbase/skills -y --workdir ~/.clawdbot/skills
```

**Verify installation:**

```bash
ls skills/ | grep cloudbase
```

You should see skills like:
- `cloudbase-guidelines`
- `web-development`
- `miniprogram-development`
- `cloud-functions`
- `auth-web-cloudbase`
- etc.

---

## Step 6: Copy App Template (Optional)

The workspace includes a **CloudBase + React template** (`app/` directory) that you can copy as a starting point for new projects.

**What's included in the template:**

- React 19 + Vite 6 + TypeScript
- Tailwind CSS + DaisyUI
- CloudBase Web SDK integration
- Example project (Swimming Tracker)
- Build configuration and deployment scripts

**To copy the template to your workspace:**

```bash
# Option 1: Copy to a new project directory
cp -r <workspace>/app <workspace>/my-new-project

# Option 2: Use the setup script to copy
npx @cloudbase/setup-openclaw copy-template --dest <workspace>/my-project
```

**After copying, update the configuration:**

1. **Update `cloudbaserc.json`** - Replace `{{env.ENV_ID}}` with your actual Environment ID
2. **Install dependencies:**
   ```bash
   cd <workspace>/my-new-project
   npm install
   ```
3. **Run development server:**
   ```bash
   npm run dev
   ```
4. **Build for production:**
   ```bash
   npm run build
   ```

**Template structure:**

```
app/
├── src/
│   ├── components/         # React components
│   ├── types/             # TypeScript types
│   ├── utils/             # Utilities (CloudBase SDK, API)
│   └── main.tsx           # App entry point
├── public/                # Static assets
├── cloudfunctions/        # Cloud functions (optional)
├── cloudbaserc.json       # CloudBase deployment config
├── vite.config.ts         # Vite build config
├── tailwind.config.js     # Tailwind CSS config
├── tsconfig.json          # TypeScript config
└── package.json           # Dependencies and scripts
```

---

## Step 7: Apply Changes

Use **/new** to start a new session so the agent picks up the updated configuration (AGENTS.md, MCP, skills).

---

## Verification

To verify everything is working correctly:

1. **Check MCP is available:**
   ```
   Ask the agent: "List available MCP tools"
   Should see CloudBase-related tools
   ```

2. **Check skills are loaded:**
   ```
   Ask the agent: "What CloudBase skills do you have?"
   Should list cloudbase-guidelines, web-development, etc.
   ```

3. **Test a CloudBase query:**
   ```
   Ask the agent: "Check my CloudBase environment info"
   Should use MCP to query environment details
   ```

---

## Troubleshooting

### MCP not showing up

1. Verify mcporter.json syntax is valid JSON
2. Check that credentials are correct (no extra spaces)
3. Restart the gateway after config changes
4. Run `npx mcporter list` to verify MCP servers

### Skills not loading

1. Check that skills are in the correct directory
2. Verify SYMLINKS are created correctly in `<workspace>/skills/`
3. Restart the gateway after installing skills
4. Check file permissions on skill directories

### Workspace not found

1. Verify the workspace path in your config file
2. Ensure AGENTS.md exists in the workspace root
3. Check that the agent has read/write permissions

---

## Reference: OpenClaw Skills Loading

OpenClaw loads skills from multiple locations, in priority order:

1. **Workspace skills** (`<workspace>/skills/`) - Highest priority, single workspace
2. **Managed skills** (`~/.openclaw/skills/` or `~/.clawdbot/skills/`) - All agents
3. **Bundled skills** - Installation default, lowest priority

**Tip:** Install CloudBase skills to managed skills (`~/.openclaw/skills/`) to make them available to all agents on the system.

---

## Need Help?

- [CloudBase MCP Documentation](https://github.com/ TencentCloudBase/cloudbase-mcp)
- [CloudBase Console](https://tcb.cloud.tencent.com)
- [Skills Hub](https://skills.sh/)
- [OpenClaw Documentation](https://docs.molt.bot)
