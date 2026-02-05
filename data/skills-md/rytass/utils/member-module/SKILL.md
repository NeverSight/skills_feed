---
name: member-module
description: |
  Member system NestJS module (會員系統 NestJS 模組). Use when working with user authentication (用戶認證), JWT tokens, OAuth2 integration (Google/Facebook), RBAC/ABAC permission control (權限控制), password policies (密碼策略), or Casbin integration. Keywords: 會員, 用戶, 認證, 授權, 權限, 登入, JWT, OAuth, Casbin, RBAC, ABAC, member, user, authentication, authorization, login, password
---

# Member Base NestJS Module (會員系統模組)

## Overview

`@rytass/member-base-nestjs-module` 提供完整的 NestJS 會員管理系統，包含 JWT 認證、OAuth2 整合、RBAC+Domain 權限控制（Casbin）和密碼策略管理。

## Quick Start

### 安裝

```bash
npm install @rytass/member-base-nestjs-module
```

### 基本設定

```typescript
import { MemberBaseModule } from '@rytass/member-base-nestjs-module';

@Module({
  imports: [
    TypeOrmModule.forRoot({ /* 資料庫配置 */ }),
    MemberBaseModule.forRoot({
      accessTokenExpiration: 900,       // 15 分鐘
      refreshTokenExpiration: 7776000,  // 90 天
      passwordMinLength: 12,
      casbinAdapterOptions: {
        type: 'postgres',
        host: 'localhost',
        // ...
      },
    }),
  ],
})
export class AppModule {}
```

### 會員登入

```typescript
import { MemberBaseService } from '@rytass/member-base-nestjs-module';

@Injectable()
export class AuthService {
  constructor(private readonly memberService: MemberBaseService) {}

  // 基本登入
  async login(account: string, password: string, ip?: string) {
    const tokens = await this.memberService.login(account, password, ip);
    return {
      accessToken: tokens.accessToken,
      refreshToken: tokens.refreshToken,
    };
  }

  // 登入並指定 domain（用於多租戶場景）
  async loginWithDomain(account: string, password: string, domain: string, ip?: string) {
    const tokens = await this.memberService.login(account, password, { domain, ip });
    return tokens;
  }
}
```

## Core Concepts

### JWT 認證流程

```
Client → [Bearer Token] → CasbinGuard → Verify JWT → Extract Payload → Route Handler
                                ↓
                         Check Decorators
                                ↓
                    @IsPublic / @Authenticated / @AllowActions
```

### 權限裝飾器

| 裝飾器 | 用途 | 範例 |
|--------|------|------|
| `@IsPublic()` | 完全公開 | 登入、註冊頁面 |
| `@Authenticated()` | 僅需有效 Token | 個人資料頁面 |
| `@AllowActions([...])` | RBAC 權限檢查 | 管理功能 |
| `@HasPermission([subject, action])` | 動態權限檢查 | 參數裝飾器，用於 Field Resolver |
| `@MemberId()` | 注入會員 ID | 參數裝飾器 |
| `@Account()` | 注入會員帳號 | 參數裝飾器 |

### RBAC+Domain 模型

```typescript
// Casbin 策略格式: [subject, domain, object, action]

// 定義權限: [subject, domain, object, action]
await enforcer.addPolicy('admin-role', 'articles', 'article', 'create');
await enforcer.addPolicy('admin-role', 'articles', 'article', 'delete');

// 指派角色: [member, role, domain]
await enforcer.addGroupingPolicy(memberId, 'admin-role', 'articles');

// 路由保護: @AllowActions 接受 [Subject, Action][] 二元組陣列
@AllowActions([['article', 'create']])
async createArticle() { }
```

## Common Patterns

### 完整認證設定

```typescript
MemberBaseModule.forRootAsync({
  imports: [ConfigModule],
  inject: [ConfigService],
  useFactory: async (config: ConfigService) => ({
    accessTokenSecret: config.get('JWT_ACCESS_SECRET'),
    accessTokenExpiration: 900,
    refreshTokenSecret: config.get('JWT_REFRESH_SECRET'),
    refreshTokenExpiration: 7776000,

    // 密碼策略
    passwordMinLength: 12,
    passwordShouldIncludeUppercase: true,
    passwordShouldIncludeLowercase: true,
    passwordShouldIncludeDigit: true,
    passwordShouldIncludeSpecialCharacters: true,
    passwordHistoryLimit: 5,
    passwordAgeLimitInDays: 90,

    // 登入安全
    loginFailedBanThreshold: 5,
    loginFailedAutoUnlockSeconds: 1800,

    // Casbin
    casbinAdapterOptions: {
      type: 'postgres',
      host: config.get('DB_HOST'),
      port: config.get('DB_PORT'),
      username: config.get('DB_USER'),
      password: config.get('DB_PASS'),
      database: config.get('DB_NAME'),
    },
  }),
})
```

