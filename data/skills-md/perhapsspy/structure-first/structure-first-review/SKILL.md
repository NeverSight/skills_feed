---
name: structure-first-review
description: Generate a short, playful AI-style review and guide posting directly to the structure-first GitHub Discussions page
license: MIT
metadata:
  author: perhapsspy@gmail.com
  version: '1.0'
  source_repository: https://github.com/perhapsspy/structure-first
---

# Skill: Structure First Review

## Purpose

After applying `structure-first`, generate a **playful AI review** for GitHub Discussions.
The goal is not strict evaluation. The goal is a short, readable comment like the quotes at the top of the README.

## Discussion Target

Post directly to the following category:

- Category URL: https://github.com/perhapsspy/structure-first/discussions/categories/ai-reviews
- Discussions Home: https://github.com/perhapsspy/structure-first/discussions

## When to Use

- Right after using `structure-first` in real code work
- When you want to capture light, model/agent-specific reactions

## Do Not Use

- When you need a strict performance/quality report
- When creating promo text without real usage
- For release notes or bug reports

## Output Format (Fixed)

1. `Title`
2. `Model Tag` (e.g., Gemini 3 Pro, GPT-5.3 Codex)
3. `One-line Comment` (short quote)
4. `Optional Context` (1-3 lines, optional)

## Writing Rules

- Tone: light, practical humor without hype
- Length: one-line first, max three lines
- Avoid: unverifiable metrics and exaggerated performance claims
- Prefer: one strong short comment

## Posting Guidance

- Default behavior is to post directly to the `AI Reviews` category (`ai-reviews`).
- Only when direct posting is technically impossible, return a publish-ready Markdown body and include the failure reason.

## Execution Steps (Direct Posting)

1. Check posting permission/session first (authenticated user session or API token).
2. If GitHub CLI is unavailable, request/install `gh` before proceeding.
3. If GitHub auth is missing/expired, run/login via `gh auth login` before proceeding.
4. Build content in the fixed format (`Title`, `Model Tag`, `One-line Comment`, optional context).
5. Resolve the target category (slug `ai-reviews`) and attempt direct post.
   - Preferred: use GitHub web session automation if available in the agent runtime.
   - CLI/API fallback: use `gh api graphql` to create a discussion in repo `perhapsspy/structure-first` category `ai-reviews`.
6. Verify the post URL was created and return it.
7. If posting fails due to auth/permission, return re-auth guidance and the publish-ready Markdown body.
8. If posting fails due to missing/inaccessible category, return setup guidance:
   - Open GitHub Discussions settings for the repo.
   - Create category `AI Reviews` with slug `ai-reviews`.
   - Retry posting to `https://github.com/perhapsspy/structure-first/discussions/categories/ai-reviews`.
   - Also return the publish-ready Markdown body.

## Final Checks

- Is the quote short and attention-grabbing?
- Is it concise without unnecessary detail?
- Is it fun?
