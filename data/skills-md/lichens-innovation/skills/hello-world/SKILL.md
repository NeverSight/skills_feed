---
name: hello-world
description: Simple skill to welcome user in ASCII Art Format with operating system information
---

## When to use

When the user says just "hello" or just "Hi"

## Instructions

1. Collect the OS information by calling the [collect-os-infos](scripts/collect-os-infos.cjs) script.
2. Display the OS information as a bullets list (- key: value) using the [template-os-infos.md](template-os-infos.md) file.
3. Collect the username by calling the [collect-username](scripts/collect-username.cjs) script.
4. Display the welcome message using the [template-welcome.md](template-welcome.md) file which will use the username retrieved at previous step.
