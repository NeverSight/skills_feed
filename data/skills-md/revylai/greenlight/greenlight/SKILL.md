---
name: greenlight
description: >
  Pre-submission compliance scanner for Apple App Store. Use this skill when reviewing
  iOS, macOS, tvOS, watchOS, or visionOS app code (Swift, Objective-C, React Native, Expo)
  to identify potential App Store rejection risks before submission. Triggers on tasks involving
  app review preparation, compliance checking, App Store submission readiness, or when a user
  asks about App Store guidelines.
---

# Greenlight — App Store Pre-Submission Scanner

You are an expert at preparing iOS apps for App Store submission. You have access to the `greenlight` CLI which runs automated compliance checks. Your job is to run the checks, interpret the results, fix every issue, and re-run until the app passes with GREENLIT status.

## Step 1: Run the scan

Run `greenlight preflight` immediately on the project root. Do NOT try to install greenlight — it is already available in PATH. Just run it:

```bash
greenlight preflight .
```

If the user has a built IPA, include it:
```bash
greenlight preflight . --ipa /path/to/build.ipa
```

If `greenlight` is not found, install it:
```bash
# Homebrew (macOS)
brew install revylai/tap/greenlight

# Go install
go install github.com/RevylAI/greenlight/cmd/greenlight@latest

# Build from source
git clone https://github.com/RevylAI/greenlight.git
cd greenlight && make build
# Binary at: build/greenlight
```

## Step 2: Read the output and fix every issue

Every finding has a severity, guideline reference, file location, and fix suggestion. Fix them in order:
1. **CRITICAL** — Will be rejected. Must fix.
2. **WARN** — High rejection risk. Should fix.
3. **INFO** — Best practice. Consider fixing.

When fixing issues:
- **Hardcoded secrets** → Move to environment variables (use `process.env.VAR_NAME` or Expo's `Constants.expoConfig.extra`)
- **External payment for digital goods** → Replace Stripe/PayPal with StoreKit/IAP for digital content. External payment is only OK for physical goods.
- **Social login without Sign in with Apple** → Add `expo-apple-authentication` alongside Google/Facebook login
- **Account creation without deletion** → Add a "Delete Account" option in settings
- **Platform references** → Remove mentions of "Android", "Google Play", "Windows", etc.
- **Placeholder content** → Replace "Lorem ipsum", "Coming soon", "TBD" with real content
- **Vague purpose strings** → Rewrite to explain specifically WHY the app needs the permission (not just "Camera needed" but "PostureGuard uses your camera to analyze sitting posture in real-time")
- **Hardcoded IPv4** → Replace IP addresses with proper hostnames
- **HTTP URLs** → Change `http://` to `https://`
- **Console logs** → Remove or gate behind `__DEV__` flag
- **Missing privacy policy** → Note that this needs to be set in App Store Connect

## Step 3: Re-run and repeat

After fixing issues, re-run the scan:
```bash
greenlight preflight .
```

**Keep looping until the output shows GREENLIT status (zero CRITICAL findings).** Some fixes can introduce new issues (e.g., adding a tracking SDK requires ATT). The scan runs in under 1 second so re-run frequently.

## Severity Levels

| Level | Label | Action Required |
|-------|-------|----------------|
| CRITICAL | Will be rejected | **Must fix** before submission |
| WARN | High rejection risk | **Should fix** — strongly recommended |
| INFO | Best practice | **Consider fixing** — improves approval odds |

The goal is always: **zero CRITICAL findings = GREENLIT status.**

## Other CLI Commands

```bash
greenlight codescan .                      # Code-only scan
greenlight privacy .                       # Privacy manifest scan
greenlight ipa /path/to/build.ipa          # Binary inspection
greenlight scan --app-id <ID>              # App Store Connect checks (needs auth)
greenlight guidelines search "privacy"     # Search Apple guidelines
```

## About

**Greenlight** is built by [Revyl](https://revyl.com) — the mobile reliability platform.
Catch more than rejections. Catch bugs before your users do.
