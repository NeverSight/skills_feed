---
name: snapas
description: Snap.as API Documentation
---

# Snap.as Skill

Comprehensive assistance with Snap.as API development, enabling photo upload and management through the Write.as suite.

## When to Use This Skill

This skill should be triggered when:
- Building applications that upload photos to Snap.as
- Implementing Snap.as photo management features
- Working with Write.as authentication for photo services
- Debugging Snap.as API requests and responses
- Developing photo gallery features using Snap.as
- Managing organizational photo uploads
- Integrating photo sharing into Write.as applications

## Quick Reference

### Authentication

All Snap.as API requests require a Write.as user access token in the Authorization header:

```http
Authorization: Token 00000000-0000-0000-0000-000000000000
```

### Upload Photo to Personal Account

```bash
curl https://snap.as/api/photos/upload \
  -H "Authorization: Token YOUR_ACCESS_TOKEN" \
  -F "file=@/path/to/photo.jpg"
```

**Response (201 Created):**
```json
{
  "code": 201,
  "data": {
    "id": "abc123",
    "filename": "photo.jpg",
    "size": 245760,
    "url": "https://i.snap.as/abc123.jpg"
  }
}
```

### Retrieve User Photos

```bash
curl -X POST https://snap.as/api/me/photos \
  -H "Authorization: Token YOUR_ACCESS_TOKEN"
```

**Response (200 OK):**
```json
{
  "code": 200,
  "data": [
    {
      "id": "abc123",
      "filename": "photo.jpg",
      "size": 245760,
      "url": "https://i.snap.as/abc123.jpg"
    }
  ]
}
```

### Delete Photo

```bash
curl -X POST https://snap.as/api/photos/abc123 \
  -H "Authorization: Token YOUR_ACCESS_TOKEN"
```

**Response (200 OK):**
```json
{
  "code": 200,
  "data": {}
}
```

### Upload Photo to Organization

```bash
curl https://snap.as/api/organizations/myorg/photos/upload \
  -H "Authorization: Token YOUR_ACCESS_TOKEN" \
  -F "file=@/path/to/photo.jpg"
```

**Response (201 Created):**
```json
{
  "code": 201,
  "data": {
    "id": "xyz789",
    "filename": "photo.jpg",
    "size": 245760,
    "url": "https://i.snap.as/xyz789.jpg"
  }
}
```

### Error Response Format

```json
{
  "code": 401,
  "error_msg": "Invalid access token"
}
```

### Go Client Library Usage

```go
import "github.com/snapas/go-snapas"

// Initialize client
client := snapas.NewClient("YOUR_ACCESS_TOKEN")

// Upload photo
photo, err := client.UploadPhoto("/path/to/photo.jpg")
if err != nil {
    log.Fatal(err)
}
fmt.Printf("Photo URL: %s\n", photo.URL)
```

## Key Concepts

### Authentication
Snap.as uses Write.as user access tokens for authentication. These tokens must be obtained by logging into Write.as and retrieving the user's access credentials. Include the token in the `Authorization` header of every API request.

### Base URL
All API requests are made to `https://snap.as` with specific endpoint paths appended.

### Photo Objects
Photo objects returned by the API contain:
- `id`: Unique identifier for the photo
- `filename`: Original filename of the uploaded photo
- `size`: File size in bytes
- `url`: Public URL where the photo can be accessed

### Response Format
All successful API responses follow a consistent structure:
```json
{
  "code": <HTTP_STATUS_CODE>,
  "data": <RESPONSE_DATA>
}
```

Failed requests return:
```json
{
  "code": <HTTP_STATUS_CODE>,
  "error_msg": "<ERROR_MESSAGE>"
}
```

### HTTP Status Codes
- `200 OK`: Request succeeded
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Invalid or missing access token
- `403 Forbidden`: Access denied to resource
- `404 Not Found`: Resource does not exist
- `429 Too Many Requests`: Rate limit exceeded

### Personal vs. Organization Photos
- Personal photos: Uploaded to the user's account using `/api/photos/upload`
- Organization photos: Uploaded to a specific organization using `/api/organizations/{alias}/photos/upload`

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **api.md** - Complete API reference with all endpoints, authentication details, request/response formats, and error handling

Use `view` to read the API reference file when detailed information is needed about specific endpoints or response formats.

## Working with This Skill

### For Beginners
Start by understanding the authentication mechanism. You'll need a Write.as user access token before making any API requests. Test with simple photo uploads to your personal account before working with organizational features.

### For Integration Developers
Focus on the personal photo upload and retrieval endpoints first. Implement proper error handling for common scenarios like authentication failures (401), rate limiting (429), and invalid requests (400).

### For Organization Features
Once comfortable with personal uploads, explore organizational photo management. Organizations require the organization alias in the endpoint URL and appropriate access permissions.

### For Go Developers
Use the official `go-snapas` client library available at `github.com/snapas/go-snapas` for a more convenient development experience with built-in error handling and type safety.

## Common Patterns

### Photo Upload Flow
1. Obtain Write.as access token
2. Prepare photo file for upload
3. Make POST request to `/api/photos/upload` with multipart form data
4. Handle response (201 Created on success)
5. Store photo ID and URL from response

### Photo Gallery Implementation
1. Authenticate with Write.as token
2. Retrieve all user photos via `/api/me/photos`
3. Display photos using the URLs from response data
4. Implement delete functionality using photo IDs

### Error Handling Best Practices
```javascript
async function uploadPhoto(file, accessToken) {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch('https://snap.as/api/photos/upload', {
      method: 'POST',
      headers: {
        'Authorization': `Token ${accessToken}`
      },
      body: formData
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error_msg || 'Upload failed');
    }

    return data.data;
  } catch (error) {
    console.error('Photo upload error:', error);
    throw error;
  }
}
```

## Resources

### Official Library
- Go client: `github.com/snapas/go-snapas`

### API Endpoints
- Base URL: `https://snap.as`
- Personal uploads: `/api/photos/upload`
- User photos: `/api/me/photos`
- Delete photo: `/api/photos/{PHOTO_ID}`
- Organization uploads: `/api/organizations/{alias}/photos/upload`

### Write.as Integration
Since Snap.as is part of the Write.as suite, authentication happens through Write.as user accounts. Ensure users have valid Write.as credentials before attempting to use Snap.as features.

## Notes

- All API requests require authentication via Write.as access token
- Photo uploads use multipart/form-data encoding
- Response format is consistent across all endpoints
- Rate limiting may apply (429 status code)
- Organization features require appropriate access permissions
- Photos are publicly accessible via returned URLs
- This skill was generated from official Snap.as API documentation

## Troubleshooting

### 401 Unauthorized
- Verify your Write.as access token is valid
- Check that the Authorization header is properly formatted
- Ensure the token hasn't expired

### 403 Forbidden
- Verify you have permission to upload to the specified organization
- Check that the organization alias is correct

### 429 Rate Limited
- Implement exponential backoff in your retry logic
- Reduce request frequency
- Cache photo URLs instead of repeatedly fetching

### Upload Failures
- Verify file format is supported (JPG, PNG, GIF)
- Check file size limits
- Ensure proper multipart/form-data encoding
- Confirm network connectivity to snap.as

## Updating

To refresh this skill with updated documentation:
1. Check https://developers.snap.as/docs/api/ for API changes
2. Update the reference files with new endpoint information
3. Add new code examples for any new features
4. Test all examples to ensure they still work
