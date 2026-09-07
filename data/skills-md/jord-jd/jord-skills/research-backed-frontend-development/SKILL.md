---
name: research-backed-frontend-development
description: "Apply before creating, changing, or reviewing any frontend or user interface, including websites, apps, games, desktop software, kiosks, and embedded displays for ESP32, Arduino, or other devices. Research real comparable interfaces online: inspect screens, flows, game footage, device manuals, and screenshots before choosing a direction. Use that evidence to plan, build, and visually verify an original interface with exceptional visual quality, suited to its users, display, controls, and system constraints."
---

# Research-backed interface development

Build the interface in front of you, not a generic version of its category. Research how real products solve the same user problem, understand why their interfaces work, then make an original design whose controls, visible states, and underlying system agree.

Visual quality is a core deliverable. Aim for an interface that is immediately striking, coherent in every state, and recognisably specific to the product. A correct but generic interface is unfinished. Visual ambition never excuses unreadable information, inaccessible controls, poor performance, or unsafe behaviour.

This skill applies to any interface a person sees or controls. Websites, native apps, game HUDs, menus, touchscreens, command consoles, instrument panels, appliances, kiosks, OLED and LCD modules, and LED or button-driven devices are examples, not boundaries.

The normal sequence is:

1. Understand the medium, the user, and the job.
2. Research comparable interfaces online.
3. Synthesize the evidence.
4. Set an original interface direction.
5. Define the UI/system contract.
6. Build complete interaction slices.
7. Test behaviour and inspect the rendered interface.
8. Report the evidence, implementation, and verification.

Match the later steps to the user's request. For review-only work, research, inspect, verify, and report without changing the project. For design-only work, stop after the direction and contract. This skill does not authorise changes to the system behind the interface unless they are part of the assignment.

Do not design from memory when real examples are available. Do not start coding because the first plausible layout came to mind.

## 1. Understand the medium and the job

Read the user's brief, the project instructions, and the relevant code or hardware documentation before proposing a direction. Work out:

- the product or subject;
- the intended users and the main job they need to finish;
- the conditions in which they use it, including distance, lighting, motion, noise, time pressure, gloves, or shared use when relevant;
- the target medium, display hardware, resolution, orientation, colour depth, and viewing distance;
- the input and output methods, such as pointer, keyboard, touch, controller, buttons, rotary encoder, voice, LEDs, sound, or haptics;
- the required screens, modes, states, data, and integrations;
- the existing framework, game engine, UI toolkit, firmware stack, component system, and visual language;
- accessibility, memory, performance, power, latency, offline, and safety constraints;
- what the user has already decided, including brand rules and technical limits.

Inspect the repository and target specifications before choosing a new library or architecture. Preserve the existing stack unless the task gives a concrete reason to change it. Existing user changes are part of the working context.

If the brief leaves the subject, audience, or target hardware open, choose a specific, plausible answer and state the assumption. Ask only when different answers would lead to materially different interfaces and the context cannot resolve the choice.

## 2. Research comparable interfaces

Research is required for interface work. Scale the depth to the task. Inspect at least three relevant interfaces for a new product, screen, or flow. One or two focused references may be enough for a small change. When an interface already exists, inspect its current state before looking elsewhere.

Search is only discovery. Use the browser to open the actual product or the best available evidence of it. Before the first browser action, read and follow the available browser-safety instructions, such as `polite-browser-use`. Do not enter private areas, create accounts, start trials, or submit data unless the user has authorised it. Close tabs and stop test processes when the work is finished.

### Choose useful comparisons

Include whichever comparisons expose the real design problem:

- direct alternatives used for the same job and in the same medium;
- products with similar controls, display limits, or usage conditions;
- adjacent products that solve the same interaction or information problem;
- a strong reference outside the category when it offers a useful pattern the direct alternatives lack.

At least one reference should earn its place because its visual execution is exceptional, even if it sits outside the product category. Functional competitors can teach conventions, but a group of bland competitors sets a low ceiling.

