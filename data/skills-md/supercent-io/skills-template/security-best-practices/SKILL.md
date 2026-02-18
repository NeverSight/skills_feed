---
name: security-best-practices
description: Implement security best practices for web applications and infrastructure. Use when securing APIs, preventing common vulnerabilities, or implementing security policies. Handles HTTPS, CORS, XSS, SQL Injection, CSRF, rate limiting, and OWASP Top 10.
tags: [security, HTTPS, CORS, XSS, SQL-injection, CSRF, OWASP, rate-limiting]
platforms: [Claude, ChatGPT, Gemini]
---

# Security Best Practices


## When to use this skill

- **신규 프로젝트**: 처음부터 보안 고려
- **보안 감사**: 취약점 점검 및 수정
- **API 공개**: 외부 접근 API 보안 강화
- **컴플라이언스**: GDPR, PCI-DSS 등 준수

## Instructions

### Step 1: HTTPS 강제 및 보안 헤더

**Express.js 보안 미들웨어**:
```typescript
import express from 'express';
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';

const app = express();

// Helmet: 보안 헤더 자동 설정
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'unsafe-inline'", "https://trusted-cdn.com"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", "data:", "https:"],
      connectSrc: ["'self'", "https://api.example.com"],
      fontSrc: ["'self'", "https:", "data:"],
      objectSrc: ["'none'"],
      mediaSrc: ["'self'"],
      frameSrc: ["'none'"],
    },
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true
  }
}));

// HTTPS 강제
app.use((req, res, next) => {
  if (process.env.NODE_ENV === 'production' && !req.secure) {
    return res.redirect(301, `https://${req.headers.host}${req.url}`);
  }
  next();
});

// Rate Limiting (DDoS 방지)
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15분
  max: 100, // IP당 최대 100 요청
  message: 'Too many requests from this IP, please try again later.',
  standardHeaders: true,
  legacyHeaders: false,
});

app.use('/api/', limiter);

// Auth 엔드포인트는 더 엄격하게
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5, // 15분에 5번만
  skipSuccessfulRequests: true // 성공 요청은 카운트하지 않음
});

app.use('/api/auth/login', authLimiter);
```

### Step 2: Input Validation (SQL Injection, XSS 방지)

**Joi 검증**:
```typescript
import Joi from 'joi';

const userSchema = Joi.object({
  email: Joi.string().email().required(),
  password: Joi.string().min(8).pattern(/^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/).required(),
  name: Joi.string().min(2).max(50).required()
});

app.post('/api/users', async (req, res) => {
  // 1. Input 검증
  const { error, value } = userSchema.validate(req.body);

  if (error) {
    return res.status(400).json({ error: error.details[0].message });
  }

  // 2. SQL Injection 방지: Parameterized Queries
  // ❌ 나쁜 예
  // db.query(`SELECT * FROM users WHERE email = '${email}'`);

  // ✅ 좋은 예
  const user = await db.query('SELECT * FROM users WHERE email = ?', [value.email]);

  // 3. XSS 방지: Output Encoding
  // React/Vue는 자동으로 escape, 그 외는 라이브러리 사용
  import DOMPurify from 'isomorphic-dompurify';
  const sanitized = DOMPurify.sanitize(userInput);

  res.json({ user: sanitized });
});
```

### Step 3: CSRF 방지

**CSRF Token**:
```typescript
import csrf from 'csurf';
import cookieParser from 'cookie-parser';

app.use(cookieParser());

// CSRF protection
const csrfProtection = csrf({ cookie: true });

// CSRF 토큰 제공
app.get('/api/csrf-token', csrfProtection, (req, res) => {
  res.json({ csrfToken: req.csrfToken() });
});

// 모든 POST/PUT/DELETE 요청에 CSRF 검증
app.post('/api/*', csrfProtection, (req, res, next) => {
  next();
});

// 클라이언트에서 사용
// fetch('/api/users', {
//   method: 'POST',
//   headers: {
//     'CSRF-Token': csrfToken
//   },
//   body: JSON.stringify(data)
// });
```

### Step 4: Secrets 관리

**.env (절대 커밋하지 않음)**:
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/mydb

# JWT
ACCESS_TOKEN_SECRET=your-super-secret-access-token-key-min-32-chars
REFRESH_TOKEN_SECRET=your-super-secret-refresh-token-key-min-32-chars

# API Keys
STRIPE_SECRET_KEY=sk_test_xxx
SENDGRID_API_KEY=SG.xxx
```

