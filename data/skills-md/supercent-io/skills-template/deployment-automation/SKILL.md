---
name: deployment-automation
description: Automate application deployment to cloud platforms and servers. Use when setting up CI/CD pipelines, deploying to Docker/Kubernetes, or configuring cloud infrastructure. Handles GitHub Actions, Docker, Kubernetes, AWS, Vercel, and deployment best practices.
tags: [deployment, CI/CD, Docker, Kubernetes, AWS, GitHub-Actions, automation]
platforms: [Claude, ChatGPT, Gemini]
---

# Deployment Automation


## When to use this skill

- **신규 프로젝트**: 처음부터 자동 배포 설정
- **수동 배포 개선**: 반복적인 수동 작업 자동화
- **멀티 환경**: dev, staging, production 환경 분리
- **스케일링**: 트래픽 증가 대비 Kubernetes 도입

## Instructions

### Step 1: Docker 컨테이너화

애플리케이션을 Docker 이미지로 패키징합니다.

**Dockerfile** (Node.js 앱):
```dockerfile
# Multi-stage build for smaller image size
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm ci --only=production

# Copy source code
COPY . .

# Build application (if needed)
RUN npm run build

# Production stage
FROM node:18-alpine

WORKDIR /app

# Copy only necessary files from builder
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./

# Create non-root user for security
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001
USER nodejs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node healthcheck.js

# Start application
CMD ["node", "dist/index.js"]
```

**.dockerignore**:
```
node_modules
npm-debug.log
.git
.env
.env.local
dist
build
coverage
.DS_Store
```

**빌드 및 실행**:
```bash
# Build image
docker build -t myapp:latest .

# Run container
docker run -d -p 3000:3000 --name myapp-container myapp:latest

# Check logs
docker logs myapp-container

# Stop and remove
docker stop myapp-container
docker rm myapp-container
```

### Step 2: GitHub Actions CI/CD

코드 푸시 시 자동으로 테스트 및 배포합니다.

**.github/workflows/deploy.yml**:
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: '18'
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linter
        run: npm run lint

      - name: Run tests
        run: npm test -- --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/coverage-final.json

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=sha,prefix={{branch}}-
            type=semver,pattern={{version}}
            latest

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment: production

    steps:
      - name: Deploy to production
        uses: appleboy/ssh-action@v1.0.0
        with:
          host: ${{ secrets.PROD_HOST }}
          username: ${{ secrets.PROD_USER }}
          key: ${{ secrets.PROD_SSH_KEY }}
          script: |
            cd /app
            docker pull ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
            docker-compose up -d --no-deps --build web
            docker image prune -f
```

### Step 3: Kubernetes 배포

확장 가능한 컨테이너 오케스트레이션을 구현합니다.

**k8s/deployment.yaml**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: production
  labels:
    app: myapp
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: ghcr.io/username/myapp:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 3000
        env:
        - name: NODE_ENV
          value: "production"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: myapp-secrets
              key: database-url
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
  namespace: production
spec:
  selector:
    app: myapp
  ports:
  - protocol: TCP
    port: 80
    targetPort: 3000
  type: LoadBalancer

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

**배포 스크립트** (deploy.sh):
```bash
#!/bin/bash
set -e

# Variables
NAMESPACE="production"
IMAGE_TAG="${1:-latest}"

echo "Deploying myapp:${IMAGE_TAG} to ${NAMESPACE}..."

# Apply Kubernetes manifests
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Update image
kubectl set image deployment/myapp myapp=ghcr.io/username/myapp:${IMAGE_TAG} -n ${NAMESPACE}

# Wait for rollout
kubectl rollout status deployment/myapp -n ${NAMESPACE} --timeout=5m

# Verify
kubectl get pods -n ${NAMESPACE} -l app=myapp

echo "Deployment completed successfully!"
```

### Step 4: Vercel/Netlify (프론트엔드)

정적 사이트 및 Next.js 앱을 간단히 배포합니다.

**vercel.json**:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/next"
    }
  ],
  "env": {
    "DATABASE_URL": "@database-url",
    "API_KEY": "@api-key"
  },
  "regions": ["sin1", "icn1"],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        }
      ]
    }
  ],
  "redirects": [
    {
      "source": "/old-path",
      "destination": "/new-path",
      "permanent": true
    }
  ]
}
```