### OAuth2 整合

支援三種 OAuth2 Provider 類型：

```typescript
import { OAuth2Provider, GoogleOAuth2Provider, FacebookOAuth2Provider, CustomOAuth2Provider } from '@rytass/member-base-nestjs-module';

// Google Provider
const googleProvider: GoogleOAuth2Provider = {
  channel: 'google',
  clientId: process.env.GOOGLE_CLIENT_ID!,
  clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
  redirectUri: 'https://app.com/auth/callbacks/google',
  scope: ['profile', 'email'],  // 可選
  getState: () => crypto.randomUUID(),  // 可選
};

// Facebook Provider
const facebookProvider: FacebookOAuth2Provider = {
  channel: 'facebook',
  clientId: process.env.FACEBOOK_APP_ID!,
  clientSecret: process.env.FACEBOOK_APP_SECRET!,
  redirectUri: 'https://app.com/auth/callbacks/facebook',
  scope: ['email', 'public_profile'],
};

// Custom OAuth2 Provider（自訂 OAuth2 服務）
const customProvider: CustomOAuth2Provider = {
  channel: 'line',  // 自訂名稱（非 google/facebook）
  clientId: process.env.LINE_CLIENT_ID!,
  clientSecret: process.env.LINE_CLIENT_SECRET!,
  redirectUri: 'https://app.com/auth/callbacks/line',
  scope: ['profile', 'openid'],  // 必填
  requestUrl: 'https://access.line.me/oauth2/v2.1/authorize',  // 必填
  getAccessTokenFromCode: async (code) => {
    // 實作從 code 取得 access token 的邏輯
    const response = await fetch('https://api.line.me/oauth2/v2.1/token', { /* ... */ });
    return response.access_token;
  },
  getAccountFromAccessToken: async (accessToken) => {
    // 實作從 access token 取得使用者識別的邏輯
    const profile = await fetch('https://api.line.me/v2/profile', { /* ... */ });
    return profile.userId;  // 回傳唯一識別碼
  },
};

// 模組配置
MemberBaseModule.forRoot({
  oauth2Providers: [googleProvider, facebookProvider, customProvider],
  oauth2ClientDestUrl: '/dashboard',
});
```

**內建 OAuth2 Controller 路由：**

```
GET /auth/login/google           // 重導向到 Google OAuth
GET /auth/callbacks/google       // 處理 Google 回調
GET /auth/login/facebook         // 重導向到 Facebook OAuth
GET /auth/callbacks/facebook     // 處理 Facebook 回調
GET /auth/login/:channel         // 自訂 OAuth provider
GET /auth/callbacks/:channel     // 自訂 provider 回調
```

**OAuthService 方法：**

> **注意：** `OAuthService` 未透過 `index.ts` 導出，僅能透過 NestJS 依賴注入使用。

```typescript
// OAuthService 透過 DI 注入（不能直接 import）
import { Inject, Injectable } from '@nestjs/common';

@Injectable()
export class AuthController {
  constructor(private readonly oauthService: OAuthService) {}

  // 取得 OAuth 登入 URL
  async getGoogleUrl(): Promise<string> {
    return this.oauthService.getGoogleOAuthLoginUrl();
  }

  async getFacebookUrl(): Promise<string> {
    return this.oauthService.getFacebookOAuthLoginUrl();
  }

  async getCustomUrl(channel: string): Promise<string> {
    return this.oauthService.getCustomOAuthLoginUrl(channel);
  }

  // 處理 OAuth callback（回傳 TokenPairDto & { state?: string }）
  async googleCallback(code: string, state?: string) {
    return this.oauthService.loginWithGoogleOAuth2Code(code, state);
  }

  async facebookCallback(code: string, state?: string) {
    return this.oauthService.loginWithFacebookOAuth2Code(code, state);
  }

  async customCallback(channel: string, code: string, state?: string) {
    return this.oauthService.loginWithCustomOAuth2Code(channel, code, state);
  }
}
```

**OAuth2Provider Type Guards：**

> **注意：** 這些 Type Guards 目前未透過 `index.ts` 導出，若需要使用請在專案中自行定義：

