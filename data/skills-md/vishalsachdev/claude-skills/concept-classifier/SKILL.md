---
name: concept-classifier
description: Create an interactive classification quiz MicroSim using p5.js where students read scenarios and classify them into the correct category from multiple choice options. Uses a data.json file for easy question editing. Ideal for teaching students to recognize patterns, identify types, or categorize examples across any subject domain.
---

# Concept Classifier Quiz MicroSim Skill

## Overview

This skill creates interactive classification quiz MicroSims using p5.js. Students are presented with scenarios, examples, or descriptions and must classify them into the correct category from multiple choice options. The quiz format is ideal for teaching pattern recognition, concept identification, and categorization skills across any subject domain.

## When to Use This Skill

Use this skill when you need to create a quiz where students must:

- **Identify types or categories** - e.g., identify which cognitive bias is shown, which logical fallacy is used, which literary device is present
- **Classify examples** - e.g., classify animals into taxonomic groups, chemical reactions by type, historical events by era
- **Recognize patterns** - e.g., recognize which design pattern is used, which musical form is playing, which art movement a painting belongs to
- **Match scenarios to concepts** - e.g., match business scenarios to management theories, symptoms to conditions, code snippets to algorithms

## Features

- **Scenario-based questions** with detailed descriptions
- **Multiple choice answers** (typically 4 options per question)
- **Hint system** that reduces points but helps struggling students
- **Automatic explanations** shown after each answer
- **Score tracking** with visual progress indicator
- **Randomized question selection** from a larger pool
- **Encouraging feedback messages** for both correct and incorrect answers
- **Animated mascot character** that reacts to answers
- **End screen** with performance summary and tips
- **Fully configurable** via data.json file

## Data Structure

All quiz content is stored in a `data.json` file for easy editing. Here is the required structure:

```json
{
  "title": "Quiz Title Here",
  "description": "Brief description of what this quiz tests",
  "config": {
    "questionsPerQuiz": 10,
    "pointsCorrect": 10,
    "pointsWithHint": 5,
    "scenarioLabel": "SCENARIO",
    "instructionText": "Select the correct category for this scenario",
    "correctAnswerField": "correctAnswer"
  },
  "scenarios": [
    {
      "id": 1,
      "scenario": "Description of the scenario or example to classify...",
      "correctAnswer": "Category Name",
      "options": ["Category Name", "Wrong Option 1", "Wrong Option 2", "Wrong Option 3"],
      "explanation": "Explanation of why this answer is correct...",
      "hint": "A helpful hint for this question..."
    }
  ],
  "encouragingMessages": {
    "correct": [
      "Excellent!",
      "Well done!",
      "Great job!",
      "You got it!",
      "Perfect!"
    ],
    "incorrect": [
      "Not quite—now you know for next time!",
      "Good try! This one is tricky.",
      "Learning from mistakes makes us better!",
      "Keep practicing!",
      "Almost! Now you'll remember it."
    ]
  },
  "categoryDescriptions": {
    "Category Name": "Brief description of this category",
    "Another Category": "Brief description of another category"
  },
  "endScreen": {
    "tipsTitle": "Tips for Success:",
    "tips": [
      "First tip for students...",
      "Second tip for students...",
      "Third tip for students..."
    ],
    "performanceMessages": {
      "excellent": {
        "threshold": 90,
        "message": "Outstanding!",
        "subMessage": "You have excellent classification skills."
      },
      "good": {
        "threshold": 70,
        "message": "Great Job!",
        "subMessage": "You classified most items correctly."
      },
      "fair": {
        "threshold": 50,
        "message": "Good Progress!",
        "subMessage": "Keep practicing to improve."
      },
      "needsWork": {
        "threshold": 0,
        "message": "Keep Learning!",
        "subMessage": "Practice makes perfect."
      }
    }
  }
}
```

## File Structure

Each Concept Classifier MicroSim creates these files:

```
/docs/sims/$MICROSIM_NAME/
├── index.md           # Documentation page with iframe embed
├── main.html          # HTML wrapper loading p5.js
├── $MICROSIM_NAME.js  # p5.js quiz logic
├── data.json          # Quiz questions and configuration
└── metadata.json      # Dublin Core metadata
```

## Customization Options

### Visual Customization

The JavaScript file contains configurable parameters:

