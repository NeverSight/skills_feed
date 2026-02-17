---
name: canvas-component-upload
description:
  Upload validated components to Drupal Canvas and recover from common upload
  failures. Use after component work is complete and validated. Handles upload
  failures including dependency-related issues that require retry.
---

## Upload to Canvas

Before uploading, confirm the user has Drupal Canvas CLI installed and
configured for their target site.

### Setup gate (ask first)

Ask the user whether `@drupal-canvas/cli` is already installed and authenticated
for the project/site they want to upload to.

- If **yes**, proceed with upload commands below.
- If **no** (or they are unsure), **do not guess setup steps**. Point them to
  the official docs and ask them to complete setup first:
  - Drupal Canvas OAuth module setup:
    <https://git.drupalcode.org/project/canvas/-/tree/1.x/modules/canvas_oauth#2-setup>
  - Drupal Canvas CLI package/docs:
    <https://www.npmjs.com/package/@drupal-canvas/cli>

After they confirm setup is complete, continue with upload.

## Run upload

When component work is complete and validated, ask the user if they would like
to upload the modified components to Canvas. Make sure to use the right package
manager. For example, if using npm, run the following command:

```bash
npx canvas upload -c component1,component2,component3 -y
```

Replace `component1,component2,component3` with the actual component names that
were created or modified (e.g., `canvas upload -c button,card,hero`).

## Handling upload failures

**Always retry failed uploads.** Uploads can fail for various transient reasons
(network issues, timeouts, server load). When an upload fails, retry the same
command—it will often succeed on a subsequent attempt.

### Dependency-related failures

When uploading multiple new components where one component depends on another
(e.g., `hero` imports `heading`), the upload may fail with a message indicating
that a component doesn't exist. This happens when a component that includes
another gets uploaded before its dependency.

**This is expected behavior.** Simply retry the upload command. On subsequent
attempts, the dependencies that were successfully uploaded in the previous run
will already exist, allowing the dependent components to upload successfully.

Example scenario:

1. First upload attempt: `hero` fails because `heading` doesn't exist yet, but
   `heading` uploads successfully.
2. Second upload attempt: `hero` now succeeds because `heading` exists.

If uploads continue to fail after multiple retries, check that all dependency
components are included in the upload command.
