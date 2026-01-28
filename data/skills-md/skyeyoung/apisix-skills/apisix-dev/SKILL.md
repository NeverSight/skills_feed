---
name: apisix-dev
description: Guide APISIX Development environment setup and run tests. Trigger when user mentions "APISIX test", "run APISIX tests", "APISIX testing", "setup APISIX test environment", "TEST::NGINX", "prove test", "APISIX CI", "test-nginx", "APISIX development environment", "APISIX deployment mode", "config_provider yaml", "apisix.yaml", "standalone mode", "data_plane role", or asks about running specific APISIX test files.
---

# APISIX Development Environment Setup

This skill guides you through setting up the APISIX testing environment and running tests using TEST::NGINX.

## Environment Requirements

### Ubuntu Only

**IMPORTANT**: Direct test execution is only supported on **Ubuntu**.

Before proceeding, check the operating system:

```bash
uname -a && cat /etc/os-release 2>/dev/null | head -5
```

**If NOT Ubuntu:**

1. **Option A: Use Ubuntu Environment**
   - Start an Ubuntu VM, container, or WSL2
   - Run commands there and paste error logs back for analysis

2. **Option B: Use DevContainers (VSCode)**
   - See: https://apisix.apache.org/docs/apisix/build-apisix-dev-environment-devcontainers/
   - Setup steps:
     ```bash
     git clone https://github.com/apache/apisix.git
     cd apisix
     code .
     # In VSCode: Cmd/Ctrl+Shift+P -> "Dev Containers: Reopen in Container"
     ```
   - **Warning**: Some tests may not run normally in DevContainer due to container limitations

**If Ubuntu**: Proceed with the setup below.

## Quick Start (Ubuntu)

### Step 1: Clone Repository with Submodules

```bash
git clone --recurse-submodules https://github.com/apache/apisix.git
cd apisix
```

If already cloned without submodules:

```bash
git submodule update --init --recursive
```

### Step 2: Install Dependencies Using CI Scripts

APISIX provides CI scripts that handle all dependency installation. Use these scripts to ensure consistency with the official CI environment.

**Reference the CI workflow**: https://github.com/apache/apisix/blob/master/.github/workflows/build.yml

**Key CI Scripts:**

- `ci/common.sh` - Common utilities and dependency functions
- `ci/linux_openresty_runner.sh` - Main runner script
- `ci/linux_openresty_common_runner.sh` - Installation functions (`before_install`, `do_install`)

**Run the installation:**

```bash
# Source the CI scripts and run installation
cd apisix

# Set required environment variables
export OPENRESTY_VERSION=default
export SERVER_NAME=linux_openresty

# Source and run the CI installation functions
. ./ci/common.sh
. ./ci/linux_openresty_common_runner.sh

# Run before_install (installs system dependencies, Test::Nginx)
before_install

# Run do_install (installs OpenResty, Lua deps, test-nginx, etc.)
do_install
```

**What the CI scripts install:**

- System packages (cpanminus, build-essential, libssl-dev, etc.)
- Test::Nginx via cpanm
- OpenResty with correct version
- Lua dependencies (`make deps`)
- test-nginx from openresty/test-nginx
- Additional tools (grpcurl, Node.js, etc.)

**Note**: etcd runs in Docker container, not installed locally.

### Step 3: Verify Installation

```bash
# Verify OpenResty
openresty -v

# Verify test-nginx exists
ls test-nginx/
```

**Note**: If you encounter issues with the CI scripts, check the latest `build.yml` for any changes to the installation process. The CI scripts are the source of truth for the test environment setup.

## Environment Variables

Set these environment variables before running tests:

```bash
export OPENRESTY_PREFIX="/usr/local/openresty"
export PATH=$OPENRESTY_PREFIX/nginx/sbin:$OPENRESTY_PREFIX/luajit/bin:$OPENRESTY_PREFIX/bin:$PATH

# Optional - adjust based on your setup
export OPENRESTY_VERSION=default
export SERVER_NAME=linux_openresty
```

Verify the setup:

```bash
which openresty
openresty -v
which etcd
etcd --version
```

