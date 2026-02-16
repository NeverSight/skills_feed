---
name: building-python-clis
description: Builds command-line interfaces for Python libraries using Click or Typer. Includes command groups, argument handling, progress bars, shell completion, and CLI testing with CliRunner. Use when adding CLI functionality to a library or building standalone command-line tools.
---

# Python CLI Development

## Framework Selection

**Click** (Recommended): Mature, extensive features
**Typer**: Modern, type-hint focused
**argparse**: Zero dependencies, standard library

## Click Quick Start

```python
import click

@click.group()
@click.version_option(version='1.0.0')
def cli():
    """My CLI tool."""
    pass

@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output', '-o', default='-', help='Output file')
@click.option('--verbose', '-v', is_flag=True)
def process(input_file, output, verbose):
    """Process an input file."""
    if verbose:
        click.echo(f"Processing {input_file}")
    # ...

if __name__ == '__main__':
    cli()
```

## Entry Point (pyproject.toml)

```toml
[project.scripts]
mycli = "my_package.cli:cli"

[project.optional-dependencies]
cli = ["click>=8.0"]
```

## Common Patterns

```python
# File I/O with stdin/stdout support
@click.argument('input', type=click.File('r'), default='-')
@click.argument('output', type=click.File('w'), default='-')

# Progress bar
with click.progressbar(items, label='Processing') as bar:
    for item in bar:
        process(item)

# Colored output
click.secho("Success!", fg='green', bold=True)
click.secho("Error!", fg='red', err=True)

# Error handling
if not valid:
    raise click.BadParameter(f'Invalid value: {value}')
```

## Testing with CliRunner

```python
from click.testing import CliRunner
from mypackage.cli import cli

def test_process():
    runner = CliRunner()
    result = runner.invoke(cli, ['process', 'input.txt'])
    assert result.exit_code == 0
    assert 'expected output' in result.output

def test_stdin():
    runner = CliRunner()
    result = runner.invoke(cli, ['process', '-'], input='test data\n')
    assert result.exit_code == 0
```

## Shell Completion

```bash
# Generate completion scripts
_MYCLI_COMPLETE=bash_source mycli > ~/.mycli-complete.bash
_MYCLI_COMPLETE=zsh_source mycli > ~/.mycli-complete.zsh
```

For detailed patterns, see:
- **[CLICK_PATTERNS.md](CLICK_PATTERNS.md)** - Advanced Click usage
- **[TYPER_GUIDE.md](TYPER_GUIDE.md)** - Typer alternative

## CLI Checklist

```
Setup:
- [ ] Entry point in pyproject.toml
- [ ] --help works for all commands
- [ ] --version displays version

UX:
- [ ] Errors go to stderr with non-zero exit
- [ ] Helpful error messages
- [ ] stdin/stdout support where appropriate

Testing:
- [ ] Tests for all commands
- [ ] Test error cases
- [ ] Test stdin processing
```

## Learn More

This skill is based on the [Guide to Developing High-Quality Python Libraries](https://mcginniscommawill.com/guides/python-library-development/) by [Will McGinnis](https://mcginniscommawill.com/). See the full guide for deeper coverage of CLI patterns and library distribution.
