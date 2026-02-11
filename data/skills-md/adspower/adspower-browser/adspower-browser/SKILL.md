---
name: adspower-browser
description: Runs AdsPower Local API operations via the adspower-browser CLI (no MCP required). Use when the user asks to create or manage AdsPower browsers, groups, proxies, or check status; run Node CLI commands that call the same handlers as the MCP server.
---

# AdsPower Local API with adspower-browser

The Skills CLI (npx adspower-browser) is the package manager for operate AdsPower browser profiles, groups, proxies, and application/category lists via the **adspower-browser** CLI. 

## When to Use This Skill

Apply when the user:

- Asks to create, update, delete, or list AdsPower browser profiles
- Mentions opening or closing browsers/profiles, fingerprint, UA, or proxy
- Wants to manage groups, proxies, or check API status
- Refers to AdsPower or adspower-browser (and MCP is not running or not desired)

Ensure AdsPower is running (default port 50325). Set `PORT` and `API_KEY` via environment or `--port` / `--api-key` if needed.

## How to Run

```bash
adspower-browser [--port PORT] [--api-key KEY] <command> [<arg>]
```

**Two forms for `<arg>`:**

1. **Single value (shorthand)** — for profile-related commands, pass one profile ID or number:
   - `adspower-browser open-browser <ProfileId>`
   - `adspower-browser close-browser <ProfileId>`
   - `adspower-browser get-profile-cookies <ProfileId>`
   - `adspower-browser get-browser-active <ProfileId>`
   - `adspower-browser get-profile-ua <ProfileId>` (single ID)
   - `adspower-browser new-fingerprint <ProfileId>` (single ID)

2. **JSON string** — full parameters for any command (see Command Reference below):
   - `adspower-browser open-browser '{"profileId":"abc123","launchArgs":"..."}'`
   - Commands with no params: omit `<arg>` or use `'{}'`.

## Essential Commands

### Browser profile – open/close

```bash
adspower-browser open-browser <profileId>                    # Or JSON: profileId, profileNo?, ipTab?, launchArgs?, clearCacheAfterClosing?, cdpMask?
adspower-browser close-browser <profileId>                   # Or JSON: profileId? | profileNo? (one required)
```

### Browser profile – create/update/delete/list

```bash
adspower-browser create-browser '{"groupId":"0","proxyid":"random",...}'  # groupId + account field + proxy required
adspower-browser update-browser '{"profileId":"...",...}'    # profileId required
adspower-browser delete-browser '{"profileIds":["..."]}'     # profileIds required
adspower-browser get-browser-list '{}'                       # Or groupId?, limit?, page?, profileId?, profileNo?, sortType?, sortOrder?
adspower-browser get-opened-browser                          # No params
```

### Browser profile – move/cookies/UA/fingerprint/cache/share/active

```bash
adspower-browser move-browser '{"groupId":"1","userIds":["..."]}'   # groupId + userIds required
adspower-browser get-profile-cookies <profileId>             # Or JSON: profileId? | profileNo?
adspower-browser get-profile-ua <profileId>                  # Or JSON: profileId[]? | profileNo[]? (up to 10)
adspower-browser close-all-profiles                          # No params
adspower-browser new-fingerprint <profileId>                 # Or JSON: profileId[]? | profileNo[]? (up to 10)
adspower-browser delete-cache-v2 '{"profileIds":["..."],"type":["cookie","history"]}'  # type: local_storage|indexeddb|extension_cache|cookie|history|image_file
adspower-browser share-profile '{"profileIds":["..."],"receiver":"email@example.com"}' # receiver required; shareType?, content?
adspower-browser get-browser-active <profileId>              # Or JSON: profileId? | profileNo?
adspower-browser get-cloud-active '{"userIds":"id1,id2"}'    # userIds comma-separated, max 100
```

### Group

```bash
adspower-browser create-group '{"groupName":"My Group","remark":"..."}'   # groupName required
adspower-browser update-group '{"groupId":"1","groupName":"New Name"}'    # groupId + groupName required; remark? (null to clear)
adspower-browser get-group-list '{}'                         # groupName?, size?, page?
```

### Application (categories)

```bash
adspower-browser check-status                                # No params – API availability
adspower-browser get-application-list '{}'                   # category_id?, page?, limit?
```

### Proxy

