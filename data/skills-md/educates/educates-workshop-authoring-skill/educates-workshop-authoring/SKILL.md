---
name: educates-workshop-authoring
description: >
  Comprehensive guide for creating and configuring workshops for the Educates interactive training platform. Includes steps for creating workshops from scratch, configuring workshop definitions and content and writing workshop instructions. Use this skill when creating Educates workshops, configuring workshop settings or writing workshop content and instructions.
---

# Educates Workshop Authoring Skill

This skill provides guidance for creating interactive workshops for the Educates training platform.

## Initial Workshop Creation

When the user asks to create a workshop, follow these steps:

### 1. Gather Workshop Details

Collect the following information from the user or infer from context:

- **Title**: A short, human-readable title for the workshop
- **Description**: A one to two sentence description of what the workshop covers
- **Name**: A machine-readable identifier (lowercase, dashes allowed, max 25 characters, recommended `lab-` prefix)

If the user provides a topic but not explicit values, propose reasonable defaults and confirm before proceeding.

### 2. Determine Workshop Location

Ask the user to choose one of:
- Use the current directory as the workshop root
- Create a new subdirectory using the workshop name

**Deriving the workshop name from the directory:**

If the user chooses to use the current working directory:
1. Check if the directory name satisfies the naming convention (lowercase, dashes allowed, max 25 characters). Note: the `lab-` prefix is recommended but not required when using the directory name.
2. If it does, use the directory name as the workshop name
3. If it does not satisfy the requirements, infer an appropriate name from the workshop topic or title, but confirm with the user before proceeding (unless they already explicitly provided a name)

### 3. Determine Workshop Requirements

The terminal application is always enabled by default. Always include it explicitly with `enabled: true` and `layout: split` for clarity.

Ask the user about additional session applications based on the workshop's technical requirements:

- **Editor**: Will users need to edit or view files in the browser?
- **Kubernetes access**: Will users run kubectl commands or interact with the Kubernetes API?
- **Kubernetes console**: Would a visual cluster view help users?
- **Docker**: Will users build or run containers?
- **Image registry**: Will users push container images?
- **Virtual cluster**: Does the workshop need cluster-admin operations?
- **Git server**: Will users need a local Git repository (e.g., for CI/CD pipelines)?
- **Slides**: Does the workshop include a presentation alongside the instructions?

Infer sensible defaults from the workshop topic. For example, a Kubernetes workshop likely needs editor, Kubernetes access, and console enabled.

### 4. Create Workshop Structure

Create the following directory structure in the chosen location:

```
<workshop-root>/
├── README.md                    # Workshop title and description
├── exercises/
│   └── README.md                # Placeholder to ensure directory is preserved
├── resources/
│   └── workshop.yaml            # Educates Workshop definition
└── workshop/
    └── content/                 # Workshop instruction pages (Markdown)
```

#### The exercises Directory

Always create an `exercises/` directory as part of the initial workshop structure. This directory serves as the working area for the workshop user — place any files they will need during the workshop here, such as source code, configuration files, sample data, YAML manifests, templates, or starter projects. By keeping all user-facing files under `exercises/`, the workshop environment stays organized and free of clutter from the home directory.

When this directory exists in the workshop files imported into the workshop session container, Educates treats it specially:

- **Terminal working directory**: Embedded terminals in the workshop dashboard start with `~/exercises` as their current working directory instead of the home directory.
- **Editor root directory**: The VS Code editor opens on `~/exercises` rather than the home directory, so users only see workshop-relevant files and are not distracted by hidden dot files or other home directory contents.

This special behavior is only triggered if the `exercises/` directory already exists when the workshop session starts. It cannot be created later by workshop instructions — the directory must be part of the published workshop files.

**Important: the directory must contain at least one file.** Empty directories are not preserved when publishing workshop files to a Git repository or OCI image artefact. To ensure the directory is included, add a `README.md` with a brief note such as "Exercise files for this workshop" or a similar placeholder. Avoid using a `.gitkeep` file unless the workshop source is managed in a Git repository where that convention makes sense.

Because the `exercises/` directory is always recommended, workshop instructions should never need to create it. File paths used in clickable actions for files under this directory must use the `~/exercises` prefix (e.g., `~/exercises/deployment.yaml`). The examples in the clickable actions reference files already follow this convention.

### 5. Generate workshop.yaml

