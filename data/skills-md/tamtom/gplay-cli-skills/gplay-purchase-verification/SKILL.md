---
name: gplay-purchase-verification
description: Server-side purchase verification for in-app products and subscriptions using Google Play Developer API. Use when implementing receipt validation in your backend.
---

# Purchase Verification for Google Play

Use this skill when you need to verify in-app purchases or subscriptions from your backend server.

## Why Verify Purchases Server-Side?

Client-side verification can be bypassed. Always verify purchases on your server:
- Prevent fraud and piracy
- Ensure user actually paid
- Check subscription status
- Handle refunds and cancellations

## Authentication Setup

Your backend needs a service account with permissions to verify purchases.

### Create service account
1. Go to [Google Cloud Console](https://console.cloud.google.com/iam-admin/serviceaccounts)
2. Create service account
3. Grant "Service Account User" role
4. Download JSON key

### Grant API access
1. Go to [Play Console](https://play.google.com/console)
2. Users & Permissions → Service Accounts
3. Grant service account access to your apps

## Verify In-App Product Purchase

### Get purchase details
```bash
gplay purchases products get \
  --package com.example.app \
  --product-id premium_upgrade \
  --token <PURCHASE_TOKEN>
```

### Response
```json
{
  "kind": "androidpublisher#productPurchase",
  "purchaseTimeMillis": "1706400000000",
  "purchaseState": 0,
  "consumptionState": 0,
  "developerPayload": "user_123",
  "orderId": "GPA.1234-5678-9012-34567",
  "purchaseType": 0
}
```

### Purchase states
- `0` = Purchased
- `1` = Canceled
- `2` = Pending

### Consumption states
- `0` = Yet to be consumed
- `1` = Consumed

## Acknowledge Purchase

After verifying, acknowledge the purchase:

```bash
gplay purchases products acknowledge \
  --package com.example.app \
  --product-id premium_upgrade \
  --token <PURCHASE_TOKEN>
```

**Important:** Unacknowledged purchases will be refunded after 3 days.

## Consume Purchase (for consumables)

For consumable items (coins, gems, etc.):

```bash
gplay purchases products consume \
  --package com.example.app \
  --product-id coins_100 \
  --token <PURCHASE_TOKEN>
```

## Verify Subscription

### Get subscription details
```bash
gplay purchases subscriptions get \
  --package com.example.app \
  --token <SUBSCRIPTION_TOKEN>
```

### Response
```json
{
  "kind": "androidpublisher#subscriptionPurchase",
  "startTimeMillis": "1706400000000",
  "expiryTimeMillis": "1709000000000",
  "autoRenewing": true,
  "priceCurrencyCode": "USD",
  "priceAmountMicros": "4990000",
  "paymentState": 1,
  "cancelReason": null,
  "userCancellationTimeMillis": null,
  "orderId": "GPA.1234-5678-9012-34567",
  "linkedPurchaseToken": null,
  "subscriptionState": 0
}
```

### Subscription states
- `0` = Active
- `1` = Canceled (still valid until expiry)
- `2` = In grace period
- `3` = On hold (payment failed, retrying)
- `4` = Paused
- `5` = Expired

### Payment states
- `0` = Payment pending
- `1` = Payment received
- `2` = Free trial
- `3` = Pending deferred upgrade/downgrade

## Backend Implementation Example

### Node.js/Express
```javascript
const { google } = require('googleapis');

async function verifyPurchase(packageName, productId, token) {
  const auth = new google.auth.GoogleAuth({
    keyFile: '/path/to/service-account.json',
    scopes: ['https://www.googleapis.com/auth/androidpublisher'],
  });

  const androidpublisher = google.androidpublisher({
    version: 'v3',
    auth: await auth.getClient(),
  });

  const result = await androidpublisher.purchases.products.get({
    packageName: packageName,
    productId: productId,
    token: token,
  });

  return result.data;
}

// Endpoint
app.post('/verify-purchase', async (req, res) => {
  const { packageName, productId, token } = req.body;

  try {
    const purchase = await verifyPurchase(packageName, productId, token);

    if (purchase.purchaseState === 0) {
      // Purchase is valid
      // Grant access to user
      // Acknowledge purchase
      res.json({ valid: true, purchase });
    } else {
      res.json({ valid: false });
    }
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});
```

### Python/Flask
```python
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/androidpublisher']
SERVICE_ACCOUNT_FILE = '/path/to/service-account.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

androidpublisher = build('androidpublisher', 'v3', credentials=credentials)

@app.route('/verify-purchase', methods=['POST'])
def verify_purchase():
    data = request.json
    package_name = data['packageName']
    product_id = data['productId']
    token = data['token']

    try:
        result = androidpublisher.purchases().products().get(
            packageName=package_name,
            productId=product_id,
            token=token
        ).execute()

        if result['purchaseState'] == 0:
            # Purchase is valid
            return jsonify({'valid': True, 'purchase': result})
        else:
            return jsonify({'valid': False})

    except Exception as e:
        return jsonify({'error': str(e)}), 400
```

## Handle Subscription Events

### Real-time Developer Notifications (RTDN)

Set up Pub/Sub to receive subscription events:

1. **Create Pub/Sub topic** in Google Cloud Console
2. **Configure in Play Console**:
   - Monetization Setup → Real-time developer notifications
   - Enter topic name

3. **Subscribe to events**:
```python
from google.cloud import pubsub_v1

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message):
    data = json.loads(message.data)

    if 'subscriptionNotification' in data:
        notification = data['subscriptionNotification']
        notification_type = notification['notificationType']
        purchase_token = notification['purchaseToken']

        # Handle different events
        if notification_type == 1:  # SUBSCRIPTION_RECOVERED
            # Subscription was recovered from account hold
            pass
        elif notification_type == 2:  # SUBSCRIPTION_RENEWED
            # Subscription renewed successfully
            pass
        elif notification_type == 3:  # SUBSCRIPTION_CANCELED
            # User canceled subscription
            pass
        elif notification_type == 4:  # SUBSCRIPTION_PURCHASED
            # New subscription purchase
            pass
        elif notification_type == 7:  # SUBSCRIPTION_EXPIRED
            # Subscription expired
            pass
        elif notification_type == 10:  # SUBSCRIPTION_PAUSED
            # Subscription paused
            pass
        elif notification_type == 12:  # SUBSCRIPTION_REVOKED
            # Subscription revoked (refunded)
            pass

    message.ack()

subscriber.subscribe(subscription_path, callback=callback)
```

## Subscription Management

### Cancel subscription
```bash
gplay purchases subscriptions cancel \
  --package com.example.app \
  --token <SUBSCRIPTION_TOKEN>
```

### Defer subscription
```bash
gplay purchases subscriptions defer \
  --package com.example.app \
  --token <SUBSCRIPTION_TOKEN> \
  --json @defer.json
```

### defer.json
```json
{
  "deferralInfo": {
    "expectedExpiryTimeMillis": "1709000000000"
  }
}
```

### Revoke subscription (refund)
```bash
gplay purchases subscriptions revoke \
  --package com.example.app \
  --token <SUBSCRIPTION_TOKEN>
```

## Check Voided Purchases

Get list of refunded/canceled purchases:

```bash
gplay purchases voided list \
  --package com.example.app \
  --start-time 1706400000000 \
  --end-time 1709000000000
```

Remove entitlements for these purchases on your backend.

## Order Information

### Get order details
```bash
gplay orders get \
  --package com.example.app \
  --order-id GPA.1234-5678-9012-34567
```

### Batch get orders
```bash
gplay orders batch-get \
  --package com.example.app \
  --order-ids "GPA.1234,GPA.5678,GPA.9012"
```

### Refund order
```bash
gplay orders refund \
  --package com.example.app \
  --order-id GPA.1234-5678-9012-34567 \
  --revoke  # Also revoke access
```

## Security Best Practices

### DO:
- ✅ Always verify on server, never trust client
- ✅ Store purchase tokens securely
- ✅ Acknowledge purchases within 3 days
- ✅ Handle refunds and cancellations
- ✅ Use HTTPS for all API calls
- ✅ Rate limit your verification endpoint
- ✅ Log all verification attempts

### DON'T:
- ❌ Verify purchases only on client
- ❌ Expose service account credentials
- ❌ Skip acknowledging purchases
- ❌ Grant access before verification
- ❌ Ignore voided purchases
- ❌ Store credit card info (PCI compliance)

## Common Verification Flow

1. **User makes purchase** in app
2. **App sends purchase token** to your server
3. **Server verifies** with Google Play API
4. **Server acknowledges** purchase (if valid)
5. **Server grants** access/content to user
6. **Server stores** purchase token for future checks
7. **Server listens** for RTDN events (cancellations, renewals)

## Error Handling

### Common errors
- `401 Unauthorized` - Service account not authorized
- `404 Not Found` - Purchase token invalid or expired
- `410 Gone` - Purchase was refunded/canceled

### Retry logic
```javascript
async function verifyWithRetry(packageName, productId, token, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      return await verifyPurchase(packageName, productId, token);
    } catch (error) {
      if (error.code === 404 || error.code === 410) {
        throw error; // Don't retry if purchase is invalid
      }
      if (i === retries - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
    }
  }
}
```

## Testing

### Test purchases
Use Google Play's test accounts to make test purchases without charging real money.

### Test verification
```bash
# Verify test purchase
gplay purchases products get \
  --package com.example.app \
  --product-id android.test.purchased \
  --token <TEST_TOKEN>
```

## Monitoring

Track these metrics:
- Purchase verification success rate
- Acknowledgment rate
- Refund rate
- Subscription churn rate
- Failed payment rate

Use this data to improve your monetization strategy.
