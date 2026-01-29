---
name: didit-best-practises
description: Best practices for integrating Didit identity verification platform. Use when implementing KYC/identity verification with Didit, setting up verification workflows, configuring webhooks, integrating web/mobile apps, or migrating from Sumsub to Didit. Triggers on Didit API integration, verification sessions, ID verification, liveness checks, AML screening, face matching, and KYC implementation.
---

# Didit Integration Best Practices

## Quick Reference

| Resource | URL |
|----------|-----|
| API Base | `https://verification.didit.me/v3/` |
| Console | `https://business.didit.me/` |
| Docs | `https://docs.didit.me/reference/` |

## Integration Workflow

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  1. Console     │────▶│  2. Backend      │────▶│  3. Frontend    │
│  Setup          │     │  Integration     │     │  Integration    │
└─────────────────┘     └──────────────────┘     └─────────────────┘
        │                       │                        │
        ▼                       ▼                        ▼
   Create App            Create Session           Open Session URL
   Get API Key           Handle Webhooks          Handle Callback
   Configure Workflow    Retrieve Results         Update UI
```

## 1. Console Setup

### Create Application
1. Log in to Didit Business Console
2. Create new Application (workspace for project/environment)
3. Navigate to Verifications → Settings (⚙️) → Copy API Key

### Configure Workflow
Select verification features based on requirements:

| Feature | Use Case |
|---------|----------|
| ID Verification | Document verification (220+ countries) |
| Liveness | Prevent spoofing/deepfakes |
| Face Match 1:1 | Compare selfie to document photo |
| AML Screening | Watchlist/PEP database checks |
| NFC Verification | Enhanced security via NFC chip |
| Age Estimation | Age verification without full KYC |
| Proof of Address | Residential address verification |

## 2. Backend Integration

### Authentication

All requests require `x-api-key` header:

```typescript
const headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'x-api-key': process.env.DIDIT_API_KEY
};
```

### Create Verification Session

```typescript
// POST https://verification.didit.me/v3/session/
const createSession = async (userId: string, callbackUrl: string) => {
  const response = await fetch('https://verification.didit.me/v3/session/', {
    method: 'POST',
    headers,
    body: JSON.stringify({
      workflow_id: process.env.DIDIT_WORKFLOW_ID,
      vendor_data: userId,  // Your internal user ID
      callback: callbackUrl // Redirect URL after verification
    })
  });
  
  const { session_id, url } = await response.json();
  // Store session_id, redirect user to url
  return { session_id, url };
};
```

### Retrieve Session Status

```typescript
// GET https://verification.didit.me/v3/session/{session_id}
const getSession = async (sessionId: string) => {
  const response = await fetch(
    `https://verification.didit.me/v3/session/${sessionId}`,
    { headers }
  );
  return response.json();
};
```

### Webhook Handler

```typescript
// Webhook payload structure
interface DiditWebhook {
  session_id: string;
  status: 'Approved' | 'Declined' | 'In Review' | 'Expired';
  vendor_data: string;
  // Additional verification data based on workflow
}

app.post('/webhooks/didit', async (req, res) => {
  const payload: DiditWebhook = req.body;
  
  switch (payload.status) {
    case 'Approved':
      await updateUserVerificationStatus(payload.vendor_data, 'verified');
      break;
    case 'Declined':
      await handleDeclinedVerification(payload);
      break;
    case 'In Review':
      await flagForManualReview(payload.vendor_data);
      break;
  }
  
  res.status(200).send('OK');
});
```

## 3. Frontend Integration

### Web Integration

Redirect user to session URL or embed in iframe:

```typescript
// Redirect approach (recommended)
window.location.href = sessionUrl;

// Popup approach
window.open(sessionUrl, 'didit-verification', 'width=500,height=700');
```

### Mobile Integration (React Native)

```tsx
import { WebView } from 'react-native-webview';

const VerificationScreen = ({ sessionUrl }: { sessionUrl: string }) => (
  <WebView
    source={{ uri: sessionUrl }}
    userAgent="Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36"
    mediaPlaybackRequiresUserAction={false}
    allowsInlineMediaPlayback={true}
    domStorageEnabled={true}
  />
);
```

### Mobile Integration (iOS Swift)

```swift
import WebKit

class VerificationViewController: UIViewController {
  private var webView: WKWebView!
  
  override func viewDidLoad() {
    super.viewDidLoad()
    
    let config = WKWebViewConfiguration()
    config.allowsInlineMediaPlayback = true
    config.mediaTypesRequiringUserActionForPlayback = []
    
    webView = WKWebView(frame: view.bounds, configuration: config)
    webView.customUserAgent = "Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36"
    
    view.addSubview(webView)
    
    if let url = URL(string: sessionUrl) {
      webView.load(URLRequest(url: url))
    }
  }
}
```

### Mobile Integration (Android)

```kotlin
val webView = findViewById<WebView>(R.id.webview)
webView.settings.apply {
  javaScriptEnabled = true
  mediaPlaybackRequiresUserGesture = false
}
webView.webChromeClient = WebChromeClient()
webView.settings.userAgentString = "Mozilla/5.0 (Linux; Android 10; Mobile) AppleWebKit/537.36"
webView.loadUrl(sessionUrl)
```

## Verification Statuses

| Status | Description | Action |
|--------|-------------|--------|
| Not Started | Session created, user hasn't begun | Wait or send reminder |
| In Progress | User actively verifying | Wait for completion |
| Approved | Verification successful | Grant access |
| Declined | Verification failed | Show reason, allow retry |
| In Review | Manual review required | Wait for compliance team |
| Expired | Session timed out | Create new session |
| Abandoned | User didn't complete | Send follow-up |
| KYC Expired | Previous KYC expired | Request re-verification |

## Best Practices

### Security
- Store API key in environment variables, never in code
- Validate webhook signatures if available
- Use HTTPS for all callback URLs
- Implement rate limiting on your webhook endpoint

### User Experience
- Show clear instructions before redirecting to verification
- Handle all status states in your UI
- Provide retry options for declined verifications
- Show progress indicators during verification

### Error Handling
```typescript
try {
  const session = await createSession(userId, callbackUrl);
} catch (error) {
  if (error.status === 401) {
    // Invalid API key
  } else if (error.status === 429) {
    // Rate limited - implement exponential backoff
  } else if (error.status === 400) {
    // Invalid request - check workflow_id
  }
}
```

### Rate Limits
- Free workflows: 10 sessions/minute
- Paid workflows: 600 sessions/minute
- Implement exponential backoff on 429 responses

## White Label Configuration

Customize verification UI in Console → White Label:
- Colors: buttons, text, panels, backgrounds
- Typography: custom fonts
- Logos: square and rectangular formats
- Custom domain: host on your domain instead of verify.didit.me

## Migration from Sumsub

See [references/sumsub-migration.md](references/sumsub-migration.md) for detailed migration guide.

**Key differences:**
- Didit uses `x-api-key` header (Sumsub uses different auth)
- Session-based flow vs applicant-based
- Simpler webhook payload structure
- Built-in white-label support

## Resources

- [API Reference](https://docs.didit.me/reference/)
- [Webhook Configuration](https://docs.didit.me/reference/webhooks)
- [Verification Statuses](https://docs.didit.me/reference/verification-statuses)
- [Mobile Integration](https://docs.didit.me/reference/ios-android)
