---
name: monitoring
description: Create and manage monitoring checks using the Checkly CLI. Use when working with API checks, browser checks, URL monitors, Playwright checks, heartbeat monitors, alert channels, dashboards, or status pages.
allowed-tools: Bash(npx:checkly:*) Bash(npm:create:checkly@latest)
metadata:
  author: checkly
---

# Checkly Monitoring

- Refer to docs for Checkly CLI v6.0.0 and above.
- Check the Checkly CLI output to figure out into which folder the setup was generated.
- Use the [Checkly CLI reference documentation](https://www.checklyhq.com/docs/cli/overview/).
- Use the [Checkly construct reference documentation](https://www.checklyhq.com/docs/constructs/overview/).
- Import and / or require any constructs you need in your code, such as `ApiCheck`, `BrowserCheck`, or `PlaywrightCheck` from the `checkly/constructs` package.
- Always ground generated code and CLI commands against the official documentation and examples in this file.

## Installing the Checkly CLI

- ALWAYS use `npm create checkly@latest`.
- NEVER make up commands that do not exist.

## Project Structure

- `checkly.config.ts` - Mandatory global project and CLI configuration. We recommend using TypeScript.
- `*.check.ts|js` - TS / JS files that define the checks.
- `*.spec.ts|js` - TS / JS files that contain Playwright code for Browser and MultiStep checks.
- `src/__checks__` - Default directory where all your checks are stored. Use this directory if it already exists, otherwise create a new directory for your checks.
- `package.json` - Standard NPM project manifest.

Here is an example directory tree of what that would look like:

.
|-- checkly.config.ts
|-- package.json
`-- src
    `-- __checks__
|-- alert-channels.ts
|-- api-check.check.ts
`-- homepage.spec.ts

The `checkly.config.ts` at the root of your project defines a range of defaults for all your checks.

**Reference:** https://www.checklyhq.com/docs/constructs/project/

```typescript
import { defineConfig } from 'checkly'
import { Frequency } from 'checkly/constructs'

export default defineConfig({
  projectName: "Production Monitoring Suite",
  logicalId: "prod-monitoring-2025",
  repoUrl: "https://github.com/acme/monitoring",
  checks: {
    activated: true,
    muted: false,
    runtimeId: "2025.04",
    frequency: Frequency.EVERY_10M,
    locations: ["us-east-1", "eu-west-1", "ap-southeast-1"],
    tags: ["production", "critical"],
    checkMatch: "**/__checks__/*.check.ts",
    ignoreDirectoriesMatch: ["node_modules/**", "dist/**"],
    playwrightConfig: {
      use: {
        baseURL: "https://app.example.com",
      },
    },
    browserChecks: {
      frequency: Frequency.EVERY_30M,
      testMatch: "**/__tests__/*.spec.ts",
    },
  },
  cli: {
    runLocation: "eu-west-1",
    privateRunLocation: "private-dc1",
    retries: 2,
  },
})
```

## Check and Monitor Constructs

### API Check

- Import the `ApiCheck` construct from `checkly/constructs`.
- When adding `assertions`, always use `AssertionBuilder` class for API Checks.
- When referencing environment variables always use the handlebar syntax `{{MY_ENV_VAR}}`.
- When referencing secrets always use the handlebar syntax `{{MY_SECRET}}`.
- If endpoints require authentication ask the user which authentication method to use and then generate a setupScript to authenticate the given requests.
- Referenced `setupScript.ts` and `teardownScript.ts` for API checks must be plain ts files and not export anything.
- Check in the code if API endpoints require authentication.

**Reference:** https://www.checklyhq.com/docs/constructs/api-check/

```typescript
import { AlertEscalationBuilder, ApiCheck, Frequency, RetryStrategyBuilder } from 'checkly/constructs'

new ApiCheck('example-api-check', {
  name: 'Example API Check',
  request: {
    url: 'https://api.example.com/v1/products',
    method: 'GET',
    ipFamily: 'IPv4',
  },
  setupScript: {
    entrypoint: './setup-script.ts',
  },
  tearDownScript: {
    entrypoint: './teardown-script.ts',
  },
  degradedResponseTime: 5000,
  maxResponseTime: 20000,
  activated: true,
  muted: false,
  shouldFail: false,
  locations: [
    'eu-central-1',
    'eu-west-2',
  ],
  frequency: Frequency.EVERY_5M,
  alertEscalationPolicy: AlertEscalationBuilder.runBasedEscalation(1, {
    amount: 0,
    interval: 5,
  }, {
    enabled: false,
    percentage: 10,
  }),
  retryStrategy: RetryStrategyBuilder.linearStrategy({
    baseBackoffSeconds: 60,
    maxRetries: 2,
    maxDurationSeconds: 600,
    sameRegion: true,
  }),
  runParallel: true,
})
```

#### Authentication Setup Scripts for API Checks

- Setup scripts should be flat scripts, no functions, no exports, they will be executed straight by Checkly.
- Use axios for making HTTP requests.
- Read the input credentials from env variables using `process.env`.
- Pass auth tokens to the request object using `request.headers['key'] = AUTH_TOKEN_VALUE`.

### Browser Check

- Import the `BrowserCheck` construct from `checkly/constructs`.
- Generate a separate `.spec.ts` file for the Playwright code referenced in the `BrowserCheck` construct.
- Use the `code.entrypoint` property to specify the path to your Playwright test file.

**Reference:** https://www.checklyhq.com/docs/constructs/browser-check/

```typescript
import { AlertEscalationBuilder, BrowserCheck, Frequency, RetryStrategyBuilder } from 'checkly/constructs'

new BrowserCheck('example-browser-check', {
  name: 'Example Browser Check',
  code: {
    entrypoint: './example-browser-check.spec.ts',
  },
  activated: false,
  muted: false,
  shouldFail: false,
  locations: [
    'eu-central-1',
    'eu-west-2',
  ],
  frequency: Frequency.EVERY_10M,
  alertEscalationPolicy: AlertEscalationBuilder.runBasedEscalation(1, {
    amount: 0,
    interval: 5,
  }, {
    enabled: false,
    percentage: 10,
  }),
  retryStrategy: RetryStrategyBuilder.linearStrategy({
    baseBackoffSeconds: 60,
    maxRetries: 2,
    maxDurationSeconds: 600,
    sameRegion: true,
  }),
  runParallel: true,
})
```

### Playwright Check Suite

- Import the `PlaywrightCheck` construct from `checkly/constructs`.
- use `pwProjects` if your tasked to reuse a Playwright project.

**Reference:** https://www.checklyhq.com/docs/constructs/playwright-check/

```typescript
import { PlaywrightCheck } from "checkly/constructs"

const playwrightChecks = new PlaywrightCheck("multi-browser-check", {
  name: "Multi-browser check suite",
  playwrightConfigPath: "./playwright.config.ts",
  // Playwright Check Suites support all browsers
  // defined in your `playwright.config`
  pwProjects: ["chromium", "firefox", "webkit"],
});
```

### MultiStep Check

- Import the `MultiStepCheck` construct from `checkly/constructs`.
- Generate a separate `.spec.ts` file for the Playwright code referenced in the `MultiStepCheck` construct.
- Use the `code.entrypoint` property to specify the path to your Playwright test file.

**Reference:** https://www.checklyhq.com/docs/constructs/multistep-check/

```typescript
import { AlertEscalationBuilder, Frequency, MultiStepCheck, RetryStrategyBuilder } from 'checkly/constructs'

new MultiStepCheck('example-multi-step-check', {
  name: 'Example Multistep Check',
  code: {
    entrypoint: './example-multistep-check.spec.ts',
  },
  activated: true,
  muted: false,
  shouldFail: false,
  locations: [
    'eu-central-1',
    'eu-west-2',
  ],
  frequency: Frequency.EVERY_1H,
  alertEscalationPolicy: AlertEscalationBuilder.runBasedEscalation(1, {
    amount: 0,
    interval: 5,
  }, {
    enabled: false,
    percentage: 10,
  }),
  retryStrategy: RetryStrategyBuilder.noRetries(),
  runParallel: true,
})
```

### TCP Monitor

- Import the `TcpMonitor` construct from `checkly/constructs`.
- When adding `assertions`, always use `TcpAssertionBuilder` class for TCP monitors.

**Reference:** https://www.checklyhq.com/docs/constructs/tcp-monitor/

```typescript
import { AlertEscalationBuilder, Frequency, RetryStrategyBuilder, TcpAssertionBuilder, TcpMonitor } from 'checkly/constructs'

new TcpMonitor('example-tcp-monitor', {
  name: 'Example TCP Monitor',
  request: {
    hostname: 'tcp.example.com',
    port: 4242,
    ipFamily: 'IPv4',
    assertions: [
      TcpAssertionBuilder.responseTime().lessThan(200),
      TcpAssertionBuilder.responseData().isEmpty(),
    ],
  },
  degradedResponseTime: 5000,
  maxResponseTime: 5000,
  activated: true,
  muted: false,
  shouldFail: false,
  locations: [
    'eu-central-1',
    'eu-west-2',
  ],
  frequency: Frequency.EVERY_1H,
  alertEscalationPolicy: AlertEscalationBuilder.runBasedEscalation(1, {
    amount: 0,
    interval: 5,
  }, {
    enabled: false,
    percentage: 10,
  }),
  retryStrategy: RetryStrategyBuilder.linearStrategy({
    baseBackoffSeconds: 60,
    maxRetries: 2,
    maxDurationSeconds: 600,
    sameRegion: true,
  }),
  runParallel: true,
})
```

### URL Monitor

- Import the `UrlMonitor` construct from `checkly/constructs`.
- When adding `assertions`, always use `UrlAssertionBuilder`.

**Reference:** https://www.checklyhq.com/docs/constructs/url-monitor/

```typescript
import { AlertEscalationBuilder, Frequency, RetryStrategyBuilder, UrlAssertionBuilder, UrlMonitor } from 'checkly/constructs'

new UrlMonitor('example-url-monitor', {
  name: 'Example URL Monitor',
  request: {
    url: 'https://example.com',
    ipFamily: 'IPv4',
    assertions: [
      UrlAssertionBuilder.statusCode().equals(200),
    ],
  },
  degradedResponseTime: 5000,
  maxResponseTime: 20000,
  activated: true,
  muted: false,
  shouldFail: false,
  locations: [
    'eu-central-1',
    'eu-west-2',
  ],
  frequency: Frequency.EVERY_5M,
  alertEscalationPolicy: AlertEscalationBuilder.runBasedEscalation(1, {
    amount: 0,
    interval: 5,
  }, {
    enabled: false,
    percentage: 10,
  }),
  retryStrategy: RetryStrategyBuilder.linearStrategy({
    baseBackoffSeconds: 60,
    maxRetries: 2,
    maxDurationSeconds: 600,
    sameRegion: true,
  }),
  runParallel: true,
})
```

### DNS Monitor

- Import the `DnsMonitor` construct from `checkly/constructs`.
- Reference [the docs for DNS monitors](https://www.checklyhq.com/docs/constructs/dns-monitor/) before generating any code.
- When adding `assertions`, always use `DnsAssertionBuilder` class.

**Reference:** https://www.checklyhq.com/docs/constructs/dns-monitor/

```typescript
import { AlertEscalationBuilder, DnsAssertionBuilder, DnsMonitor, Frequency, RetryStrategyBuilder } from 'checkly/constructs'

new DnsMonitor('example-dns-monitor', {
  name: 'Example DNS Monitor',
  request: {
    recordType: 'AAAA',
    query: 'welcome.checklyhq.com',
    assertions: [
      DnsAssertionBuilder.responseCode().equals('NOERROR'),
    ],
  },
  degradedResponseTime: 500,
  maxResponseTime: 1000,
  activated: true,
  muted: false,
  shouldFail: false,
  locations: [
    'eu-central-1',
    'eu-north-1',
  ],
  frequency: Frequency.EVERY_10M,
  alertEscalationPolicy: AlertEscalationBuilder.runBasedEscalation(1, {
    amount: 0,
    interval: 5,
  }, {
    enabled: false,
    percentage: 10,
  }),
  retryStrategy: RetryStrategyBuilder.noRetries(),
  runParallel: false,
})
```

### Heartbeat Monitor

- Import the `HeartbeatMonitor` construct from `checkly/constructs`.

**Reference:** https://www.checklyhq.com/docs/constructs/heartbeat-monitor/

```typescript
import { AlertEscalationBuilder, Frequency, HeartbeatMonitor, RetryStrategyBuilder } from 'checkly/constructs'

new HeartbeatMonitor('example-heartbeat-monitor', {
  name: 'Example Heartbeat Monitor',
  period: 1,
  periodUnit: 'hours',
  grace: 30,
  graceUnit: 'minutes',
  activated: true,
  muted: false,
  shouldFail: false,
  frequency: Frequency.EVERY_10S,
  alertEscalationPolicy: AlertEscalationBuilder.runBasedEscalation(1, {
    amount: 0,
    interval: 5,
  }, {
    enabled: false,
    percentage: 10,
  }),
  retryStrategy: RetryStrategyBuilder.linearStrategy({
    baseBackoffSeconds: 60,
    maxRetries: 2,
    maxDurationSeconds: 600,
    sameRegion: true,
  }),
  runParallel: true,
})
```

### Check Group

- Import the `CheckGroupV2` construct from `checkly/constructs`.
- Check Groups are used to group checks together for easier management and organization.
- Checks are added to Check Groups by referencing the group in the `group` property of a check.

**Reference:** https://www.checklyhq.com/docs/constructs/check-group/

```typescript
import { CheckGroupV2 } from 'checkly/constructs'

export const exampleGroup = new CheckGroupV2('example-group', {
  name: 'Example Group',
})
```

## Alert Channel Constructs

- Alert channels are used to send notifications when checks and monitors fail or recover.
- Alert channels are added to checks, monitors, and check groups constructs by adding them to the `alertChannels` array property.

Here are some examples of how to create different types of alert channels. All alert are described in the [Checkly docs](https://www.checklyhq.com/docs/constructs/overview/).

### Email Alert Channel

**Reference:** https://www.checklyhq.com/docs/constructs/email-alert-channel/

```typescript
import { EmailAlertChannel } from 'checkly/constructs'

export const testEmailAlert = new EmailAlertChannel('example-email-alert-channel', {
  address: 'test@example.com',
  sslExpiry: true,
})
```


### Phone Call Alert Channel

**Reference:** https://www.checklyhq.com/docs/constructs/phone-call-alert-channel/

```typescript
import { PhoneCallAlertChannel } from 'checkly/constructs'

export const testUserPhoneCallAlert = new PhoneCallAlertChannel('example-call-alert-channel', {
  name: 'Test User',
  phoneNumber: '+311234567890',
})
```


### Slack Alert Channel

**Reference:** https://www.checklyhq.com/docs/constructs/slack-alert-channel/

```typescript
import { SlackAlertChannel } from 'checkly/constructs'

export const generalSlackAlert = new SlackAlertChannel('example-slack-alert-channel', {
  url: 'https://hooks.slack.com/services/TK123456789123/12345/123456789',
  channel: '#general',
})
```


## Supporting Constructs

### Status Page

- Import the `StatusPage` construct from `checkly/constructs`.
- Status pages are used to display the status of your services to your users.
- A Status Page consists of cards which include Status Page Services.

**Reference:** https://www.checklyhq.com/docs/constructs/status-page/

```typescript
import { StatusPage } from 'checkly/constructs'
import { exampleService } from './services/example-service.check'

new StatusPage('example-status-page', {
  name: 'Example Status Page',
  url: 'example-status-page',
  cards: [
    {
      name: 'Example service',
      services: [
        exampleService,
      ],
    },
  ],
  customDomain: 'status.example.com',
  defaultTheme: 'AUTO',
})
```

### Status Page Service

- Import the `StatusPageService` construct from `checkly/constructs`.
- Status Page Services are used to represent individual services on a Status Page.

**Reference:** https://www.checklyhq.com/docs/constructs/status-page-service/

```typescript
import { StatusPageService } from 'checkly/constructs'

export const exampleService = new StatusPageService('example-status-page-service', {
  name: 'Example Service',
})
```

### Dashboard

- Import the `Dashboard` construct from `checkly/constructs`.
- Dashboards are used to display the results of your checks on screens external to Checkly.

**Reference:** https://www.checklyhq.com/docs/constructs/dashboard/

```typescript
import { Dashboard } from 'checkly/constructs'

new Dashboard('example-dashboard', {
  tags: [
    'app:webshop',
  ],
  customUrl: 'example-dashboard',
  customDomain: 'dash.example.com',
  header: 'Example Dashboard',
  description: 'Example dashboard',
  width: 'FULL',
  refreshRate: 60,
  paginate: true,
  paginationRate: 60,
  checksPerPage: 15,
  useTagsAndOperator: false,
  hideTags: false,
  enableIncidents: false,
  expandChecks: false,
  showHeader: true,
  isPrivate: false,
  showP95: true,
  showP99: true,
})
```

### Maintenance Window

- Import the `MaintenanceWindow` construct from `checkly/constructs`.
- Maintenance windows are used to pause checks during maintenance periods so no alerts are sent.
- Checks are referenced by their tags in the `tags` property.

**Reference:** https://www.checklyhq.com/docs/constructs/maintenance-window/

```typescript
import { MaintenanceWindow } from 'checkly/constructs'

new MaintenanceWindow('example-maintenance-window', {
  name: 'Example Maintenance Window',
  tags: [
    'app:webshop',
  ],
  startsAt: new Date('2025-07-01T09:00:00.000Z'),
  endsAt: new Date('2025-07-01T10:00:00.000Z'),
  repeatInterval: 1,
  repeatUnit: 'WEEK',
  repeatEndsAt: new Date('2025-08-01T00:00:00.000Z'),
})
```

### Private Location

- Import the `PrivateLocation` construct from `checkly/constructs`.
- Private locations are used to run checks from your own infrastructure with the Checkly Agent, an OCI compatible container.

**Reference:** https://www.checklyhq.com/docs/constructs/private-location/

```typescript
import { PrivateLocation } from 'checkly/constructs'

export const examplePrivateLocation = new PrivateLocation('example-private-location', {
  name: 'Example Private Location',
  slugName: 'example-private-location',
  icon: 'location',
})
```

## Testing and Debugging

- Test checks using `npx checkly test` command pass env variables using `-e` param, use `--record` to persist results and `--verbose` to be able to see all errors
