---
name: premium_web_design
description: Guidelines and principles for creating premium, high-end web designs.
---

# Premium Web Design Principles

This skill outlines the key elements required to create "wow" factor, premium web applications.

## 1. Typography
- **Font Choice**: Use modern, geometric sans-serifs (e.g., Inter, Outfit, Manrope) or elegant serifs for headings. Avoid default system fonts unless intentionally styled.
- **Hierarchy**: Establish clear scale (h1 vs p). Use extreme contrast in size (huge headlines, small refined labels).
- **Spacing**: Generous line-height (1.5-1.7 for body). tracking-tight for large headings to make them feel solid.

## 2. Color & Depth
- **Palette**: Use a curated palette. Avoid pure black (#000000) or pure white (#FFFFFF) for backgrounds; use off-blacks (#0a0a0a) or soft creams (#fafafa).
- **Gradients**: Use subtle, noise-textured gradients rather than flat linear ones.
- **Glassmorphism**: Use backdrop-filter blur for overlays and navbars.
  ```css
  .glass {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
  }
  ```

## 3. Motion & Interaction (Framer Motion)
- **Micro-interactions**: Buttons should scale or glow on hover.
- **Page Transitions**: Smooth fade/slide between routes.
- **Scroll Animations**: Elements should fade up or reveal as they enter the viewport.
  ```typescript
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    whileInView={{ opacity: 1, y: 0 }}
    viewport={{ once: true }}
    transition={{ duration: 0.6 }}
  >
  ```

## 4. Layout & Rhythm
- **Grid**: Adhere to a strict grid system but break it intentionally for interest.
- **Whitespace**: Use whitespace (padding/margin) aggressively. "Premium" means space to breathe.
- **Bento Grids**: Use boxy, card-based layouts for feature showcases.

## 5. Imagery
- **Quality**: Use high-res, optimized images (WebP).
- **Styling**: Rounded corners (e.g., `rounded-2xl` or `rounded-3xl` for that modern feel).
- **Parallax**: Subtle scroll parallax on background images adds depth.
