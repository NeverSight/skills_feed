---
name: effect-cli
description: Building CLI applications with @effect/cli. Use when defining commands, options, args, or prompts for a CLI tool using effect.
---

## Structure

```
Command.run(command, { name, version })
├── Command (parent)
│   ├── Options (named flags: --verbose, --depth 5)
│   ├── Args (positional: <repo> <path>)
│   └── Command.withSubcommands([...])
│       ├── Command (child — can yield* parent for its config)
│       └── Command (child)
```

## Minimal App

```ts
import { Command, Options, Args } from "@effect/cli"
import { NodeContext, NodeRuntime } from "@effect/platform-node"
import { Console, Effect } from "effect"

const greet = Command.make(
  "greet",
  {
    name: Args.text({ name: "name" }),
    loud: Options.boolean("loud").pipe(Options.withAlias("l"))
  },
  ({ name, loud }) =>
    Console.log(loud ? name.toUpperCase() + "!" : `Hello, ${name}!`)
)

const cli = Command.run(greet, { name: "Greeter", version: "1.0.0" })

Effect.suspend(() => cli(process.argv)).pipe(
  Effect.provide(NodeContext.layer),
  NodeRuntime.runMain
)
```

## Commands

```ts
// No config
const root = Command.make("app")

// With config (record of Options + Args, arbitrarily nested)
const cmd = Command.make("cmd", {
  verbose: Options.boolean("verbose"),
  file: Args.text({ name: "file" })
}, ({ verbose, file }) => Console.log(file))

// Attach handler later
const cmd2 = Command.make("cmd", { n: Args.integer({ name: "n" }) }).pipe(
  Command.withHandler(({ n }) => Console.log(n))
)

// Description
const cmd3 = cmd.pipe(Command.withDescription("Does something useful"))
```

### Subcommands

```ts
const git = Command.make("git", {
  verbose: Options.boolean("verbose").pipe(Options.withAlias("v"))
})

const clone = Command.make("clone", { repo: Args.text({ name: "repo" }) },
  ({ repo }) =>
    Effect.gen(function* () {
      const { verbose } = yield* git  // access parent's parsed config
      yield* Console.log(`Cloning ${repo}, verbose=${verbose}`)
    })
)

const add = Command.make("add", { path: Args.text({ name: "path" }) },
  ({ path }) => Console.log(`Adding ${path}`)
)

const command = git.pipe(Command.withSubcommands([clone, add]))
```

Key pattern: subcommand handlers `yield* parentCommand` to access the parent's parsed config. This works because `Command` extends `Effect`.

### Providing Services

```ts
cmd.pipe(Command.provide(MyService.layer))
cmd.pipe(Command.provide((config) => MyService.layer(config.path)))  // config-dependent
cmd.pipe(Command.provideEffect(MyService, (_config) => Effect.succeed(impl)))
cmd.pipe(Command.provideSync(MyService, impl))
cmd.pipe(Command.provideEffectDiscard((_config) => Effect.log("Starting...")))

// Transform handler
cmd.pipe(Command.transformHandler((effect, config) =>
  Effect.provideService(effect, MyService, impl)
))
```

## Options (Named Flags)

For detailed options reference see [effect-cli-options.md](./effect-cli-options.md).

| Constructor | CLI syntax | Type |
|---|---|---|
| `Options.boolean("verbose")` | `--verbose` | `boolean` |
| `Options.text("name")` | `--name foo` | `string` |
| `Options.integer("depth")` | `--depth 5` | `number` |
| `Options.float("amount")` | `--amount 3.14` | `number` |
| `Options.date("when")` | `--when 2024-01-01` | `Date` |
| `Options.redacted("token")` | `--token abc` | `Redacted` |
| `Options.choice("fmt", ["json", "csv"])` | `--fmt json` | `"json" \| "csv"` |
| `Options.file("config")` | `--config ./f.json` | `string` |
| `Options.directory("out")` | `--out ./dist` | `string` |
| `Options.fileText("input")` | `--input ./f.txt` | `[path, string]` |
| `Options.fileSchema("cfg", S)` | `--cfg ./f.json` | `Schema.Type<S>` |
| `Options.keyValueMap("c")` | `-c k=v -c k2=v2` | `HashMap<string,string>` |

### Common Combinators

