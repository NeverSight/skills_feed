---
name: authentication
description: Implement secure, production-grade authentication systems with token-based session management. Use this skill when the user asks to build user authentication, login/registration systems, session management, user identity features, or secure access control for web applications.
license: Complete terms in LICENSE.txt
---

This skill guides implementation of secure authentication systems with persistent session management, token-based authentication, and comprehensive user identity handling.

The user provides authentication requirements: login, registration, session management, or user profile features. They may include context about security needs, user experience expectations, or integration requirements.

## Authentication System Principles

Before implementing, understand the security context and user experience requirements:
- **Security First**: What data needs protection? What are the threat vectors?
- **User Experience**: Balance security with friction - seamless for legitimate users, secure against attacks
- **Session Management**: How long should sessions last? When should re-authentication be required?
- **Scalability**: How will authentication scale with user growth?
- **Compliance**: What regulatory requirements apply (GDPR, data protection, etc.)?

**CRITICAL**: Authentication is a security-critical component. Every decision must prioritize user data protection while maintaining a smooth user experience.

## Core Authentication Requirements

### User Registration
- Collect unique username and email address with format validation
- Implement secure password hashing (never store plain text passwords)
- Use industry-standard hashing algorithms with salt
- Validate uniqueness of username and email before account creation
- Optional profile information collection (names, profile picture)
- Automatic account creation timestamp tracking
- Email format and username validation required

### User Login
- Support authentication with either email or username
- Verify credentials against securely stored hashes
- Generate both access token (short-lived) and refresh token (long-lived)
- Return user profile data with authentication tokens
- Track failed login attempts to prevent brute force attacks
- Implement account lockout after multiple failed attempts
- Support session persistence across browser sessions

### Token Management
- **Access Token**: Short expiration (15-60 minutes recommended)
  - Used for API authentication on each request
  - Contains minimal user identification data
  - Transmitted with each authenticated request

- **Refresh Token**: Extended expiration (7-30 days recommended)
  - Used to obtain new access tokens
  - Stored securely on client side
  - Rotated on each refresh for security

- **Token Lifecycle**:
  - Automatic token refresh before access token expiration
  - Token invalidation on explicit logout
  - Token blacklisting mechanism to prevent reuse of logged-out tokens
  - Secure token generation with sufficient entropy

### Session Persistence
- Store authentication state in browser storage (localStorage or sessionStorage)
- Automatically restore login state on page refresh
- Validate stored tokens on application initialization
- Clear all authentication state on logout
- Handle token expiration gracefully with automatic refresh
- Synchronize authentication state across browser tabs if needed

### User Logout
- Invalidate current access token
- Add refresh token to blacklist to prevent reuse
- Clear all client-side authentication state
- Clear any cached user data
- Redirect to public area after successful logout
- Revoke any active sessions on server side

## User Profile Management

### User Identity
- Display username, email, and registration date
- Support profile picture upload during registration or later
- Generate default avatar from user initials when no picture provided
- Store and display user preferences and settings
- Link user identity across all user-generated content

### Profile Picture Management
- Accept common image formats (JPEG, PNG)
- Enforce maximum file size limits (5MB recommended)
- Store optimized versions of uploaded images
- Display profile pictures in navigation, content, and user references
- Implement image validation to prevent malicious uploads
- Generate thumbnails for different display contexts

### User Identity Display
- Show author information consistently across the platform
- Display user avatars in navigation bar when authenticated
- Link author profiles to their published content
- Ensure consistent user identification across all features

## Security Requirements

### Authentication Security
- **Password Security**:
  - Hash passwords with salt using industry-standard algorithms
  - Enforce minimum password strength requirements
  - Never log or display passwords in any form
  - Implement secure password reset mechanisms

- **Token Security**:
  - Generate tokens with cryptographically secure random generation
  - Encrypt tokens in transit (HTTPS required)
  - Implement token expiration enforcement
  - Rotate refresh tokens regularly
  - Prevent token leakage through logging or error messages

