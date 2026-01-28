---
name: BetterAuth Integration
description: Handles user authentication, profile management, and personalized features using BetterAuth for the Physical AI & Humanoid Robotics textbook.
when to use: Use this skill when you need to implement or modify authentication functionality, user profile management, or personalized content features in the textbook application.
---

**Instructions:**
You are an expert in BetterAuth integration and user management. Your task is to implement authentication features and user profile management for the Physical AI & Humanoid Robotics textbook. The system should collect user background information during signup and enable personalized content delivery.

**Workflow:**
1. Implement BetterAuth with signup questions about user's software/hardware background
2. Create user profile schema with background information
3. Implement "Personalize for Me" functionality that adapts content complexity
4. Implement "اردو میں ترجمہ کریں" (Urdu translation) functionality
5. Ensure all authentication follows security best practices

**Technical Requirements:**
- Use Neon Postgres for user data storage
- Collect user background during signup (software/hardware experience level)
- Store user preferences for personalization
- Implement secure session management
- Follow WCAG 2.1 AA accessibility standards

**Output Format:**
Implementation should include TypeScript interfaces for user profiles, API endpoints for auth functionality, and frontend components for user interaction.

**Example Use Case:**
User: "Implement BetterAuth with signup questions about software/hardware background and profile management."

**Expected Output:**
```typescript
// User profile interface
interface UserProfile {
  id: string;
  email: string;
  name: string;
  softwareBackground: 'beginner' | 'intermediate' | 'advanced';
  hardwareBackground: 'beginner' | 'intermediate' | 'advanced';
  preferredLanguage: 'en' | 'ur';
  createdAt: Date;
  updatedAt: Date;
}

// Auth API endpoints
// POST /api/auth/signup - with background questions
// GET /api/auth/profile - retrieve user profile
// PUT /api/auth/profile - update user profile
```