---
name: zhin-context-services
description: Details Zhin context services (config, database, cron, permission) and how to register or consume them in plugins.
license: MIT
metadata:
  author: zhinjs
  version: "1.0"
  framework: zhin
---

# Zhin Context & Services Skill

Use this skill when developers need to interact with built-in contexts or provide custom services via `defineContext`.

## Accessing Built-in Services

```ts
import { usePlugin } from '@zhin.js/core'

const plugin = usePlugin()

// Inject built-in contexts
const config = plugin.inject('config')
const permissions = plugin.inject('permission')
const cronService = plugin.inject('cron')
```

Use `plugin.contextIsReady('service')` to check if a context is available before using it.

## Config Service

Load or read config files via `ConfigService`:

```ts
const configService = plugin.inject('config')
const config = configService?.get('zhin.config.yaml', {
  debug: false,
  plugins: []
})
```

Notes:
- Supported formats: `.json`, `.yaml`, `.yml`
- Config values can reference environment variables using `${ENV_NAME:default}`

## Cron Service

Register scheduled tasks using the `Cron` class and `addCron`:

```ts
import { Cron } from '@zhin.js/core'

plugin.addCron(new Cron('0 * * * *', async () => {
  plugin.logger.info('Hourly task')
}))
```

Cron entries are auto-started and stopped when the plugin is disposed.

## Permission Service

The permission service provides checks in `MessageCommand.permit(...)`. You can also extend it by pushing a new check function:

```ts
const permission = plugin.inject('permission')
permission?.add({
  name: /^role\(.+\)$/,
  check: async (name, message) => {
    // custom role validation
    return false
  }
})
```

## Database Service

If the database context is enabled, use it via `plugin.inject('database')`:

```ts
const database = plugin.inject('database')
const users = await database?.select('User')
```

To define new models, call `plugin.defineModel(name, definition)` if the database service is active.

## Defining Custom Contexts

```ts
import { defineContext, usePlugin } from '@zhin.js/core'

const plugin = usePlugin()

plugin.provide(defineContext({
  name: 'metrics',
  description: 'Metrics service',
  mounted: async () => ({
    counter: 0
  }),
  dispose: (value) => {
    // cleanup
  },
  extensions: {
    increment() {
      this.counter += 1
    }
  }
}))
```

Custom contexts can also extend `Plugin.Extensions` so you can call new helper methods from plugins.
