---
name: threads-api
description: Threads API Documentation
---

# Threads API Skill

Comprehensive assistance with Meta's Threads API development for building applications that integrate with the Threads social platform.

## When to Use This Skill

This skill should be triggered when you are:
- **Building Threads integrations** - Creating apps that post to or read from Threads
- **Implementing authentication** - Setting up OAuth flows for Threads API access
- **Working with media uploads** - Uploading images, videos, or carousel posts to Threads
- **Managing user content** - Publishing, retrieving, or managing Threads posts
- **Fetching analytics** - Retrieving insights and metrics for Threads content
- **Handling webhooks** - Processing real-time updates from Threads
- **Troubleshooting API errors** - Debugging authentication, rate limits, or API responses
- **Reading Threads profiles** - Fetching user profile data and posts

## Quick Reference

### Authentication - Getting an Access Token

```javascript
// Step 1: Redirect user to authorization endpoint
const authUrl = `https://threads.net/oauth/authorize?client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&scope=threads_basic,threads_content_publish&response_type=code`;

// Step 2: Exchange authorization code for access token
const response = await fetch('https://graph.threads.net/oauth/access_token', {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: new URLSearchParams({
    client_id: CLIENT_ID,
    client_secret: CLIENT_SECRET,
    grant_type: 'authorization_code',
    redirect_uri: REDIRECT_URI,
    code: authorizationCode
  })
});

const { access_token } = await response.json();
```

### Publishing a Text Post

```javascript
// Create a simple text post
const response = await fetch(`https://graph.threads.net/v1.0/me/threads`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${accessToken}`
  },
  body: JSON.stringify({
    media_type: 'TEXT',
    text: 'Hello from Threads API! 🎉'
  })
});

const data = await response.json();
console.log('Post ID:', data.id);
```

### Publishing an Image Post

```python
import requests

# Upload and publish an image
url = "https://graph.threads.net/v1.0/me/threads"
headers = {"Authorization": f"Bearer {access_token}"}

data = {
    "media_type": "IMAGE",
    "image_url": "https://example.com/image.jpg",
    "text": "Check out this image! #API"
}

response = requests.post(url, headers=headers, json=data)
post_id = response.json()["id"]
print(f"Posted image with ID: {post_id}")
```

### Publishing a Video Post

```javascript
// Step 1: Create a video container
const container = await fetch(`https://graph.threads.net/v1.0/me/threads`, {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${accessToken}` },
  body: JSON.stringify({
    media_type: 'VIDEO',
    video_url: 'https://example.com/video.mp4',
    text: 'Check out this video!'
  })
});

const { id: containerId } = await container.json();

