---
name: dashform
description: Create and manage AI-powered smart forms, surveys, and quizzes through the Dashform MCP server. Supports open-ended, single-choice, multiple-choice, and rating questions with AI-powered conversational experiences.
compatibility: Requires Dashform MCP server running locally at https://getaiform.com/api/mcp
metadata:
  author: Dashform
  version: "2.0.0"
  website: https://getaiform.com
---

# Dashform Form Creation Skill

Create intelligent forms through the Dashform MCP (Model Context Protocol) server. This skill enables you to build surveys, quizzes, and feedback forms using MCP tools.

## When to Use This Skill

Use this skill when the user needs to:
- Create surveys, feedback forms, or questionnaires
- Design quizzes or personality tests
- Build conversational AI-powered forms
- Collect structured data from respondents

## Prerequisites

**IMPORTANT**: This skill requires:

1. **Dashform MCP Server**: The local development server must be running at `https://getaiform.com`
2. **User Authentication**: User session token from https://getaiform.com

## Workflow

### Step 1: Check for Cached Credentials

When the user asks to create a form, **ALWAYS check for cached credentials first**:

```bash
cat .claude/skills/dashform/credentials.json
```

- **If credentials exist**: Extract `userId`, `organizationId`, and `userName`, proceed to Step 4
- **If credentials don't exist**: Continue to Step 2

### Step 2: Request User Authentication

If credentials are not cached, guide the user to provide their session token:

```
"I need to authenticate you with Dashform first. Please follow these steps:

1. Sign in to https://getaiform.com
2. Open browser DevTools (F12)
3. Go to Application → Cookies
4. Find 'better-auth.session_token'
5. Copy its value and send it to me

Once you provide the token, I'll cache your credentials automatically."
```

### Step 3: Cache Credentials Automatically

When the user provides their session token, run the setup script with the token as an argument:

```bash
.claude/skills/dashform/scripts/setup-credentials.sh "user-provided-token"
```

Then read the cached credentials:

```bash
cat .claude/skills/dashform/credentials.json
```

Extract `userId`, `organizationId`, and `userName` for use in form creation.

### Step 4: Ask About Form Requirements

Ask the user what kind of form they want to create, addressing them by their userName:

```
"Great, {userName}! Your credentials are cached. What kind of form would you like to create?

For example:
- Customer satisfaction survey
- Employee feedback form
- Event registration
- Quiz or personality test
- NPS survey

Please describe what you need."
```

## Available MCP Tools

The Dashform MCP server provides the following tools:

### 1. `create_form` - Create a New Form

Creates a new form with full configuration support including questions, screens, theme, and branding.

**Basic Parameters:**
- `organizationId` (string, required): The organization ID to create the form in
- `userId` (string, required): The user ID creating the form
- `name` (string, required): The name of the form (1-255 characters)
- `type` (string, optional): Form type - `"structured"` (traditional, default) or `"dynamic"` (AI-powered conversational)
- `description` (string, optional): Description of the form
- `tone` (string, optional): Tone for the form (e.g., "friendly", "professional")

**Advanced Configuration Parameters:**
- `welcomeScreen` (object, optional): Welcome screen configuration (title, message, CTA)
- `endScreen` (object, optional): End screen configuration
- `endScreenEnabled` (boolean, optional): Whether to enable the end screen
- `endings` (array, optional): Multiple quiz endings for conditional selection
- `questions` (array, optional): List of questions for structured forms
- `snippets` (array, optional): Information snippets for AI to reference (dynamic forms)
- `maxFollowUpQuestions` (number, optional): Max follow-up questions (0-10, for dynamic forms)
- `theme` (object, optional): Visual theme (colors, fonts)
- `branding` (object, optional): Branding settings (logo, watermark)
- `backgrounds` (array, optional): Array of backgrounds (max 10)

**Returns:**
```json
{
  "success": true,
  "formId": "uuid",
  "name": "Form Name",
  "type": "structured",
  "description": "Form description",
  "tone": "friendly",
  "questionsCount": 5,
  "createdAt": "2024-01-29T...",
  "shareUrl": "https://getaiform.com/r/abc123",
  "editUrl": "https://getaiform.com/forms/uuid"
}
```

### 2. `create_reply` - Create a Form Response

Creates a new reply/response for an existing form.

**Parameters:**
- `formId` (string, required): The ID of the form to create a reply for
- `organizationId` (string, required): The organization ID the form belongs to
- `respondentName` (string, optional): Name of the person filling out the form
- `respondentEmail` (string, optional): Email of the person filling out the form
- `respondentEmotion` (string, optional): Initial emotional state - `"neutral"`, `"positive"`, or `"negative"`. Defaults to `"neutral"`
- `data` (object, optional): Initial form data as key-value pairs (question key → answer)

