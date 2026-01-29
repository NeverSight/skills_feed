---
name: epsimo-agent
description: Interact with the EpsimoAI platform to manage agents, projects, and threads, and design frontends.
---

# EpsimoAI Agent Skill (Beta)

> [!NOTE]
> This is a **Beta** version of the EpsimoAI Agent Skill. Features and APIs may be subject to change.


This skill allows you to interact with the EpsimoAI platform. You can manage projects, assistants, threads, and run streams. You can also design frontend applications that integrate with the platform.

**Base URL:** `https://api.epsimoagents.com`
**Frontend URL:** `https://app.epsimoagents.com`

## Prerequisites

### Authentication

This skill requires authentication with the EpsimoAI platform.

You can set up authentication by running the login script interactively:

```bash
python3 .agent/skills/epsimo-agent/scripts/auth.py login
```

This will prompt you for your email and password securely, then save the session token.

Alternatively, you can set the following environment variables:

- `EPSIMO_EMAIL`: Your EpsimoAI account email.
- `EPSIMO_PASSWORD`: Your EpsimoAI account password.
- `EPSIMO_API_URL`: Optional (defaults to `https://api.epsimoagents.com`).

If the session token expires or is missing, you will be prompted to log in again.

**User Creation:**
If you try to log in with an email that does not exist, the script can support valid flow if configured, but typically you should use an existing verified account.

## Capabilities

### 1. Manage Projects
- Create new projects.
- List existing projects.
- Get project details.

### 2. Manage Assistants
- Create new AI assistants. Application logic ensures required configuration (`configurable: { type: "agent" }`) is automatically applied.
- Configure assistant tools and instructions.
- List assistants.

### 3. Manage Threads
- Create new conversation threads.
- List threads.

### 4. Run & Stream
- Execute runs on a thread.
- Stream responses from the assistant using server-sent events (SSE).

### 5. Design Frontend
- Generate React/Next.js code for a frontend application that connects to your EpsimoAI agent.

## Usage

### Scripts

The skill provides several Python scripts in the `scripts/` directory to handle API interactions.

#### Setup & Auth
Authentication is handled automatically by the scripts. If no valid token is found, you will be prompted to log in.

To manually log in:
```bash
python3 .agent/skills/epsimo-agent/scripts/auth.py login
```

#### List Projects
```bash
python3 .agent/skills/epsimo-agent/scripts/project.py list
```

#### Create an Assistant
```bash
python3 .agent/skills/epsimo-agent/scripts/assistant.py create --project-id <PROJECT_ID> --name "My Assistant" --instructions "You are a helpful assistant." --model "gpt-4o"
```

#### Create a Thread
```bash
python3 .agent/skills/epsimo-agent/scripts/thread.py create --project-id <PROJECT_ID> --name "New Chat" --assistant-id <ASSISTANT_ID>
```

#### Stream a Run
```bash
python3 .agent/skills/epsimo-agent/scripts/run.py stream --project-id <PROJECT_ID> --thread-id <THREAD_ID> --assistant-id <ASSISTANT_ID> --message "Hello, world!"
```

### Verification
You can run the full verification suite to ensure all components are working:
```bash
python3 .agent/skills/epsimo-agent/scripts/verify_skill.py
```

### Frontend Design

When designing a frontend, ensure your API calls match the structure used by the platform:

1.  **Project Context**: You may need to fetch a project-specific token via `GET /projects/{id}`.
2.  **Thread Creation**: When creating a thread, include the `assistant_id` and required metadata:
    ```javascript
    await api.post('/threads/', {
      body: {
        name: "Thread Name",
        assistant_id: assistantId,
        metadata: { configurable: {}, type: "thread" },
        configurable: { type: "agent" }
      }
    });
    ```
3.  **Streaming**: Use the `/runs/stream` endpoint with `stream_mode: ["messages", "events", "values"]`.

## Component Templates

The skill includes ready-to-use React components in `templates/components`. These are designed to jumpstart your frontend implementation.

### Available Components

1.  **ThreadChat**: A full-featured chat interface that handles streaming, tool rendering, and markdown.
    -   Location: `templates/components/ThreadChat`
    -   Features: Streaming support, tool call visualization, file upload, markdown rendering.
2.  **AuthModal**: A modal component for Login and Signup flows.
    -   Location: `templates/components/AuthModal`
    -   Features: Tabbed interface, form validation, error handling.
3.  **BuyCredits**: Components for displaying credit balance and purchasing more.
    -   Location: `templates/components/BuyCredits`
    -   Features: Progress bar display, pricing cards modal, Stripe checkout integration.

### How to Use

You can copy these components into your project's component directory:

```bash
# Copy ThreadChat
cp -r .agent/skills/epsimo-agent/templates/components/ThreadChat src/components/

# Copy AuthModal
cp -r .agent/skills/epsimo-agent/templates/components/AuthModal src/components/

# Copy BuyCredits
cp -r .agent/skills/epsimo-agent/templates/components/BuyCredits src/components/
```

Ensure you have the required dependencies installed (e.g., `react-markdown`, `react-syntax-highlighter`, `remark-gfm`).

### Managing Credits via Script

You can also check your balance and buy credits using the python script:

```bash
# Check balance
python3 .agent/skills/epsimo-agent/scripts/credits.py balance

# Buy 100 credits (creates checkout URL)
python3 .agent/skills/epsimo-agent/scripts/credits.py buy --quantity 100
```

