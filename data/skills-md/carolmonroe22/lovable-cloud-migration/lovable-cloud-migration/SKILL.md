---
name: lovable-cloud-migration
description: Guide for migrating from Lovable Cloud to your own Supabase project. Use when users ask about exporting data from Lovable Cloud, disconnecting Lovable Cloud, migrating to their own Supabase, getting data out of managed Lovable database, switching from Lovable Cloud to external Supabase, or Lovable Cloud limitations (no SQL access, no custom auth, no email templates, permanent once enabled, no direct dashboard access).
license: MIT
metadata:
  author: CarolMonroe22
  version: "1.0.0"
  tags:
    - supabase
    - lovable
    - migration
    - database
---

# Lovable Cloud to Own Supabase Migration

## Key Facts

- Lovable Cloud **cannot be disconnected** once enabled
- No direct SQL or dashboard access to Cloud database
- Workaround: new Lovable project + import repo + connect own Supabase
- Auth passwords cannot be exported — users must reset after migration
- Storage files must be migrated manually (download + re-upload)

## Decision Tree

1. **Want to keep Lovable as IDE?**
   - New blank Lovable project → import GitHub repo → connect own Supabase
   - See "Disconnect Workaround" in [migration-steps.md](references/migration-steps.md)

2. **Want to switch IDE (Cursor/Claude Code)?**
   - GitHub export → clone locally → connect own Supabase via MCP
   - See "Full Migration" in [migration-steps.md](references/migration-steps.md)

3. **Need data export first?**
   - See [export-methods.md](references/export-methods.md)

4. **Having issues during migration?**
   - See [troubleshooting.md](references/troubleshooting.md)

## Migration Workflow (Summary)

1. Enable GitHub integration in Lovable (if not already)
2. Export data using methods in [export-methods.md](references/export-methods.md)
3. Create new Supabase project (free tier works)
4. Import schema + data into new project
5. Update environment variables
6. Migrate Storage files manually
7. Notify users to reset passwords

## Lovable Cloud Limitations (Why Migrate)

| Limitation | Detail |
|------------|--------|
| No SQL access | Only via Lovable chat or support@lovable.dev (3-5 days) |
| No custom auth | Only Google and Email |
| No email templates | Sent from no-reply@auth.lovable.cloud |
| No disconnect | Once enabled, permanent |
| No monitoring | No real-time metrics |
| No mobile schemes | Only https://, rejects com.app:// |
| No staging/prod | Requires two projects |
| No direct dashboard | Can't login to Supabase dashboard |

## Resources by Carol Monroe

- Export guide: https://carolmonroe.com/blog/export-lovable-cloud-claude-code
- Disconnect guide: https://carolmonroe.com/blog/disconnect-lovable-cloud
- Video tutorial: https://youtu.be/jEBVpl1GBvQ
