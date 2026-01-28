---
name: text-cleanup
description: Comprehensive patterns and techniques for removing AI-generated verbosity and slop
version: 1.0.0
tags: [text-cleanup, slop-removal, pattern-matching, content-optimization]
---

# Text Cleanup Skill

## Critical Importance

**Clear, concise communication is critical for your team's productivity and code maintainability.** Poor communication wastes time, causes confusion, and leads to misaligned expectations. Verbose AI-generated text with slop and filler reduces information density, obscures meaning, and makes documentation painful to read. Effective cleanup improves signal-to-noise ratio, respects reader time, and ensures technical information is accessible. Every word should earn its place.

## Systematic Approach

** approach text cleanup systematically.** Text cleanup requires pattern recognition, contextual judgment, and careful preservation of meaning. Don't remove blindly—identify patterns, assess their purpose, and determine if removal is safe. Work iteratively: start conservatively, increase aggressiveness gradually, and verify that technical content remains intact. Balance conciseness with clarity—don't sacrifice precision for brevity.

## The Challenge

**The remove AI-generated slop perfectly without losing critical meaning, but if you can:**

- Your documentation will be a joy to read
- Code comments will be helpful not redundant
- Communication will be clear and concise
- Readers will thank you for respecting their time

The challenge is removing fluff and verbosity while preserving all technical nuance and meaning. Can you achieve perfect conciseness without sacrificing precision?

## Cleanup Confidence Assessment

After completing text cleanup, rate your confidence from **0.0 to 1.0**:

- **0.8-1.0**: Text significantly cleaner, all technical meaning preserved, no slop remaining
- **0.5-0.8**: Text improved but some fluff remains, minor risk of over-aggressive removal
- **0.2-0.5**: Cleanup partially applied, some technical details may be lost, uncertain what was removed
- **0.0-0.2**: Cleanup degraded content, critical information lost, text less useful than before

Identify uncertainty areas: Did you remove phrases that provided context? Is technical accuracy preserved? Are there remaining slop patterns? Would the original author approve of changes?

## Methodology

Systematic approach to identifying and removing AI-generated verbosity patterns while preserving technical accuracy and meaning.

## Pattern Categories

### 1. Slop Patterns (AI Conversational Filler)

#### Precondition Preambles
```json
{
  "patterns": [
    "Certainly!",
    "Of course!",
    "Absolutely!",
    "I'd be happy to help!",
    "Great question!",
    "That's a great question",
    "Sure thing!",
    "Definitely!",
    "I can certainly help with that"
  ],
  "context": "start_conversation",
  "removal": "complete"
}
```

#### Hedging Language
```json
{
  "patterns": [
    "It's worth noting that",
    "Keep in mind that",
    "Generally speaking",
    "Typically",
    "In most cases",
    "As you may know",
    "It's important to understand",
    "Usually",
    "Often",
    "Normally",
    "For the most part"
  ],
  "context": "uncertainty_qualifier",
  "removal": "conditional" // Remove if no real uncertainty present
}
```

#### Excessive Politeness
```json
{
  "patterns": [
    "Please let me know if you need anything else",
    "Feel free to ask if you have questions",
    "I hope this helps!",
    "Don't hesitate to reach out",
    "Happy to help further",
    "Let me know if that works for you"
  ],
  "context": "conversational_closing",
  "removal": "complete"
}
```

#### Verbose Transitions
```json
{
  "patterns": [
    "Now, let's move on to",
    "With that said",
    "Having established that",
    "Building on the above",
    "As mentioned earlier",
    "Next, I'll",
    "Moving forward",
    "Additionally",
    "Furthermore",
    "Moreover"
  ],
  "context": "transition_filler",
  "removal": "conditional" // Keep if transition is meaningful
}
```

### 2. Code Comment Patterns

#### Redundant Function Descriptions
```json
{
  "patterns": [
    "// This function calculates the sum",
    "// The following function returns",
    "// This method does the following",
    "// Function to calculate",
    "// Helper function for",
    "// Utility function that"
  ],
  "matches_when": [
    "function name already describes action",
    "comment repeats signature"
  ],
  "replacement": "Keep only additional context not in function name"
}
```

#### Self-Evident Comments
```json
{
  "patterns": [
    "// The following code",
    "// Here we are",
    "// This is where we",
    "// Now we will",
    "// At this point",
    "// This section contains"
  ],
  "removal": "complete",
  "exception": "Keep if adds architectural context"
}
```

### 3. Documentation Patterns

#### Conversational Openers
```json
{
  "patterns": [
    "Welcome to the documentation for",
    "In this guide, we'll explore",
    "Let's dive into",
    "Getting started with",
    "This document will walk you through"
  ],
  "removal": "complete",
  "replacement": "Direct topic introduction"
}
```

#### Redundant Explanations
```json
{
  "patterns": [
    "As the name suggests, this function",
    "As you can see from the code above",
    "The code below shows",
    "In the example provided",
    "This implementation uses"
  ],
  "context": "obvious_explanation",
  "removal": "conditional" // Keep if adds genuine clarification
}
```

