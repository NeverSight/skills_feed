---
name: authentication-setup
description: Design and implement authentication and authorization systems. Use when setting up user login, JWT tokens, OAuth, session management, or role-based access control. Handles password security, token management, SSO integration.
tags: [authentication, authorization, security, JWT, OAuth, RBAC]
platforms: [Claude, ChatGPT, Gemini]
---

# Authentication Setup


## When to use this skill

이 스킬을 트리거해야 하는 구체적인 상황을 나열합니다:

- **사용자 로그인 시스템**: 새로운 애플리케이션에 사용자 인증 기능을 추가할 때
- **API 보안**: REST API나 GraphQL API에 인증 레이어를 추가할 때
- **권한 관리**: 사용자 역할에 따른 접근 제어가 필요할 때
- **인증 마이그레이션**: 기존 인증 시스템을 JWT나 OAuth로 전환할 때
- **SSO 통합**: Google, GitHub, Microsoft 등의 소셜 로그인을 통합할 때

## 입력 형식 (Input Format)

사용자로부터 받아야 할 입력의 형식과 필수/선택 정보:

### 필수 정보
- **인증 방식**: JWT, Session, OAuth 2.0 중 선택
- **백엔드 프레임워크**: Express, Django, FastAPI, Spring Boot 등
- **데이터베이스**: PostgreSQL, MySQL, MongoDB 등
- **보안 요구사항**: 비밀번호 정책, 토큰 만료 시간 등

### 선택 정보
- **MFA 지원**: 2FA/MFA 활성화 여부 (기본값: false)
- **소셜 로그인**: OAuth 제공자 (Google, GitHub, etc.)
- **세션 저장소**: Redis, in-memory 등 (Session 방식인 경우)
- **Refresh Token**: 사용 여부 (기본값: true)

### 입력 예시

```
사용자 인증 시스템을 구축해줘:
- 인증 방식: JWT
- 프레임워크: Express.js + TypeScript
- 데이터베이스: PostgreSQL
- MFA: Google Authenticator 지원
- 소셜 로그인: Google, GitHub
- Refresh Token: 사용
```

## Instructions

단계별로 정확하게 따라야 할 작업 순서를 명시합니다.

### Step 1: 데이터 모델 설계

사용자 및 인증 관련 데이터베이스 스키마를 설계합니다.

**작업 내용**:
- User 테이블 설계 (id, email, password_hash, role, created_at, updated_at)
- RefreshToken 테이블 (선택사항)
- OAuthProvider 테이블 (소셜 로그인 사용시)
- 비밀번호는 절대 평문 저장하지 않음 (bcrypt/argon2 해싱 필수)

**예시** (PostgreSQL):
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),  -- NULL if OAuth only
    role VARCHAR(50) DEFAULT 'user',
    is_verified BOOLEAN DEFAULT false,
    mfa_secret VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE refresh_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    token VARCHAR(500) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_refresh_tokens_user_id ON refresh_tokens(user_id);
```

### Step 2: 비밀번호 보안 구현

비밀번호 해싱 및 검증 로직을 구현합니다.

**작업 내용**:
- bcrypt (Node.js) 또는 argon2 (Python) 사용
- Salt rounds 최소 10 이상 설정
- 비밀번호 강도 검증 (최소 8자, 대소문자, 숫자, 특수문자)

**판단 기준**:
- Node.js 프로젝트 → bcrypt 라이브러리 사용
- Python 프로젝트 → argon2-cffi 또는 passlib 사용
- 성능이 중요한 경우 → bcrypt 선택
- 최고 보안이 필요한 경우 → argon2 선택

**예시** (Node.js + TypeScript):
```typescript
import bcrypt from 'bcrypt';

const SALT_ROUNDS = 12;

export async function hashPassword(password: string): Promise<string> {
    // 비밀번호 강도 검증
    if (password.length < 8) {
        throw new Error('Password must be at least 8 characters');
    }

    const hasUpperCase = /[A-Z]/.test(password);
    const hasLowerCase = /[a-z]/.test(password);
    const hasNumber = /\d/.test(password);
    const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(password);

    if (!hasUpperCase || !hasLowerCase || !hasNumber || !hasSpecial) {
        throw new Error('Password must contain uppercase, lowercase, number, and special character');
    }

    return await bcrypt.hash(password, SALT_ROUNDS);
}

