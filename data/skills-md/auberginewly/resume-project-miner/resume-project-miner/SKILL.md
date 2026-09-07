---
name: resume-project-miner
description: Use when mining a local or GitHub Git repository for evidence-backed Chinese resume project bullets, project background or responsibility summaries, role or JD adaptation, STAR evidence, interview preparation, project comparison, contribution attribution, or authenticity auditing.
---

# Resume Project Miner

Mine claims from evidence, not repository marketing. Keep every repository operation read-only and every final claim traceable.

## Required references

Read all three before analysis:

- `references/evidence_rules.md` for attribution, grading, privacy, and claim gates.
- `references/role_profiles.md` for role/JD selection and ranking.
- `references/resume_writing_rules.md` for bullets, STAR material, interview content, and output schema.

## Workflow

1. Normalize the source: current repository, local path, `owner/repo`, or GitHub URL. Accept an optional branch, tag, commit, PR, `--since`, or `--until`. Resolve a requested PR with read-only `gh pr view`/`gh api` metadata and fetch refs only into a temporary bare repository; never check out into the user's working tree.
2. For any remote source, run `gh auth status` first. Prefer authenticated `gh` access for public and private repositories. Never request or persist a token. If authentication or access fails, report the exact boundary and continue only with accessible evidence.
3. Establish identity once from Git config, `gh api user`, commit authors, PR authors, reviews, issues, and user-supplied aliases. If identity is not unique, finish repository discovery, then ask one consolidated round of at most five questions.
4. Create a private temporary parent directory, choose a nonexistent or empty child path for evidence, and run:

   ```bash
   bash scripts/collect_repo_evidence.sh --source <source> --output <private-temp-dir> [--ref <ref>] [--since <date>] [--until <date>] [--author <identity>]...
   ```

   Repeat `--author` for each confirmed name, email, or login alias. Read `summary.md`, `manifest.tsv`, `history.tsv`, `contributors.tsv`, `ownership.tsv`, and optional `github.json`. The collector inventories paths and metadata; selectively read only high-value source files afterward. Remove the temporary directory when the task ends.
5. Build a low-cost project profile, core technology stack, and product capability map before ranking technical highlights. Select only technologies that explain the architecture, primary runtime, core data or communication path, or the user's strongest implementation boundary; do not turn manifests into dependency lists. Inventory the current user-visible journey across core task, creation/output modes, history or saved state, configuration and onboarding, platform integration, and delivery or update surfaces. Mark each capability `current`, `removed`, `UI-only`, `dependency-only`, or `unverified`; only `current` capabilities may define the product today. Derive the positioning value from the complete journey and the alternative it improves, not from the hardest module alone.
6. Inspect high-value modules with `rg`, `git log`, `git show`, `git blame`, `git diff`, and read-only `gh api`/`gh pr view`/`gh issue view`/`gh release view`/`gh run view`; never use commands that comment, review, rerun, cancel, dispatch, edit, create, merge, close, or delete. Ignore dependencies, generated code, build products, binaries, secrets, and unrelated user files. Do not infer importance from line counts.
7. Separate five layers: product positioning and capability map; project facts; personal contribution and evidence; role/JD relevance; resume wording. Grade every candidate A/B/C/D before drafting. Never promote B or C to fact without confirmation; omit D. Keep audit caveats out of resume prose: translate supported work into completed capabilities and technical decisions, while reserving gaps, mocks, removed states, and overclaim warnings for the audit sections.
8. If a JD is provided, extract responsibilities, core technologies, bonus items, and business terms, then re-rank supported highlights. If no role is provided, produce a general technical version and recommend three directions with evidence-based reasons.
9. Ask at most one consolidated follow-up round after scanning. Include a compact presentation choice when useful: whether the final resume entry should add separate `项目背景` and/or `个人负责` blocks. Recommend which blocks earn their space from the evidence and target role; do not ask when the user already specified the structure or the entry is too small to benefit. For factual gaps, state why each answer matters, how to find it, and the conservative wording used if unanswered.
10. Before drafting, build the required coverage ledger defined in `references/resume_writing_rules.md`, including every product line, technical boundary, result theme, and presentation structure the user explicitly requested. Produce sections A-G exactly as defined there, then run the final coverage and prose audit: no required item may disappear silently, no unsupported metric or ownership may enter, and no audit/process wording may weaken an otherwise supported resume bullet. Redact private implementation details and personal emails; cite private evidence by safe path/commit/PR identifiers without reproducing source.

## Non-negotiable boundaries

- Keep the source repository unchanged: no checkout, branch, commit, push, Issue, PR, review, workflow trigger, or configuration write.
- Never expose `.env`, credentials, tokens, certificates, keys, proprietary source, or complete private-file contents. Do not print environment variables.
- Never invent scale, latency, accuracy, coverage, revenue, adoption, performance gains, or ownership. Calculate a number only from reproducible repository evidence and label its source and method.
- Distinguish dependency capability from the user's implementation and team outcome from individual contribution.
- Use `负责`, `主导`, `参与`, `协同完成`, or `独立实现` only at the strength allowed by the evidence rules.