Prefer live products, interactive demos, official screenshots, manuals, app-store pages, game footage, device footage, source repositories, and detailed reviews. Design galleries, award pages, templates, and search-result thumbnails show isolated frames without proving how an interface works.

A website can be researched through its live pages. A game may require game footage and screenshots of HUDs, menus, inventories, or other states. A hardware interface may require its manual, product videos, emulator, firmware repository, or close-up photos of the display and controls. If the real product is inaccessible, say which evidence you used instead.

### Inspect, capture, and record

For each reference:

1. Open the relevant product, demo, recording, manual, or image source.
2. Examine the screens, physical controls, states, and transitions that matter to the task.
3. Capture focused screenshots or video frames at useful states and sizes. Use emulator captures, render captures, or device photos when the target is not browser-based.
4. Open and inspect every capture. Taking a screenshot without looking at it is not research.
5. Record the source URL, product and state, access date, and screenshot path.
6. Write down what was observed separately from what was inferred.

Pay attention to:

- navigation, hierarchy, grouping, density, and the order in which information appears;
- the mapping between controls and results, including focus, selection, shortcuts, back behaviour, and accidental activation;
- layout behaviour across screen sizes, orientations, safe areas, resolutions, and fixed pixel grids;
- legibility at the real physical size and viewing distance;
- composition, focal point, visual rhythm, density, layering, image treatment, and the details that make the strongest frames feel finished;
- typography, colour or monochrome roles, spacing, borders, icons, imagery, animation, sound, haptics, and indicator lights;
- forms, menus, inventories, HUD elements, gauges, alerts, settings, search, filters, and destructive actions when present;
- startup, onboarding, loading, empty, success, error, warning, disconnected, offline, sleep, and recovery states;
- response time and the feedback shown while software, a network, a sensor, or a physical mechanism catches up;
- accessibility, platform conventions, redundant warnings, and safety-related behaviour;
- signs of the underlying system, such as entities, permissions, device modes, persistence, sensor states, connectivity, timing, power loss, and hardware faults.

A compact evidence table is usually enough:

| Reference | Screen, state, or control | Screenshot | Observed pattern | System implication | Keep, adapt, or avoid |
| --- | --- | --- | --- | --- | --- |

Label system implications as inferences unless the product documents them. A visible delay may imply asynchronous work. It does not reveal whether the product uses a queue, a thread, a network request, or a slow sensor.

Screenshots are research evidence, not permission to reuse another product's art, copy, logo, or distinctive composition. Learn the conventions people depend on, then make a design that belongs to this product.

If web or browser access is unavailable, use supplied screenshots, recordings, manuals, local builds, emulators, and hardware documentation. Say what could not be inspected. Never invent sources, observations, or screenshots.

## 3. Synthesize before designing

Turn the research into decisions. A useful synthesis names:

- the conventions shared by several references and why users may expect them;
- the strongest solution to each important interaction problem;
- recurring weaknesses, clutter, hidden modes, or confusing states to avoid;
- gaps where this product can be clearer or easier to control;
- the visual benchmark the finished interface should meet, with specific reference frames and the qualities worth matching;
- the software, service, or hardware capabilities implied by the desired experience;
- which findings apply to this medium and which do not.

Then write a short product direction with one concrete audience, one primary job, the usage conditions, the main journeys, and the states each journey can enter. If the evidence contradicts the initial idea, revise the idea. Do not collect screenshots merely to justify a decision already made.

## 4. Set an original interface direction

The subject's own language, tools, materials, data, controls, and working environment should drive the design. References show what people understand. They do not choose the product's identity.

State the visual ambition in one concrete sentence before planning the parts. Name what the strongest finished screenshot or device view should make memorable and which parts of the subject justify that choice.

Create a compact plan before coding:

- **Art direction:** Describe the visual world and the subject-specific source of its shapes, materials, imagery, or atmosphere.
- **Visual system:** Choose a palette suited to the display, whether that means named web colours, a limited game palette, a monochrome OLED, or a few LED states. Give each value a job.
- **Type and symbols:** Choose readable type, numerals, icons, and status symbols for the available pixels, physical size, language, and viewing distance.
- **Layout:** Sketch the main screens and transitions with short prose, ASCII wireframes, or exact pixel maps for fixed displays.
- **Imagery and assets:** Decide whether the direction needs photography, illustration, texture, custom icons, game art, or display-specific graphics. Use purpose-made assets when generic placeholders would weaken the result.
- **Interaction:** Define how pointer, touch, keyboard, controller, buttons, or encoders move focus and trigger actions.
- **Structure:** Use labels, dividers, grouping, modes, and indicators to communicate real relationships and state.
- **Feedback:** Decide where visual change, motion, sound, haptics, or LEDs confirm input and show progress.
- **Signature:** Choose one unmistakable element or moment tied to the subject when the medium has room for it.

Do not confuse restraint with ordinariness. A minimal interface needs precise type, spacing, proportion, alignment, and state changes. An expressive interface needs enough custom execution to make its art direction believable. Match the amount of detail to the idea.

The default screen should express the product's main job. That could be a marketing hero, a useful app state, a readable HUD, a device status screen, or one unambiguous indicator.

For an expressive interface, take one aesthetic risk that you can explain from the brief or research. Keep everything around it disciplined. On a tiny, safety-related, or highly constrained interface, put character where it cannot obscure state or controls. Clarity wins.

Critique the plan before building. Ask:

- Could this direction be pasted onto an unrelated product with only the name changed?
- Did the palette, type, layout, or HUD fall back to a fashionable default without a reason?
- Would the strongest planned frame hold up beside the best visual reference, without copying it?
- Does every major visual choice support the same art direction?
- Can someone understand the control mapping without guessing?
- Is it readable at its real resolution, physical size, distance, and lighting?
- Does the signature element help the task or express something true about the subject?
- Is any decoration pretending to be information?
- Does the design follow the user's brief, platform conventions, and safety requirements where those outweigh the references?

Revise the weak choices now. Code is an expensive place to discover that the direction is generic or the interaction model does not fit the hardware.

## 5. Define the UI/system contract

Map each important journey as an interaction slice:

```text
human input
  -> immediate visual, audible, or physical feedback
  -> UI state transition
  -> application, engine, firmware, device, or service operation
  -> validation, permission, or safety check
  -> data, network, sensor, or hardware result
  -> visible state and recovery path
```

Omit stages that do not exist. A static page may have no operation. A local game menu may have no server. An embedded controller may have no conventional backend.

Define what the task needs:

- UI states, transitions, modes, invariants, and impossible combinations;
- input events, long presses, repeats, shortcuts, focus rules, and debounce behaviour;
- the data model and application, engine, firmware, device, or service interfaces that drive the UI;
- inputs, outputs, errors, timing, and ownership at each boundary;
- validation, permissions, safety interlocks, and destructive-action confirmation;
- loading, retry, cancellation, disconnection, offline use, restart, and power-loss recovery;
- persistence, synchronisation, defaults, and migration of saved settings;
- latency, frame time, memory, draw-call, bandwidth, refresh, and power budgets where they matter;
- logs, telemetry, analytics, and audit events when the product requires them;
- fixtures, simulated sensors, fake services, or emulator states needed to exercise realistic conditions.

The backend is optional. The contract is between the interface and whatever drives it.

Use the smallest architecture that satisfies the interaction. Do not add services, abstractions, or hardware assumptions because a reference product might use them. Observable behaviour can suggest a requirement. It cannot reveal another product's implementation.

## 6. Build complete interaction slices

Implement one working user task at a time, including the interface states, underlying behaviour within scope, and tests. If the assignment is UI-only, use the existing contracts and do not rewrite the system behind them.

Build the chosen art direction into the first slice. Do not leave the interface visually generic and promise to add its identity in a final polish pass.

While building:

- derive visual values from the agreed system rather than scattering one-off colours, dimensions, and timing values;
- use suitable platform primitives, such as semantic HTML, native controls, game-engine UI components, or the existing embedded drawing library;
- support the intended input method, including visible keyboard or controller focus, touch targets, button mappings, encoder steps, and a reliable way back;
- render correctly at the target sizes, orientations, safe areas, pixel densities, colour depths, and physical viewing distance;
- keep action and state names consistent from control to result;
- make startup, loading, empty, validation, warning, permission, error, disconnected, success, and destructive states deliberate when they can occur;
- replace placeholder icons, imagery, textures, and effects with assets that fit the direction when the task and available tools permit it;
- tune typography, spacing, alignment, surfaces, focus treatments, transitions, and responsive or state changes as one system rather than isolated decorations;
- avoid controls that do nothing and placeholder data that survives into a real path;
- watch CSS specificity for web work, anchors and draw order in game engines, native layout constraints in apps, and buffers, repaints, flash, and RAM use on embedded displays;
- keep performance within the target's limits, including images, fonts, animation, list size, draw calls, device polling, network requests, and display refresh;
- preserve relevant accessibility and safety behaviour. Use redundant cues when colour, sound, or a single indicator is not enough.

Prototype shortcuts are fine when the user asked for a prototype. Name them as shortcuts and keep the boundary clear.

### Write interface copy as part of the design

Apply `natural-writing` to interface copy, documentation, research notes, and the final handoff when that skill is available.

Use the terms real users and comparable products use, but write original copy for this product. Prefer plain verbs and specific nouns. A control says what it will do. The same action keeps the same name through confirmation and error states. Errors say what happened and what the user can do next. Empty states point to a relevant first action. Remove filler, slogans, and claims the product cannot prove.

## 7. Verify behaviour and appearance

Run the project's relevant formatter, linter, type checks, tests, build, game export, firmware compile, or emulator checks. Test the UI/system contract as well as the normal path. Include invalid input, unavailable data, lost focus, repeated input, disconnection, slow operations, restart, missing permission, and hardware or service failure when they can occur.

Verify the implemented interface in the closest available version of its target environment:

1. Exercise each main journey with the intended controls.
2. Check browser consoles, application logs, engine output, network failures, serial output, and device diagnostics as applicable.
3. Capture focused screenshots, render frames, emulator images, or device photos of important states and target configurations.
4. Open every capture and inspect hierarchy, spacing, clipping, legibility, contrast, selection, control feedback, icon treatment, and visual consistency.
5. Check the actual resolution and physical scale. A 128 by 64 display enlarged on a monitor can hide unreadable type and one-pixel mistakes.
6. Fix what is wrong, repeat the interaction, and recapture the affected states.

After behaviour works, run at least one dedicated visual critique. Compare the strongest captures with the declared visual ambition and the best research references at a similar scale. Do not copy their composition. Judge whether the result has comparable clarity, confidence, detail, and finish. Identify the weakest visible area, improve it, and recapture it.

Use a browser for browser-based interfaces. Use the project's preview, emulator, game build, off-device renderer, or target hardware for other media. Flash or operate hardware only when the task authorises it and the device is available. If target-hardware testing is not possible, say which substitute was used and what remains unverified.

Follow the fuller `visual-inspection-improvement` process when it is available. Inspect captures individually rather than relying on a contact sheet. Include dense, empty, loading, error, warning, disconnected, and constrained-screen states when they exist.

Do not stop at correct or tidy. Stop only when the required interactions work, automated checks pass or their failures are explained, the captures no longer show problems worth fixing within the task's scope, and the strongest view meets the stated visual ambition.

## 8. Hand off the work

Keep the final report concrete. Include:

- the comparable products and source material inspected, with links;
- the screenshot paths or other research evidence that informed the work;
- the patterns adopted, changed, or deliberately rejected;
- the visual ambition and the final captures that demonstrate it;
- the interface and system behaviour implemented;
- the display, input, viewport, emulator, or hardware configurations verified;
- the checks run and their results;
- any limitation, unverified target state, or remaining decision.

Do not call the interface polished, intuitive, or production-ready as a substitute for evidence. Name what works and how it was verified.
