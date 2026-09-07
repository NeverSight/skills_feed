---
name: herdr-delegation
description: Delegate bounded implementation through Herdr when authorized by the user or applicable project policy. Requires HERDR_ENV=1 and covers pane setup, Pi execution, workstream isolation, verification, and review.
---

# Herdr Delegation

## Preconditions

1. Resolve authorization under the applicable instruction hierarchy. Follow explicit project delegation policy; otherwise require an explicit user request for Herdr.
2. Confirm that `HERDR_ENV=1`. If not, tell the user Herdr is unavailable and stop this path.
3. Complete code exploration with normal read-only tools before Herdr implementation begins.
4. Keep Herdr and internal-subagent delegation separate within a workstream unless the user explicitly requests the combination.

The preflight is complete when the request, environment, implementation scope, and execution mode are all explicit.

## Execution

1. Create a fresh pane with `herdr_layout` for each new delegated workstream. Default to a sibling pane in the caller's tab and working directory; if the user names a workspace, create the pane there. Preserve focus unless the user asks otherwise. Reuse a pane only when it was created for the same workstream or the user explicitly identifies that pane or agent for reuse. An idle agent is not permission to reuse its pane, and naming a workspace does not authorize messaging its existing agents. Before sending a prompt, verify that the target pane meets one of these conditions.
2. Use Herdr only for implementation. Split panes only for independent workstreams or when the user explicitly requests multiple panes.
3. Start `pi` through `herdr_agent` using the implementation model and reasoning effort from the applicable configuration and project policy. Honor explicit user choices within the instruction hierarchy; do not impose a skill-specific maximum effort.
4. Give each pane a bounded scope, relevant context, observable success criteria, expected verification, and explicit file ownership. Use isolated checkouts if concurrent modifications could overlap. Require workers to preserve changes outside their assignment.
5. Include this restriction in every worker brief: work directly within the assigned scope; do not spawn agents, launch workflows, create panes, or delegate through any mechanism. Return blockers and requests for additional workers to the main thread.
6. Require each pane to report its changes and verification to the main thread.
7. Review the actual changes and checks. Send required corrections to the same pane before accepting its work.

Leave panes you did not create open unless the user asks to close them.

## Completion

The Herdr work is complete when every assigned workstream has reported, the main thread has inspected its actual changes, relevant checks pass, and required revisions are resolved.