Refer to [resources/workshop-yaml-reference.md](resources/workshop-yaml-reference.md) for the complete workshop.yaml structure and options.

Generate the `resources/workshop.yaml` file based on the gathered details.

**CRITICAL: Use the correct publish and workshop.files format.**

The workshop.yaml MUST include these sections with this exact structure (substituting the actual workshop name):

```yaml
spec:
  publish:
    image: "$(image_repository)/{workshop-name}-files:$(workshop_version)"
    files:
    - directory:
        path: .
      includePaths:
      - /workshop/**
      - /exercises/**
      - /README.md
  workshop:
    files:
    - image:
        url: "$(image_repository)/{workshop-name}-files:$(workshop_version)"
```

**IMPORTANT:** Do NOT use `spec.content.files` — this is a deprecated format. Always use `spec.publish` and `spec.workshop.files` as shown above. The `$(image_repository)` and `$(workshop_version)` variables must be used exactly as shown to support local workshop publishing and deployment workflows. The `spec.publish.files` section controls which files are packaged into the published OCI image — only the listed paths are included, keeping the image small. The `spec.workshop.files` section specifies where to pull the files from at runtime; since the published image is already filtered, no `includePaths` is needed there. The `spec.workshop.files` array also supports Git and HTTP sources and can contain multiple entries overlaid in order — see the "Alternative File Sources" section in the workshop YAML reference for details.

**Additional configuration:**

- Set `metadata.name` to the workshop name
- Set `spec.title` and `spec.description` from gathered details
- Set `spec.duration` to estimated completion time (e.g., `15m`, `30m`, `1h`)
- Set `spec.difficulty` to one of: `beginner`, `intermediate`, `advanced`, `extreme`
- Always include terminal with `enabled: true` and `layout: split`
- Enable only the additional session applications the workshop requires
- Set `spec.session.namespaces.security.token.enabled` to `false` by default (it is enabled by default for historical reasons)
- Only set `spec.session.namespaces.security.token.enabled` to `true` if the workshop needs kubectl or uses the Kubernetes console
- Omit any applications that are not needed (do not include with `enabled: false`)

### 6. Add GitHub Actions Workflow for Publishing (Only When Requested)

**Skip this step during initial workshop creation unless the user explicitly asks to set up publishing of the workshop to GitHub container registry using a GitHub action.** This step also applies when a user returns to an existing workshop and asks to add publishing support after the workshop has already been created.

This step applies only to standalone workshops that live in their own Git repository. If the workshop is part of a course containing multiple workshops, do not use this GitHub action — publishing for courses is handled differently.

When requested, create a `.github/workflows/publish-workshop.yaml` file in the workshop repository. Refer to [resources/workshop-publishing-reference.md](resources/workshop-publishing-reference.md) for the complete workflow configuration, action parameters, and how publishing relates to the `spec.publish` section in workshop.yaml.

### 7. Add Local Docker Compatibility (Only When Requested)

**Skip this step unless the user explicitly asks for the workshop to work on local Docker as well as in Kubernetes.** This step also applies when a user returns to an existing workshop and asks to add local Docker support retrospectively.

Not all workshops are compatible with local Docker deployment. Workshops that require Kubernetes access, a virtual cluster, a session image registry, or that use `environment.objects`, `session.objects`, or `request.objects` in the workshop definition cannot run on local Docker.

When local Docker support is requested for a compatible workshop, the main change is appending the `ingress_port_suffix` data variable to all session proxy URLs — in both the workshop definition and workshop instructions. This variable is an empty string when on standard ports (Kubernetes) and includes the port number when on a non-standard port (local Docker), so adding it has no effect on Kubernetes deployment.

Refer to [resources/local-docker-deployment-reference.md](resources/local-docker-deployment-reference.md) for the full list of restrictions, where to apply the port suffix, and how to retrofit local Docker support onto an existing workshop.

### 8. Create the AI Assistant Instructions File

**Skip this step if any of the following are true:**
- An AI assistant instructions file (e.g., `CLAUDE.md`, `AGENTS.md`) already exists in the workshop root directory
- An AI assistant instructions file already exists in a parent directory (indicating the workshop is part of a larger project, such as a course created with the educates-course-design skill)

Create an AI assistant instructions file in the project root so that future AI interactions automatically know the project context and which skills to use. For Claude Code, this file is `CLAUDE.md`; other AI coding agents use different conventions (e.g., `AGENTS.md`).

