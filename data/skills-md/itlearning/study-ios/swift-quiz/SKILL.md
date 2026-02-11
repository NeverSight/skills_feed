---
name: swift-quiz
description: Adaptive Swift/iOS quiz with 5 questions. Difficulty adjusts based on your answers. Use when reviewing or testing your Swift knowledge.
---

# swift-quiz - Swift/iOS Quiz

Adaptive quiz and coding exercises for Swift/iOS.
(적응형 퀴즈와 코딩 연습을 위한 스킬.)

## Instructions

Give a Swift/iOS quiz. Difficulty adjusts automatically based on the learner's level.
(Swift/iOS 퀴즈를 출제한다. 난이도는 학습자 수준에 맞게 자동 조절한다.)

### Step 0: Language Selection

Ask the user to choose a language at the start using AskUserQuestion:
(스킬 시작 시 AskUserQuestion으로 언어를 선택한다)

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

Use the selected language for all communication. Code and Swift keywords stay in English.
(선택한 언어로 이후 모든 소통을 진행한다. 코드와 Swift 키워드는 영어 그대로 유지한다.)

### Step 1: Choose Quiz Topic

Ask in plain text:
(텍스트로 물어본다)

**Korean:**
"어떤 주제로 퀴즈를 풀까요? 주제를 알려주세요. 뭘 할지 모르겠으면 '추천해줘'라고 해주세요."

**English:**
"What topic should the quiz cover? Tell me a topic, or say 'recommend' if you're not sure."

- If the user enters a topic: start the quiz on that topic.
  (유저가 주제를 입력한 경우: 해당 주제로 바로 퀴즈 시작)
- If the user says "recommend" / "추천해줘": check learning history (SwiftLearningProgress in memory) and suggest 3-4 recently studied topics. Present choices via AskUserQuestion.
  (학습 이력을 참고하여 최근 학습한 주제 중심으로 3-4개 추천. AskUserQuestion으로 선택지 제시.)

### Step 2: Run the Quiz (5 questions)

5 questions total. Track difficulty internally from 1-5 (start at 3).
(총 5문제. 내부적으로 난이도를 1~5로 추적한다. 시작: 3.)

- Correct answer -> difficulty +1 (정답 -> 난이도 +1)
- Wrong answer -> difficulty -1 (오답 -> 난이도 -1)

### Question Types

Each question uses one of the types below. **Default to open-ended, mix in others as appropriate.**
(아래 유형 중 하나로 출제. 서술형을 기본으로 하되, 적절히 섞는다.)

#### Type A: Predict Output (open-ended / 서술형)
```
What does this code print? Explain your answer.
(다음 코드의 출력 결과는? 답과 이유를 함께 적어주세요.)

var nums = [1, 2, 3]
var copy = nums
copy.append(4)
print(nums.count)
```
The user types their own answer. (유저가 직접 답을 타이핑한다.)

#### Type B: Find the Bug (open-ended / 서술형)
```
What's wrong with this code? Explain why it errors.
(다음 코드에서 문제가 되는 부분은? 왜 에러가 나는지 설명해주세요.)

let name: String = "Swift"
name = "SwiftUI"
print(name)
```
The user types their own answer. (유저가 직접 답을 타이핑한다.)

#### Type C: Concept Question (multiple-choice allowed / 객관식 허용)
```
What keyword do you need to modify a struct's property inside a method?
(Swift에서 struct 인스턴스의 프로퍼티를 메서드 안에서 변경하려면 어떤 키워드가 필요할까요?)
```
Present 4 choices via AskUserQuestion. Multiple-choice is fine for concept checks.
(AskUserQuestion으로 4지선다 제시. 개념 확인용은 객관식도 괜찮다.)

#### Type D: Write Code (difficulty 4+ only / 난이도 4 이상)
```
Write a function that meets these requirements:
(다음 조건을 만족하는 함수를 작성하세요:)

- Name: isEven (함수명: isEven)
- Takes an Int, returns Bool (Int를 받아서 Bool을 반환)
- Returns true for even, false for odd (짝수면 true, 홀수면 false)
```
When the user writes code, use the Task tool with `subagent_type: "Bash"` to verify it with the Swift compiler (`swift` command).
(사용자가 코드를 작성하면 Task 도구로 서브에이전트를 활용하여 Swift 컴파일러로 검증한다.)

### Feedback Rules

**On correct answer / 정답일 때:**
```
Correct!

Key point: Array is a value type, so `copy` is an independent copy.
That means nums.count is still 3.

(정답입니다! 핵심 포인트: Array는 값 타입이라서 copy는 독립적인 복사본입니다.)
```

**On wrong answer / 오답일 때:**
Give a short text explanation. Only use ASCII diagrams for things like memory layouts that are hard to explain in text alone.
(간결한 텍스트 해설을 제공한다. ASCII 다이어그램은 텍스트만으로 설명하기 어려운 경우에만 사용.)
```
Not quite. The answer is "3".

Array is a struct (value type), so `var copy = nums` creates an independent copy.
Appending to copy doesn't affect the original nums.

(아쉽지만 틀렸습니다. 정답은 "3"입니다.
Array는 struct(값 타입)이므로 독립적인 복사본을 만듭니다.)
```

### Step 3: Results Summary

After all 5 questions, show a summary:
(5문제 완료 후 결과 요약)

```
Quiz Results / 퀴즈 결과
- Topic / 주제: Basic syntax
- Score / 정답: 3/5
- Final difficulty / 최종 난이도: 4/5
- Strengths / 강점: Optional handling, type system
- Needs work / 보완 필요: Value types vs reference types
- Suggestion / 추천: Review "value vs reference types" with /swift-study
```

### Rules

1. **Use the selected language** - from Step 0. Only code and keywords in English. (선택한 언어로 소통)
2. **One question at a time** - next question only after the current one is answered (한 번에 한 문제만)
3. **Open-ended by default** - the user must think and write answers. Multiple-choice OK for concept checks. (서술형 중심)
4. **ASCII diagrams only when needed** - default to text explanations (ASCII 다이어그램은 필요할 때만)
5. **Adaptive difficulty** - adjust to the learner's level automatically (난이도 적응)
6. **Encouraging tone** - wrong answers are learning opportunities (격려하는 톤)
7. **No emojis** - clean text only (이모지 사용 금지)
