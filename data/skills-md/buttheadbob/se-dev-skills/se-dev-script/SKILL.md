---
name: se-dev-script
description: In-game (programmable block, aka PB) script development for Space Engineers version 1
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
- The `SteamScripts` folder contains game content (mods, scripts, blueprints) the player downloaded. Filter scripts by the existence of a `Script.cs` file directly in the numbered content folder. 
- The `LocalScripts` folder contains mods the player is developing. It is a link to `%AppData%/SpaceEngineers/IngameScripts`.

Use only names matching the PB API whitelist: [PBApiWhitelist.txt](PBApiWhitelist.txt)
The whitelist was exported from game version `1.208.015` using MDK2's `Mdk.Extractor`.

In-game (PB) scripts are released on the Steam Workshop or Mod.IO, mostly on the former.
In-game scripts are compiled by the game on loading into the PB or world loading (if the PB has a script loaded)
with a PB Script API whitelist enforced, which is supposed to guarantee safety and security. 
Scripts cannot crash the game, since any exception is caught and the script is killed by the game.
Scripts can still lag the game if no specific resource usage enforcement is set up by the player or server admin.

The script's source code size is limited to 100,000 bytes when the player loads it. The ScriptDev plugin can load
more from local file into offline (local) games for testing purposes, therefore scripts can be tested without
source code compression, which is useful to get fully detailed exception tracebacks. 

Use the `se-dev-game-code` skill to search the game's decompiled code. You may need this to
understand how the game's internals work and how to script it properly. Stick to game code
searches corresponding to names on the PB API whitelist for efficiency.

References:
- [Script Template repo](https://github.com/viktor-ferenczi/se-script-template) PB script template repository to start a new project. See [ScriptTemplate.md](ScriptTemplate.md)
- [Script Merge tool](https://github.com/viktor-ferenczi/se-script-merge) Merging PB scripts from C# projects into single file with optional code compression. See [ScriptMerge.md](ScriptMerge.md)
- [Script Dev plugin](https://github.com/viktor-ferenczi/se-script-dev) Automatic script loading into the PB in-game for easier testing. See [ScriptDev.md](ScriptDev.md)
- [Mod Development Kit (MDK2)](https://github.com/malforge/mdk2)
- [Programmable Block API](https://malforge.github.io/spaceengineers/pbapi)
- [Wiki on Scripting](https://spaceengineers.wiki.gg/wiki/Scripting)
