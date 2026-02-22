---
name: surveygo
description: >-
  Guides usage of the surveygo Go library (github.com/rendis/surveygo/v2)
  for building and managing surveys with validation, conditional logic, and
  output rendering. Covers parsing surveys from JSON, creating surveys
  programmatically, adding questions and groups, answer validation and
  translation, DependsOn conditional visibility, grouped/repeatable answers,
  and output generation (CSV, HTML, JSON, TipTap). Use when working with
  surveygo imports, Survey structs, question types, answer review, schema
  construction, or the render package.
---

# surveygo

Go library for creating and managing surveys with validation, conditional logic, and rendering.

Import: `github.com/rendis/surveygo/v2`

## Quick Start

```go
// Parse survey from JSON
survey, err := surveygo.ParseFromJsonStr(jsonStr)

// Review answers
answers := surveygo.Answers{
    "question1": {"answer_value"},
    "choice_q":  {"option_nameId"},
}
resume, err := survey.ReviewAnswers(answers)

// Translate choice nameIds to labels/values
translated, err := survey.TranslateAnswers(answers, false)
```

## Core Workflows

### Parse / Create Survey

```go
// From JSON string or bytes
survey, err := surveygo.ParseFromJsonStr(jsonStr)
survey, err := surveygo.ParseFromBytes(jsonBytes)

// Programmatically
survey, err := surveygo.NewSurvey("My Survey", "1.0", nil)
```

Parsing auto-validates struct, checks consistency, and assigns positions.

### Add Questions and Groups

```go
// Add question from JSON
err := survey.AddQuestionJson(`{
    "nameId": "fav_color",
    "visible": true,
    "type": "single_select",
    "label": "Favorite color?",
    "value": {
        "options": [
            {"nameId": "red", "label": "Red"},
            {"nameId": "blue", "label": "Blue"}
        ]
    }
}`)

// Assign question to group (position -1 = append)
err = survey.AddQuestionToGroup("fav_color", "my_group", -1)

// Add group
err = survey.AddGroupJson(`{"nameId": "my_group"}`)
survey.UpdateGroupsOrder([]string{"my_group", "other_group"})
```

All Add/Update methods have variants: `*Question(q)`, `*QuestionJson(s)`, `*QuestionBytes(b)`, `*QuestionMap(m)`.
Same for groups. Also `AddOrUpdate*` variants that upsert.

### Review Answers

```go
resume, err := survey.ReviewAnswers(answers)

// Check completion
fmt.Println(resume.TotalRequiredQuestionsAnswered, "/", resume.TotalRequiredQuestions)

// Check invalid answers
for _, inv := range resume.InvalidAnswers {
    fmt.Printf("%s: %s\n", inv.QuestionNameId, inv.Error)
}

// Per-group stats
groupResume := resume.GroupsResume["group_nameId"]
```

### Grouped (Repeatable) Answers

Groups with `AllowRepeat: true` accept multiple answer sets:

```go
answers := surveygo.Answers{
    "repeatable_group": {
        map[string][]any{"q1": {"a1"}, "q2": {"a2"}},  // set 1
        map[string][]any{"q1": {"b1"}, "q2": {"b2"}},  // set 2
    },
}
```

### DependsOn Conditional Logic

Questions/groups become visible only when referenced choice options are selected.

```json
{
  "dependsOn": [
    [{ "questionNameId": "q1", "optionNameId": "opt_a" }],
    [
      { "questionNameId": "q2", "optionNameId": "opt_b" },
      { "questionNameId": "q3", "optionNameId": "opt_c" }
    ]
  ]
}
```

- Outer array = **OR** (any group matches = visible)
- Inner array = **AND** (all conditions must match)
- Referenced question must be a **choice type**
- Invisible questions are excluded from `SurveyResume` totals

### Rendering

```go
import "github.com/rendis/surveygo/v2/render"

csvBytes, err := render.AnswersToCSV(survey, answers)
card, err := render.AnswersToJSON(survey, answers)
htmlResult, err := render.AnswersToHTML(survey, answers)
tiptap, err := render.AnswersToTipTap(survey, answers)

// Multi-format single pass
result, err := render.AnswersTo(survey, answers, render.OutputOptions{
    CSV: true, JSON: true, HTML: true, TipTap: true,
})

// HTMLResult has separate HTML + CSS
htmlResult.WithCSSPath("/static/card.css")  // replace CSS href
```

See [references/render.md](references/render.md) for full render API and typesGotchas

- **Answers type**: always `map[string][]any` — values are arrays even for single answers
- **Choice answers**: stored as option **nameIds** (strings). Use `TranslateAnswers` to get labels/values
- **Asset MaxFiles/MinFiles**: `0` means default `1`, **not** unlimited/zero. The lib does NOT validate file counts — consuming apps must handle this
- **External questions**: use direct type assertion `q.Value.(*external.ExternalQuestion)` — no `CastToExternal` function exists
- **AnswerExpr**: expr-lang/expr expression. Environment: `ans` ([]any) + `options` (map[nameId]label for choice types). Silent fallback on error (nil, false). Never writes to stderr
- **Group.Title**: is `*string`, not `string`
- **NameId regex**: `^[a-zA-Z][a-zA-Z\d_-]{1,62}[a-zA-Z\d]$` (3-64 chars, start with letter, end with alphanumeric)
- **Position**: auto-calculated — do not set manually
- **Slider**: is a choice type (complex) with `Min`, `Max`, `Step`, `Default`, `Unit` — not `Options`
- **RemoveQuestion**: auto-cleans DependsOn references from other questions and groups

## References

- [references/api.md](references/api.md) — Full API: all exported structs, methods, and function signatures
- [references/question-types.md](references/question-types.md) — All question types with their specific fields and cast functions
- [references/render.md](references/render.md) — Render package: output functions, types, and formats
