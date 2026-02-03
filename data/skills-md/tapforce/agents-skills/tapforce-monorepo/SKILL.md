---
name: tapforce-monorepo
description: Practices use Moon Repo tools to manage mono-repo project in Tapforce
---

# tapforce-monorepo

Provide good way and practices to manage and develop mono-repo projects in Tapforce company. This skill prefer use `Moon Repo` as main monorepo management tool.

Information about tool can be found in [Moon Repo documentation](https://moonrepo.dev/docs/install).

## When to use

Use this skill when project mention or related to Tapforce, and required by user or you think project complex enough to use monorepo structure.

## Instructions

Skill separated to rules under `./rules` with prefix, following priority:

| Priority | Rule    | prefix | Description                                             |
| -------- | ------- | ------ | ------------------------------------------------------- |
| 1        | prepare | `pr`   | Steps and practices to prepare project to use moonrepo. |
| 2        | policy  | `pl`   | Practices to follow when use moonrepo.                  |

Each rules have own name, description, and tags.
Rule can include **Incorrect**, **Correct**, or **Example** code block.

Full version of skill and rules represent with file AGENTS.md.

## Reference

- [Moon repo documentation](https://moonrepo.dev/docs/install)
- [Concerpts](https://moonrepo.dev/docs/concepts)