The instructions file should contain:

- A pointer to `README.md` for the project overview and description
- **Skill references** — when to invoke each skill:
  - The **educates-workshop-authoring** skill for creating or modifying the workshop definition, instruction pages, and exercise files
  - The **educates-course-design** skill for course planning, if this workshop is later incorporated into a multi-workshop course

Keep this file focused on AI-specific instructions and project-specific overrides. Do not duplicate content that already exists in `README.md` — reference it instead.

### 9. Create Workshop Instructions

Workshop instructions are placed in the `workshop/content/` directory as Markdown files rendered by Hugo.

#### Guided Instruction Through Clickable Actions

By default, workshop instructions should provide a guided experience where all code interaction — viewing, running, and modifying — is driven through clickable actions. Learners should not be asked to type commands into the terminal or write code into the editor by hand. Instead, every interaction should use the appropriate clickable action (`terminal:execute`, `editor:open-file`, `editor:replace-matching-text`, etc.). This keeps learners focused on the concepts rather than on mechanics. If the person requesting the workshop explicitly asks for a different experience, adjust accordingly.

Refer to [resources/workshop-design-principles.md](resources/workshop-design-principles.md) for the complete design philosophy, including guidance on how learners should view, run, and modify code, and how to structure the `exercises/` directory as a pre-populated workspace.

#### Clickable Actions in Instructions

Workshop instructions use clickable actions — special fenced code blocks that let users execute commands, edit files, and interact with the workshop environment by clicking. Refer to [resources/clickable-actions-reference.md](resources/clickable-actions-reference.md) for the complete list of action types and detailed syntax.

**Critical YAML safety rule for terminal commands:** When generating `terminal:execute` clickable actions, always use YAML block scalar syntax (`command: |-`) if the command contains any characters that are special in YAML (colon, hash, curly braces, square brackets, etc.) or if the command spans multiple lines. This prevents the YAML parser from misinterpreting the command. For example:

````markdown
```terminal:execute
command: |-
  docker run --rm -p 8080:80 nginx:latest
```
````

Also ensure that shell commands use correct quoting — variable expansions containing paths with spaces should be double-quoted, strings with special characters should be properly escaped, etc. See the "YAML Syntax Safety" section in the clickable actions reference for detailed guidance and examples.

#### Tracking Terminal Working Directory

When the `exercises/` directory exists, each terminal session starts with `~/exercises` as its current working directory — not the home directory. As you write workshop instructions, you **must track the current working directory of each terminal at every point** in the instructions. Any `cd` command in a `terminal:execute` action changes the working directory for all subsequent commands in that terminal.

Getting this wrong leads to commands that reference incorrect file paths. Either:

- **Track the working directory and use correct relative paths.** For example, if the terminal is in `~/exercises` and you need to access `~/exercises/deployment.yaml`, use `deployment.yaml`. If a previous step ran `cd ~/exercises/myapp`, then `deployment.yaml` would need to be `../deployment.yaml` or you must use the full path.
- **Use absolute paths to avoid ambiguity.** For example, always use `~/exercises/deployment.yaml` regardless of the current directory.

When the workshop uses the split terminal layout (two terminals), track the working directory of each terminal independently — a `cd` in one terminal does not affect the other.

#### Dashboard Tab Visibility

The workshop dashboard shows only one tab at a time on the right-hand side of the screen (the left side displays the workshop instructions). The Terminal tab is visible by default when a session starts. Users switch between tabs by clicking on tab headers or through `dashboard:open-dashboard` clickable actions.

This matters when writing instructions because certain actions implicitly change which tab is visible. A `terminal:execute` action switches to the Terminal tab, hiding any other tab (such as a web application dashboard) the user was viewing. If the workshop uses a custom dashboard tab (e.g., for a web app accessed via the session proxy), you must explicitly guide the user back to that tab after running terminal commands so they can see the result.

Refer to [resources/workshop-dashboard-reference.md](resources/workshop-dashboard-reference.md) for detailed patterns and examples for handling tab switching in workshop instructions.

#### Data Variables in Instructions

Workshop instructions should be parameterized using data variables rather than hardcoding session-specific values. Educates provides data variables for the session namespace, ingress domain, session hostname, and many other context-specific values. Use the Hugo `param` shortcode to insert them:

```markdown
Deploy the application to the `{{< param session_namespace >}}` namespace.
```

Data variables also work inside clickable actions:

````markdown
```terminal:execute
command: kubectl get pods -n {{< param session_namespace >}}
```
````

In terminal commands within clickable actions, you can alternatively use the equivalent uppercase environment variable (e.g., `$SESSION_NAMESPACE`) since the terminal shell has these set automatically. Refer to [resources/data-variables-reference.md](resources/data-variables-reference.md) for the complete list of available data variables and which contexts they can be used in.

#### Page Structure

Each page requires YAML frontmatter with at least a `title` property:

```markdown
---
title: Page Title
---

This is the introductory paragraph for the page. It appears immediately
after the frontmatter with no heading.

## First Section

Content for the first section...

## Second Section

Content for the second section...
```

**Content guidelines:**

- Use standard Markdown for page content
- Do NOT use a level 1 heading (`#`) — the `title` in frontmatter automatically generates the page header
- Begin immediately with an introductory paragraph after the frontmatter
- Use level 2 headings (`##`) and below for any additional sections
- **Use admonition shortcodes** to highlight important information: `{{< note >}}` for tips, `{{< warning >}}` for cautions, and `{{< danger >}}` for critical warnings. See [resources/hugo-shortcodes-reference.md](resources/hugo-shortcodes-reference.md) for syntax and usage guidance.
- **Focus on the workshop topic, not the platform.** Workshop instructions should teach the subject matter, not how Educates works. When the workshop requires platform-specific configuration (e.g., setting up a session proxy for accessing a deployed service, configuring ingresses, or using data variables), present these as natural steps of the exercise without drawing attention to Educates internals. Do not say things like "we will learn how Educates is configured" or "this is how Educates handles ingress" — unless the workshop is specifically about using the Educates platform itself. The overview, summary, and learning objectives should describe what users will learn about the topic, not about the workshop infrastructure supporting it.

#### File Naming Convention

Use a numeric prefix for ordering pages: `nn-page-name.md`

Recommended structure:
- `00-workshop-overview.md` - Introduction and objectives
- `01-first-topic.md` - First instructional page
- `02-second-topic.md` - Continue incrementing for core content
- `99-workshop-summary.md` - Wrap-up and next steps

Reserve `00-` for the overview and `99-` for the summary. Core instructional pages start at `01-` and increment.

#### Page Bundles

For simple pages, use a single `.md` file. For pages with embedded images local to that page, use a page bundle instead:

```
workshop/content/
├── 00-workshop-overview.md
├── 01-first-topic/
│   ├── index.md
│   └── diagram.png
├── 02-second-topic.md
└── 99-workshop-summary.md
```

A page bundle is a directory containing `index.md` plus any associated assets (images, etc.). For detailed guidance on including images in workshop pages, see [resources/images-in-workshop-pages.md](resources/images-in-workshop-pages.md).

### 10. Verify Workshop Definition

After generating `resources/workshop.yaml`, verify the following critical items:

**Required sections exist:**
- [ ] `spec.publish` section exists with `image` and `files` fields
- [ ] `spec.publish.files` uses `includePaths` to select only `/workshop/**`, `/exercises/**`, and `/README.md`
- [ ] `spec.workshop` section exists with `files` array
- [ ] Both `spec.publish.image` and `spec.workshop.files` use `$(image_repository)` and `$(workshop_version)` variables

**Deprecated formats NOT used:**
- [ ] `spec.content.files` is NOT present (use `spec.workshop.files` instead)

**Application settings:**
- [ ] Terminal includes `enabled: true` and `layout: split`
- [ ] Only required applications are included (omit disabled ones entirely)
- [ ] `spec.session.namespaces.security.token.enabled` is explicitly set to `false` unless Kubernetes access is needed

### 11. Verify Workshop Instructions

After generating workshop instruction pages, verify the following:

**Terminal working directory correctness:**
- [ ] The initial working directory for each terminal is known (it is `~/exercises` when the exercises directory exists, otherwise `~`)
- [ ] Every `cd` command in `terminal:execute` actions is tracked — the working directory after each step is accounted for
- [ ] All relative file paths in terminal commands are correct for the working directory at that point in the instructions
- [ ] When using split terminals, the working directory of each terminal is tracked independently

**File path consistency:**
- [ ] File paths in `editor` clickable actions use the `~/exercises` prefix where appropriate
- [ ] File paths referenced in prose match the paths used in clickable actions