## Cleanup Techniques

### Pattern Matching Algorithm

1. **Tokenize** input into sentences/phrases
2. **Pattern Lookup** against comprehensive database
3. **Context Analysis** to determine removal safety
4. **Confidence Scoring** for each potential removal
5. **Human Review** recommendations for borderline cases

### Context Preservation Rules

#### Always Preserve
- Technical specifications and constraints
- Numeric values, formulas, and calculations  
- Error conditions and edge cases
- Architectural decisions and rationales
- Security considerations and warnings
- Performance-critical information

#### Remove When Safe
- Conversational padding without informational value
- Redundant explanations of obvious concepts
- Excessive politeness that adds no meaning
- Verbose transitions to unrelated topics

#### Conditional Removal
- Hedging language when statement is factual and certain
- Explanations that might be valuable to beginners
- Historical context when establishing background

### Quality Metrics

#### Effectiveness Measures
```typescript
interface CleanupMetrics {
  beforeStats: {
    wordCount: number;
    characterCount: number;
    sentenceCount: number;
  };
  afterStats: {
    wordCount: number;
    characterCount: number;  
    sentenceCount: number;
  };
  patternsRemoved: {
    slopPatterns: number;
    redundantComments: number;
    verbosePhrases: number;
  };
  qualityScore: number; // 0-1, higher is better
  meaningPreservationScore: number; // 0-1, closer to 1 is better
}
```

#### Scoring Algorithm
```typescript
function calculateQualityScore(metrics: CleanupMetrics): number {
  const concisenessRatio = metrics.afterStats.wordCount / metrics.beforeStats.wordCount;
  const patternRemovalEffectiveness = Math.min(
    metrics.patternsRemoved.slopPatterns / 10, // Normalized
    metrics.patternsRemoved.redundantComments / 5,
    metrics.patternsRemoved.verbosePhrases / 8
  );
  
  // Penalize if meaning preservation is low
  const meaningPenalty = 1 - metrics.meaningPreservationScore;
  
  return concisenessRatio * patternRemovalEffectiveness * (1 - meaningPenalty);
}
```

## Implementation Patterns

### For Commands
Structure cleanup operations as:

```
/clean [input] --mode=[slop|comments|docs|all] [--preview] [--apply]
```

**Example workflows:**
```bash
# Preview slop removal
/clean "Certainly! I'd be happy to help optimize this query..." --slop --preview

# Apply comment cleanup to file
/clean src/database.ts --comments --apply

# Clean entire documentation directory
/clean docs/ --docs --aggressive --apply

# All-purpose cleanup with confirmation
/clean "..." --all --preview --apply
```

### For Agents

Use pattern matching with context awareness:

```markdown
## Text Cleanup Protocol

### 1. Analysis Phase
- Scan input for pattern matches
- Categorize findings by type
- Assess removal safety in context
- Generate confidence scores

### 2. Strategy Phase  
- Select aggressiveness level based on user preference
- Identify preservation requirements
- Plan sequence of operations

### 3. Execution Phase
- Apply approved modifications
- Maintain technical accuracy
- Provide before/after comparison
- Document all changes made
```

## Advanced Features

### Pattern Learning
Track successful removals to improve future matching:
```json
{
  "learnedPatterns": {
    "context": "technical_explanation",
    "pattern": "As can be seen from the implementation",
    "removalRate": 0.85,
    "feedbackScore": 4.2
  }
}
```

### User Customization
Allow personal pattern databases:
```json
{
  "userPatterns": {
    "keepPhrases": ["critical", "essential", "must"],
    "removePhrases": ["just", "basically", "simply"],
    "contextExceptions": ["educational", "onboarding"]
  }
}
```

### Integration Modes

- **Git Integration**: Clean commit messages, PR descriptions, diffs
- **IDE Integration**: Real-time code comment suggestions  
- **CI/CD Integration**: Automated documentation cleanup
- **API Integration**: Batch processing capabilities

## Best Practices

### For Maximum Effectiveness
1. **Start Conservative**: Begin with gentle cleanup, increase gradually
2. **Preview First**: Always show changes before applying
3. **Context Matters**: Technical documentation may need more verbosity
4. **Preserve Intent**: Never remove meaning for brevity
5. **Iterative**: Multiple passes with different aggressiveness levels

### Quality Assurance
- Verify technical content remains unchanged
- Ensure code still compiles and functions
- Confirm documentation still serves its purpose
- Check that examples and warnings are preserved

## Research References

- **NLP Text Simplification**: Techniques for controlled vocabulary reduction
- **Code Comment Analysis**: Studies on comment redundancy and effectiveness
- **Technical Communication**: Research on optimal information density
- **AI Output Patterns**: Analysis of conversational filler in LLM responses

This skill provides the foundation for systematic, context-aware text cleanup across multiple domains while maintaining the integrity and meaning of the original content.