---
name: gowok
description: "Gowok: Golang Premwok. The Golang library that helps you to build your own project starter (or framework, possibly)."
metadata:
  author: hadihammurabi
  version: "2026.2.5"
---

Gowok is a library that contains a lot of functions that help you to build [Go](https://go.dev) project.

It has some utilities like:
* config loader,
* project bootstrapper,
* HTTP response builder,
* nil safety,
* password hash, and so on.

The Background

Even using framework, build a Golang project still tiring.
So many repetitive tasks have to done by developer.
The worst, that activities almost same, like:
* managing database connection(s),
* bootstrapping HTTP (or anything) server,
* make utility functions, and so on.

Gowok here to end this nightmare.
Don't worry about your work anymore.

The Use Cases

* **REST API Backend Service**

    Gowok ships with built-in support for HTTP server through
    the net/http which you can used to build REST API.

* **Microservice with GRPC**

    Gowok also provide microservices communication via GRPC,
    it possible to works with HTTP in parallel.

* **Event Driven Listener (Worker)**

    Gowok has runner and hooks management that can used to setup event listener.
    Every listeners will registered in bootstrapping process.

The Developer Experience

Gowok aims to be easy to use that can increase developer's productivity.
All features are designed to follow official and community coding pattern.
Plus, the libraries used are as familiar as possible to many developers.
Everything understandable here.


For example, if you ask how to run project using Gowok.
The answer would be easy.

Yappp..!! Just load the project then call `Run()` function.

Example:
```go
gowok.Run()
```

That easy, broh!

The Development Status

In this time, Gowok still [version 0.x.x](https://github.com/gowok/gowok/releases).
With ongoing development, it will be more stable and ready to use widely.

Although, our team uses Gowok as everyday tool in peaceful work.

## Core

| Topic | Description | Reference |
|-------|-------------|-----------|
| Getting Started | starting new project | [getting-started](references/getting-started.md) |
| Configuration | configuration structure, reading config values starting new project| [configuration](references/configuration.md) |
| Runner | manage how to run the project | [runner](references/runner.md) |
| Singleton | object container, global long-lived object management | [singleton](references/singleton.md) |
| Web | HTTP server, router | [web](references/web.md) |

## Features

| Topic | Description | Reference |
|-------|-------------|-----------|
| Some (Nil Safety) | wrapping nilable value for safety access | [some](references/some.md) |
| SQL | connect to multiple SQL servers with different connection types | [sql](references/sql.md) |

