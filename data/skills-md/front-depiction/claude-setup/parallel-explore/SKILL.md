---
name: parallel-explore
description: Parallel exploration of codebase questions by decomposing into independent tracks. Use when exploring architecture, understanding systems, or investigating complex questions that benefit from multiple perspectives.
---

<exploration>
<philosophy>
exploration := decompose(question) → parallel(tracks) → aggregate(findings)
track       := independent ∧ parallelizable ∧ logical-unit
agent       := explorer(track) → findings(structured)
synthesis   := merge(findings) → coherent(answer)
</philosophy>

<decomposition>
analyze :: Question → [Track]
analyze question = do
  dimensions  ← identify (orthogonal (aspects question))
  granularity ← ensure (|dimensions| >= 3 ∧ |dimensions| <= 6)
  tracks      ← map toTrack dimensions
  verify      (independent tracks)
  pure tracks

-- each track explores one dimension without overlap
-- tracks are logical units of investigation
-- minimum 3 tracks to ensure sufficient coverage
</decomposition>

<track>
data Track = Track
  { name        :: String         -- short identifier
  , focus       :: Scope          -- what to investigate
  , approach    :: Strategy       -- how to investigate
  , gates       :: [Gate]         -- verification checkpoints
  , deliverable :: Artifact       -- what to return
  }

data Gate = Gate
  { checkpoint  :: Condition      -- what must be true
  , verification :: Command       -- how to verify
  }

-- each track subdivides into gated steps
-- step N must pass gate before step N+1
</track>

<when-to-use>
trigger :: Question → Bool
trigger question
  | complex (architecture question)     = True
  | multiple (dimensions question)      = True
  | benefits (parallelPerspectives)     = True
  | investigating (multiCauseBug)       = True
  | researching (crossCuttingPatterns)  = True
  | otherwise                           = False
</when-to-use>

<phases>
<phase name="decomposition">
decompose :: Question → Effect [Track]
decompose question = do
  aspects ← identify (dimensions question)
  tracks  ← traverse toTrack aspects
  verify  (all independent tracks)
  pure tracks
</phase>

<phase name="dispatch">
dispatch :: [Track] → Effect [Agent]
dispatch tracks = parallel $ fmap spawnExplorer tracks

spawnExplorer :: Track → Effect Agent
spawnExplorer track = spawn Explore (prompt track)
</phase>

<phase name="aggregate">
aggregate :: [TrackFindings] → Synthesis
aggregate findings = do
  common    ← intersect (conclusions findings)
  divergent ← difference (conclusions findings)
  gaps      ← union (uncertainties findings)
  confidence ← assess divergent
  pure $ Synthesis { common, divergent, gaps, confidence }
</phase>
</phases>

<module-specialists>
-- ADDITION to parallel tracks, not replacement
-- When complex modules detected → spawn module specialists in parallel with tracks
-- Targets BOTH Effect library modules AND internal codebase modules

detect :: Code → [Module]
detect code = filter isComplex (modulesUsed code)

isComplex :: Module → Bool
isComplex m = isEffectModule m ∨ isCodebaseModule m

isEffectModule :: Module → Bool
isEffectModule m = m ∈ { Stream, Layer, Fiber, Scope, Schema, Effect.gen, Match }

isCodebaseModule :: Module → Bool
isCodebaseModule m = m ∈ /modules        -- internal modules with ai-context.md

data ModuleSource = EffectLibrary | CodebaseInternal

moduleSource :: Module → ModuleSource
moduleSource m
  | isEffectModule m   = EffectLibrary
  | isCodebaseModule m = CodebaseInternal

spawn :: Module → Effect Specialist
spawn m = do
  context ← case moduleSource m of
    EffectLibrary    → /module m         -- external Effect documentation
    CodebaseInternal → /module path      -- internal ai-context.md
  scope   ← extractUsage m code          -- ONLY how m is used
  pure $ Specialist
    { context    := context              -- module documentation only
    , scope      := scope                -- usage patterns in code
    , goal       := efficiency           -- missed conveniences, anti-patterns
    , constraint := reviewOnly           -- no implementation, just review
    }

<specialist-prompt>
You are a [MODULE] specialist.

Your ONLY context: the /module [MODULE] documentation
Your ONLY scope: how [MODULE] is used in the provided code
Your ONLY goal: identify efficiency issues

Review for:
- Missed conveniences (simpler APIs available)
- Anti-patterns (common misuse)
- Idiomatic alternatives (more Effect-like approaches)

Output:
- Specific file:line citations
- What could be improved
- How to improve it (idiomatic pattern)

Do NOT:
- Implement changes
- Review anything outside [MODULE] usage
- Consider broader architecture
</specialist-prompt>

<composition>
explore :: Question → Code → Effect Synthesis
explore question code = do
  -- Regular parallel tracks (existing behavior)
  tracks     ← decompose question
  trackAgents ← dispatch tracks

  -- ADDITION: module specialists (orthogonal overlay)
  modules    ← detect code
  specialists ← parallel (spawn <$> modules)

  -- Aggregate both
  trackFindings      ← await trackAgents
  specialistFindings ← await specialists

  aggregate (trackFindings ++ specialistFindings)
</composition>
</module-specialists>

<agent-prompt>
<execution>
execute :: Track → Effect Findings
execute track = do
  context  ← gatherContext track
  gate₁    ← verify (understood context)
  findings ← explore context track
  gate₂    ← verify (evidence findings)
  summary  ← synthesize findings
  gate₃    ← verify (complete summary)
  pure summary
</execution>

<gates>
gate :: Checkpoint → Effect ()
gate = \case
  Understood ctx → can describe files/patterns found
  Evidence fnd   → every claim has file:line citation
  Complete sum   → summary answers track question
</gates>

<output>
data TrackFindings = TrackFindings
  { track       :: String
  , findings    :: [(Finding, Citation)]
  , evidence    :: [(FilePath, LineNumber, Description)]
  , conclusions :: Text
  , gaps        :: [Uncertainty]
  }
</output>
</agent-prompt>

<synthesis>
<output>
data Synthesis = Synthesis
  { unified       :: Text
  , nuances       :: [Divergence]
  , openQuestions :: [Gap]
  , confidence    :: Confidence
  }

data Confidence = High | Moderate | Low
</output>
</synthesis>

<recursive>
deepen :: Track → Effect Synthesis
deepen track = do
  subtracks ← decompose (question track)
  agents    ← dispatch subtracks
  findings  ← await agents
  aggregate findings

-- apply same decomposition recursively for deeper exploration
</recursive>
</exploration>
