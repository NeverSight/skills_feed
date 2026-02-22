---
name: bizi
description: How to use bizi effectively to run tasks collaboratively with users.
---

# bizi

bizi is a tool to make it easier to manage concurrent dependent tasks.

## When to Use

- When you need to run tasks in the repository (i.e. lint, format, dev, build, etc.)

## Instructions

The bizi config is located in the `task.config.json` file.

Lets take for example the following config:

```jsonc
{
	"$schema": "https://getbizi.dev/schemas/task.config.json",
	"tasks": {
		// task names are the keys of the task object
		"lint": {
			// command that this task will run
			"command": "pnpm lint",
		},
		"format": {
			"command": "pnpm format",
		},
		"dev": {
			"tasks": {
				"generate": {
					"command": "pnpm generate",
				},
				// tasks can have subtasks
				// this task would be identified by "dev:packages"
				"packages": {
					"command": "pnpm dev packages",
					// this task will only run once "dev:generate" has finished because we defined it as a dependency
					// it's important to note that you should never put a long running task like a dev command as a dependency since it will never finish until it's canceled preventing the dependent task from running
					"dependsOn": ["dev:generate"],
				},
			},
		},
	},
}
```

To run tasks you can use the bizi cli:

```sh
bizi run lint # run the lint task
bizi run format # run the format task
bizi run dev # run the dev task
```

Running a task may not necessarily starting a new process. For instance if the user is already running the `dev` task then running `bizi run dev` will not start a new process. It will instead retrieve the logs from the currently running process.

Commands detect if the environment is TTY but we always recommend running commands with the `--non-interactive` flag to ensure that the command always runs in a non-interactive mode and doesn't accidentally cancel user tasks.

You should generally prefer running tasks from the root of the task file since users will have set them up that way intentionally.
