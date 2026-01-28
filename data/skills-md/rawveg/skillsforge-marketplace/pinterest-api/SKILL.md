---
name: pinterest-api
description: Pinterest API v5 Development - Authentication, Pins, Boards, Analytics
---

# Pinterest API Skill

Comprehensive assistance with Pinterest API v5 development, including OAuth authentication, pin/board management, analytics, and API integration patterns.

## When to Use This Skill

This skill should be triggered when:
- Implementing Pinterest OAuth 2.0 authentication flows
- Creating, updating, or managing Pins and Boards via API
- Integrating Pinterest analytics and metrics into applications
- Building Pinterest API clients or SDKs
- Working with Pinterest user account data
- Debugging Pinterest API requests or responses
- Implementing Pinterest sharing features in web/mobile apps
- Setting up Pinterest business account integrations
- Working with Pinterest ad account APIs

## Key Concepts

### Pinterest API v5 Overview
- **Base URL**: `https://api.pinterest.com/v5/`
- **Authentication**: OAuth 2.0 with access tokens
- **Rate Limiting**: Token-based rate limits (varies by endpoint)
- **Response Format**: JSON
- **Required Headers**: `Authorization: Bearer {access_token}`

### Core Resources
- **Pins**: Individual pieces of content (images, videos) saved to Pinterest
- **Boards**: Collections that organize Pins by theme or topic
- **Sections**: Subsections within Boards for additional organization
- **User Account**: Pinterest user profile and account information
- **Ad Accounts**: Business accounts for advertising functionality

### Access Levels
- **Public Access**: Read-only access to public data
- **User Authorization**: Full access to user's Pins, Boards, and account
- **Business Access**: Additional analytics and ad account management (requires appropriate roles)

## Quick Reference

### OAuth 2.0 Authentication Flow

#### Step 1: Generate Authorization URL
```javascript
// Redirect user to Pinterest authorization page
const authUrl = `https://www.pinterest.com/oauth/?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=boards:read,pins:read,user_accounts:read`;

window.location.href = authUrl;
```

#### Step 2: Exchange Code for Access Token
```bash
# After user authorizes, exchange authorization code for access token
curl -X POST https://api.pinterest.com/v5/oauth/token \
  --header "Authorization: Basic {BASE64_ENCODED_CLIENT_CREDENTIALS}" \
  --header "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "grant_type=authorization_code" \
  --data-urlencode "code={AUTHORIZATION_CODE}" \
  --data-urlencode "redirect_uri={REDIRECT_URI}"
```

**Base64 Encoding Client Credentials:**
```bash
# Encode client_id:client_secret
echo -n "your_client_id:your_client_secret" | base64
```

**Response:**
```json
{
  "access_token": "pina_ABC123...",
  "token_type": "bearer",
  "expires_in": 2592000,
  "refresh_token": "DEF456...",
  "scope": "boards:read,pins:read,user_accounts:read"
}
```

### Pin Management

#### Create a Pin
```bash
curl -X POST https://api.pinterest.com/v5/pins \
  -H "Authorization: Bearer {ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "link": "https://example.com/my-article",
    "title": "My Amazing Pin Title",
    "description": "Detailed description of the pin content",
    "board_id": "123456789",
    "media_source": {
      "source_type": "image_url",
      "url": "https://example.com/image.jpg"
    }
  }'
```

#### Get Pin Details
```bash
curl -X GET https://api.pinterest.com/v5/pins/{PIN_ID} \
  -H "Authorization: Bearer {ACCESS_TOKEN}"
```

**Response:**
```json
{
  "id": "987654321",
  "created_at": "2025-01-15T10:30:00",
  "link": "https://example.com/my-article",
  "title": "My Amazing Pin Title",
  "description": "Detailed description of the pin content",
  "board_id": "123456789",
  "media": {
    "media_type": "image",
    "images": {
      "150x150": { "url": "...", "width": 150, "height": 150 },
      "400x300": { "url": "...", "width": 400, "height": 300 },
      "originals": { "url": "...", "width": 1200, "height": 800 }
    }
  }
}
```

#### Update a Pin
```bash
curl -X PATCH https://api.pinterest.com/v5/pins/{PIN_ID} \
  -H "Authorization: Bearer {ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Pin Title",
    "description": "Updated description",
    "link": "https://example.com/updated-link"
  }'
