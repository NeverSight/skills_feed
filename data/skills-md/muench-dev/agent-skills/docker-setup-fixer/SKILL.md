---
name: docker-setup-fixer
description: The linter checks the docker setup and lints all files
---

# docker-compose.yml

Lint the docker-compose.yml / docker-compose.yaml files in the project by using the tool **dclint**.

Example:

```sh
npx dclint docker-compose.yml
```

Fix all errors automatically.