**Returns:**
```json
{
  "success": true,
  "replyId": "uuid",
  "formVersionId": "uuid",
  "status": "partial",
  "respondentName": "John Doe",
  "respondentEmail": "john@example.com",
  "respondentEmotion": "neutral",
  "data": {},
  "createdAt": "2024-01-29T..."
}
```

### Step 5: Generate Form Configuration

**IMPORTANT: Read Documentation First**

Before generating the form JSON configuration, **ALWAYS read these files**:

```bash
cat .claude/skills/dashform/references/SCHEMA.md
cat .claude/skills/dashform/references/API.md
```

This ensures correct structure and prevents MCP call errors.

Based on the user's requirements, generate a complete form JSON configuration.

**CRITICAL RULES:**

1. **Always create complete, production-ready forms** with:
   - ✅ Welcome screen (title, message, CTA)
   - ✅ Questions (at least 2-3 relevant questions)
   - ✅ End screen (thank you message)
   - ✅ Theme (colors and fonts)

2. **DO NOT create minimal forms** with only name and description

3. **Reference the examples/ directory** for complete templates:
   - `customer-survey.json` - Customer satisfaction survey
   - `quiz.json` - Personality quiz with multiple endings
   - `employee-satisfaction-survey.json` - Employee engagement survey
   - `event-registration.json` - Event registration form
   - `nps-survey.json` - NPS survey with AI follow-ups

4. **Reference the references/ directory** for detailed documentation:
   - `SCHEMA.md` - Complete form structure and question types
   - `API.md` - API endpoint documentation

5. **Form Type Selection**:
   - **Default**: Use `type: "structured"` (or omit type parameter)
   - **Only use `type: "dynamic"`** when user explicitly mentions:
     - "conversational form"
     - "AI-powered"
     - "follow-up questions"
     - "adaptive questions"

**Save the JSON configuration:**

Save the generated form configuration to the data/ directory with a descriptive filename:

```bash
# Filename format: {form-name}_{timestamp}.json
# Example: customer-survey_2024-01-30-143022.json
```

**Note:** Do NOT include `userId` or `organizationId` in the JSON file - these will be added automatically by the create-form script.

### Step 6: Create the Form

Run the create-form script with the JSON file path:

```bash
.claude/skills/dashform/scripts/create-form.sh "path/to/form.json"
```

The script will:
1. Read cached credentials (userId, organizationId)
2. Merge credentials with form configuration
3. Call MCP create_form tool
4. Return the form URLs

### Step 7: Inform the User

After successfully creating the form, provide:
- ✅ Success confirmation
- 📋 Share URL (for distributing to respondents)
- ✏️ Edit URL (for customizing the form)

Example response:
```
✅ Form created successfully!

📋 Share URL: https://getaiform.com/r/abc123
   (Share this link with your respondents)

✏️ Edit URL: https://getaiform.com/forms/uuid
   (Use this to customize your form)
```

## Form Types

| Type | Description | Use Case |
|------|-------------|----------|
| `structured` | Traditional fixed-question form (default) | Contact forms, registrations, surveys with fixed questions |
| `dynamic` | AI-powered conversational form | Complex surveys, interviews, personality quizzes |

**Recommendation**: Use `"structured"` for most cases with predefined questions. Use `"dynamic"` only when you need AI-powered conversational experiences with follow-up questions.

## Question Types Supported

| Type | Key | Description |
|------|-----|-------------|
| Open-ended | `open-ended` | Free text input |
| Single Choice | `single-choice` | Radio buttons (one answer) |
| Multiple Choice | `multiple-choice` | Checkboxes (multiple answers) |
| Rating | `rating` | 1-5 star rating |

## Tips for Best Results

1. **Always include complete configuration**: Don't create forms with just name and type
2. **Use appropriate form type**: Dynamic for conversational, structured for traditional
3. **Add welcome screens**: Set expectations and engage users
4. **Include end screens**: Thank users and provide next steps
5. **Apply themes**: Make forms visually appealing
6. **Reference examples**: Use the examples/ directory as templates

## Troubleshooting

### MCP Server Not Running

If you get connection errors:
1. Check that the server is running at `https://getaiform.com`
2. Verify the MCP endpoint is accessible at `/api/mcp`

### Invalid Credentials

If you get authentication errors:
1. Verify the Organization ID and User ID are correct
2. Check that the user has permission to create forms

### Form Creation Fails

If form creation fails:
1. Check that all required fields are provided
2. Verify the form configuration matches the schema
3. Review the error message for specific issues
