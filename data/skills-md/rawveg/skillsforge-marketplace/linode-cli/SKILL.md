---
name: linode-cli
description: Linode CLI Documentation
---

# Linode CLI Skill

The official command-line interface for Linode/Akamai cloud infrastructure. Provides easy access to Linode API endpoints directly from the terminal for managing compute instances, Kubernetes clusters, volumes, networking, DNS, and more.

## When to Use This Skill

This skill should be triggered when:
- **Managing Linode compute instances** (creating, listing, updating, deleting Linodes)
- **Working with Linode Kubernetes Engine (LKE)** clusters and node pools
- **Configuring DNS domains** and records through Linode's DNS Manager
- **Managing Block Storage volumes** and volume attachments
- **Setting up NodeBalancers** and networking infrastructure
- **Automating Linode operations** in scripts or CI/CD pipelines
- **Learning Linode CLI commands** and API interactions
- **Debugging Linode CLI issues** or authentication problems
- **Formatting CLI output** (JSON, tables, custom fields)

## Key Concepts

### CLI Architecture
- **Auto-generated from OpenAPI**: The CLI is automatically generated from Linode's OpenAPI specification, providing direct access to all API endpoints
- **Python-based**: Built with Python 3.10+, installed via pip
- **Command structure**: `linode-cli <resource> <action> [options]`
- **Authentication**: Uses API tokens stored in configuration or environment variables

### Core Resources
- **linodes**: Compute instances (virtual machines)
- **lke**: Linode Kubernetes Engine clusters
- **domains**: DNS domain management
- **volumes**: Block Storage volumes
- **nodebalancers**: Load balancers
- **regions**: Available data center locations
- **images**: OS images and custom images

### Output Formatting
- **Default**: Organized tables with key information
- **--json**: Raw JSON output for scripting
- **--pretty**: Formatted JSON with indentation
- **--format**: Custom field selection
- **--all**: Show all available fields

## Quick Reference

### Installation and Setup

```bash
# Install via pip
pip3 install linode-cli

# First-time configuration (interactive)
linode-cli configure

# Set API token via environment
export LINODE_CLI_TOKEN=your_api_token_here
```

### Getting Help

```bash
# View all available commands
linode-cli --help

# View help for specific resource
linode-cli linodes --help

# View help for specific action
linode-cli linodes create --help

# List all available regions
linode-cli regions list

# List all available images
linode-cli images list
```

### Listing Resources

```bash
# List all Linodes on your account
linode-cli linodes list

# List domains
linode-cli domains list

# List volumes
linode-cli volumes list

# List Kubernetes clusters
linode-cli lke clusters-list

# Format output with custom fields
linode-cli linodes list --format "id,label,status,region"

# Output as JSON
linode-cli linodes list --json

# Output all available fields
linode-cli linodes list --all
```

### Creating Compute Instances

```bash
# Create a basic Linode (uses defaults from config)
linode-cli linodes create \
  --type g6-standard-2 \
  --region us-east \
  --image linode/debian11 \
  --label my-server \
  --root_pass "SecurePassword123!"

# Create with specific configuration
linode-cli linodes create \
  --type g6-standard-4 \
  --region us-central \
  --image linode/ubuntu22.04 \
  --label production-web \
  --root_pass "MySecurePass!" \
  --group webservers

# Create with authorized SSH keys
linode-cli linodes create \
  --type g6-standard-2 \
  --region us-west \
  --image linode/debian11 \
  --label secure-server \
  --root_pass "Password123!" \
  --authorized_keys "ssh-rsa AAAAB3Nz..."
```

### Managing Kubernetes (LKE)

```bash
# Create a Kubernetes cluster with multiple node pools
linode-cli lke cluster-create \
  --label my-k8s-cluster \
  --region us-central \
  --k8s_version 1.28 \
  --node_pools.type g6-standard-4 --node_pools.count 3 \
  --node_pools.type g6-standard-8 --node_pools.count 2 \
  --tags production

# List all clusters
linode-cli lke clusters-list

# Update cluster configuration
linode-cli lke cluster-update $CLUSTER_ID \
  --label renamed-cluster \
  --tags production \
  --tags monitoring \
  --tags backup

# Update node pool size
linode-cli lke pool-update $CLUSTER_ID $POOL_ID \
  --count 5

# Delete a cluster
linode-cli lke cluster-delete $CLUSTER_ID
```

