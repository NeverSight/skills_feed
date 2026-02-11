---
name: openproject
description: OpenProject API v3 integration for project management. Manage projects, work packages, time entries, documents, users, notifications, queries. Use when user needs to interact with OpenProject instance - create/update work packages, track time, manage projects, query data, handle documents and attachments.
version: 1.0.0
---

# OpenProject Integration

Full OpenProject API v3 integration with Python packages for project management automation.

## When to Use

- Project management (create, update, delete projects)
- Task/issue tracking (work packages, relations, activities)
- Time tracking (log hours, generate reports)
- Document management (attachments, wiki pages)
- User/team management (users, groups, memberships)
- Notification handling (read, mark, clear)
- Custom views/queries (saved filters, views)
- System configuration (types, statuses, roles)

## Sub-Skills

| Skill | Purpose | Package |
|-------|---------|---------|
| `openproject-core` | Base client, auth, HAL parsing | `openproject_core` |
| `openproject-projects` | Project CRUD | `openproject_projects` |
| `openproject-work-packages` | Tasks, issues, features | `openproject_work_packages` |
| `openproject-time` | Time tracking | `openproject_time` |
| `openproject-users` | User management | `openproject_users` |
| `openproject-documents` | Files & wiki | `openproject_documents` |
| `openproject-queries` | Saved queries | `openproject_queries` |
| `openproject-notifications` | Notifications | `openproject_notifications` |
| `openproject-admin` | System config | `openproject_admin` |

## Setup

```bash
# 1. Navigate to skill directory
cd .claude/skills/openproject

# 2. Install dependencies
uv sync

# 3. Configure .env
OPENPROJECT_URL=https://your-instance.com
OPENPROJECT_API_KEY=your-api-key
```

API key from: **OpenProject → My Account → Access Tokens**

## Config Initialization (REQUIRED)

**CRITICAL: Phải init config trước khi sử dụng bất kỳ tính năng nào!**

Config lưu project metadata vào `.openproject-config.yml` để tránh gọi API lặp lại mỗi lần. Bao gồm: project info, members, types, statuses, priorities, versions, categories, custom fields.

### Init Config (lần đầu)

```bash
cd .claude/skills/openproject
uv run python -c "
from openproject_core import init_config, print_config_summary
from dotenv import load_dotenv
load_dotenv()
init_config(PROJECT_ID)  # Thay PROJECT_ID bằng ID số của project
print_config_summary()
"
```

### Refresh Config (khi có thay đổi)

```bash
cd .claude/skills/openproject
uv run python -c "
from openproject_core import refresh_config, print_config_summary
from dotenv import load_dotenv
load_dotenv()
refresh_config()
print_config_summary()
"
```

### Sử dụng Config

```python
from openproject_core import (
    load_config,           # Load toàn bộ config
    require_config,        # Load config, raise error nếu chưa init
    get_project_id,        # Lấy project ID đã config
    get_type_id,           # Lấy type ID theo tên: get_type_id("Task") → 1
    get_status_id,         # Lấy status ID theo tên: get_status_id("New") → 1
    get_priority_id,       # Lấy priority ID theo tên: get_priority_id("Normal") → 8
    get_version_id,        # Lấy version ID theo tên
    get_custom_field_name, # Lấy tên custom field: get_custom_field_name("customField8", 1) → "Excute Point"
    is_config_initialized, # Kiểm tra config đã init chưa
)
```

**Luôn dùng `require_config()` hoặc `is_config_initialized()` trước khi thực hiện operations!**

## Session Startup (BẮT BUỘC)

**CRITICAL: Phải load config trước MỌI phiên làm việc mới!**

Mỗi khi bắt đầu session mới hoặc khi skill được activate, PHẢI chạy đoạn code sau ĐẦU TIÊN trước khi làm bất kỳ thao tác nào khác:

```bash
cd .claude/skills/openproject
uv run python -c "
from openproject_core import load_session_config
from dotenv import load_dotenv
load_dotenv()
session = load_session_config()
if not session['ok']:
    print(f'ERROR: {session[\"error\"]}')
    print('Run init_config(project_id) to initialize!')
else:
    print(f'Project: {session[\"project\"]} (ID: {session[\"project_id\"]})')
    print(f'User: {session[\"user\"]} @ {session[\"instance\"]}')
    print(f'Config updated: {session[\"updated_at\"]}')
    print(f'Types: {session[\"types_count\"]}, Members: {session[\"members_count\"]}')
"
```

Nếu `ok=False` → phải chạy `init_config(project_id)` trước.
Nếu `ok=True` → sẵn sàng sử dụng các tính năng.

