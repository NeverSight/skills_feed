---
name: apple-container-skill
description: Interact with the Apple Container CLI to manage containers, images, volumes, networks, and system services on macOS. Use this skill when the user asks to run, build, or inspect containers or manage the container runtime.
---

# Apple Container Skill

To use the Apple Container CLI, execute the commands below using the `run_shell_command` tool.
**Note:** This CLI is specific to Apple's container implementation.

## Common Workflows & Architecture
These patterns represent best practices for using the Apple Container CLI effectively.

### 1. System Lifecycle Management
Unlike standard Docker Desktop, the container system services are explicit.
*   **Startup:** Always verify `container system status` before running operations. If stopped, run `container system start`.
*   **Kernel:** On first run, `system start` may prompt to install a Linux kernel. The agent should be aware of this initialization step.
*   **Cleanup:** To save resources when not in use, run `container system stop`.

### 2. Networking & Connectivity
*   **DNS:** For stable service discovery, configure a local domain:
    1.  `sudo container system dns create <domain>` (e.g., `test`)
    2.  `container system property set dns.domain <domain>`
    3.  Access containers via `http://<container-name>.<domain>`.
*   **Inter-Container:** Containers are on a `vmnet`. Direct IP communication (`192.168.64.x`) works but can be fragile due to isolation.
*   **Host Gateway Strategy (Reliable Fallback):** If network plugins are missing or you encounter "No route to host":
    1.  Publish the service port to the host (e.g., `-p 5432:5432`).
    2.  Connect from other containers using the **Host Gateway IP** (`192.168.64.1`).
    3.  *Note:* Disable SSL (`sslmode=disable`) if connection resets occur via the gateway.
*   **Localhost:** Port forwarding (`-p 8080:80`) works as expected for accessing containers from the host.

### 3. Data Persistence
*   **Volume Initialization:** New volumes may contain a `lost+found` directory, which can cause "directory not empty" errors.
*   **Best Practice:** Always configure services (like PostgreSQL) to use a **subdirectory** within the volume.
    *   *Example:* `PGDATA=/var/lib/postgresql/data/pgdata` instead of the root mount point.

### 4. Development Patterns
*   **Git/SSH:** Use the `--ssh` flag (`container run --ssh ...`) to forward the host's SSH agent. This is the preferred method for cloning private repositories inside containers.
*   **Hot Reloading:** Use `--volume` (e.g., `-v $(pwd):/app`) to mount source code for immediate feedback, just like standard Docker.
*   **Builder Tuning:** The build process runs in its own VM. For large builds, explicitly scale the builder: `container builder start --cpus 4 --memory 8g`.

## Critical Setup
Before running containers, the system services usually need to be running.
*   **Check Status:** `container system status`
*   **Start Services:** `container system start` (may require `sudo` if installing kernel/root components, but usually run as user)

## Commands

### System Management

*   **`container system start`**: Starts the container services.
    *   Options: `--enable-kernel-install`, `--disable-kernel-install`, `--app-root <path>`, `--install-root <path>`.
*   **`container system stop`**: Stops the container services.
    *   Options: `--prefix <string>`.
*   **`container system status`**: Checks if services are running.
*   **`container system version`**: Shows CLI and API server versions.
*   **`container system logs`**: Displays system logs.
    *   Options: `--follow`, `--last <time>` (e.g., `5m`, `1h`).
*   **`container system df`**: Shows disk usage.
*   **`container system dns create <domain>`**: Creates a local DNS domain (requires sudo).
*   **`container system dns list`**: Lists configured local DNS domains.
*   **`container system dns delete <domain>`**: Deletes a local DNS domain (requires sudo).
*   **`container system property list`**: Lists system properties (config).
*   **`container system property get <id>`**: Gets a system property value.
*   **`container system property set <id> <value>`**: Sets a system property.
    *   Examples: `container system property set dns.domain my.local`
*   **`container system property clear <id>`**: Resets a system property to default.
*   **`container system kernel set`**: Installs/updates the Linux kernel.
    *   Options: `--recommended`, `--arch <arch>`, `--binary <path>`.

### Container Lifecycle