**CLI 배포**:
```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy to preview
vercel

# Deploy to production
vercel --prod

# Set environment variable
vercel env add DATABASE_URL
```

### Step 5: 무중단 배포 전략

서비스 중단 없이 새 버전을 배포합니다.

**Blue-Green 배포** (docker-compose):
```yaml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - app-blue
      - app-green

  app-blue:
    image: myapp:blue
    environment:
      - NODE_ENV=production
      - COLOR=blue

  app-green:
    image: myapp:green
    environment:
      - NODE_ENV=production
      - COLOR=green
```

**switch.sh** (Blue/Green 전환):
```bash
#!/bin/bash

CURRENT_COLOR=$(cat current_color.txt)
NEW_COLOR=$([[ "$CURRENT_COLOR" == "blue" ]] && echo "green" || echo "blue")

# Deploy new version to inactive environment
docker-compose up -d app-${NEW_COLOR}

# Wait for health check
sleep 10

# Health check
if curl -f http://localhost:8080/health; then
  # Update nginx to point to new environment
  sed -i "s/${CURRENT_COLOR}/${NEW_COLOR}/g" nginx.conf
  docker-compose exec nginx nginx -s reload

  # Update current color
  echo ${NEW_COLOR} > current_color.txt

  # Stop old environment after 5 minutes (rollback window)
  sleep 300
  docker-compose stop app-${CURRENT_COLOR}

  echo "Deployment successful! Switched to ${NEW_COLOR}"
else
  echo "Health check failed! Keeping ${CURRENT_COLOR}"
  docker-compose stop app-${NEW_COLOR}
  exit 1
fi
```

## Output format

### 배포 체크리스트

```markdown
## Deployment Checklist

### Pre-Deployment
- [ ] All tests passing (unit, integration, E2E)
- [ ] Code review approved
- [ ] Environment variables configured
- [ ] Database migrations ready
- [ ] Rollback plan documented

### Deployment
- [ ] Docker image built and tagged
- [ ] Image pushed to container registry
- [ ] Kubernetes manifests applied
- [ ] Rolling update started
- [ ] Pods healthy and ready

### Post-Deployment
- [ ] Health check endpoint responding
- [ ] Metrics/logs monitoring active
- [ ] Performance baseline established
- [ ] Old pods terminated (after grace period)
- [ ] Deployment documented in changelog
```

## Constraints

### 필수 규칙 (MUST)

1. **Health Checks**: 모든 서비스에 health check 엔드포인트
   ```typescript
   app.get('/health', (req, res) => {
     res.status(200).json({ status: 'ok' });
   });
   ```

2. **Graceful Shutdown**: SIGTERM 신호 처리
   ```javascript
   process.on('SIGTERM', async () => {
     console.log('SIGTERM received, shutting down gracefully');
     await server.close();
     await db.close();
     process.exit(0);
   });
   ```

3. **환경변수 분리**: 하드코딩 금지, .env 사용

### 금지 사항 (MUST NOT)

1. **Secrets 커밋 금지**: API 키, 비밀번호를 Git에 절대 커밋하지 않음
2. **프로덕션에서 디버그 모드**: `NODE_ENV=production` 필수
3. **latest 태그만 사용**: 버전 태그 사용 (v1.0.0, sha-abc123)

## Best practices

1. **Multi-stage Docker builds**: 이미지 크기 최소화
2. **Immutable infrastructure**: 서버 수정 대신 새로 배포
3. **Blue-Green deployment**: 무중단 배포 및 쉬운 롤백
4. **Monitoring 필수**: Prometheus, Grafana, Datadog

## References

- [Docker Docs](https://docs.docker.com/)
- [Kubernetes Docs](https://kubernetes.io/docs/)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Vercel](https://vercel.com/docs)
- [12 Factor App](https://12factor.net/)

## Metadata

### 버전
- **현재 버전**: 1.0.0
- **최종 업데이트**: 2025-01-01
- **호환 플랫폼**: Claude, ChatGPT, Gemini

### 관련 스킬
- [monitoring](../monitoring/SKILL.md): 배포 후 모니터링
- [security](../security/SKILL.md): 배포 보안

### 태그
`#deployment` `#CI/CD` `#Docker` `#Kubernetes` `#automation` `#infrastructure`

## Examples

### Example 1: Basic usage
<!-- Add example content here -->

### Example 2: Advanced usage
<!-- Add advanced example content here -->
