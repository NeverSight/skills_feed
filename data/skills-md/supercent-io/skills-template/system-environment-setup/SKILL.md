---
name: system-environment-setup
description: Configure development and production environments for consistent and reproducible setups. Use when setting up new projects, Docker environments, or development tooling. Handles Docker Compose, .env configuration, dev containers, and infrastructure as code.
tags: [environment-setup, Docker-Compose, dev-environment, IaC, configuration]
platforms: [Claude, ChatGPT, Gemini]
---

# System & Environment Setup


## When to use this skill

- **신규 프로젝트**: 초기 환경 설정
- **팀 온보딩**: 새 개발자 환경 통일
- **다중 서비스**: 마이크로서비스 로컬 실행
- **프로덕션 재현**: 로컬에서 프로덕션 환경 테스트

## Instructions

### Step 1: Docker Compose 설정

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  # Web Application
  web:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://postgres:password@db:5432/myapp
      - REDIS_URL=redis://redis:6379
    volumes:
      - .:/app
      - /app/node_modules
    depends_on:
      - db
      - redis
    command: npm run dev

  # PostgreSQL Database
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: myapp
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql

  # Redis Cache
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  # Nginx (Reverse Proxy)
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - web

volumes:
  postgres_data:
  redis_data:
```

**사용**:
```bash
# 모든 서비스 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f web

# 특정 서비스만 재시작
docker-compose restart web

# 중지 및 제거
docker-compose down

# 볼륨까지 제거
docker-compose down -v
```

### Step 2: 환경변수 관리

**.env.example**:
```bash
# Application
NODE_ENV=development
PORT=3000
APP_URL=http://localhost:3000

# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/myapp
DATABASE_POOL_SIZE=10

# Redis
REDIS_URL=redis://localhost:6379

# JWT
ACCESS_TOKEN_SECRET=change-me-in-production-min-32-characters
REFRESH_TOKEN_SECRET=change-me-in-production-min-32-characters
TOKEN_EXPIRY=15m

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# External APIs
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_PUBLISHABLE_KEY=pk_test_xxx
AWS_ACCESS_KEY_ID=AKIAXXXXXXX
AWS_SECRET_ACCESS_KEY=xxxxxxxx
AWS_REGION=us-east-1
```

**.env** (로컬에서만, gitignore에 추가):
```bash
# .gitignore
.env
.env.local
.env.*.local
```

**환경변수 로드** (Node.js):
```typescript
import dotenv from 'dotenv';
import path from 'path';

// Load .env file
dotenv.config();

// Type-safe environment variables
interface Env {
  NODE_ENV: 'development' | 'production' | 'test';
  PORT: number;
  DATABASE_URL: string;
  REDIS_URL: string;
  ACCESS_TOKEN_SECRET: string;
}

function loadEnv(): Env {
  const required = ['DATABASE_URL', 'ACCESS_TOKEN_SECRET', 'REDIS_URL'];

  for (const key of required) {
    if (!process.env[key]) {
      throw new Error(`Missing required environment variable: ${key}`);
    }
  }

  return {
    NODE_ENV: (process.env.NODE_ENV as any) || 'development',
    PORT: parseInt(process.env.PORT || '3000'),
    DATABASE_URL: process.env.DATABASE_URL!,
    REDIS_URL: process.env.REDIS_URL!,
    ACCESS_TOKEN_SECRET: process.env.ACCESS_TOKEN_SECRET!
  };
}

export const env = loadEnv();
```

### Step 3: Dev Container (VS Code)

**.devcontainer/devcontainer.json**:
```json
{
  "name": "Node.js & PostgreSQL",
  "dockerComposeFile": "../docker-compose.yml",
  "service": "web",
  "workspaceFolder": "/app",

  "customizations": {
    "vscode": {
      "extensions": [
        "dbaeumer.vscode-eslint",
        "esbenp.prettier-vscode",
        "ms-azuretools.vscode-docker",
        "prisma.prisma"
      ],
      "settings": {
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "eslint.validate": ["javascript", "typescript"]
      }
    }
  },

  "forwardPorts": [3000, 5432, 6379],

  "postCreateCommand": "npm install",

  "remoteUser": "node"
}
```

### Step 4: Makefile (편의 명령어)

**Makefile**:
```makefile
.PHONY: help install dev build test clean docker-up docker-down migrate seed

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	npm install

