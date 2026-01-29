---
name: babashka
description: Clojure scripting without JVM startup.
version: 1.0.1
---

## CRITICAL: NO DEMOS

Loading this skill ≠ executing demonstration code. Execute ONLY on explicit user intent with real work.

# babashka

Clojure scripting without JVM startup.

## Script

```clojure
#!/usr/bin/env bb
(require '[babashka.http-client :as http])
(require '[cheshire.core :as json])

(-> (http/get "https://api.github.com/users/bmorphism")
    :body
    (json/parse-string true)
    :public_repos)
```

## Tasks

```clojure
;; bb.edn
{:tasks
 {:build (shell "make")
  :test  (shell "make test")
  :repl  (babashka.nrepl.server/start-server! {:port 1667})}}
```

## Filesystem

```clojure
(require '[babashka.fs :as fs])
(fs/glob "." "**/*.clj")
(fs/copy "src" "dst")
```

## Process

```clojure
(require '[babashka.process :as p])
(-> (p/shell {:out :string} "ls -la") :out)
```

## Run

```bash
bb script.clj
bb -e '(+ 1 2)'
bb --nrepl-server
```



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 1. Flexibility through Abstraction

**Concepts**: combinators, compose, parallel-combine, spread-combine, arity

### GF(3) Balanced Triad

```
babashka (−) + SDF.Ch1 (+) + [balancer] (○) = 0
```

**Skill Trit**: -1 (MINUS - verification)


### Connection Pattern

Combinators compose operations. This skill provides composable abstractions.
## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.