---
name: resend-integration-skills
description: Integrate Resend email service via MCP protocol for AI agents to send emails with Claude Desktop, GitHub Copilot, and Cursor. Set up transactional and marketing emails, configure sender verification, and use AI to automate email workflows.
---

## Links

- **Resend Official**: https://resend.com
- **Resend API Docs**: https://resend.com/docs/api-reference
- **Resend MCP Server**: https://resend.com/docs/knowledge-base/mcp-server
- **Resend MCP GitHub**: https://github.com/resend/mcp-send-email
- **MCP Protocol Spec**: https://modelcontextprotocol.io
- **GitHub MCP Registry**: https://github.com/mcp
- **VS Code Insider Setup**: https://code.visualstudio.com/insiders

## Quick Start

### 1. Prerequisites

- Node.js 20 or higher (required - the MCP server specifies `engines: { "node": ">=20" }`)
- Resend account (free tier available at https://resend.com)
- GitHub Copilot Pro or Cursor with Agent mode enabled
- VS Code Insider (required for full MCP support)
- npm or pnpm package manager

### 2. Clone and Build Resend MCP Server

```bash
# Clone the Resend MCP server repository
git clone https://github.com/resend/mcp-send-email.git
cd mcp-send-email

# Install dependencies (npm or pnpm both supported)
npm install
# or if you prefer pnpm:
# pnpm install

# Build the project (TypeScript compilation + executable permissions)
npm run build
```

The build process:
1. Compiles TypeScript to JavaScript
2. Sets executable permissions on the built script (Unix/macOS)
3. Creates the MCP server executable at `build/index.js`

### 3. Create Resend API Key

1. Visit https://resend.com/api-keys
2. Create a new API key
3. Copy the key to your clipboard (you'll need it for configuration)

### 4. (Optional) Verify Your Domain

To send emails from a custom domain:

1. Go to https://resend.com/domains
2. Add and verify your domain
3. Update MCP configuration with `--sender` flag (see Configuration section)

### 5. Configure MCP for Your Client

Choose your setup based on your GitHub Copilot tier:

**For GitHub Copilot Coding Agent (Repository-level setup):**

This is the recommended approach for team collaboration. Repository admins configure MCP servers at the repository level.

1. Navigate to your repository on GitHub.com
2. Go to Settings → Copilot → Coding agent
3. Add the following JSON configuration:

```json
{
  "mcpServers": {
    "resend": {
      "type": "local",
      "command": "node",
      "args": ["/absolute/path/to/mcp-send-email/build/index.js"],
      "env": {
        "RESEND_API_KEY": "COPILOT_MCP_RESEND_API_KEY"
      },
      "tools": ["*"]
    }
  }
}
```

4. Set up the Copilot environment:
   - Go to Settings → Environments
   - Create new environment called `copilot`
   - Add secret: `COPILOT_MCP_RESEND_API_KEY` with your API key value

5. Click Save and Copilot will validate the configuration

**For VS Code Local Development (Developer setup):**

If you're developing locally or prefer VS Code configuration:

1. Create `.vscode/mcp.json` in your project root:

```json
{
  "servers": {
    "resend": {
      "type": "command",
      "command": "node",
      "args": ["/absolute/path/to/mcp-send-email/build/index.js"],
      "env": {
        "RESEND_API_KEY": "re_xxxxxxxxxxxxxx"
      }
    }
  }
}
```

2. Get the absolute path to `build/index.js`:
   - Right-click `build/index.js` in VS Code → Copy Path

**For Cursor Agent Mode:**

Open Cursor Settings (Cmd+Shift+P → "Cursor Settings") and add to MCP config:

```json
{
  "mcpServers": {
    "resend": {
      "type": "command",
      "command": "node /absolute/path/to/mcp-send-email/build/index.js --key=re_xxxxxxxxxxxxxx"
    }
  }
}
```

**For Claude Desktop:**

1. Open Claude Desktop settings
2. Go to Developer tab → Edit Config
3. Add configuration:

```json
{
  "mcpServers": {
    "resend": {
      "command": "node",
      "args": ["/absolute/path/to/mcp-send-email/build/index.js"],
      "env": {
        "RESEND_API_KEY": "re_xxxxxxxxxxxxxx",
        "SENDER_EMAIL_ADDRESS": "onboarding@resend.dev",
        "REPLY_TO_EMAIL_ADDRESS": "reply@example.com"
      }
    }
  }
}
```

### 6. Test the Connection Using email.md Pattern

The official Resend repository includes a test pattern using an `email.md` file:

1. **Create `email.md` in your project:**
   ```markdown
   to: your-email@example.com
   subject: Test from Resend MCP
   content: This is a test email.

   Hello! This is a test email sent via Resend MCP.
   
   # You can also test CC and BCC:
   # cc: colleague@example.com
   # bcc: manager@example.com
   ```

2. **In Cursor (with Agent mode):**
   - Open the `email.md` file
   - Select all text (`Cmd+A` / `Ctrl+A`)
   - Press `Cmd+L` / `Ctrl+L` (or use the context menu)
   - Tell Cursor: "send this as an email" or "send this email using resend MCP"
   - Make sure you're in Agent mode (toggle in chat dropdown)

3. **In Claude Desktop:**
   - Paste the email.md content in the chat
   - Ask Claude to send it: "Send this email using the resend tool"

4. **In GitHub Copilot:**
   - Open email.md file
   - Reference it in the chat: "@email.md send this email using resend"

If configured correctly, the email will be sent immediately and you'll receive confirmation.

## Key Concepts

### MCP Configuration Types

There are two main ways to configure Resend MCP with GitHub Copilot:

**1. GitHub Copilot Coding Agent (Repository-level)**
- Configuration in GitHub repository settings (Repository admin required)
- Used when assigning Copilot tasks to work on GitHub issues
- Requires explicit `tools` array specifying which tools Copilot can use
- API keys stored as GitHub Actions secrets (prefixed with `COPILOT_MCP_`)
- Autonomous execution without approval (security considerations apply)

**2. VS Code Local Development**
- Configuration in `.vscode/mcp.json` (local developer setup)
- Used for local development with VS Code Insider
- API keys stored directly in config or environment variables
- Better for individual developers or testing

### Resend MCP Server

The Resend MCP Server is a local Node.js application that exposes Resend's email functionality as tools for LLMs. It implements the Model Context Protocol, allowing AI agents to:

- **Send emails** via natural language commands (plain text or HTML)
- **Schedule emails** for future delivery
- **Add recipients** (To, CC, BCC)
- **Configure sender information** (From, Reply-To)
- **Broadcast emails** to audience segments
- **Manage audiences** - List Resend audiences for targeted sending
- **Support HTML and plain text** email bodies

Recent additions (as of early 2026):
- Broadcast and audience management tools for marketing campaigns
- Better error handling and validation via Zod schemas

### MCP Configuration Methods

There are three ways to run the Resend MCP server:

1. **Command-type (VS Code/Cursor)**: Direct Node.js execution with inline arguments
2. **Stdio-type (Claude Desktop)**: Server handles I/O through environment variables
3. **HTTP-type (Remote/Cloud)**: Server exposed via HTTP endpoint

### GitHub Copilot Coding Agent Specifics

For GitHub Copilot Coding Agent (repository-based setup):

- **Required `tools` array**: Must specify which tools from the Resend MCP server Copilot can use
  - Use `"tools": ["send_email", "schedule_email", ...]` to allowlist specific tools
  - Use `"tools": ["*"]` to enable all tools
  - Use case-specific tool names from the MCP server documentation
  
- **No approval required**: Once configured, Copilot will use these tools autonomously without asking
  
- **Security consideration**: Copilot will have automated access to the Resend API via the configured tools, so only enable the tools you need
  
- **Environment variable handling**: API keys must be stored as GitHub Actions secrets with `COPILOT_MCP_` prefix
  - Reference them in config as `"COPILOT_MCP_RESEND_API_KEY"` (without the value)
  - GitHub automatically passes the secret value to the MCP server

### Authentication

Resend MCP server requires:

- **RESEND_API_KEY** (required): Your Resend API key from https://resend.com/api-keys
- **SENDER_EMAIL_ADDRESS** (optional): Verified domain email. If not set, AI will prompt for it
- **REPLY_TO_EMAIL_ADDRESS** (optional): Email address for reply-to header

### Verified Domains

By default, Resend allows sending to your own account email using the test domain `onboarding@resend.dev`. To send to other addresses:

1. **For testing**: Use the default `onboarding@resend.dev` sender (no verification needed)
2. **For custom domains**: Verify your domain at https://resend.com/domains
3. Create a sender email from your verified domain
4. Configure it in MCP environment variables (`SENDER_EMAIL_ADDRESS`)

Note: If you don't provide a `SENDER_EMAIL_ADDRESS`, the MCP server will prompt you each time you send an email.

## Code Examples

### Example 1: Simple Email via Copilot Chat

In VS Code Insider with GitHub Copilot Agent mode:

```
@workspace I need to send a notification email to john@example.com about the project completion. Use the resend MCP tool to send "Project ABC is now live" as the email body.
```

### Example 2: HTML Email with Custom Configuration

```
Send an HTML email to team@example.com with subject "Monthly Report" and body formatted as an HTML table showing Q1 metrics. Use Resend MCP to send it.
```

### Example 3: Email with CC/BCC

```
Send an email from onboarding@mycompany.com to customer@example.com CC'ing manager@company.com about account activation. Use Resend MCP.
```

### Example 4: Scheduled Email

```
Schedule an email to be sent tomorrow at 9 AM using Resend MCP, reminding the team about the standup meeting.
```

### Example 5: Integration with Data Processing

```
Read the CSV file users.csv, extract the top 10 active users with their emails, and send each a personalized thank you email using Resend MCP. Include their usage statistics in the email.
```

## Advanced Features

### Broadcast Emails

Send emails to audience segments in your Resend account:

```
Send a broadcast email to my 'premium_users' audience with subject 'New Feature Release' using Resend MCP
```

### Audience Management

Query and work with audiences:

```
List all my audiences in Resend using the MCP tool
```

## Best Practices

### GitHub Copilot Coding Agent Security

**Important**: When configuring Resend MCP for GitHub Copilot Coding Agent:

1. **Tool allowlisting** - Only enable the specific tools Copilot needs:
   ```json
   "tools": ["send_email", "schedule_email"]
   ```
   Instead of enabling all tools with `"*"`

2. **Secret management** - Never commit API keys to version control
   - Store API keys as GitHub Actions secrets (Settings → Environments)
   - Secret names must start with `COPILOT_MCP_`
   - Reference secrets by name in the configuration

3. **Scope your API key** - Consider using a restricted Resend API key if available

4. **Review Copilot's actions** - Check pull requests created by Copilot to verify emails would be sent appropriately

5. **Environment isolation** - Use the `copilot` environment to manage which repositories/workflows have access to your email sending capability

### Configuration Management

1. **Use `.env.local` for development**:
   ```bash
   # .env.local (not committed)
   RESEND_API_KEY=re_test_xxx
   SENDER_EMAIL_ADDRESS=dev@example.com
   ```

2. **Separate configs per environment**:
   - Development: Test API key, limited recipients
   - Production: Full API key, all recipients allowed

3. **Document required env vars** in `README.md`:
   ```markdown
   ## Environment Variables
   - RESEND_API_KEY: Resend API key (required)
   - SENDER_EMAIL_ADDRESS: Verified sender email (optional)
   - REPLY_TO_EMAIL_ADDRESS: Reply-to email (optional)
   ```

### Email Content

1. **Always include unsubscribe links** for marketing emails
2. **Test emails with multiple email clients** (Gmail, Outlook, Apple Mail)
3. **Keep templates responsive** for mobile devices
4. **Use clear subject lines** that describe the email purpose
5. **Include plain text alternative** to HTML for accessibility

### AI Agent Usage

1. **Provide context** about who should receive emails
2. **Specify sender information** in the initial setup
3. **Review email content** generated by AI before sending
4. **Use agent mode** for complex workflows requiring multiple steps
5. **Test with your own email first** before sending to others

## Troubleshooting

### Issue: "Node version too old" or "Node 20+ required"

**Solution**: Check and update Node.js version
```bash
node --version  # Should be v20.0.0 or higher
```
- Install Node.js 20+ from https://nodejs.org (LTS version recommended)
- macOS: `brew install node@20` (if using Homebrew)
- Windows: Download from https://nodejs.org or use `nvm-windows`
- Linux: `nvm install 20` or use package manager
- Verify: `node --version` should show `v20.x.x` or later
- Restart your terminal/IDE after installation

### Issue: "Command not found: node"

**Solution**: Node.js is not installed or not in PATH
- Install Node.js from https://nodejs.org (version 20+ required)
- Verify installation: `node --version`
- Restart your terminal/IDE after installation

### Issue: "RESEND_API_KEY is required"

**Solution**: API key not provided or invalid
- Generate new key at https://resend.com/api-keys
- Ensure key starts with `re_`
- Check MCP configuration for correct environment variable name
- Verify there are no extra spaces in the key

### Issue: "Email not delivered / 401 Unauthorized"

**Solution**: Authentication or domain verification issue
- Verify API key is correct and active
- Check domain is verified at https://resend.com/domains
- Ensure sender email matches verified domain
- Check Resend dashboard for rate limiting or delivery errors

### Issue: "Build command fails during npm run build"

**Solution**: Dependency or TypeScript compilation error
```bash
# Clear and reinstall dependencies
rm -rf node_modules package-lock.json
npm install
npm run build
```

Common build errors:
- **TypeScript compilation error**: Check that all dependencies are installed
- **Permission denied on Unix/macOS**: The build script includes `chmod +x` - try running from a different directory
- **Module not found**: Delete `node_modules` and reinstall fresh

### Issue: "MCP server not appearing in IDE tools list"

**Solution**: Configuration or server startup issue

**GitHub Copilot:**
1. Verify `.vscode/mcp.json` is in project root (not nested)
2. Check absolute path to `build/index.js` is correct
3. Reload VS Code window (Cmd+R on macOS, Ctrl+R on Windows)
4. Verify Agent mode is enabled (toggle in chat)

**Cursor:**
1. Open Cursor Settings (Cmd+Shift+P → "Cursor Settings")
2. Navigate to MCP tab
3. Verify configuration syntax is valid JSON
4. Check absolute path exists and is readable
5. Restart Cursor application

**Claude Desktop:**
1. Close Claude completely
2. Verify `claude_desktop_config.json` syntax
3. Check that `build/index.js` file exists
4. Reopen Claude Desktop
5. Check Developer tab for resend tool

### Issue: "Sending emails works but AI doesn't offer to use Resend MCP"

**Solution**: Agent model or mode issue
- Switch to Claude Sonnet 4 or GPT-4.1 (better tool understanding)
- Enable Agent mode explicitly
- Use explicit mention: "use the resend MCP tool to send..."
- Check MCP server is running (look for console output)

### Issue: "Getting 'invalid sender' error"

**Solution**: Sender email not verified
1. Go to https://resend.com/domains
2. Verify your custom domain if using one
3. Use default onboarding@resend.dev for testing
4. Update SENDER_EMAIL_ADDRESS in MCP config
5. Restart MCP server

## Advanced Configuration

### Custom MCP Server with HTTP Transport

For shared team environments or cloud-based setups:

```json
{
  "servers": {
    "resend": {
      "type": "http",
      "url": "https://your-mcp-server.example.com/mcp"
    }
  }
}
```

Your HTTP server should forward requests to Resend API.

### Environment-Specific Configurations

Use different `.mcp.json` files per environment:

```bash
# Development
cp .mcp.dev.json .vscode/mcp.json

# Production
cp .mcp.prod.json .vscode/mcp.json
```

### Integration with Claude Desktop + GitHub Copilot

You can configure both simultaneously:

**Claude Desktop config:**
```json
{
  "mcpServers": {
    "resend": {
      "command": "node",
      "args": ["/path/to/mcp-send-email/build/index.js"],
      "env": {
        "RESEND_API_KEY": "re_xxxxx"
      }
    }
  }
}
```

**VS Code `.vscode/mcp.json`:**
```json
{
  "servers": {
    "resend": {
      "type": "command",
      "command": "node /path/to/mcp-send-email/build/index.js",
      "env": {
        "RESEND_API_KEY": "re_xxxxx"
      }
    }
  }
}
```

Both will use the same local MCP server instance.

## Workflow Examples

### Transactional Email Workflow

1. **Setup Phase**: Deploy MCP server with production API key
2. **Automation Phase**: Configure in Claude Desktop or Copilot
3. **Integration Phase**: Use in application logic via AI agent
   ```
   When order is confirmed, send confirmation email with order details using Resend MCP
   ```
4. **Monitoring Phase**: Check Resend dashboard for delivery status

### Marketing Campaign Workflow

1. Prepare email template and recipient list
2. Use AI agent to generate personalized content
3. Review generated emails before sending
4. Send via Resend MCP in batches
5. Monitor open rates and engagement

### Notification Workflow

1. Configure Resend MCP for your notification service
2. Create email templates for different notification types
3. Use AI agent to format notifications as emails
4. Send via Resend MCP to subscribers
5. Track delivery and handle bounces

## Resources

- [Resend Documentation](https://resend.com/docs)
- [MCP Protocol Documentation](https://modelcontextprotocol.io/introduction)
- [GitHub MCP Registry](https://github.com/mcp)
- [VS Code Insider Developer Docs](https://code.visualstudio.com/blogs/2025/04/07/agentMode)
- [Cursor Documentation](https://docs.cursor.com)
- [Claude Desktop Configuration](https://support.anthropic.com/claude-desktop/)
