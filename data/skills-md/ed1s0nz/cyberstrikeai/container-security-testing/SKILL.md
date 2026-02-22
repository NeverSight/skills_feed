---
name: container-security-testing
description: 容器安全测试的专业技能和方法论
version: 1.0.0
---

# 容器安全测试

## 概述

容器安全测试是确保容器化应用安全性的重要环节。本技能提供容器安全测试的方法、工具和最佳实践，涵盖Docker、Kubernetes等容器技术。

## 测试范围

### 1. 镜像安全

**检查项目：**
- 基础镜像漏洞
- 依赖包漏洞
- 镜像配置
- 敏感信息

### 2. 运行时安全

**检查项目：**
- 容器权限
- 资源限制
- 网络隔离
- 文件系统

### 3. 编排安全

**检查项目：**
- Kubernetes配置
- 服务账户
- RBAC
- 网络策略

## Docker安全测试

### 镜像扫描

**使用Trivy：**
```bash
# 扫描镜像
trivy image nginx:latest

# 扫描本地镜像
trivy image --input nginx.tar

# 只显示高危漏洞
trivy image --severity HIGH,CRITICAL nginx:latest
```

**使用Clair：**
```bash
# 启动Clair
docker run -d --name clair clair:latest

# 扫描镜像
clair-scanner --ip 192.168.1.100 nginx:latest
```

**使用Docker Bench：**
```bash
# 运行Docker安全基准测试
docker run --rm --net host --pid host --userns host --cap-add audit_control \
  -e DOCKER_CONTENT_TRUST=$DOCKER_CONTENT_TRUST \
  -v /etc:/etc:ro \
  -v /usr/bin/containerd:/usr/bin/containerd:ro \
  -v /usr/bin/runc:/usr/bin/runc:ro \
  -v /usr/lib/systemd:/usr/lib/systemd:ro \
  -v /var/lib:/var/lib:ro \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  --label docker_bench_security \
  docker/docker-bench-security
```

### 容器配置检查

**检查Dockerfile：**
```dockerfile
# 安全问题示例
FROM ubuntu:latest  # 使用latest标签
RUN apt-get update && apt-get install -y curl  # 未指定版本
COPY . /app  # 可能包含敏感文件
ENV PASSWORD=secret  # 硬编码密码
USER root  # 使用root用户
```

**安全最佳实践：**
```dockerfile
# 使用特定版本
FROM ubuntu:20.04

# 指定包版本
RUN apt-get update && apt-get install -y curl=7.68.0-1ubuntu2.7

# 使用非root用户
RUN useradd -m appuser
USER appuser

# 最小化镜像
FROM alpine:3.15

# 多阶段构建
FROM golang:1.18 AS builder
WORKDIR /app
COPY . .
RUN go build -o app

FROM alpine:3.15
COPY --from=builder /app/app /app
```

### 运行时检查

**检查容器权限：**
```bash
# 检查特权容器
docker ps --filter "label=privileged=true"

# 检查挂载的主机目录
docker inspect container_name | grep -A 10 Mounts

# 检查容器网络
docker network inspect network_name
```

**检查资源限制：**
```bash
# 检查内存限制
docker stats container_name

# 检查CPU限制
docker inspect container_name | grep -i cpu
```

## Kubernetes安全测试

### 配置检查

**使用kube-bench：**
```bash
# 运行kube-bench
kube-bench run

# 检查特定基准
kube-bench run --targets master,node,etcd
```

**使用kube-hunter：**
```bash
# 运行kube-hunter
kube-hunter --remote target-ip

# 主动模式
kube-hunter --active
```

### Pod安全

**检查Pod安全策略：**
```yaml
# 不安全的Pod配置
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: app
    image: nginx
    securityContext:
      privileged: true  # 特权模式
      runAsUser: 0  # root用户
```

**安全配置：**
```yaml
apiVersion: v1
kind: Pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 2000
  containers:
  - name: app
    image: nginx
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
        - ALL
        add:
        - NET_BIND_SERVICE
```

### RBAC检查

**检查角色权限：**
```bash
# 列出所有角色
kubectl get roles --all-namespaces

# 检查角色绑定
kubectl get rolebindings --all-namespaces

# 检查集群角色
kubectl get clusterroles

# 检查用户权限
kubectl auth can-i --list --as=system:serviceaccount:default:sa-name
```

**常见问题：**
- 过度权限
- 未使用的角色
- 未使用的服务账户

### 网络策略

**检查网络策略：**
```bash
# 列出所有网络策略
kubectl get networkpolicies --all-namespaces

# 检查网络策略配置
kubectl describe networkpolicy policy-name -n namespace
```

**网络策略示例：**
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

## 工具使用

### Falco

**运行时安全监控：**
```bash
# 安装Falco
helm repo add falcosecurity https://falcosecurity.github.io/charts
helm install falco falcosecurity/falco

# 检查规则
falco -r /etc/falco/rules.d/
```

### Aqua Security

```bash
# 扫描镜像
aqua image scan nginx:latest

# 扫描Kubernetes集群
aqua k8s scan
```

### Snyk

```bash
# 扫描Dockerfile
snyk test --docker nginx:latest

# 扫描Kubernetes配置
snyk iac test k8s/
```

## 测试清单

### 镜像安全
- [ ] 扫描基础镜像漏洞
- [ ] 扫描依赖包漏洞
- [ ] 检查Dockerfile配置
- [ ] 检查敏感信息泄露

### 运行时安全
- [ ] 检查容器权限
- [ ] 检查资源限制
- [ ] 检查网络隔离
- [ ] 检查文件系统挂载

### 编排安全
- [ ] 检查Kubernetes配置
- [ ] 检查RBAC配置
- [ ] 检查网络策略
- [ ] 检查Pod安全策略

## 常见安全问题

### 1. 镜像漏洞

**问题：**
- 基础镜像包含漏洞
- 依赖包包含漏洞
- 未及时更新

**修复：**
- 定期扫描镜像
- 及时更新基础镜像
- 使用最小化镜像

### 2. 过度权限

**问题：**
- 容器以root运行
- 特权模式
- 挂载敏感目录

**修复：**
- 使用非root用户
- 禁用特权模式
- 限制文件系统访问

### 3. 配置错误

**问题：**
- 默认配置不安全
- 网络策略缺失
- RBAC配置错误

**修复：**
- 遵循安全最佳实践
- 实施网络策略
- 正确配置RBAC

### 4. 敏感信息泄露

**问题：**
- 镜像包含密钥
- 环境变量暴露
- 配置文件泄露

**修复：**
- 使用密钥管理
- 避免硬编码
- 使用Secret对象

## 最佳实践

### 1. 镜像安全

- 使用官方基础镜像
- 定期更新镜像
- 扫描镜像漏洞
- 最小化镜像大小

### 2. 运行时安全

- 使用非root用户
- 限制容器权限
- 实施资源限制
- 启用安全上下文

### 3. 编排安全

- 配置网络策略
- 实施RBAC
- 使用Pod安全策略
- 启用审计日志

## 注意事项

- 仅在授权环境中进行测试
- 避免对生产环境造成影响
- 注意不同容器平台的差异
- 定期进行安全扫描