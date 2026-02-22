---
name: running-webdriverio-tests
description: Run WebdriverIO test files from the command line. Use when debugging tests, gathering context about test behavior, or verifying changes resolved an issue.
---

# Running WebdriverIO Tests

## Main Command

```bash
npx wdio
```

Config is in `wdio.conf.js` by default.

## Project Context Files

Before selecting run commands, read project cache files when available:

- `.webdriverio-skills/project-context.md`
- `.webdriverio-skills/project-context.json`
- `.webdriverio-skills/custom-rules.md`
- `references/website-analysis/<target>/website-analysis.md`

Use these files to prefer project-approved scripts, configs, environment flags, and server targets.

Use website analysis references to prioritize high-impact route/component test runs first.

Resolve `<target>` as lowercase site host (prefer explicit URL or project `baseUrl` host), fallback `unknown-target`.

If files are missing or stale, run `managing-project-customizations` first.

## Duration

Tests take 20 seconds to 5 minutes. Do not treat a slow test as a failure.

## Selecting Tests to Run

Prefer `package.json` scripts discovered in project context when they exist (e.g. `npm run test:e2e`, `npm run test:wdio:debug`) before using raw `npx wdio`.

### By spec file

```bash
# Single file
npx wdio --spec=test/specs/home.js

# Multiple files
npx wdio --spec=test/specs/home.js --spec=test/specs/register.js
```

### By suite

Suite names are defined in the WebdriverIO config file under the `suites` property.

```bash
npx wdio --suite=auth
```

### Excluding files

```bash
npx wdio --exclude=test/specs/home.js
```

Can be mixed with `--spec` or `--suite`.

## Key CLI Options

| Option | Description |
|---|---|
| `--spec` | Run specific spec file(s) or wildcard |
| `--suite` | Run a named suite from wdio.conf.js |
| `--exclude` | Exclude spec file(s) from run |
| `--logLevel` | `trace`, `debug`, `info`, `warn`, `error`, `silent` |
| `--bail` | Stop after N failures (default: 0 = run all) |
| `--maxInstances` | Number of parallel browser instances (2–10) |
| `--baseUrl` | Override base URL for `browser.url()` calls |
| `--repeat` | Repeat specs/suites N times |

### Log Level

- Use `--logLevel=trace` when debugging (maximum output)
- Use default (`info`) when confirming tests pass (less noise)

```bash
npx wdio --logLevel=trace --spec=test/specs/home.js
```

### Bail

```bash
npx wdio --bail=1
```

### Max Instances

```bash
npx wdio --maxInstances=3
```

### Base URL

Changes the base server used with relative paths (e.g., `browser.url('./homepage.html')`).

```bash
npx wdio --baseUrl=https://example.com/
```

## Isolating Individual Tests (Mocha)

Edit the test file temporarily to add `.only` or `.skip`.

### Run only specific tests

```js
describe.only("Form Fields", function () { ... });
it.only("should submit form", function () { ... });
```

[Mocha docs: exclusive tests](https://mochajs.org/#exclusive-tests)

### Skip specific tests

```js
it.skip("should return -1 unless present", function () { ... });
```

[Mocha docs: inclusive tests](https://mochajs.org/#inclusive-tests)

**Remember to revert `.only`/`.skip` changes after debugging.**
