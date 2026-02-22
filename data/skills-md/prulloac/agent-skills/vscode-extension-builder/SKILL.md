---
name: vscode-extension-builder
description: Guide for creating Visual Studio Code extensions/plugins. Use when users want to build VS Code extensions, add functionality to VS Code, create language support, add themes, build webviews, implement debuggers, or any VS Code plugin development task. Helps navigate VS Code Extension API documentation and provides guidance on extension capabilities, project setup, and best practices.
---

# VS Code Extension Builder

## Overview

This skill guides the development of Visual Studio Code extensions by helping navigate the extensive VS Code Extension API documentation and providing structured guidance for common extension development tasks.

## Documentation Base

All VS Code extension development guidance is based on the official documentation at:
**https://code.visualstudio.com/api**

When assisting users, fetch relevant documentation pages to provide accurate, up-to-date information.

### Official Documentation References
- **Your First Extension**: https://code.visualstudio.com/api/get-started/your-first-extension
  - Step-by-step guide for scaffolding and running your first extension
  - Yeoman generator setup and project creation
  - Quick iteration with Extension Development Host
  - Essential debugging and testing techniques
  
- **Extension Anatomy**: https://code.visualstudio.com/api/get-started/extension-anatomy
  - File structure and configuration explanation
  - `package.json` manifest details
  - Extension entry point (`activate` and `deactivate` functions)
  - Implicit activation events (VS Code 1.74.0+)
  
- **Wrapping Up**: https://code.visualstudio.com/api/get-started/wrapping-up
  - Next steps after creating your first extension
  - Navigation to specialized guides and samples
  - Testing, publishing, and CI/CD resources

## Core Workflow

### 1. Understand User Intent

First, determine what the user wants to accomplish with their extension:

**Common extension types:**
- **Commands & UI extensions** - Add commands, menus, keybindings, status bar items
- **Language support** - Syntax highlighting, IntelliSense, diagnostics, formatting
- **Themes** - Color themes, file icon themes, product icon themes
- **Webviews** - Custom UI panels with HTML/CSS/JavaScript
- **Debuggers** - Debug adapter integrations
- **Source control** - SCM provider integrations
- **Tree views** - Custom sidebar explorers
- **AI/Chat extensions** - Chat participants, language model tools
- **Testing** - Test provider integrations
- **Notebook support** - Custom notebook renderers

### 2. Fetch Relevant Documentation

Based on the user's intent, fetch the appropriate documentation:

**For getting started (Getting Started Track):**
- Your First Extension: https://code.visualstudio.com/api/get-started/your-first-extension
- Extension Anatomy: https://code.visualstudio.com/api/get-started/extension-anatomy
- Wrapping Up: https://code.visualstudio.com/api/get-started/wrapping-up

**For capability planning:**
- Extension Capabilities Overview: https://code.visualstudio.com/api/extension-capabilities/overview
- Common Capabilities: https://code.visualstudio.com/api/extension-capabilities/common-capabilities
- Extending Workbench: https://code.visualstudio.com/api/extension-capabilities/extending-workbench
- Theming: https://code.visualstudio.com/api/extension-capabilities/theming

**For specific features, use the extension guides:**
- Overview: https://code.visualstudio.com/api/extension-guides/overview
- AI features: https://code.visualstudio.com/api/extension-guides/ai/ai-extensibility-overview
  - Language Model Tool: https://code.visualstudio.com/api/extension-guides/ai/tools
  - Chat Participant: https://code.visualstudio.com/api/extension-guides/ai/chat
  - MCP Dev Guide: https://code.visualstudio.com/api/extension-guides/ai/mcp
