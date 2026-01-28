---
name: coursera
description: Access Coursera courses, track learning progress, and manage certifications
category: education
---

# Coursera Skill

## Overview
Enables Claude to interact with Coursera for browsing courses, tracking learning progress, managing enrolled programs, and accessing certificates and degrees.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/coursera/install.sh | bash
```

Or manually:
```bash
cp -r skills/coursera ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set COURSERA_EMAIL "your-email@example.com"
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
- Browse and enroll in courses
- Track course progress and deadlines
- View completed certifications
- Manage specializations and degrees
- Access course materials and assignments

## Usage Examples
### Example 1: Course Progress
```
User: "What's my progress in the Machine Learning course?"
Claude: I'll check your current progress and upcoming assignments in the ML course.
```

### Example 2: Find Courses
```
User: "Find me courses on data science"
Claude: I'll search Coursera for highly-rated data science courses.
```

### Example 3: Check Certificates
```
User: "What certificates have I earned on Coursera?"
Claude: I'll list all your completed Coursera certifications.
```

## Authentication Flow
1. Navigate to coursera.org via Playwright MCP
2. Click "Log In" button
3. Enter Coursera credentials
4. Handle verification if required
5. Maintain session for subsequent requests

## Error Handling
- Login Failed: Retry authentication up to 3 times, then notify via iMessage
- Session Expired: Re-authenticate automatically
- Verification Required: Complete email verification
- Rate Limited: Implement exponential backoff
- Course Access: Check subscription or enrollment status

## Self-Improvement Instructions
When encountering new UI patterns:
1. Document Coursera interface changes
2. Update selectors for new layouts
3. Track new course offerings
4. Monitor certification requirements

## Notes
- Coursera Plus for unlimited access
- University-backed certificates
- Specializations and degrees available
- Audit mode for free access