## Instructions

**CRITICAL: Always use package imports - NEVER write inline API calls!**

1. **Load session config first** - Phải chạy `load_session_config()` trước mỗi phiên làm việc
2. **Init config if needed** - Nếu session config trả `ok=False`, chạy `init_config(project_id)`
3. **Use package imports** - All operations via clean imports
4. **Run with uv** - Always `uv run python` from skill directory
5. **Load dotenv** - Always call `load_dotenv()` before API calls
6. **Use config helpers** - Dùng `get_type_id()`, `get_status_id()` thay vì hardcode IDs
7. **Check permissions** - Some operations require admin
8. **Handle pagination** - Use `paginate()` for large datasets

## ⚠️ Important Notes

**Project identifier ≠ Project name!**

```python
# ❌ WRONG - project name không phải identifier
project = get_project('sol-proj-25001')  # 404 Error!

# ✅ CORRECT - tìm project trước để lấy đúng identifier hoặc ID
for p in list_projects():
    if 'sol-proj-25001' in p['name']:
        project_id = p['id']  # ID số: 3
        identifier = p['identifier']  # '008-mii-pb-mh008'
        break

project = get_project(project_id)  # Works!
```

OpenProject có 2 khái niệm:
- `name`: Tên hiển thị (VD: "sol-proj-25001")
- `identifier`: Slug URL (VD: "008-mii-pb-mh008")

Luôn dùng `list_projects()` để tìm đúng ID/identifier trước khi gọi `get_project()`.

---

**All `list_*` functions return generators, NOT lists!**

```python
# ❌ WRONG - generator has no len()
entries = list_time_entries(filters=filters)
print(len(entries))  # TypeError!

# ✅ CORRECT - convert to list first
entries = list(list_time_entries(filters=filters))
print(len(entries))  # Works!
```

This applies to: `list_projects`, `list_work_packages`, `list_time_entries`, `list_users`, `list_notifications`, `list_queries`, etc.

**Time entry `hours` field returns ISO 8601 duration, NOT a number!**

```python
# ❌ WRONG - hours is 'PT1H30M45S', not 1.5
hours = entry['hours']
total += hours  # TypeError!

# ✅ CORRECT - use parse_duration()
from openproject_time import parse_duration
hours = parse_duration(entry['hours'])  # 1.5125
total += hours  # Works!
```

---

**Time entries: Filter theo Work Package**

```python
# ❌ WRONG - filter work_package không tồn tại
filters = [{'work_package': {'operator': '=', 'values': ['123']}}]

# ✅ CORRECT - dùng entity_type + entity_id
from openproject_time import get_work_package_time, get_work_packages_time

# Cho 1 WP
entries = get_work_package_time(wp_id=675)

# Cho nhiều WPs (1 API call)
result = get_work_packages_time(wp_ids=[675, 598, 577])

# Hoặc filter trực tiếp
filters = [
    {"entity_type": {"operator": "=", "values": ["WorkPackage"]}},
    {"entity_id": {"operator": "=", "values": ["675"]}}
]
```

Filters hợp lệ: `entity_type`, `entity_id`, `project_id`, `user_id`, `spent_on`, `activity_id`, `ongoing`, `created_at`, `updated_at`.

---

**`get_work_packages_time()` returns Dict, NOT list!**

```python
# ❌ WRONG - result is dict, not list
result = get_work_packages_time(wp_ids=[675, 598, 577])
for entry in result[:5]:  # KeyError!
    print(entry)

# ✅ CORRECT - iterate over dict items
result = get_work_packages_time(wp_ids=[675, 598, 577])
# result = {675: [entries...], 598: [entries...], 577: [entries...]}

for wp_id, entries in result.items():
    for entry in entries:
        hours = parse_duration(entry['hours'])
        print(f'WP {wp_id}: {hours}h')
```

Return type: `Dict[int, List[dict]]` - key là WP ID, value là list time entries.

---

**`get_schema()` requires BOTH `project_id` AND `type_id`!**

```python
# ❌ WRONG - missing type_id
schema = get_schema(project_id=3)  # TypeError!

# ✅ CORRECT - provide both params
schema = get_schema(project_id=3, type_id=6)  # type 6 = User Story

# Get custom field names
for key, val in schema.items():
    if key.startswith('customField') and isinstance(val, dict):
        print(f'{key}: {val.get("name")}')
# Output:
# customField10: Research Point
# customField8: Excute Point
# customField9: Verify Point
# customField15: Review Point
```