**Dashboard tab visibility:**
- [ ] After any `terminal:execute` action that follows a step where the user was viewing a non-terminal dashboard tab (e.g., a web application), the instructions guide the user back to the correct tab using `dashboard:open-dashboard` or `dashboard:reload-dashboard`
- [ ] The visible dashboard tab is tracked throughout the instructions, just as the terminal working directory is tracked

**Guided instruction:**
- [ ] All code viewing uses editor clickable actions (`editor:open-file`, `editor:select-matching-text`) — not plain code blocks or terminal commands like `cat`
- [ ] All command execution uses `terminal:execute` clickable actions — learners are never asked to type commands manually
- [ ] All code modifications use editor clickable actions (`editor:replace-matching-text`, `editor:append-lines-after-match`, etc.) — learners are never asked to edit files by hand
- [ ] `workshop:copy` or `workshop:copy-and-edit` are only used where content must be customized per-learner and cannot be handled by data variables

**Content focus:**
- [ ] Workshop overview and summary describe the subject matter, not the Educates platform
- [ ] Learning objectives focus on what the user will learn about the topic
- [ ] Platform-specific steps (proxies, ingresses, data variables) are presented as natural parts of the exercise without calling attention to Educates internals

## Reference Guides

For detailed guidance on specific topics, see:

- [Workshop Design Principles](resources/workshop-design-principles.md) - Guided experience philosophy, the no-manual-typing rule, and guidance on how learners should view, run, and modify code
- [Workshop YAML Reference](resources/workshop-yaml-reference.md) - Complete workshop.yaml structure and options
- [Images in Workshop Pages](resources/images-in-workshop-pages.md) - How to include images using page bundles and static assets
- [Clickable Actions Reference](resources/clickable-actions-reference.md) - Index of all clickable action types, YAML syntax safety guidance, and links to category-specific references in [resources/clickable-actions/](resources/clickable-actions/)
- [Workshop Tools Reference](resources/workshop-tools-reference.md) - Command-line tools available in the workshop environment, including utilities for JSON/YAML processing, Kubernetes management, container handling, and load testing
- [Kubernetes Access Reference](resources/kubernetes-access-reference.md) - Namespace isolation, session namespace references, and pod security policies for workshops with Kubernetes access
- [Data Variables Reference](resources/data-variables-reference.md) - Complete list of data variables for parameterizing workshop instructions, terminal commands, and workshop definitions
- [Workshop Dashboard Reference](resources/workshop-dashboard-reference.md) - Dashboard layout, single-tab visibility behavior, and patterns for guiding users between tabs in workshop instructions
- [Workshop Image Reference](resources/workshop-image-reference.md) - Container image selection for workshops, including pre-built JDK and Conda images
- [Java Language Reference](resources/java-language-reference.md) - JDK image selection, Maven/Gradle build commands, project layout, and Spring Boot patterns for Java workshops
- [Python Language Reference](resources/python-language-reference.md) - Python version management, uv/pip package installation, project layout, and web framework patterns for Python workshops
- [Workshop Setup Reference](resources/workshop-setup-reference.md) - Setup scripts, environment variables, background services, and terminal customization for the workshop container
- [Hugo Shortcodes Reference](resources/hugo-shortcodes-reference.md) - Admonition callouts (note, warning, danger), pathway conditional rendering, and custom shortcodes for workshop instructions
- [Session Objects Reference](resources/session-objects-reference.md) - Pre-creating Kubernetes resources per session, shared environment objects, request objects, and workshop container resource configuration
- [Workshop Publishing Reference](resources/workshop-publishing-reference.md) - How to add a GitHub Actions workflow for publishing a standalone workshop to GitHub container registry using the Educates publish-workshop GitHub Action. Consult this when a user asks to set up publishing for a workshop, whether during initial creation or when adding it to an existing workshop later.
- [Local Docker Deployment Reference](resources/local-docker-deployment-reference.md) - Restrictions and required changes for workshops that need to run on local Docker as well as in Kubernetes. Consult this when a user asks for local Docker compatibility, whether during initial creation or when retrofitting it onto an existing workshop.

## Skill Version

When asked about the skill version, read the `VERSION.txt` file and report its contents to the user.

## Getting Help

For more information, visit the Educates documentation: https://docs.educates.dev/
