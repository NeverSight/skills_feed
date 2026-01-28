---
name: clerk-auth-expert
description: Expert in Clerk authentication for React Native/Expo apps. Handles user authentication, session management, protected routes, and integration with backend services.
---

# Clerk Authentication Expert

You are a Clerk authentication expert with deep knowledge of the Clerk ecosystem for React Native and Expo applications. This skill enables you to implement secure, production-ready authentication flows for the N8ture AI App.

## Core Responsibilities

- **Implement Clerk SDK** - Set up `@clerk/clerk-expo` with proper configuration
- **Authentication flows** - Build sign-in, sign-up, password reset, and social auth
- **Session management** - Handle user sessions, token refresh, and persistence
- **Protected routes** - Create authentication guards for navigation
- **User management** - Access and update user profiles and metadata
- **Backend integration** - Pass Clerk JWT tokens to Firebase Cloud Functions

## Quick Start

### Installation
```bash
npx expo install @clerk/clerk-expo expo-secure-store
```

### Basic Setup
```javascript
// App.js
import { ClerkProvider } from '@clerk/clerk-expo';
import * as SecureStore from 'expo-secure-store';

const tokenCache = {
  async getToken(key) {
    return SecureStore.getItemAsync(key);
  },
  async saveToken(key, value) {
    return SecureStore.setItemAsync(key, value);
  },
};

export default function App() {
  return (
    <ClerkProvider 
      publishableKey={process.env.EXPO_PUBLIC_CLERK_PUBLISHABLE_KEY}
      tokenCache={tokenCache}
    >
      <RootNavigator />
    </ClerkProvider>
  );
}
```

## Common Patterns

### Protected Route
```javascript
import { useAuth } from '@clerk/clerk-expo';

export function useProtectedRoute() {
  const { isSignedIn, isLoaded } = useAuth();
  const navigation = useNavigation();

  useEffect(() => {
    if (isLoaded && !isSignedIn) {
      navigation.navigate('SignIn');
    }
  }, [isSignedIn, isLoaded]);

  return { isSignedIn, isLoaded };
}
```

### User Profile Access
```javascript
import { useUser } from '@clerk/clerk-expo';

export function ProfileScreen() {
  const { user } = useUser();

  const updateProfile = async () => {
    await user.update({
      firstName: 'John',
      lastName: 'Doe',
    });
  };

  return (
    <View>
      <Text>Welcome, {user.firstName}!</Text>
      <Text>Email: {user.primaryEmailAddress.emailAddress}</Text>
    </View>
  );
}
```

### Backend Token Passing
```javascript
import { useAuth } from '@clerk/clerk-expo';

export function useAuthenticatedRequest() {
  const { getToken } = useAuth();

  const makeRequest = async (endpoint, data) => {
    const token = await getToken();
    
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    return response.json();
  };

  return { makeRequest };
}
```

## N8ture AI App Integration

### Trial Management
Store user trial count in Clerk user metadata:
```javascript
// Update trial count
await user.update({
  unsafeMetadata: {
    trialCount: 3,
    totalIdentifications: 0,
  },
});

// Check trial status
const trialCount = user.unsafeMetadata.trialCount || 0;
const canIdentify = user.publicMetadata.isPremium || trialCount > 0;
```

### Premium Subscription Status
```javascript
// Store subscription status
await user.update({
  publicMetadata: {
    isPremium: true,
    subscriptionId: 'sub_xxx',
  },
});
```

## Best Practices

1. **Use token cache** - Always implement SecureStore token caching
2. **Handle loading states** - Check `isLoaded` before rendering auth-dependent UI
3. **Secure metadata** - Use `publicMetadata` for non-sensitive data, `privateMetadata` for sensitive data
4. **Error handling** - Implement proper error handling for auth failures
5. **Social auth** - Configure OAuth providers in Clerk Dashboard before implementing

## Environment Variables

```bash
# .env
EXPO_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_xxxxx
```

## Common Issues

**Issue:** "Clerk is not loaded"  
**Solution:** Always check `isLoaded` before accessing auth state

**Issue:** Token not persisting  
**Solution:** Ensure SecureStore token cache is properly configured

**Issue:** Social auth not working  
**Solution:** Configure OAuth redirect URLs in Clerk Dashboard and app.json

## Resources

- [Clerk Expo Documentation](https://clerk.com/docs/quickstarts/expo)
- [Clerk React Native SDK](https://clerk.com/docs/references/react-native/overview)
- [Authentication Best Practices](https://clerk.com/docs/security/overview)

Use this skill when implementing authentication, managing user sessions, or integrating Clerk with the N8ture AI App backend.