- Commands: https://code.visualstudio.com/api/extension-guides/command
- Webviews: https://code.visualstudio.com/api/extension-guides/webview
- Tree views: https://code.visualstudio.com/api/extension-guides/tree-view
- Language features: https://code.visualstudio.com/api/language-extensions/overview
- Debuggers: https://code.visualstudio.com/api/extension-guides/debugger-extension
- Themes: https://code.visualstudio.com/api/extension-guides/color-theme
- File Icon Theme: https://code.visualstudio.com/api/extension-guides/file-icon-theme
- Product Icon Theme: https://code.visualstudio.com/api/extension-guides/product-icon-theme
- Custom Editors: https://code.visualstudio.com/api/extension-guides/custom-editors
- Notebooks: https://code.visualstudio.com/api/extension-guides/notebook
- Virtual Documents: https://code.visualstudio.com/api/extension-guides/virtual-documents
- Virtual Workspaces: https://code.visualstudio.com/api/extension-guides/virtual-workspaces
- Web Extensions: https://code.visualstudio.com/api/extension-guides/web-extensions
- Workspace Trust: https://code.visualstudio.com/api/extension-guides/workspace-trust
- Task Provider: https://code.visualstudio.com/api/extension-guides/task-provider
- Source Control: https://code.visualstudio.com/api/extension-guides/scm-provider
- Markdown Extension: https://code.visualstudio.com/api/extension-guides/markdown-extension
- Test Extension: https://code.visualstudio.com/api/extension-guides/testing
- Custom Data Extension: https://code.visualstudio.com/api/extension-guides/custom-data-extension
- Telemetry: https://code.visualstudio.com/api/extension-guides/telemetry

**For UX best practices:**
- UX Guidelines Overview: https://code.visualstudio.com/api/ux-guidelines/overview
- Activity Bar: https://code.visualstudio.com/api/ux-guidelines/activity-bar
- Sidebars: https://code.visualstudio.com/api/ux-guidelines/sidebars
- Command Palette: https://code.visualstudio.com/api/ux-guidelines/command-palette
- Status Bar: https://code.visualstudio.com/api/ux-guidelines/status-bar
- Quick Picks: https://code.visualstudio.com/api/ux-guidelines/quick-picks
- Context Menus: https://code.visualstudio.com/api/ux-guidelines/context-menus
- Webviews: https://code.visualstudio.com/api/ux-guidelines/webviews

**For API reference:**
- VS Code API: https://code.visualstudio.com/api/references/vscode-api
- Contribution Points: https://code.visualstudio.com/api/references/contribution-points
- Activation Events: https://code.visualstudio.com/api/references/activation-events
- Extension Manifest: https://code.visualstudio.com/api/references/extension-manifest
- Built-In Commands: https://code.visualstudio.com/api/references/commands
- When Clause Contexts: https://code.visualstudio.com/api/references/when-clause-contexts
- Theme Color: https://code.visualstudio.com/api/references/theme-color
- Document Selector: https://code.visualstudio.com/api/references/document-selector

**For testing and publishing:**
- Testing Extensions: https://code.visualstudio.com/api/working-with-extensions/testing-extension
- Publishing Extensions: https://code.visualstudio.com/api/working-with-extensions/publishing-extension
- Bundling Extensions: https://code.visualstudio.com/api/working-with-extensions/bundling-extension
- Continuous Integration: https://code.visualstudio.com/api/working-with-extensions/continuous-integration

**For advanced topics:**
- Extension Host: https://code.visualstudio.com/api/advanced-topics/extension-host
- Remote Development: https://code.visualstudio.com/api/advanced-topics/remote-extensions
- Using Proposed API: https://code.visualstudio.com/api/advanced-topics/using-proposed-api
- Language Server Extension Guide: https://code.visualstudio.com/api/language-extensions/language-server-extension-guide

### 3. Guide Implementation

After fetching documentation, provide step-by-step guidance:

1. **Project setup** - Use Yeoman generator or guide manual setup
2. **Package.json configuration** - Help define contribution points
3. **Core implementation** - Provide code guidance based on documentation
4. **Testing** - Help set up extension testing
5. **Debugging** - Guide F5 debugging setup
6. **Publishing** - Assist with vsce packaging

## Quick Start Pattern

For new extensions, always start with:

```bash
# Install dependencies (if needed)
npm install -g yo generator-code

# Or use npx without global install
npx --package yo --package generator-code -- yo code
```

Guide users through the prompts based on their extension type.

## Key Concepts to Explain

### Activation Events

