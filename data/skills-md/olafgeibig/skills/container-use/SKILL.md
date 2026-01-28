---
name: container-use
description: Use this skill when working with Apple Containers (lightweight Linux VMs) as a native Docker replacement on macOS. This includes building container images, running containers, managing container lifecycle, configuring networking, handling volumes, mounting files with SSH forwarding, or performing multi-platform builds. Invoke for tasks involving the container CLI, Apple container tool, or Linux containers on Apple Silicon macOS 26+.
license: Apache-2.0
compatibility: Requires Apple Container tool installed and macOS 26+ (Apple Silicon)
metadata:
  source: https://github.com/olafgeibig/skills
  version: "0.1.1"
---

# Apple Container Usage

Guide for using Apple's `container` tool to run Linux containers on macOS.

## TL;DR

`container` runs Linux containers in lightweight virtual machines (one VM per container) on macOS 26+ (Apple Silicon). It creates a native, secure, and performant alternative to Docker Desktop.

## When to Use

- You want to run Linux containers on macOS without the overhead of Docker Desktop.
- You need strong isolation (VM per container).
- You are developing on macOS 26+ with Apple Silicon.
- You want to build multi-platform images (arm64/amd64).

## Installation

1.  **Download**: Get the latest signed `.pkg` from [GitHub Releases](https://github.com/apple/container/releases).
2.  **Install**: Double-click the `.pkg` and follow instructions.
3.  **Start Service**:
    ```bash
    container system start
    ```

## Common Workflows

### 1. Running Containers

Basic run (similar to Docker):
```bash
# Run interactive alpine shell
container run -it --rm alpine:latest sh

# Run web server detached with port mapping
container run -d --name web -p 8080:80 nginx:latest
```

**Key Options:**
-   `--cpus <count>`: Limit CPUs (default: 4)
-   `--memory <size>`: Limit RAM (default: 1G). e.g., `--memory 4g`
-   `--volume <host>:<container>`: Mount volumes.
    ```bash
    container run -v ~/project:/code python:3.9
    ```
-   `--ssh`: Forward host SSH agent (great for git in containers).
    ```bash
    container run --ssh -it ubuntu git clone git@github.com:me/repo.git
    ```
-   `--mac-address <addr>`: Set custom MAC address.

### 2. Building Images

Builds run in a special builder VM.

```bash
# Build current directory
container build -t my-app:latest .

# Build for multiple architectures
container build --arch arm64 --arch amd64 -t my-app:multi .
```

*Tip: Increase builder resources if builds are slow:*
```bash
container builder start --cpus 8 --memory 16g
```

### 3. Managing State

```bash
# List running containers
container ls

# List all (including stopped)
container ls -a

# Stop/Start
container stop <name>
container start <name>

# View logs
container logs -f <name>

# Monitor stats (CPU/RAM)
container stats
```

### 4. Networking

Apple Containers use `vmnet`. Each network is isolated.

```bash
# Create a new isolated network
container network create backend --subnet 192.168.100.0/24

# Run container in network
container run --network backend nginx
```

## References

- [Tutorial](reference/tutorial.md) - Guided tour of building and running a simple web server.
- [How-to Guide](reference/how-to.md) - Tasks like sharing files, multi-platform builds, and networking.
- [Command Reference](reference/command-reference.md) - Comprehensive list of CLI commands and options.

## Migration from Docker

| Docker Command | Container Command | Notes |
| :--- | :--- | :--- |
| `docker run ...` | `container run ...` | Mostly compatible flags (`-v`, `-p`, `-d`, `-it`) |
| `docker ps` | `container ls` | |
| `docker build ...` | `container build ...` | |
| `docker logs ...` | `container logs ...` | |
| `docker exec ...` | *No direct equivalent yet* | Use ssh or attach if supported, or design containers to not need exec. |
| `docker network ...` | `container network ...` | |

**Key Differences:**
-   **Architecture**: Docker Desktop uses one big VM. `container` uses one lightweight VM *per container*. This improves isolation but changes resource usage patterns.
-   **Storage**: Images and containers are stored in `~/Library/Containers/...`.
-   **Daemon**: The daemon (`vminitd`) runs per-container inside the VM.

## Troubleshooting

**System Logs:**
If something fails, check the system logs:
```bash
container system logs
```

**Uninstall:**
To remove everything (including data):
```bash
/usr/local/bin/uninstall-container.sh -d
```
