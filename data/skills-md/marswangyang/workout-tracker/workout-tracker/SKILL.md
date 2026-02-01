---
name: workout-tracker
description: Tracks fitness workouts (reps, sets, weight) using a local SQLite database and smart scripts. Supports image recognition for equipment.
---

# Workout Tracker

A skill to log and track fitness activities using a local SQLite database.

## Capabilities

1.  **Log Workout:** Record exercise details.
2.  **View History:** See past performance.
3.  **Smart Rest Time:** Auto-fills rest time based on previous sessions if not provided.
4.  **Visual Recognition:** Can identify gym equipment from images to suggest exercises.

## Usage

### 1. Logging a Workout

When the user says "I did 5 sets of Bench Press at 60kg for 8 reps", parse the details and run:

```bash
cd skills/workout-tracker/scripts && uv run log.py \
  --exercise "Bench Press" \
  --weight 60 \
  --unit kg \
  --sets 5 \
  --reps 8 \
  --body_part "Chest" \
  --rest_time 90  # Optional: User provided or leave empty to auto-fill
  --notes "Optional notes"
```

**Parameters:**
- `--exercise` (Required): Name of the movement.
- `--body_part`: **(New)** Target muscle group (e.g. Chest, Back, Legs). **INFER THIS** from the exercise if not provided (e.g. Bench -> Chest).
- `--weight` (Required): Weight value.
- `--unit`: 'kg' or 'lb' (default kg).
- `--sets`: Number of sets.
- `--reps`: Reps per set.
- `--rest_time`: Seconds. **OMIT THIS if the user didn't specify.** The script will auto-fill from history.

### 2. Viewing History

When the user asks "How is my Squat progress?" or "Show last workouts":

```bash
cd skills/workout-tracker/scripts && uv run render.py --exercise "Squat"
```
**Then send the generated image:**
`message(action="send", filePath="/tmp/workout_report.png", message="Here is your report:")`

### 3. Image Recognition (Vision)

If the user uploads an image (e.g., of a machine):
1.  **Analyze the image** using your vision capabilities.
2.  **Identify the equipment** (e.g., "Leg Press Machine", "Dumbbells").
3.  **Ask the user:** "This looks like a Leg Press. Do you want to log a set? How much weight?"
4.  Once they reply, use the `log.py` script as usual.

## Design & Behavior Rules (User Preferences)

### 1. User Profile
- **Type:** General User (Casual).
- **Interaction:** Use natural language. **Automatically infer** the `body_part` from the exercise name (e.g., "Bench Press" -> "Chest") without asking, unless ambiguous.

### 2. Display Format (Mobile Portrait)
- **Preferred Output:** Always generate an **Image** for reports using `render.py`.
- **Style:** Vertical (Portrait) aspect ratio optimized for mobile screens.
- **Layout:**
  - Narrow width (`figsize` width ~6).
  - Wrap long text in "Notes" column.
  - Hide "Exercise" column if filtering by a single exercise (title context is enough).
  - Sort chronologically (Oldest -> Newest) within the day/session.

### 3. Logging Logic
- **Drop Sets:** Must be logged as **separate rows** for data accuracy.
  - **Rest Time:** Set to `0` between drop set segments.
  - **Notes:** Mark as "Drop set part X/Y" for clarity.
- **Units:** User prefers **lb** (pounds).

## Database

Data is stored in `skills/workout-tracker/workout.db` (SQLite).
The schema includes `date`, `exercise`, `weight`, `unit`, `sets`, `reps`, `rest_time`, `notes`.

## Technical Setup (Maintenance)

This skill uses **uv** for Python package management.

### Installation

1.  Ensure `uv` is installed: `brew install uv`
2.  Sync dependencies:
    ```bash
    cd skills/workout-tracker/scripts
    uv sync
    ```

### Database Schema (SQLModel)

The SQLite database (`workout.db`) uses the following schema:
- `id`: Integer (PK)
- `date`: ISO8601 String
- `exercise`: String
- `body_part`: String (Target muscle group)
- `weight`: Float
- `unit`: String (default "kg")
- `sets`: Integer
- `reps`: Integer
- `rest_time`: Integer (Seconds, optional)
- `notes`: String (Optional)
