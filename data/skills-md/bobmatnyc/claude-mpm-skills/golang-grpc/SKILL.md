---
name: golang-grpc
description: "Production gRPC in Go: protobuf layout, codegen, interceptors, deadlines, error codes, streaming, health checks, TLS, and testing with bufconn"
version: 1.0.0
category: toolchain
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Build production gRPC services in Go with protobuf-first APIs, interceptors, deadlines, status codes, and streaming patterns"
    when_to_use: "When building Go microservices that need typed RPC, streaming, low latency, or strong client/server contracts with protobuf"
    quick_start: "1. Define versioned protos (pkg v1) 2. Generate Go code 3. Implement server + interceptors 4. Enforce deadlines 5. Test with bufconn"
  token_estimate:
    entry: 160
    full: 6500
context_limit: 900
tags:
  - golang
  - grpc
  - protobuf
  - microservices
  - streaming
  - interceptors
  - observability
requires_tools: []
---

# Go gRPC (Production)

## Overview

gRPC provides strongly-typed RPC APIs backed by Protocol Buffers, with first-class streaming support and excellent performance for service-to-service communication. This skill focuses on production defaults: versioned protos, deadlines, error codes, interceptors, health checks, TLS, and testability.

## Quick Start

### 1) Define a versioned protobuf API

✅ **Correct: versioned package**
```proto
// proto/users/v1/users.proto
syntax = "proto3";

package users.v1;
option go_package = "example.com/myapp/gen/users/v1;usersv1";

service UsersService {
  rpc GetUser(GetUserRequest) returns (GetUserResponse);
  rpc ListUsers(ListUsersRequest) returns (stream User);
}

message GetUserRequest { string id = 1; }
message GetUserResponse { User user = 1; }
message ListUsersRequest { int32 page_size = 1; string page_token = 2; }

message User {
  string id = 1;
  string email = 2;
  string display_name = 3;
}
```

❌ **Wrong: unversioned package (hard to evolve)**
```proto
package users;
```

### 2) Generate Go code

Install generators:
```bash
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
```

Generate:
```bash
protoc -I proto \
  --go_out=./gen --go_opt=paths=source_relative \
  --go-grpc_out=./gen --go-grpc_opt=paths=source_relative \
  proto/users/v1/users.proto
```

### 3) Implement server with deadlines and status codes

✅ **Correct: validate + map errors to gRPC codes**
```go
package usersvc

import (
    "context"

    "google.golang.org/grpc/codes"
    "google.golang.org/grpc/status"

    usersv1 "example.com/myapp/gen/users/v1"
)

type Service struct {
    usersv1.UnimplementedUsersServiceServer
    Repo Repo
}

type Repo interface {
    GetUser(ctx context.Context, id string) (User, error)
}

type User struct {
    ID, Email, DisplayName string
}

func (s *Service) GetUser(ctx context.Context, req *usersv1.GetUserRequest) (*usersv1.GetUserResponse, error) {
    if req.GetId() == "" {
        return nil, status.Error(codes.InvalidArgument, "id is required")
    }

    u, err := s.Repo.GetUser(ctx, req.GetId())
    if err != nil {
        if err == ErrNotFound {
            return nil, status.Error(codes.NotFound, "user not found")
        }
        return nil, status.Error(codes.Internal, "internal error")
    }

    return &usersv1.GetUserResponse{
        User: &usersv1.User{
            Id:          u.ID,
            Email:       u.Email,
            DisplayName: u.DisplayName,
        },
    }, nil
}
```

❌ **Wrong: return raw errors (clients lose code semantics)**
```go
return nil, errors.New("user not found")
```

## Core Concepts

### Deadlines and cancellation

Make every call bounded; enforce server-side timeouts for expensive handlers.

✅ **Correct: require deadline**
```go
if _, ok := ctx.Deadline(); !ok {
    return nil, status.Error(codes.InvalidArgument, "deadline required")
}
```

### Metadata

Use metadata for auth/session correlation, not for primary request data.

✅ **Correct: read auth token from metadata**
```go
md, _ := metadata.FromIncomingContext(ctx)
auth := ""
if vals := md.Get("authorization"); len(vals) > 0 {
    auth = vals[0]
}
```

## Interceptors (Middleware)

Use interceptors for cross-cutting concerns: auth, logging, metrics, tracing, request IDs.

