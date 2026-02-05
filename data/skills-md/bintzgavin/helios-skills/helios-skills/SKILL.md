---
name: helios-skills
description: Collection of agent skills for Helios video engine. Use when working with programmatic video creation, browser-native animations, or Helios compositions. Install individual skills by path for specific capabilities.
---

# Helios Skills Collection

This repository contains agent skills for [Helios](https://github.com/BintzGavin/helios), a browser-native video engine for programmatic animation and rendering.

## Installation

This is a **collection repository** containing multiple skills. To use these skills, install individual skills by their path:

```bash
# Getting started
npx skills add BintzGavin/helios-skills/skills/getting-started

# Core skills
npx skills add BintzGavin/helios-skills/skills/core
npx skills add BintzGavin/helios-skills/skills/renderer
npx skills add BintzGavin/helios-skills/skills/player
npx skills add BintzGavin/helios-skills/skills/studio

# Workflows
npx skills add BintzGavin/helios-skills/skills/workflows/create-composition
npx skills add BintzGavin/helios-skills/skills/workflows/render-video
npx skills add BintzGavin/helios-skills/skills/workflows/visualize-data

# Framework examples
npx skills add BintzGavin/helios-skills/skills/examples/react
npx skills add BintzGavin/helios-skills/skills/examples/vue
npx skills add BintzGavin/helios-skills/skills/examples/svelte

# Animation libraries
npx skills add BintzGavin/helios-skills/skills/examples/gsap
npx skills add BintzGavin/helios-skills/skills/examples/framer-motion
npx skills add BintzGavin/helios-skills/skills/examples/threejs
```

## Available Skills

### Getting Started

- **skills/getting-started** - Installation and quick start guide. Covers package installation, requirements (Node.js, FFmpeg), basic setup, and initial composition structure. Use when setting up a new Helios project.

### Core Package Skills

- **skills/core** - Core API for Helios video engine. Covers Helios class instantiation, signals, animation helpers, and DOM synchronization.
- **skills/renderer** - Server-side rendering of Helios compositions to video files.
- **skills/player** - Embeddable video player with composition playback and controls.
- **skills/studio** - Visual editor for Helios compositions.

### Workflow Skills

- **skills/workflows/create-composition** - Workflow for creating a new Helios composition.
- **skills/workflows/render-video** - Workflow for rendering compositions to video.
- **skills/workflows/visualize-data** - Workflow for data visualization animations.

### Framework Integration Skills

- **skills/examples/react** - React integration patterns
- **skills/examples/vue** - Vue integration patterns
- **skills/examples/svelte** - Svelte integration patterns
- **skills/examples/solid** - Solid.js integration patterns
- **skills/examples/vanilla** - Vanilla JavaScript patterns

### Animation Library Skills

- **skills/examples/gsap** - GSAP animation integration
- **skills/examples/framer-motion** - Framer Motion integration
- **skills/examples/lottie** - Lottie animation playback
- **skills/examples/threejs** - Three.js 3D scenes
- **skills/examples/pixi** - PixiJS 2D graphics
- **skills/examples/p5** - p5.js creative coding

### Data Visualization Skills

- **skills/examples/d3** - D3.js visualizations
- **skills/examples/chartjs** - Chart.js animated charts

### Rendering Technique Skills

- **skills/examples/canvas** - Canvas 2D rendering
- **skills/examples/signals** - Reactive signals patterns
- **skills/examples/tailwind** - Tailwind CSS styling
- **skills/examples/podcast-visualizer** - Audio visualization

## When to Use

Use these skills when:

- Creating programmatic video compositions
- Working with browser-native animations (CSS, WAAPI)
- Building video rendering pipelines
- Integrating Helios with React, Vue, Svelte, or other frameworks
- Using animation libraries like GSAP, Framer Motion, or Three.js
- Creating data visualizations as video
- Setting up Helios development workflows

## Repository

View all skills and source code at: https://github.com/BintzGavin/helios-skills