### DNS Management

```bash
# Create a domain
linode-cli domains create \
  --type master \
  --domain example.com \
  --soa_email admin@example.com

# List domains
linode-cli domains list

# Create DNS record
linode-cli domains records-create $DOMAIN_ID \
  --type A \
  --name www \
  --target 192.0.2.1

# Delete a domain
linode-cli domains delete $DOMAIN_ID
```

### Volume Management

```bash
# Create a Block Storage volume
linode-cli volumes create \
  --label my-volume \
  --size 100 \
  --region us-east

# List volumes
linode-cli volumes list

# Attach volume to Linode
linode-cli volumes attach $VOLUME_ID \
  --linode_id $LINODE_ID

# Detach volume
linode-cli volumes detach $VOLUME_ID
```

### Advanced Usage

```bash
# Filtering output with jq (requires jq installed)
linode-cli linodes list --json | jq '.[] | select(.status=="running")'

# Using variables in scripts
LINODE_ID=$(linode-cli linodes list --json | jq -r '.[0].id')
echo "First Linode ID: $LINODE_ID"

# Bulk operations example
for region in us-east us-west eu-central; do
  linode-cli linodes create \
    --type g6-nanode-1 \
    --region $region \
    --image linode/alpine3.18 \
    --label "test-$region" \
    --root_pass "TempPassword123!"
done
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **other.md** - Links to official Linode CLI Wiki on GitHub with additional documentation, guides, and community resources

Use `view` to read specific reference files when detailed information is needed.

## Working with This Skill

### For Beginners
1. **Start with installation**: Run `pip3 install linode-cli` and configure with `linode-cli configure`
2. **Learn the basics**: Use `--help` flag extensively to discover available commands
3. **Practice listing**: Start with simple list commands like `linode-cli linodes list`
4. **Test in safe mode**: Use small, inexpensive instance types (g6-nanode-1) for testing
5. **Read the output**: Default table output is designed to be human-readable

### For Intermediate Users
1. **Master output formatting**: Learn `--json`, `--format`, and `--all` flags for scripting
2. **Automate common tasks**: Create bash scripts for repetitive operations
3. **Combine with jq**: Use jq for powerful JSON filtering and processing
4. **Manage multiple resources**: Create infrastructure as code with shell scripts
5. **Use environment variables**: Set `LINODE_CLI_TOKEN` for non-interactive automation

### For Advanced Users
1. **CI/CD integration**: Incorporate linode-cli into deployment pipelines
2. **Infrastructure automation**: Build complete infrastructure provisioning scripts
3. **API exploration**: Use the CLI to understand Linode's API structure
4. **Custom tooling**: Wrap linode-cli in your own management tools
5. **OpenAPI access**: Contribute to the OpenAPI spec for new features

### Navigation Tips
- **Discover resources**: Use `linode-cli --help` to see all available resource types
- **Action discovery**: Each resource has different actions (list, create, update, delete, etc.)
- **Parameter help**: Use `--help` on any action to see required and optional parameters
- **JSON inspection**: Use `--json` to see all available fields for any resource
- **Region planning**: Run `linode-cli regions list` before creating resources

## Common Patterns

### Authentication Setup
```bash
# Method 1: Interactive configuration
linode-cli configure

# Method 2: Environment variable
export LINODE_CLI_TOKEN=your_token_here

# Method 3: Config file (~/.config/linode-cli)
[DEFAULT]
token = your_token_here
region = us-east
type = g6-standard-2
image = linode/ubuntu22.04
```

### Instance Lifecycle
```bash
# Create → Boot (automatic) → Use → Power off → Delete
linode-cli linodes create --label test --type g6-nanode-1 --region us-east --image linode/alpine3.18 --root_pass "Test123!"
# Get ID from output or list
LINODE_ID=$(linode-cli linodes list --json | jq -r '.[] | select(.label=="test") | .id')
# Shutdown
linode-cli linodes shutdown $LINODE_ID
# Delete
linode-cli linodes delete $LINODE_ID
```

### Scripting Pattern
```bash
#!/bin/bash
set -e  # Exit on error