```typescript
// 自行定義 Type Guards（因未從 package 導出）
type OAuth2Provider = GoogleOAuth2Provider | FacebookOAuth2Provider | CustomOAuth2Provider;

function isGoogleProvider(p: OAuth2Provider): p is GoogleOAuth2Provider {
  return p.channel === 'google';
}
function isFacebookProvider(p: OAuth2Provider): p is FacebookOAuth2Provider {
  return p.channel === 'facebook';
}
function isCustomProvider(p: OAuth2Provider): p is CustomOAuth2Provider {
  return p.channel !== 'google' && p.channel !== 'facebook';
}
```

### 自訂會員實體

```typescript
import { BaseMemberEntity } from '@rytass/member-base-nestjs-module';

@Entity('members')
@ChildEntity()
export class CustomMember extends BaseMemberEntity {
  @Column({ nullable: true })
  displayName?: string;

  @Column({ default: false })
  isVerified: boolean;

  @Column({ type: 'jsonb', nullable: true })
  profile?: Record<string, any>;
}

// 模組配置
MemberBaseModule.forRoot({
  memberEntity: CustomMember,
})
```

### 自訂 JWT Payload

```typescript
MemberBaseModule.forRoot({
  customizedJwtPayload: (member) => ({
    id: member.id,
    account: member.account,
    displayName: member.displayName,
    roles: member.roles,
  }),
})
```

### 會員註冊

```typescript
@Injectable()
export class RegistrationService {
  constructor(private readonly memberService: MemberBaseService) {}

  // 一般註冊
  async register(account: string, password: string) {
    return this.memberService.register(account, password, {
      displayName: 'New User',  // 可傳入自訂欄位
    });
  }

  // 無密碼註冊（系統產生密碼）
  async registerWithoutPassword(account: string) {
    const [member, generatedPassword] = await this.memberService.registerWithoutPassword(account, {
      shouldUpdatePassword: true,  // 預設 true
    });
    // 發送 email 包含臨時密碼
    return member;
  }
}
```

### 密碼重設流程

```typescript
@Injectable()
export class PasswordResetService {
  constructor(private readonly memberService: MemberBaseService) {}

  async requestReset(account: string) {
    const token = await this.memberService.getResetPasswordToken(account);
    // 發送 email 包含 token
    return { message: 'Reset email sent' };
  }

  async resetPassword(token: string, newPassword: string) {
    await this.memberService.changePasswordWithToken(token, newPassword);
    return { message: 'Password changed' };
  }

  // 變更密碼（需舊密碼）
  async changePassword(memberId: string, oldPassword: string, newPassword: string) {
    await this.memberService.changePassword(memberId, oldPassword, newPassword);
    return { message: 'Password changed' };
  }
}
```

### Token 刷新

```typescript
@Injectable()
export class TokenService {
  constructor(private readonly memberService: MemberBaseService) {}

  async refresh(refreshToken: string, domain?: string) {
    return this.memberService.refreshToken(refreshToken, { domain });
  }
}
```

### 解鎖帳號

```typescript
@Injectable()
export class AdminService {
  constructor(private readonly memberService: MemberBaseService) {}

  // 重設登入失敗次數（解鎖帳號）
  async unlockMember(memberId: string) {
    return this.memberService.resetLoginFailedCounter(memberId);
  }
}
```

### 管理員操作 (MemberBaseAdminService)

```typescript
import { MemberBaseAdminService } from '@rytass/member-base-nestjs-module';

@Injectable()
export class AdminManagementService {
  constructor(private readonly adminService: MemberBaseAdminService) {}

  // 軟刪除會員
  async archiveMember(memberId: string): Promise<void> {
    return this.adminService.archiveMember(memberId);
  }

  // 管理員重設密碼（可跳過密碼策略檢查）
  async resetMemberPassword(
    memberId: string,
    newPassword: string,
    ignorePasswordPolicy?: boolean  // 預設 false
  ) {
    return this.adminService.resetMemberPassword(memberId, newPassword, ignorePasswordPolicy);
  }
}
```

### 密碼驗證工具 (PasswordValidatorService)

```typescript
import { PasswordValidatorService } from '@rytass/member-base-nestjs-module';

@Injectable()
export class PasswordService {
  constructor(private readonly passwordValidator: PasswordValidatorService) {}

  // 產生符合策略的隨機密碼
  generatePassword(): string {
    return this.passwordValidator.generateValidPassword();
  }

  // 檢查密碼是否過期
  checkPasswordExpiry(member: MemberEntity): boolean {
    return this.passwordValidator.shouldUpdatePassword(member);
  }

  // 驗證密碼是否符合策略（支援歷史檢查）
  async validatePassword(password: string, memberId?: string): Promise<boolean> {
    return this.passwordValidator.validatePassword(password, memberId);
  }
}
```