```

#### Delete a Pin
```bash
curl -X DELETE https://api.pinterest.com/v5/pins/{PIN_ID} \
  -H "Authorization: Bearer {ACCESS_TOKEN}"
```

### Board Management

#### Create a Board
```bash
curl -X POST https://api.pinterest.com/v5/boards \
  -H "Authorization: Bearer {ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My New Board",
    "description": "A collection of my favorite ideas",
    "privacy": "PUBLIC"
  }'
```

**Privacy Options:** `PUBLIC`, `PROTECTED`, `SECRET`

#### List User's Boards
```bash
curl -X GET https://api.pinterest.com/v5/boards \
  -H "Authorization: Bearer {ACCESS_TOKEN}"
```

#### Get Board Pins
```bash
curl -X GET https://api.pinterest.com/v5/boards/{BOARD_ID}/pins \
  -H "Authorization: Bearer {ACCESS_TOKEN}"
```

### User Account

#### Get Current User Account
```bash
curl -X GET https://api.pinterest.com/v5/user_account \
  -H "Authorization: Bearer {ACCESS_TOKEN}"
```

**Response:**
```json
{
  "account_type": "BUSINESS",
  "id": "123456789",
  "username": "myusername",
  "website_url": "https://example.com",
  "profile_image": "https://i.pinimg.com/...",
  "follower_count": 1500,
  "following_count": 320,
  "board_count": 25,
  "pin_count": 450
}
```

### Analytics

#### Get Pin Analytics
```bash
curl -X GET "https://api.pinterest.com/v5/pins/{PIN_ID}/analytics?start_date=2025-01-01&end_date=2025-01-31&metric_types=IMPRESSION,SAVE,PIN_CLICK" \
  -H "Authorization: Bearer {ACCESS_TOKEN}"
```

**Available Metrics:**
- `IMPRESSION` - Number of times pin was shown
- `SAVE` - Number of times pin was saved
- `PIN_CLICK` - Number of clicks to pin destination
- `OUTBOUND_CLICK` - Clicks to external website
- `VIDEO_START` - Video plays started

**Response:**
```json
{
  "all": {
    "daily_metrics": [
      {
        "date": "2025-01-01",
        "data_status": "READY",
        "metrics": {
          "IMPRESSION": 1250,
          "SAVE": 45,
          "PIN_CLICK": 89
        }
      }
    ]
  }
}
```

### Error Handling

#### Common Error Response
```json
{
  "code": 3,
  "message": "Requested pin not found"
}
```

**Common Error Codes:**
- `1` - Invalid request parameters
- `2` - Rate limit exceeded
- `3` - Resource not found
- `4` - Insufficient permissions
- `8` - Invalid access token

#### Python Error Handling Example
```python
import requests

def create_pin(access_token, board_id, title, image_url):
    url = "https://api.pinterest.com/v5/pins"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "board_id": board_id,
        "title": title,
        "media_source": {
            "source_type": "image_url",
            "url": image_url
        }
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        error_data = e.response.json()
        print(f"Error {error_data.get('code')}: {error_data.get('message')}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {str(e)}")
        return None
