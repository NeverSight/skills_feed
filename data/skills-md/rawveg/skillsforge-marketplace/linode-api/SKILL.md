---
name: linode-api
description: Linode API Documentation
---

# Linode-Api Skill

Comprehensive assistance with the Linode API - a RESTful API for programmatically managing Linode cloud infrastructure including compute instances, networking, storage, domains, and billing.

## When to Use This Skill

This skill should be triggered when:
- Working with Linode cloud infrastructure programmatically
- Creating, managing, or monitoring Linode instances (virtual machines)
- Automating Linode infrastructure with API calls
- Implementing Linode OAuth applications
- Managing Linode account, billing, or payment methods
- Working with Linode networking (DNS, NodeBalancers, VLANs)
- Debugging Linode API authentication or request issues
- Implementing infrastructure as code with Linode
- Integrating Linode services into applications
- Managing Linode Kubernetes Engine (LKE) clusters

## Quick Reference

### Authentication with Personal Access Token

```python
from linode import LinodeClient

# Initialize client with your personal access token
token = "your-personal-access-token"
client = LinodeClient(token)
```

**Getting a token:** Log into cloud.linode.com → Profile → "Create a Personal Access Token"

### List All Linode Instances

```python
# Retrieve all Linodes on your account
my_linodes = client.linode.get_instances()

# Iterate and display instance labels
for linode in my_linodes:
    print(linode.label)
```

### Create a New Linode Instance (Python)

```python
# Get available regions
available_regions = client.get_regions()
chosen_region = available_regions[0]

# Create instance with region, type, and image
new_linode, password = client.linode.create_instance(
    chosen_region,
    'g5-standard-4',
    image='linode/debian9'
)

# Display SSH connection info
print(f"ssh root@{new_linode.ipv4[0]} - {password}")
```

### Create a Linode Instance (cURL)

```bash
curl -X POST https://api.linode.com/v4/linode/instances \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "g5-standard-2",
    "region": "us-east",
    "image": "linode/debian12",
    "root_pass": "secure_password_here",
    "label": "prod-web-1"
  }'
```

### Get Account Information

```bash
curl https://api.linode.com/v4/account \
  -H "Authorization: Bearer <your-token>"
```

### List Invoices

```bash
curl https://api.linode.com/v4/account/invoices \
  -H "Authorization: Bearer <your-token>"
```

### Check Regional Service Availability

```bash
curl https://api.linode.com/v4/account/availability \
  -H "Authorization: Bearer <your-token>"
```

### Install Python Library

```bash
# Install the official Python library
pip install linode-api

# Or from source
git clone git@github.com:Linode/python-linode-api
cd python-linode-api
python setup.py install
```

### Basic Python Setup Pattern

```python
from linode import LinodeClient

# Initialize the client
token = "your-personal-access-token"
client = LinodeClient(token)

# Now you can access resources
regions = client.get_regions()
instances = client.linode.get_instances()
```

### Authentication Header Format (REST)

All API requests to non-public resources must include an Authorization header:

```
Authorization: Bearer <your-personal-access-token>
```

## Key Concepts

### API Versions
- **v4**: Current stable API version (base URL: `https://api.linode.com/v4`)
- **v4beta**: Beta features and endpoints (use with caution in production)

### Authentication
The Linode API uses **Personal Access Tokens** (PATs) for authentication. Tokens can have different permission scopes (read/write) for different resource types. Always keep tokens secure and never commit them to version control.

### Pagination
API responses use envelope-based pagination with metadata:
- `page`: Current page number
- `pages`: Total number of pages
- `results`: Number of results per page

### Filtering
The API supports advanced filtering via the `X-Filter` header with operators:
- `+gt`: Greater than
- `+lte`: Less than or equal
- `+or`: Logical OR
- Complex nested conditions supported

### Instance Types
Common Linode instance types:
- **Shared CPU**: `g5-standard-1`, `g5-standard-2`, etc. (cost-effective for general workloads)
- **Dedicated CPU**: `g6-dedicated-2`, etc. (guaranteed CPU resources)
- **High Memory**: `g6-highmem-1`, etc. (memory-intensive applications)

### Regions
Linode has global data centers. Common regions:
- `us-east`: Newark, NJ
- `us-west`: Fremont, CA
- `eu-west`: London, UK
- `ap-south`: Singapore
- Many more available via `GET /regions` endpoint

### Images
Supported operating system images:
- `linode/debian12`: Debian 12
- `linode/ubuntu22.04`: Ubuntu 22.04 LTS
- `linode/centos-stream9`: CentOS Stream 9
- Custom images also supported

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **api.md** - Complete OpenAPI specification reference with all endpoints, request/response schemas, and authentication details

Use `view references/api.md` when you need:
- Detailed endpoint specifications
- Request/response schema definitions
- Available HTTP methods for each endpoint
- Field validation rules and constraints
- OAuth client configuration details
- Beta feature documentation

