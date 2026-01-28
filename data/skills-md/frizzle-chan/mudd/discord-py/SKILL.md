---
name: discord-py
description: Build Discord bots using discord.py. Use when the user asks about Discord bot development, discord.py library, bot commands, slash commands, Discord intents, or Discord API integration. Covers Client, Bot, events, commands extension, app_commands, views, buttons, modals, and cogs.
---

# discord.py Quick Reference

This skill provides guidance for building Discord bots with the discord.py library.

## Quick Start: Minimal Bot

```python
import discord

intents = discord.Intents.default()
intents.message_content = True  # Required for reading message content

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Ignore self
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run('YOUR_BOT_TOKEN')
```

**Important**: Never name your file `discord.py` - it conflicts with the library.

## Critical: Intents Setup

Intents are **required** in discord.py 2.0+. They control which events your bot receives.

### Basic Setup

```python
intents = discord.Intents.default()  # Common intents, excludes privileged
```

### Enabling Specific Intents

```python
intents = discord.Intents.default()
intents.message_content = True  # Read message text (privileged)
intents.members = True          # Member join/leave events (privileged)
intents.presences = True        # Status updates (privileged)
```

### Privileged Intents Require Portal Setup

These three intents must ALSO be enabled in the Discord Developer Portal:
1. **Message Content Intent** - Required for reading message text
2. **Server Members Intent** - Required for member events and accurate member lists
3. **Presence Intent** - Required for tracking user status/activity

Go to: Discord Developer Portal > Your App > Bot > Privileged Gateway Intents

## Client vs Bot

| Use Case | Class | Import |
|----------|-------|--------|
| Basic events, no commands | `Client` | `discord.Client` |
| Prefix commands (!help) | `Bot` | `commands.Bot` |
| Slash commands | Either + `CommandTree` | `app_commands` |

### When to Use Bot (commands extension)

```python
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

bot.run('TOKEN')
```

## Event Handling

Common events (decorate with `@client.event` or `@bot.event`):

| Event | When it fires |
|-------|---------------|
| `on_ready()` | Bot connected and cache ready |
| `on_message(message)` | Message received |
| `on_member_join(member)` | User joined guild (needs members intent) |
| `on_member_remove(member)` | User left guild |
| `on_reaction_add(reaction, user)` | Reaction added |
| `on_guild_join(guild)` | Bot joined a server |
| `on_error(event, *args)` | Uncaught exception in event |

## Commands Extension Basics

```python
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def greet(ctx, name: str):
    """Greet someone by name."""
    await ctx.send(f'Hello, {name}!')

@bot.command(name='add')
async def add_numbers(ctx, a: int, b: int):
    """Add two numbers."""
    await ctx.send(f'{a} + {b} = {a + b}')
```

### Command Groups

```python
@bot.group()
async def settings(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Use !settings <subcommand>')

@settings.command()
async def show(ctx):
    await ctx.send('Current settings: ...')
```

## Slash Commands Basics

```python
import discord
from discord import app_commands

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name='ping', description='Check bot latency')
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f'Pong! {round(client.latency * 1000)}ms')

@client.event
async def on_ready():
    await tree.sync()  # Sync commands with Discord
    print(f'Synced commands for {client.user}')

client.run('TOKEN')
```

### Slash Command with Parameters

```python
@tree.command(name='greet', description='Greet a user')
@app_commands.describe(user='The user to greet')
async def greet(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.send_message(f'Hello, {user.mention}!')
```

## Sending Messages

```python
# In event handler
await message.channel.send('Hello!')
await message.channel.send('With embed', embed=embed)
await message.channel.send('With file', file=discord.File('image.png'))

# Reply to message
await message.reply('Replying to you!')

# In slash command
await interaction.response.send_message('Response')
await interaction.response.send_message('Only you see this', ephemeral=True)

# Edit/followup for slash commands
await interaction.response.defer()
await interaction.followup.send('Delayed response')
```

## Common Patterns

### Check if Message Author is Bot Owner

```python
@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send('Shutting down...')
    await bot.close()
```

### Permission Checks

```python
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
```

### Error Handling

```python
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You lack permissions for this command.')
    elif isinstance(error, commands.CommandNotFound):
        pass  # Ignore unknown commands
    else:
        raise error
```

## Fetching Latest Documentation

When you need up-to-date API details or are unsure about a feature, fetch the official documentation:

```
# Core API reference
WebFetch: https://discordpy.readthedocs.io/en/latest/api.html

# Commands extension
WebFetch: https://discordpy.readthedocs.io/en/latest/ext/commands/api.html

# Slash commands (app_commands)
WebFetch: https://discordpy.readthedocs.io/en/latest/interactions/api.html

# Intents guide
WebFetch: https://discordpy.readthedocs.io/en/latest/intents.html

# Quickstart guide
WebFetch: https://discordpy.readthedocs.io/en/latest/quickstart.html

# Frequently asked questions
WebFetch: https://discordpy.readthedocs.io/en/latest/faq.html
```

Always fetch documentation when:
- The user asks about a feature not covered in this skill
- You need to verify exact method signatures or parameters
- Working with less common features (webhooks, voice, threads)
- The user reports behavior different from what you expect

**Note**: Forum channels are documented in [reference.md](reference.md#forum-channels) with examples in [examples.md](examples.md#forum-channel-operations).

## Additional Resources

- For detailed API reference, see [reference.md](reference.md)
- For complete code examples, see [examples.md](examples.md)
- Official docs: https://discordpy.readthedocs.io/en/latest/
