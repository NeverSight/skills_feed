---
name: se-dev-mod
description: Mod development for Space Engineers version 1
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
- The `SteamMods` folder contains game content (mods, scripts, blueprints) the player downloaded. Filter mods by the existence of a non-empty `Data/Scripts` folder inside the numbered content folder. 
- The `LocalMods` folder contains mods the player is developing. It is a link to `%AppData%/SpaceEngineers/Mods`.

Use only names matching the Mod API whitelist: [ModApiWhitelist.txt](ModApiWhitelist.txt)
The whitelist was exported from game version `1.208.015` using MDK2's `Mdk.Extractor`.

Mods are released on the Steam Workshop or Mod.IO, mostly on the former.
Mods are compiled by the game on world loading with a Mod API whitelist enforced,
which is supposed to guarantee safety and security. Mods may still crash the game with an exception.

Use the `se-dev-game-code` skill to search the game's decompiled code. You may need this to
understand how the game's internals work and how to interface with it properly. Stick to
game code searches corresponding to names on the Mod API whitelist for efficiency.

References:
- [Mod Template repo](https://github.com/viktor-ferenczi/se-mod-template) Mod template repository to start a new mod project which will include scripts. See [ModTemplate.md](ModTemplate.md)
- [Mod API for script mods](https://malforge.github.io/spaceengineers/modapi/index.html) Structured Mod API documentation
- [Mod API documentation by Keen Software House](https://github.com/KeenSoftwareHouse/SpaceEngineersModAPI) May be outdated
- [Mod Development Kit (MDK2)](https://github.com/malforge/mdk2) Mod development tooling mostly for VS2022