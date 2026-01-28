---
name: vastai-api
description: Vast.ai API Documentation - Affordable GPU Cloud Marketplace
---

# Vastai-Api Skill

Comprehensive assistance with the Vast.ai API for managing GPU instances, machine operations, and automating AI/ML workflows. This skill provides access to official documentation for programmatically controlling the Vast.ai platform.

## When to Use This Skill

This skill should be triggered when working with:
- **GPU Instance Management**: Creating, destroying, starting, stopping, or managing GPU instances
- **Machine Operations**: Listing machines for rent, setting pricing, managing maintenance windows
- **SSH & Authentication**: Managing SSH keys, API keys, and secure connections to instances
- **Billing & Credits**: Viewing invoices, earnings, deposits, or transferring credits
- **Network Volumes**: Creating, listing, or managing network storage volumes
- **Serverless Endpoints**: Working with Vast.ai serverless workergroups and endpoints
- **Data Transfer**: Copying data between instances or cloud services
- **Account Management**: Managing subaccounts, environment variables, or team roles
- **CLI Operations**: Using the `vastai` command-line tool
- **API Integration**: Building applications that integrate with Vast.ai's REST API

## Quick Reference

### Creating and Managing Instances

#### Create a New GPU Instance
```bash
# Create instance from an offer
vastai create instance <offer_id> \
  --image pytorch/pytorch:latest \
  --disk 50 \
  --ssh
```

#### List Your Active Instances
```bash
# Show all instances
vastai show instances

# Show specific instance details
vastai show instance <instance_id>
```

#### Manage Instance State
```bash
# Stop an instance (pause GPU billing, storage still charged)
vastai stop instance <instance_id>

# Start a stopped instance
vastai start instance <instance_id>

# Reboot instance without losing GPU priority
vastai reboot instance <instance_id>

# Destroy instance permanently (irreversible)
vastai destroy instance <instance_id>
```

### SSH Key Management

#### Add SSH Key to Account
```bash
# Add your public SSH key
vastai create ssh-key "ssh-rsa AAAAB3NzaC1yc2EA... user@host"

# List all SSH keys
vastai show ssh-keys

# Attach SSH key to specific instance
vastai attach ssh <instance_id> <ssh_key>
```

### Search and Filter Offers

#### Search for GPU Offers
```bash
# Search with filters
vastai search offers \
  --gpu_name RTX_4090 \
  --num_gpus 2 \
  --disk_space 100

# Order by price
vastai search offers --order dph_total
```

### Environment Variables (Secrets)

#### Manage Environment Variables
```bash
# Create encrypted environment variable
vastai create env-var MY_API_KEY "secret_value_here"

# List all environment variables
vastai show env-vars

# Update existing variable
vastai update env-var MY_API_KEY "new_secret_value"

# Delete environment variable
vastai delete env-var MY_API_KEY
```

### Billing and Credits

#### View Billing Information
```bash
# Show invoices
vastai show invoices

# Show earnings (for hosts)
vastai show earnings

# Show deposit for specific instance
vastai show deposit <instance_id>

# Transfer credits to another user
vastai transfer credit recipient@email.com 25.00
```

### Instance Logs

#### Retrieve Container Logs
```bash
# Get last 100 lines of logs
vastai show logs <instance_id> --tail 100

# Filter logs with grep pattern
vastai show logs <instance_id> --filter "error"

# Get daemon system logs
vastai show logs <instance_id> --daemon-logs
```

### Data Transfer Operations

#### Copy Between Instances
```bash
# Copy from one instance to another
vastai copy <src_id> <dst_id> /source/path /destination/path

# Cloud copy using rclone
vastai cloud copy <instance_id> remote:bucket/path /local/path
```

### Machine Management (for Hosts)

#### List Your Machine for Rent
```bash
# List machine with pricing
vastai list machine <machine_id> \
  --price_gpu 0.50 \
  --price_disk 0.10

# Unlist machine (stop renting)
vastai unlist machine <machine_id>

# Schedule maintenance window
vastai schedule maint <machine_id> \
  --sdate "2025-11-01T10:00:00" \
  --duration 3600
```

## Key Concepts

### Instance Types
- **On-Demand Instances**: Pay-as-you-go GPU instances you create and manage
- **Interruptible Instances**: Lower-cost instances that can be reclaimed by hosts
- **Reserved Instances**: Pre-paid instances with usage discounts (up to 40%)

### Pricing Model
- **GPU Pricing**: Charged per hour while instance is running
- **Storage Pricing**: Charged for disk space even when instance is stopped
- **Network Transfer**: Upload/download bandwidth costs
- **Discounts**: Available through prepayment on reserved instances

### Instance States
- `starting`: Instance is initializing
- `running`: Instance is active and billable
- `stopped`: Container stopped (storage still billable)
- `exited`: Container exited or failed
- `rebooting`: In process of restarting
- `recycling`: Being destroyed and recreated from fresh image

### Authentication
- **API Keys**: Used for programmatic access via REST API
- **SSH Keys**: For secure shell access to running instances
- **Environment Variables**: Encrypted secrets injected into containers

### Templates
Pre-configured setups containing:
- Docker image specifications
- Environment variables
- Onstart scripts
- Resource requirements
- Port mappings

Popular templates include PyTorch, TensorFlow, Jupyter, ComfyUI, and Stable Diffusion.

### Network Volumes
Shared network storage that can be:
- Attached to multiple instances
- Persisted independently of instance lifecycle
- Used for datasets and model weights
- Scaled independently

### Serverless Architecture
- **Endpoints**: Top-level routing and configuration
- **Workergroups**: Pools of GPU instances that autoscale
- **Test Workers**: Exploration phase for performance profiling
- **Target Utilization**: Controls scaling behavior

