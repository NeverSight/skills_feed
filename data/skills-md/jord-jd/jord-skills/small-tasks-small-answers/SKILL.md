---
name: small-tasks-small-answers
description: Keep answers brief when the user's request is small and straightforward. Use this skill when the user has asked you to do something small/simple, such as making a few wording changes, committing and pushing code, starting a server, doing a simple calculation, or answering a simple yes/no question.
---

Your human doesn't need an essay if they've asked for you to do something small/simple.

# Examples

## Example 1 - Wording changes

You're making some small wording changes to a document, or fixing some typos that the user has already told you about or pointed out.

### Bad

Human: Okay, make those changes.

Assistant: Updated document.md:

* Changed 'but you must' to 'but you have to'.
* Removed the duplicate word on line 42.
* Reworded the sentence in the 'Health' section to be clearer.
* Corrected the spelling of 'accomodate' to 'accommodate'.

### Good

Human: Okay, make those changes.

Assistant: Done!

## Example 2 - Git commit and push

Your human has asked you to commit and push changes you made in a previous turn.

### Bad

Human: Commit and push everything.

Assistant: Committed and pushed to `origin/main`.

- Commit: `d2cb32f Scale up handheld item artwork`
- Full `npm test` suite passed after rebasing
- Local and remote `main` match
- Worktree is clean

### Good

Human: Commit and push everything.

Assistant: Done - Committed and pushed to `main`.

## Example 3 - Start the server

You are starting a server (such as a local development server) for your human.

### Bad

Human: Start the local dev server.

Assistant: Yes - the local development server has now been started via `npm run dev`. You can access it at `http://localhost:3000`. The server is running in development mode, and any changes you make to the code will automatically reload the server.

### Good

Human: Start the local dev server.

Assistant: Done - you can access it at `http://localhost:3000`

## Example 4 - Simple calculations

Your human has asked you to do a simple calculation.

### Bad

Human: What's 15% of 200?

Assistant: 15% of 200 is 30. You can calculate this by multiplying 200 by 0.15, which gives you 30.

### Good

Human: What's 15% of 200?

Assistant: 30

## Example 5 - Simple yes/no questions

Your human has asked you a simple yes/no question.

### Bad

Human: Do we have a fire extinguisher object in the game?

Assistant: Yes. `"fire extinguisher"` is a summonable tool, with `"extinguisher"` as an alias. It sprays water up to 240 units and has its own visual rig. Firefighters also spawn and equip one when responding to fires.

### Good

Human: Do we have a fire extinguisher object in the game?

Assistant: Yes. You can summon them, and firefighters spawn them when responding to fires.

## Example 6 - Counting

Your human has asked you to count the number of things, maybe in a code base or in a document.

### Bad

Human: How many objects do we have in this game in total?

Assistant: The game has **2,477 unique spawnable objects**.

Including aliases and synonyms, players can enter **7,479 noun names**. The full dictionary contains **8,279 accepted strings** when adjectives are included. I confirmed these totals with the current data validator. See [README.md](/home/jordan/git_repos/magic-pad/README.md:70).

### Good

Human: How many objects do we have in this game in total?

Assistant:

* **2,477 unique spawnable objects**
* 7,479 noun names if you include aliases/synonyms
* 8,279 accepted strings if you include adjectives
