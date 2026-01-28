---
name: FastAPI
description: FastAPI web framework for building modern APIs with async support
version: "2.1.0"
sasmp_version: "1.3.0"
bonded_agent: 02-web-development
bond_type: PRIMARY_BOND

# Skill Configuration
retry_strategy: exponential_backoff
observability:
  logging: true
  metrics: request_latency
---

# FastAPI Skill

## Overview
Build modern, high-performance APIs with FastAPI, including async endpoints, automatic documentation, and type-safe request handling.

## Topics Covered

### FastAPI Basics
- Application structure
- Route decorators
- Path and query parameters
- Request body handling
- Response models

### Pydantic Integration
- Request validation
- Response serialization
- Custom validators
- Settings management
- Nested models

### Async Programming
- Async endpoint handlers
- Background tasks
- Async database access
- Concurrent requests
- Event handlers

### Security
- OAuth2 implementation
- JWT authentication
- API key authentication
- Dependency injection
- CORS configuration

### Advanced Features
- WebSocket support
- File uploads
- Streaming responses
- Middleware creation
- Testing FastAPI

## Prerequisites
- Python fundamentals
- Async/await basics
- HTTP concepts

## Learning Outcomes
- Build production APIs
- Implement authentication
- Create async endpoints
- Generate API documentation