## Running Tests

### Basic Test Execution

Tests use the `prove` command with TEST::NGINX. Run from the APISIX repository root:

```bash
# Run a single test file
FLUSH_ETCD=1 prove -I./test-nginx/lib -I./ t/path/to/test.t

# Example: Run a specific test
FLUSH_ETCD=1 prove -I./test-nginx/lib -I./ t/plugin/limit-count.t
```

### Test Command Options

| Option               | Description                                   |
| -------------------- | --------------------------------------------- |
| `FLUSH_ETCD=1`       | Flush etcd before running tests (recommended) |
| `-I./test-nginx/lib` | Include test-nginx library path               |
| `-I./`               | Include current directory                     |
| `-v`                 | Verbose output                                |
| `-r`                 | Recurse into directories                      |

### Run Multiple Tests

```bash
# Run all tests in a directory
FLUSH_ETCD=1 prove -I./test-nginx/lib -I./ -r t/plugin/

# Run tests matching a pattern
FLUSH_ETCD=1 prove -I./test-nginx/lib -I./ t/plugin/limit-*.t
```

### Start Required Services

Before running tests, start the CI environment using Docker:

```bash
# Start all required services (etcd, etc.) via Docker
make ci-env-up project_compose_ci=ci/pod/docker-compose.common.yml
```

This starts the necessary containers including etcd. No manual etcd installation is required.

To stop the services:

```bash
make ci-env-down
```

### Lint Before Committing

**IMPORTANT**: Always lint test files before committing.

```bash
# Lint all code (source + tests)
make lint

# Or run individual lint scripts
./utils/check-lua-code-style.sh      # Lint source code
./utils/check-test-code-style.sh     # Lint test files
```

The `make lint` target:
1. Requires `utils` target (downloads linting utilities)
2. Runs `check-lua-code-style.sh` for source code
3. Runs `check-test-code-style.sh` for test files

Reference: https://github.com/apache/apisix/blob/master/Makefile#L171-L178

## Skippable Steps (Initial Setup)

For initial testing, you can skip these steps from the CI workflow:

1. **WASM-related steps** - Only needed for WASM plugin tests
2. **Start some services** - Only needed for specific integration tests
3. **Build XDS Library** - Only needed for xDS-related tests
4. **Build WASM Core** - Only needed for WASM tests
5. **Dubbo backend** - Only needed for Dubbo plugin tests

## APISIX Deployment Modes

**Reference**: https://apisix.apache.org/docs/apisix/deployment-modes/

APISIX supports three deployment modes:

| Mode          | Description                         | Config Provider |
| ------------- | ----------------------------------- | --------------- |
| `traditional` | Data plane + control plane together | etcd only       |
| `decoupled`   | Separate data/control planes        | etcd only       |
| `standalone`  | Data plane with local file config   | yaml or json    |

### Using YAML Config Provider

**CRITICAL**: Only `data_plane` role supports `config_provider: yaml`.

**CORRECT configuration** (in `conf/config.yaml`):

```yaml
deployment:
  role: data_plane
  role_data_plane:
    config_provider: yaml
```

**INCORRECT** - This does NOT work:

```yaml
# DO NOT USE - traditional role does not support yaml config provider
deployment:
  role: traditional
  role_traditional:
    config_provider: yaml
```

**Symptoms of incorrect configuration:**

1. `config.yaml` gets overwritten when running `apisix start/reload/init`
2. Content configured in `apisix.yaml` has no effect

### YAML Configuration File

When using `config_provider: yaml`:

- Rules are stored in `conf/apisix.yaml`
- File must end with `#END` marker for APISIX to load it
- APISIX checks for changes every second and hot-reloads

Example `conf/apisix.yaml`:

```yaml
routes:
  - uri: /hello
    upstream:
      nodes:
        '127.0.0.1:8080': 1
      type: roundrobin
#END
```

## CI Reference

**IMPORTANT**: Always check the official CI workflow for the latest installation process. The CI scripts are maintained by the APISIX team and are the source of truth.

**Official CI workflow**: https://github.com/apache/apisix/blob/master/.github/workflows/build.yml

