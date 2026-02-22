---
name: es-toolkit
description: Up-to-date es-toolkit documentation reference. Use when writing JavaScript/TypeScript code – writing new utility helpers, working with arrays/objects/Maps/Sets/Promises/math/string manipulation, refactoring code, reviewing code, evaluating whether a custom utility can be replaced with es-toolkit, or when explicitly asked to scan/refactor code toward es-toolkit functions (for example, "Go through the codebase and find potential cases where es-toolkit could be used instead of custom implementations")
---

# es-toolkit

Run initialization first to sync references for the target project's installed `es-toolkit` version. If `package.json` is missing, does not include `es-toolkit`, or contains an unparsable `es-toolkit` range, initialization falls back to the latest `es-toolkit` release:

```sh
sh ./scripts/init.sh [/path/to/project/package.json]
```

Treat initialization as a hard prerequisite:

- Do not read any file under `references/` until `init.sh` exits with code `0`.
- Do not run initialization and reference reads in parallel.
- If initialization fails, stop and report the error instead of reading references.

When writing/refactoring/reviewing utility code, check the references first and prefer an existing `es-toolkit` function over custom implementations whenever behavior matches.

Do not use functions under `compat` ("Lodash compatibility").

## References (available once initialization is complete)

- [Array Utilities](references/array-utilities.md)
- [Function Utilities](references/function-utilities.md)
- [Map Utilities](references/map-utilities.md)
- [Math Utilities](references/math-utilities.md)
- [Object Utilities](references/object-utilities.md)
- [Predicates](references/predicates.md)
- [Promise Utilities](references/promise-utilities.md)
- [String Utilities](references/string-utilities.md)
- [Set Utilities](references/set-utilities.md)
- [Utility Functions](references/utility-functions.md)
- [Errors](references/errors.md)
