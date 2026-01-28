---
name: jwt-authentication
description: Implement secure JWT (JSON Web Token) authentication in Node.js applications with access/refresh tokens and role-based access control
sasmp_version: "1.3.0"
bonded_agent: 01-nodejs-fundamentals
bond_type: PRIMARY_BOND
---

# JWT Authentication Skill

Implement secure, scalable authentication in Node.js applications using JSON Web Tokens.

## Quick Start

JWT authentication in 4 steps:
1. **Install** - `npm install jsonwebtoken bcryptjs`
2. **Register** - Hash password, create user, generate token
3. **Login** - Verify password, generate token
4. **Protect** - Verify token in middleware

## Core Concepts

### Generate JWT
```javascript
const jwt = require('jsonwebtoken');

function generateToken(userId) {
  return jwt.sign(
    { id: userId },
    process.env.JWT_SECRET,
    { expiresIn: '1h' }
  );
}

function generateRefreshToken(userId) {
  return jwt.sign(
    { id: userId },
    process.env.JWT_REFRESH_SECRET,
    { expiresIn: '7d' }
  );
}
```

### User Registration
```javascript
const bcrypt = require('bcryptjs');

async function register(req, res) {
  const { email, password, name } = req.body;

  // Check if user exists
  const existingUser = await User.findOne({ email });
  if (existingUser) {
    return res.status(409).json({ error: 'User already exists' });
  }

  // Hash password
  const hashedPassword = await bcrypt.hash(password, 10);

  // Create user
  const user = await User.create({
    email,
    password: hashedPassword,
    name
  });

  // Generate tokens
  const accessToken = generateToken(user._id);
  const refreshToken = generateRefreshToken(user._id);

  res.status(201).json({
    user: { id: user._id, email, name },
    accessToken,
    refreshToken
  });
}
```

### User Login
```javascript
async function login(req, res) {
  const { email, password } = req.body;

  // Find user
  const user = await User.findOne({ email });
  if (!user) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  // Verify password
  const isValid = await bcrypt.compare(password, user.password);
  if (!isValid) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  // Generate tokens
  const accessToken = generateToken(user._id);
  const refreshToken = generateRefreshToken(user._id);

  res.json({
    user: { id: user._id, email: user.email },
    accessToken,
    refreshToken
  });
}
```

### Authentication Middleware
```javascript
async function authenticate(req, res, next) {
  try {
    // Get token from header
    const authHeader = req.headers.authorization;
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res.status(401).json({ error: 'No token provided' });
    }

    const token = authHeader.split(' ')[1];

    // Verify token
    const decoded = jwt.verify(token, process.env.JWT_SECRET);

    // Get user
    const user = await User.findById(decoded.id).select('-password');
    if (!user) {
      return res.status(401).json({ error: 'User not found' });
    }

    req.user = user;
    next();
  } catch (error) {
    res.status(401).json({ error: 'Invalid token' });
  }
}

// Usage
router.get('/profile', authenticate, getProfile);
```

## Learning Path

### Beginner (1-2 weeks)
- ✅ Understand JWT structure
- ✅ Implement registration/login
- ✅ Create authentication middleware
- ✅ Protect routes

### Intermediate (3-4 weeks)
- ✅ Refresh token flow
- ✅ Role-based access control
- ✅ Password reset flow
- ✅ Token blacklisting

### Advanced (5-6 weeks)
- ✅ OAuth integration
- ✅ Two-factor authentication
- ✅ Session management
- ✅ Security best practices

## Advanced Patterns

### Role-Based Access Control
```javascript
const authorize = (...roles) => {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({ error: 'Not authenticated' });
    }

    if (!roles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }

    next();
  };
};

// Usage
router.delete('/users/:id',
  authenticate,
  authorize('admin', 'moderator'),
  deleteUser
);
```

### Token Refresh
```javascript
async function refreshAccessToken(req, res) {
  const { refreshToken } = req.body;

  try {
    const decoded = jwt.verify(refreshToken, process.env.JWT_REFRESH_SECRET);

    // Verify refresh token exists in database
    const stored = await RefreshToken.findOne({
      token: refreshToken,
      userId: decoded.id
    });

    if (!stored) {
      return res.status(401).json({ error: 'Invalid refresh token' });
    }

    // Generate new access token
    const accessToken = generateToken(decoded.id);

    res.json({ accessToken });
  } catch (error) {
    res.status(401).json({ error: 'Token refresh failed' });
  }
}
```

### Password Reset Flow
```javascript
async function requestPasswordReset(req, res) {
  const { email } = req.body;
  const user = await User.findOne({ email });

  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }

  // Generate reset token (short expiry)
  const resetToken = jwt.sign(
    { id: user._id, purpose: 'reset' },
    process.env.JWT_SECRET,
    { expiresIn: '15m' }
  );

  // Send email with reset link
  await sendResetEmail(user.email, resetToken);

  res.json({ message: 'Reset email sent' });
}

async function resetPassword(req, res) {
  const { token, newPassword } = req.body;

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);

    if (decoded.purpose !== 'reset') {
      return res.status(400).json({ error: 'Invalid token' });
    }

    const hashedPassword = await bcrypt.hash(newPassword, 10);
    await User.findByIdAndUpdate(decoded.id, { password: hashedPassword });

    res.json({ message: 'Password reset successful' });
  } catch (error) {
    res.status(400).json({ error: 'Invalid or expired token' });
  }
}
```

## Security Best Practices
- ✅ Use strong JWT secrets (32+ characters, random)
- ✅ Short expiry for access tokens (15min - 1h)
- ✅ Longer expiry for refresh tokens (7d - 30d)
- ✅ Store refresh tokens in database
- ✅ Hash passwords with bcrypt (10+ rounds)
- ✅ Use HTTPS in production
- ✅ Implement rate limiting
- ✅ Validate all inputs
- ✅ Don't store sensitive data in JWT payload

## JWT Structure
```
header.payload.signature

Header (base64):
{
  "alg": "HS256",
  "typ": "JWT"
}

Payload (base64):
{
  "id": "user123",
  "iat": 1516239022,
  "exp": 1516242622
}

Signature:
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret
)
```

## Common JWT Claims
- `iss` - Issuer
- `sub` - Subject (user ID)
- `aud` - Audience
- `exp` - Expiration time
- `iat` - Issued at
- `nbf` - Not before

## When to Use

Use JWT authentication when:
- Building stateless REST APIs
- Need scalability (no server-side sessions)
- Mobile app authentication
- Microservices architecture
- Single sign-on (SSO)

## Related Skills
- Express REST API (protect API endpoints)
- Database Integration (store users)
- Testing & Debugging (test auth flows)
- Performance Optimization (token caching)

## Resources
- [JWT.io](https://jwt.io)
- [OWASP Authentication Guide](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [bcrypt Documentation](https://www.npmjs.com/package/bcryptjs)