## Working with This Skill

### For Beginners

1. **Start with authentication**: Generate a Personal Access Token from cloud.linode.com
2. **Test basic endpoints**: Try `GET /account` to verify your token works
3. **Use the Python library**: It's easier than raw REST API calls for getting started
4. **Start small**: List existing resources before creating new ones
5. **Check regional availability**: Ensure services are available in your chosen region

### For API Integration

1. **Review authentication patterns** in the Quick Reference section
2. **Use the Python client library** for rapid development
3. **Implement proper error handling** for API rate limits and validation errors
4. **Store tokens securely** using environment variables or secret management
5. **Test in non-production** accounts first

### For Infrastructure Automation

1. **Explore the full API specification** in references/api.md
2. **Use filtering and pagination** for large resource queries
3. **Implement idempotent operations** where possible
4. **Monitor API usage** to stay within rate limits
5. **Use OAuth** for multi-user applications

### Common Workflows

**Basic Instance Management:**
1. List available regions → Choose region
2. List available instance types → Choose type
3. List available images → Choose image
4. Create instance with chosen parameters
5. Monitor instance status until "running"
6. Retrieve IP address and connect

**Account Management:**
1. Get account information
2. List invoices and payment history
3. Check service availability by region
4. Manage OAuth clients for applications
5. View notifications and events

## Resources

### Official Documentation
- **API Reference**: https://www.linode.com/docs/api/
- **Getting Started Guide**: https://www.linode.com/docs/products/tools/api/get-started/
- **Python Library Docs**: https://python-linode-api.readthedocs.io/

### Code Libraries
- **Python**: `linode-api` (official)
- **JavaScript/Node.js**: Available via npm
- **Go, PHP, Ruby**: Community libraries available

### references/
The `references/api.md` file contains:
- Complete OpenAPI specification (JSON format)
- All available endpoints organized by resource type
- Detailed request/response schemas
- Authentication requirements per endpoint
- Field validation rules and data types
- Pagination and filtering documentation
- Beta feature flags

## Best Practices

### Security
- Never hardcode API tokens in your code
- Use environment variables: `token = os.getenv('LINODE_API_TOKEN')`
- Set appropriate token scopes (read-only when possible)
- Rotate tokens regularly
- Revoke unused tokens

### Error Handling
- Handle HTTP 429 (rate limit) with exponential backoff
- Validate input before making API calls
- Check for field validation errors in 400 responses
- Implement retry logic for transient failures

### Performance
- Use pagination for large result sets
- Implement caching for infrequently-changing data (regions, types)
- Use batch operations when available
- Filter results server-side using X-Filter header

### Code Organization
- Create wrapper functions for common operations
- Separate configuration from application code
- Use type hints with the Python library
- Document token permission requirements

## Notes

- This skill was automatically generated from the official Linode API OpenAPI specification
- The API uses standard REST conventions (GET, POST, PUT, DELETE)
- All non-public endpoints require authentication via Bearer token
- Rate limits apply - implement appropriate backoff strategies
- Beta endpoints (v4beta) may change without notice
- The Python library handles pagination and authentication automatically

## Common Operations Reference

### Compute Instances
- List instances: `GET /linode/instances`
- Create instance: `POST /linode/instances`
- Get instance: `GET /linode/instances/{linodeId}`
- Update instance: `PUT /linode/instances/{linodeId}`
- Delete instance: `DELETE /linode/instances/{linodeId}`
- Reboot instance: `POST /linode/instances/{linodeId}/reboot`

### Account & Billing
- Get account: `GET /account`
- List invoices: `GET /account/invoices`
- List payments: `GET /account/payments`
- Get settings: `GET /account/settings`

### Networking
- List NodeBalancers: `GET /nodebalancers`
- List Firewalls: `GET /networking/firewalls`
- List VLANs: `GET /networking/vlans`

### Storage
- List volumes: `GET /volumes`
- Create volume: `POST /volumes`
- Attach volume: `POST /volumes/{volumeId}/attach`

## Troubleshooting

### Authentication Errors
- **401 Unauthorized**: Invalid or expired token
- **403 Forbidden**: Token lacks required permissions
- **Solution**: Verify token in cloud.linode.com, check scopes

### Rate Limiting
- **429 Too Many Requests**: Rate limit exceeded
- **Solution**: Implement exponential backoff, reduce request frequency

### Validation Errors
- **400 Bad Request**: Invalid input data
- **Solution**: Check error message for specific field issues, consult API docs

### Installation Issues (Python)
- **Namespace conflicts**: Older libraries use 'linode' namespace
- **Solution**: Use virtualenv to isolate dependencies

## Updating

This skill is based on the OpenAPI specification from the Linode API GitHub repository. To refresh with the latest API changes:
1. The specification is automatically pulled from: https://github.com/linode/linode-api-docs
2. Re-run the skill generation process to capture new endpoints and changes
3. Review changelog for breaking changes before updating production code