- **Attack Prevention**:
  - Rate limiting on authentication endpoints
  - Account lockout after multiple failed login attempts
  - CSRF protection on authentication state changes
  - SQL injection prevention through parameterized queries
  - XSS prevention in user-generated profile content

### Authorization Controls
- Verify resource ownership before allowing modifications
- Implement permission checks on all protected endpoints
- Prevent unauthorized access to user data
- Validate user identity on every authenticated request
- Separate authentication (who you are) from authorization (what you can do)

### Data Protection
- Encrypt sensitive data in transit (TLS/HTTPS)
- Consider encryption at rest for sensitive user data
- Implement secure session management
- Sanitize all user inputs to prevent injection attacks
- Output encoding for display of user-generated content
- Validate file uploads thoroughly (type, size, content)

## Implementation Guidelines

### Client-Side Implementation
- Store tokens securely (avoid localStorage for highly sensitive apps, consider httpOnly cookies)
- Implement automatic token refresh before expiration
- Handle authentication state globally (context/state management)
- Provide clear loading and error states during authentication
- Clear all user data from memory on logout
- Redirect unauthenticated users appropriately
- Show authentication status clearly in UI

### Server-Side Implementation
- Use established authentication libraries/frameworks
- Implement token generation with proper randomness
- Create token blacklist table for logout tracking
- Index authentication-related database fields
- Log authentication events for security monitoring
- Implement rate limiting middleware
- Handle concurrent login attempts properly

### User Experience
- Minimize friction during registration (request only essential data)
- Provide clear error messages without leaking security information
- Show password strength indicators during registration
- Implement "remember me" functionality securely
- Auto-login after successful registration
- Smooth transition between authenticated and unauthenticated states
- Loading states during authentication operations

### Error Handling
- Generic error messages for authentication failures (don't specify if username or password was wrong)
- Clear error messages for validation failures
- Handle network errors gracefully
- Retry logic for token refresh failures
- Fallback to logout if token refresh repeatedly fails
- User-friendly messages for account lockouts

## Optional Advanced Features

Consider implementing these features based on project requirements:

### Enhanced Security
- Two-factor authentication (2FA/MFA)
- Email verification for new accounts
- Security questions for account recovery
- IP-based access monitoring
- Login notification emails
- Suspicious activity detection
- Device tracking and management

### Enhanced User Experience
- Social authentication (OAuth providers)
- Single sign-on (SSO) integration
- Biometric authentication support
- Passwordless authentication options
- "Stay logged in" with secure implementation

### Profile Enhancements
- Public profile pages with user biography
- Social media links integration
- User activity history and statistics
- Profile customization options
- Follower/following system
- User reputation or badge system
- Profile privacy controls

### Session Management
- View active sessions
- Remote session termination
- Session timeout warnings
- Multi-device session management

## Testing Requirements

Implement comprehensive testing for authentication:
- Test all registration validation rules
- Test successful and failed login scenarios
- Test token generation and validation
- Test token refresh mechanism
- Test logout and token invalidation
- Test password hashing and verification
- Test rate limiting and brute force protection
- Test session persistence across page reloads
- Test concurrent session handling
- Security testing for common vulnerabilities (SQL injection, XSS, CSRF)

## Compliance Considerations

Ensure authentication system meets regulatory requirements:
- Implement privacy policy acceptance mechanism
- Provide data access controls for user data
- Implement data export functionality
- Support data deletion (right to be forgotten)
- Cookie consent management if using cookies
- Log retention policies for security events
- Comply with data protection regulations (GDPR, CCPA)

## Common Pitfalls to Avoid

- Never store passwords in plain text or reversible encryption
- Don't expose user enumeration through different error messages
- Avoid client-side only validation (always validate server-side)
- Don't log sensitive data (passwords, tokens, personal information)
- Never trust client-sent data without validation
- Don't implement custom cryptography (use established libraries)
- Avoid storing tokens in insecure locations
- Don't skip rate limiting on authentication endpoints
- Never expose stack traces or detailed errors to clients

Remember: Authentication is the foundation of application security. Implement it thoroughly, test it comprehensively, and maintain it diligently. A secure authentication system protects both users and the entire application.