✅ **Correct: unary interceptor with request ID**
```go
func unaryRequestID() grpc.UnaryServerInterceptor {
    return func(ctx context.Context, req any, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (any, error) {
        id := uuid.NewString()
        ctx = context.WithValue(ctx, requestIDKey{}, id)
        resp, err := handler(ctx, req)
        return resp, err
    }
}
```

## Streaming patterns

### Server streaming (paginate or stream results)

✅ **Correct: stop on ctx.Done()**
```go
func (s *Service) ListUsers(req *usersv1.ListUsersRequest, stream usersv1.UsersService_ListUsersServer) error {
    users, err := s.Repo.ListUsers(stream.Context(), int(req.GetPageSize()))
    if err != nil {
        return status.Error(codes.Internal, "internal error")
    }

    for _, u := range users {
        select {
        case <-stream.Context().Done():
            return stream.Context().Err()
        default:
        }

        if err := stream.Send(&usersv1.User{
            Id:          u.ID,
            Email:       u.Email,
            DisplayName: u.DisplayName,
        }); err != nil {
            return err
        }
    }
    return nil
}
```

### Unary vs streaming decision

- Use **unary** for single request/response and simple retries.
- Use **server streaming** for large result sets or continuous updates.
- Use **client streaming** for bulk uploads with one final response.
- Use **bidirectional streaming** for interactive protocols.

## Production Hardening

### Health checks and reflection

Add health service; enable reflection only in non-production environments.

✅ **Correct: health + conditional reflection**
```go
hs := health.NewServer()
grpc_health_v1.RegisterHealthServer(s, hs)

if env != "production" {
    reflection.Register(s)
}
```

### Graceful shutdown

Prefer `GracefulStop` with a deadline.

✅ **Correct: graceful stop**
```go
stopped := make(chan struct{})
go func() {
    grpcServer.GracefulStop()
    close(stopped)
}()

select {
case <-stopped:
case <-time.After(10 * time.Second):
    grpcServer.Stop()
}
```

### TLS

Use TLS (or mTLS) in production; avoid insecure credentials outside local dev.

✅ **Correct: server TLS**
```go
creds, err := credentials.NewServerTLSFromFile("server.crt", "server.key")
if err != nil { return err }

grpcServer := grpc.NewServer(grpc.Creds(creds))
```

## Testing (bufconn)

Test gRPC handlers without opening real sockets using `bufconn`.

✅ **Correct: in-memory gRPC test server**
```go
const bufSize = 1024 * 1024

lis := bufconn.Listen(bufSize)
srv := grpc.NewServer()
usersv1.RegisterUsersServiceServer(srv, &Service{Repo: repo})

go func() { _ = srv.Serve(lis) }()

ctx := context.Background()
conn, err := grpc.DialContext(
    ctx,
    "bufnet",
    grpc.WithContextDialer(func(context.Context, string) (net.Conn, error) { return lis.Dial() }),
    grpc.WithTransportCredentials(insecure.NewCredentials()),
)
if err != nil { t.Fatal(err) }
defer conn.Close()

client := usersv1.NewUsersServiceClient(conn)
resp, err := client.GetUser(ctx, &usersv1.GetUserRequest{Id: "1"})
_ = resp
_ = err
```

## Anti-Patterns

- **Ignore deadlines**: unbounded handlers cause tail latency and resource exhaustion.

- **Return string errors**: map domain errors to `codes.*` with `status.Error` or `status.Errorf`.

- **Stream without backpressure**: stop on `ctx.Done()` and handle `Send` errors.

- **Expose reflection in production**: treat reflection as a discovery surface.

## Troubleshooting

### Symptom: clients see `UNKNOWN` errors

Actions:
- Return `status.Error(codes.X, "...")` instead of raw errors.
- Wrap domain errors into typed errors, then map to gRPC codes.

### Symptom: slow/hanging requests

Actions:
- Require deadlines and propagate `ctx` to downstream calls.
- Add server-side timeouts and bounded concurrency in repositories.

### Symptom: flaky streaming

Actions:
- Stop streaming on `ctx.Done()` and handle `stream.Send` errors.
- Avoid buffering entire result sets before sending.

## Resources

- gRPC Go: https://github.com/grpc/grpc-go
- Protobuf Go: https://pkg.go.dev/google.golang.org/protobuf
- gRPC error codes: https://grpc.io/docs/guides/error/