Common type IDs: `1` = Task, `6` = User Story, `10` = TechDebt. Use `list_types()` to get all.

---

**Custom fields are project/type specific!**

```python
# Custom fields vary by project and type
# Always use get_schema() to discover field names

from openproject_work_packages import get_schema, list_work_packages

# 1. Get schema to know custom field mapping
schema = get_schema(project_id=3, type_id=6)
cf_names = {k: v.get('name') for k, v in schema.items()
            if k.startswith('customField') and isinstance(v, dict)}
print(cf_names)
# {'customField10': 'Research Point', 'customField8': 'Excute Point', ...}

# 2. Then access custom fields in work packages
for wp in list_work_packages(project_id=3):
    research = wp.get('customField10') or 0
    execute = wp.get('customField8') or 0
```

---

**`list_activities()` from openproject_time may return empty!**

Activities are often project-specific. Use work package activities instead:

```python
# ❌ May return empty
from openproject_time import list_activities
activities = list(list_activities())  # []

# ✅ Use work package activities for comments/history
from openproject_work_packages import list_activities
activities = list(list_activities(work_package_id=675))
```

## Running Scripts

**IMPORTANT: Always run from skill directory with `uv run`!**

```bash
cd .claude/skills/openproject
uv run python -c "YOUR_CODE"
```

### Script Template

```python
from openproject_core import check_connection
from openproject_projects import list_projects
from dotenv import load_dotenv

load_dotenv()  # Required!

# Your code here
status = check_connection()
print(f"Connected as: {status['user']}")
```

## Available Packages

### openproject_core

```python
from openproject_core import (
    # Connection
    check_connection,      # Verify API connection
    OpenProjectClient,     # HTTP client class

    # Session (REQUIRED - call first each session!)
    load_session_config,   # Load & verify config for session

    # Config (init once, use helpers)
    init_config,           # Init config: init_config(project_id)
    load_config,           # Load full config from YAML
    refresh_config,        # Refresh/update config
    require_config,        # Load config, raise if not init
    is_config_initialized, # Check if config exists
    get_project_id,        # Get configured project ID
    get_type_id,           # Get type ID by name
    get_status_id,         # Get status ID by name
    get_priority_id,       # Get priority ID by name
    get_version_id,        # Get version ID by name
    get_member_id,         # Get user ID by member name (partial match)
    get_member_name,       # Get member name by user ID
    get_custom_field_id,   # Get custom field key by name
    get_custom_field_name, # Get custom field name by key
    print_config_summary,  # Print human-readable config

    # Helpers
    build_filters,         # Build filter JSON
    build_sort,            # Build sort JSON
    paginate,              # Auto-paginate results
    extract_id_from_href,  # Extract ID from HAL href
)
```

### openproject_projects

```python
from openproject_projects import (
    list_projects,    # List all projects
    get_project,      # Get by ID or identifier
    create_project,   # Create new project
    update_project,   # Update project
    delete_project,   # Delete project
    copy_project,     # Copy project structure
    get_versions,     # Get project versions
    get_categories,   # Get project categories
    get_types,        # Get available types
    toggle_favorite,  # Star/unstar project
)
```

### openproject_work_packages

```python
from openproject_work_packages import (
    list_work_packages,       # List with filters
    get_work_package,         # Get by ID
    create_work_package,      # Create task/issue
    update_work_package,      # Update fields (auto-handles lockVersion)
    delete_work_package,      # Delete
    get_schema,               # Get form schema
    list_activities,          # Get comments/history
    add_comment,              # Add comment
    list_relations,           # Get relations
    create_relation,          # Create relation
    delete_relation,          # Delete relation
)
```

### openproject_time

```python
from openproject_time import (
    list_time_entries,     # List with filters (use entity_type+entity_id for WP)
    get_time_entry,        # Get by ID
    create_time_entry,     # Create entry
    update_time_entry,     # Update entry
    delete_time_entry,     # Delete entry
    log_time,              # Shortcut for create
    list_activities,       # Available activities
    get_user_time_today,   # User's today entries
    get_work_package_time, # Single WP's time entries
    get_work_packages_time,# Multiple WPs (1 API call)
    parse_duration,        # Parse ISO 8601 duration to hours
)
```

### openproject_users

```python
from openproject_users import (
    list_users,           # List users
    get_user,             # Get by ID
    get_current_user,     # Get current user
    create_user,          # Create/invite user
    update_user,          # Update user
    delete_user,          # Delete user
    lock_user,            # Lock account
    unlock_user,          # Unlock account
    list_groups,          # List groups
    get_group,            # Get group
    create_group,         # Create group
    add_member,           # Add to group
    remove_member,        # Remove from group
    list_memberships,     # List project memberships
    create_membership,    # Add to project
    delete_membership,    # Remove from project
)
```

