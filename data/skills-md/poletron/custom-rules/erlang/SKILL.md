---
name: erlang
description: >
  Erlang/OTP patterns for concurrent and fault-tolerant systems.
  Trigger: When writing Erlang/OTP applications.
license: Apache-2.0
metadata:
  author: poletron
  version: "1.0"
  scope: [root]
  auto_invoke: "Working with erlang"

## When to Use

Use this skill when:
- Building concurrent systems with Erlang
- Implementing OTP behaviors
- Creating fault-tolerant supervisors
- Working with message passing

---

## Critical Patterns

### OTP GenServer (REQUIRED)

```erlang
-module(counter).
-behaviour(gen_server).
-export([start_link/0, increment/0, get/0]).
-export([init/1, handle_call/3, handle_cast/2]).

start_link() ->
    gen_server:start_link({local, ?MODULE}, ?MODULE, [], []).

init([]) -> {ok, 0}.

handle_call(get, _From, State) ->
    {reply, State, State}.

handle_cast(increment, State) ->
    {noreply, State + 1}.
```

### Supervisor (REQUIRED)

```erlang
-module(my_sup).
-behaviour(supervisor).
-export([start_link/0, init/1]).

start_link() ->
    supervisor:start_link({local, ?MODULE}, ?MODULE, []).

init([]) ->
    SupFlags = #{strategy => one_for_one, intensity => 5, period => 10},
    Children = [
        #{id => worker, start => {my_worker, start_link, []}}
    ],
    {ok, {SupFlags, Children}}.
```

---

## Decision Tree

```
Need request/response?     → Use gen_server call
Need fire-and-forget?      → Use gen_server cast
Need supervision?          → Use supervisor behavior
Need state machine?        → Use gen_statem
Need event handling?       → Use gen_event
```

---

## Commands

```bash
erl                         # Start REPL
erlc module.erl            # Compile
rebar3 compile             # Build project
rebar3 shell               # Interactive shell
```

---

## Resources

- **Concurrent Programming**: [concurrent-programming.md](concurrent-programming.md)
- **Fault Tolerance**: [fault-tolerance.md](fault-tolerance.md)
- **OTP Patterns**: [otp-patterns.md](otp-patterns.md)
