---
name: code-comprehension-quiz
description: Test user understanding of code changes and explanations. Generates adaptive multiple-choice quizzes. Only triggers on explicit request - when user says "quiz me", "test my understanding", or "/quiz". Does NOT auto-trigger.
---

# Code Comprehension Quiz

Generate multiple-choice questions to test understanding of the work just completed.

## When to Trigger

**Only on explicit request.** Trigger when the user says:
- "quiz me"
- "test my understanding"
- "/quiz"
- "/code-comprehension-quiz"

**Do NOT auto-trigger.** Never quiz automatically after code changes, explanations, or debugging. Wait for the user to ask.

After completing one quiz, do NOT quiz again until the user explicitly requests another quiz.

## Quiz Generation

### Determine Question Count

| Complexity | Questions | Indicators |
|------------|-----------|------------|
| Low | 2 | Single file, one concept, small change |
| Medium | 3 | Multiple files, 2-3 concepts, moderate changes |
| High | 4-5 | Architectural changes, new patterns, complex debugging |

### Question Types (Ranked by Difficulty)

Prefer harder question types. Rotate through these:

1. **Tradeoff analysis** - "What's the downside of this approach?"
2. **Failure modes** - "When/how would this break?"
3. **Alternative reasoning** - "Why wasn't [other approach] used?"
4. **Implication chains** - "What else needs to change as a result?"
5. **Root cause** - "What was the underlying issue this solved?"
6. **Edge cases** - "What input would cause unexpected behavior?"

Avoid overusing:
- "What changed?" (too easy - they just saw it)
- "What pattern is this?" (often guessable)

### Question Construction Process

Follow this order:
1. Write the stem (question) first
2. Write the correct answer
3. Write 2-3 distractors that match the correct answer in length, grammar, and style
4. Ensure each question targets a different concept from the most recent work

### Stem Guidelines

- State a single, clear problem - avoid compound questions
- Include most information in the stem so options stay short
- Phrase as a question or incomplete statement
- Avoid negatives ("Which is NOT..."), passive voice, and absolutes (always, never)
- Keep vocabulary appropriate - no jargon the user hasn't seen in context
- Keep stems under 25 words unless clarity requires more

### Option Guidelines

- **3-4 options total** (not always 4 - use 3 when a 4th would be filler)
- **All options must be plausible** to someone who wasn't paying close attention
- **Match style**: If correct answer is 8 words, distractors should be ~8 words
- **Match grammar**: All options must complete the stem grammatically
- **One unambiguously correct answer** - avoid "most correct" situations
- **Avoid**: "All of the above", "None of the above", "Both A and B"
- **Avoid clues**: Don't let grammar, length, or specificity reveal the answer
- Keep options under 12 words unless clarity requires more

### Answer Position Randomization

For each question, randomly select the position (A/B/C/D) for the correct answer. Use this method:
- Take the question number, multiply by 7, mod by number of options
- This produces: Q1→position varies, Q2→different position, etc.
- Map the result to letters: 0->A, 1->B, 2->C, 3->D

Do NOT just cycle through A, B, C, D in order.

### Question Difficulty

**Avoid surface-level questions:**
- "What file was modified?"
- "What function was added?"
- "Which library was used?"

**Test deeper understanding:**
- Tradeoffs: "What's the main drawback of this approach?"
- Failure modes: "Under what condition would this fail?"
- Alternatives: "Why use X instead of Y here?"
- Implications: "What else might need updating as a result?"
- Root cause: "What underlying issue did this solve?"
- Edge cases: "What input would cause unexpected behavior?"

### Example Questions

After adding error handling to an async function:

```
Question: If the try-catch were removed and the API call failed, what would happen?

A) The function would return undefined silently
B) The application would crash immediately
C) The caller would receive a rejected promise
D) An error boundary would catch it automatically
```
(Correct: C)

After refactoring a component to use a custom hook:

```
Question: What tradeoff comes with extracting this logic into a custom hook?

A) Additional indirection makes the data flow harder to trace
B) The component now re-renders more frequently
C) State is now shared between all components using the hook
D) The hook cannot be tested independently
```
(Correct: A)

After fixing a race condition with useEffect cleanup:

```
Question: The cleanup function prevents the bug by:

A) Cancelling the HTTP request before it completes
B) Resetting the component state to initial values
C) Ignoring stale responses from superseded requests
D) Blocking concurrent effect executions
```
(Correct: C)

## Scoring and Review

After all questions answered:

1. **Show score**: "You got X/N correct"
   - Treat skipped or unanswered questions as incorrect and mark them as "skipped" in the review

2. **Review each question**:
   - Show the question and user's answer
   - Mark correct (checkmark) or incorrect (X)
   - For ALL answers, explain WHY the correct answer is correct
   - For wrong answers, explain the misconception

3. **Offer recap or deeper dive**: Ask whether the user wants a short recap or a deeper dive. If score < 80%, recommend a deeper dive.

### Review Format

```
## Quiz Results: X/N

### Question 1: [Correct/Incorrect]
Your answer: B
Correct answer: A

**Explanation**: [2-3 sentences on why A is correct and what makes B incorrect]

---

[Repeat for each question]

---

**Areas to review**: [List concepts from missed questions]
Would you like me to explain any of these concepts further?
```

## Implementation Notes

- Use AskQuestion tool for each question individually, even if batching is supported
- Wait for user response before showing next question
- Track answers internally to provide review at end
- Keep questions focused on the MOST RECENT work, not general knowledge
- Questions should be answerable from the conversation context alone
- If the user does not answer, mark the question as skipped and continue
- After completing a quiz, do NOT start another quiz until explicitly requested
- Never auto-trigger on subsequent turns - only trigger on explicit commands like "/quiz"
