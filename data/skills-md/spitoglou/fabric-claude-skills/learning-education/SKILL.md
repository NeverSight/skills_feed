---
name: learning-education
description: Create learning materials, explain concepts, generate quizzes and study aids. Use when asked to explain topics, create tutorials, generate practice questions, make flashcards, design curricula, or help study. Triggers include "explain this", "help me learn", "create a quiz", "tutorial for", "study guide", "how does X work", "teach me", "practice questions".
---

# Learning Education

Create effective learning experiences and study materials.

## Pattern Selection

| Intent | Pattern | When to Use |
|--------|---------|-------------|
| Concept explanation | `explain_terms` | Define and clarify terminology |
| Math explanation | `explain_math` | Step-by-step math concepts |
| Code explanation | `explain_code` | Code walkthroughs |
| Doc simplification | `explain_docs` | Make docs accessible |
| Narrative learning | `create_story_explanation` | Concept → engaging story |
| Coding basics | `coding_master` | Programming for beginners |
| Quiz creation | `create_quiz` | Practice questions by level |
| Flashcards | `create_flash_cards` | Q&A study cards |
| Reading plan | `create_reading_plan` | Structured learning path |
| DIY tutorial | `create_diy` | Step-by-step how-to |
| Evaluate learning | `analyze_answers` | Student response feedback |
| Lecture summary | `summarize_lecture` | Lecture key takeaways |
| Socratic method | `dialog_with_socrates` | Learn through questioning |
| Interview prep | `answer_interview_question` | Technical interview help |

## Decision Flow

```
User request
    │
    ├─ "explain/what is" ─┬─ code? ──→ explain_code
    │                     ├─ math? ──→ explain_math
    │                     ├─ terms/definitions? ──→ explain_terms
    │                     └─ general concept? ──→ create_story_explanation
    │
    ├─ "create study materials" ─┬─ quiz/test? ──→ create_quiz
    │                            ├─ flashcards? ──→ create_flash_cards
    │                            └─ reading plan? ──→ create_reading_plan
    │
    ├─ "tutorial/how-to" ──→ create_diy
    │
    └─ "help me understand" ──→ dialog_with_socrates
```

## Pattern References

See `references/` for full patterns:
- [explain_terms.md](references/explain_terms.md)
- [explain_math.md](references/explain_math.md)
- [create_story_explanation.md](references/create_story_explanation.md)
- [create_quiz.md](references/create_quiz.md)
- [create_flash_cards.md](references/create_flash_cards.md)
- [create_reading_plan.md](references/create_reading_plan.md)
- [dialog_with_socrates.md](references/dialog_with_socrates.md)

## Output Guidelines

- Match complexity to learner level (ask if unsure)
- Use concrete examples before abstract principles
- Build on prior knowledge
- Include practice opportunities
- Provide immediate feedback on exercises
- Use analogies from familiar domains

## Chaining Suggestions

- After `explain_terms` → offer `create_quiz` to test understanding
- After `create_reading_plan` → offer to explain first topic
- After `create_quiz` → offer `analyze_answers` for submitted responses