### GraphQL 整合

```typescript
import { GraphQLModule } from '@nestjs/graphql';
import { GraphQLContextTokenResolver } from '@rytass/member-base-nestjs-module';

@Module({
  imports: [
    GraphQLModule.forRoot({
      context: GraphQLContextTokenResolver,  // 自動提取 Token
      fieldResolverEnhancers: ['guards'],
    }),
    MemberBaseModule.forRoot({ /* ... */ }),
  ],
})
export class AppModule {}
```

## Module Options

### 認證選項

| 選項 | 預設 | 說明 |
|------|------|------|
| `accessTokenSecret` | 隨機 | JWT Access Token 簽署密鑰 |
| `accessTokenExpiration` | 900 | Access Token 過期時間（秒）|
| `refreshTokenSecret` | 隨機 | Refresh Token 密鑰 |
| `refreshTokenExpiration` | 7776000 | Refresh Token 過期時間（秒）|
| `onlyResetRefreshTokenExpirationByPassword` | false | 僅在密碼變更時重設 Refresh Token 過期時間 |
| `cookieMode` | false | 使用 HTTP-only Cookie（分兩個 cookie: ACCESS_TOKEN 和 REFRESH_TOKEN）|
| `accessTokenCookieName` | 'ACCESS_TOKEN' | Access Token Cookie 名稱（cookieMode 時有效）|
| `refreshTokenCookieName` | 'REFRESH_TOKEN' | Refresh Token Cookie 名稱（cookieMode 時有效）|

### 密碼重設

| 選項 | 預設 | 說明 |
|------|------|------|
| `resetPasswordTokenSecret` | 隨機 | 密碼重設 Token 簽署密鑰 |
| `resetPasswordTokenExpiration` | 3600 | 密碼重設 Token 過期時間（秒，預設 1 小時）|

### 密碼策略

| 選項 | 預設 | 說明 |
|------|------|------|
| `passwordMinLength` | 8 | 最小長度 |
| `passwordShouldIncludeUppercase` | true | 需含大寫 |
| `passwordShouldIncludeLowercase` | true | 需含小寫 |
| `passwordShouldIncludeDigit` | true | 需含數字 |
| `passwordShouldIncludeSpecialCharacters` | false | 需含特殊字符 |
| `passwordPolicyRegExp` | undefined | 自訂密碼驗證 RegExp（設定後覆蓋上述選項）|
| `passwordHistoryLimit` | undefined | 密碼歷史限制（禁止重複使用最近 N 組密碼）|
| `passwordAgeLimitInDays` | undefined | 密碼有效天數 |

### 登入安全

| 選項 | 預設 | 說明 |
|------|------|------|
| `loginFailedBanThreshold` | 5 | 失敗次數上限 |
| `loginFailedAutoUnlockSeconds` | null | 自動解鎖時間（秒）|
| `forceRejectLoginOnPasswordExpired` | false | 密碼過期時拒絕登入 |

### Casbin 權限控制

| 選項 | 預設 | 說明 |
|------|------|------|
| `enableGlobalGuard` | true | 啟用全域 Guard |
| `casbinAdapterOptions` | - | TypeORM Adapter 配置 |
| `casbinModelString` | RBAC with domains | Casbin Model 定義 |
| `casbinPermissionDecorator` | - | 自訂權限裝飾器 |
| `casbinPermissionChecker` | - | 自訂權限檢查函式 |

### 實體與 Payload

| 選項 | 預設 | 說明 |
|------|------|------|
| `memberEntity` | BaseMemberEntity | 自訂會員實體類別 |
| `customizedJwtPayload` | - | 自訂 JWT Payload 產生函式 |

### OAuth2

| 選項 | 預設 | 說明 |
|------|------|------|
| `oauth2Providers` | - | OAuth2 Provider 陣列 |
| `oauth2ClientDestUrl` | '/login' | OAuth2 登入後重導向 URL |

## Symbol Tokens

可用於依賴注入的 Symbol Tokens：

