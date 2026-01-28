---
name: python-telegram-bot
description: python-telegram-bot library for building Telegram bots. Use for handlers, callbacks, inline keyboards, conversations, and bot commands.
---

# Python-Telegram-Bot Skill

Comprehensive assistance with python-telegram-bot development, generated from official documentation.

## When to Use This Skill

This skill should be triggered when:
- Working with python-telegram-bot
- Asking about python-telegram-bot features or APIs
- Implementing python-telegram-bot solutions
- Debugging python-telegram-bot code
- Learning python-telegram-bot best practices

## Quick Reference

### Common Patterns

**Pattern 1:** base_url (str | Callable[[str], str], optional) – Telegram Bot API service URL. If the string contains {token}, it will be replaced with the bot’s token. If a callable is passed, it will be called with the bot’s token as the only argument and must return the base URL. Otherwise, the token will be appended to the string. Defaults to "https://api.telegram.org/bot". Tip Customizing the base URL can be used to run a bot against Local Bot API Server or using Telegrams test environment. Example:"https://api.telegram.org/bot{token}/test" Changed in version 21.11: Supports callable input and string formatting.

```
str
```

**Pattern 2:** Tip Customizing the base URL can be used to run a bot against Local Bot API Server or using Telegrams test environment. Example:"https://api.telegram.org/bot{token}/test"

```
"https://api.telegram.org/bot{token}/test"
```

**Pattern 3:** Tip Customizing the base URL can be used to run a bot against Local Bot API Server or using Telegrams test environment. Example:"https://api.telegram.org/file/bot{token}/test"

```
"https://api.telegram.org/file/bot{token}/test"
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **other.md** - Other documentation

Use `view` to read specific reference files when detailed information is needed.

## Working with This Skill

### For Beginners
Start with the getting_started or tutorials reference files for foundational concepts.

### For Specific Features
Use the appropriate category reference file (api, guides, etc.) for detailed information.

### For Code Examples
The quick reference section above contains common patterns extracted from the official docs.

## Resources

### references/
Organized documentation extracted from official sources. These files contain:
- Detailed explanations
- Code examples with language annotations
- Links to original documentation
- Table of contents for quick navigation

### scripts/
Add helper scripts here for common automation tasks.

### assets/
Add templates, boilerplate, or example projects here.

## Notes

- This skill was automatically generated from official documentation
- Reference files preserve the structure and examples from source docs
- Code examples include language detection for better syntax highlighting
- Quick reference patterns are extracted from common usage examples in the docs

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest information