### openproject_documents

```python
from openproject_documents import (
    get_attachment,       # Get attachment metadata
    list_attachments,     # List container attachments (NOT documents!)
    download_attachment,  # Download file
    upload_attachment,    # Upload file
    delete_attachment,    # Delete attachment
    list_documents,       # List all documents (read-only API)
    get_document,         # Get document
    get_wiki_page,        # Get wiki page
    update_wiki_page,     # Update wiki page
)
# NOTE: Documents API is read-only. Create/delete via web UI only.
```

### openproject_queries

```python
from openproject_queries import (
    list_queries,         # List saved queries
    get_query,            # Get query config
    create_query,         # Create query
    update_query,         # Update query
    delete_query,         # Delete query
    star_query,           # Add to favorites
    unstar_query,         # Remove from favorites
    get_query_default,    # Get default query
    get_available_columns,# Get column options
)
```

### openproject_notifications

```python
from openproject_notifications import (
    list_notifications,   # List all
    get_notification,     # Get by ID
    mark_read,            # Mark as read
    mark_unread,          # Mark as unread
    mark_all_read,        # Mark all read
    get_unread_count,     # Count unread
    list_unread,          # List unread only
    list_by_reason,       # Filter by reason
)
```

### openproject_admin

```python
from openproject_admin import (
    get_configuration,    # System config
    list_statuses,        # All statuses
    get_status,           # Status details
    list_open_statuses,   # Open statuses only
    list_closed_statuses, # Closed statuses only
    list_priorities,      # All priorities
    get_priority,         # Priority details
    get_default_priority, # Default priority
    list_types,           # WP types
    get_type,             # Type details
    list_project_types,   # Project-specific types
    list_roles,           # All roles
    get_role,             # Role with permissions
)
```

## Examples

### Check Connection

```bash
cd .claude/skills/openproject
uv run python -c "
from openproject_core import check_connection
from dotenv import load_dotenv
load_dotenv()
status = check_connection()
print(f'OK: {status[\"ok\"]}, User: {status[\"user\"]}')
"
```

### List Projects

```bash
cd .claude/skills/openproject
uv run python -c "
from openproject_projects import list_projects
from dotenv import load_dotenv
load_dotenv()
for p in list_projects():
    print(f'{p[\"id\"]}: {p[\"name\"]}')
"
```

### Create Work Package

```bash
cd .claude/skills/openproject
uv run python -c "
from openproject_work_packages import create_work_package
from dotenv import load_dotenv
load_dotenv()
wp = create_work_package(project_id=5, subject='New task', type_id=1)
print(f'Created: #{wp[\"id\"]}')
"
```

### Log Time

```bash
cd .claude/skills/openproject
uv run python -c "
from openproject_time import log_time
from dotenv import load_dotenv
load_dotenv()
entry = log_time(work_package_id=123, hours=2.5, comment='Dev work')
print(f'Logged: {entry[\"id\"]}')
"
```

### List Open Work Packages with Filters

```bash
cd .claude/skills/openproject
uv run python -c "
from openproject_work_packages import list_work_packages
from dotenv import load_dotenv
load_dotenv()
# Filter: open status
filters = [{'status': {'operator': 'o', 'values': []}}]
for wp in list_work_packages(filters=filters):
    print(f'#{wp[\"id\"]}: {wp[\"subject\"]}')
"
```

## Reference Documentation

Each sub-skill has detailed documentation:

| Skill | SKILL.md | API Reference |
|-------|----------|---------------|
| Core | `openproject-core/SKILL.md` | `references/api-basics.md` |
| Projects | `openproject-projects/SKILL.md` | `references/projects-api.md` |
| Work Packages | `openproject-work-packages/SKILL.md` | `references/work-packages-api.md` |
| Time | `openproject-time/SKILL.md` | `references/time-api.md` |
| Users | `openproject-users/SKILL.md` | `references/users-api.md` |
| Documents | `openproject-documents/SKILL.md` | `references/documents-api.md` |
| Queries | `openproject-queries/SKILL.md` | `references/queries-api.md` |
| Notifications | `openproject-notifications/SKILL.md` | `references/notifications-api.md` |
| Admin | `openproject-admin/SKILL.md` | `references/admin-api.md` |

## Full API Specification

Complete OpenAPI spec: `spec.yml` (1.2MB)
