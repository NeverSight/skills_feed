---
name: github-authenticator
description: Verify and troubleshoot GitHub CLI authentication. Use when gh commands fail with auth errors or when setting up GitHub integration for the first time.
---

# GitHub Authenticator

## Instructions

### When to Invoke This Skill
- `gh` commands fail with authentication errors
- User is setting up GitHub CLI for the first time
- Need to verify current authentication status
- Switching between GitHub accounts
- Troubleshooting permission issues

### Standard Workflow

1. **Check Current Authentication Status**
   ```bash
   gh auth status
   ```

2. **Interpret Output**
   - **Logged in**: Shows username, scopes, and token status
   - **Not logged in**: Shows "You are not logged in to any GitHub hosts"
   - **Token expired**: Shows authentication but with errors

3. **Handle Authentication Issues**

   **If not authenticated:**
   ```bash
   gh auth login
   ```
   - Choose: GitHub.com or GitHub Enterprise
   - Choose: HTTPS (recommended) or SSH
   - Authenticate via: Browser (recommended) or Token
   - Complete authentication flow

   **If token expired:**
   ```bash
   gh auth refresh
   ```

   **If wrong account:**
   ```bash
   gh auth logout
   gh auth login
   ```

### Required Scopes

Verify the token has necessary scopes:
- `repo` - Full control of private repositories
- `workflow` - Update GitHub Action workflows
- `admin:org` - Read organization data (if working with org repos)

### Error Scenarios

**"HTTP 401: Bad credentials"**
- Token is invalid or expired
- Run: `gh auth refresh` or re-authenticate

**"HTTP 403: Resource not accessible"**
- Insufficient permissions
- Check repository access
- Verify organization membership

**"HTTP 404: Not Found"**
- Repository doesn't exist
- User doesn't have access
- Check repository name and permissions

### Configuration Check

**View current configuration:**
```bash
gh auth status --show-token
```
(Be careful - this displays the token)

**Check which host is configured:**
```bash
gh config get git_protocol
```

**Set preferences:**
```bash
gh config set git_protocol https
gh config set editor vim
```

## Examples

### Example 1: Authentication check before operations
```
Action: About to create PR
Step 1: Run gh auth status
Step 2: If authenticated, proceed with PR creation
Step 3: If not, guide user through gh auth login
```

### Example 2: Authentication failure during operation
```
Error: "gh: HTTP 401: Bad credentials"
Action:
1. Inform user of authentication issue
2. Run gh auth status to diagnose
3. Guide through gh auth refresh or gh auth login
4. Retry original operation
```

### Example 3: First-time setup
```
User: "Setup GitHub CLI"
Action:
1. Check if gh is installed: gh --version
2. Run gh auth login
3. Guide through authentication flow
4. Verify with gh auth status
5. Test with simple command: gh repo view
```

### Example 4: Switching accounts
```
User: "I need to use my work GitHub account"
Action:
1. Show current account: gh auth status
2. Logout: gh auth logout
3. Login with work account: gh auth login
4. Verify: gh auth status
```
