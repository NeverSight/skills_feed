---
name: obsidian-nvim
description: Guide for implementing obsidian.nvim - a Neovim plugin for Obsidian vault management. Use when configuring, troubleshooting, or extending obsidian.nvim features including workspace setup, daily notes, templates, completion, pickers, and UI customization.
---

# obsidian.nvim Skill

A comprehensive guide for implementing and configuring obsidian.nvim - the Neovim plugin for managing Obsidian vaults.

## Quick Start

### Minimal Installation (lazy.nvim)

```lua
return {
  "obsidian-nvim/obsidian.nvim",
  version = "*",
  ft = "markdown",
  opts = {
    workspaces = {
      { name = "personal", path = "~/vaults/personal" },
    },
  },
}
```

### System Requirements

- **Neovim**: >= 0.10.0
- **ripgrep**: Required for completion and search (`brew install ripgrep`)
- **pngpaste** (macOS): For image pasting (`brew install pngpaste`)
- **xclip/wl-clipboard** (Linux): For image pasting

## Configuration

See [references/configuration.md](references/configuration.md) for complete configuration options.

### Essential Configuration Options

```lua
require("obsidian").setup({
  -- Workspace configuration (required)
  workspaces = {
    { name = "personal", path = "~/vaults/personal" },
    { name = "work", path = "~/vaults/work" },
  },

  -- Daily notes
  daily_notes = {
    folder = "daily",
    date_format = "%Y-%m-%d",
    alias_format = "%B %-d, %Y",
    default_tags = { "daily-notes" },
  },

  -- Templates
  templates = {
    folder = "templates",
    date_format = "%Y-%m-%d",
    time_format = "%H:%M",
  },

  -- Note ID generation (Zettelkasten-style by default)
  note_id_func = function(title)
    local suffix = ""
    if title ~= nil then
      suffix = title:gsub(" ", "-"):gsub("[^A-Za-z0-9-]", ""):lower()
    else
      for _ = 1, 4 do
        suffix = suffix .. string.char(math.random(65, 90))
      end
    end
    return tostring(os.time()) .. "-" .. suffix
  end,

  -- Completion settings
  completion = {
    nvim_cmp = true,  -- or blink = true for blink.cmp
    min_chars = 2,
  },

  -- UI customization
  ui = {
    enable = true,
    checkboxes = {
      [" "] = { char = "󰄱", hl_group = "ObsidianTodo" },
      ["x"] = { char = "", hl_group = "ObsidianDone" },
    },
  },
})
```

## Commands

See [references/commands.md](references/commands.md) for complete command reference.

### Primary Commands

| Command | Description |
|---------|-------------|
| `:Obsidian` | Open command picker |
| `:Obsidian today [OFFSET]` | Open/create daily note |
| `:Obsidian new [TITLE]` | Create new note |
| `:Obsidian search [QUERY]` | Search vault with ripgrep |
| `:Obsidian quick_switch` | Fuzzy find notes |
| `:Obsidian backlinks` | Show references to current note |
| `:Obsidian template [NAME]` | Insert template |
| `:Obsidian workspace [NAME]` | Switch workspace |

### Visual Mode Commands

| Command | Description |
|---------|-------------|
| `:Obsidian link [QUERY]` | Link selection to existing note |
| `:Obsidian link_new [TITLE]` | Create note and link selection |
| `:Obsidian extract_note [TITLE]` | Extract selection to new note |

## Keymaps

### Smart Action (Recommended: `<CR>`)

```lua
vim.keymap.set("n", "<CR>", function()
  if require("obsidian").util.cursor_on_markdown_link() then
    return "<cmd>Obsidian follow_link<CR>"
  else
    return "<CR>"
  end
end, { expr = true })
```

### Navigation Links

```lua
vim.keymap.set("n", "[o", function()
  require("obsidian").util.nav_link("prev")
end, { buffer = true, desc = "Previous link" })

vim.keymap.set("n", "]o", function()
  require("obsidian").util.nav_link("next")
end, { buffer = true, desc = "Next link" })
```

## Picker Integration

Configure your preferred picker:

```lua
picker = {
  name = "telescope",  -- or "fzf-lua", "mini.pick", "snacks.picker"
  note_mappings = {
    new = "<C-x>",
    insert_link = "<C-l>",
  },
  tag_mappings = {
    tag_note = "<C-x>",
    insert_tag = "<C-l>",
  },
},
```

## Completion Integration

### With blink.cmp

```lua
completion = {
  blink = true,
  nvim_cmp = false,
  min_chars = 2,
},
```

### With nvim-cmp

```lua
completion = {
  nvim_cmp = true,
  blink = false,
  min_chars = 2,
},
```

**Triggers:**
- `[[` - Wiki link completion
- `[` - Markdown link completion
- `#` - Tag completion

## Templates

### Template Variables

| Variable | Description |
|----------|-------------|
| `{{title}}` | Note title |
| `{{date}}` | Current date |
| `{{time}}` | Current time |
| `{{id}}` | Note ID |

### Custom Substitutions

```lua
templates = {
  folder = "templates",
  substitutions = {
    yesterday = function()
      return os.date("%Y-%m-%d", os.time() - 86400)
    end,
    tomorrow = function()
      return os.date("%Y-%m-%d", os.time() + 86400)
    end,
  },
},
```

## Frontmatter Management

```lua
frontmatter = {
  enabled = true,
  func = function(note)
    local out = { id = note.id, aliases = note.aliases, tags = note.tags }
    if note.metadata ~= nil and not vim.tbl_isempty(note.metadata) then
      for k, v in pairs(note.metadata) do
        out[k] = v
      end
    end
    return out
  end,
  sort = { "id", "aliases", "tags" },
},
```

## Troubleshooting

See [references/troubleshooting.md](references/troubleshooting.md) for comprehensive troubleshooting.

### Health Check

```vim
:checkhealth obsidian
```

### Quick Fixes

| Issue | Solution |
|-------|----------|
| Completion not working | Install ripgrep: `brew install ripgrep` |
| Picker not opening | Verify picker name matches installed plugin |
| Images not pasting | macOS: `brew install pngpaste` |
| Links not following | Ensure cursor is on `[[link]]` or `[text](link)` |
| Checkboxes not rendering | Set `:set conceallevel=2` |
| Workspace not found | Verify path exists and file is inside vault |

### Debug Mode

```lua
log_level = vim.log.levels.DEBUG,
```

## Examples

See [references/examples.md](references/examples.md) for practical configuration examples.

## Resources

- [GitHub Repository](https://github.com/obsidian-nvim/obsidian.nvim)
- [Wiki Documentation](https://github.com/obsidian-nvim/obsidian.nvim/wiki)
- [Breaking Changes](https://github.com/obsidian-nvim/obsidian.nvim/wiki/Breaking-Changes)
