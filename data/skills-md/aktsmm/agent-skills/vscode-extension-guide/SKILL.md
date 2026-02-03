---
name: vscode-extension-guide
description: "Guide for creating VS Code extensions from scratch to Marketplace publication. Use when: (1) Creating a new VS Code extension, (2) Adding commands, keybindings, or settings to an extension, (3) Publishing to VS Code Marketplace, (4) Troubleshooting extension activation or packaging issues, (5) Building TreeView or Webview UI, (6) Setting up extension tests."
license: CC BY-NC-SA 4.0
metadata:
  author: yamapan (https://github.com/aktsmm)
---

# VS Code Extension Guide

Create, develop, and publish VS Code extensions.

## When to Use

- **VS Code extension**, **extension development**, **vscode plugin**
- Creating a new VS Code extension from scratch
- Adding commands, keybindings, or settings to an extension
- Publishing to VS Code Marketplace

## Quick Start

```bash
# Scaffold new extension (recommended)
npm install -g yo generator-code
yo code

# Or minimal manual setup
mkdir my-extension && cd my-extension
npm init -y && npm install -D typescript @types/vscode
```

## Project Structure

```
my-extension/
├── package.json          # Extension manifest (CRITICAL)
├── src/extension.ts      # Entry point
├── out/                  # Compiled JS (gitignore)
├── images/icon.png       # 128x128 PNG for Marketplace
└── .vscodeignore         # Exclude files from VSIX
```

## Building & Packaging

```bash
npm run compile      # Build once
npm run watch        # Watch mode (F5 to launch debug)
npx @vscode/vsce package   # Creates .vsix
```

## Done Criteria

- [ ] Extension activates without errors
- [ ] All commands registered and working
- [ ] Package size < 5MB (use `.vscodeignore`)
- [ ] README.md includes Marketplace/GitHub links

## Quick Troubleshooting

| Symptom               | Fix                                    |
| --------------------- | -------------------------------------- |
| Extension not loading | Add `activationEvents` to package.json |
| Command not found     | Match command ID in package.json/code  |
| Shortcut not working  | Remove `when` clause, check conflicts  |


| Topic               | Reference                                                            |
| ------------------- | -------------------------------------------------------------------- |
| AI Customization    | [references/ai-customization.md](references/ai-customization.md)     |
| Code Review Prompts | [references/code-review-prompts.md](references/code-review-prompts.md) |
| Code Samples        | [references/code-samples.md](references/code-samples.md)             |
| TreeView            | [references/treeview.md](references/treeview.md)                     |
| Webview             | [references/webview.md](references/webview.md)                       |
| Testing             | [references/testing.md](references/testing.md)                       |
| Publishing          | [references/publishing.md](references/publishing.md)                 |
| Troubleshooting     | [references/troubleshooting.md](references/troubleshooting.md)       |

## Best Practices

### 命名の一貫性

公開前にパッケージ名・設定キー・コマンド名を統一：

| 項目 | 例 |
|------|-----|
| パッケージ名 | `copilot-scheduler` |
| 設定キー | `copilotScheduler.enabled` |
| コマンドID | `copilotScheduler.createTask` |
| ビューID | `copilotSchedulerTasks` |

### 通知の一元管理

```typescript
type NotificationMode = "sound" | "silentToast" | "silentStatus";

function getNotificationMode(): NotificationMode {
  const config = vscode.workspace.getConfiguration("myExtension");
  return config.get<NotificationMode>("notificationMode", "sound");
}

function notifyInfo(message: string, timeoutMs = 4000): void {
  const mode = getNotificationMode();
  switch (mode) {
    case "silentStatus":
      vscode.window.setStatusBarMessage(message, timeoutMs);
      break;
    case "silentToast":
      void vscode.window.withProgress(
        { location: vscode.ProgressLocation.Notification, title: message },
        async () => {},
      );
      break;
    default:
      void vscode.window.showInformationMessage(message);
  }
}

function notifyError(message: string, timeoutMs = 6000): void {
  const mode = getNotificationMode();
  if (mode === "silentStatus") {
    vscode.window.setStatusBarMessage(`⚠ ${message}`, timeoutMs);
    console.error(message);
    return;
  }
  void vscode.window.showErrorMessage(message);
}
```

設定で `notificationMode` を選べるようにすることで、ユーザーが通知音を制御可能。
