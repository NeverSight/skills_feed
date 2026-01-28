---
name: customer-support
description: Handle customer support tickets for themes and plugins with empathy, clarity, and efficiency. Use when responding to support tickets, troubleshooting issues, writing help responses, or managing Zoho Desk/support queues.
---

# Customer Support Skill for Theme & Plugin Agency

## Instructions

When handling support tickets:

### 1. Response Structure

```
Hi [Name],

[Acknowledge their issue with empathy]

[Solution or next steps]

[Additional helpful info if relevant]

[Closing + offer further help]

Best regards,
[Your name]
```

### 2. Common Issue Templates

**Installation Issues:**
```
Hi [Name],

I understand you're having trouble installing [product]. Let me help!

Please try these steps:
1. Ensure WordPress is version 6.0 or higher
2. Check PHP version is 8.0+ (Hosting → PHP Settings)
3. Increase memory limit to 256MB
4. Try uploading via FTP if dashboard fails

If the issue persists, please share:
- WordPress version
- PHP version
- Any error messages you see

I'm here to help!
```

**Feature Request:**
```
Hi [Name],

Thank you for suggesting [feature]! I've added this to our feature request list.

While I can't promise a timeline, your feedback helps us prioritize future updates. Many of our best features came from user suggestions like yours.

In the meantime, here's a workaround that might help: [workaround if available]

Thanks for being a valued customer!
```

**Refund Request:**
```
Hi [Name],

I'm sorry [product] didn't meet your expectations.

I've processed your refund — you should see it within 5-7 business days.

If you don't mind sharing, I'd love to know what we could improve. Your feedback helps us get better.

Wishing you all the best!
```

**Bug Report:**
```
Hi [Name],

Thank you for reporting this issue. I've confirmed the bug and our team is working on a fix.

**Workaround for now:**
[Temporary solution if available]

**Expected fix:**
This will be resolved in our next update (typically within [timeframe]).

I'll follow up once the fix is live. Thanks for your patience!
```

### 3. Troubleshooting Flow

1. **Gather info:**
   - WordPress version
   - Theme/plugin version
   - PHP version
   - Browser (if frontend issue)
   - Error messages/screenshots

2. **Check common causes:**
   - Plugin conflicts (disable other plugins)
   - Theme conflicts (switch to default theme)
   - Caching (clear all caches)
   - Outdated version (update everything)

3. **Replicate the issue:**
   - Try on staging/test site
   - Document steps to reproduce

4. **Provide solution:**
   - Step-by-step fix
   - Screenshots if helpful
   - Explain the cause briefly

### 4. Tone Guidelines

**Do:**
- Use customer's name
- Acknowledge their frustration
- Be specific and actionable
- Offer alternatives
- Thank them for patience

**Don't:**
- Blame the customer
- Use technical jargon
- Make promises you can't keep
- Copy/paste without personalizing
- Rush the response

### 5. Priority Handling

| Priority | Response Time | Examples |
|----------|--------------|----------|
| **Critical** | < 2 hours | Site down, security issue, payment broken |
| **High** | < 8 hours | Major feature broken, upgrade issues |
| **Medium** | < 24 hours | Minor bugs, how-to questions |
| **Low** | < 48 hours | Feature requests, general questions |

### 6. Escalation Criteria

Escalate to development when:
- Bug confirmed and reproducible
- Security vulnerability reported
- Multiple users reporting same issue
- Issue requires code changes

### 7. Closing Tickets

Before closing:
- [ ] Issue confirmed resolved
- [ ] Customer confirmed satisfaction
- [ ] Added internal notes for future reference
- [ ] Tagged appropriately for reporting
- [ ] Updated knowledge base if new solution found

### Integration with Zoho Desk

- Use tags: `bug`, `feature-request`, `billing`, `installation`, `customization`
- Add private notes for internal context
- Link related tickets
- Update ticket priority as needed
