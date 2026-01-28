---
name: se-dev-plugin
description: Plugin development for Space Engineers version 1
license: MIT
---
Do the one-time preparation steps described in `Prepare.md`, but only if the `Prepare.DONE` file is missing.

How to build custom tool script to conduct search and for other tasks:
- A Python virtual environment in this folder was made available by the preparation.
- Use this Python virtual environment to write short, targeted, reusable utility scripts as needed. 
  Build a catalog of such scripts in `UtilityScripts.md` next to this skill file. 
- Use `uv run script_name.py` in this folder (as CWD) to run your scripts.
- Use `busybox bash` to open a bash shell, which you can use easier, because it is close to UNIX.
- Alternatively use the Windows PowerShell if busybox would not work for something.
- On the Windows command line (cmd) (NOT on busybox!) use the `&` delimiter commands instead of `&&`.
- See the list of available Python packages in `pyproject.toml`.

Read the appropriate documents for further details:
- `Plugin.md` Plugin development (shared skills for both client and server)
- `ClientPlugin.md` Client plugin development (relevant on client side)
- `ServerPlugin.md` Server plugin development (relevant on server side)
- `Guide.md` Use this to answer questions about the plugin development process in general.
- `Publicizer.md` How to use the Krafs publicizer to access internal, protected or private members in the original game code (optional).
- `OtherPluginsAsExamples.md` How to look into the source code of other plugins as examples.

Plugins are released exclusively on the PluginHub. All plugins must be open source, since they are compiled on
the player's machine from the GitHub source revision identified by its PluginHub registration. Plugins are
reviewed for safety and security on submission, but only on a best effort basis, without any legal guarantees.
Plugins are running native code and can do anything.

Use the `se-dev-game-code` skill to search the game's decompiled code. You will need this to
understand how the game's internals work and how to interface with it and patch it properly.

General rules:
- Use `busybox bash` to open a bash shell, which you can use easier, because it is close to UNIX.
- Alternatively use the Windows PowerShell if busybox would not work for something.
- On the Windows command line (cmd) (NOT on busybox!) use the `&` delimiter commands instead of `&&`.

References:
- [Pulsar](https://github.com/SpaceGT/Pulsar) Plugin loader for Space Engineers
- [Pulsar Installer](https://github.com/StarCpt/Pulsar-Installer) Installer for Pulsar on Windows
- [PluginHub](https://github.com/StarCpt/PluginHub/) Public plugin registry for Pulsar