**Key CI scripts in the repository:**

| Script                                | Purpose                                                   |
| ------------------------------------- | --------------------------------------------------------- |
| `ci/common.sh`                        | Common utilities, dependency functions, tool installation |
| `ci/linux_openresty_runner.sh`        | Main Linux runner (sources common_runner)                 |
| `ci/linux_openresty_common_runner.sh` | `before_install()`, `do_install()`, `script()` functions  |

**CI Functions:**

- `before_install()` - Installs system dependencies, Test::Nginx
- `do_install()` - Installs OpenResty, etcd, Lua deps, test-nginx, grpcurl, etc.
- `script()` - Runs the actual test suite

**When something doesn't work**: Check if the CI scripts have been updated. The build.yml and CI scripts evolve with the project.

## Troubleshooting

### Test Fails with "nginx: command not found"

Ensure OpenResty is in PATH:

```bash
export PATH=/usr/local/openresty/nginx/sbin:$PATH
which nginx
```

### etcd Connection Failed

Ensure the CI environment is running:

```bash
# Start CI services (includes etcd)
make ci-env-up project_compose_ci=ci/pod/docker-compose.common.yml

# Check if containers are running
docker ps | grep etcd
```

### Permission Denied Errors

Some tests require sudo:

```bash
sudo -E FLUSH_ETCD=1 prove -I./test-nginx/lib -I./ t/path/to/test.t
```

### Missing Lua Dependencies

Reinstall dependencies:

```bash
make deps
```

### Submodule Issues

Re-initialize submodules:

```bash
git submodule update --init --recursive
```

## TEST::NGINX Basics

APISIX tests are written using TEST::NGINX, a Perl-based testing framework.

### Reference Existing Tests First

**IMPORTANT**: When writing new tests, **always reference similar existing tests** in the APISIX repository first.

**Test directory**: https://github.com/apache/apisix/tree/master/t

| Directory | Test Type |
|-----------|-----------|
| `t/plugin/` | Plugin tests (limit-count, key-auth, cors, etc.) |
| `t/admin/` | Admin API tests |
| `t/core/` | Core functionality tests |
| `t/node/` | Node/upstream tests |
| `t/router/` | Router tests |
| `t/stream/` | Stream proxy tests |
| `t/discovery/` | Service discovery tests |
| `t/xrpc/` | xRPC protocol tests |

**How to find similar tests:**

```bash
# Search for tests related to a plugin
ls t/plugin/ | grep -i <keyword>

# Search for specific patterns in test files
grep -r "your_pattern" t/

# Example: Find tests using key-auth
grep -r "key-auth" t/plugin/
```

**Why reference existing tests:**
1. Follow established patterns and conventions
2. Understand how to set up test fixtures
3. Learn correct assertion methods
4. Avoid reinventing test utilities

### Test File Structure

```perl
use t::APISIX 'no_plan';

repeat_each(1);
no_long_string();
no_root_location();

run_tests;

__DATA__

=== TEST 1: test description
--- config
location /t {
    content_by_lua_block {
        -- test code here
    }
}
--- request
GET /t
--- response_body
expected response
--- no_error_log
[error]
```

### Common Test Sections

| Section             | Description                                  |
| ------------------- | -------------------------------------------- |
| `--- config`        | Nginx configuration                          |
| `--- request`       | HTTP request to send                         |
| `--- response_body` | Expected response body                       |
| `--- error_code`    | Expected HTTP status code                    |
| `--- no_error_log`  | Patterns that should NOT appear in error log |
| `--- error_log`     | Patterns that SHOULD appear in error log     |

## Non-Ubuntu Environment Workflow

If you're not on Ubuntu:

1. **Start Ubuntu environment** (VM, container, WSL2)
2. **Run commands there**
3. **If errors occur**: Copy the complete error log
4. **Paste to AI for analysis**: The AI can help diagnose issues without direct execution

Example error sharing format:

```
Command: FLUSH_ETCD=1 prove -I./test-nginx/lib -I./ t/plugin/limit-count.t
Error:
[paste complete error output here]
```
