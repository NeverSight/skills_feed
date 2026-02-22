---
name: notification-best-practices
description: Comprehensive guidelines for designing, writing, and implementing effective notification systems across email, push, SMS, in-app, and chat channels.
---

# Notification best practices skill

This skill provides comprehensive guidelines and best practices for designing, writing, and implementing effective notification systems across all channels.

## Overview

The notification best practices skill includes six detailed rule sets covering:

1. **Channel-specific notification guidelines** - Specifications for email, push, SMS, in-app, and chat notifications
2. **Notification copy best practices** - Core principles for writing effective notification copy
3. **Notification system implementation rules** - Technical implementation guidelines including timing, preferences, error handling, and compliance
4. **Notification template examples** - Ready-to-use templates for common notification use cases
5. **Transactional email best practices** - Deliverability, templates, localization, and dynamic content for transactional emails
6. **Welcome email best practices** - Guidelines for crafting effective SaaS welcome emails

## How to use this skill

### For writing notifications

When you need to write notification copy:

1. **Start with copy best practices** (`rules/notification-copy-best-practices.md`)
   - Follow core principles: be specific, include context, use active voice
   - Choose the right tone and structure for your notification type

2. **Check channel-specific guidelines** (`rules/channel-specific-notifications-guidelines.md`)
   - Verify character limits for your target channel
   - Follow channel-specific formatting requirements
   - Ensure your message fits the channel's constraints

3. **Reference templates** (`rules/notification-template-examples.md`)
   - Find similar use cases to your notification
   - Adapt template structure and variables
   - Use provided examples as starting points

### For email notifications

When working with email notifications:

1. **Review transactional email best practices** (`rules/transactional-email-best-practices.md`)
   - Follow deliverability guidelines
   - Use componentized templates and partials
   - Implement proper localization

2. **For welcome emails specifically** (`rules/welcome-email-best-practices.md`)
   - Choose the right pattern for your product
   - Follow timing best practices
   - Focus on value and clear CTAs

### For system implementation

When implementing a notification system:

1. **Follow system implementation rules** (`rules/notification-system-implementation.md`)
   - Understand channel selection criteria
   - Implement proper timing and frequency controls
   - Set up preference management
   - Handle errors and retries correctly
   - Ensure compliance with regulations

2. **Use channel-specific guidelines** for technical constraints
   - Character limits
   - Formatting requirements
   - Delivery specifications

## Rule files reference

- `rules/channel-specific-notifications-guidelines.md` - Channel specifications and constraints
- `rules/notification-copy-best-practices.md` - Writing principles and guidelines
- `rules/notification-system-implementation.md` - Technical implementation rules
- `rules/notification-template-examples.md` - Template library with examples
- `rules/transactional-email-best-practices.md` - Email-specific best practices
- `rules/welcome-email-best-practices.md` - Welcome email patterns and guidelines

## Quick reference

### Channel selection
- **Email**: Persistent reference, detailed content, non-time-critical
- **Push**: Time-sensitive, requires app return, urgent actions
- **SMS**: Guaranteed delivery, authentication, extreme time-criticality
- **In-app**: User active in product, can wait until next session
- **Chat**: Team collaboration, immediate visibility needed

### Copy principles
- Be specific and actionable
- Include maximum context
- Use active voice
- Maintain consistent terminology
- Format for each channel

### Common patterns
- Transactional: Confirm what happened, include identifiers, provide next steps
- System: Translate technical events to user impact, offer actionable steps
- Lifecycle: Balance value with frequency, use social proof appropriately
- Promotional: Lead with benefits, make offers specific and time-bound

## Best practices summary

1. **Always provide context** - Users need enough information to decide whether to act
2. **Respect channel constraints** - Follow character limits and formatting requirements
3. **Use appropriate timing** - Consider immediate vs. batched vs. scheduled sends
4. **Implement preferences** - Give users control over notification types and channels
5. **Test thoroughly** - Verify across channels, devices, and with real data
6. **Monitor and optimize** - Track delivery, engagement, and user satisfaction metrics
