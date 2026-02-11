---
argument-hint: '[--fix]'
context: fork
name: code-review
user-invocable: true
description: This skill should be used when the user asks to "review code", "review PR", "code review", "audit code", "check for bugs", "security review", "review my changes", "find issues in this code", "review the diff", or asks for pull request review or code audit.
---

# Code Review Skill

> **File paths**: All `~/.agents/skills/code-review/references/` paths in this skill resolve under `~/.agents/skills/code-review/`. Do not look for them in the current working directory.

## Overview

Perform expert-level code review focusing on security vulnerabilities, correctness, performance implications, and maintainability. Support multiple languages and ecosystems including TypeScript, React, Node.js, Python, Bash, Solidity, and Solana. Apply industry best practices, security standards, and language-specific idioms. Prioritize findings by severity and provide actionable recommendations with evidence-based reasoning. Keep reviews thorough yet pragmatic, distinguishing between critical issues requiring immediate attention and minor improvements that can be addressed later.

## Review Workflow

**Before starting**: Verify you're in a git repository by running `git rev-parse --git-dir`. If this fails (exit code 128), inform the user they must run the code review from within a git repository and stop.

Parse arguments from `$ARGUMENTS`:
- `--fix`: After presenting findings, automatically apply all suggested fixes without waiting for confirmation. Implement fixes in severity order (CRITICAL → HIGH → MEDIUM → LOW), then report what was changed.
- Default (no `--fix`): Present findings and wait for user confirmation before applying changes.

Begin every code review by running `git diff` to understand the scope of changes. Examine both the changed lines and surrounding context to understand intent. Identify file types being modified: application code, test files, configuration, database migrations, or documentation.

Assess risk level based on change scope and type. High-risk areas include authentication logic, authorization checks, payment processing, data persistence, external API integrations, and cryptographic operations.

Apply appropriate review strategies per file type. Application code requires deep analysis of logic, error handling, and security. Configuration files need validation of limits, timeouts, and environment-specific values. Test files should verify coverage of edge cases and error scenarios.

## Severity Classification

Categorize findings by severity to prioritize remediation efforts:

**🚨 CRITICAL**: Security vulnerabilities enabling unauthorized access, data exfiltration, or code execution. Data loss scenarios including unguarded deletions or destructive migrations without backups. Production outage risks from resource exhaustion, infinite loops, or unhandled exceptions in critical paths. Breaking API changes without versioning or migration paths.

**⚠️ HIGH**: Logic errors producing incorrect results in core functionality. Performance degradation through inefficient algorithms, N+1 queries, or missing indexes. Error handling gaps where failures cascade or leave systems in inconsistent states. Race conditions in concurrent code. Missing input validation on external data.

**💡 MEDIUM**: Maintainability issues including tight coupling, god objects, or violation of single responsibility principle. Missing validation on internal boundaries. Incomplete error messages hindering debugging. Code duplication suggesting need for abstraction. Missing transaction boundaries risking partial updates.

**ℹ️ LOW**: Style inconsistencies not enforced by linters. Documentation gaps in complex logic. Minor naming improvements. Non-critical optimizations with minimal impact.

## Universal Checklist

Apply these language-agnostic patterns to every code review:

**Security Fundamentals**: Check for secrets, API keys, or credentials in code—these belong in environment variables or secure vaults. Examine all input handling for injection vulnerabilities: SQL injection, command injection, path traversal, XSS. Verify authentication checks protect sensitive operations. Confirm authorization validates resource ownership, not just authentication status. Review cryptographic usage for appropriate algorithms, key sizes, and secure random number generation.

**Logic Correctness**: Analyze null and undefined handling—are all code paths safe? Test boundary conditions: empty arrays, zero values, maximum sizes, negative numbers. Trace error paths to ensure failures are handled gracefully and don't expose internal details. Identify potential race conditions in concurrent code: check-then-act patterns, shared mutable state, missing synchronization. Verify loops terminate and recursion has base cases.

**Performance Considerations**: Evaluate algorithmic complexity—O(n²) or worse on unbounded inputs is problematic. Check resource cleanup: files closed, connections released, timers cleared, event listeners removed. Assess caching opportunities for expensive computations or external calls. Review lazy loading and pagination for large datasets. Identify synchronous operations blocking event loops or main threads.

**Maintainability Standards**: Assess coupling—changes should be localized, not rippling across modules. Verify single responsibility—functions and classes should have one reason to change. Check for magic numbers and strings—extract named constants. Review error messages for actionability—include context for debugging.

**Naming Quality**: Names should reveal intent—verb phrases for functions (`validateOrder`, not `process`), descriptive nouns for variables (`userCount`, not `n`), boolean prefixes (`is`, `has`, `can`). See `~/.agents/skills/code-review/references/naming.md` for detailed conventions by language and common anti-patterns.

## Relative Change Analysis

Distinguish between incremental adjustments and fundamental shifts in system behavior. A timeout changing from 1 second to 2 seconds represents 100% increase but minimal risk. The same timeout changing from 1 second to 60 seconds represents 6000% increase and warrants investigation.

Compare new values against established baselines. When reviewing a connection pool size change from 10 to 100, consider current utilization metrics. Is the system exhausting the pool? What's the saturation pattern? Demand evidence supporting the magnitude of change.

Scale risk assessment with change magnitude. Small adjustments (10-50% variation) may reflect tuning. Medium changes (2-5x) require justification with metrics or load testing results. Large changes (10x or more) demand comprehensive evidence: benchmarks, capacity planning, failure mode analysis.

