---
name: supabase-reset-test-gen-types
description: Run a local Supabase reset, database tests, and type generation in sequence. Use when the user asks to run `supabase db reset`, `supabase test db`, and `npm run gen-types` for this repo.
---

# Supabase Reset/Test/Gen Types

## Workflow

1. Confirm the working directory is the intended project root:
   - It contains `supabase/` configuration.
   - It contains a type-generation script (for example `npm run gen-types`).
2. Execute the one-shot command:

```bash
supabase db reset --yes && supabase test db && npm run gen-types
```

3. If the command succeeds, summarize:
   - database reset succeeded
   - database tests passed
   - types were generated
4. If any step fails, stop and report the failing command output clearly.

## Notes

- Use `--yes` to avoid prompts during `supabase db reset`.
- Use `supabase test db` (not `supabase db test`) for pgTAP tests.
- If local services are not running, start required Supabase services before retrying.