```ts
Options.text("name").pipe(
  Options.withAlias("n"),              // -n shorthand
  Options.withDescription("Your name"),
  Options.optional,                    // Option<string>
  // or: Options.withDefault("world"), // string with default
)

// Repetition
Options.text("tag").pipe(Options.repeated)          // Array<string>
Options.text("tag").pipe(Options.atLeast(1))        // NonEmptyArray<string>

// Schema validation
Options.text("balance").pipe(Options.withSchema(Schema.BigDecimal))

// Fallback to env var (via Effect Config)
Options.integer("port").pipe(Options.withFallbackConfig(Config.integer("PORT")))

// Fallback to interactive prompt
Options.text("name").pipe(
  Options.withFallbackPrompt(Prompt.text({ message: "Enter name:" }))
)
```

## Args (Positional Arguments)

For detailed args reference see [effect-cli-args.md](./effect-cli-args.md).

| Constructor | Type |
|---|---|
| `Args.text({ name: "repo" })` | `string` |
| `Args.integer({ name: "n" })` | `number` |
| `Args.float({ name: "x" })` | `number` |
| `Args.boolean()` | `boolean` |
| `Args.date()` | `Date` |
| `Args.file()` | `string` |
| `Args.file({ exists: "yes" })` | `string` (must exist) |
| `Args.directory()` | `string` |
| `Args.fileText()` | `[path, string]` |
| `Args.fileSchema(MySchema)` | `Schema.Type<S>` |

### Common Combinators

```ts
Args.text({ name: "dir" }).pipe(
  Args.optional,                    // Option<string>
  // or: Args.withDefault("/"),     // string with default
  // or: Args.repeated,             // Array<string>
  // or: Args.atLeast(1),           // NonEmptyArray<string>
)

Args.text({ name: "n" }).pipe(Args.withSchema(Schema.NumberFromString))
Args.text({ name: "r" }).pipe(Args.withFallbackConfig(Config.string("REPO")))
Args.text({ name: "r" }).pipe(Args.withDescription("The repository URL"))
```

## Prompts

For detailed prompt reference see [effect-cli-prompt.md](./effect-cli-prompt.md).

```ts
import { Prompt } from "@effect/cli"

Prompt.text({ message: "Name:", default: "Alice" })             // string
Prompt.password({ message: "Password:" })                       // Redacted
Prompt.integer({ message: "Age:", min: 0, max: 150 })          // number
Prompt.confirm({ message: "Sure?" })                            // boolean
Prompt.toggle({ message: "Enable?", active: "on", inactive: "off" }) // boolean

Prompt.select({
  message: "Pick env:",
  choices: [
    { title: "Production", value: "prod" },
    { title: "Staging", value: "staging" },
    { title: "Dev", value: "dev" }
  ]
})                                                               // string

Prompt.list({ message: "Tags:", delimiter: "," })               // Array<string>

// Combine prompts
Prompt.all({ name: namePrompt, age: agePrompt })
```

### Prompt-Based Commands

```ts
const favorites = Command.prompt(
  "favorites",
  Prompt.all([
    Prompt.select({ message: "Color?", choices: [...] }),
    Prompt.confirm({ message: "Continue?" })
  ]),
  ([color, confirmed]) => Console.log(`Color: ${color}`)
)
```

## Running

```ts
const cli = Command.run(command, {
  name: "My App",
  version: "1.0.0",
  // summary: Span.text("Short summary"),
  // footer: HelpDoc.p("Footer text"),
})

// cli: (args: ReadonlyArray<string>) => Effect<void, ...>

Effect.suspend(() => cli(process.argv)).pipe(
  Effect.provide(NodeContext.layer),
  NodeRuntime.runMain
)
```

`process.argv` is automatically stripped of the node executable and script path.

## Built-In Options (Automatic)

Every CLI app gets these for free:

| Flag | Effect |
|---|---|
| `-h`, `--help` | Print auto-generated help |
| `--version` | Print version |
| `--wizard` | Interactive wizard for all options/args |
| `--completions bash\|fish\|zsh` | Shell completion scripts |
| `--log-level debug\|info\|warn\|error` | Set log level |

## Config File Support

```ts
import { ConfigFile } from "@effect/cli"

Effect.suspend(() => cli(process.argv)).pipe(
  Effect.provide(
    Layer.mergeAll(
      NodeContext.layer,
      ConfigFile.layer("myapp")  // reads myapp.json, myapp.yaml, etc.
    )
  ),
  NodeRuntime.runMain
)
```

Options using `withFallbackConfig` will read from the config file.

## Config Precedence

CLI args > `withFallbackConfig` (env/config file) > `withFallbackPrompt` (interactive) > `withDefault` (static)

## Additional Resources

[Detailed Options reference](./effect-cli-options.md)
[Detailed Args reference](./effect-cli-args.md)
[Detailed Prompt reference](./effect-cli-prompt.md)
