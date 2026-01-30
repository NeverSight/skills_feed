---
name: uv-tdd
description: A development process for Python code that uses Test Drivern Development (TDD) to iterate on a new project based around uv. Use when creating a new Python project, writing Python code with tests, or working on Python development using test-driven development practices with the uv package manager.
---

# uv-tdd skill

A development process for Python applications that uses TDD to iterate on a new project based around uv.

Create a project with this command:

```bash
mkdir name-of-project
cd name-of-project
uv init --python 3.14
git init (if not already in a git repo)
```

This creates an initial pyproject.toml file

Add dependencies using:

```bash
uv add httpx
```

Always start by adding a dev dependency of pytest like this:

```bash
uv add pytest --dev
```

Then add a starting test:

```bash
mkdir tests
echo 'def test_add():
    assert 1 + 1 == 2' > tests/test_add.py
```

Then run the tests like this:

```bash
uv run pytest
```

Always run Python code like this:

```bash
uv run python -c "..."
```

Always create a README.md for the project, which starts with just the project name as a heading plus a short description.

Start by creating a spec.md file with a detailed specification that includes markdown TODO lists. Update the spec and those TODOs as you progress, including adding new ones and checking off previous ones.

Practice TDD. For every change start by writing a test (grouped sensible in test files with other related tests) and then use `uv run pytest -k name_of_test` to watch it fail. Then implement the change and watch the test pass. Update the TODOs and add or update relevant documentation in the README, then commit the implementation and tests and documentation as a single commit.

Use and reuse pytest fixtures where appropriate, including for temporary files used for the duration of the test run. Use `pytest.mark.parameterized` to avoid duplicated test code.

Delete that test_add.py file once you have implemented your first real test. Do not include that test_add.py file in any of your commits.

Commit often, in sensible chunks. If a remote is configured then push after every commit.