```

### JavaScript/Node.js Integration

```javascript
// Pinterest API Client Example
class PinterestClient {
  constructor(accessToken) {
    this.accessToken = accessToken;
    this.baseUrl = 'https://api.pinterest.com/v5';
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    const headers = {
      'Authorization': `Bearer ${this.accessToken}`,
      'Content-Type': 'application/json',
      ...options.headers
    };

    const response = await fetch(url, {
      ...options,
      headers
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(`Pinterest API Error: ${error.message}`);
    }

    return response.json();
  }

  async createPin(boardId, title, imageUrl, description = '', link = '') {
    return this.request('/pins', {
      method: 'POST',
      body: JSON.stringify({
        board_id: boardId,
        title: title,
        description: description,
        link: link,
        media_source: {
          source_type: 'image_url',
          url: imageUrl
        }
      })
    });
  }

  async getUserBoards() {
    return this.request('/boards');
  }

  async getPinAnalytics(pinId, startDate, endDate) {
    const params = new URLSearchParams({
      start_date: startDate,
      end_date: endDate,
      metric_types: 'IMPRESSION,SAVE,PIN_CLICK'
    });
    return this.request(`/pins/${pinId}/analytics?${params}`);
  }
}

// Usage
const client = new PinterestClient('your_access_token');
const pin = await client.createPin('board_id', 'Pin Title', 'https://example.com/image.jpg');
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **api.md** - Complete Pinterest API v5 endpoint reference extracted from official documentation

Use `view` to read reference files when detailed information about specific endpoints is needed.

## Working with This Skill

### For Beginners
1. Start by understanding OAuth 2.0 authentication flow (see Quick Reference above)
2. Get your API credentials from Pinterest Developer Portal
3. Test authentication with curl commands before implementing in your application
4. Use the provided Python/JavaScript examples as starting templates

### For API Integration
1. Implement OAuth flow to obtain access tokens
2. Store refresh tokens securely for long-term access
3. Use the Pin/Board management examples for CRUD operations
4. Implement proper error handling for rate limits and API errors

### For Analytics & Business Features
1. Ensure you have appropriate business account access
2. Use analytics endpoints to track Pin performance
3. Aggregate metrics across date ranges for reporting
4. Implement caching to avoid unnecessary API calls

### Best Practices
- **Token Security**: Never expose access tokens in client-side code or version control
- **Rate Limiting**: Implement exponential backoff for rate limit errors
- **Pagination**: Use cursor-based pagination for large result sets
- **Webhooks**: Consider using webhooks for real-time updates instead of polling
- **Scopes**: Request only the minimum OAuth scopes needed for your application

## Common Patterns

### Pagination
```bash
# Initial request
curl -X GET "https://api.pinterest.com/v5/boards/{BOARD_ID}/pins?page_size=25" \
  -H "Authorization: Bearer {ACCESS_TOKEN}"

# Follow-up with bookmark from response
curl -X GET "https://api.pinterest.com/v5/boards/{BOARD_ID}/pins?page_size=25&bookmark={BOOKMARK}" \
  -H "Authorization: Bearer {ACCESS_TOKEN}"
```

### Bulk Operations
```python
# Create multiple pins efficiently
def bulk_create_pins(access_token, board_id, pin_data_list):
    results = []
    for pin_data in pin_data_list:
        result = create_pin(
            access_token,
            board_id,
            pin_data['title'],
            pin_data['image_url']
        )
        results.append(result)
        time.sleep(0.5)  # Respect rate limits
    return results
```

## Resources

### Official Documentation
- Pinterest API v5 Docs: https://developers.pinterest.com/docs/api/v5/
- API Quickstart: https://github.com/pinterest/api-quickstart
- OAuth Documentation: https://developers.pinterest.com/docs/getting-started/authentication/

### OAuth Scopes
Common scopes you'll need:
- `boards:read` - Read board data
- `boards:write` - Create/update boards
- `pins:read` - Read pin data
- `pins:write` - Create/update pins
- `user_accounts:read` - Read user account data
- `ads:read` - Read ad account analytics (business accounts)

### Rate Limits
- Pinterest implements per-user rate limiting
- Typical limits: 1000 requests per hour per user
- Rate limit headers in response:
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Reset`

## Notes

- Pinterest API v5 is the current version (as of 2025)
- All endpoints require authentication via OAuth 2.0
- Access tokens expire after 30 days
- Use refresh tokens to obtain new access tokens
- Business accounts have access to additional analytics features
- Video pins require special handling compared to image pins
- Some features require app review by Pinterest

## Troubleshooting

### "Invalid access token"
- Verify token hasn't expired (30-day lifetime)
- Use refresh token to obtain new access token
- Check Authorization header format: `Bearer {token}`

### "Insufficient permissions"
- Verify OAuth scopes include required permissions
- Business features require verified business account
- Some operations require board/pin ownership

### "Rate limit exceeded"
- Implement exponential backoff
- Cache responses when possible
- Use webhooks instead of polling
- Check `X-RateLimit-Reset` header for retry time

### "Media upload failed"
- Verify image URL is publicly accessible
- Check image meets size requirements (max 10MB)
- Ensure image format is supported (JPG, PNG, GIF)
- For video, use video-specific endpoints

## Updating

This skill was generated from Pinterest's official API documentation. To get the latest API changes:
1. Visit https://developers.pinterest.com/docs/api/v5/
2. Check changelog for API updates
3. Review deprecation notices
4. Update OAuth scopes if new features added
