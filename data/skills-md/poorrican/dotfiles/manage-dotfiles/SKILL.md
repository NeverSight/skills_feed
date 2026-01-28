---
name: manage-dotfiles
description: Manage dotfiles and keep synced with external directories. Use on Linux / macOS systemswhen thetre are external connfigs which are being imported into the dotfiles, or when stored dotfiles need to be brought outside to the XDG environment.
---

## Instructions

On Linux and macOS, dotfiles will be managed via GNU stow.

The stored dotfiles will use the XDG configuration for simplicity and organization.

The commands below assume that there is a specific config package which is being interacted with (eg: `nvim`)

## Syncing Dotfiles - Exporting Configurations

Sync a dotfiles package to its target location using GNU stow.

### Instructions

1. Validate the package exists at `~/dotfiles/{package}`:
   - If it doesn't exist, list available packages (top-level directories in ~/dotfiles that aren't hidden or special like `result`, `docs`, `░▒▓ OLD ▓▒░`)
   - Fail with a clear error message

2. Run stow to deploy the package:
   ```bash
   stow -v -d ~/dotfiles -t ~ {package}
   ```

3. Report what was linked. If stow reports conflicts, explain what's blocking and suggest using `stow -D` to unstow first, or `stow -R` to restow.

## Importing Configurations

Import an external config into the dotfiles repository and stow it.

### Instructions

1. **Resolve the path**: Expand `~` and resolve to an absolute path. Verify the file/directory exists.

2. **Compute the home-relative path**: The path must be under `$HOME`. Strip the `$HOME` prefix to get the relative path.
   - Example: `~/.config/foo/bar.conf` → `.config/foo/bar.conf`
   - Example: `~/.zshrc` → `.zshrc`

3. **Derive the package name**:
   - For `.config/<app>/...` paths → package name is `<app>`
   - For `.<dotfile>` (hidden file in home root) → package name is `<dotfile>` without the leading dot
   - For `.local/share/<app>/...` → package name is `<app>`
   - For other structures → use the first directory component, or ask the user

4. **Create the package structure** in `~/dotfiles`:
   ```bash
   mkdir -p ~/dotfiles/<package>/<parent-dirs>
   ```
   Where `<parent-dirs>` mirrors the home-relative path's directory structure.

5. **Move the config** into the package:
   ```bash
   mv <original-path> ~/dotfiles/<package>/<home-relative-path>
   ```

6. **Stow the package** to create symlinks:
   ```bash
   stow -v -d ~/dotfiles -t ~ <package>
   ```

7. **Verify**: Confirm the original path is now a symlink pointing into dotfiles.

## Example

Importing `~/.config/wezterm/wezterm.lua`:
- Package name: `wezterm`
- Creates: `~/dotfiles/wezterm/.config/wezterm/wezterm.lua`
- Symlinks: `~/.config/wezterm/` → `~/dotfiles/wezterm/.config/wezterm/`

## Notes

- If the package already exists, merge the new config into it
- Do NOT use `ln` - only use `stow` for symlinking
- If importing a single file from a directory that has other files, ask if the user wants to import the entire directory or just the file
