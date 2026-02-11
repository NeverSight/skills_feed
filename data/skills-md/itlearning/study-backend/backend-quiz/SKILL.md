---
name: backend-quiz
description: Adaptive Kotlin/Spring backend quiz with 5 questions. Difficulty adjusts based on your answers. Use when reviewing or testing your backend knowledge.
---

# backend-quiz - Kotlin/Spring Backend Quiz

Adaptive quiz and coding exercises for Kotlin/Spring backend.

## Instructions

Give a Kotlin/Spring backend quiz. Difficulty adjusts automatically based on the learner's level.

### Step 0: Language Selection

Ask the user to choose a language at the start using AskUserQuestion:

```
questions:
  - question: "Which language do you prefer? / 어떤 언어로 진행할까요?"
    header: "Language"
    options:
      - label: "한국어"
        description: "한국어로 퀴즈를 풉니다"
      - label: "English"
        description: "Take the quiz in English"
    multiSelect: false
```

Use the selected language for all communication. Code and Kotlin/Spring keywords stay in English.

### Step 1: Choose Quiz Topic

Ask in plain text:

**Korean:**
"어떤 주제로 퀴즈를 풀까요? 주제를 알려주세요. 뭘 할지 모르겠으면 '추천해줘'라고 해주세요."

**English:**
"What topic should the quiz cover? Tell me a topic, or say 'recommend' if you're not sure."

- If the user enters a topic: start the quiz on that topic.
- If the user says "recommend" / "추천해줘": check learning history (BackendLearningProgress in memory) and suggest 3-4 recently studied topics. Present choices via AskUserQuestion.

### Step 2: Run the Quiz (5 questions)

5 questions total. Track difficulty internally from 1-5 (start at 3).

- Correct answer -> difficulty +1
- Wrong answer -> difficulty -1

### Question Types

Each question uses one of the types below. **Default to open-ended, mix in others as appropriate.**

#### Type A: Predict Output (open-ended)
```
What does this code return? Explain your answer.

@Transactional
fun transfer(from: Long, to: Long, amount: Int) {
    val sender = accountRepository.findById(from).orElseThrow()
    val receiver = accountRepository.findById(to).orElseThrow()
    sender.balance -= amount
    receiver.balance += amount
}
// What happens if amount > sender.balance?
```
The user types their own answer.

#### Type B: Find the Bug (open-ended)
```
What's wrong with this code? Explain the issue.

@RestController
class UserController(private val userService: UserService) {
    @GetMapping("/users/{id}")
    fun getUser(@PathVariable id: Long): User {
        return userService.findById(id)  // returns null if not found
    }
}
```
The user types their own answer.

#### Type C: Concept Question (multiple-choice allowed)
```
What is the default propagation level of @Transactional in Spring?
```
Present 4 choices via AskUserQuestion. Multiple-choice is fine for concept checks.

#### Type D: Write Code (difficulty 4+ only)
```
Write a REST endpoint that meets these requirements:

- POST /api/users
- Accepts a JSON body with name (String) and email (String)
- Validates that email contains '@'
- Returns 201 Created with the saved user
- Returns 400 Bad Request if validation fails
```
The user writes their own code solution.

### Feedback Rules

**On correct answer:**
```
Correct!

Key point: @Transactional with default propagation (REQUIRED) joins
the existing transaction or creates a new one if none exists.
```

**On wrong answer:**
Give a short text explanation. Only use ASCII diagrams for things like request flows or architecture that are hard to explain in text alone.
```
Not quite. The answer is "REQUIRED".

REQUIRED means: if a transaction exists, join it; if not, create a new one.
This is the most common behavior and Spring's default.
```

### Step 3: Results Summary

After all 5 questions, show a summary:

```
Quiz Results
- Topic: Spring Transaction Management
- Score: 3/5
- Final difficulty: 4/5
- Strengths: @Transactional basics, isolation levels
- Needs work: Propagation types, rollback rules
- Suggestion: Review "transaction propagation" with /backend-study
```

### Rules

1. **Use the selected language** - from Step 0. Only code and keywords in English.
2. **One question at a time** - next question only after the current one is answered
3. **Open-ended by default** - the user must think and write answers. Multiple-choice OK for concept checks.
4. **ASCII diagrams only when needed** - default to text explanations
5. **Adaptive difficulty** - adjust to the learner's level automatically
6. **Encouraging tone** - wrong answers are learning opportunities
7. **No emojis** - clean text only
