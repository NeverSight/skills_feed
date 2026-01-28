---
name: microsoft-forms
description: Enables Claude to create, manage, and analyze Microsoft Forms surveys and quizzes via Playwright MCP
category: microsoft
---

# Microsoft Forms Skill

## Overview
Claude can create and manage Microsoft Forms for surveys, quizzes, and data collection. Build forms with various question types, analyze responses, and share forms with respondents.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/microsoft-forms/install.sh | bash
```

Or manually:
```bash
cp -r skills/microsoft-forms ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set MICROSOFT_EMAIL "your-email@outlook.com"
```

## Privacy & Authentication

**Your credentials, your choice.** Canifi LifeOS respects your privacy.

### Option 1: Manual Browser Login (Recommended)
If you prefer not to share credentials with Claude Code:
1. Complete the [Browser Automation Setup](/setup/automation) using CDP mode
2. Login to the service manually in the Playwright-controlled Chrome window
3. Claude will use your authenticated session without ever seeing your password

### Option 2: Environment Variables
If you're comfortable sharing credentials, you can store them locally:
```bash
canifi-env set SERVICE_EMAIL "your-email"
canifi-env set SERVICE_PASSWORD "your-password"
```

**Note**: Credentials stored in canifi-env are only accessible locally on your machine and are never transmitted.

## Capabilities
- Create surveys and quizzes
- Add various question types
- Configure branching logic
- Set form settings and restrictions
- View and analyze responses
- Export responses to Excel
- Share forms via link or email
- Create quiz with auto-grading
- Add images and videos
- Apply themes and branding
- Set response notifications
- Duplicate and template forms

## Usage Examples

### Example 1: Create Survey
```
User: "Create an employee satisfaction survey"
Claude: Creates form with title, adds satisfaction rating questions,
        open-ended feedback section.
        Returns: "Created survey with 6 questions: [link]"
```

### Example 2: View Responses
```
User: "How many people responded to the training feedback form?"
Claude: Opens form, checks responses.
        Reports: "28 responses received. Average satisfaction: 4.2/5.
        Key feedback themes: more hands-on exercises requested"
```

### Example 3: Create Quiz
```
User: "Make a quiz about company policies with 10 questions"
Claude: Creates quiz form, adds multiple choice questions
        with correct answers and points.
        Returns: "Quiz created with 10 questions, 100 points total"
```

### Example 4: Add Branching
```
User: "If someone selects 'Remote', ask about their home office setup"
Claude: Adds branching logic from Remote option to follow-up questions.
        Confirms: "Branching logic added for Remote selection"
```

## Authentication Flow
1. Claude navigates to forms.office.com via Playwright MCP
2. Authenticates with MICROSOFT_EMAIL if needed
3. Handles 2FA if prompted (notifies user via iMessage)
4. Maintains session for Forms operations

## Selectors Reference
```javascript
// New form button
'[aria-label="New Form"]'

// Form title
'.form-title-input'

// Add question
'[aria-label="Add new"]'

// Question type menu
'.question-type-menu'

// Question text
'.question-title-input'

// Answer options
'.choice-input'

// Required toggle
'[aria-label="Required"]'

// Branching
'[aria-label="Branching"]'

// Responses tab
'[aria-label="Responses"]'

// Share button
'[aria-label="Share"]'

// Settings
'[aria-label="Settings"]'
```

## Question Types
```
Choice           // Multiple choice (single select)
Text             // Short or long answer
Rating           // Star or number rating
Date             // Date picker
Ranking          // Order items
Likert           // Agreement scale
File upload      // Upload attachments
Net Promoter Score // NPS question
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Form Create Failed**: Retry, check permissions
- **Question Add Failed**: Retry, verify question type
- **Export Failed**: Check Excel availability, retry
- **Share Failed**: Verify sharing settings

## Self-Improvement Instructions
When you learn a better way to accomplish a task with Microsoft Forms:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific question design best practices
4. Note quiz vs form differences

## Notes
- Forms auto-saves changes
- Quiz mode enables grading
- Branching creates dynamic forms
- Response notifications available
- Export to Excel for analysis
- Anonymous or identified responses
- Forms accessible on mobile
- Templates available for common use cases
