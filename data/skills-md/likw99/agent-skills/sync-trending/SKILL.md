---
name: sync-trending
description: Monitior technology trends (GitHub, etc.), contextualize them against the user's project, and autonomously verify them through installation and testing. Use when the user asks about trending repositories, new tools, or wants to stay updated on tech relevant to their current work.
---

# Sync Trending

Keep up-to-date with technology trends by monitoring GitHub Trending, brainstorming their value against your current context, and autonomously verifying selected technologies.

## Workflow

### 1. Monitor, Brainstorm & Summarize
When triggered, follow these steps:
1. **Understand Context:** Read the local `README.md`, `package.json`, or search the current directory to understand the user's project context. Check `save_memory` for user preferences or other projects.
2. **Fetch Trends:** Use `web_fetch` to retrieve content from the sources listed in [sources.md](references/sources.md) (primarily GitHub Trending).
3. **Analyze & Brainstorm:** For the top repositories, brainstorm how they could benefit the user's specific project or role.
4. **Report:** Present a "Contextualized Trend Report" including:
   - **Facts:** Repo Name, URL, Language, Stars, and a brief description.
   - **Contextual Value:** A one-sentence insight on why this matters (e.g., "Could replace your current auth implementation," "Relevant for the data visualization feature you're planning").

### 2. Permission & Deep Dive
If the user expresses interest in a specific repository:
1. **Ask Permission:** Clearly ask: "Shall I clone [Repo Name] and attempt to run it for verification?"
2. **Setup:**
   - Use `run_shell_command` to `git clone` the repository into a temporary directory (e.g., in `~/.gemini/tmp/`).
   - Read `README.md` or `CONTRIBUTING.md` to identify build/run instructions.
3. **Execution:**
   - Detect project type (Node.js, Python, Rust, Go, etc.).
   - Install dependencies (`npm install`, `pip install -r requirements.txt`, etc.).
   - Run the application or demo (`npm start`, `python main.py`, etc.).
4. **Verification:**
   - If it starts a web server, use `browser_navigate` to check `http://localhost:<port>`.
   - If it's a CLI tool, check the output for success/failure.
5. **Report Outcome:** Summarize the setup process, any issues found, and the final verification result.

### 3. Generate Artifacts
Based on the deep dive and the initial brainstorming, offer to generate one of the following:
- **`todo.md`:** A concrete integration plan for the user's existing project, including technical snippets discovered during the deep dive.
- **`idea.md`:** A blueprint for a new project based on the trending tech.
- **`brief.md`:** A high-level summary suitable for sharing with a CEO, Board of Directors, or a Team.

## Safety Guidelines
- **NEVER** clone or execute code without explicit user permission.
- **ALWAYS** perform deep dives in a temporary or isolated directory.
- **NEVER** expose the user's local secrets or environment variables to the trending repository.
