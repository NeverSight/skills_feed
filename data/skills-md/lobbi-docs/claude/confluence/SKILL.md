---
name: confluence
description: Confluence documentation including pages, spaces, templates, and Atlassian integration. Activate for wiki pages, documentation, knowledge bases, and team collaboration.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Confluence Skill

Provides comprehensive Confluence documentation capabilities for the Golden Armada AI Agent Fleet Platform.

## When to Use This Skill

Activate this skill when working with:
- Documentation pages
- Space management
- Templates and blueprints
- Knowledge base creation
- Confluence API integration

## Confluence API Quick Reference

### Authentication
\`\`\`python
from atlassian import Confluence

confluence = Confluence(
    url='https://your-domain.atlassian.net',
    username='email@example.com',
    password='API_TOKEN',
    cloud=True
)
\`\`\`

### Page Operations

\`\`\`python
# Create page
page = confluence.create_page(
    space='GA',
    title='Agent Architecture',
    body='<h1>Overview</h1><p>Architecture documentation...</p>',
    parent_id=12345  # Optional parent page
)

# Get page
page = confluence.get_page_by_title(
    space='GA',
    title='Agent Architecture',
    expand='body.storage,version'
)

# Get page by ID
page = confluence.get_page_by_id(
    page_id=12345,
    expand='body.storage,version'
)

# Update page
confluence.update_page(
    page_id=12345,
    title='Agent Architecture v2',
    body='<h1>Updated Overview</h1><p>New content...</p>'
)

# Delete page
confluence.remove_page(page_id=12345)

# Get page content
content = confluence.get_page_by_id(page_id, expand='body.storage')
html_content = content['body']['storage']['value']
\`\`\`

### Space Operations

\`\`\`python
# Create space
space = confluence.create_space(
    space_key='GA',
    space_name='Golden Armada',
    description='AI Agent Fleet Platform documentation'
)

# Get space
space = confluence.get_space('GA', expand='homepage')

# Get all pages in space
pages = confluence.get_all_pages_from_space(
    space='GA',
    start=0,
    limit=100,
    expand='body.storage'
)
\`\`\`

### Search

\`\`\`python
# CQL search
results = confluence.cql(
    'space = GA AND type = page AND text ~ "agent"',
    limit=25
)

# Search pages
results = confluence.search(
    query='agent architecture',
    space='GA',
    type='page'
)
\`\`\`

## Page Templates

### Architecture Document
\`\`\`html
<h1>System Architecture</h1>

<ac:structured-macro ac:name="toc">
  <ac:parameter ac:name="printable">true</ac:parameter>
  <ac:parameter ac:name="style">disc</ac:parameter>
  <ac:parameter ac:name="maxLevel">3</ac:parameter>
</ac:structured-macro>

<h2>Overview</h2>
<p>Brief description of the system...</p>

<h2>Components</h2>
<ac:structured-macro ac:name="panel">
  <ac:parameter ac:name="title">Key Components</ac:parameter>
  <ac:rich-text-body>
    <ul>
      <li><strong>Component 1</strong> - Description</li>
      <li><strong>Component 2</strong> - Description</li>
    </ul>
  </ac:rich-text-body>
</ac:structured-macro>

<h2>Architecture Diagram</h2>
<ac:image>
  <ri:attachment ri:filename="architecture.png"/>
</ac:image>

<h2>Data Flow</h2>
<p>Description of data flow...</p>

<h2>Security Considerations</h2>
<ac:structured-macro ac:name="warning">
  <ac:rich-text-body>
    <p>Security notes...</p>
  </ac:rich-text-body>
</ac:structured-macro>
\`\`\`

### API Documentation
\`\`\`html
<h1>API Reference</h1>

<h2>Authentication</h2>
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">bash</ac:parameter>
  <ac:plain-text-body><![CDATA[
curl -X POST https://api.example.com/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "pass"}'
  ]]></ac:plain-text-body>
</ac:structured-macro>

<h2>Endpoints</h2>

<h3>GET /agents</h3>
<p>List all agents.</p>

<ac:structured-macro ac:name="expand">
  <ac:parameter ac:name="title">Example Response</ac:parameter>
  <ac:rich-text-body>
    <ac:structured-macro ac:name="code">
      <ac:parameter ac:name="language">json</ac:parameter>
      <ac:plain-text-body><![CDATA[
{
  "agents": [
    {"id": "1", "name": "Agent 1", "status": "active"}
  ]
}
      ]]></ac:plain-text-body>
    </ac:structured-macro>
  </ac:rich-text-body>
</ac:structured-macro>
\`\`\`

### Meeting Notes
\`\`\`html
<h1>Meeting Notes: <ac:placeholder>Meeting Title</ac:placeholder></h1>

<ac:structured-macro ac:name="info">
  <ac:rich-text-body>
    <p><strong>Date:</strong> <ac:placeholder>Date</ac:placeholder></p>
    <p><strong>Attendees:</strong> <ac:placeholder>Names</ac:placeholder></p>
  </ac:rich-text-body>
</ac:structured-macro>

<h2>Agenda</h2>
<ul>
  <li>Topic 1</li>
  <li>Topic 2</li>
</ul>

<h2>Discussion</h2>
<p>Notes from discussion...</p>

<h2>Action Items</h2>
<ac:task-list>
  <ac:task>
    <ac:task-status>incomplete</ac:task-status>
    <ac:task-body>Action item 1 <ac:link><ri:user ri:userkey="assignee"/></ac:link></ac:task-body>
  </ac:task>
</ac:task-list>

<h2>Next Steps</h2>
<p>Follow-up items...</p>
\`\`\`

## Macros Reference

### Common Macros
\`\`\`html
<!-- Table of Contents -->
<ac:structured-macro ac:name="toc"/>

<!-- Code Block -->
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">python</ac:parameter>
  <ac:plain-text-body><![CDATA[print("Hello")]]></ac:plain-text-body>
</ac:structured-macro>

<!-- Info Panel -->
<ac:structured-macro ac:name="info">
  <ac:rich-text-body><p>Info text</p></ac:rich-text-body>
</ac:structured-macro>

<!-- Warning Panel -->
<ac:structured-macro ac:name="warning">
  <ac:rich-text-body><p>Warning text</p></ac:rich-text-body>
</ac:structured-macro>

<!-- Expand (Collapsible) -->
<ac:structured-macro ac:name="expand">
  <ac:parameter ac:name="title">Click to expand</ac:parameter>
  <ac:rich-text-body><p>Hidden content</p></ac:rich-text-body>
</ac:structured-macro>

<!-- Status Badge -->
<ac:structured-macro ac:name="status">
  <ac:parameter ac:name="colour">Green</ac:parameter>
  <ac:parameter ac:name="title">COMPLETED</ac:parameter>
</ac:structured-macro>

<!-- Jira Issue Link -->
<ac:structured-macro ac:name="jira">
  <ac:parameter ac:name="key">GA-123</ac:parameter>
</ac:structured-macro>
\`\`\`

## Golden Armada Commands

\`\`\`bash
# Publish to Confluence
/confluence-publish --space GA --title "Agent API Docs" --file docs/api.md

# Update page
/confluence-update --page-id 12345 --file docs/updated.md

# Sync documentation
/atlassian-sync --confluence --space GA
\`\`\`

## Best Practices

1. **Use templates** for consistent documentation
2. **Organize with page hierarchy** (parent/child pages)
3. **Include diagrams** for complex concepts
4. **Link to Jira issues** for traceability
5. **Version important pages** with labels
6. **Use macros** for dynamic content
