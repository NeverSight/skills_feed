---
name: collaboration
description: Guide for collaborating on code in open source projects. This skill should be used when contributing to public repositories, creating PRs, reviewing code, or managing issues on GitHub.
license: MIT
---

# Collaboration

This skill documents how to collaborate on code in open source projects on GitHub.

## Working on Open Source Projects

When contributing to public repositories:

1. Create a fork under your own GitHub user account
2. Work exclusively on the fork, not the original repository
3. The fork is your workspace for all development

## Making Changes

To submit changes to a project:

1. Create a new branch on your fork (never commit directly to main)
2. Make commits on this branch as work progresses
3. When ready, create a PR from your fork's branch towards the original repository's main branch

## Code Reviews

When asked to review code:

1. Do the review directly on the GitHub PR
2. Add comments inline in the code where they make sense
3. Use general PR comments only for overarching feedback

## Addressing Review Comments

When responding to review feedback:

1. Address comments on GitHub, not just in code
2. Reply to each comment explaining what was changed or why something was kept
3. Mark conversations as resolved when the feedback has been addressed

## After PR is Merged

Once a PR has been merged:

1. Switch back to the main branch on your fork
2. Pull from origin to sync with the merged changes

## Issues

Always create GitHub issues on the original repository, never on the fork. The fork is only for development work.
