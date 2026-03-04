---
name: problem-diagnosis
description: Use when animation "feels wrong" but you can't pinpoint why—debugging floaty movement, stiff characters, unclear action, or any motion that isn't working and needs systematic troubleshooting.
---

# Problem Diagnosis

Think like a doctor examining symptoms. Something feels wrong. Your job is to identify the specific principle being violated and prescribe the cure. Systematic diagnosis beats random fixes.

## Core Mental Model

When animation feels off, ask: **What principle is being violated, and how?**

"It doesn't look right" isn't actionable. The 12 principles are your diagnostic checklist. Every animation problem is a principle problem—find which one, and the solution becomes clear.

## Diagnostic Framework

### Symptom: "Floaty" or "Weightless"
**Likely Causes:**
- Missing slow-in/slow-out (objects should accelerate with gravity)
- Insufficient anticipation before jumps
- No squash on landing impacts
- Timing too uniform (everything same speed)
- Missing secondary weight (hair/clothing not responding to gravity)

**Fixes:**
1. Add ease-in at motion start
2. Add squash frames at impact points
3. Include settling oscillations after stops
4. Vary timing based on mass

### Symptom: "Stiff" or "Robotic"
**Likely Causes:**
- Missing arcs (linear interpolation instead of curves)
- No overlapping action (all parts move together)
- Twinning (left and right doing identical things)
- No secondary action
- Timing too uniform

**Fixes:**
1. Add arc curves to all motion paths
2. Offset timing of connected body parts
3. Break symmetry in poses
4. Add breathing and weight shifts
5. Include micro-movements

### Symptom: "Unclear" or "Hard to Read"
**Likely Causes:**
- Poor staging (elements overlap confusingly)
- Weak silhouettes
- Insufficient anticipation (action comes from nowhere)
- Not enough exaggeration
- Competing attention points

**Fixes:**
1. Simplify background during key action
2. Push poses to clear silhouettes
3. Extend anticipation timing
4. Increase exaggeration 20%
5. Reduce secondary action during primary beats

### Symptom: "Boring" or "Lifeless"
**Likely Causes:**
- No appeal in character posing
- Timing lacks contrast (no fast vs. slow)
- Missing anticipation-payoff structure
- Insufficient exaggeration
- No secondary action or texture

**Fixes:**
1. Push personality in poses
2. Create timing contrast (faster fasts, slower slows)
3. Add clear anticipation beats
4. Increase exaggeration of key poses
5. Layer in secondary movement

### Symptom: "Cartoony" (Unintentionally)
**Likely Causes:**
- Excessive squash and stretch
- Over-exaggerated timing
- Physics violations too extreme
- Follow-through too elastic

**Fixes:**
1. Reduce squash/stretch to 10-20% range
2. Add more frames to smooth extremes
3. Ground with realistic settling time
4. Pull back follow-through delay

### Symptom: "Too Fast" / "Too Slow"
**Likely Causes:**
- Frame count mismatch with intention
- Missing ease-in or ease-out
- Key poses not held long enough
- Anticipation/payoff imbalance

**Fixes:**
1. Adjust frame count (add/remove in-betweens)
2. Check easing curves
3. Hold key poses 2-4 more frames
4. Rebalance anticipation vs. action timing

## Diagnostic Process

1. **Identify the symptom** — Name what's wrong in plain terms
2. **Isolate the problem** — Is it the whole scene or specific moments?
3. **Check principles systematically:**
   - Timing and spacing?
   - Squash and stretch?
   - Anticipation and follow-through?
   - Arcs?
   - Staging?
   - Exaggeration level?
   - Secondary action?
4. **Test hypothesis** — Make one change, evaluate
5. **Iterate** — If unfixed, try next most likely principle

## The Golden Rule

**One fix at a time.** Animation problems often have multiple causes, but changing everything at once makes it impossible to learn what worked. Diagnose, treat one principle, evaluate, repeat.