// Step 2: Publish the container
await fetch(`https://graph.threads.net/v1.0/me/threads_publish`, {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${accessToken}` },
  body: JSON.stringify({ creation_id: containerId })
});
```

### Fetching User Profile

```python
import requests

# Get authenticated user's profile
url = f"https://graph.threads.net/v1.0/me"
headers = {"Authorization": f"Bearer {access_token}"}
params = {
    "fields": "id,username,name,threads_profile_picture_url,threads_biography"
}

response = requests.get(url, headers=headers, params=params)
profile = response.json()

print(f"Username: {profile['username']}")
print(f"Bio: {profile['threads_biography']}")
```

### Fetching User's Threads

```javascript
// Get user's recent threads with pagination
const response = await fetch(
  `https://graph.threads.net/v1.0/me/threads?fields=id,text,timestamp,media_url&limit=25`,
  {
    headers: { 'Authorization': `Bearer ${accessToken}` }
  }
);

const { data, paging } = await response.json();
data.forEach(thread => {
  console.log(`${thread.timestamp}: ${thread.text}`);
});

// Use paging.next for next page
```

### Publishing a Carousel Post

```python
import requests

# Create a carousel with multiple images
url = "https://graph.threads.net/v1.0/me/threads"
headers = {"Authorization": f"Bearer {access_token}"}

data = {
    "media_type": "CAROUSEL",
    "children": [
        {"media_type": "IMAGE", "image_url": "https://example.com/img1.jpg"},
        {"media_type": "IMAGE", "image_url": "https://example.com/img2.jpg"},
        {"media_type": "IMAGE", "image_url": "https://example.com/img3.jpg"}
    ],
    "text": "Swipe through these images! 📸"
}

response = requests.post(url, headers=headers, json=data)
carousel_id = response.json()["id"]
```

### Retrieving Insights (Analytics)

```javascript
// Get insights for a specific thread
const threadId = '123456789';
const response = await fetch(
  `https://graph.threads.net/v1.0/${threadId}/insights?metric=views,likes,replies,reposts`,
  {
    headers: { 'Authorization': `Bearer ${accessToken}` }
  }
);

const { data } = await response.json();
data.forEach(metric => {
  console.log(`${metric.name}: ${metric.values[0].value}`);
});
```

### Error Handling Pattern

```python
import requests

def make_threads_request(url, access_token, method='GET', **kwargs):
    """Robust error handling for Threads API requests"""
    headers = kwargs.pop('headers', {})
    headers['Authorization'] = f"Bearer {access_token}"

    try:
        response = requests.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as e:
        error_data = e.response.json()
        error_code = error_data.get('error', {}).get('code')
        error_msg = error_data.get('error', {}).get('message')

        if error_code == 190:
            raise Exception(f"Invalid access token: {error_msg}")
        elif error_code == 32:
            raise Exception(f"Rate limit exceeded: {error_msg}")
        else:
            raise Exception(f"API Error {error_code}: {error_msg}")

    except requests.exceptions.RequestException as e:
        raise Exception(f"Network error: {str(e)}")
```

## Key Concepts

### Access Tokens and Permissions
- **Access Tokens**: OAuth 2.0 tokens required for all API requests
- **Scopes**: Define what your app can access (e.g., `threads_basic`, `threads_content_publish`, `threads_manage_insights`)
- **Token Expiration**: Long-lived tokens (60 days) and refresh tokens for extended access

### Media Types
- **TEXT**: Simple text posts
- **IMAGE**: Single image with optional caption
- **VIDEO**: Single video with optional caption
- **CAROUSEL**: Multiple images or videos in a swipeable format

### Publishing Flow
1. **Container Creation**: Create a media container with content
2. **Publishing**: Publish the container to make it visible
3. **Two-stage process**: Required for videos and carousels to allow processing time

### Rate Limits
- Rate limits vary by endpoint and access level
- Standard rate limit: 200 calls per hour per user
- Monitor `X-Business-Use-Case-Usage` header in responses
- Implement exponential backoff for rate limit errors

### Webhooks
- Real-time notifications for events like mentions, replies, or new followers
- Requires HTTPS endpoint for receiving notifications
- Must validate webhook signatures for security

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **other.md** - Complete Threads API documentation including:
  - Authentication and authorization flows
  - API endpoints reference
  - Request/response formats
  - Error codes and troubleshooting
  - Best practices and guidelines

Use the skill's reference files when you need detailed information about specific API endpoints, parameters, or advanced features.

## Working with This Skill

### For Beginners
Start by understanding the authentication flow - this is the foundation of all Threads API integrations. Focus on:
1. Setting up your Meta developer account and app
2. Implementing OAuth 2.0 authorization
3. Making your first API request to fetch user profile
4. Publishing a simple text post

### For Intermediate Users
Build on the basics by exploring:
1. Media uploads (images and videos)
2. Carousel posts for multi-image content
3. Webhook integration for real-time updates
4. Error handling and retry logic
5. Rate limit management

### For Advanced Users
Optimize your integration with:
1. Insights and analytics data
2. Batch operations for efficiency
3. Advanced content scheduling
4. Custom webhook event processing
5. Multi-account management

### Navigation Tips
- **Quick Reference**: Use the code examples above for common tasks
- **Reference Files**: Dive into `references/other.md` for complete API documentation
- **Authentication First**: Always start with proper authentication setup
- **Test in Sandbox**: Use Meta's test users and sandbox environment during development

## Common Workflows

### Complete Post Publishing Flow
1. Obtain access token via OAuth flow
2. Create media container (if using images/videos)
3. Wait for container processing (for videos)
4. Publish the container
5. Retrieve post ID and insights

### User Data Retrieval Flow
1. Authenticate user
2. Fetch user profile with required fields
3. Retrieve user's threads with pagination
4. Process and display content

### Webhook Integration Flow
1. Set up HTTPS endpoint
2. Register webhook subscription
3. Validate webhook signatures
4. Process incoming events
5. Respond with 200 OK status

## Best Practices

1. **Security**
   - Never expose access tokens in client-side code
   - Always validate webhook signatures
   - Use environment variables for sensitive data
   - Implement token refresh before expiration

2. **Performance**
   - Cache API responses when appropriate
   - Use batch requests for multiple operations
   - Implement pagination for large result sets
   - Monitor and respect rate limits

3. **User Experience**
   - Provide clear error messages to users
   - Show loading states during API calls
   - Handle network failures gracefully
   - Request only necessary permissions

4. **Content Publishing**
   - Validate media URLs before uploading
   - Check media format requirements
   - Add appropriate error handling for failed uploads
   - Consider using alt text for accessibility

## Resources

### Official Documentation
- Meta for Developers: https://developers.facebook.com/docs/threads
- API Reference: Available in `references/other.md`

### Developer Tools
- Meta App Dashboard: Configure your app and manage permissions
- Graph API Explorer: Test API calls interactively
- Webhook Testing: Test webhook endpoints before production

## Troubleshooting

### Common Issues

**Authentication Errors (Code 190)**
- Check access token validity
- Verify token hasn't expired
- Ensure correct permissions/scopes

**Rate Limit Errors (Code 32)**
- Implement exponential backoff
- Monitor API usage
- Consider caching responses

**Media Upload Failures**
- Verify media URL is publicly accessible
- Check file format and size requirements
- Ensure proper media_type parameter

**Webhook Not Receiving Events**
- Verify endpoint is HTTPS
- Check webhook signature validation
- Ensure endpoint responds with 200 OK quickly

## Notes

- This skill was generated from Meta's official Threads API documentation
- The Threads API is part of Meta's Graph API family
- API features and endpoints may be updated by Meta - refer to official docs for latest changes
- Some features may require additional app review or permissions from Meta

## Updating

To refresh this skill with updated documentation:
1. Visit https://developers.facebook.com/docs/threads for the latest information
2. Re-run the documentation scraper with updated configuration
3. The skill will be rebuilt with current API information
