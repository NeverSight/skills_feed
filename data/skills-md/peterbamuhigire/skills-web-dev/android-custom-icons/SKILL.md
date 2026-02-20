---
name: android-custom-icons
description: "Use custom PNG icons in Android apps instead of library icons. Enforces placeholder usage, standard directory, and PROJECT_ICONS.md tracking. Applies to Jetpack Compose and XML layouts."
---

# Android Custom PNG Icons

Use **custom PNG icons** in Android apps instead of icon libraries. Whenever UI code includes an icon, the agent must use a PNG placeholder and update `PROJECT_ICONS.md` so the icon list is tracked for later upload.

## Scope

**Use for:** All Android UI generation (Compose and XML).

**Do not use:** Material Icons, Font Awesome, or any bundled icon libraries unless the user explicitly asks for them.

## Standard Icon Directory

- **Primary location:** `app/src/main/res/drawable/`
- **If you need 1:1 pixels (no scaling):** `app/src/main/res/drawable-nodpi/`

> If multiple densities are provided later, place them in `drawable-hdpi`, `drawable-xhdpi`, `drawable-xxhdpi`, `drawable-xxxhdpi` using the same file name.

## File Naming Rules (Required)

- Lowercase letters, numbers, underscores only
- No hyphens, no spaces, no uppercase
- File name becomes `R.drawable.<name>`

**Examples:**

- `cancel.png` -> `R.drawable.cancel`
- `chart.png` -> `R.drawable.chart`
- `filter.png` -> `R.drawable.filter`

## Compose Usage (Required)

```kotlin
Icon(
    painter = painterResource(R.drawable.cancel),
    contentDescription = "Cancel",
    modifier = Modifier.size(24.dp)
)
```

```kotlin
Image(
    painter = painterResource(R.drawable.chart),
    contentDescription = null,
    modifier = Modifier.size(48.dp)
)
```

## XML Usage (Required)

```xml
<ImageView
    android:layout_width="24dp"
    android:layout_height="24dp"
    android:src="@drawable/cancel"
    android:contentDescription="@string/cancel" />
```

## PROJECT_ICONS.md (Required)

Maintain a `PROJECT_ICONS.md` file at the **project root**. Every time code introduces a new icon placeholder, **append a row**.

### Template

```markdown
# Project Icons

Standard path: app/src/main/res/drawable/

| Icon File  | Usage        | Screen/Component  | Status      | Notes            |
| ---------- | ------------ | ----------------- | ----------- | ---------------- |
| cancel.png | Close action | EditProfileTopBar | placeholder | Provide 24dp PNG |
```

### Update Rules

- Add a row **every time** a new icon placeholder is referenced in code.
- Use the exact file name used in code (e.g., `cancel.png`).
- Keep status as `placeholder` until the PNG is provided.

## Mandatory Checklist (Per UI Generation)

- [ ] Use PNG placeholders only (no icon libraries)
- [ ] Use `painterResource(R.drawable.<name>)` or `@drawable/<name>`
- [ ] Add or update `PROJECT_ICONS.md`
- [ ] Placeholders use valid Android resource naming
