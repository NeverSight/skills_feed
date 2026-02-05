---
name: conport-memory
description: Access Context Portal (ConPort) as persistent project memory via MCPorter. Load/update project context, log decisions and progress, track patterns. Use PROACTIVELY at session start to load context and throughout work to log decisions. Combats AI amnesia across sessions.
---

<conport_memory_skill>
  <overview>
    ConPort is your project's memory bank - a SQLite-backed knowledge base that
    persists decisions, progress, patterns, and context across Claude Code sessions.
    Access via MCPorter CLI without MCP installation.
  </overview>

  <when_to_use_proactively>
    <scenario trigger="session_start">Load product_context and active_context</scenario>
    <scenario trigger="architectural_decision">Log decision with rationale and tags</scenario>
    <scenario trigger="task_completion">Update progress with status</scenario>
    <scenario trigger="pattern_discovery">Log system_pattern for reuse</scenario>
    <scenario trigger="session_end">Update active_context with current state</scenario>
  </when_to_use_proactively>

  <mcporter_base_command>
    npx mcporter call --stdio "uvx --from context-portal-mcp conport-mcp --mode stdio" conport.TOOL_NAME
  </mcporter_base_command>

  <core_commands>
    <command name="Get Product Context" purpose="Load overall project goals/architecture">
      npx mcporter call --stdio "uvx --from context-portal-mcp conport-mcp --mode stdio" \
        conport.get_product_context
    </command>

    <command name="Update Product Context" purpose="Set project overview">
      npx mcporter call --stdio "uvx --from context-portal-mcp conport-mcp --mode stdio" \
        conport.update_product_context content:"Project overview text..."
    </command>

    <command name="Get Active Context" purpose="Load current working focus">
      npx mcporter call --stdio "uvx --from context-portal-mcp conport-mcp --mode stdio" \
        conport.get_active_context
    </command>

    <command name="Update Active Context" purpose="Update current session state">
      npx mcporter call --stdio "uvx --from context-portal-mcp conport-mcp --mode stdio" \
        conport.update_active_context content:"Currently working on..."
    </command>

    <command name="Log Decision" purpose="Record architectural decision">
      npx mcporter call --stdio "uvx --from context-portal-mcp conport-mcp --mode stdio" \
        conport.log_decision \
        summary:"Decision title" \
        rationale:"Why this was decided" \
        details:"Full decision details" \
        tags:'["architecture", "database"]'
    </command>

    <command name="Get Decisions" purpose="Retrieve logged decisions">
      npx mcporter call --stdio "uvx --from context-portal-mcp conport-mcp --mode stdio" \
        conport.get_decisions tags:'["architecture"]'
    </command>

    <command name="Search Decisions" purpose="Full-text search across decisions">
      npx mcporter call --stdio "uvx --from context-portal-mcp conport-mcp --mode stdio" \
        conport.search_decisions_fts query:"authentication"
    </command>

    <command name="Log Progress" purpose="Record task status">
      npx mcporter call --stdio "uvx --from context-portal-mcp conport-mcp --mode stdio" \
        conport.log_progress \
        status:"in_progress" \
        description:"Implementing user authentication"
    </command>

    <command name="Get Progress" purpose="Retrieve progress entries">
      npx mcporter call --stdio "uvx --from context-portal-mcp conport-mcp --mode stdio" \
        conport.get_progress status:"in_progress"
    </command>

    <command name="Log System Pattern" purpose="Document reusable pattern">
      npx mcporter call --stdio "uvx --from context-portal-mcp conport-mcp --mode stdio" \
        conport.log_system_pattern \
        name:"Repository Pattern" \
        description:"Data access abstraction" \
        tags:'["architecture", "data-layer"]'
    </command>

    <command name="Get System Patterns" purpose="Retrieve documented patterns">
      npx mcporter call --stdio "uvx --from context-portal-mcp conport-mcp --mode stdio" \
        conport.get_system_patterns
    </command>

    <command name="Log Custom Data" purpose="Store project-specific key-value data">
      npx mcporter call --stdio "uvx --from context-portal-mcp conport-mcp --mode stdio" \
        conport.log_custom_data \
        category:"glossary" \
        key:"MFA" \
        value:'{"definition": "Multi-Factor Authentication", "context": "Security feature"}'
    </command>

    <command name="Export to Markdown" purpose="Export all ConPort data">
      npx mcporter call --stdio "uvx --from context-portal-mcp conport-mcp --mode stdio" \
        conport.export_conport_to_markdown output_dir:"./context-export"
    </command>
  </core_commands>

  <session_workflow>
    <phase name="Session Start">
      1. Check if context_portal/context.db exists
      2. If exists:
         - get_product_context - understand project goals
         - get_active_context - resume from last session
         - get_progress status:"in_progress" - see pending tasks
         - get_decisions - review recent architectural decisions
      3. If not exists: prompt user to run /conport-init
    </phase>

    <phase name="During Work">
      - log_decision - when making architectural choices
      - log_progress - when completing tasks
      - log_system_pattern - when discovering reusable patterns
      - log_custom_data - for project-specific context
    </phase>

    <phase name="Session End">
      1. update_active_context - record current state and next steps
      2. log_progress - mark completed items
    </phase>
  </session_workflow>

  <knowledge_graph>
    Link related items to build explicit relationships:

    npx mcporter call --stdio "uvx --from context-portal-mcp conport-mcp --mode stdio" \
      conport.link_conport_items \
      source_type:"decision" source_id:"dec-123" \
      target_type:"progress" target_id:"prog-456" \
      relationship:"implements"

    Retrieve linked items:
    npx mcporter call --stdio "uvx --from context-portal-mcp conport-mcp --mode stdio" \
      conport.get_linked_items item_type:"decision" item_id:"dec-123"
  </knowledge_graph>

  <available_tools>
    Product/Active Context:
    - get_product_context, update_product_context
    - get_active_context, update_active_context

    Decisions:
    - log_decision, get_decisions, search_decisions_fts, delete_decision_by_id

    Progress:
    - log_progress, get_progress, update_progress, delete_progress_by_id

    Patterns:
    - log_system_pattern, get_system_patterns, delete_system_pattern_by_id

    Custom Data:
    - log_custom_data, get_custom_data, delete_custom_data
    - search_project_glossary_fts, search_custom_data_value_fts

    Knowledge Graph:
    - link_conport_items, get_linked_items

    Utility:
    - get_item_history, get_recent_activity_summary
    - export_conport_to_markdown, import_markdown_to_conport
    - batch_log_items, get_conport_schema
  </available_tools>
</conport_memory_skill>