```javascript
// Canvas dimensions
let canvasWidth = 800;
let drawHeight = 480;
let controlHeight = 50;

// Colors (can be customized)
// Drawing area: 'aliceblue' with 'silver' border
// Correct answer: green tones
// Incorrect answer: orange/red tones
// Mascot: pink brain character (can be replaced)
```

### Mascot Character

The default mascot is an animated brain character with three expressions:
- **neutral** - default state
- **happy** - when answer is correct
- **thinking** - when hint is used or answer is incorrect

You can customize or replace the `drawMascotCharacter()` function to use a different mascot appropriate to your subject domain.

### Question Count

By default, 10 questions are randomly selected from the pool. Adjust in the config:

```json
"config": {
  "questionsPerQuiz": 10
}
```

Or modify in JavaScript:

```javascript
scenarios = shuffled.slice(0, 10);  // Change 10 to desired number
```

## Example Use Cases

### 1. Cognitive Bias Quiz (Ethics/Psychology)
Students read scenarios demonstrating cognitive biases and must identify which bias is shown.

### 2. Logical Fallacy Identifier (Philosophy/Critical Thinking)
Students analyze arguments and identify which logical fallacy is present.

### 3. Literary Device Recognizer (English/Literature)
Students read passages and identify metaphors, similes, personification, etc.

### 4. Chemical Reaction Classifier (Chemistry)
Students read reaction descriptions and classify as synthesis, decomposition, single replacement, etc.

### 5. Historical Era Matcher (History)
Students read about events or artifacts and match them to the correct historical period.

### 6. Design Pattern Identifier (Computer Science)
Students read code scenarios and identify which software design pattern applies.

### 7. Musical Form Quiz (Music)
Students listen to or read about musical pieces and identify the form (sonata, rondo, theme and variations, etc.).

### 8. Art Movement Classifier (Art History)
Students view or read about artworks and classify them into movements (Impressionism, Cubism, etc.).

## Implementation Steps

1. **Define your categories** - List all possible classification categories (typically 4-8)

2. **Create scenarios** - Write 15-30 scenarios, each clearly demonstrating one category

3. **Write explanations** - For each scenario, explain why it belongs to that category

4. **Add hints** - Provide helpful hints that guide without giving away the answer

5. **Customize messages** - Adjust encouraging messages and tips for your subject

6. **Test thoroughly** - Ensure all scenarios have correct answers and clear explanations

## Best Practices

### Writing Good Scenarios

- **Be specific** - Scenarios should clearly demonstrate one category
- **Avoid ambiguity** - Each scenario should have one clearly correct answer
- **Use realistic examples** - Real-world scenarios are more memorable
- **Vary difficulty** - Mix easy and challenging scenarios
- **Keep length manageable** - Scenarios should fit in the display area (roughly 2-4 sentences)

### Writing Good Distractors (Wrong Answers)

- **Make them plausible** - Wrong answers should be reasonable alternatives
- **Avoid obviously wrong options** - Each option should require thought
- **Use common misconceptions** - Include options that represent typical errors
- **Keep similar length** - Options should be roughly equal in length

### Writing Good Explanations

- **Explain the "why"** - Don't just state the answer, explain the reasoning
- **Reference key features** - Point out what makes this scenario fit the category
- **Keep it concise** - 2-3 sentences is ideal
- **Educational tone** - Use this as a teaching moment

## Template Files

This skill includes template files in the `/templates` directory:

- `concept-classifier-template.js` - Generalized p5.js quiz logic
- `data-template.json` - Example data structure with placeholders
- `main-template.html` - HTML wrapper
- `index-template.md` - Documentation page template

## Bloom's Taxonomy Level

This quiz format primarily addresses **Application (Level 3)** - students must apply their knowledge of categories to analyze new scenarios they haven't seen before.

## Integration with MkDocs

After creating the MicroSim, add it to `mkdocs.yml`:

```yaml
nav:
  - MicroSims:
    - Your Quiz Name: sims/your-quiz-name/index.md
```

## Technical Notes

- **Framework**: p5.js 1.11.10
- **Responsive**: Width-responsive, fixed height
- **Data loading**: Uses p5.js `loadJSON()` in `preload()`
- **Accessibility**: Includes `describe()` for screen readers
- **Browser support**: Modern browsers (Chrome, Firefox, Safari, Edge)

## Conclusion

The Concept Classifier skill provides a proven, engaging format for teaching classification and categorization skills. By separating content (data.json) from logic (JavaScript), it's easy to create new quizzes for any subject domain without modifying code.
