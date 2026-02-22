---
name: nix-platform-specific-options
description: Write Nix modules with platform-specific options (NixOS vs Darwin) without infinite recursion. Use when mkIf causes evaluation errors or options don't exist across platforms.
---

# Nix Module Platform-Specific Options

## Overview

When writing Nix modules that need to hide platform-specific options (NixOS vs Darwin), using `mkIf` alone causes infinite recursion. This skill documents the correct pattern.

## The Problem

`mkIf` is evaluated lazily but the option **path** is still visible during module evaluation. This causes errors like:

```
error: The option `users.defaultUserShell' does not exist.
```

Or infinite recursion when `config` is referenced in option defaults or `optionalAttrs` conditions.

## The Pattern

**Use `optionalAttrs` for platform checks, `mkIf` for config-dependent checks.**

| Check Type                                 | Tool            | Evaluated  |
| ------------------------------------------ | --------------- | ---------- |
| Platform (`isDarwin`, `!isDarwin`)         | `optionalAttrs` | Parse time |
| Config values (`cfg.enable`, `cfg.flavor`) | `mkIf`          | Lazy       |

## Examples

### ❌ Wrong: mkIf for platform check

```nix
config = mkIf (!isDarwin) {
  users.defaultUserShell = pkgs.zsh;  # Darwin sees this path!
};
```

### ✅ Correct: optionalAttrs for platform check

```nix
config = optionalAttrs (!isDarwin) {
  users.defaultUserShell = pkgs.zsh;  # Hidden from Darwin
};
```

### ❌ Wrong: Config value in optionalAttrs condition

```nix
# cfg.flavor evaluated at parse time → infinite recursion
(optionalAttrs (isDarwin && cfg.flavor == "personal") {
  services.onepassword-secrets.enable = true;
})
```

### ✅ Correct: Nest mkIf inside optionalAttrs

```nix
# Platform check at parse time, config check lazy
(optionalAttrs isDarwin (mkIf (cfg.flavor == "personal") {
  services.onepassword-secrets.enable = true;
}))
```

### ❌ Wrong: config reference in option default

```nix
options.modules.foo = {
  user = mkOpt types.str config.user.name;  # Infinite recursion!
};
```

### ✅ Correct: Static default, use config in config section

```nix
options.modules.foo = {
  user = mkOpt types.str null;
};

config = mkIf cfg.enable (let
  user = if cfg.user != null then cfg.user else config.user.name;
in {
  # Use 'user' variable here
});
```

## Combined Pattern

For modules with both platform-specific options AND config-dependent behavior:

```nix
config = mkIf cfg.enable (mkMerge [
  # Common config (all platforms)
  { /* ... */ }

  # Darwin-only options
  (optionalAttrs isDarwin {
    programs.zsh.interactiveShellInit = "...";
  })

  # NixOS-only options
  (optionalAttrs (!isDarwin) {
    users.defaultUserShell = pkgs.zsh;
  })

  # Darwin + config-dependent (nested)
  (optionalAttrs isDarwin (mkIf (cfg.flavor == "personal") {
    services.onepassword-secrets.enable = true;
  }))
]);
```

## Quick Reference

| Scenario                   | Pattern                                                    |
| -------------------------- | ---------------------------------------------------------- |
| NixOS-only option          | `optionalAttrs (!isDarwin) { ... }`                        |
| Darwin-only option         | `optionalAttrs isDarwin { ... }`                           |
| Platform + enable check    | `optionalAttrs isDarwin (mkIf cfg.enable { ... })`         |
| Platform + config value    | `optionalAttrs isDarwin (mkIf (cfg.foo == "bar") { ... })` |
| Option default from config | Use `null` default, resolve in `config` section            |

## Debugging

When you see infinite recursion errors mentioning `_module.freeformType` or `anon-43`:

1. Search for `config.` references in option defaults
2. Search for `cfg.` references in `optionalAttrs` conditions
3. Search for `mkIf (!isDarwin)` or `mkIf isDarwin` guarding platform-specific options

```bash
# Find problematic patterns
grep -rn "mkOpt.*config\." modules/
grep -rn "optionalAttrs.*cfg\." modules/
grep -rn "mkIf.*isDarwin" modules/
```