export async function verifyPassword(password: string, hash: string): Promise<boolean> {
    return await bcrypt.compare(password, hash);
}
```

### Step 3: JWT 토큰 생성 및 검증

JWT 기반 인증을 위한 토큰 시스템을 구현합니다.

**작업 내용**:
- Access Token (짧은 만료 시간: 15분)
- Refresh Token (긴 만료 시간: 7일~30일)
- JWT 서명에 강력한 SECRET 키 사용 (환경변수로 관리)
- 토큰 페이로드에 최소 정보만 포함 (user_id, role)

**예시** (Node.js):
```typescript
import jwt from 'jsonwebtoken';

const ACCESS_TOKEN_SECRET = process.env.ACCESS_TOKEN_SECRET!;
const REFRESH_TOKEN_SECRET = process.env.REFRESH_TOKEN_SECRET!;
const ACCESS_TOKEN_EXPIRY = '15m';
const REFRESH_TOKEN_EXPIRY = '7d';

interface TokenPayload {
    userId: string;
    email: string;
    role: string;
}

export function generateAccessToken(payload: TokenPayload): string {
    return jwt.sign(payload, ACCESS_TOKEN_SECRET, {
        expiresIn: ACCESS_TOKEN_EXPIRY,
        issuer: 'your-app-name',
        audience: 'your-app-users'
    });
}

export function generateRefreshToken(payload: TokenPayload): string {
    return jwt.sign(payload, REFRESH_TOKEN_SECRET, {
        expiresIn: REFRESH_TOKEN_EXPIRY,
        issuer: 'your-app-name',
        audience: 'your-app-users'
    });
}

export function verifyAccessToken(token: string): TokenPayload {
    return jwt.verify(token, ACCESS_TOKEN_SECRET, {
        issuer: 'your-app-name',
        audience: 'your-app-users'
    }) as TokenPayload;
}

export function verifyRefreshToken(token: string): TokenPayload {
    return jwt.verify(token, REFRESH_TOKEN_SECRET, {
        issuer: 'your-app-name',
        audience: 'your-app-users'
    }) as TokenPayload;
}
```

### Step 4: 인증 미들웨어 구현

API 요청을 보호하는 인증 미들웨어를 작성합니다.

**확인 사항**:
- [x] Authorization 헤더에서 Bearer 토큰 추출
- [x] 토큰 검증 및 만료 확인
- [x] 유효한 토큰인 경우 req.user에 사용자 정보 추가
- [x] 에러 처리 (401 Unauthorized)

**예시** (Express.js):
```typescript
import { Request, Response, NextFunction } from 'express';
import { verifyAccessToken } from './jwt';

export interface AuthRequest extends Request {
    user?: {
        userId: string;
        email: string;
        role: string;
    };
}

export function authenticateToken(req: AuthRequest, res: Response, next: NextFunction) {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1]; // Bearer TOKEN

    if (!token) {
        return res.status(401).json({ error: 'Access token required' });
    }

    try {
        const payload = verifyAccessToken(token);
        req.user = payload;
        next();
    } catch (error) {
        if (error.name === 'TokenExpiredError') {
            return res.status(401).json({ error: 'Token expired' });
        }
        return res.status(403).json({ error: 'Invalid token' });
    }
}

// Role-based authorization middleware
export function requireRole(...roles: string[]) {
    return (req: AuthRequest, res: Response, next: NextFunction) => {
        if (!req.user) {
            return res.status(401).json({ error: 'Authentication required' });
        }

        if (!roles.includes(req.user.role)) {
            return res.status(403).json({ error: 'Insufficient permissions' });
        }

        next();
    };
}
```

### Step 5: 인증 API 엔드포인트 구현

회원가입, 로그인, 토큰 갱신 등의 API를 작성합니다.

**작업 내용**:
- POST /auth/register - 회원가입
- POST /auth/login - 로그인
- POST /auth/refresh - 토큰 갱신
- POST /auth/logout - 로그아웃
- GET /auth/me - 현재 사용자 정보

**예시**:
```typescript
import express from 'express';
import { hashPassword, verifyPassword } from './password';
import { generateAccessToken, generateRefreshToken, verifyRefreshToken } from './jwt';
import { authenticateToken } from './middleware';

