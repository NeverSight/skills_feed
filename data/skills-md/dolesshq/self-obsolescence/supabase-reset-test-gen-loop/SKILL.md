---
name: supabase-reset-test-gen-loop
description: Iteratively run a local Supabase reset, database tests, and type generation until they succeed, fixing issues between runs. Use when asked to reset the local Supabase DB, run `supabase test db`, and regenerate types (`npm run gen-types`) in a loop.
---

# Supabase Reset / Test / Gen Loop

## Workflow

1. Confirm working directory contains the intended `supabase/` config and `package.json`.
2. Run the loop:
   - `supabase db reset && supabase test db && npm run gen-types`
3. If the command fails, read the error output, fix the underlying issue, and rerun the same command.
4. Continue until the command completes successfully.
5. If the same error repeats after fixes, pause and ask the user for guidance.

## Notes

- Use `supabase test db` (not `supabase db test`) for running pgTAP tests.
- If the project requires environment setup (e.g., `supabase start`), ensure it is running before the loop.
