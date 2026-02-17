---
name: wilma-triage
version: 1.0.1
description: Daily triage of Wilma school notifications for Finnish parents. Fetches exams, messages, news, schedules, and homework — filters for actionable items, syncs exams to Google Calendar, and reports via chat. Requires the `wilma` skill and `gog` CLI (or `gog` skill from ClawHub) for calendar access.
metadata:
  {
    "openclaw":
      {
        "requires":
          {
            "bins": ["wilma", "gog"],
            "skills": ["wilma"],
            "configPaths":
              [
                "~/.config/wilmai/config.json",
                "~/Library/Application Support/gogcli/",
              ],
          },
        "credentials":
          {
            "note": "Requires local Wilma credentials (~/.config/wilmai/config.json) for school data access and gog CLI auth (Google OAuth) for calendar sync. Both must be set up interactively before use.",
          },
      },
  }
---

# Wilma Triage

Automated daily triage of Wilma school data for parents. Filters noise, surfaces actionable items, and syncs exams/events to Google Calendar.

## Dependencies

- **wilma skill** — install from ClawHub (`clawhub install wilma`) for Wilma CLI commands and setup
- **gog skill** — install from ClawHub (`clawhub install gog`) for Google Calendar sync

## First Run Setup

On first use, collect and store configuration:

1. **Discover kids:** Run `wilma kids list --json` to get student names, numbers, and schools
2. **Calendar ID:** Run `gog calendar calendars` to list available calendars. Ask the user which calendar to use for school events. Store the calendar ID in **TOOLS.md** under a `## Wilma Triage` section along with naming conventions for events.
3. **Preferences:** Ask about any kid-specific rules (e.g., subject overrides like ET instead of religion). Store in **MEMORY.md** as part of the Wilma triage context.

Over time, the user will give feedback on what to report and what to skip — store these preferences in MEMORY.md. The triage gets smarter with use.

## Workflow

1. **Fetch data** — check TOOLS.md for student details, then start with summary:
   ```bash
   # Best starting point — returns schedule, exams, homework, news, messages
   wilma summary --all-students --json

   # Drill into specifics as needed
   wilma exams list --all-students --json
   wilma schedule list --when today --all-students --json
   wilma schedule list --when tomorrow --all-students --json
   wilma homework list --all-students --limit 10 --json
   wilma grades list --all-students --limit 5 --json
   wilma messages list --all-students --limit 10 --json
   wilma news list --all-students --limit 10 --json

   # Read full content when subject line looks actionable
   wilma messages read <id> --student <name> --json
   wilma news read <id> --student <name> --json
   ```

2. **Filter** — apply triage rules below plus any kid-specific rules from MEMORY.md

3. **Calendar sync** — add missing exams and actionable events using gog CLI commands from TOOLS.md
   - **ALWAYS check for existing events before adding** to avoid duplicates
   - Use naming conventions stored in TOOLS.md
   - Remove cancelled events from calendar

4. **Report** — if actionable items found, send details. If nothing actionable, stay silent or send a brief confirmation. Check MEMORY.md for the user's notification preference.

## Calendar Sync

Refer to TOOLS.md for the calendar ID, naming conventions, and exact gog CLI commands.

**NO DUPLICATES rule:**
1. Before adding any event, check calendar for that date range
2. If a matching event exists (same date + child + subject keywords), skip it
3. Only add if not already there

## Understanding Wilma Messages

Wilma messages come from different sources and have very different signal-to-noise ratios. Knowing the difference is critical for good triage:

- **Viikkoviesti / weekly letter** (from class teacher) — **HIGH VALUE.** These are the class teacher's weekly updates. They look like casual newsletters but frequently contain buried actionable items: upcoming exams, materials to bring, schedule changes, field trips, deadlines. **Always read the full content.** Never skip based on subject line.
- **Teacher messages** (from subject teachers) — Usually about specific exams, homework, or class events. High signal.
- **School office / rehtori messages** — Administrative: schedule changes, events, policy updates. Medium signal — skim for actions.
- **Kuukausitiedote / monthly newsletter** (from school office) — **Read these.** They typically contain important dates: holidays, school year start/end, event schedules, enrollment deadlines. Don't skip based on the generic subject line.
- **City-wide notices** (from Helsinki/municipality) — Health campaigns, transport info, surveys. Usually noise for daily triage. Skim subject, skip unless clearly actionable.
- **Parent union / vanhempainyhdistys** — Low signal by default (fundraising, volunteer calls). However, check MEMORY.md — if the parent is actively involved in the union, these become high priority.

**Rule of thumb:** If a message is from a teacher (class teacher or subject teacher), always read it. If it's from the school office or city, skim the subject and skip unless it's clearly actionable.

## Triage Rules

### Always Report (Actionable)
- Forms, permission slips, replies needed
- Deadlines (sign-ups, payments, materials to bring)
- Schedule changes (early dismissal, cancelled classes, substitute arrangements)
- Special gear/materials needed (e.g., "bring ski gear", "outdoor clothing")
- After-school events kids might want to attend (discos, movie nights)
- Exam schedule updates or new exams
- Cancelled events that are on the calendar → remove them

### Report Briefly (Worth Mentioning)
- Field trips, themed days with date info
- School closures, holiday schedule changes
- Health notices (lice alerts, illness outbreaks)
- New grades (brief mention with grade)

### Important: Always Read Weekly Letters (viikkoviesti)
Weekly letters from class teachers often contain actionable items buried in the text: exams, materials to bring, schedule changes, field trips. **Always read the full content** of viikkoviesti messages — do not skip based on subject line alone.

### Skip Silently
- Concerts, cultural performances (FYI only)
- Generic "welcome back" or seasonal greetings
- City-wide informational notices (health campaigns, transport info, surveys)
- Parent union messages (unless user is actively involved — check MEMORY.md)

**Check MEMORY.md for additional skip/report rules** the user has provided over time (e.g., subject overrides, school-specific filtering).

## Suggested Cron Setup

Run daily at 07:00 local time as an isolated agentTurn job:

```
Schedule: 07:00 daily
Timeout: 180s
Task: "Read the wilma-triage skill, then run the full triage workflow. Report actionable findings."
```

Stagger with other morning jobs (e.g., email check at 07:05) to avoid API rate limits.

## Output Format Example

```
📚 Wilma Update

Child A (8th grade)
• Math exam tomorrow — yhtälöt, kpl 1-8
• Friday short day (9:20-12:35) — kulttuuripäivä, bring laptop + outdoor clothes

Child B (6th grade)
• No actionable items

📅 Calendar: Added Child A math exam (Feb 10), removed cancelled disco (Feb 11)
```

Keep it brief. One line per item. Silence is better than noise.