Apply the risk formula: `risk = magnitude × blast_radius × reversibility_difficulty`. High magnitude on low-traffic features may be acceptable. Small magnitude on critical path authentication logic still warrants scrutiny. Consider rollback complexity—database schema changes are harder to reverse than configuration adjustments.

## Environment-Aware Review

Recognize that development, staging, and production environments often employ different limits and configurations. Aggressive timeouts acceptable in development may cause issues in high-latency production environments. Generous resource allocations in staging may not reflect production constraints.

Evaluate whether risky changes are protected by feature flags allowing gradual rollout and quick rollback. Recommend feature flags for changes affecting critical paths, introducing new algorithms, or modifying established behavior with broad impact.

Consider gradual rollout patterns. Canary deployments test changes on small traffic percentages. Blue-green deployments enable atomic switches with quick rollback. Percentage-based feature flags allow progressive exposure monitoring impact at each stage.

Assess rollback planning. Can changes be reverted safely? Do database migrations have down migrations? Are configuration changes backward compatible? Does the deploy process support rapid rollback to previous versions?

## Monitoring Requirements

Define specific metrics to track for different change types. Performance optimizations require before/after latency measurements, throughput metrics, and resource utilization. Database changes need query execution time, lock contention, and connection pool saturation. External API integrations require success rates, timeout occurrences, and circuit breaker state transitions.

Establish alerting thresholds before deploying changes. Define acceptable error rate increases, latency percentiles, and throughput degradation. Set thresholds based on historical baselines and business requirements. Alert on anomalies rather than absolute values when traffic patterns vary.

Identify necessary dashboards and observability improvements. New features need monitoring of adoption metrics, error rates, and performance. Refactored code should maintain existing observability or improve it. Infrastructure changes require visibility into resource utilization and saturation.

Assess SLO and SLA impact. Will changes affect availability, latency, or error rate commitments? Do capacity changes risk SLA breaches under peak load? Are there graceful degradation strategies if changes introduce issues?

## Output Format

Structure review findings for maximum clarity and actionability:

Group issues by severity level, presenting CRITICAL findings first, followed by HIGH, MEDIUM, and LOW. Within each severity tier, group related issues together.

Include file paths and line numbers when available. When line numbers are uncertain, cite function names with quoted snippets. Never fabricate line references. Use the format `path/to/file.ts:42-45` to specify exact locations. Quote relevant code snippets when helpful for context.

Provide evidence-based findings rather than opinions. Reference security standards (OWASP), performance benchmarks, or language best practices. Explain the potential impact and attack vectors for security issues. Quantify performance implications when possible.

Deliver actionable recommendations with specificity. Instead of "improve error handling," suggest "wrap database operations in try-catch and return user-friendly error response." Provide code examples demonstrating fixes when helpful, but avoid rewriting entire functions unless requested.

Acknowledge good practices observed in the code. Highlight effective patterns, thorough test coverage, or well-designed abstractions. Balanced feedback strengthens credibility and encourages continuation of positive practices.

## Review Template

Structure reviews consistently:

1. **Context Questions** (if needed): 1-3 clarifying questions about intent or constraints
2. **Findings**: Grouped by severity (CRITICAL → HIGH → MEDIUM → LOW)
3. **Suggested Fixes**: Code snippets or specific recommendations
4. **Deployment Notes**: Rollout strategy, monitoring requirements (when applicable)
5. **Applied Fixes** (only when `--fix` is present): concrete list of implemented changes with file references

**Important**:
- Default behavior: After presenting findings, wait for the user to confirm which issues to address.
- With `--fix`: Do not wait for confirmation. Apply all suggested fixes automatically, then provide an implementation summary and any remaining follow-ups.

## Additional Resources

Consult specialized reference documents for in-depth guidance on specific review areas:

- **~/.agents/skills/code-review/references/configuration.md** - Configuration file review patterns including environment-specific validation, secrets management, and limit tuning
- **~/.agents/skills/code-review/references/security.md** - Comprehensive security review covering OWASP Top 10, authentication patterns, authorization models, cryptography, input validation, and secure defaults
- **~/.agents/skills/code-review/references/typescript-react.md** - Frontend and Node.js patterns including React hooks, state management, TypeScript type safety, async handling, and API design
- **~/.agents/skills/code-review/references/python.md** - Python-specific patterns covering type hints, async/await, exception handling, context managers, and common library pitfalls
- **~/.agents/skills/code-review/references/smart-contracts.md** - Blockchain security for Solidity and Solana including reentrancy, integer overflow, access control, and economic attack vectors
- **~/.agents/skills/code-review/references/shell.md** - Bash script review covering quoting, error handling, portability, security risks from command injection and path traversal
- **~/.agents/skills/code-review/references/data-formats.md** - CSV, JSON, and data format handling including parsing safety, schema validation, and encoding issues
- **~/.agents/skills/code-review/references/naming.md** - Naming conventions covering functions, variables, files, classes, and constants with language-specific patterns and common anti-patterns

Reference these documents when reviewing code in their respective domains for detailed checklists and language-specific vulnerabilities.

### Examples

- **~/.agents/skills/code-review/references/example-good-review.md** - Exemplary review output demonstrating proper structure, severity grouping, and actionable recommendations
- **~/.agents/skills/code-review/references/example-bad-review.md** - Anti-patterns to avoid including fabricated line numbers, vague findings, and opinion without evidence
