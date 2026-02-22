---
name: mobile-app-security-testing
description: 移动应用安全测试的专业技能和方法论
version: 1.0.0
---

# 移动应用安全测试

## 概述

移动应用安全测试是确保移动应用安全性的重要环节。本技能提供移动应用安全测试的方法、工具和最佳实践，涵盖Android和iOS平台。

## 测试范围

### 1. 应用安全

**检查项目：**
- 代码混淆
- 反编译防护
- 调试防护
- 证书绑定

### 2. 数据安全

**检查项目：**
- 数据加密
- 密钥管理
- 敏感数据存储
- 数据传输

### 3. 认证授权

**检查项目：**
- 认证机制
- Token管理
- 生物识别
- 会话管理

### 4. 通信安全

**检查项目：**
- TLS/SSL配置
- 证书验证
- API安全
- 中间人攻击防护

## Android安全测试

### 静态分析

**使用APKTool：**
```bash
# 反编译APK
apktool d app.apk

# 查看AndroidManifest.xml
cat app/AndroidManifest.xml

# 查看Smali代码
find app/smali -name "*.smali"
```

**使用Jadx：**
```bash
# 反编译APK
jadx -d output app.apk

# 查看Java源码
find output -name "*.java"
```

**使用MobSF：**
```bash
# 启动MobSF
docker run -it -p 8000:8000 opensecurity/mobsf

# 上传APK进行分析
# 访问 http://localhost:8000
```

### 动态分析

**使用Frida：**
```javascript
// Hook函数
Java.perform(function() {
    var MainActivity = Java.use("com.example.MainActivity");
    MainActivity.onCreate.implementation = function(savedInstanceState) {
        console.log("[*] onCreate called");
        this.onCreate(savedInstanceState);
    };
});
```

**使用Objection：**
```bash
# 启动Objection
objection -g com.example.app explore

# Hook函数
android hooking watch class_method com.example.MainActivity.onCreate
```

**使用Burp Suite：**
```bash
# 配置代理
# Android设置代理指向Burp Suite
# 安装Burp证书
```

### 常见漏洞

**硬编码密钥：**
```java
// 不安全的代码
String apiKey = "1234567890abcdef";
String password = "admin123";
```

**不安全的存储：**
```java
// SharedPreferences存储敏感数据
SharedPreferences prefs = getSharedPreferences("data", MODE_WORLD_READABLE);
prefs.edit().putString("password", password).apply();
```

**证书验证绕过：**
```java
// 不验证证书
TrustManager[] trustAllCerts = new TrustManager[] {
    new X509TrustManager() {
        public X509Certificate[] getAcceptedIssuers() { return null; }
        public void checkClientTrusted(X509Certificate[] certs, String authType) { }
        public void checkServerTrusted(X509Certificate[] certs, String authType) { }
    }
};
```

## iOS安全测试

### 静态分析

**使用class-dump：**
```bash
# 导出头文件
class-dump app.ipa

# 查看头文件
find app -name "*.h"
```

**使用Hopper：**
```bash
# 使用Hopper反汇编
# 打开app二进制文件
# 分析汇编代码
```

**使用otool：**
```bash
# 查看Mach-O信息
otool -L app

# 查看字符串
strings app | grep -i "password\|key\|secret"
```

### 动态分析

**使用Frida：**
```javascript
// Hook Objective-C方法
var className = ObjC.classes.ViewController;
var method = className['- login:password:'];
Interceptor.attach(method.implementation, {
    onEnter: function(args) {
        console.log("[*] Login called");
        console.log("Username: " + ObjC.Object(args[2]).toString());
        console.log("Password: " + ObjC.Object(args[3]).toString());
    }
});
```

**使用Cycript：**
```bash
# 附加到进程
cycript -p app

# 执行命令
[UIApplication sharedApplication]
```

### 常见漏洞

**硬编码密钥：**
```objective-c
// 不安全的代码
NSString *apiKey = @"1234567890abcdef";
NSString *password = @"admin123";
```

**不安全的存储：**
```objective-c
// Keychain存储不当
NSUserDefaults *defaults = [NSUserDefaults standardUserDefaults];
[defaults setObject:password forKey:@"password"];
```

**证书验证绕过：**
```objective-c
// 不验证证书
- (void)connection:(NSURLConnection *)connection 
didReceiveAuthenticationChallenge:(NSURLAuthenticationChallenge *)challenge {
    [challenge.sender useCredential:[NSURLCredential credentialForTrust:challenge.protectionSpace.serverTrust] 
          forAuthenticationChallenge:challenge];
}
```

## 工具使用

### MobSF

```bash
# 启动MobSF
docker run -it -p 8000:8000 opensecurity/mobsf

# 上传应用进行分析
# 支持Android和iOS
```

### Frida

```bash
# 安装Frida
pip install frida-tools

# 运行脚本
frida -U -f com.example.app -l script.js
```

### Objection

```bash
# 安装Objection
pip install objection

# 启动Objection
objection -g com.example.app explore
```

### Burp Suite

**配置代理：**
1. 配置Burp Suite监听器
2. 移动设备设置代理
3. 安装Burp证书
4. 拦截和分析流量

## 测试清单

### 应用安全
- [ ] 代码混淆检查
- [ ] 反编译防护
- [ ] 调试防护
- [ ] 证书绑定

### 数据安全
- [ ] 数据加密检查
- [ ] 密钥管理
- [ ] 敏感数据存储
- [ ] 数据传输安全

### 认证授权
- [ ] 认证机制测试
- [ ] Token管理
- [ ] 会话管理
- [ ] 生物识别

### 通信安全
- [ ] TLS/SSL配置
- [ ] 证书验证
- [ ] API安全测试
- [ ] 中间人攻击防护

## 常见安全问题

### 1. 硬编码密钥

**问题：**
- API密钥硬编码
- 密码硬编码
- 加密密钥硬编码

**修复：**
- 使用密钥管理服务
- 使用环境变量
- 使用安全存储

### 2. 不安全的存储

**问题：**
- 明文存储敏感数据
- 使用不安全的存储方式
- 数据未加密

**修复：**
- 使用加密存储
- 使用Keychain/Keystore
- 实施数据加密

### 3. 证书验证绕过

**问题：**
- 不验证SSL证书
- 接受自签名证书
- 证书固定未实施

**修复：**
- 实施证书固定
- 验证证书链
- 使用系统证书存储

### 4. 调试信息泄露

**问题：**
- 日志包含敏感信息
- 错误信息泄露
- 调试模式未禁用

**修复：**
- 移除调试代码
- 限制日志输出
- 生产环境禁用调试

## 最佳实践

### 1. 代码安全

- 实施代码混淆
- 禁用调试功能
- 实施反调试保护
- 使用证书绑定

### 2. 数据安全

- 加密敏感数据
- 使用安全存储
- 实施密钥管理
- 限制数据访问

### 3. 通信安全

- 使用TLS/SSL
- 实施证书固定
- 验证服务器证书
- 使用安全API

### 4. 认证安全

- 实施强认证
- 安全Token管理
- 实施会话管理
- 使用生物识别

## 注意事项

- 仅在授权环境中进行测试
- 遵守法律法规
- 注意不同平台的差异
- 保护用户隐私