---
name: homebrew-cask-authoring
description: Create, update, validate, and submit Homebrew Casks. Use when the user mentions Homebrew cask/cask, Homebrew/homebrew-cask, adding a new cask, updating a cask, cask token naming, sha256, url verified:, livecheck, zap/uninstall, or when asked to run brew style/audit for a cask.
---

# Homebrew Cask Authoring

Author and maintain Homebrew Casks with correct token naming, stanzas, audit/style compliance, and local install testing.

## Operating rules

- Prefer the official Homebrew documentation (Cask Cookbook, Acceptable Casks) when uncertain.
- Keep casks minimal: only add stanzas that are required for correct install/uninstall/cleanup.
- Avoid destructive system changes unless explicitly requested; call out any `rm`/tap changes before suggesting them.
- When testing local casks, ensure Homebrew reads from the local file (not the API).

## Quick intake (ask these first)

Collect:
- App name (exact `.app` bundle name)
- Homepage (official)
- Download URL(s) (DMG/ZIP/PKG) and whether they differ by arch
- Version scheme (single version? per-arch?)
- Install artifact type (`app`, `pkg`, `suite`, etc.)
- Uninstall requirements (pkgutil ids, launch agents, kernel extensions)
- Desired cleanup (zap paths)

If any of these are unknown, propose a short plan to discover them.

## Workflow: create or update a cask

### 1) Choose the token

- Start from the `.app` bundle name.
- Remove `.app` and common suffixes: “App”, “Mac”, “Desktop”, “for macOS”, version numbers.
- Downcase; replace spaces/underscores with hyphens.
- Remove non-alphanumerics except hyphens.
- Use `@beta`, `@nightly`, or `@<major>` for variants.

Confirm the token before writing the file.

### 2) Draft a minimal cask

Use this canonical structure:

```ruby
cask "token" do
  version "1.2.3"
  sha256 "..."

  url "https://example.com/app-#{version}.dmg"
  name "Official App Name"
  desc "Short one-line description"
  homepage "https://example.com"

  app "AppName.app"
end
```

Rules of thumb:
- Prefer `https` URLs.
- Add `verified:` when download host domain differs from `homepage` domain.
- Keep `desc` factual and concise (no marketing).

### 3) Handle architecture (if needed)

If URLs and/or sha256 differ by CPU:
- Use `arch` + `sha256 arm: ..., intel: ...` when versions match.
- Use `on_arm` / `on_intel` blocks when versions differ.

### 4) Add required uninstall/zap

- Add `uninstall` for `pkg` installs (include `pkgutil:` identifiers).
- Add `zap` for user data cleanup (support directories, preferences, caches), but keep it accurate.

### 5) Validate and test locally

Run, in this order:

```bash
brew style --fix <token>
brew audit --cask --online <token>
```

For new casks also run:

```bash
brew audit --cask --new <token>
HOMEBREW_NO_INSTALL_FROM_API=1 brew install --cask <token>
brew uninstall --cask <token>
```

If install fails:
- Re-check URL reachability, `sha256`, and artifact name.
- Re-run with verbosity: `brew install --cask --verbose <token>`.

### 6) PR hygiene

Before suggesting submission:
- Ensure `brew style` and all relevant `brew audit` commands pass.
- For new casks, check the token has not been previously refused/unmerged.

## Local development patterns

If the user is editing `Homebrew/homebrew-cask` locally and wants Homebrew to execute their working copy, use a tap symlink workflow.

Read the full end-to-end checklist here:
- `references/homebrew-cask-contribution-workflow.md`
