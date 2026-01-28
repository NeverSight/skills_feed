---
name: implementing-cli-patterns
description: "Implements CLI user experience with output formatting, progress indicators, and interactive prompts. Uses chalk, ora, and inquirer for consistent terminal interactions. Triggers on: CLI output, progress bar, spinner, ora, chalk, inquirer prompts, error formatting, exit codes, reporter."
allowed-tools: "Read, Grep, Glob, Write, Edit"
---

# CLI User Experience Patterns

## Purpose

Guide the implementation of consistent and user-friendly CLI interactions including output formatting, progress tracking, interactive prompts, and error messaging.

## When to Use

- Implementing command output
- Adding progress indicators
- Creating user prompts
- Formatting error messages
- Designing reporter output

## Table of Contents

- [CLI Stack](#cli-stack)
- [Console Module Patterns](#console-module-patterns)
- [Progress Indicators](#progress-indicators)
- [Interactive Prompts](#interactive-prompts)
- [Reporter Patterns](#reporter-patterns)
- [Error Message Formatting](#error-message-formatting)
- [Exit Codes](#exit-codes)
- [Best Practices](#best-practices)
- [References](#references)

## CLI Stack

| Tool | Purpose |
|------|---------|
| **chalk** | Colored terminal output |
| **ora** | Spinner/progress indicators |
| **@inquirer/prompts** | Interactive user prompts |
| **tslog** | Structured logging |

## Console Module Patterns

### Message Types

Located in `src/cli/console.ts`:

```typescript
import chalk from 'chalk';

export const console = {
  // Error messages (red)
  error: (message: string) => {
    console.log(chalk.red(`✖ ${message}`));
  },

  // Success messages (green)
  success: (message: string) => {
    console.log(chalk.green(`✔ ${message}`));
  },

  // Warning messages (yellow)
  warning: (message: string) => {
    console.log(chalk.yellow(`⚠ ${message}`));
  },

  // Hint messages (cyan)
  hint: (message: string) => {
    console.log(chalk.cyan(`💡 ${message}`));
  },

  // Important messages (bold)
  important: (message: string) => {
    console.log(chalk.bold(message));
  },

  // Code blocks (gray background)
  code: (code: string) => {
    console.log(chalk.bgGray.white(` ${code} `));
  },

  // Info messages (blue)
  info: (message: string) => {
    console.log(chalk.blue(`ℹ ${message}`));
  },
};
```

### Usage Examples

```typescript
import { console } from '@/cli/console';

// Command success
console.success('Configuration deployed successfully');

// Error with context
console.error(`Failed to create category: ${error.message}`);

// Helpful hints
console.hint('Run `configurator diff` to preview changes');

// Important information
console.important('This action cannot be undone');

// Code snippets
console.code('pnpm deploy --url=<URL> --token=<TOKEN>');
```

## Progress Indicators

### Spinner for Single Operations

```typescript
import ora from 'ora';

const spinner = ora('Fetching categories...').start();

try {
  const categories = await fetchCategories();
  spinner.succeed(`Fetched ${categories.length} categories`);
} catch (error) {
  spinner.fail('Failed to fetch categories');
  throw error;
}
```

### Progress Bar for Bulk Operations

```typescript
// src/cli/progress.ts
export class BulkOperationProgress {
  private total: number;
  private completed: number = 0;
  private failed: number = 0;

  constructor(total: number, private label: string) {
    this.total = total;
  }

  tick(success: boolean = true): void {
    if (success) {
      this.completed++;
    } else {
      this.failed++;
    }
    this.render();
  }

  private render(): void {
    const percent = Math.round(((this.completed + this.failed) / this.total) * 100);
    const bar = this.createBar(percent);
    process.stdout.write(`\r${this.label}: ${bar} ${percent}% (${this.completed}/${this.total})`);
  }

  private createBar(percent: number): string {
    const filled = Math.round(percent / 5);
    const empty = 20 - filled;
    return `[${'█'.repeat(filled)}${'░'.repeat(empty)}]`;
  }

  finish(): void {
    console.log(''); // New line
    if (this.failed > 0) {
      console.warning(`Completed with ${this.failed} failures`);
    } else {
      console.success(`All ${this.completed} items processed`);
    }
  }
}
```

### Usage

```typescript
const progress = new BulkOperationProgress(items.length, 'Deploying products');

for (const item of items) {
  try {
    await deployItem(item);
    progress.tick(true);
  } catch (error) {
    progress.tick(false);
    failures.push({ item, error });
  }
}

progress.finish();
```

## Interactive Prompts

### Confirmation Prompt

```typescript
import { confirm } from '@inquirer/prompts';

const shouldProceed = await confirm({
  message: 'This will overwrite existing configuration. Continue?',
  default: false,
});

if (!shouldProceed) {
  console.info('Operation cancelled');
  process.exit(0);
}
```

### Select Prompt

```typescript
import { select } from '@inquirer/prompts';

const action = await select({
  message: 'Select deployment mode:',
  choices: [
    { name: 'Full deployment', value: 'full' },
    { name: 'Incremental (only changes)', value: 'incremental' },
    { name: 'Dry run (preview only)', value: 'dry-run' },
  ],
});
```

### Multi-Select Prompt

```typescript
import { checkbox } from '@inquirer/prompts';

const entities = await checkbox({
  message: 'Select entities to deploy:',
  choices: [
    { name: 'Product Types', value: 'productTypes', checked: true },
    { name: 'Categories', value: 'categories', checked: true },
    { name: 'Products', value: 'products', checked: false },
    { name: 'Menus', value: 'menus', checked: false },
  ],
});
```

### Input Prompt

```typescript
import { input } from '@inquirer/prompts';

const apiUrl = await input({
  message: 'Enter Saleor API URL:',
  default: 'https://your-store.saleor.cloud/graphql/',
  validate: (value) => {
    if (!value.startsWith('https://')) {
      return 'URL must start with https://';
    }
    return true;
  },
});
```

### Password Prompt

```typescript
import { password } from '@inquirer/prompts';

const token = await password({
  message: 'Enter API token:',
  mask: '*',
});
```

## Reporter Patterns

### Deployment Result Reporter

```typescript
// src/cli/reporters/deployment-reporter.ts
export interface DeploymentResult {
  entity: string;
  created: number;
  updated: number;
  deleted: number;
  failed: number;
  duration: number;
}

export const reportDeploymentResults = (results: DeploymentResult[]): void => {
  console.log('');
  console.important('Deployment Summary');
  console.log('─'.repeat(60));

  const headers = ['Entity', 'Created', 'Updated', 'Deleted', 'Failed', 'Time'];
  console.log(formatTableRow(headers));
  console.log('─'.repeat(60));

  for (const result of results) {
    const row = [
      result.entity,
      chalk.green(String(result.created)),
      chalk.blue(String(result.updated)),
      chalk.yellow(String(result.deleted)),
      result.failed > 0 ? chalk.red(String(result.failed)) : '0',
      `${result.duration}ms`,
    ];
    console.log(formatTableRow(row));
  }

  console.log('─'.repeat(60));

  const totals = results.reduce(
    (acc, r) => ({
      created: acc.created + r.created,
      updated: acc.updated + r.updated,
      deleted: acc.deleted + r.deleted,
      failed: acc.failed + r.failed,
    }),
    { created: 0, updated: 0, deleted: 0, failed: 0 }
  );

  if (totals.failed > 0) {
    console.warning(`Completed with ${totals.failed} failures`);
  } else {
    console.success('Deployment completed successfully');
  }
};
```

### Diff Reporter

```typescript
export const reportDiff = (diffs: DiffResult[]): void => {
  for (const diff of diffs) {
    switch (diff.action) {
      case 'create':
        console.log(chalk.green(`+ ${diff.entity}: ${diff.identifier}`));
        break;
      case 'update':
        console.log(chalk.blue(`~ ${diff.entity}: ${diff.identifier}`));
        for (const change of diff.changes) {
          console.log(chalk.gray(`  ${change.field}: ${change.from} → ${change.to}`));
        }
        break;
      case 'delete':
        console.log(chalk.red(`- ${diff.entity}: ${diff.identifier}`));
        break;
    }
  }

  console.log('');
  console.info(`Total: ${diffs.filter(d => d.action === 'create').length} to create, ` +
    `${diffs.filter(d => d.action === 'update').length} to update, ` +
    `${diffs.filter(d => d.action === 'delete').length} to delete`);
};
```

### Duplicate Issue Reporter

```typescript
export const reportDuplicates = (duplicates: DuplicateIssue[]): void => {
  if (duplicates.length === 0) return;

  console.log('');
  console.warning('Duplicate identifiers detected:');
  console.log('');

  for (const dup of duplicates) {
    console.log(chalk.yellow(`  ${dup.entityType}: "${dup.identifier}"`));
    console.log(chalk.gray(`    Found at: ${dup.locations.join(', ')}`));
  }

  console.log('');
  console.hint('Fix duplicates before deploying to avoid conflicts');
};
```

## Error Message Formatting

### Structured Error Output

```typescript
export const formatError = (error: BaseError): void => {
  console.log('');
  console.error(error.message);

  if (error.code) {
    console.log(chalk.gray(`  Error code: ${error.code}`));
  }

  if (error.context) {
    console.log(chalk.gray(`  Context: ${JSON.stringify(error.context)}`));
  }

  const suggestions = error.getSuggestions?.();
  if (suggestions?.length) {
    console.log('');
    console.hint('Suggestions:');
    for (const suggestion of suggestions) {
      console.log(chalk.cyan(`  • ${suggestion}`));
    }
  }
};
```

### GraphQL Error Formatting

```typescript
export const formatGraphQLError = (error: GraphQLError): void => {
  console.error(`GraphQL operation failed: ${error.operationName}`);

  if (error.errors?.length) {
    for (const gqlError of error.errors) {
      console.log(chalk.red(`  • ${gqlError.message}`));
      if (gqlError.path) {
        console.log(chalk.gray(`    Path: ${gqlError.path.join('.')}`));
      }
    }
  }
};
```

## Exit Codes

```typescript
export const ExitCodes = {
  SUCCESS: 0,
  GENERAL_ERROR: 1,
  VALIDATION_ERROR: 2,
  NETWORK_ERROR: 3,
  AUTH_ERROR: 4,
  CONFLICT_ERROR: 5,
} as const;

// Usage
if (validationErrors.length > 0) {
  reportValidationErrors(validationErrors);
  process.exit(ExitCodes.VALIDATION_ERROR);
}
```

## Best Practices

### Do's

- Use consistent colors for message types
- Provide progress feedback for long operations
- Include actionable suggestions with errors
- Confirm destructive operations
- Support both interactive and non-interactive modes

### Don'ts

- Don't spam the console with debug output
- Don't use raw console.log in production code
- Don't block on prompts in CI/headless mode
- Don't hide important information behind verbosity flags

## References

- `{baseDir}/src/cli/console.ts` - Console module
- `{baseDir}/src/cli/progress.ts` - Progress tracking
- `{baseDir}/src/cli/reporters/` - Reporter implementations
- chalk documentation: https://github.com/chalk/chalk
- ora documentation: https://github.com/sindresorhus/ora
- inquirer documentation: https://github.com/SBoudrias/Inquirer.js

## Related Skills

- **Complete entity workflow**: See `adding-entity-types` for CLI integration patterns
- **Error handling**: See `reviewing-typescript-code` for error message standards

## Quick Reference Rule

For a condensed quick reference, see `.claude/rules/cli-development.md` (automatically loaded when editing `src/cli/**/*.ts` and `src/commands/**/*.ts` files).
