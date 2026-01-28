---
name: google-forms
description: Enables Claude to create, edit, and analyze Google Forms surveys and quizzes via Playwright MCP
category: google
---

# Google Forms Skill

## Overview
Claude can create and manage Google Forms to build surveys, quizzes, and data collection forms. This includes designing questions, analyzing responses, and sharing forms with respondents.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/google-forms/install.sh | bash
```

Or manually:
```bash
cp -r skills/google-forms ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set GOOGLE_EMAIL "your-email@gmail.com"
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
- Create new forms and quizzes
- Add various question types
- Configure form settings and logic
- Add sections and page breaks
- Set up response validation
- View and analyze responses
- Export responses to Sheets
- Share forms via link or email
- Set form as quiz with scoring
- Add images and videos to questions
- Create branching logic
- Set response limits and deadlines

## Usage Examples

### Example 1: Create Survey
```
User: "Create a customer feedback survey with 5 questions"
Claude: Creates form "Customer Feedback Survey", adds questions for
        satisfaction, service quality, recommendations, etc.
        Returns: "Created survey with 5 questions: [link]"
```

### Example 2: View Responses
```
User: "How many people responded to my event RSVP form?"
Claude: Opens form, checks responses tab.
        Reports: "42 responses received. 35 attending, 7 not attending.
        Most common +1s: 1 guest"
```

### Example 3: Create Quiz
```
User: "Make a quiz about US history with 10 multiple choice questions"
Claude: Creates quiz form, adds 10 MC questions with correct answers
        and point values. Returns: "Quiz created: [link]"
```

### Example 4: Add Logic
```
User: "If someone selects 'Other', show a text field to explain"
Claude: Adds conditional logic to show follow-up text question
        when 'Other' is selected. Confirms: "Conditional logic added"
```

## Authentication Flow
1. Claude navigates to forms.google.com via Playwright MCP
2. Authenticates with GOOGLE_EMAIL if needed
3. Handles 2FA if prompted (notifies user via iMessage)
4. Maintains session for subsequent Forms operations

## Selectors Reference
```javascript
// Create new form
'[aria-label="Blank"]'

// Form title
'.freebirdFormeditorViewHeaderTitleInput'

// Add question
'[aria-label="Add question"]'

// Question text
'.freebirdFormeditorViewItemTitleContainer'

// Question type dropdown
'.freebirdFormeditorViewQuestionTypeDropdown'

// Answer options
'.freebirdFormeditorViewQuestionOptionListItem'

// Add option
'[aria-label="Add option"]'

// Required toggle
'[aria-label="Required"]'

// Responses tab
'[aria-label="Responses"]'

// Settings button
'[aria-label="Settings"]'

// Send button
'[aria-label="Send"]'

// Quiz mode toggle
'[aria-label="Make this a quiz"]'
```

## Question Types
```
Short answer      // Single line text
Paragraph        // Multi-line text
Multiple choice  // Single select
Checkboxes       // Multi select
Dropdown         // Select from list
File upload      // Upload files
Linear scale     // 1-5 or 1-10 rating
Multiple choice grid  // Grid of options
Checkbox grid    // Grid with multi-select
Date             // Date picker
Time             // Time picker
```

## Error Handling
- **Login Failed**: Retry 3 times, notify user via iMessage
- **Session Expired**: Re-authenticate automatically
- **Form Creation Failed**: Retry, check for permission issues
- **Question Add Failed**: Retry, verify question type supported
- **Response Export Failed**: Check Sheets permissions, retry
- **Share Failed**: Verify form settings allow sharing

## Self-Improvement Instructions
When you learn a better way to accomplish a task with Google Forms:
1. Document the improvement in your response
2. Suggest updating this skill file with the new approach
3. Include specific question design best practices
4. Note any new question types or features

## Notes
- Forms automatically save changes
- Responses can link to Google Sheets for analysis
- Quiz mode enables auto-grading for supported question types
- File uploads count against Drive storage
- Form can be closed after deadline or response limit
- Respondents can be limited to one response
- Pre-filled links can set default answers
- Forms support 26 languages
- Responses can require sign-in for verified identity