## Reference Files

This skill includes comprehensive documentation in `references/`:

### llms-full.md
Complete API reference with all endpoints organized by category:
- **Accounts**: API keys, SSH keys, user management, subaccounts
- **Billing**: Invoices, earnings, deposits, credit transfers
- **Instances**: Create, manage, destroy, reboot, logs, SSH
- **Machines**: List for rent, pricing, maintenance, default jobs
- **Network Volumes**: Create, list, manage shared storage
- **Search**: Find offers, benchmarks, filter GPU availability
- **Serverless**: Endpoints, workergroups, autoscaling configuration

Each endpoint includes:
- HTTP method and path
- Detailed description
- CLI usage examples
- Parameter specifications
- Source documentation links

### llms-txt.md
Focused documentation covering:
- Serverless workergroup parameters and configuration
- Endpoint management
- QuickStart guide with setup instructions
- Common questions and answers
- Schema.org structured data for better searchability

### llms.md
Curated list of all API operations with brief descriptions and CLI examples, organized by category for quick lookup.

## Working with This Skill

### For Beginners

**Start here:**
1. Review the QuickStart section in `llms-txt.md`
2. Follow the 4-step setup process (signup, add credit, prepare SSH, create instance)
3. Try the basic examples in Quick Reference above
4. Learn about instance states and pricing model in Key Concepts

**First tasks to try:**
- Create an API key for authentication
- Add your SSH public key to your account
- Search for available GPU offers
- Create your first instance with a template

### For Intermediate Users

**Focus on:**
- Environment variable management for secrets
- Data transfer between instances and cloud storage
- Instance lifecycle management (stop/start/reboot vs destroy)
- Billing optimization with reserved instances
- Custom template creation for your workflows

**Useful patterns:**
- Set up auto-billing to avoid instance interruptions
- Use environment variables for API keys and credentials
- Schedule regular backups with copy commands
- Monitor costs with invoice and earnings endpoints

### For Advanced Users

**Advanced topics:**
- Serverless endpoint and workergroup configuration
- Machine hosting and marketplace optimization
- Network volume architecture for shared datasets
- Team and subaccount management
- API integration in custom applications
- Automated scaling strategies

**Power user tips:**
- Use filter operators in search (eq, neq, gt, lt, gte, lte, in, nin)
- Leverage launch_args for advanced instance customization
- Implement monitoring and alerting via logs API
- Optimize costs with bid price adjustments
- Build workflows with cloud copy for data pipelines

### Navigation Tips

**Finding API endpoints:**
- All endpoints documented in `llms-full.md` with full details
- Organized by category (accounts, billing, instances, machines, etc.)
- Each includes CLI usage examples

**Quick lookups:**
- `llms.md` provides condensed list of all operations
- Use browser search (Ctrl+F) to find specific commands
- Look for "CLI Usage:" sections for command syntax

**Understanding concepts:**
- Key Concepts section above for terminology
- QuickStart in `llms-txt.md` for getting started
- Workergroup Parameters section for serverless configuration

## Common Workflows

### Setting Up a New Development Environment
1. Create API key with appropriate permissions
2. Add SSH key to account for access
3. Create environment variables for secrets
4. Search for GPU offers matching requirements
5. Create instance from template
6. Connect via SSH and verify setup

### Managing Long-Running Training Jobs
1. Create instance with sufficient disk space
2. Set up auto-billing to prevent interruptions
3. Use reserved instance with prepayment for discounts
4. Monitor with logs endpoint
5. Copy model checkpoints to cloud storage
6. Stop (not destroy) when paused to save costs

### Hosting Machines for Profit
1. Set machine pricing with list command
2. Define minimum bid thresholds
3. Configure default jobs for background work
4. Schedule maintenance windows when needed
5. Monitor earnings and clean up expired contracts
6. Adjust pricing based on market conditions

## Best Practices

### Cost Management
- **Destroy vs Stop**: Use stop for short pauses, destroy for long breaks
- **Disk Space**: Choose carefully - cannot be changed later
- **Reserved Instances**: Prepay for 40% discount on long-running work
- **Auto-billing**: Set threshold above daily spend to prevent interruptions
- **Low Balance Alerts**: Enable email notifications as backup

### Security
- **API Keys**: Use permission scoping, rotate regularly
- **SSH Keys**: Use different keys for different purposes
- **Environment Variables**: Store secrets as encrypted env vars
- **Subaccounts**: Use for team members with restricted access

### Performance
- **Template Caching**: Pre-pulled images start much faster (seconds vs minutes)
- **Network Volumes**: Use for large datasets shared across instances
- **Bid Pricing**: Higher bids get better hardware availability
- **Test Workers**: Let serverless explore before scaling

### Reliability
- **Logs**: Monitor regularly for errors
- **Health Checks**: Implement in your applications
- **Data Backup**: Copy critical data off instances regularly
- **Redundancy**: For critical work, run on multiple instances

## Resources

### Official Links
- **Console**: https://cloud.vast.ai/
- **API Docs**: https://docs.vast.ai/
- **Postman Collection**: https://www.postman.com/vast33/vast-ai-public-api-docs
- **Templates**: https://cloud.vast.ai/templates/
- **Search**: https://cloud.vast.ai/create/

### Support
- Minimum deposit: $5
- Balance shown at top right of dashboard
- Email verification required to rent or create teams
- Auto-billing prevents interruptions when configured

## Notes

- This skill was automatically generated from official Vast.ai documentation
- Reference files preserve structure and examples from source docs
- CLI examples use the `vastai` command-line tool
- API endpoints support both REST API and CLI access
- All prices in USD, billed per hour for compute and storage

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest API information
3. Check for API version changes or deprecated endpoints