When extensions are loaded (see https://code.visualstudio.com/api/references/activation-events):
- `onCommand:` - When a command is invoked
- `onLanguage:` - When a file of specific language is opened
- `onView:` - When a view is expanded
- `workspaceContains:` - When workspace matches a pattern
- `onDebug` - When debug session starts
- `*` - On startup (use sparingly, impacts performance)

**Important:** Starting with VS Code 1.74.0, commands declared in `contributes.commands` automatically activate extensions without explicit `onCommand` entries.

### Contribution Points

Static declarations in `package.json` that extend VS Code (see https://code.visualstudio.com/api/references/contribution-points):
- `commands` - Define commands available in Command Palette
- `menus` - Add commands to UI menus
- `keybindings` - Define keyboard shortcuts
- `views` - Create custom sidebar views
- `viewsContainers` - Define view containers (sidebars, panels)
- `configuration` - Define configuration settings
- `languages` - Register new language support
- `grammars` - Define syntax highlighting rules
- `themes` - Register color themes
- `debuggers` - Register debug adapters
- `snippets` - Define code snippets
- `taskDefinitions` - Define custom task types
- `semanticTokenTypes/Modifiers` - Extend semantic highlighting
- `walkthroughs` - Create interactive extension walkthroughs
- `notebookProvider` - Register notebook renderers
- `customEditors` - Register custom editor providers

### Manifest Best Practices

For optimal marketplace presentation:
- Use `displayName` and `description` clearly and concisely
- Set `categories` from allowed values for better discoverability
- Provide `icon` (PNG, 128x128 minimum) and `galleryBanner` for visual appeal
- Include `repository`, `bugs`, and `homepage` in resources section
- Use `keywords` array (up to 30) for search optimization
- Set appropriate `engines.vscode` version (don't use `*`)
- Configure `extensionPack` for bundling related extensions
- Declare `extensionDependencies` if your extension relies on others
- Mark `capabilities` for `untrustedWorkspaces` and `virtualWorkspaces` support

For pricing and availability:
- Use `pricing` field (Free/Trial)
- Set `preview: true` for beta extensions
- Use `preview` for extensions not ready for production

### Extension Anatomy

Understanding the core components of VS Code extensions:

**File Structure:**
```
.
├── .vscode
│   ├── launch.json     # Debug configuration for F5 debugging
│   └── tasks.json      # Build task configuration (TypeScript compilation)
├── .gitignore
├── README.md
├── src
│   └── extension.ts    # Main extension code (entry point)
├── package.json        # Extension manifest
└── tsconfig.json       # TypeScript configuration
```

**package.json - Critical Fields:**
- `name` - Extension identifier (lowercase, no spaces)
- `displayName` - Human-readable name for Marketplace
- `version` - SemVer version number
- `publisher` - Publisher identifier
- `description` - Short description of functionality
- `engines.vscode` - Minimum VS Code version (e.g., `"^1.80.0"`)
- `main` - Entry point to extension (compiled JavaScript)
- `browser` - Entry point for Web extensions
- `activationEvents` - When the extension is activated
- `contributes` - Static declarations of extension capabilities
- `categories` - Marketplace categories for discoverability
- `icon` - Extension icon (128x128 pixels minimum)
- `license` - License information
- `repository` - Repository URL

**Extension Entry File (extension.ts/js):**
- `activate(context)` - Called when extension activates; setup your extension here
- `deactivate()` - Called when extension deactivates; clean up resources here
- Disposables must be added to `context.subscriptions` for proper cleanup

**Key Modern Features (VS Code 1.74.0+):**
- Implicit activation events: Commands declared in `contributes.commands` automatically activate extensions
- No need for explicit `onCommand` activation events
- Reduces startup impact by lazy-loading extensions only when needed

## Common Patterns

## Testing Your Extension

Modern testing approach using the VS Code Test CLI:

```bash
# Install test dependencies
npm install --save-dev @vscode/test-cli @vscode/test-electron
```

**Configuration (.vscode-test.js):**
```javascript
const { defineConfig } = require('@vscode/test-cli');
module.exports = defineConfig({ files: 'out/test/**/*.test.js' });
```

**Run tests:**
```bash
npm test
```

**Key testing features:**
- Extensions run in Extension Development Host with full API access
- Mocha test framework by default
- Can debug tests with VS Code's debugger
- Support for multiple test configurations
- Workspace folder support during testing
- CI/CD integration ready

See https://code.visualstudio.com/api/working-with-extensions/testing-extension for detailed setup.

## Debugging Your Extension

**Quick Debug with F5:**
1. Open extension project in VS Code
2. Press F5 or run **Debug: Start Debugging** from Command Palette
3. Extension Development Host window opens with your extension loaded
4. Set breakpoints by clicking line numbers
5. Use Debug Console to evaluate expressions
6. Use Run and Debug panel to inspect variables

**Key debugging features:**
- Full Node.js debugging capabilities
- Hover over variables to see values
- Watch expressions and call stacks
- VS Code's built-in debugger works with extensions

## Modern VS Code Features (1.74.0+)

### Implicit Command Activation
- Commands in `contributes.commands` auto-activate the extension
- Reduces explicit configuration needed
- Improves extension startup time

### Web Extensions
- Extensions can run in browser-based VS Code (code.visualstudio.com)
- Use `browser` field in package.json
- See https://code.visualstudio.com/api/extension-guides/web-extensions

### Workspace Trust
- Extensions can declare trustworthiness requirements
- Respect user's workspace trust decisions
- See https://code.visualstudio.com/api/extension-guides/workspace-trust

### AI and Language Model Integration
- Chat Participants for AI interactions
- Language Model Tool integration
- MCP (Model Context Protocol) support
- See https://code.visualstudio.com/api/extension-guides/ai/ai-extensibility-overview

### Extension Marketplace Features
- `extensionPack` for bundling extensions
- `extensionDependencies` for runtime dependencies
- `extensionKind` for remote/local execution preference
- Pricing models (Free/Trial)
- Preview flag for beta releases

## Common Patterns and Examples

### Registering a Command
```typescript
import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
    // Register a command - no explicit onCommand needed (VS Code 1.74.0+)
    let disposable = vscode.commands.registerCommand('extension.commandName', () => {
        vscode.window.showInformationMessage('Hello World!');
    });
    
    context.subscriptions.push(disposable);
}

export function deactivate() {}
```

**In package.json:**
```json
{
  "contributes": {
    "commands": [
      {
        "command": "extension.commandName",
        "title": "My Command"
      }
    ]
  }
}
```

### Creating a Tree View
Provide hierarchical data in sidebar:
- Implement `TreeDataProvider<T>`
- Register with `createTreeView()`
- Use `onDidChangeTreeData` for updates
- See https://code.visualstudio.com/api/extension-guides/tree-view

### Building a Webview
Custom HTML UI for complex interfaces:
- Create webview panels with `createWebviewPanel()`
- Communicate via `postMessage()` API
- Manage content security policy properly
- See https://code.visualstudio.com/api/extension-guides/webview

### Language Server Protocol
For rich language support:
- Integrate Language Server Protocol (LSP)
- Use `vscode-languageclient` npm package
- Provide IntelliSense, diagnostics, formatting
- See https://code.visualstudio.com/api/language-extensions/language-server-extension-guide

### Storing Data
- **Global**: `context.globalState.update(key, value)`
- **Workspace**: `context.workspaceState.update(key, value)`
- **Configuration**: `vscode.workspace.getConfiguration()`

### Showing UI Elements
```typescript
// Information message
vscode.window.showInformationMessage('Message');

// Quick pick for selection
const pick = await vscode.window.showQuickPick(['Option 1', 'Option 2']);

// Input box for text
const input = await vscode.window.showInputBox({ prompt: 'Enter text' });

// Progress indication
await vscode.window.withProgress({
    location: vscode.ProgressLocation.Notification,
    title: 'Processing...'
}, async (progress) => {
    // Long-running operation
});
```

## Documentation Navigation Strategy

1. **Start broad** - Fetch overview pages to understand scope
2. **Go specific** - Fetch detailed guides for the exact feature needed
3. **Check references** - Fetch API references for specific types/methods
4. **Review examples** - Point users to sample extensions at https://github.com/microsoft/vscode-extension-samples

## Extension Capabilities and Restrictions

### What Extensions Can Do
- Extend VS Code UI (sidebars, panels, status bar, decorations, etc.)
- Add commands and keybindings
- Create custom views with TreeView API
- Build custom UI with Webview API
- Provide language features (IntelliSense, diagnostics, formatting, etc.)
- Integrate debuggers and test frameworks
- Add themes and icons
- Register configuration settings
- Contribute walkthroughs and tutorials
- Integrate with Source Control providers
- Build custom editors and notebooks

### Important Restrictions
- **No DOM access** - Cannot access VS Code's internal DOM directly
- **No custom CSS** - Cannot inject custom stylesheets into VS Code UI
- **Runs in Extension Host** - Extensions run in a separate process
- **Must use VS Code API** - Cannot use undocumented internal APIs
- **Performance constraints** - Heavy operations impact all extensions

**Rationale:** These restrictions ensure stability, performance, and security while allowing VS Code to evolve freely without breaking extensions.

### Best Practices

1. **Minimal Startup Impact**
   - Use activation events wisely; avoid `*` unless necessary
   - Lazy-load dependencies and APIs
   - Rely on implicit activation for declared commands (VS Code 1.74.0+)

2. **Resource Management**
   - Always dispose of resources in `deactivate()` or add to `context.subscriptions`
   - Clean up event listeners, file watchers, and language clients
   - Prevent memory leaks by removing references

3. **Type Safety**
   - Use TypeScript for better developer experience
   - Install correct `@types/vscode` version matching `engines.vscode`
   - Enable strict TypeScript compilation

4. **Error Handling**
   - Catch and handle errors in command implementations
   - Provide meaningful error messages to users
   - Log errors to extension output channel for debugging

5. **Performance**
   - Bundle extensions for production (webpack/esbuild)
   - Use Tree Data Provider for large datasets with pagination
   - Minimize async operations in activation

6. **UX Guidelines**
   - Follow https://code.visualstudio.com/api/ux-guidelines/overview
   - Use standard notification types: information, warning, error
   - Implement quick picks for user selections
   - Respect workspace trust settings

7. **Testing**
   - Write integration tests using VS Code's test runner
   - Use https://code.visualstudio.com/api/working-with-extensions/testing-extension
   - Run tests with `npm run test` (Mocha-based)
   - Use `@vscode/test-cli` for modern test setup

8. **Publishing**
   - Follow marketplace guidelines at https://code.visualstudio.com/api/working-with-extensions/publishing-extension
   - Include comprehensive README with examples
   - Use `vsce` (Visual Studio Code Extension Manager) for packaging
   - Implement CI/CD with GitHub Actions or Azure DevOps

## Progressive Assistance Levels

### For Absolute Beginners
**Goal:** Get them building and debugging quickly

1. Guide through "Your First Extension" walkthrough
2. Explain the three core concepts:
   - **Activation Events**: When extension loads
   - **Contribution Points**: What the extension contributes to VS Code
   - **VS Code API**: How to interact with VS Code
3. Walk through Yeoman scaffolding step-by-step
4. Show how to modify the extension and test with F5
5. Explain package.json basics (name, version, main, engines)
6. Show how to register and run a command

**Resources:**
- Start with: https://code.visualstudio.com/api/get-started/your-first-extension
- Then: https://code.visualstudio.com/api/get-started/extension-anatomy

### For Intermediate Users
**Goal:** Build feature-rich extensions independently

1. Fetch specific extension guide documentation
2. Explain API patterns and best practices
3. Guide through VS Code API exploration
4. Help with:
   - Configuration settings
   - File system operations
   - Tree views and sidebars
   - Webview implementation
   - Language features
5. Assist with debugging techniques and issue diagnosis
6. Help set up and run extension tests

**Resources:**
- Extension Guides: https://code.visualstudio.com/api/extension-guides/overview
- VS Code API Reference: https://code.visualstudio.com/api/references/vscode-api
- Testing: https://code.visualstudio.com/api/working-with-extensions/testing-extension
- UX Guidelines: https://code.visualstudio.com/api/ux-guidelines/overview

### For Advanced Users
**Goal:** Build complex, production-grade extensions

1. Point to proposed APIs for experimental features
2. Help with Language Server Protocol integration
3. Guide multi-extension architecture
4. Assist with:
   - Remote and web extension support
   - Custom editors and notebooks
   - Advanced tree view providers
   - Semantic highlighting
   - Debug adapter integration
5. Help prepare for Marketplace publishing
6. Advise on CI/CD setup

**Resources:**
- Advanced Topics: https://code.visualstudio.com/api/advanced-topics/extension-host
- Remote Extensions: https://code.visualstudio.com/api/advanced-topics/remote-extensions
- Proposed API: https://code.visualstudio.com/api/advanced-topics/using-proposed-api
- Publishing: https://code.visualstudio.com/api/working-with-extensions/publishing-extension
- CI/CD: https://code.visualstudio.com/api/working-with-extensions/continuous-integration

## Reference Documentation

For comprehensive guides on specific extension types and advanced patterns, see:
- [Official Documentation Map](references/official-docs-map.md) - Complete map of VS Code Extension API documentation (https://code.visualstudio.com/api)
- [Extension Development Guide](references/extension-guide.md) - Detailed guide for common extension patterns
- [API Quick Reference](references/api-quick-reference.md) - Quick lookup for common VS Code APIs

Read these references when users need deeper guidance on specific topics or navigation help through the official documentation.
