---
name: download-swagger-file
description: Download Swagger/OpenAPI specification file from a URL. Use phrases like "Download swagger file", "Fetch OpenAPI spec", "Get API documentation", etc.
---

# Download Swagger/OpenAPI File

Downloads an OpenAPI (Swagger) specification file from a remote URL and saves it locally. Supports both JSON and YAML formats for OpenAPI 2.0 and 3.x specifications.

## How It Works

1. Validates the provided URL is accessible
2. Downloads the specification file using curl
3. Detects and validates the file format (JSON/YAML)
4. Saves the file to the specified output path
5. Returns the file path and basic metadata

## Usage

```bash
bash /mnt/skills/user/download-swagger-file/scripts/download.sh <url> [output-path]
```

**Arguments:**
- `url` - The URL of the OpenAPI/Swagger specification file (required)
- `output-path` - Local file path to save the downloaded file (optional, defaults to `openapi.json` in current directory)

**Examples:**

Download to default location:
```bash
bash /mnt/skills/user/download-swagger-file/scripts/download.sh https://api.example.com/swagger.json
```

Download with custom output path:
```bash
bash /mnt/skills/user/download-swagger-file/scripts/download.sh https://api.example.com/swagger.json ./specs/my-api.json
```

Download YAML specification:
```bash
bash /mnt/skills/user/download-swagger-file/scripts/download.sh https://api.example.com/openapi.yaml ./docs/api.yaml
```

## Output

```json
{
  "success": true,
  "filePath": "./specs/petstore.json",
  "format": "json",
  "size": 15234,
  "url": "https://petstore.swagger.io/v2/swagger.json"
}
```

## Present Results to User

Successfully downloaded OpenAPI specification:

- **File**: `./specs/petstore.json`
- **Format**: JSON
- **Size**: 15.2 KB
- **Source**: https://petstore.swagger.io/v2/swagger.json

The file is ready to use with other OpenAPI skills for generating TypeScript models and API clients.

## Troubleshooting

**Error: Failed to download file**
- Check that the URL is accessible in a browser
- Verify the server has CORS enabled if accessed from a browser
- Ensure the URL points directly to the JSON/YAML file, not a documentation page

**Error: Invalid OpenAPI format**
- Verify the downloaded file is a valid OpenAPI/Swagger specification
- Check that the file is not HTML (common when URL points to docs page instead of raw spec)
- Use a JSON/YAML validator to check file syntax

**Error: Permission denied writing to output path**
- Ensure you have write permissions for the output directory
- Try specifying a different output path in a writable location
- Create the target directory before running the script
