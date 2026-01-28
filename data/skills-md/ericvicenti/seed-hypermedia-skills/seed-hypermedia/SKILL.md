---
name: seed-hypermedia
description: Access content on the Hypermedia Network using Seed Hypermedia CLI.
  Read and interact with URLs that are prefixed with hm://
---

## Overview

The Seed CLI is a command-line interface for interacting with the Seed Hypermedia network. It allows you to fetch documents, search content, manage accounts, and perform various operations on the hypermedia network.

Seed servers are open source and self-hostable servers running on the peer-to-peer Hypermedia network. You can use the CLI to interact with any Seed server using its API.

Browse the open source Seed Hypermedia repository here: https://github.com/seed-hypermedia/seed

Learn more at https://seed.hyper.media

Download the Seed desktop app: https://download.seed.hyper.media

## Installation

You can run the Seed CLI directly using npx without installation:

```bash
npx -y @seed-hypermedia/cli
```

## URL Types

You should ALWAYS use this skill to open hm:// URLs. The CLI can be used once you have a URL with the prefix of hm://

Many https:// web sites are actually Hypermedia-enabled! If the user says that a URL is a Hypermedia URL or a Seed Site, then you should resolve the URL using this approach.

### HTTPS -> HM URL conversion

For an example HTTPS URL such as https://seed.hyper.media/community

Run this command to query for Hypermedia headers:

```sh
curl https://seed.hyper.media/community -X OPTIONS -I 2>&1 | grep -i x-hypermedia
```

Example headers might look like this:

```
x-hypermedia-authors: hm%3A%2F%2Fz6MkpHiG87oJnyMajxKyJcEwNRTbrHWjKSnmVxuuxq7bP3nb
x-hypermedia-id: hm%3A%2F%2Fz6MkpHiG87oJnyMajxKyJcEwNRTbrHWjKSnmVxuuxq7bP3nb
x-hypermedia-title: Lunaticoin
x-hypermedia-type: Document
x-hypermedia-version: bafy2bzacecf3jzmqao7zppmemna3ioz4p4nek37knlygr6n5rssdzhlikvkck
```

The headers are URL encoded but you can see the hm:// URL is available in `x-hypermedia-id:` . Now you can use that URL with the CLI.

## Global Options

- `-V, --version`: Output the version number
- `-s, --server <url>`: Server URL (default: "https://hyper.media")
- `--json`: JSON output (default)
- `--yaml`: YAML output
- `--pretty`: Pretty formatted output
- `-q, --quiet`: Minimal output
- `-h, --help`: Display help for command

## Commands

### Document Operations

#### `get <id>` - Fetch a document, comment, or entity

Fetch content by Hypermedia ID.

**Options:**

- `-m, --metadata`: Fetch metadata only
- `--md`: Output as markdown
- `--frontmatter`: Include YAML frontmatter (with --md)
- `-r, --resolve`: Resolve embeds, mentions, and queries (with --md)
- `-q, --quiet`: Output minimal info

**Example:**

```bash
npx -y @seed-hypermedia/cli get --md "hm://HYPERMEDIA_URL_HERE"
```

#### `cid <cid>` - Fetch raw IPFS block by CID

Retrieve raw IPFS content by Content Identifier.

#### `stats <id>` - Get interaction statistics for a document

Get metrics and statistics for a specific document.

### Search and Query

#### `search <query>` - Search for documents

Search across the hypermedia network.

**Options:**

- `-a, --account <uid>`: Limit search to specific account
- `-q, --quiet`: Output IDs and titles only

#### `query <space>` - List documents in a space

Query documents within a specific space.

**Options:**

- `-p, --path <path>`: Path prefix
- `-m, --mode <mode>`: Query mode: Children or AllDescendants (default: "Children")
- `-l, --limit <n>`: Limit results
- `--sort <term>`: Sort by: Path, Title, CreateTime, UpdateTime, DisplayTime
- `--reverse`: Reverse sort order
- `-q, --quiet`: Output IDs and names only

#### `children <space>` - List child documents

Shorthand for `query --mode Children`.

#### `citations <id>` - List documents citing this resource

Find documents that reference or cite a specific resource.

### Account Management

#### `account <uid>` - Get account information

Retrieve information about a specific account.

**Options:**

- `-q, --quiet`: Output ID only

#### `accounts` - List all known accounts

List all accounts known to the system.

**Options:**

- `-q, --quiet`: Minimal output

#### `contacts <uid>` - List contacts for an account

Get the contact list for a specific account.

**Options:**

- `-q, --quiet`: Minimal output

### Comments and Discussions

#### `comments <targetId>` - List comments on a document

Get all comments for a specific document.

**Options:**

- `-q, --quiet`: Output IDs and authors only

#### `discussions <targetId>` - List threaded discussions on a document

Get threaded discussion view for a document.

**Options:**

- `-q, --quiet`: Minimal output

#### `comment <id>` - Get a single comment by ID

Retrieve a specific comment.

### Access Control

#### `capabilities <id>` - List access control capabilities

View access control permissions for a resource.

### Activity and History

#### `activity` - List activity events

View recent activity across the network.

**Options:**

- `-l, --limit <n>`: Page size
- `-t, --token <token>`: Page token for pagination
- `--authors <uids>`: Filter by author UIDs (comma-separated)
- `--resource <id>`: Filter by resource
- `-q, --quiet`: Output summary only

#### `changes <targetId>` - List document change history

View the change history for a specific document.

**Options:**

- `-q, --quiet`: Output CIDs and authors only

### Key Management

#### `key` - Manage signing keys

Manage cryptographic keys for signing and authentication.

**Subcommands:**

- `generate [options]`: Generate a new signing key from mnemonic
- `import [options] <mnemonic>`: Import a key from existing mnemonic
- `list`: List stored signing keys
- `show [options] [nameOrId]`: Show key information
- `remove [options] <nameOrId>`: Remove a stored key
- `default [nameOrId]`: Set or show default signing key
- `derive [options] <mnemonic>`: Derive account ID from mnemonic (without storing)

### Configuration

#### `config` - Manage CLI configuration

Configure CLI settings.

**Options:**

- `--server <url>`: Set default server URL
- `--show`: Show current configuration

## Common Use Cases

### Reading a Document as Markdown

```bash
npx -y @seed-hypermedia/cli get --md "hm://document-id-here"
```

### Reading with Full Context Resolution

```bash
npx -y @seed-hypermedia/cli get --md --resolve --frontmatter "hm://document-id-here"
```

### Searching for Content

```bash
npx -y @seed-hypermedia/cli search "your search terms"
```

### Listing Documents in a Space

```bash
npx -y @seed-hypermedia/cli query "space-id" --sort UpdateTime --reverse
```

### Getting Account Information

```bash
npx -y @seed-hypermedia/cli account "account-uid"
```

### Viewing Comments

```bash
npx -y @seed-hypermedia/cli comments "document-id"
```

## Output Formats

The CLI supports multiple output formats:

- **JSON** (default): Machine-readable structured data
- **YAML**: Human-readable structured data (`--yaml`)
- **Pretty**: Formatted output (`--pretty`)
- **Markdown**: For documents (`--md` with get command)
- **Quiet**: Minimal output (`--quiet`)

## Server Configuration

By default, the CLI connects to `https://hyper.media`. You can:

- Use a different server for a single command: `-s, --server <url>`
- Set a default server: `npx -y @seed-hypermedia/cli config --server <url>`
- View current configuration: `npx -y @seed-hypermedia/cli config --show`