const router = express.Router();

// 회원가입
router.post('/register', async (req, res) => {
    try {
        const { email, password } = req.body;

        // 이메일 중복 확인
        const existingUser = await db.user.findUnique({ where: { email } });
        if (existingUser) {
            return res.status(409).json({ error: 'Email already exists' });
        }

        // 비밀번호 해싱
        const passwordHash = await hashPassword(password);

        // 사용자 생성
        const user = await db.user.create({
            data: { email, password_hash: passwordHash, role: 'user' }
        });

        // 토큰 생성
        const accessToken = generateAccessToken({
            userId: user.id,
            email: user.email,
            role: user.role
        });
        const refreshToken = generateRefreshToken({
            userId: user.id,
            email: user.email,
            role: user.role
        });

        // Refresh token DB 저장
        await db.refreshToken.create({
            data: {
                user_id: user.id,
                token: refreshToken,
                expires_at: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000) // 7일
            }
        });

        res.status(201).json({
            user: { id: user.id, email: user.email, role: user.role },
            accessToken,
            refreshToken
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// 로그인
router.post('/login', async (req, res) => {
    try {
        const { email, password } = req.body;

        // 사용자 찾기
        const user = await db.user.findUnique({ where: { email } });
        if (!user || !user.password_hash) {
            return res.status(401).json({ error: 'Invalid credentials' });
        }

        // 비밀번호 확인
        const isValid = await verifyPassword(password, user.password_hash);
        if (!isValid) {
            return res.status(401).json({ error: 'Invalid credentials' });
        }

        // 토큰 생성
        const accessToken = generateAccessToken({
            userId: user.id,
            email: user.email,
            role: user.role
        });
        const refreshToken = generateRefreshToken({
            userId: user.id,
            email: user.email,
            role: user.role
        });

        // Refresh token 저장
        await db.refreshToken.create({
            data: {
                user_id: user.id,
                token: refreshToken,
                expires_at: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)
            }
        });

        res.json({
            user: { id: user.id, email: user.email, role: user.role },
            accessToken,
            refreshToken
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// 토큰 갱신
router.post('/refresh', async (req, res) => {
    try {
        const { refreshToken } = req.body;

        if (!refreshToken) {
            return res.status(401).json({ error: 'Refresh token required' });
        }

        // Refresh token 검증
        const payload = verifyRefreshToken(refreshToken);

        // DB에서 토큰 확인
        const storedToken = await db.refreshToken.findUnique({
            where: { token: refreshToken }
        });

        if (!storedToken || storedToken.expires_at < new Date()) {
            return res.status(403).json({ error: 'Invalid or expired refresh token' });
        }

        // 새 Access token 생성
        const accessToken = generateAccessToken({
            userId: payload.userId,
            email: payload.email,
            role: payload.role
        });

        res.json({ accessToken });
    } catch (error) {
        res.status(403).json({ error: 'Invalid refresh token' });
    }
});

// 현재 사용자 정보
router.get('/me', authenticateToken, async (req: AuthRequest, res) => {
    try {
        const user = await db.user.findUnique({
            where: { id: req.user!.userId },
            select: { id: true, email: true, role: true, created_at: true }
        });

        res.json({ user });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

export default router;
```

## Output format

결과물이 따라야 할 정확한 형식을 정의합니다.

### 기본 구조

```
프로젝트 디렉토리/
├── src/
│   ├── auth/
│   │   ├── password.ts          # 비밀번호 해싱/검증
│   │   ├── jwt.ts                # JWT 토큰 생성/검증
│   │   ├── middleware.ts         # 인증 미들웨어
│   │   └── routes.ts             # 인증 API 엔드포인트
│   ├── models/
│   │   └── User.ts               # 사용자 모델
│   └── database/
│       └── schema.sql            # 데이터베이스 스키마
├── .env.example                  # 환경변수 템플릿
└── README.md                     # 인증 시스템 문서
```

### 환경변수 파일 (.env.example)

```bash
# JWT Secrets (MUST change in production)
ACCESS_TOKEN_SECRET=your-access-token-secret-min-32-characters
REFRESH_TOKEN_SECRET=your-refresh-token-secret-min-32-characters

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/myapp

# OAuth (Optional)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
```

## Constraints

반드시 지켜야 할 규칙과 금지 사항을 명시합니다.

### 필수 규칙 (MUST)

1. **비밀번호 보안**: 절대 평문으로 저장하지 않음
   - bcrypt, argon2 등 검증된 해싱 알고리즘 사용
   - Salt rounds 최소 10 이상

2. **환경변수 관리**: 모든 시크릿 키는 환경변수로 관리
   - .env 파일은 .gitignore에 추가
   - .env.example로 필요한 변수 목록 제공

3. **토큰 만료**: Access Token은 짧게 (15분), Refresh Token은 적절히 (7일)
   - 보안과 UX의 균형 고려
   - Refresh Token은 DB에 저장하여 무효화 가능하게

### 금지 사항 (MUST NOT)

1. **평문 비밀번호**: 절대 비밀번호를 평문으로 저장하거나 로그에 출력하지 않음
   - 심각한 보안 위험
   - 법적 책임 문제

2. **JWT SECRET 하드코딩**: 코드에 SECRET 키를 직접 작성하지 않음
   - GitHub에 노출될 위험
   - 프로덕션 보안 취약점

3. **민감정보 토큰 포함**: JWT 페이로드에 비밀번호, 카드번호 등 민감정보 포함 금지
   - JWT는 디코딩 가능 (암호화 아님)
   - 최소한의 정보만 포함 (user_id, role)

### 보안 규칙

- **Rate Limiting**: 로그인 API에 rate limiting 적용 (brute force 방지)
- **HTTPS 필수**: 프로덕션 환경에서는 HTTPS만 사용
- **CORS 설정**: 허용된 도메인만 API 접근 가능하도록 설정
- **Input Validation**: 모든 사용자 입력 검증 (SQL Injection, XSS 방지)

## Examples

실제 사용 사례를 통해 스킬의 적용 방법을 보여줍니다.

### 예시 1: Express.js + PostgreSQL JWT 인증

**상황**: Node.js Express 앱에 JWT 기반 사용자 인증 추가

**사용자 요청**:
```
Express.js 앱에 JWT 인증을 추가해줘. PostgreSQL 사용하고,
access token은 15분, refresh token은 7일로 설정해줘.
```

**스킬 적용 과정**:

1. 패키지 설치:
   ```bash
   npm install jsonwebtoken bcrypt pg
   npm install --save-dev @types/jsonwebtoken @types/bcrypt
   ```

2. 데이터베이스 스키마 생성 (위의 SQL 사용)

3. 환경변수 설정:
   ```bash
   ACCESS_TOKEN_SECRET=$(openssl rand -base64 32)
   REFRESH_TOKEN_SECRET=$(openssl rand -base64 32)
   ```

4. 인증 모듈 구현 (위의 코드 예시 사용)

5. API 라우트 연결:
   ```typescript
   import authRoutes from './auth/routes';
   app.use('/api/auth', authRoutes);
   ```

**최종 결과**: JWT 기반 인증 시스템 완성, 회원가입/로그인/토큰갱신 API 동작

### 예시 2: Role-Based Access Control (RBAC)

**상황**: 관리자와 일반 사용자를 구분하는 권한 시스템

**사용자 요청**:
```
관리자만 접근 가능한 API를 만들어줘.
일반 사용자는 403 에러를 받아야 해.
```

**최종 결과**:
```typescript
// 관리자 전용 API
router.delete('/users/:id',
    authenticateToken,           // 인증 확인
    requireRole('admin'),         // 역할 확인
    async (req, res) => {
        // 사용자 삭제 로직
        await db.user.delete({ where: { id: req.params.id } });
        res.json({ message: 'User deleted' });
    }
);

// 사용 예시
// 일반 사용자(role: 'user') 요청 → 403 Forbidden
// 관리자(role: 'admin') 요청 → 200 OK
```

## Best practices

효과적으로 이 스킬을 사용하기 위한 권장사항입니다.

### 품질 향상

1. **Password Rotation Policy**: 주기적인 비밀번호 변경 권장
   - 90일마다 변경 알림
   - 이전 5개 비밀번호 재사용 방지
   - 사용자 경험과 보안의 균형

2. **Multi-Factor Authentication (MFA)**: 중요 계정에 2FA 적용
   - Google Authenticator, Authy 등 TOTP 앱 사용
   - SMS는 보안성 낮음 (SIM swapping 위험)
   - Backup codes 제공

3. **Audit Logging**: 모든 인증 이벤트 로깅
   - 로그인 성공/실패, IP 주소, User Agent 기록
   - 이상 탐지 및 사후 분석
   - GDPR 준수 (민감정보 제외)

### 효율성 개선

- **Token Blacklist**: 로그아웃 시 Refresh Token 무효화
- **Redis Caching**: 자주 사용하는 사용자 정보 캐싱
- **Database Indexing**: email, refresh_token에 인덱스 추가

## 자주 발생하는 문제 (Common Issues)

흔히 발생하는 문제와 해결 방법입니다.

### 문제 1: "JsonWebTokenError: invalid signature"

**증상**:
- 토큰 검증 시 에러 발생
- 로그인은 되지만 인증된 API 호출 실패

**원인**:
Access Token과 Refresh Token의 SECRET 키가 다른데,
같은 키로 검증하려고 시도

**해결방법**:
1. 환경변수 확인: `ACCESS_TOKEN_SECRET`, `REFRESH_TOKEN_SECRET`
2. 각 토큰 타입에 맞는 SECRET 사용
3. 환경변수가 제대로 로드되는지 확인 (`dotenv` 초기화)

### 문제 2: CORS 에러로 프론트엔드에서 로그인 불가

**증상**: 브라우저 콘솔에 "CORS policy" 에러

**원인**: Express 서버에 CORS 설정 누락

**해결방법**:
```typescript
import cors from 'cors';

app.use(cors({
    origin: process.env.FRONTEND_URL || 'http://localhost:3000',
    credentials: true
}));
```

### 문제 3: Refresh Token이 계속 만료됨

**증상**: 사용자가 자주 로그아웃되는 현상

**원인**: Refresh Token이 DB에서 제대로 관리되지 않음

**해결방법**:
1. Refresh Token 생성 시 DB에 저장 확인
2. 만료 시간 적절히 설정 (최소 7일)
3. 만료된 토큰 정기적으로 정리하는 cron job 추가

## References

### 공식 문서
- [JWT.io - JSON Web Token Introduction](https://jwt.io/introduction)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [OAuth 2.0 RFC 6749](https://datatracker.ietf.org/doc/html/rfc6749)

### 라이브러리
- [jsonwebtoken (Node.js)](https://github.com/auth0/node-jsonwebtoken)
- [bcrypt (Node.js)](https://github.com/kelektiv/node.bcrypt.js)
- [Passport.js](http://www.passportjs.org/) - 다양한 인증 전략
- [NextAuth.js](https://next-auth.js.org/) - Next.js 인증

### 보안 가이드
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [NIST Digital Identity Guidelines](https://pages.nist.gov/800-63-3/)

## Metadata

### 버전
- **현재 버전**: 1.0.0
- **최종 업데이트**: 2025-01-01
- **호환 플랫폼**: Claude, ChatGPT, Gemini

### 관련 스킬
- [api-design](../api-design/SKILL.md): API 엔드포인트 설계
- [security](../../infrastructure/security/SKILL.md): 보안 베스트 프랙티스

### 태그
`#authentication` `#authorization` `#JWT` `#OAuth` `#security` `#backend`