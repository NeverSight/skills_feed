---
name: ship
description: Deliver code to users. Optimize the path from merged code to working install. Use when execution is complete and you need to get changes into users' hands.
---

# /ship

Optimize the delivery path from completed work to working install. The insight: **when execution is cheap, delivery is the work.**

Ship is the final step of the Execution phase. Code that isn't in users' hands isn't delivering value. This skill identifies and removes friction in your delivery path.

## When to Use

Invoke `/ship` when:

- **Execution is complete** - code is ready, tests pass, review is done
- **You need to deploy** - getting changes from merged to running
- **Delivery feels slow** - the code is done but it's not reaching users
- **You're blocked on gates** - reviews, scans, approvals are piling up
- **You want to automate delivery** - make the path from code to install frictionless

**Do not use when:** You're still building. Ship is for getting completed work to users, not for execution.

## The Ship Process

### Step 1: Identify the Delivery Path

Before shipping, map the path from code to working install:

> "The delivery path for this change is: [local] -> [PR/review] -> [merge] -> [CI/CD] -> [staging/prod] -> [user install]."

Be specific. Name each step and who/what owns it.

### Step 2: Assess the Delivery-Path Tax

The delivery-path tax is the friction that slows velocity. Identify where time is lost:

#### Review Time
- How long do PRs wait for review?
- Is the review queue a bottleneck?
- Can AI review pre-check before human review?

#### Merge Time
- Are there merge conflicts blocking progress?
- Is the main branch unstable?
- How long from approval to merge?

#### Gate/Scan Time
- Security scans, compliance checks, quality gates
- Are gates running in parallel or serial?
- Which gates are flaky or slow?

#### Approval Time
- Who needs to approve?
- Are approvers available?
- Can approval be automated for low-risk changes?

#### Deploy Time
- How long does deployment take?
- Is rollback fast if needed?
- Are there manual steps?

### Step 3: Execute the Ship

Based on context available, execute the appropriate shipping actions:

#### With CI/CD Context
If you have access to the CI/CD configuration (build YAML, pipeline definitions):

1. **Reference the pipeline** - Point to the specific build/deploy configuration
2. **Trigger the appropriate workflow** - Label PRs, push to deploy branches, etc.
3. **Monitor the pipeline** - Watch for failures, report status
4. **Verify deployment** - Confirm the change is live

#### Without CI/CD Context
If shipping manually or without pipeline access:

1. **List deployment steps** - What needs to happen in order?
2. **Execute each step** - Or provide commands to execute
3. **Verify each stage** - Confirm success before proceeding
4. **Report final status** - Confirm user-facing change is live

### Step 4: Post-Ship Verification

Shipping isn't done until you verify:

- **Is it running?** - The code is deployed and executing
- **Is it working?** - The intended behavior is present
- **Is it reachable?** - Users can access/use it

Create ad-hoc verification tests if needed. These can be kept or discarded - the point is confidence, not permanent test infrastructure.

## Output Format

Always produce a ship report in this structure:

```
## Ship Report

**Shipped:** [what was shipped]
**Target:** [where it was shipped to]
**Path:** [the delivery path taken]

### Delivery-Path Tax Identified
- [Friction point 1]: [time/effort cost]
- [Friction point 2]: [time/effort cost]

### Ship Actions Taken
1. [Action 1 - result]
2. [Action 2 - result]
3. [Action 3 - result]

### Verification
- [x] Deployed successfully
- [x] Running in target environment
- [x] User-facing functionality confirmed

### Recommendations
[Any suggestions for reducing delivery-path tax in future]
```

## Examples

### Example 1: Shipping with CI/CD Pipeline

```
/ship

PR #247 is approved. Need to get it deployed to production.
```

**Output:**
```
## Ship Report

**Shipped:** PR #247 - Add dark mode toggle
**Target:** Production (users)
**Path:** Approved PR -> Merge -> CI build -> Staging auto-deploy -> Prod deploy

### Delivery-Path Tax Identified
- Review time: 2 hours (acceptable)
- CI build: 8 minutes
- Staging deploy: 3 minutes
- Prod approval: Waiting (manual gate)

### Ship Actions Taken
1. Merged PR #247 to main - success
2. CI build triggered automatically - passed (8m)
3. Staging deploy completed - verified working
4. Requested prod deployment approval
5. Prod deploy completed after approval

### Verification
- [x] Build passed CI
- [x] Staging environment shows dark mode toggle
- [x] Production deployment complete
- [x] User-facing: toggle visible in settings

### Recommendations
- Consider auto-deploy to prod for UI-only changes (low risk)
- Staging verification could be automated
```