*   **`container run [OPTIONS] IMAGE [COMMAND] [ARG...]`**: Runs a command in a new container.
    *   **Common Options:**
        *   `-d, --detach`: Run in background.
        *   `-i, --interactive`: Keep STDIN open.
        *   `-t, --tty`: Allocate a pseudo-TTY.
        *   `-p, --publish <host-port:container-port>`: Publish a port.
        *   `-v, --volume <host-path:container-path>`: Mount a volume.
        *   `--name <string>`: Assign a name.
        *   `--rm`: Remove after stop.
        *   `-e, --env <key=value>`: Set environment variable.
        *   `-u, --user <user>`: Set user (name|uid[:gid]).
        *   `-w, --workdir <dir>`: Set working directory.
        *   `-c, --cpus <count>`: CPU limit.
        *   `-m, --memory <size>`: Memory limit (e.g., `512M`, `2G`).
*   **`container create [OPTIONS] IMAGE [ARG...]`**: Creates a container without starting it (same options as `run`).
*   **`container start [OPTIONS] CONTAINER...`**: Starts stopped containers.
    *   Options: `-a, --attach`, `-i, --interactive`.
*   **`container stop [OPTIONS] CONTAINER...`**: Stops running containers.
    *   Options: `-t, --time <seconds>` (wait before kill), `-s, --signal <signal>`.
*   **`container kill [OPTIONS] CONTAINER...`**: Kills containers immediately.
    *   Options: `-s, --signal <signal>`.
*   **`container delete [OPTIONS] CONTAINER...`**: Deletes containers (aliases: `rm`).
    *   Options: `-f, --force` (delete even if running).
*   **`container exec [OPTIONS] CONTAINER COMMAND [ARG...]`**: Executes a command in a running container.
    *   Options: `-it`, `-d`, `-w`, `-e`, `-u, --user`.
*   **`container list [OPTIONS]`**: Lists containers (aliases: `ls`, `ps`).
    *   Options: `-a, --all` (show stopped too), `-q` (quiet, IDs only).
*   **`container inspect CONTAINER...`**: JSON details of containers.
*   **`container logs [OPTIONS] CONTAINER`**: Fetches container logs.
    *   Options: `-f, --follow`, `--tail <n>`, `--boot` (show boot logs).
*   **`container stats`**: Live stream of resource usage.
    *   Options: `--no-stream`.

### Image Management

*   **`container build [OPTIONS] PATH`**: Builds an image from a Dockerfile.
    *   Options: `-t <tag>`, `-f <dockerfile>`, `--build-arg <key=val>`, `--no-cache`, `-o, --output <type>`.
*   **`container image pull [OPTIONS] NAME[:TAG]`**: Pulls an image from a registry.
    *   Options: `--platform <os/arch>`, `--arch <arch>`, `--os <os>`.
*   **`container image push NAME[:TAG]`**: Pushes an image.
*   **`container image list`**: Lists local images (aliases: `ls`, `images`).
*   **`container image delete IMAGE...`**: Deletes images (aliases: `rm`, `rmi`).
*   **`container image prune`**: Removes unused images.
*   **`container image tag SOURCE TARGET`**: Tags an image.
*   **`container image inspect IMAGE...`**: JSON details of images.
*   **`container image save -o <path> IMAGE`**: Saves image to tar.
    *   Options: `--platform <os/arch>`.
*   **`container image load -i <path>`**: Loads image from tar.

### Volume Management

*   **`container volume create [OPTIONS] NAME`**: Creates a volume.
    *   Options: `-s, --size <size>`, `--label <key=val>`.
*   **`container volume list`**: Lists volumes (aliases: `ls`).
*   **`container volume inspect NAME...`**: JSON details.
*   **`container volume delete NAME...`**: Deletes volumes (aliases: `rm`).
*   **`container volume prune`**: Removes unused volumes.

### Network Management

*   **`container network create NAME`**: Creates a network.
    *   Options: `--subnet <cidr>`, `--subnet-v6 <cidr>`, `--label <key=val>`.
*   **`container network list`**: Lists networks (aliases: `ls`).
*   **`container network inspect NAME...`**: JSON details.
*   **`container network delete NAME...`**: Deletes networks (aliases: `rm`).
*   **`container network prune`**: Removes unused networks.

### Registry & Builder

*   **`container registry login SERVER`**: Log in to a registry.
    *   Options: `-u <username>`, `--password-stdin`, `--scheme <auto|https|http>`.
*   **`container registry logout SERVER`**: Log out.
*   **`container builder status`**: Check BuildKit builder status.
*   **`container builder start`**: Start the builder manually.
    *   Options: `--cpus <count>`, `--memory <size>`.
*   **`container builder stop`**: Stops the builder.
*   **`container builder delete`**: Deletes the builder.
*   **`container builder prune`**: Clear builder cache.