dev: ## Start development server
	npm run dev

build: ## Build for production
	npm run build

test: ## Run tests
	npm test

test-watch: ## Run tests in watch mode
	npm test -- --watch

lint: ## Run linter
	npm run lint

lint-fix: ## Fix linting issues
	npm run lint -- --fix

docker-up: ## Start Docker services
	docker-compose up -d

docker-down: ## Stop Docker services
	docker-compose down

docker-logs: ## View Docker logs
	docker-compose logs -f

migrate: ## Run database migrations
	npm run migrate

migrate-create: ## Create new migration
	@read -p "Migration name: " name; \
	npm run migrate:create -- $$name

seed: ## Seed database
	npm run seed

clean: ## Clean build artifacts
	rm -rf dist node_modules coverage

reset: clean install ## Reset project (clean + install)
```

**사용**:
```bash
make help         # 명령어 목록
make install      # 의존성 설치
make dev          # 개발 서버 시작
make docker-up    # Docker 서비스 시작
```

### Step 5: Infrastructure as Code (Terraform)

**main.tf** (AWS 예시):
```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket = "myapp-terraform-state"
    key    = "production/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name        = "${var.project_name}-vpc"
    Environment = var.environment
  }
}

# RDS (PostgreSQL)
resource "aws_db_instance" "postgres" {
  identifier           = "${var.project_name}-db"
  engine               = "postgres"
  engine_version       = "15.4"
  instance_class       = "db.t3.micro"
  allocated_storage    = 20
  storage_encrypted    = true

  db_name  = var.db_name
  username = var.db_username
  password = var.db_password

  vpc_security_group_ids = [aws_security_group.db.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name

  backup_retention_period = 7
  skip_final_snapshot     = false
  final_snapshot_identifier = "${var.project_name}-final-snapshot"

  tags = {
    Name        = "${var.project_name}-db"
    Environment = var.environment
  }
}

# ECS (Container Service)
resource "aws_ecs_cluster" "main" {
  name = "${var.project_name}-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

# Load Balancer
resource "aws_lb" "main" {
  name               = "${var.project_name}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = aws_subnet.public[*].id
}
```

**variables.tf**:
```hcl
variable "project_name" {
  description = "Project name"
  type        = string
  default     = "myapp"
}

variable "environment" {
  description = "Environment (dev, staging, production)"
  type        = string
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "db_username" {
  description = "Database username"
  type        = string
  sensitive   = true
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}
```

## Output format

### 프로젝트 구조

```
project/
├── .devcontainer/
│   └── devcontainer.json
├── docker-compose.yml
├── Dockerfile
├── Makefile
├── .env.example
├── .gitignore
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
└── README.md
```

## Constraints

### 필수 규칙 (MUST)

1. **.env.example 제공**: 필요한 환경변수 목록
2. **.gitignore**: .env 파일 절대 커밋하지 않음
3. **README.md**: 설치 및 실행 방법 문서화

### 금지 사항 (MUST NOT)

1. **Secrets 커밋 금지**: .env, credentials 파일 절대 커밋하지 않음
2. **하드코딩 금지**: 모든 설정은 환경변수로

## Best practices

1. **Docker Compose**: 로컬 개발은 Docker Compose
2. **Volume Mount**: 코드 변경 즉시 반영
3. **Health Checks**: 서비스 준비 상태 확인

## References

- [Docker Compose](https://docs.docker.com/compose/)
- [Dev Containers](https://containers.dev/)
- [Terraform](https://www.terraform.io/)

## Metadata

### 버전
- **현재 버전**: 1.0.0
- **최종 업데이트**: 2025-01-01
- **호환 플랫폼**: Claude, ChatGPT, Gemini

### 관련 스킬
- [deployment](../deployment/SKILL.md)
- [environment-setup](../../utilities/environment-setup/SKILL.md)

### 태그
`#environment-setup` `#Docker-Compose` `#dev-environment` `#IaC` `#Terraform` `#infrastructure`

## Examples

### Example 1: Basic usage
<!-- Add example content here -->

### Example 2: Advanced usage
<!-- Add advanced example content here -->
