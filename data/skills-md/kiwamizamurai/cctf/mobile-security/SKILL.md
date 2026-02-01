---
name: mobile-security
description: Reverses and exploits mobile applications. Use when working with Android APK files, iOS IPA files, mobile app reversing, Frida hooking, or app security analysis challenges.
allowed-tools: Bash, Read, Write, Grep, Glob
---

# Mobile Security Skill

## Quick Workflow

```
Progress:
- [ ] Extract APK/IPA
- [ ] Decompile (jadx for Android)
- [ ] Search for hardcoded secrets
- [ ] Check native libraries
- [ ] Dynamic analysis with Frida if needed
- [ ] Extract flag
```

## Quick Analysis Pipeline

```bash
# Android APK
file app.apk
apktool d app.apk -o extracted/
jadx app.apk -d output/
grep -r "flag\|secret" output/

# iOS IPA
unzip app.ipa -d extracted/
strings Payload/App.app/App | grep -i flag
```

## Reference Files

| Topic | Reference |
|-------|-----------|
| Android APK Analysis | [reference/android.md](reference/android.md) |
| iOS IPA Analysis | [reference/ios.md](reference/ios.md) |
| Frida & objection | [reference/frida.md](reference/frida.md) |

## Tools Summary

| Tool | Purpose | Install |
|------|---------|---------|
| jadx | Java decompiler | github.com/skylot/jadx |
| apktool | APK decode/rebuild | apktool.org |
| Frida | Dynamic instrumentation | `pip install frida-tools` |
| objection | Runtime exploration | `pip install objection` |
| Ghidra | Native lib reversing | ghidra-sre.org |
| dex2jar | DEX to JAR | github.com/pxb1988/dex2jar |

## CTF Quick Patterns

```bash
# Flag in resources
grep -r "flag\|ctf\|secret" extracted/res/

# Flag in native library
strings extracted/lib/*/*.so | grep -i flag

# Hardcoded secrets
grep -r "api_key\|secret\|password" output/
```
