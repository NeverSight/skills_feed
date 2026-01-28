---
name: justfile
description: "Use when writing Justfiles to understand the latest syntax, features, and best practices"
---

# Writing Justfiles

The below readme is pulled from: https://github.com/casey/just/blob/master/README.md

It fully documents the Justfile syntax and system.

---


<h1 align=center><code>just</code></h1>



`just` is a handy way to save and run project-specific commands.

This readme is also available as a [book](https://just.systems/man/en/). The
book reflects the latest release, whereas the
[readme on GitHub](https://github.com/casey/just/blob/master/README.md)
reflects latest master.

(中文文档在 [这里](https://github.com/casey/just/blob/master/README.中文.md),
快看过来!)

Commands, called recipes, are stored in a file called `justfile` with syntax
inspired by `make`:

![screenshot](https://raw.githubusercontent.com/casey/just/master/screenshot.png)

You can then run them with `just RECIPE`:

```console
$ just test-all
cc *.c -o main
./test --all
Yay, all your tests passed!
```

`just` has a ton of useful features, and many improvements over `make`:

- `just` is a command runner, not a build system, so it avoids much of
[`make`'s complexity and idiosyncrasies](#what-are-the-idiosyncrasies-of-make-that-just-avoids).
No need for `.PHONY` recipes!
- Linux, MacOS, Windows, and other reasonable unices are supported with no
additional dependencies. (Although if your system doesn't have an `sh`,
you'll need to [choose a different shell](#shell).)
- Errors are specific and informative, and syntax errors are reported along
with their source context.
- Recipes can accept [command line arguments](#recipe-parameters).
- Wherever possible, errors are resolved statically. Unknown recipes and
circular dependencies are reported before anything runs.
- `just` [loads `.env` files](#dotenv-settings), making it easy to populate
environment variables.
- Recipes can be [listed from the command line](#listing-available-recipes).
- Command line completion scripts are
[available for most popular shells](#shell-completion-scripts).
- Recipes can be written in
[arbitrary languages](#shebang-recipes), like Python or NodeJS.
- `just` can be invoked from any subdirectory, not just the directory that
contains the `justfile`.
- And [much more](https://just.systems/man/en/)!

If you need help with `just` please feel free to open an issue or ping me on
[Discord](https://discord.gg/ezYScXR). Feature requests and bug reports are
always welcome!

## Quick Start

See the installation section for how to install `just` on your computer. Try
running `just --version` to make sure that it's installed correctly.

For an overview of the syntax, check out
[this cheatsheet](https://cheatography.com/linux-china/cheat-sheets/justfile/).

Once `just` is installed and working, create a file named `justfile` in the
root of your project with the following contents:

```just
recipe-name:
  echo 'This is a recipe!'

# this is a comment
another-recipe:
  @echo 'This is another recipe.'
```

When you invoke `just` it looks for file `justfile` in the current directory
and upwards, so you can invoke it from any subdirectory of your project.

The search for a `justfile` is case insensitive, so any case, like `Justfile`,
`JUSTFILE`, or `JuStFiLe`, will work. `just` will also look for files with the
name `.justfile`, in case you'd like to hide a `justfile`.

Running `just` with no arguments runs the first recipe in the `justfile`:

```console
$ just
echo 'This is a recipe!'
This is a recipe!
```

One or more arguments specify the recipe(s) to run:

```console
$ just another-recipe
This is another recipe.
```

`just` prints each command to standard error before running it, which is why
`echo 'This is a recipe!'` was printed. This is suppressed for lines starting
with `@`, which is why `echo 'This is another recipe.'` was not printed.

Recipes stop running if a command fails. Here `cargo publish` will only run if
`cargo test` succeeds:

```just
publish:
  cargo test
  # tests passed, time to publish!
  cargo publish
```

Recipes can depend on other recipes. Here the `test` recipe depends on the
`build` recipe, so `build` will run before `test`:

```just
build:
  cc main.c foo.c bar.c -o main

test: build
  ./test

sloc:
  @echo "`wc -l *.c` lines of code"
```

```console
$ just test
cc main.c foo.c bar.c -o main
./test
testing… all tests passed!
```

Recipes without dependencies will run in the order they're given on the command
line:

```console
$ just build sloc
cc main.c foo.c bar.c -o main
1337 lines of code
```

Dependencies will always run first, even if they are passed after a recipe that
depends on them:

```console
$ just test build
cc main.c foo.c bar.c -o main
./test
testing… all tests passed!
```

Recipes may depend on recipes in submodules:

```justfile
mod foo

baz: foo::bar
```

## Examples

A variety of `justfile`s can be found in the
[examples directory](https://github.com/casey/just/tree/master/examples) and on
[GitHub](https://github.com/search?q=path%3A**%2Fjustfile&type=code).

## Features

### The Default Recipe

When `just` is invoked without a recipe, it runs the recipe with the
`[default]` attribute, or the first recipe in the `justfile` if no recipe has
the `[default]` attribute.

This recipe might be the most frequently run command in the project, like
running the tests:

```just
test:
  cargo test
```

You can also use dependencies to run multiple recipes by default:

```just
default: lint build test

build:
  echo Building…

test:
  echo Testing…

lint:
  echo Linting…
```

If no recipe makes sense as the default recipe, you can add a recipe to the
beginning of your `justfile` that lists the available recipes:

```just
default:
  just --list
```

### Listing Available Recipes

Recipes can be listed in alphabetical order with `just --list`:

```console
$ just --list
Available recipes:
    build
    test
    deploy
    lint
```

Recipes in [submodules](#modules1190) can be listed with `just --list PATH`,
where `PATH` is a space- or `::`-separated module path:

```
$ cat justfile
mod foo
$ cat foo.just
mod bar
$ cat bar.just
baz:
$ just --list foo bar
Available recipes:
    baz
$ just --list foo::bar
Available recipes:
    baz
```

`just --summary` is more concise:

```console
$ just --summary
build test deploy lint
```

Pass `--unsorted` to print recipes in the order they appear in the `justfile`:

```just
test:
  echo 'Testing!'

build:
  echo 'Building!'
```

```console
$ just --list --unsorted
Available recipes:
    test
    build
```

```console
$ just --summary --unsorted
test build
```

If you'd like `just` to default to listing the recipes in the `justfile`, you
can use this as your default recipe:

```just
default:
  @just --list
```

Note that you may need to add `--justfile {{justfile()}}` to the line above.
Without it, if you executed `just -f /some/distant/justfile -d .` or
`just -f ./non-standard-justfile`, the plain `just --list` inside the recipe
would not necessarily use the file you provided. It would try to find a
justfile in your current path, maybe even resulting in a `No justfile found`
error.

The heading text can be customized with `--list-heading`:

```console
$ just --list --list-heading $'Cool stuff…\n'
Cool stuff…
    test
    build
```

And the indentation can be customized with `--list-prefix`:

```console
$ just --list --list-prefix ····
Available recipes:
····test
····build
```

The argument to `--list-heading` replaces both the heading and the newline
following it, so it should contain a newline if non-empty. It works this way so
you can suppress the heading line entirely by passing the empty string:

```console
$ just --list --list-heading ''
    test
    build
```

### Invoking Multiple Recipes

Multiple recipes may be invoked on the command line at once:

```just
build:
  make web

serve:
  python3 -m http.server -d out 8000
```

```console
$ just build serve
make web
python3 -m http.server -d out 8000
```

Keep in mind that recipes with parameters will swallow arguments, even if they
match the names of other recipes:

```just
build project:
  make {{project}}

serve:
  python3 -m http.server -d out 8000
```

```console
$ just build serve
make: *** No rule to make target `serve'.  Stop.
```

The `--one` flag can be used to restrict command-line invocations to a single
recipe:

```console
$ just --one build serve
error: Expected 1 command-line recipe invocation but found 2.
```

### Working Directory

By default, recipes run with the working directory set to the directory that
contains the `justfile`.

The `[no-cd]` attribute can be used to make recipes run with the working
directory set to directory in which `just` was invoked.

```just
@foo:
  pwd

[no-cd]
@bar:
  pwd
```

```console
$ cd subdir
$ just foo
/
$ just bar
/subdir
```

You can override the working directory for all recipes with
`set working-directory := '…'`:

```just
set working-directory := 'bar'

@foo:
  pwd
```

```console
$ pwd
/home/bob
$ just foo
/home/bob/bar
```

You can override the working directory for a specific recipe with the
`working-directory` attribute<sup>1.38.0</sup>:

```just
[working-directory: 'bar']
@foo:
  pwd
```

```console
$ pwd
/home/bob
$ just foo
/home/bob/bar
```

The argument to the `working-directory` setting or `working-directory`
attribute may be absolute or relative. If it is relative it is interpreted
relative to the default working directory.

### Aliases

Aliases allow recipes to be invoked on the command line with alternative names:

```just
alias b := build

build:
  echo 'Building!'
```

```console
$ just b
echo 'Building!'
Building!
```

The target of an alias may be a recipe in a submodule:

```justfile
mod foo

alias baz := foo::bar
```

### Settings

Settings control interpretation and execution. Each setting may be specified at
most once, anywhere in the `justfile`.

For example:

```just
set shell := ["zsh", "-cu"]

foo:
  # this line will be run as `zsh -cu 'ls **/*.txt'`
  ls **/*.txt
```

#### Table of Settings

| Name | Value | Default | Description |
|------|-------|---------|-------------|
| `allow-duplicate-recipes` | boolean | `false` | Allow recipes appearing later in a `justfile` to override earlier recipes with the same name. |
| `allow-duplicate-variables` | boolean | `false` | Allow variables appearing later in a `justfile` to override earlier variables with the same name. |
| `dotenv-filename` | string | - | Load a `.env` file with a custom name, if present. |
| `dotenv-load` | boolean | `false` | Load a `.env` file, if present. |
| `dotenv-override` | boolean | `false` | Override existing environment variables with values from the `.env` file. |
| `dotenv-path` | string | - | Load a `.env` file from a custom path and error if not present. Overrides `dotenv-filename`. |
| `dotenv-required` | boolean | `false` | Error if a `.env` file isn't found. |
| `export` | boolean | `false` | Export all variables as environment variables. |
| `fallback` | boolean | `false` | Search `justfile` in parent directory if the first recipe on the command line is not found. |
| `ignore-comments` | boolean | `false` | Ignore recipe lines beginning with `#`. |
| `positional-arguments` | boolean | `false` | Pass positional arguments. |
| `quiet` | boolean | `false` | Disable echoing recipe lines before executing. |
| `script-interpreter`<sup>1.33.0</sup> | `[COMMAND, ARGS…]` | `['sh', '-eu']` | Set command used to invoke recipes with empty `[script]` attribute. |
| `shell` | `[COMMAND, ARGS…]` | - | Set command used to invoke recipes and evaluate backticks. |
| `tempdir` | string | - | Create temporary directories in `tempdir` instead of the system default temporary directory. |
| `unstable`<sup>1.31.0</sup> | boolean | `false` | Enable unstable features. |
| `windows-powershell` | boolean | `false` | Use PowerShell on Windows as default shell. (Deprecated. Use `windows-shell` instead. |
| `windows-shell` | `[COMMAND, ARGS…]` | - | Set the command used to invoke recipes and evaluate backticks. |
| `working-directory`<sup>1.33.0</sup> | string | - | Set the working directory for recipes and backticks, relative to the default working directory. |

Boolean settings can be written as:

```justfile
set NAME
```

Which is equivalent to:

```justfile
set NAME := true
```

Non-boolean settings can be set to both strings and
expressions.<sup>1.46.0</sup>

However, because settings affect the behavior of backticks and many functions,
those expressions may not contain backticks or function calls, directly or
transitively via reference.

#### Allow Duplicate Recipes

If `allow-duplicate-recipes` is set to `true`, defining multiple recipes with
the same name is not an error and the last definition is used. Defaults to
`false`.

```just
set allow-duplicate-recipes

@foo:
  echo foo

@foo:
  echo bar
```

```console
$ just foo
bar
```

#### Allow Duplicate Variables

If `allow-duplicate-variables` is set to `true`, defining multiple variables
with the same name is not an error and the last definition is used. Defaults to
`false`.

```just
set allow-duplicate-variables

a := "foo"
a := "bar"

@foo:
  echo {{a}}
```

```console
$ just foo
bar
```

#### Dotenv Settings

If any of `dotenv-load`, `dotenv-filename`, `dotenv-override`, `dotenv-path`,
or `dotenv-required` are set, `just` will try to load environment variables
from a file.

If `dotenv-path` is set, `just` will look for a file at the given path, which
may be absolute, or relative to the working directory.

The command-line option `--dotenv-path`, short form `-E`, can be used to set or
override `dotenv-path` at runtime.

If `dotenv-filename` is set `just` will look for a file at the given path,
relative to the working directory and each of its ancestors.

If `dotenv-filename` is not set, but `dotenv-load` or `dotenv-required` are
set, just will look for a file named `.env`, relative to the working directory
and each of its ancestors.

`dotenv-filename` and `dotenv-path` are similar, but `dotenv-path` is only
checked relative to the working directory, whereas `dotenv-filename` is checked
relative to the working directory and each of its ancestors.

It is not an error if an environment file is not found, unless
`dotenv-required` is set.

The loaded variables are environment variables, not `just` variables, and so
must be accessed using `$VARIABLE_NAME` in recipes and backticks.

If `dotenv-override` is set, variables from the environment file will override
existing environment variables.

For example, if your `.env` file contains:

```console
# a comment, will be ignored
DATABASE_ADDRESS=localhost:6379
SERVER_PORT=1337
```

And your `justfile` contains:

```just
set dotenv-load

serve:
  @echo "Starting server with database $DATABASE_ADDRESS on port $SERVER_PORT…"
  ./server --database $DATABASE_ADDRESS --port $SERVER_PORT
```

`just serve` will output:

```console
$ just serve
Starting server with database localhost:6379 on port 1337…
./server --database $DATABASE_ADDRESS --port $SERVER_PORT
```

#### Export

The `export` setting causes all `just` variables to be exported as environment
variables. Defaults to `false`.

```just
set export

a := "hello"

@foo b:
  echo $a
  echo $b
```

```console
$ just foo goodbye
hello
goodbye
```

#### Positional Arguments

If `positional-arguments` is `true`, recipe arguments will be passed as
positional arguments to commands. For linewise recipes, argument `$0` will be
the name of the recipe.

For example, running this recipe:

```just
set positional-arguments

@foo bar:
  echo $0
  echo $1
```

Will produce the following output:

```console
$ just foo hello
foo
hello
```

When using an `sh`-compatible shell, such as `bash` or `zsh`, `$@` expands to
the positional arguments given to the recipe, starting from one. When used
within double quotes as `"$@"`, arguments including whitespace will be passed
on as if they were double-quoted. That is, `"$@"` is equivalent to `"$1" "$2"`…
When there are no positional parameters, `"$@"` and `$@` expand to nothing
(i.e., they are removed).

This example recipe will print arguments one by one on separate lines:

```just
set positional-arguments

@test *args='':
  bash -c 'while (( "$#" )); do echo - $1; shift; done' -- "$@"
```

Running it with *two* arguments:

```console
$ just test foo "bar baz"
- foo
- bar baz
```

Positional arguments may also be turned on on a per-recipe basis with the
`[positional-arguments]` attribute<sup>1.29.0</sup>:

```just
[positional-arguments]
@foo bar:
  echo $0
  echo $1
```

Note that PowerShell does not handle positional arguments in the same way as
other shells, so turning on positional arguments will likely break recipes that
use PowerShell.

If using PowerShell 7.4 or better, the `-CommandWithArgs` flag will make
positional arguments work as expected:

```just
set shell := ['pwsh.exe', '-CommandWithArgs']
set positional-arguments

print-args a b c:
  Write-Output @($args[1..($args.Count - 1)])
```

#### Shell

The `shell` setting controls the command used to invoke recipe lines and
backticks. Shebang recipes are unaffected. The default shell is `sh -cu`.

```just
# use python3 to execute recipe lines and backticks
set shell := ["python3", "-c"]

# use print to capture result of evaluation
foos := `print("foo" * 4)`

foo:
  print("Snake snake snake snake.")
  print("{{foos}}")
```

`just` passes the command to be executed as an argument. Many shells will need
an additional flag, often `-c`, to make them evaluate the first argument.

##### Windows Shell

`just` uses `sh` on Windows by default. To use a different shell on Windows,
use `windows-shell`:

```just
set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

hello:
  Write-Host "Hello, world!"
```

See
[powershell.just](https://github.com/casey/just/blob/master/examples/powershell.just)
for a justfile that uses PowerShell on all platforms.

##### Windows PowerShell

*`set windows-powershell` uses the legacy `powershell.exe` binary, and is no
longer recommended. See the `windows-shell` setting above for a more flexible
way to control which shell is used on Windows.*

`just` uses `sh` on Windows by default. To use `powershell.exe` instead, set
`windows-powershell` to true.

```just
set windows-powershell := true

hello:
  Write-Host "Hello, world!"
```

##### Python 3

```just
set shell := ["python3", "-c"]
```

##### Bash

```just
set shell := ["bash", "-uc"]
```

##### Z Shell

```just
set shell := ["zsh", "-uc"]
```

##### Fish

```just
set shell := ["fish", "-c"]
```

##### Nushell

```just
set shell := ["nu", "-c"]
```

If you want to change the default table mode to `light`:

```just
set shell := ['nu', '-m', 'light', '-c']
```

*[Nushell](https://github.com/nushell/nushell) was written in Rust, and **has
cross-platform support for Windows / macOS and Linux**.*

### Documentation Comments

Comments immediately preceding a recipe will appear in `just --list`:

```just
# build stuff
build:
  ./bin/build

# test stuff
test:
  ./bin/test
```

```console
$ just --list
Available recipes:
    build # build stuff
    test # test stuff
```

The `[doc]` attribute can be used to set or suppress a recipe's doc comment:

```just
# This comment won't appear
[doc('Build stuff')]
build:
  ./bin/build

# This one won't either
[doc]
test:
  ./bin/test
```

```console
$ just --list
Available recipes:
    build # Build stuff
    test
```

### Expressions and Substitutions

Various operators and function calls are supported in expressions, which may be
used in assignments, default recipe arguments, and inside recipe body `{{…}}`
substitutions.

```just
tmpdir  := `mktemp -d`
version := "0.2.7"
tardir  := tmpdir / "awesomesauce-" + version
tarball := tardir + ".tar.gz"
config  := quote(config_dir() / ".project-config")

publish:
  rm -f {{tarball}}
  mkdir {{tardir}}
  cp README.md *.c {{ config }} {{tardir}}
  tar zcvf {{tarball}} {{tardir}}
  scp {{tarball}} me@server.com:release/
  rm -rf {{tarball}} {{tardir}}
```

#### Concatenation

The `+` operator returns the left-hand argument concatenated with the
right-hand argument:

```just
foobar := 'foo' + 'bar'
```

#### Logical Operators

The logical operators `&&` and `||` can be used to coalesce string
values<sup>1.37.0</sup>, similar to Python's `and` and `or`. These operators
consider the empty string `''` to be false, and all other strings to be true.

These operators are currently unstable.

The `&&` operator returns the empty string if the left-hand argument is the
empty string, otherwise it returns the right-hand argument:

```justfile
foo := '' && 'goodbye'      # ''
bar := 'hello' && 'goodbye' # 'goodbye'
```

The `||` operator returns the left-hand argument if it is non-empty, otherwise
it returns the right-hand argument:

```justfile
foo := '' || 'goodbye'      # 'goodbye'
bar := 'hello' || 'goodbye' # 'hello'
```

#### Joining Paths

The `/` operator can be used to join two strings with a slash:

```just
foo := "a" / "b"
```

```
$ just --evaluate foo
a/b
```

Note that a `/` is added even if one is already present:

```just
foo := "a/"
bar := foo / "b"
```

```
$ just --evaluate bar
a//b
```

Absolute paths can also be constructed<sup>1.5.0</sup>:

```just
foo := / "b"
```

```
$ just --evaluate foo
/b
```

The `/` operator uses the `/` character, even on Windows. Thus, using the `/`
operator should be avoided with paths that use universal naming convention
(UNC), i.e., those that start with `\?`, since forward slashes are not
supported with UNC paths.

#### Escaping `{{`

To write a recipe containing `{{`, use `{{{{`:

```just
braces:
  echo 'I {{{{LOVE}} curly braces!'
```

(An unmatched `}}` is ignored, so it doesn't need to be escaped.)

Another option is to put all the text you'd like to escape inside of an
interpolation:

```just
braces:
  echo '{{'I {{LOVE}} curly braces!'}}'
```

Yet another option is to use `{{ "{{" }}`:

```just
braces:
  echo 'I {{ "{{" }}LOVE}} curly braces!'
```

### Strings

`'single'`, `"double"`, and `'''triple'''` quoted string literals are
supported. Unlike in recipe bodies, `{{…}}` interpolations are not supported
inside strings.

Double-quoted strings support escape sequences:

```just
carriage-return   := "\r"
double-quote      := "\""
newline           := "\n"
no-newline        := "\
"
slash             := "\\"
tab               := "\t"
unicode-codepoint := "\u{1F916}"
```

```console
$ just --evaluate
"arriage-return   := "
double-quote      := """
newline           := "
"
no-newline        := ""
slash             := "\"
tab               := "     "
unicode-codepoint := "🤖"
```

The unicode character escape sequence `\u{…}`<sup>1.36.0</sup> accepts up to
six hex digits.

Strings may contain line breaks:

```just
single := '
hello
'

double := "
goodbye
"
```

Single-quoted strings do not recognize escape sequences:

```just
escapes := '\t\n\r\"\\'
```

```console
$ just --evaluate
escapes := "\t\n\r\"\\"
```

Indented versions of both single- and double-quoted strings, delimited by
triple single- or double-quotes, are supported. Indented string lines are
stripped of a leading line break, and leading whitespace common to all
non-blank lines:

```just
# this string will evaluate to `foo\nbar\n`
x := '''
  foo
  bar
'''

# this string will evaluate to `abc\n  wuv\nxyz\n`
y := """
  abc
    wuv
  xyz
"""
```

Similar to unindented strings, indented double-quoted strings process escape
sequences, and indented single-quoted strings ignore escape sequences. Escape
sequence processing takes place after unindentation. The unindentation
algorithm does not take escape-sequence produced whitespace or newlines into
account.

#### Shell-expanded strings

Strings prefixed with `x` are shell expanded<sup>1.27.0</sup>:

```justfile
foobar := x'~/$FOO/${BAR}'
```

| Value | Replacement |
|------|-------------|
| `$VAR` | value of environment variable `VAR` |
| `${VAR}` | value of environment variable `VAR` |
| `${VAR:-DEFAULT}` | value of environment variable `VAR`, or `DEFAULT` if `VAR` is not set |
| Leading `~` | path to current user's home directory |
| Leading `~USER` | path to `USER`'s home directory |

This expansion is performed at compile time, so variables from `.env` files and
exported `just` variables cannot be used. However, this allows shell expanded
strings to be used in places like settings and import paths, which cannot
depend on `just` variables and `.env` files.

#### Format strings

Strings prefixed with `f` are format strings<sup>1.44.0</sup>:

```justfile
name := "world"
message := f'Hello, {{name}}!'
```

Format strings may contain interpolations delimited with `{{…}}` that contain
expressions. Format strings evaluate to the concatenated string fragments and
evaluated expressions.

Use `{{{{` to include a literal `{{` in a format string:

```justfile
foo := f'I {{{{LOVE} curly braces!'
```

### Ignoring Errors

Normally, if a command returns a non-zero exit status, execution will stop. To
continue execution after a command, even if it fails, prefix the command with
`-`:

```just
foo:
  -cat foo
  echo 'Done!'
```

```console
$ just foo
cat foo
cat: foo: No such file or directory
echo 'Done!'
Done!
```

### Functions

`just` provides many built-in functions for use in expressions, including
recipe body `{{…}}` substitutions, assignments, and default parameter values.

All functions ending in `_directory` can be abbreviated to `_dir`. So
`home_directory()` can also be written as `home_dir()`. In addition,
`invocation_directory_native()` can be abbreviated to
`invocation_dir_native()`.

#### System Information

- `arch()` — Instruction set architecture. Possible values are: `"aarch64"`,
`"arm"`, `"asmjs"`, `"hexagon"`, `"mips"`, `"msp430"`, `"powerpc"`,
`"powerpc64"`, `"s390x"`, `"sparc"`, `"wasm32"`, `"x86"`, `"x86_64"`, and
`"xcore"`.
- `num_cpus()`<sup>1.15.0</sup> - Number of logical CPUs.
- `os()` — Operating system. Possible values are: `"android"`, `"bitrig"`,
`"dragonfly"`, `"emscripten"`, `"freebsd"`, `"haiku"`, `"ios"`, `"linux"`,
`"macos"`, `"netbsd"`, `"openbsd"`, `"solaris"`, and `"windows"`.
- `os_family()` — Operating system family; possible values are: `"unix"` and
`"windows"`.

For example:

```just
system-info:
  @echo "This is an {{arch()}} machine".
```

```console
$ just system-info
This is an x86_64 machine
```

The `os_family()` function can be used to create cross-platform `justfile`s
that work on various operating systems. For an example, see
[cross-platform.just](https://github.com/casey/just/blob/master/examples/cross-platform.just)
file.

#### External Commands

- `shell(command, args...)`<sup>1.27.0</sup> returns the standard output of shell script
`command` with zero or more positional arguments `args`. The shell used to
interpret `command` is the same shell that is used to evaluate recipe lines,
and can be changed with `set shell := […]`.
  
  `command` is passed as the first argument, so if the command is `'echo $@'`,
the full command line, with the default shell command `sh -cu` and `args`
`'foo'` and `'bar'` will be:
  
  ```
  'sh' '-cu' 'echo $@' 'echo $@' 'foo' 'bar'
  ```
  
  This is so that `$@` works as expected, and `$1` refers to the first
argument. `$@` does not include the first positional argument, which is
expected to be the name of the program being run.

```just
# arguments can be variables or expressions
file := '/sys/class/power_supply/BAT0/status'
bat0stat := shell('cat $1', file)

# commands can be variables or expressions
command := 'wc -l'
output := shell(command + ' "$1"', 'main.c')

# arguments referenced by the shell command must be used
empty := shell('echo', 'foo')
full := shell('echo $1', 'foo')
error := shell('echo $1')
```

```just
# Using python as the shell. Since `python -c` sets `sys.argv[0]` to `'-c'`,
# the first "real" positional argument will be `sys.argv[2]`.
set shell := ["python3", "-c"]
olleh := shell('import sys; print(sys.argv[2][::-1])', 'hello')
```

#### Environment Variables

- `env(key)`<sup>1.15.0</sup> — Retrieves the environment variable with name `key`, aborting
if it is not present.

```just
home_dir := env('HOME')

test:
  echo "{{home_dir}}"
```

```console
$ just
/home/user1
```

- `env(key, default)`<sup>1.15.0</sup> — Retrieves the environment variable with
name `key`, returning `default` if it is not present.
- `env_var(key)` — Deprecated alias for `env(key)`.
- `env_var_or_default(key, default)` — Deprecated alias for `env(key, default)`.

A default can be substituted for an empty environment variable value with the
`||` operator, currently unstable:

```just
set unstable

foo := env('FOO', '') || 'DEFAULT_VALUE'
```

#### Executables

- `require(name)`<sup>1.39.0</sup> — Search directories in the `PATH`
environment variable for the executable `name` and return its full path, or
halt with an error if no executable with `name` exists.
  
  ```just
  bash := require("bash")
  
  @test:
      echo "bash: '{{bash}}'"
  ```
  
  ```console
  $ just
  bash: '/bin/bash'
  ```
- `which(name)`<sup>1.39.0</sup> — Search directories in the `PATH` environment
variable for the executable `name` and return its full path, or the empty
string if no executable with `name` exists. Currently unstable.
  
  ```just
  set unstable
  
  bosh := which("bosh")
  
  @test:
      echo "bosh: '{{bosh}}'"
  ```
  
  ```console
  $ just
  bosh: ''
  ```

#### Invocation Information

- `is_dependency()` - Returns the string `true` if the current recipe is being
run as a dependency of another recipe, rather than being run directly,
otherwise returns the string `false`.

#### Invocation Directory

- `invocation_directory()` - Retrieves the absolute path to the current
directory when `just` was invoked, before  `just` changed it (chdir'd) prior
to executing commands. On Windows, `invocation_directory()` uses `cygpath` to
convert the invocation directory to a Cygwin-compatible `/`-separated path.
Use `invocation_directory_native()` to return the verbatim invocation
directory on all platforms.

For example, to call `rustfmt` on files just under the "current directory"
(from the user/invoker's perspective), use the following rule:

```just
rustfmt:
  find {{invocation_directory()}} -name \*.rs -exec rustfmt {} \;
```

Alternatively, if your command needs to be run from the current directory, you
could use (e.g.):

```just
build:
  cd {{invocation_directory()}}; ./some_script_that_needs_to_be_run_from_here
```

- `invocation_directory_native()` - Retrieves the absolute path to the current
directory when `just` was invoked, before  `just` changed it (chdir'd) prior
to executing commands.

#### Justfile and Justfile Directory

- `justfile()` - Retrieves the path of the current `justfile`.
- `justfile_directory()` - Retrieves the path of the parent directory of the
current `justfile`.

For example, to run a command relative to the location of the current
`justfile`:

```just
script:
  {{justfile_directory()}}/scripts/some_script
```

#### Source and Source Directory

- `source_file()`<sup>1.27.0</sup> - Retrieves the path of the current source file.
- `source_directory()`<sup>1.27.0</sup> - Retrieves the path of the parent directory of the
current source file.

`source_file()` and `source_directory()` behave the same as `justfile()` and
`justfile_directory()` in the root `justfile`, but will return the path and
directory, respectively, of the current `import` or `mod` source file when
called from within an import or submodule.

#### Just Executable

- `just_executable()` - Absolute path to the `just` executable.

For example:

```just
executable:
  @echo The executable is at: {{just_executable()}}
```

```console
$ just
The executable is at: /bin/just
```

#### Just Process ID

- `just_pid()` - Process ID of the `just` executable.

For example:

```just
pid:
  @echo The process ID is: {{ just_pid() }}
```

```console
$ just
The process ID is: 420
```

#### String Manipulation

- `append(suffix, s)`<sup>1.27.0</sup> Append `suffix` to whitespace-separated
strings in `s`. `append('/src', 'foo bar baz')` → `'foo/src bar/src baz/src'`
- `prepend(prefix, s)`<sup>1.27.0</sup> Prepend `prefix` to
whitespace-separated strings in `s`. `prepend('src/', 'foo bar baz')` →
`'src/foo src/bar src/baz'`
- `encode_uri_component(s)`<sup>1.27.0</sup> - Percent-encode characters in `s`
except `[A-Za-z0-9_.!~*'()-]`, matching the behavior of the
[JavaScript `encodeURIComponent` function](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/encodeURIComponent).
- `quote(s)` - Replace all single quotes with `'\''` and prepend and append
single quotes to `s`. This is sufficient to escape special characters for
many shells, including most Bourne shell descendants.
- `replace(s, from, to)` - Replace all occurrences of `from` in `s` to `to`.
- `replace_regex(s, regex, replacement)` - Replace all occurrences of `regex`
in `s` to `replacement`. Regular expressions are provided by the
[Rust `regex` crate](https://docs.rs/regex/latest/regex/). See the
[syntax documentation](https://docs.rs/regex/latest/regex/#syntax) for usage
examples. Capture groups are supported. The `replacement` string uses
[Replacement string syntax](https://docs.rs/regex/latest/regex/struct.Regex.html#replacement-string-syntax).
- `trim(s)` - Remove leading and trailing whitespace from `s`.
- `trim_end(s)` - Remove trailing whitespace from `s`.
- `trim_end_match(s, substring)` - Remove suffix of `s` matching `substring`.
- `trim_end_matches(s, substring)` - Repeatedly remove suffixes of `s` matching
`substring`.
- `trim_start(s)` - Remove leading whitespace from `s`.
- `trim_start_match(s, substring)` - Remove prefix of `s` matching `substring`.
- `trim_start_matches(s, substring)` - Repeatedly remove prefixes of `s`
matching `substring`.

#### Case Conversion

- `capitalize(s)`<sup>1.7.0</sup> - Convert first character of `s` to uppercase
and the rest to lowercase.
- `kebabcase(s)`<sup>1.7.0</sup> - Convert `s` to `kebab-case`.
- `lowercamelcase(s)`<sup>1.7.0</sup> - Convert `s` to `lowerCamelCase`.
- `lowercase(s)` - Convert `s` to lowercase.
- `shoutykebabcase(s)`<sup>1.7.0</sup> - Convert `s` to `SHOUTY-KEBAB-CASE`.
- `shoutysnakecase(s)`<sup>1.7.0</sup> - Convert `s` to `SHOUTY_SNAKE_CASE`.
- `snakecase(s)`<sup>1.7.0</sup> - Convert `s` to `snake_case`.
- `titlecase(s)`<sup>1.7.0</sup> - Convert `s` to `Title Case`.
- `uppercamelcase(s)`<sup>1.7.0</sup> - Convert `s` to `UpperCamelCase`.
- `uppercase(s)` - Convert `s` to uppercase.

#### Path Manipulation

##### Fallible

- `absolute_path(path)` - Absolute path to relative `path` in the working
directory. `absolute_path("./bar.txt")` in directory `/foo` is
`/foo/bar.txt`.
- `canonicalize(path)`<sup>1.24.0</sup> - Canonicalize `path` by resolving symlinks and removing
`.`, `..`, and extra `/`s where possible.
- `extension(path)` - Extension of `path`. `extension("/foo/bar.txt")` is
`txt`.
- `file_name(path)` - File name of `path` with any leading directory components
removed. `file_name("/foo/bar.txt")` is `bar.txt`.
- `file_stem(path)` - File name of `path` without extension.
`file_stem("/foo/bar.txt")` is `bar`.
- `parent_directory(path)` - Parent directory of `path`.
`parent_directory("/foo/bar.txt")` is `/foo`.
- `without_extension(path)` - `path` without extension.
`without_extension("/foo/bar.txt")` is `/foo/bar`.

These functions can fail, for example if a path does not have an extension,
which will halt execution.

##### Infallible

- `clean(path)` - Simplify `path` by removing extra path separators,
intermediate `.` components, and `..` where possible. `clean("foo//bar")` is
`foo/bar`, `clean("foo/..")` is `.`, `clean("foo/./bar")` is `foo/bar`.
- `join(a, b…)` - *This function uses `/` on Unix and `\` on Windows, which can
be lead to unwanted behavior. The `/` operator, e.g., `a / b`, which always
uses `/`, should be considered as a replacement unless `\`s are specifically
desired on Windows.* Join path `a` with path `b`. `join("foo/bar", "baz")` is
`foo/bar/baz`. Accepts two or more arguments.

#### Filesystem Access

- `path_exists(path)` - Returns `true` if the path points at an existing entity
and `false` otherwise. Traverses symbolic links, and returns `false` if the
path is inaccessible or points to a broken symlink.
- `read(path)`<sup>1.39.0</sup> - Returns the content of file at `path` as
string.

##### Error Reporting

- `error(message)` - Abort execution and report error `message` to user.

#### UUID and Hash Generation

- `blake3(string)`<sup>1.25.0</sup> - Return [BLAKE3][blake3] hash of `string` as hexadecimal string.
- `blake3_file(path)`<sup>1.25.0</sup> - Return [BLAKE3][blake3] hash of file at `path` as hexadecimal
string.
- `sha256(string)` - Return the SHA-256 hash of `string` as hexadecimal string.
- `sha256_file(path)` - Return SHA-256 hash of file at `path` as hexadecimal
string.
- `uuid()` - Generate a random version 4 UUID.

[blake3]: https://github.com/BLAKE3-team/BLAKE3/

#### Random

- `choose(n, alphabet)`<sup>1.27.0</sup> - Generate a string of `n` randomly
selected characters from `alphabet`, which may not contain repeated
characters. For example, `choose('64', HEX)` will generate a random
64-character lowercase hex string.

#### Datetime

- `datetime(format)`<sup>1.30.0</sup> - Return local time with `format`.
- `datetime_utc(format)`<sup>1.30.0</sup> - Return UTC time with `format`.

The arguments to `datetime` and `datetime_utc` are `strftime`-style format
strings, see the
[`chrono` library docs](https://docs.rs/chrono/latest/chrono/format/strftime/index.html)
for details.

#### Semantic Versions

- `semver_matches(version, requirement)`<sup>1.16.0</sup> - Check whether a
[semantic `version`](https://semver.org), e.g., `"0.1.0"` matches a
`requirement`, e.g., `">=0.1.0"`, returning `"true"` if so and `"false"`
otherwise.

#### Style

- `style(name)`<sup>1.37.0</sup> - Return a named terminal display attribute
escape sequence used by `just`. Unlike terminal display attribute escape
sequence constants, which contain standard colors and styles, `style(name)`
returns an escape sequence used by `just` itself, and can be used to make
recipe output match `just`'s own output.
  
  Recognized values for `name` are `'command'`, for echoed recipe lines,
`error`, and `warning`.
  
  For example, to style an error message:
  
  ```just
  scary:
    @echo '{{ style("error") }}OH NO{{ NORMAL }}'
  ```

##### User Directories<sup>1.23.0</sup>

These functions return paths to user-specific directories for things like
configuration, data, caches, executables, and the user's home directory.

On Unix, these functions follow the
[XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html).

On MacOS and Windows, these functions return the system-specified user-specific
directories. For example, `cache_directory()` returns `~/Library/Caches` on
MacOS and `{FOLDERID_LocalAppData}` on Windows.

See the [`dirs`](https://docs.rs/dirs/latest/dirs/index.html) crate for more
details.

- `cache_directory()` - The user-specific cache directory.
- `config_directory()` - The user-specific configuration directory.
- `config_local_directory()` - The local user-specific configuration directory.
- `data_directory()` - The user-specific data directory.
- `data_local_directory()` - The local user-specific data directory.
- `executable_directory()` - The user-specific executable directory.
- `home_directory()` - The user's home directory.

If you would like to use XDG base directories on all platforms you can use the
`env(…)` function with the appropriate environment variable and fallback,
although note that the XDG specification requires ignoring non-absolute paths,
so for full compatibility with spec-compliant applications, you would need to
do:

```just
xdg_config_dir := if env('XDG_CONFIG_HOME', '') =~ '^/' {
  env('XDG_CONFIG_HOME')
} else {
  home_directory() / '.config'
}
```

### Constants

A number of constants are predefined:

| Name | Value | Value on Windows |
|---|---|---|
| `HEX`<sup>1.27.0</sup> | `"0123456789abcdef"` |  |
| `HEXLOWER`<sup>1.27.0</sup> | `"0123456789abcdef"` |  |
| `HEXUPPER`<sup>1.27.0</sup> | `"0123456789ABCDEF"` |  |
| `PATH_SEP`<sup>1.41.0</sup> | `"/"` | `"\"` |
| `PATH_VAR_SEP`<sup>1.41.0</sup> | `":"` | `";"` |
| `CLEAR`<sup>1.37.0</sup> | `"\ec"` |  |
| `NORMAL`<sup>1.37.0</sup> | `"\e[0m"` |  |
| `BOLD`<sup>1.37.0</sup> | `"\e[1m"` |  |
| `ITALIC`<sup>1.37.0</sup> | `"\e[3m"` |  |
| `UNDERLINE`<sup>1.37.0</sup> | `"\e[4m"` |  |
| `INVERT`<sup>1.37.0</sup> | `"\e[7m"` |  |
| `HIDE`<sup>1.37.0</sup> | `"\e[8m"` |  |
| `STRIKETHROUGH`<sup>1.37.0</sup> | `"\e[9m"` |  |
| `BLACK`<sup>1.37.0</sup> | `"\e[30m"` |  |
| `RED`<sup>1.37.0</sup> | `"\e[31m"` |  |
| `GREEN`<sup>1.37.0</sup> | `"\e[32m"` |  |
| `YELLOW`<sup>1.37.0</sup> | `"\e[33m"` |  |
| `BLUE`<sup>1.37.0</sup> | `"\e[34m"` |  |
| `MAGENTA`<sup>1.37.0</sup> | `"\e[35m"` |  |
| `CYAN`<sup>1.37.0</sup> | `"\e[36m"` |  |
| `WHITE`<sup>1.37.0</sup> | `"\e[37m"` |  |
| `BG_BLACK`<sup>1.37.0</sup> | `"\e[40m"` |  |
| `BG_RED`<sup>1.37.0</sup> | `"\e[41m"` |  |
| `BG_GREEN`<sup>1.37.0</sup> | `"\e[42m"` |  |
| `BG_YELLOW`<sup>1.37.0</sup> | `"\e[43m"` |  |
| `BG_BLUE`<sup>1.37.0</sup> | `"\e[44m"` |  |
| `BG_MAGENTA`<sup>1.37.0</sup> | `"\e[45m"` |  |
| `BG_CYAN`<sup>1.37.0</sup> | `"\e[46m"` |  |
| `BG_WHITE`<sup>1.37.0</sup> | `"\e[47m"` |  |

```just
@foo:
  echo {{HEX}}
```

```console
$ just foo
0123456789abcdef
```

Constants starting with `\e` are
[ANSI escape sequences](https://en.wikipedia.org/wiki/ANSI_escape_code).

`CLEAR` clears the screen, similar to the `clear` command. The rest are of the
form `\e[Nm`, where `N` is an integer, and set terminal display attributes.

Terminal display attribute escape sequences can be combined, for example text
weight `BOLD`, text style `STRIKETHROUGH`, foreground color `CYAN`, and
background color `BG_BLUE`. They should be followed by `NORMAL`, to reset the
terminal back to normal.

Escape sequences should be quoted, since `[` is treated as a special character
by some shells.

```just
@foo:
  echo '{{BOLD + STRIKETHROUGH + CYAN + BG_BLUE}}Hi!{{NORMAL}}'
```

### Attributes

Recipes, `mod` statements, and aliases may be annotated with attributes that
change their behavior.

| Name | Type | Description |
|------|------|-------------|
| `[arg(ARG, help="HELP")]`<sup>1.46.0</sup> | recipe | Print help string `HELP` for `ARG` in usage messages. |
| `[arg(ARG, long="LONG")]`<sup>1.46.0</sup> | recipe | Require values of argument `ARG` to be passed as `--LONG` option. |
| `[arg(ARG, short="S")]`<sup>1.46.0</sup> | recipe | Require values of argument `ARG` to be passed as short `-S` option. |
| `[arg(ARG, value="VALUE")]`<sup>1.46.0</sup> | recipe | Makes option `ARG` a flag which does not take a value. |
| `[arg(ARG, pattern="PATTERN")]`<sup>1.45.0</sup> | recipe | Require values of argument `ARG` to match regular expression `PATTERN`. |
| `[confirm]`<sup>1.17.0</sup> | recipe | Require confirmation prior to executing recipe. |
| `[confirm(PROMPT)]`<sup>1.23.0</sup> | recipe | Require confirmation prior to executing recipe with a custom prompt. |
| `[default]`<sup>1.43.0</sup> | recipe | Use recipe as module's default recipe. |
| `[doc(DOC)]`<sup>1.27.0</sup> | module, recipe | Set recipe or module's [documentation comment](#documentation-comments) to `DOC`. |
| `[extension(EXT)]`<sup>1.32.0</sup> | recipe | Set shebang recipe script's file extension to `EXT`. `EXT` should include a period if one is desired. |
| `[group(NAME)]`<sup>1.27.0</sup> | module, recipe | Put recipe or module in in [group](#groups) `NAME`. |
| `[linux]`<sup>1.8.0</sup> | recipe | Enable recipe on Linux. |
| `[macos]`<sup>1.8.0</sup> | recipe | Enable recipe on MacOS. |
| `[metadata(METADATA)]`<sup>1.42.0</sup> | recipe | Attach `METADATA` to recipe. |
| `[no-cd]`<sup>1.9.0</sup> | recipe | Don't change directory before executing recipe. |
| `[no-exit-message]`<sup>1.7.0</sup> | recipe | Don't print an error message if recipe fails. |
| `[no-quiet]`<sup>1.23.0</sup> | recipe | Override globally quiet recipes and always echo out the recipe. |
| `[openbsd]`<sup>1.38.0</sup> | recipe | Enable recipe on OpenBSD. |
| `[parallel]`<sup>1.42.0</sup> | recipe | Run this recipe's dependencies in parallel. |
| `[positional-arguments]`<sup>1.29.0</sup> | recipe | Turn on [positional arguments](#positional-arguments) for this recipe. |
| `[private]`<sup>1.10.0</sup> | alias, recipe | Make recipe, alias, or variable private. See [Private Recipes](#private-recipes). |
| `[script]`<sup>1.33.0</sup> | recipe | Execute recipe as script. See [script recipes](#script-recipes) for more details. |
| `[script(COMMAND)]`<sup>1.32.0</sup> | recipe | Execute recipe as a script interpreted by `COMMAND`. See [script recipes](#script-recipes) for more details. |
| `[unix]`<sup>1.8.0</sup> | recipe | Enable recipe on Unixes. (Includes MacOS). |
| `[windows]`<sup>1.8.0</sup> | recipe | Enable recipe on Windows. |
| `[working-directory(PATH)]`<sup>1.38.0</sup> | recipe | Set recipe working directory. `PATH` may be relative or absolute. If relative, it is interpreted relative to the default working directory. |

A recipe can have multiple attributes, either on multiple lines:

```just
[no-cd]
[private]
foo:
    echo "foo"
```

Or separated by commas on a single line<sup>1.14.0</sup>:

```just
[no-cd, private]
foo:
    echo "foo"
```

Attributes with a single argument may be written with a colon:

```just
[group: 'bar']
foo:
```

#### Enabling and Disabling Recipes<sup>1.8.0</sup>

The `[linux]`, `[macos]`, `[unix]`, and `[windows]` attributes are
configuration attributes. By default, recipes are always enabled. A recipe with
one or more configuration attributes will only be enabled when one or more of
those configurations is active.

This can be used to write `justfile`s that behave differently depending on
which operating system they run on. The `run` recipe in this `justfile` will
compile and run `main.c`, using a different C compiler and using the correct
output binary name for that compiler depending on the operating system:

```just
[unix]
run:
  cc main.c
  ./a.out

[windows]
run:
  cl main.c
  main.exe
```

#### Disabling Changing Directory<sup>1.9.0</sup>

`just` normally executes recipes with the current directory set to the
directory that contains the `justfile`. This can be disabled using the
`[no-cd]` attribute. This can be used to create recipes which use paths
relative to the invocation directory, or which operate on the current
directory.

For example, this `commit` recipe:

```just
[no-cd]
commit file:
  git add {{file}}
  git commit
```

Can be used with paths that are relative to the current directory, because
`[no-cd]` prevents `just` from changing the current directory when executing
`commit`.

#### Requiring Confirmation for Recipes<sup>1.17.0</sup>

`just` normally executes all recipes unless there is an error. The `[confirm]`
attribute allows recipes require confirmation in the terminal prior to running.
This can be overridden by passing `--yes` to `just`, which will automatically
confirm any recipes marked by this attribute.

Recipes dependent on a recipe that requires confirmation will not be run if the
relied upon recipe is not confirmed, as well as recipes passed after any recipe
that requires confirmation.

```just
[confirm]
delete-all:
  rm -rf *
```

#### Custom Confirmation Prompt<sup>1.23.0</sup>

The default confirmation prompt can be overridden with `[confirm(PROMPT)]`:

```just
[confirm("Are you sure you want to delete everything?")]
delete-everything:
  rm -rf *
```

### Groups

Recipes and modules may be annotated with one or more group names:

```just
[group('lint')]
js-lint:
    echo 'Running JS linter…'

[group('rust recipes')]
[group('lint')]
rust-lint:
    echo 'Running Rust linter…'

[group('lint')]
cpp-lint:
  echo 'Running C++ linter…'

# not in any group
email-everyone:
    echo 'Sending mass email…'
```

Recipes are listed by group:

```
$ just --list
Available recipes:
    email-everyone # not in any group

    [lint]
    cpp-lint
    js-lint
    rust-lint

    [rust recipes]
    rust-lint
```

`just --list --unsorted` prints recipes in their justfile order within each group:

```
$ just --list --unsorted
Available recipes:
    (no group)
    email-everyone # not in any group

    [lint]
    js-lint
    rust-lint
    cpp-lint

    [rust recipes]
    rust-lint
```

Groups can be listed with `--groups`:

```
$ just --groups
Recipe groups:
  lint
  rust recipes
```

Use `just --groups --unsorted` to print groups in their justfile order.

### Command Evaluation Using Backticks

Backticks can be used to store the result of commands:

```just
localhost := `dumpinterfaces | cut -d: -f2 | sed 's/\/.*//' | sed 's/ //g'`

serve:
  ./serve {{localhost}} 8080
```

Indented backticks, delimited by three backticks, are de-indented in the same
manner as indented strings:

```just
# This backtick evaluates the command `echo foo\necho bar\n`, which produces the value `foo\nbar\n`.
stuff := ```
    echo foo
    echo bar
  ```
```

See the [Strings](#strings) section for details on unindenting.

Backticks may not start with `#!`. This syntax is reserved for a future
upgrade.

The [`shell(…)` function](#external-commands) provides a more general mechanism
to invoke external commands, including the ability to execute the contents of a
variable as a command, and to pass arguments to a command.

### Conditional Expressions

`if`/`else` expressions evaluate different branches depending on if two
expressions evaluate to the same value:

```just
foo := if "2" == "2" { "Good!" } else { "1984" }

bar:
  @echo "{{foo}}"
```

```console
$ just bar
Good!
```

It is also possible to test for inequality:

```just
foo := if "hello" != "goodbye" { "xyz" } else { "abc" }

bar:
  @echo {{foo}}
```

```console
$ just bar
xyz
```

And match against regular expressions:

```just
foo := if "hello" =~ 'hel+o' { "match" } else { "mismatch" }

bar:
  @echo {{foo}}
```

```console
$ just bar
match
```

Regular expressions are provided by the
[regex crate](https://github.com/rust-lang/regex), whose syntax is documented on
[docs.rs](https://docs.rs/regex/1.5.4/regex/#syntax). Since regular expressions
commonly use backslash escape sequences, consider using single-quoted string
literals, which will pass slashes to the regex parser unmolested.

Conditional expressions short-circuit, which means they only evaluate one of
their branches. This can be used to make sure that backtick expressions don't
run when they shouldn't.

```just
foo := if env_var("RELEASE") == "true" { `get-something-from-release-database` } else { "dummy-value" }
```

Conditionals can be used inside of recipes:

```just
bar foo:
  echo {{ if foo == "bar" { "hello" } else { "goodbye" } }}
```

Multiple conditionals can be chained:

```just
foo := if "hello" == "goodbye" {
  "xyz"
} else if "a" == "a" {
  "abc"
} else {
  "123"
}

bar:
  @echo {{foo}}
```

```console
$ just bar
abc
```

### Stopping execution with error

Execution can be halted with the `error` function. For example:

```just
foo := if "hello" == "goodbye" {
  "xyz"
} else if "a" == "b" {
  "abc"
} else {
  error("123")
}
```

Which produce the following error when run:

```
error: Call to function `error` failed: 123
   |
16 |   error("123")
```

### Setting Variables from the Command Line

Variables can be overridden from the command line.

```just
os := "linux"

test: build
  ./test --test {{os}}

build:
  ./build {{os}}
```

```console
$ just
./build linux
./test --test linux
```

Any number of arguments of the form `NAME=VALUE` can be passed before recipes:

```console
$ just os=plan9
./build plan9
./test --test plan9
```

Or you can use the `--set` flag:

```console
$ just --set os bsd
./build bsd
./test --test bsd
```

### Getting and Setting Environment Variables

#### Exporting `just` Variables

Assignments prefixed with the `export` keyword will be exported to recipes as
environment variables:

```just
export RUST_BACKTRACE := "1"

test:
  # will print a stack trace if it crashes
  cargo test
```

Parameters prefixed with a `$` will be exported as environment variables:

```just
test $RUST_BACKTRACE="1":
  # will print a stack trace if it crashes
  cargo test
```

Exported variables and parameters are not exported to backticks in the same scope.

```just
export WORLD := "world"
# This backtick will fail with "WORLD: unbound variable"
BAR := `echo hello $WORLD`
```

```just
# Running `just a foo` will fail with "A: unbound variable"
a $A $B=`echo $A`:
  echo $A $B
```

When [export](#export) is set, all `just` variables are exported as environment
variables.

#### Unexporting Environment Variables<sup>1.29.0</sup>

Environment variables can be unexported with the `unexport keyword`:

```just
unexport FOO

@foo:
  echo $FOO
```

```
$ export FOO=bar
$ just foo
sh: FOO: unbound variable
```

#### Getting Environment Variables from the environment

Environment variables from the environment are passed automatically to the
recipes.

```just
print_home_folder:
  echo "HOME is: '${HOME}'"
```

```console
$ just
HOME is '/home/myuser'
```

#### Setting `just` Variables from Environment Variables

Environment variables can be propagated to `just` variables using the `env()` function.
See
[environment-variables](#environment-variables).

### Recipe Parameters

Recipes may have parameters. Here recipe `build` has a parameter called
`target`:

```just
build target:
  @echo 'Building {{target}}…'
  cd {{target}} && make
```

To pass arguments on the command line, put them after the recipe name:

```console
$ just build my-awesome-project
Building my-awesome-project…
cd my-awesome-project && make
```

To pass arguments to a dependency, put the dependency in parentheses along with
the arguments:

```just
default: (build "main")

build target:
  @echo 'Building {{target}}…'
  cd {{target}} && make
```

Variables can also be passed as arguments to dependencies:

```just
target := "main"

_build version:
  @echo 'Building {{version}}…'
  cd {{version}} && make

build: (_build target)
```

A command's arguments can be passed to dependency by putting the dependency in
parentheses along with the arguments:

```just
build target:
  @echo "Building {{target}}…"

push target: (build target)
  @echo 'Pushing {{target}}…'
```

Parameters may have default values:

```just
default := 'all'

test target tests=default:
  @echo 'Testing {{target}}:{{tests}}…'
  ./test --tests {{tests}} {{target}}
```

Parameters with default values may be omitted:

```console
$ just test server
Testing server:all…
./test --tests all server
```

Or supplied:

```console
$ just test server unit
Testing server:unit…
./test --tests unit server
```

Default values may be arbitrary expressions, but expressions containing the
`+`, `&&`, `||`, or `/` operators must be parenthesized:

```just
arch := "wasm"

test triple=(arch + "-unknown-unknown") input=(arch / "input.dat"):
  ./test {{triple}}
```

The last parameter of a recipe may be variadic, indicated with either a `+` or
a `*` before the argument name:

```just
backup +FILES:
  scp {{FILES}} me@server.com:
```

Variadic parameters prefixed with `+` accept *one or more* arguments and expand
to a string containing those arguments separated by spaces:

```console
$ just backup FAQ.md GRAMMAR.md
scp FAQ.md GRAMMAR.md me@server.com:
FAQ.md                  100% 1831     1.8KB/s   00:00
GRAMMAR.md              100% 1666     1.6KB/s   00:00
```

Variadic parameters prefixed with `*` accept *zero or more* arguments and
expand to a string containing those arguments separated by spaces, or an empty
string if no arguments are present:

```just
commit MESSAGE *FLAGS:
  git commit {{FLAGS}} -m "{{MESSAGE}}"
```

Variadic parameters can be assigned default values. These are overridden by
arguments passed on the command line:

```just
test +FLAGS='-q':
  cargo test {{FLAGS}}
```

`{{…}}` substitutions may need to be quoted if they contain spaces. For
example, if you have the following recipe:

```just
search QUERY:
  lynx https://www.google.com/?q={{QUERY}}
```

And you type:

```console
$ just search "cat toupee"
```

`just` will run the command `lynx https://www.google.com/?q=cat toupee`, which
will get parsed by `sh` as `lynx`, `https://www.google.com/?q=cat`, and
`toupee`, and not the intended `lynx` and `https://www.google.com/?q=cat toupee`.

You can fix this by adding quotes:

```just
search QUERY:
  lynx 'https://www.google.com/?q={{QUERY}}'
```

Parameters prefixed with a `$` will be exported as environment variables:

```just
foo $bar:
  echo $bar
```

Parameters may be constrained to match regular expression patterns using the
`[arg("name", pattern="pattern")]` attribute<sup>1.45.0</sup>:

```just
[arg('n', pattern='\d+')]
double n:
  echo $(({{n}} * 2))
```

A leading `^` and trailing `$` are added to the pattern, so it must match the
entire argument value.

You may constrain the pattern to a number of alternatives using the `|`
operator:

```just
[arg('flag', pattern='--help|--version')]
info flag:
  just {{flag}}
```

Regular expressions are provided by the
[Rust `regex` crate](https://docs.rs/regex/latest/regex/). See the
[syntax documentation](https://docs.rs/regex/latest/regex/#syntax) for usage
examples.

Usage information for a recipe may be printed with the `--usage`
subcommand<sup>1.46.0</sup>:

```console
$ just --usage foo
Usage: just foo [OPTIONS] bar

Arguments:
  bar
```

Help strings may be added to arguments using the `[arg(ARG, help=HELP)]` attribute:

```just
[arg("bar", help="hello")]
foo bar:
```

```console
$ just --usage foo
Usage: just foo bar

Arguments:
  bar hello
```

#### Recipe Flags and Options

Recipe parameters are positional by default.

In this `justfile`:

```just
@foo bar:
  echo bar={{bar}}
```

The parameter `bar` is positional:

```console
$ just foo hello
bar=hello
```

The `[arg(ARG, long=OPTION)]`<sup>1.46.0</sup> attribute can be used to make a
parameter a long option.

In this `justfile`:

```just
[arg("bar", long="bar")]
foo bar:
```

The parameter `bar` is given with the `--bar` option:

```console
$ just foo --bar hello
bar=hello
```

Options may also be passed with `--name=value` syntax:

```console
$ just foo --bar=hello
bar=hello
```

The value of `long` can be omitted, in which case the option defaults to the
name of the parameter:

```just
[arg("bar", long)]
foo bar:
```

The `[arg(ARG, short=OPTION)]`<sup>1.46.0</sup> attribute can be used to make a
parameter a short option.

In this `justfile`:

```just
[arg("bar", short="b")]
foo bar:
```

The parameter `bar` is given with the `-b` option:

```console
$ just foo -b hello
bar=hello
```

If a parameter has both a long and short option, it may be passed using either.

Variadic `+` and `?` parameters cannot be options.

The `[arg(ARG, value=VALUE, …)]`<sup>1.46.0</sup> attribute can be used with
`long` or `short` to make a parameter a flag which does not take a value.

In this `justfile`:

```just
[arg("bar", long="bar", value="hello")]
foo bar:
```

The parameter `bar` is given with the `--bar` option, but does not take a
value, and instead takes the value given in the `[arg]` attribute:

```console
$ just foo --bar
bar=hello
```

This is useful for unconditionally requiring a flag like `--force` on dangerous
commands.

A flag is optional if its parameter has a default:

```just
[arg("bar", long="bar", value="hello")]
foo bar="goodbye":
```

Causing it to receive the default when not passed in the invocation:

```console
$ just foo
bar=goodbye
```

### Dependencies

Dependencies run before recipes that depend on them:

```just
a: b
  @echo A

b:
  @echo B
```

```
$ just a
B
A
```

In a given invocation of `just`, a recipe with the same arguments will only run
once, regardless of how many times it appears in the command-line invocation,
or how many times it appears as a dependency:

```just
a:
  @echo A

b: a
  @echo B

c: a
  @echo C
```

```
$ just a a a a a
A
$ just b c
A
B
C
```

Multiple recipes may depend on a recipe that performs some kind of setup, and
when those recipes run, that setup will only be performed once:

```just
build:
  cc main.c

test-foo: build
  ./a.out --test foo

test-bar: build
  ./a.out --test bar
```

```
$ just test-foo test-bar
cc main.c
./a.out --test foo
./a.out --test bar
```

Recipes in a given run are only skipped when they receive the same arguments:

```just
build:
  cc main.c

test TEST: build
  ./a.out --test {{TEST}}
```

```
$ just test foo test bar
cc main.c
./a.out --test foo
./a.out --test bar
```

#### Running Recipes at the End of a Recipe

Normal dependencies of a recipes always run before a recipe starts. That is to
say, the dependee always runs before the depender. These dependencies are
called "prior dependencies".

A recipe can also have subsequent dependencies, which run immediately after the
recipe and are introduced with an `&&`:

```just
a:
  echo 'A!'

b: a && c d
  echo 'B!'

c:
  echo 'C!'

d:
  echo 'D!'
```

…running *b* prints:

```console
$ just b
echo 'A!'
A!
echo 'B!'
B!
echo 'C!'
C!
echo 'D!'
D!
```

#### Running Recipes in the Middle of a Recipe

`just` doesn't support running recipes in the middle of another recipe, but you
can call `just` recursively in the middle of a recipe. Given the following
`justfile`:

```just
a:
  echo 'A!'

b: a
  echo 'B start!'
  just c
  echo 'B end!'

c:
  echo 'C!'
```

…running *b* prints:

```console
$ just b
echo 'A!'
A!
echo 'B start!'
B start!
echo 'C!'
C!
echo 'B end!'
B end!
```

This has limitations, since recipe `c` is run with an entirely new invocation
of `just`: Assignments will be recalculated, dependencies might run twice, and
command line arguments will not be propagated to the child `just` process.

### Shebang Recipes

Recipes that start with `#!` are called shebang recipes, and are executed by
saving the recipe body to a file and running it. This lets you write recipes in
different languages:

```just
polyglot: python js perl sh ruby nu

python:
  #!/usr/bin/env python3
  print('Hello from python!')

js:
  #!/usr/bin/env node
  console.log('Greetings from JavaScript!')

perl:
  #!/usr/bin/env perl
  print "Larry Wall says Hi!\n";

sh:
  #!/usr/bin/env sh
  hello='Yo'
  echo "$hello from a shell script!"

nu:
  #!/usr/bin/env nu
  let hello = 'Hola'
  echo $"($hello) from a nushell script!"

ruby:
  #!/usr/bin/env ruby
  puts "Hello from ruby!"
```

```console
$ just polyglot
Hello from python!
Greetings from JavaScript!
Larry Wall says Hi!
Yo from a shell script!
Hola from a nushell script!
Hello from ruby!
```

On Unix-like operating systems, including Linux and MacOS, shebang recipes are
executed by saving the recipe body to a file in a temporary directory, marking
the file as executable, and executing it. The OS then parses the shebang line
into a command line and invokes it, including the path to the file. For
example, if a recipe starts with `#!/usr/bin/env bash`, the final command that
the OS runs will be something like `/usr/bin/env bash /tmp/PATH_TO_SAVED_RECIPE_BODY`.

Shebang line splitting is operating system dependent. When passing a command
with arguments, you may need to tell `env` to split them explicitly by using
the `-S` flag:

```just
run:
  #!/usr/bin/env -S bash -x
  ls
```

Windows does not support shebang lines. On Windows, `just` splits the shebang
line into a command and arguments, saves the recipe body to a file, and invokes
the split command and arguments, adding the path to the saved recipe body as
the final argument. For example, on Windows, if a recipe starts with `#! py`,
the final command the OS runs will be something like
`py C:\Temp\PATH_TO_SAVED_RECIPE_BODY`.

### Script Recipes

Recipes with a `[script(COMMAND)]`<sup>1.32.0</sup> attribute are run as
scripts interpreted by `COMMAND`. This avoids some of the issues with shebang
recipes, such as the use of `cygpath` on Windows, the need to use
`/usr/bin/env`, inconsistencies in shebang line splitting across Unix OSs, and
requiring a temporary directory from which files can be executed.

Recipes with an empty `[script]` attribute are executed with the value of `set script-interpreter := […]`<sup>1.33.0</sup>, defaulting to `sh -eu`, and *not*
the value of `set shell`.

The body of the recipe is evaluated, written to disk in the temporary
directory, and run by passing its path as an argument to `COMMAND`.

### Script and Shebang Recipe Temporary Files

Both script and shebang recipes write the recipe body to a temporary file for
execution. Script recipes execute that file by passing it to a command, while
shebang recipes execute the file directly. Shebang recipe execution will fail
if the filesystem containing the temporary file is mounted with `noexec` or is
otherwise non-executable.

The directory that `just` writes temporary files to may be configured in a
number of ways, from highest to lowest precedence:

- Globally with the `--tempdir` command-line option or the `JUST_TEMPDIR`
environment variable<sup>1.41.0</sup>.
- On a per-module basis with the `tempdir` setting.
- Globally on Linux with the `XDG_RUNTIME_DIR` environment variable.
- Falling back to the directory returned by
[std::env::temp_dir](https://doc.rust-lang.org/std/env/fn.temp_dir.html).

### Python Recipes with `uv`

[`uv`](https://github.com/astral-sh/uv) is an excellent cross-platform python
project manager, written in Rust.

Using the `[script]` attribute and `script-interpreter` setting, `just` can
easily be configured to run Python recipes with `uv`:

```just
set unstable

set script-interpreter := ['uv', 'run', '--script']

[script]
hello:
  print("Hello from Python!")

[script]
goodbye:
  # /// script
  # requires-python = ">=3.11"
  # dependencies=["sh"]
  # ///
  import sh
  print(sh.echo("Goodbye from Python!"), end='')
```

Of course, a shebang also works:

```just
hello:
  #!/usr/bin/env -S uv run --script
  print("Hello from Python!")
```

### Safer Bash Shebang Recipes

If you're writing a `bash` shebang recipe, consider adding `set -euxo pipefail`:

```just
foo:
  #!/usr/bin/env bash
  set -euxo pipefail
  hello='Yo'
  echo "$hello from Bash!"
```

It isn't strictly necessary, but `set -euxo pipefail` turns on a few useful
features that make `bash` shebang recipes behave more like normal, linewise
`just` recipe:

- `set -e` makes `bash` exit if a command fails.
- `set -u` makes `bash` exit if a variable is undefined.
- `set -x` makes `bash` print each script line before it's run.
- `set -o pipefail` makes `bash` exit if a command in a pipeline fails. This is
`bash`-specific, so isn't turned on in normal linewise `just` recipes.

Together, these avoid a lot of shell scripting gotchas.

#### Shebang Recipe Execution on Windows

On Windows, shebang interpreter paths containing a `/` are translated from
Unix-style paths to Windows-style paths using `cygpath`, a utility that ships
with [Cygwin](http://www.cygwin.com).

For example, to execute this recipe on Windows:

```just
echo:
  #!/bin/sh
  echo "Hello!"
```

The interpreter path `/bin/sh` will be translated to a Windows-style path using
`cygpath` before being executed.

If the interpreter path does not contain a `/` it will be executed without
being translated. This is useful if `cygpath` is not available, or you wish to
pass a Windows-style path to the interpreter.

### Setting Variables in a Recipe

Recipe lines are interpreted by the shell, not `just`, so it's not possible to
set `just` variables in the middle of a recipe:

```justfile
foo:
  x := "hello" # This doesn't work!
  echo {{x}}
```

It is possible to use shell variables, but there's another problem. Every
recipe line is run by a new shell instance, so variables set in one line won't
be set in the next:

```just
foo:
  x=hello && echo $x # This works!
  y=bye
  echo $y            # This doesn't, `y` is undefined here!
```

The best way to work around this is to use a shebang recipe. Shebang recipe
bodies are extracted and run as scripts, so a single shell instance will run
the whole thing:

```just
foo:
  #!/usr/bin/env bash
  set -euxo pipefail
  x=hello
  echo $x
```

### Sharing Environment Variables Between Recipes

Each line of each recipe is executed by a fresh shell, so it is not possible to
share environment variables between recipes.

#### Using Python Virtual Environments

Some tools, like [Python's venv](https://docs.python.org/3/library/venv.html),
require loading environment variables in order to work, making them challenging
to use with `just`. As a workaround, you can execute the virtual environment
binaries directly:

```just
venv:
  [ -d foo ] || python3 -m venv foo

run: venv
  ./foo/bin/python3 main.py
```

### Changing the Working Directory in a Recipe

Each recipe line is executed by a new shell, so if you change the working
directory on one line, it won't have an effect on later lines:

```just
foo:
  pwd    # This `pwd` will print the same directory…
  cd bar
  pwd    # …as this `pwd`!
```

There are a couple ways around this. One is to call `cd` on the same line as
the command you want to run:

```just
foo:
  cd bar && pwd
```

The other is to use a shebang recipe. Shebang recipe bodies are extracted and
run as scripts, so a single shell instance will run the whole thing, and thus a
`cd` on one line will affect later lines, just like a shell script:

```just
foo:
  #!/usr/bin/env bash
  set -euxo pipefail
  cd bar
  pwd
```

### Indentation

Recipe lines can be indented with spaces or tabs, but not a mix of both. All of
a recipe's lines must have the same type of indentation, but different recipes
in the same `justfile` may use different indentation.

Each recipe must be indented at least one level from the `recipe-name` but
after that may be further indented.

Here's a justfile with a recipe indented with spaces, represented as `·`, and
tabs, represented as `→`.

```justfile
set windows-shell := ["pwsh", "-NoLogo", "-NoProfileLoadTime", "-Command"]

set ignore-comments

list-space directory:
··#!pwsh
··foreach ($item in $(Get-ChildItem {{directory}} )) {
····echo $item.Name
··}
··echo ""

# indentation nesting works even when newlines are escaped
list-tab directory:
→ @foreach ($item in $(Get-ChildItem {{directory}} )) { \
→ → echo $item.Name \
→ }
→ @echo ""
```

```pwsh
PS > just list-space ~
Desktop
Documents
Downloads

PS > just list-tab ~
Desktop
Documents
Downloads
```

### Multi-Line Constructs

Recipes without an initial shebang are evaluated and run line-by-line, which
means that multi-line constructs probably won't do what you want.

For example, with the following `justfile`:

```justfile
conditional:
  if true; then
    echo 'True!'
  fi
```

The extra leading whitespace before the second line of the `conditional` recipe
will produce a parse error:

```console
$ just conditional
error: Recipe line has extra leading whitespace
  |
3 |         echo 'True!'
  |     ^^^^^^^^^^^^^^^^
```

To work around this, you can write conditionals on one line, escape newlines
with slashes, or add a shebang to your recipe. Some examples of multi-line
constructs are provided for reference.

#### `if` statements

```just
conditional:
  if true; then echo 'True!'; fi
```

```just
conditional:
  if true; then \
    echo 'True!'; \
  fi
```

```just
conditional:
  #!/usr/bin/env sh
  if true; then
    echo 'True!'
  fi
```

#### `for` loops

```just
for:
  for file in `ls .`; do echo $file; done
```

```just
for:
  for file in `ls .`; do \
    echo $file; \
  done
```

```just
for:
  #!/usr/bin/env sh
  for file in `ls .`; do
    echo $file
  done
```

#### `while` loops

```just
while:
  while `server-is-dead`; do ping -c 1 server; done
```

```just
while:
  while `server-is-dead`; do \
    ping -c 1 server; \
  done
```

```just
while:
  #!/usr/bin/env sh
  while `server-is-dead`; do
    ping -c 1 server
  done
```

#### Outside Recipe Bodies

Parenthesized expressions can span multiple lines:

```just
abc := ('a' +
        'b'
         + 'c')

abc2 := (
  'a' +
  'b' +
  'c'
)

foo param=('foo'
      + 'bar'
    ):
  echo {{param}}

bar: (foo
        'Foo'
     )
  echo 'Bar!'
```

Lines ending with a backslash continue on to the next line as if the lines were
joined by whitespace<sup>1.15.0</sup>:

```just
a := 'foo' + \
     'bar'

foo param1 \
  param2='foo' \
  *varparam='': dep1 \
                (dep2 'foo')
  echo {{param1}} {{param2}} {{varparam}}

dep1: \
    # this comment is not part of the recipe body
  echo 'dep1'

dep2 \
  param:
    echo 'Dependency with parameter {{param}}'
```

Backslash line continuations can also be used in interpolations. The line
following the backslash must be indented.

```just
recipe:
  echo '{{ \
  "This interpolation " + \
    "has a lot of text." \
  }}'
  echo 'back to recipe body'
```

### Command-line Options

`just` supports a number of useful command-line options for listing, dumping,
and debugging recipes and variables:

```console
$ just --list
Available recipes:
  js
  perl
  polyglot
  python
  ruby
$ just --show perl
perl:
  #!/usr/bin/env perl
  print "Larry Wall says Hi!\n";
$ just --show polyglot
polyglot: python js perl sh ruby
```

#### Setting Command-line Options with Environment Variables

Some command-line options can be set with environment variables

For example, unstable features can be enabled either with the `--unstable`
flag:

```console
$ just --unstable
```

Or by setting the `JUST_UNSTABLE` environment variable:

```console
$ export JUST_UNSTABLE=1
$ just
```

Since environment variables are inherited by child processes, command-line
options set with environment variables are inherited by recursive invocations
of `just`, where as command line options set with arguments are not.

Consult `just --help` for which options can be set with environment variables.

### Private Recipes

Recipes and aliases whose name starts with a `_` are omitted from `just --list`:

```just
test: _test-helper
  ./bin/test

_test-helper:
  ./bin/super-secret-test-helper-stuff
```

```console
$ just --list
Available recipes:
    test
```

And from `just --summary`:

```console
$ just --summary
test
```

The `[private]` attribute<sup>1.10.0</sup> may also be used to hide recipes or
aliases without needing to change the name:

```just
[private]
foo:

[private]
alias b := bar

bar:
```

```console
$ just --list
Available recipes:
    bar
```

This is useful for helper recipes which are only meant to be used as
dependencies of other recipes.

### Quiet Recipes

A recipe name may be prefixed with `@` to invert the meaning of `@` before each
line:

```just
@quiet:
  echo hello
  echo goodbye
  @# all done!
```

Now only the lines starting with `@` will be echoed:

```console
$ just quiet
hello
goodbye
# all done!
```

All recipes in a Justfile can be made quiet with `set quiet`:

```just
set quiet

foo:
  echo "This is quiet"

@foo2:
  echo "This is also quiet"
```

The `[no-quiet]` attribute overrides this setting:

```just
set quiet

foo:
  echo "This is quiet"

[no-quiet]
foo2:
  echo "This is not quiet"
```

Shebang recipes are quiet by default:

```just
foo:
  #!/usr/bin/env bash
  echo 'Foo!'
```

```console
$ just foo
Foo!
```

Adding `@` to a shebang recipe name makes `just` print the recipe before
executing it:

```just
@bar:
  #!/usr/bin/env bash
  echo 'Bar!'
```

```console
$ just bar
#!/usr/bin/env bash
echo 'Bar!'
Bar!
```

`just` normally prints error messages when a recipe line fails. These error
messages can be suppressed using the `[no-exit-message]`<sup>1.7.0</sup>
attribute. You may find this especially useful with a recipe that wraps a tool:

```just
git *args:
    @git {{args}}
```

```console
$ just git status
fatal: not a git repository (or any of the parent directories): .git
error: Recipe `git` failed on line 2 with exit code 128
```

Add the attribute to suppress the exit error message when the tool exits with a
non-zero code:

```just
[no-exit-message]
git *args:
    @git {{args}}
```

```console
$ just git status
fatal: not a git repository (or any of the parent directories): .git
```

### Selecting Recipes to Run With an Interactive Chooser

The `--choose` subcommand makes `just` invoke a chooser to select which recipes
to run. Choosers should read lines containing recipe names from standard input
and print one or more of those names separated by spaces to standard output.

Because there is currently no way to run a recipe that requires arguments with
`--choose`, such recipes will not be given to the chooser. Private recipes and
aliases are also skipped.

The chooser can be overridden with the `--chooser` flag. If `--chooser` is not
given, then `just` first checks if `$JUST_CHOOSER` is set. If it isn't, then
the chooser defaults to `fzf`, a popular fuzzy finder.

Arguments can be included in the chooser, i.e. `fzf --exact`.

The chooser is invoked in the same way as recipe lines. For example, if the
chooser is `fzf`, it will be invoked with `sh -cu 'fzf'`, and if the shell, or
the shell arguments are overridden, the chooser invocation will respect those
overrides.

If you'd like `just` to default to selecting recipes with a chooser, you can
use this as your default recipe:

```just
default:
  @just --choose
```

### Invoking `justfile`s in Other Directories

If the first argument passed to `just` contains a `/`, then the following
occurs:

1. The argument is split at the last `/`.
2. The part before the last `/` is treated as a directory. `just` will start
its search for the `justfile` there, instead of in the current directory.
3. The part after the last slash is treated as a normal argument, or ignored
if it is empty.

This may seem a little strange, but it's useful if you wish to run a command in
a `justfile` that is in a subdirectory.

For example, if you are in a directory which contains a subdirectory named
`foo`, which contains a `justfile` with the recipe `build`, which is also the
default recipe, the following are all equivalent:

```console
$ (cd foo && just build)
$ just foo/build
$ just foo/
```

Additional recipes after the first are sought in the same `justfile`. For
example, the following are both equivalent:

```console
$ just foo/a b
$ (cd foo && just a b)
```

And will both invoke recipes `a` and `b` in `foo/justfile`.

### Imports

One `justfile` can include the contents of another using `import` statements.

If you have the following `justfile`:

```justfile
import 'foo/bar.just'

a: b
  @echo A
```

And the following text in `foo/bar.just`:

```just
b:
  @echo B
```

`foo/bar.just` will be included in `justfile` and recipe `b` will be defined:

```console
$ just b
B
$ just a
B
A
```

The `import` path can be absolute or relative to the location of the justfile
containing it. A leading `~/` in the import path is replaced with the current
users home directory.

Justfiles are insensitive to order, so included files can reference variables
and recipes defined after the `import` statement.

Imported files can themselves contain `import`s, which are processed
recursively.

`allow-duplicate-recipes` and `allow-duplicate-variables` allow duplicate
recipes and variables, respectively, to override each other, instead of
producing an error.

Within a module, later definitions override earlier definitions:

```just
set allow-duplicate-recipes

foo:

foo:
  echo 'yes'
```

When `import`s are involved, things unfortunately get much more complicated and
hard to explain.

Shallower definitions always override deeper definitions, so recipes at the top
level will override recipes in imports, and recipes in an import will override
recipes in an import which itself imports those recipes.

When two duplicate definitions are imported and are at the same depth, the one
from the earlier import will override the one from the later import.

This is because `just` uses a stack when processing imports, pushing imports
onto the stack in source-order, and always processing the top of the stack
next, so earlier imports are actually handled later by the compiler.

This is definitely a bug, but since `just` has very strong backwards
compatibility guarantees and we take enormous pains not to break anyone's
`justfile`, we have created issue #2540 to discuss whether or not we can
actually fix it.

Imports may be made optional by putting a `?` after the `import` keyword:

```just
import? 'foo/bar.just'
```

Importing the same source file multiple times is not an error<sup>1.37.0</sup>.
This allows importing multiple justfiles, for example `foo.just` and
`bar.just`, which both import a third justfile containing shared recipes, for
example `baz.just`, without the duplicate import of `baz.just` being an error:

```justfile
# justfile
import 'foo.just'
import 'bar.just'
```

```justfile
# foo.just
import 'baz.just'
foo: baz
```

```justfile
# bar.just
import 'baz.just'
bar: baz
```

```just
# baz
baz:
```

### Modules<sup>1.19.0</sup>

A `justfile` can declare modules using `mod` statements.

`mod` statements were stabilized in `just`<sup>1.31.0</sup>. In earlier
versions, you'll need to use the `--unstable` flag, `set unstable`, or set the
`JUST_UNSTABLE` environment variable to use them.

If you have the following `justfile`:

```justfile
mod bar

a:
  @echo A
```

And the following text in `bar.just`:

```just
b:
  @echo B
```

`bar.just` will be included in `justfile` as a submodule. Recipes, aliases, and
variables defined in one submodule cannot be used in another, and each module
uses its own settings.

Recipes in submodules can be invoked as subcommands:

```console
$ just bar b
B
```

Or with path syntax:

```console
$ just bar::b
B
```

If a module is named `foo`, just will search for the module file in `foo.just`,
`foo/mod.just`, `foo/justfile`, and `foo/.justfile`. In the latter two cases,
the module file may have any capitalization.

Module statements may be of the form:

```justfile
mod foo 'PATH'
```

Which loads the module's source file from `PATH`, instead of from the usual
locations. A leading `~/` in `PATH` is replaced with the current user's home
directory. `PATH` may point to the module source file itself, or to a directory
containing the module source file with the name `mod.just`, `justfile`, or
`.justfile`. In the latter two cases, the module file may have any
capitalization.

Environment files are only loaded for the root justfile, and loaded environment
variables are available in submodules. Settings in submodules that affect
environment file loading are ignored.

Recipes in submodules without the `[no-cd]` attribute run with the working
directory set to the directory containing the submodule source file.

`justfile()` and `justfile_directory()` always return the path to the root
justfile and the directory that contains it, even when called from submodule
recipes.

Modules may be made optional by putting a `?` after the `mod` keyword:

```just
mod? foo
```

Missing source files for optional modules do not produce an error.

Optional modules with no source file do not conflict, so you can have multiple
mod statements with the same name, but with different source file paths, as
long as at most one source file exists:

```just
mod? foo 'bar.just'
mod? foo 'baz.just'
```

Modules may be given doc comments which appear in `--list`
output<sup>1.30.0</sup>:

```justfile
# foo is a great module!
mod foo
```

```console
$ just --list
Available recipes:
    foo ... # foo is a great module!
```

Modules are still missing a lot of features, for example, the ability to refer
to variables in other modules. See the [module improvement tracking
issue](https://github.com/casey/just/issues/2252) for more information.

### Hiding `justfile`s

`just` looks for `justfile`s named `justfile` and `.justfile`, which can be
used to keep a `justfile` hidden.

### Just Scripts

By adding a shebang line to the top of a `justfile` and making it executable,
`just` can be used as an interpreter for scripts:

```console
$ cat > script <<EOF
#!/usr/bin/env just --justfile

foo:
  echo foo
EOF
$ chmod +x script
$ ./script foo
echo foo
foo
```

When a script with a shebang is executed, the system supplies the path to the
script as an argument to the command in the shebang. So, with a shebang of
`#!/usr/bin/env just --justfile`, the command will be `/usr/bin/env just --justfile PATH_TO_SCRIPT`.

With the above shebang, `just` will change its working directory to the
location of the script. If you'd rather leave the working directory unchanged,
use `#!/usr/bin/env just --working-directory . --justfile`.

Note: Shebang line splitting is not consistent across operating systems. The
previous examples have only been tested on macOS. On Linux, you may need to
pass the `-S` flag to `env`:

```just
#!/usr/bin/env -S just --justfile

default:
  echo foo
```

### Formatting and dumping `justfile`s

Each `justfile` has a canonical formatting with respect to whitespace and
newlines.

You can overwrite the current justfile with a canonically-formatted version
using the currently-unstable `--fmt` flag:

```console
$ cat justfile
# A lot of blank lines





some-recipe:
  echo "foo"
$ just --fmt --unstable
$ cat justfile
# A lot of blank lines

some-recipe:
    echo "foo"
```

Invoking `just --fmt --check --unstable` runs `--fmt` in check mode. Instead of
overwriting the `justfile`, `just` will exit with an exit code of 0 if it is
formatted correctly, and will exit with 1 and print a diff if it is not.

You can use the `--dump` command to output a formatted version of the
`justfile` to stdout:

```console
$ just --dump > formatted-justfile
```

The `--dump` command can be used with `--dump-format json` to print a JSON
representation of a `justfile`.

### Fallback to parent `justfile`s

If a recipe is not found in a `justfile` and the `fallback` setting is set,
`just` will look for `justfile`s in the parent directory and up, until it
reaches the root directory. `just` will stop after it reaches a `justfile` in
which the `fallback` setting is `false` or unset.

As an example, suppose the current directory contains this `justfile`:

```just
set fallback
foo:
  echo foo
```

And the parent directory contains this `justfile`:

```just
bar:
  echo bar
```

```console
$ just bar
Trying ../justfile
echo bar
bar
```

### Avoiding Argument Splitting

Given this `justfile`:

```just
foo argument:
  touch {{argument}}
```

The following command will create two files, `some` and `argument.txt`:

```console
$ just foo "some argument.txt"
```

The user's shell will parse `"some argument.txt"` as a single argument, but
when `just` replaces `touch {{argument}}` with `touch some argument.txt`, the
quotes are not preserved, and `touch` will receive two arguments.

There are a few ways to avoid this: quoting, positional arguments, and exported
arguments.

#### Quoting

Quotes can be added around the `{{argument}}` interpolation:

```just
foo argument:
  touch '{{argument}}'
```

This preserves `just`'s ability to catch variable name typos before running,
for example if you were to write `{{argument}}`, but will not do what you want
if the value of `argument` contains single quotes.

#### Positional Arguments

The `positional-arguments` setting causes all arguments to be passed as
positional arguments, allowing them to be accessed with `$1`, `$2`, …, and
`$@`, which can be then double-quoted to avoid further splitting by the shell:

```just
set positional-arguments

foo argument:
  touch "$1"
```

This defeats `just`'s ability to catch typos, for example if you type `$2`
instead of `$1`, but works for all possible values of `argument`, including
those with double quotes.

#### Exported Arguments

All arguments are exported when the `export` setting is set:

```just
set export

foo argument:
  touch "$argument"
```

Or individual arguments may be exported by prefixing them with `$`:

```just
foo $argument:
  touch "$argument"
```

This defeats `just`'s ability to catch typos, for example if you type
`$argument`, but works for all possible values of `argument`, including those
with double quotes.

### Configuring the Shell

There are a number of ways to configure the shell for linewise recipes, which
are the default when a recipe does not start with a `#!` shebang. Their
precedence, from highest to lowest, is:

1. The `--shell` and `--shell-arg` command line options. Passing either of
these will cause `just` to ignore any settings in the current justfile.
2. `set windows-shell := [...]`
3. `set windows-powershell` (deprecated)
4. `set shell := [...]`

Since `set windows-shell` has higher precedence than `set shell`, you can use
`set windows-shell` to pick a shell on Windows, and `set shell` to pick a shell
for all other platforms.

### Timestamps

`just` can print timestamps before each recipe commands:

```just
recipe:
  echo one
  sleep 2
  echo two
```

```
$ just --timestamp recipe
[07:28:46] echo one
one
[07:28:46] sleep 2
[07:28:48] echo two
two
```

By default, timestamps are formatted as `HH:MM:SS`. The format can be changed
with `--timestamp-format`:

```
$ just --timestamp recipe --timestamp-format '%H:%M:%S%.3f %Z'
[07:32:11:.349 UTC] echo one
one
[07:32:11:.350 UTC] sleep 2
[07:32:13:.352 UTC] echo two
two
```

The argument to `--timestamp-format` is a `strftime`-style format string, see
the
[`chrono` library docs](https://docs.rs/chrono/latest/chrono/format/strftime/index.html)
for details.

### Signal Handling

[Signals](https://en.wikipedia.org/wiki/Signal_(IPC)) are messsages sent to
running programs to trigger specific behavior. For example, `SIGINT` is sent to
all processes in the terminal forground process group when `CTRL-C` is pressed.

`just` tries to exit when requested by a signal, but it also tries to avoid
leaving behind running child proccesses, two goals which are somewhat in
conflict.

If `just` exits leaving behind child processes, the user will have no recourse
but to `ps aux | grep` for the children and manually `kill` them, a tedious
endevour.

#### Fatal Signals

`SIGHUP`, `SIGINT`, and `SIGQUIT` are generated when the user closes the
terminal, types `ctrl-c`, or types `ctrl-\`, respectively, and are sent to all
processes in the foreground process group.

`SIGTERM` is the default signal sent by the `kill` command, and is delivered
only to its intended victim.

When a child process is not running, `just` will exit immediately on receipt of
any of the above signals.

When a child process *is* running, `just` will wait until it terminates, to
avoid leaving it behind.

Additionally, on receipt of `SIGTERM`, `just` will forward `SIGTERM` to any
running children<sup>1.41.0</sup>, since unlike other fatal signals, `SIGTERM`,
was likely sent to `just` alone.

Regardless of whether a child process terminates successfully after `just`
receives a fatal signal, `just` halts execution.

#### `SIGINFO`

`SIGINFO` is sent to all processes in the foreground process group when the
user types `ctrl-t` on
[BSD](https://en.wikipedia.org/wiki/Berkeley_Software_Distribution)-derived
operating systems, including MacOS, but not Linux.

`just` responds by printing a list of all child process IDs and
commands<sup>1.41.0</sup>.

#### Windows

On Windows, `just` behaves as if it had received `SIGINT` when the user types
`ctrl-c`. Other signals are unsupported.

