---
name: forge-memory
description: >
  FORGE Vector Memory — Diagnostic tool for the vector memory index.
  Operations: sync, search, status, reset, log, consolidate.
  Usage: /forge-memory sync | /forge-memory search "query" | /forge-memory status | /forge-memory log "message" | /forge-memory consolidate
---

# /forge-memory — FORGE Vector Memory

Outil de diagnostic pour l'index vectoriel de la mémoire FORGE.
Les commandes FORGE utilisent automatiquement la recherche vectorielle ; ce skill est pour le diagnostic et la maintenance.

## French Language Rule

All content generated in French MUST use proper accents (é, è, ê, à, ù, ç, ô, î, etc.), follow French grammar rules (agreements, conjugations), and use correct spelling.

## Prérequis

Le système doit être installé :
```bash
bash ~/.claude/skills/forge/scripts/forge-memory/setup.sh
```

## Commandes

### Synchroniser l'index

Synchronise les fichiers Markdown vers la base SQLite :

```bash
forge-memory sync [--force] [--verbose]
```

- Sans `--force` : réindexe uniquement les fichiers modifiés (basé sur le hash SHA-256)
- Avec `--force` : réindexe tous les fichiers
- Avec `--verbose` : affiche le détail de chaque fichier traité

### Rechercher

Recherche hybride (vectorielle + texte) dans la mémoire :

```bash
forge-memory search "query" [--namespace all|project|session|agent] [--agent NAME] [--limit 5] [--threshold 0.3] [--pretty]
```

- `--namespace` : filtrer par type (project = MEMORY.md, session = logs, agent = mémoires d'agent)
- `--agent` : filtrer par nom d'agent (pm, architect, dev, qa)
- `--limit` : nombre max de résultats (défaut: 5)
- `--threshold` : score minimum (défaut: 0.3)
- `--pretty` : affichage formaté (sinon JSON)

### Statut

Affiche les statistiques de l'index :

```bash
forge-memory status [--json]
```

### Journaliser

Ajoute une entrée dans le fichier session du jour (`.forge/memory/sessions/YYYY-MM-DD.md`) :

```bash
forge-memory log "message" [--agent NAME] [--story STORY-ID]
```

- `--agent` : nom de l'agent (dev, qa, lead, etc.)
- `--story` : identifiant de la story (STORY-001, etc.)
- Crée le répertoire `sessions/` et le fichier avec header automatiquement

### Consolider

Agrège les entrées des session logs dans MEMORY.md, groupées par story :

```bash
forge-memory consolidate [--verbose]
```

- Lit les sessions depuis la dernière consolidation (marqueur `### Consolidation — YYYY-MM-DD`)
- Ajoute une section récapitulative à la fin de MEMORY.md
- Pure Python, aucune dépendance LLM

### Réinitialiser

Supprime et recrée la base de données :

```bash
forge-memory reset --confirm
```

## Architecture

```
.forge/memory/
  MEMORY.md              <- source de vérité (écrit par les agents)
  sessions/YYYY-MM-DD.md <- source de vérité (écrit par les agents)
  agents/{agent}.md      <- source de vérité (écrit par les agents)
  index.sqlite           <- index dérivé (synchronisé depuis les .md)
```

- Synchronisation unidirectionnelle : Markdown -> SQLite
- Scope de sync élargi : `.forge/memory/` + `docs/` (stories, architecture, PRD)
- Auto-sync avant chaque recherche (vérifie les changements dans les deux répertoires)
- Recherche hybride : similarité vectorielle (70%) + FTS5 BM25 (30%)
- Embeddings locaux : sentence-transformers all-MiniLM-L6-v2 (384 dimensions)
- Chunking markdown-aware : ~400 tokens/chunk, 80 tokens overlap