# Configuration
REGION="us-central"
TYPE="g6-standard-2"
IMAGE="linode/debian11"

# Create instance
echo "Creating Linode..."
RESULT=$(linode-cli linodes create \
  --type "$TYPE" \
  --region "$REGION" \
  --image "$IMAGE" \
  --label "auto-server-$(date +%s)" \
  --root_pass "$(openssl rand -base64 32)" \
  --json)

# Extract ID
LINODE_ID=$(echo "$RESULT" | jq -r '.[0].id')
echo "Created Linode ID: $LINODE_ID"

# Wait for running status
while true; do
  STATUS=$(linode-cli linodes view $LINODE_ID --json | jq -r '.[0].status')
  echo "Status: $STATUS"
  [[ "$STATUS" == "running" ]] && break
  sleep 5
done

echo "Linode is ready!"
```

## Resources

### Official Documentation
- **GitHub Repository**: https://github.com/linode/linode-cli
- **Akamai TechDocs**: https://techdocs.akamai.com/cloud-computing/docs/cli
- **API Documentation**: https://www.linode.com/docs/api/
- **Getting Started Guide**: https://techdocs.akamai.com/cloud-computing/docs/getting-started-with-the-linode-cli

### Key Features
- **Auto-completion**: Bash completion available for command discovery
- **OpenAPI-driven**: Always up-to-date with latest API features
- **Cross-platform**: Works on Linux, macOS, and Windows (via WSL)
- **Scriptable**: Perfect for automation and infrastructure as code
- **Comprehensive**: Access to all Linode API endpoints

### Community
- **Contributors**: 49 active contributors
- **License**: BSD-3-Clause
- **Language**: Python (98.8%)
- **Installation**: PyPI package (pip installable)

## Tips and Best Practices

### Security
- **Protect tokens**: Never commit API tokens to version control
- **Use environment variables**: Store tokens in `.env` files (git-ignored)
- **Rotate regularly**: Generate new tokens periodically
- **Limit permissions**: Use scoped tokens with minimal required permissions
- **Strong passwords**: Always use strong root passwords for instances

### Cost Management
- **Start small**: Use nanode instances (g6-nanode-1) for testing
- **Delete unused**: Remove test instances to avoid unnecessary charges
- **Monitor usage**: Regularly check your account for active resources
- **Use tags**: Organize resources with tags for easier management

### Debugging
- **Verbose output**: Add `--debug` flag for detailed error information
- **JSON inspection**: Use `--json --pretty` to see full API responses
- **Check status**: Use `view` commands to inspect resource details
- **API reference**: Consult the API docs for endpoint specifics

## Troubleshooting

### Authentication Issues
```bash
# Verify token is set
echo $LINODE_CLI_TOKEN

# Test authentication
linode-cli account view

# Reconfigure CLI
linode-cli configure
```

### Common Errors
- **401 Unauthorized**: Invalid or expired API token
- **404 Not Found**: Resource ID doesn't exist or wrong region
- **422 Unprocessable**: Missing required parameters or validation error
- **429 Rate Limited**: Too many requests, implement backoff

### Getting Help
```bash
# Check CLI version
linode-cli --version

# View debug information
linode-cli linodes list --debug

# Check configuration
cat ~/.config/linode-cli
```

## Notes

- This skill was generated from official Linode CLI documentation
- The CLI is automatically generated from Linode's OpenAPI specification
- All commands and examples are based on the official Linode API v4
- Command syntax and available options may change with API updates
- Always refer to `--help` for the most current command documentation

## Updating

To stay current with Linode CLI:
```bash
# Update via pip
pip3 install --upgrade linode-cli

# Check for new features
linode-cli --help

# Review changelog
pip3 show linode-cli
```

The CLI is regularly updated to reflect changes in the Linode API. Check the GitHub repository for release notes and breaking changes.