```typescript
import {
  // Repository Token
  RESOLVED_MEMBER_REPO,         // Repository<BaseMemberEntity>
  RESOLVED_MEMBER_REPOSITORY,   // 別名，等同 RESOLVED_MEMBER_REPO
  BASE_MEMBER_REPOSITORY,       // BaseMemberRepo Symbol

  // Casbin
  CASBIN_ENFORCER,              // Casbin Enforcer 實例

  // Module Options
  MEMBER_BASE_MODULE_OPTIONS,   // 完整模組配置

  // Token Settings
  ACCESS_TOKEN_SECRET,
  ACCESS_TOKEN_EXPIRATION,
  REFRESH_TOKEN_SECRET,
  REFRESH_TOKEN_EXPIRATION,

  // Feature Flags
  ENABLE_GLOBAL_GUARD,
  ONLY_RESET_REFRESH_TOKEN_EXPIRATION_BY_PASSWORD,
  COOKIE_MODE,
  ACCESS_TOKEN_COOKIE_NAME,
  REFRESH_TOKEN_COOKIE_NAME,
} from '@rytass/member-base-nestjs-module';

// 使用範例
@Injectable()
export class CustomService {
  constructor(
    @Inject(RESOLVED_MEMBER_REPO)
    private readonly memberRepo: Repository<BaseMemberEntity>,

    @Inject(CASBIN_ENFORCER)
    private readonly enforcer: Enforcer,
  ) {}
}
```

## Constants

### DEFAULT_CASBIN_DOMAIN

預設的 Casbin Domain 值：

```typescript
import { DEFAULT_CASBIN_DOMAIN } from '@rytass/member-base-nestjs-module';

// 值: '::DEFAULT::'
// 用於未指定 domain 時的預設 domain
```

## Additional Exported Entities

```typescript
import {
  // 實體
  BaseMemberEntity,
  MemberLoginLogEntity,
  MemberPasswordHistoryEntity,
  MemberOAuthRecordEntity,

  // 實體 Repository Symbols
  MemberLoginLogRepo,           // Symbol('MemberLoginLogRepo')
} from '@rytass/member-base-nestjs-module';
```

## API Reference

詳細 API 文件請參閱 [reference.md](reference.md)。

## Data Types

### TokenPairDto

登入成功後的回傳結構：

```typescript
interface TokenPairDto {
  accessToken: string;           // JWT Access Token
  refreshToken: string;          // Refresh Token
  shouldUpdatePassword?: boolean; // 密碼是否需要更新（僅啟用密碼過期檢查時返回）
  passwordChangedAt?: string;    // ISO8601 格式，上次密碼更改時間
}
```

## Error Codes

| 代碼 | 錯誤類別 | 說明 |
|------|----------|------|
| 100 | `MemberNotFoundError` | 找不到會員 |
| 101 | `PasswordDoesNotMeetPolicyError` | 密碼不符合策略 |
| 102 | `InvalidPasswordError` | 密碼錯誤 |
| 103 | `PasswordValidationError` | 密碼驗證失敗 |
| 104 | `InvalidToken` | Token 無效 |
| 105 | `MemberAlreadyExistedError` | 會員已存在 |
| 106 | `PasswordChangedError` | 密碼已變更 |
| 107 | `MemberBannedError` | 會員已被停權 |
| 108 | `PasswordExpiredError` | 密碼已過期 |
| 109 | `PasswordShouldUpdatePasswordError` | 需要更新密碼 |
| 110 | `PasswordInHistoryError` | 密碼在歷史記錄中（不能重複使用）|

### Errors 物件導出

所有錯誤類別透過 `Errors` 物件統一導出：

```typescript
import { Errors } from '@rytass/member-base-nestjs-module';

// 使用範例
if (error instanceof Errors.MemberNotFoundError) {
  console.log('會員不存在');
}

// Errors 包含：
// - MemberNotFoundError
// - PasswordDoesNotMeetPolicyError
// - InvalidPasswordError
// - PasswordValidationError
// - InvalidToken
// - MemberAlreadyExistedError
// - PasswordChangedError
// - MemberBannedError
// - PasswordExpiredError
// - PasswordShouldUpdatePasswordError
```

> **注意：** `PasswordInHistoryError` 目前未包含在 `Errors` 物件中，需直接從 `./constants/errors/base.error` 導入使用。

## Troubleshooting

### Token 驗證失敗

1. 確認 `accessTokenSecret` 一致
2. 檢查 Token 是否過期
3. 驗證 Bearer 格式正確

### Casbin 權限不生效

1. 確認 `casbinAdapterOptions` 配置正確
2. 檢查策略是否正確添加
3. 確認 domain 參數匹配

### 密碼策略錯誤

錯誤代碼 101: `PasswordDoesNotMeetPolicyError`
- 檢查密碼長度、大小寫、數字、特殊字符要求
- 使用 `PasswordValidatorService.validatePassword()` 測試