```bash
adspower-browser create-proxy '{"proxies":[{"type":"http","host":"127.0.0.1","port":"8080"}]}'  # type, host, port required per item
adspower-browser update-proxy '{"proxyId":"...","host":"..."}'   # proxyId required
adspower-browser get-proxy-list '{}'                         # limit?, page?, proxyId?
adspower-browser delete-proxy '{"proxyIds":["..."]}'        # proxyIds required, max 100
```

## Command Reference (full interface and parameters)

All parameter names are camelCase in JSON.

### Browser Profile Management

See [references/browser-profile-management.md](references/browser-profile-management.md) for open-browser, close-browser, create-browser, update-browser, delete-browser, get-browser-list, get-opened-browser, move-browser, get-profile-cookies, get-profile-ua, close-all-profiles, new-fingerprint, delete-cache-v2, share-profile, get-browser-active, get-cloud-active and their parameters.

### Group Management

See [references/group-management.md](references/group-management.md) for create-group, update-group, and get-group-list parameters.

### Application Management

See [references/application-management.md](references/application-management.md) for check-status and get-application-list parameters.

### Proxy Management

See [references/proxy-management.md](references/proxy-management.md) for create-proxy, update-proxy, get-proxy-list, and delete-proxy parameters.

### UserProxyConfig (inline proxy config for create-browser / update-browser)

See [references/user-proxy-config.md](references/user-proxy-config.md) for all fields (proxy_soft, proxy_type, proxy_host, proxy_port, etc.) and example.

### FingerprintConfig (fingerprint config for create-browser / update-browser)

See [references/fingerprint-config.md](references/fingerprint-config.md) for all fields (timezone, language, WebRTC, browser_kernel_config, random_ua, TLS, etc.) and example.

## Automation (Not Supported by This CLI)

Commands such as `navigate`, `click-element`, `fill-input`, `screenshot` depend on a persistent browser connection and are **not** exposed by this CLI. Use the **local-api-mcp** MCP server for automation.

## Deep-Dive Documentation

Reference docs with full enum values and field lists:

| Reference | Description | When to use |
|-----------|-------------|-------------|
| [references/browser-profile-management.md](references/browser-profile-management.md) | **open-browser**, **close-browser**, **create-browser**, **update-browser**, **delete-browser**, **get-browser-list**, **get-opened-browser**, **move-browser**, **get-profile-cookies**, **get-profile-ua**, **close-all-profiles**, **new-fingerprint**, **delete-cache-v2**, **share-profile**, **get-browser-active**, **get-cloud-active** parameters. | Any browser profile operation (open, create, update, delete, list, move, cookies, UA, cache, share, status). |
| [references/group-management.md](references/group-management.md) | **create-group**, **update-group**, **get-group-list** parameters. | Creating, updating, or listing browser groups. |
| [references/application-management.md](references/application-management.md) | **check-status**, **get-application-list** parameters. | Checking API availability or listing applications (categories). |
| [references/proxy-management.md](references/proxy-management.md) | **create-proxy**, **update-proxy**, **get-proxy-list**, **delete-proxy** parameters and enums. | Creating, updating, listing, or deleting proxies. |
| [references/user-proxy-config.md](references/user-proxy-config.md) | Full **userProxyConfig** field list (proxy_soft, proxy_type, proxy_host, proxy_port, etc.) and example. | Building inline proxy config for create-browser / update-browser when not using **proxyid**. |
| [references/fingerprint-config.md](references/fingerprint-config.md) | Full **fingerprintConfig** field list (timezone, language, WebRTC, browser_kernel_config, random_ua, TLS, etc.) and example. | Building or editing fingerprint config for create-browser / update-browser. |
| [references/browser-kernel-config.md](references/browser-kernel-config.md) | **type** and **version** for `fingerprintConfig.browser_kernel_config`. Version must match type (Chrome vs Firefox). | Pinning or choosing a specific browser kernel (Chrome/Firefox and version) when creating or updating a browser. |
| [references/ua-system-version.md](references/ua-system-version.md) | **ua_system_version** enum for `fingerprintConfig.random_ua`: specific OS versions, generic “any version” per system, and omit behavior. | Constraining or randomizing UA by OS (e.g. Android only, or “any macOS version”) when creating or updating a browser. |

Use these when you need the exact allowed values or semantics; the main skill text above only summarizes.