### Example 2: Identifying Delivery-Path Tax

```
/ship

We've had 3 PRs sitting for a week. What's blocking us?
```

**Output:**
```
## Ship Report

**Shipped:** Analysis only (no deployment)
**Target:** Identifying delivery friction

### Delivery-Path Tax Identified
- Review time: 5-7 days average (CRITICAL)
  - Only 2 reviewers for 8 developers
  - Reviews happen in batches, not continuously
- Security scan: 45 minutes per PR (HIGH)
  - Runs serially, not parallel
  - Same scan runs on every commit, not just final
- Merge conflicts: 2 of 3 PRs have conflicts
  - Main branch has diverged significantly

### Recommendations
1. **Immediate:** Resolve merge conflicts on PRs #251, #253
2. **This week:** Add 2 more reviewers or implement AI pre-review
3. **This sprint:** Move security scan to run only on merge-ready PRs
4. **Consider:** Daily review slots instead of batch reviews
```

### Example 3: Manual Deployment

```
/ship

Need to deploy the firmware update to the test device. No CI for this.
```

**Output:**
```
## Ship Report

**Shipped:** Firmware v2.3.1
**Target:** Test device (ESP32)
**Path:** Local build -> USB flash -> Device verification

### Ship Actions Taken
1. Built firmware: `pio run -e esp32`
2. Connected device via USB
3. Flashed: `pio run -e esp32 -t upload`
4. Monitored boot: `pio device monitor`

### Verification
- [x] Flash completed without errors
- [x] Device booted successfully
- [x] Version shows 2.3.1 in status endpoint
- [x] New feature (power saving mode) responding

### Delivery-Path Tax Identified
- Manual USB connection required
- No OTA update path for test devices
- Build takes 2 minutes locally

### Recommendations
- Set up OTA updates for faster iteration
- Consider PR builds that produce flashable artifacts
```

## Session Persistence

When invoked with a session name (`/ship <session>`), this skill reads and writes to `.oh/<session>.md`.

**Reading:** Check for existing session file. Read **Aim** (what outcome we wanted), **Solution Space** (what approach we took), and **Execute** status.

**Writing:** After shipping, write the deployment status:

```markdown
## Ship
**Updated:** <timestamp>
**Status:** [staged | deployed | verified | rolled-back]

[shipping notes, verification results, etc.]
```

## Adaptive Enhancement

### Base Skill (prompt only)
Works anywhere. Produces ship checklist for manual execution. No persistence.

### With .oh/ session file
- Reads `.oh/<session>.md` for context on what was built and why
- Writes deployment status to the session file
- `/review` can check if shipping achieved the aim

### With CI/CD Configuration
- Reads pipeline definitions (GitHub Actions, CircleCI, etc.)
- References specific workflow files
- Triggers appropriate pipelines via labels or commands

### With Full Pipeline Integration (MCP tools)
- Directly triggers deployments
- Monitors pipeline progress in real-time
- Queries deployment status from infrastructure
- Session file serves as local cache for deployment state

## The Intent -> Execution -> Review Loop

Ship is part of the execution phase, but it has its own mini-loop:

1. **Intent:** Get this code to users
2. **Execute:** Run the deployment pipeline
3. **Review:** Verify the deployment worked

After shipping, the outer loop continues:
- `/review` - Did the shipped change achieve the aim?
- `/salvage` - If shipping revealed problems, capture learnings
- Back to `/aim` - What's the next outcome to pursue?

## Key Vocabulary

- **Delivery Path:** The journey from merged code to working install
- **Delivery-Path Tax:** Friction that slows delivery (review time, merge time, gate time, approval time)
- **Working Install:** The code is running and users can interact with it

---

**Remember:** Code that isn't shipped isn't delivering value. When execution is cheap, delivery is the bottleneck. Optimize the path, reduce the tax, get changes to users.