**Kubernetes Secrets**:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secrets
type: Opaque
stringData:
  database-url: postgresql://user:password@postgres:5432/mydb
  jwt-secret: your-jwt-secret
```

```typescript
// 환경변수에서 읽기
const dbUrl = process.env.DATABASE_URL;
if (!dbUrl) {
  throw new Error('DATABASE_URL environment variable is required');
}
```

### Step 5: API 인증 보안

**JWT + Refresh Token Rotation**:
```typescript
// Access Token 짧게 (15분)
const accessToken = jwt.sign({ userId }, ACCESS_SECRET, { expiresIn: '15m' });

// Refresh Token 길게 (7일), DB에 저장
const refreshToken = jwt.sign({ userId }, REFRESH_SECRET, { expiresIn: '7d' });
await db.refreshToken.create({
  userId,
  token: refreshToken,
  expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)
});

// Refresh Token Rotation: 사용 시마다 새로 발급
app.post('/api/auth/refresh', async (req, res) => {
  const { refreshToken } = req.body;

  const payload = jwt.verify(refreshToken, REFRESH_SECRET);

  // 기존 토큰 무효화
  await db.refreshToken.delete({ where: { token: refreshToken } });

  // 새 토큰 발급
  const newAccessToken = jwt.sign({ userId: payload.userId }, ACCESS_SECRET, { expiresIn: '15m' });
  const newRefreshToken = jwt.sign({ userId: payload.userId }, REFRESH_SECRET, { expiresIn: '7d' });

  await db.refreshToken.create({
    userId: payload.userId,
    token: newRefreshToken,
    expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)
  });

  res.json({ accessToken: newAccessToken, refreshToken: newRefreshToken });
});
```

## Constraints

### 필수 규칙 (MUST)

1. **HTTPS Only**: 프로덕션에서 HTTPS 필수
2. **Secrets 분리**: 환경변수로 관리, 절대 코드에 하드코딩 금지
3. **Input Validation**: 모든 사용자 입력 검증
4. **Parameterized Queries**: SQL Injection 방지
5. **Rate Limiting**: DDoS 방지

### 금지 사항 (MUST NOT)

1. **eval() 사용 금지**: 코드 인젝션 위험
2. **innerHTML 직접 사용**: XSS 위험
3. **Secrets 커밋**: .env 파일 절대 커밋하지 않음

## OWASP Top 10 체크리스트

```markdown
- [ ] A01: Broken Access Control - RBAC, 권한 검증
- [ ] A02: Cryptographic Failures - HTTPS, 암호화
- [ ] A03: Injection - Parameterized Queries, Input Validation
- [ ] A04: Insecure Design - Security by Design
- [ ] A05: Security Misconfiguration - Helmet, 기본 비밀번호 변경
- [ ] A06: Vulnerable Components - npm audit, 정기 업데이트
- [ ] A07: Authentication Failures - 강력한 인증, MFA
- [ ] A08: Data Integrity Failures - 서명 검증, CSRF 방지
- [ ] A09: Logging Failures - 보안 이벤트 로깅
- [ ] A10: SSRF - 외부 요청 검증
```

## Best practices

1. **Principle of Least Privilege**: 최소 권한 부여
2. **Defense in Depth**: 다층 보안
3. **Security Audits**: 정기적인 보안 점검

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [helmet.js](https://helmetjs.github.io/)
- [Security Checklist](https://github.com/shieldfy/API-Security-Checklist)

## Metadata

### 버전
- **현재 버전**: 1.0.0
- **최종 업데이트**: 2025-01-01
- **호환 플랫폼**: Claude, ChatGPT, Gemini

### 관련 스킬
- [authentication-setup](../../backend/authentication/SKILL.md)
- [deployment](../deployment/SKILL.md)

### 태그
`#security` `#OWASP` `#HTTPS` `#CORS` `#XSS` `#SQL-injection` `#CSRF` `#infrastructure`

## Examples

### Example 1: Basic usage
<!-- Add example content here -->

### Example 2: Advanced usage
<!-- Add advanced example content here -->
