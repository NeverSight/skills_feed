---
name: workflow-automation
description: This skill should be used when users need help designing content workflows, creating process documentation, implementing automation rules, designing approval processes, or optimizing content pipelines. It activates when users ask about workflow design, process documentation, automation, approval workflows, or content pipeline optimization.
location: .claude/skills/content/workflow-automation/
---

# Content Workflow Automation

## Overview

This skill enables Claude to help users design and implement content workflows, create process documentation, suggest automation rules, document approval processes, and optimize content pipelines for efficiency and quality.

## When to Use This Skill

This skill activates automatically when users:

- Ask about workflow design or content processes
- Need help documenting content workflows
- Request automation suggestions or implementation
- Want to design approval workflows
- Need content pipeline optimization
- Ask about process improvement or efficiency

## Core Capabilities

### 1. Design Content Workflows

To design effective content workflows:

1. **Understand Current Process**

   - Map existing content creation process
   - Identify workflow steps and stakeholders
   - Document current pain points and bottlenecks

2. **Design Optimal Workflow**

   - Create workflow structure: Input → Processing → Output
   - Define workflow steps and decision points
   - Identify automation opportunities
   - Design workflow for efficiency and quality

3. **Document Workflow**
   - Create visual workflow diagrams
   - Document step-by-step procedures
   - Define roles and responsibilities
   - Specify tools and integrations needed

**Example User Request:**
"Design a content workflow for my team that includes approval steps"

**Integration (discover from project):**

- Content Management Platform: Store workflow documentation
- Publishing Platform: Implement workflow automation
- Content Creation Tools: Integrate workflow steps into content generation

### 2. Create Process Documentation

To create comprehensive process documentation:

1. **Document Content Processes**

   - Content creation process
   - Content approval process
   - Content publishing process
   - Content optimization process

2. **Create Visual Flowcharts**

   - Convert written procedures into flowcharts
   - Visualize complex processes
   - Make processes easier to follow and share

3. **Maintain Documentation**
   - Keep documentation up-to-date
   - Version control for process changes
   - Share documentation with team

**Example User Request:**
"Create a flowchart for my content creation process"

**Integration (discover from project):**

- Content Management Platform: Store process documentation
- Team collaboration features: Share workflows with team

### 3. Automation Rule Suggestions

To suggest and implement automation rules:

1. **Identify Automation Opportunities**

   - Review workflow for repetitive tasks
   - Identify manual steps that can be automated
   - Assess automation feasibility and impact

2. **Design Automation Rules**

   - Define trigger conditions
   - Specify automation actions
   - Design error handling and fallbacks

3. **Implement Automation**
   - Configure automation rules in content platform (discover from project)
   - Test automation workflows
   - Monitor automation performance

**Example User Request:**
"What parts of my content workflow can be automated?"

**Integration (discover from project):**

- Publishing Platform: Automated scheduling and distribution
- Content Management Platform: Automated content organization
- Analytics Platform: Automated report generation

### 4. Approval Process Design

To design content approval workflows:

1. **Define Approval Requirements**

   - Identify approval stakeholders
   - Define approval criteria
   - Specify approval workflow steps

2. **Design Approval Workflow**

   - Create approval process structure
   - Define roles and permissions
   - Design approval notifications and reminders

3. **Implement Approval System**
   - Configure approval workflow in content platform (discover from project)
   - Set up notifications and alerts
   - Track approval status and history

**Example User Request:**
"Design an approval workflow where content needs manager approval before publishing"

**Integration (discover from project):**

- Content Management Platform: Approval workflow management
- Mobile App: Approval notifications and actions
- Publishing Platform: Approval-gated publishing

### 5. Content Pipeline Optimization

To optimize content pipelines for efficiency:

1. **Analyze Current Pipeline**

   - Map content pipeline from ideation to publishing
   - Identify bottlenecks and inefficiencies
   - Measure pipeline performance metrics

2. **Optimize Pipeline**

   - Remove unnecessary steps
   - Parallelize independent tasks
   - Automate repetitive processes
   - Optimize resource allocation

3. **Monitor and Improve**
   - Track pipeline performance
   - Identify optimization opportunities
   - Continuously improve workflow efficiency

**Example User Request:**
"Help me optimize my content pipeline to reduce time from ideation to publishing"

**Integration (discover from project):**

- All Platforms: Optimize workflows across platform
- Analytics Platform: Track pipeline performance metrics
- Content Management Platform: Monitor workflow efficiency

## Project Context Discovery

**Before designing workflows, discover the project's context:**

1. **Scan Project Documentation:**
   - Check `.agent/SYSTEM/ARCHITECTURE.md` for workflow architecture
   - Review `.agent/SOP/` for existing process documentation
   - Look for workflow diagrams or process maps

2. **Identify Workflow Components:**
   - Scan codebase for content creation tools
   - Look for publishing/distribution systems
   - Check for analytics integrations
   - Review approval/notification systems

**Common Content Workflow:**

```
Trend Detection (Extension) → Content Generation (Creation Tools) →
Distribution (Publishing Platform) → Analytics (Analytics Platform) → Optimization
```

**Workflow Components:**

- Browser Extension: Trend discovery and bookmarking
- Content Creation Tools: AI content generation
- Publishing Platform: Multi-platform scheduling and distribution
- Analytics Platform: Performance tracking and reporting
- Content Management Platform: Content library and organization

**Automation Opportunities:**

- Automated content scheduling
- Automated analytics refresh (cron job)
- Automated report generation
- Automated content organization
- Automated approval notifications

## Best Practices

1. **Start Simple**: Begin with basic workflows and add complexity gradually
2. **Document Everything**: Maintain clear documentation for all workflows
3. **Test Thoroughly**: Test automation rules before full implementation
4. **Monitor Performance**: Track workflow efficiency and optimize continuously
5. **User-Centric Design**: Design workflows that serve users, not just automate tasks

## Resources

### references/

- `workflow-design-guide.md`: Best practices for workflow design
- `automation-patterns.md`: Common automation patterns and examples
- `approval-workflow-examples.md`: Approval workflow templates and examples

### assets/

- `workflow-template.md`: Template for documenting workflows
- `process-flowchart-template.md`: Template for creating process flowcharts
- `automation-rule-template.md`: Template for defining automation rules
