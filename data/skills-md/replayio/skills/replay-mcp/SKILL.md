---
name: replay-mcp
description: Use Replay MCP to inspect the contents of https://replay.io recordings.
allowed-tools: Bash(replayio:*), mcp__replay
---

# Overview

This document provides an overview of the tools available when using Replay MCP
and how to use these tools to investigate recordings.

Replay MCP is used to inspect the contents of https://replay.io recordings.
These recordings perfectly capture everything that happened when a browser
visited an app or other web page. You can explore and investigate the app's behavior
as if you are a detective with a time machine.

Any question about the app behaved can be answered precisely using data from the
recording. The most important thing to remember when using Replay MCP to investigate
a recording is to not jump to conclusions:

1. Frame your task in the form of a question that you need to answer.
1. Use exploratory tools to identify things that happened in the recording related
   to the question.
2. Use explanatory tools to understand why those things happened.
3. Form a hypothesis and identify data you gathered which justifies that hypothesis.
4. Explain the answer referring to the data supporting your conclusion.

## Terms

The recording is essentially a gigantic database containing everything that happened
while the app executed. A couple terms are useful for understanding this database:

* Point: A specific point in the execution of the app. There is a unique point created
for every time a JS statement executes or any other interesting event with potential
side effects on the app's state.

* Element: A reference for a particular DOM element that is independent of any particular point.
Each DOM element has a lifetime for some portion of the recording.

# Exploratory Tools

Exploratory tools are used to discover what happened in the recording and when.

## Errors

Error tools identify major errors that occurred in the app which may cause it to break.

* UncaughtException: An exception was thrown and not caught by anything.
* ReactException: An exception was thrown while rendering a React component, causing the tree to unmount.

## Timeline

Timeline tools describe sequences of events for what happened across the recording.

* Timeline: Combines data from other timeline tools to show interesting events in order.
* ConsoleMessages: Shows all messages logged to the console.
* LocalStorage: Shows all accesses made to local storage.
* NetworkRequest: Shows all network requests made, or details about a specific request.
* ReactRenders: Shows all React renders and the rendered components.

## Sources

Source tools get information about the JS sources in the app and what code executed.
When showing source code in these and other tools, hit counts are shown for each line.
A blank value is used for lines that have no breakpoints.

* ListSources: Find source files by name.
* ReadSource: Read the contents of a source and show what code executed.
* SearchSources: Search the contents of all sources for a pattern and show what code executed.

# Explanatory Tools

Explanatory tools are used to understand why particular things happened in the recording.

## Dependencies

Dependency tools track happens-before relationships between events in the recording.
This is useful to understand why particular events happened or didn't happen.

* GetStack: Show the on stack frames at a point.
* ControlDependency: Describe the events in a recording that triggered execution of a point.

## Details

Detail tools show additional details about the app's state at particular points.

* DescribePoint: Describe a point's location and variable values.
* InspectElement: Describe a DOM element's details.
* ReactComponents: Describe the React component tree at a point.
* Logpoint: Show the points and values of an expression every time a statement executed.
* Evaluate: Evaluate an expression at a particular point.

# Tips

When understanding JS behavior it is a good idea to find code relevant to the question being answered,
see whether that code executed at all, and get details about the times when it executed.
The Logpoint tool is extremely useful for this: see the value of the same expression whenever a
statement executed, look for anything unexpected, and continue investigating from there.

When understanding the timing around a particular event (e.g. why it happened later than desired),
find a point in the recording associated with the event and use the ControlDependency tool to explore
the events that had to happen first and any associated delays.
