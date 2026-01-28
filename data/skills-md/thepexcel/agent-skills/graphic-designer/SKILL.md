---
name: graphic-designer
description: Designs graphics for thumbnails, social media, banners, and presentations. Applies design principles (CRAP, Gestalt, visual hierarchy) with research-backed techniques. Integrates with /geometric-elements for decorative assets. Use when creating layouts, choosing typography/colors, or designing any graphic assets. For photography/cinematography prompts, use /art-director instead.
---

# Graphic Designer

Create effective visual communication through research-backed design principles.

**Design = Communication + Aesthetics** — Good design is invisible: it guides the eye, conveys the message, and feels "right" without effort.

---

## Quick Workflow

```
1. PURPOSE   — What should viewer DO after seeing this?
2. AUDIENCE  — Who? What culture? What device?
3. HIERARCHY — What's #1, #2, #3 in importance?
4. LAYOUT    — Sketch placement (Z or F pattern)
5. COLORS    — 60-30-10 rule (check cultural meaning!)
6. TYPE      — Max 2 fonts (1 display + 1 body)
7. ELEMENTS  — Add graphics, icons, photos
8. REFINE    — Remove until it breaks, then add back
9. CHECK     — Squint test, mobile test, contrast check
10. REVIEW   — Self-critique and iterate (optional loop)
```

---

## Self-Review Loop (Auto-Improvement)

เมื่อสร้างผลงานแล้ว สามารถเปิด loop วิเคราะห์และปรับปรุงอัตโนมัติได้

### เมื่อไหร่ควรถาม User

**ถาม user ก่อนเริ่ม loop:**
> "ต้องการให้หนูเปิด Auto-Improvement Loop ไหมคะ? หนูจะวิเคราะห์ผลลัพธ์และปรับปรุงซ้ำจนกว่าจะได้คุณภาพที่ดีค่ะ"

**Options:**
1. **Quick Review** — 1 รอบวิเคราะห์ + แก้ไขถ้าจำเป็น
2. **Full Loop** — วิเคราะห์ซ้ำจนกว่าจะผ่าน Quality Checklist ทุกข้อ
3. **Skip** — ส่งมอบเลย ไม่ต้อง review

### Review Loop Workflow

```
┌─────────────────────────────────────────────────────┐
│  1. CREATE — สร้างผลงาน (slides, graphics, etc.)    │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│  2. ANALYZE — วิเคราะห์โครงสร้าง                    │
│     • อ่าน XML/code ที่สร้าง                        │
│     • ตรวจสอบ positions, sizes, colors             │
│     • สร้าง thumbnails (ถ้าเป็น PPTX)              │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│  3. CRITIQUE — วิจารณ์ตาม Design Principles         │
│     ใช้ Review Checklist (ด้านล่าง)                 │
└─────────────────────────────────────────────────────┘
                          ↓
              ┌───────────────────┐
              │  ผ่านทุกข้อ?      │
              └───────────────────┘
               ↙ NO          YES ↘
┌──────────────────┐      ┌──────────────────┐
│  4. FIX          │      │  5. DELIVER      │
│  แก้ไขปัญหา       │      │  ส่งมอบผลงาน     │
│  ที่พบ           │      │                  │
└──────────────────┘      └──────────────────┘
          ↓
    กลับไป Step 2
    (max 3 iterations)
```

### Review Checklist (Score 0-10)

| Category | Check | Weight |
|----------|-------|--------|
| **Hierarchy** | #1 element เด่นชัด 2x+ กว่าที่เหลือ? | High |
| **Contrast** | WCAG AA (4.5:1)? | High |
| **Alignment** | Elements align to grid? | Medium |
| **White Space** | ≥20% empty space? | Medium |
| **Color Count** | ≤4 colors? | Medium |
| **Font Count** | ≤2 fonts? | Low |
| **Visual Impact** | มี focal point ที่ดึงดูดสายตา? | High |
| **Brand Consistency** | ตรงกับ brand guidelines? | High |

**Pass threshold:** Average ≥ 7/10 และไม่มี High-weight items ต่ำกว่า 6

### Visual Impact Boost

ถ้า Visual Impact score ต่ำ สามารถใช้ skills เหล่านี้ช่วย:

| Need | Skill | Use Case |
|------|-------|----------|
| **Hero images** | `/art-director` | Gen prompt สำหรับ AI image ที่มี composition ดี |
| **Local image gen** | `/comfyui-user` | Gen รูปผ่าน ComfyUI server ในเครื่อง |
| **Decorative elements** | `/geometric-elements` | สร้าง corners, lines, patterns |

**Example integration:**
```
1. สร้าง slide แล้วพบว่า visual impact ต่ำ
2. ใช้ /art-director สร้าง prompt สำหรับ background image
3. ใช้ /comfyui-user gen รูป (หรือ cloud API)
4. ใส่รูปใน slide แล้ว re-analyze
```

### Iteration Limits

- **Max iterations:** 3 รอบ (ป้องกัน infinite loop)
- **Stop early if:** User บอกให้หยุด หรือ score ไม่เพิ่มขึ้น 2 รอบติดต่อกัน
- **Report:** สรุป changes ที่ทำในแต่ละ iteration

---

## Design Principles (Summary)

### CRAP Principles

| Principle | What | How |
|-----------|------|-----|
| **Contrast** | Make differences obvious | Size, color, weight |
| **Repetition** | Create consistency | Reuse colors, fonts |
| **Alignment** | Connect visually | Grid, edges |
| **Proximity** | Group related items | Spacing |

→ Details: [references/gestalt.md](references/gestalt.md)

### Visual Hierarchy (order of impact)

1. **Size** — Larger = more important
2. **Color/Contrast** — Bright catches eye first
3. **Position** — Top-left (Western), top-right (RTL)
4. **White Space** — Isolation creates emphasis
5. **Weight** — Bold stands out

### Reading Patterns

| Pattern | Best For | Flow |
|---------|----------|------|
| **Z-Pattern** | Visual/marketing | Top-L → Top-R → Bottom-L → Bottom-R |
| **F-Pattern** | Text-heavy | Horizontal scans + vertical down left |

---

## Color System

### 60-30-10 Rule

| % | Role | Example |
|---|------|---------|
| 60% | Dominant | Background |
| 30% | Secondary | Containers, cards |
| 10% | Accent | CTAs, highlights |

### Quick Palettes

| Mood | Colors |
|------|--------|
| Professional | Navy + White + Gold |
| Energetic | Orange + Black + White |
| Calm | Blue + Light Gray + White |
| Premium | Black + Gold + White |
| **2025 Trend** | Dark + Neon accent |

### Cultural Color Meanings (Check First!)

| Color | Western | East Asia | Thai Context |
|-------|---------|-----------|--------------|
| **Red** | Danger, urgency | Luck, joy | Auspicious |
| **White** | Pure, clean | Mourning | Formal/Mourning |
| **Yellow** | Optimism | Sacred | Royal |
| **Gold** | Luxury | Prosperity | Premium |

→ Full guide: [references/color-theory.md](references/color-theory.md)

### Accessibility (WCAG)

| Standard | Normal Text | Large Text (18pt+) |
|----------|-------------|-------------------|
| **AA (Minimum)** | 4.5:1 | 3:1 |
| **AAA (Enhanced)** | 7:1 | 4.5:1 |

Tool: [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)

---

## Typography

### Quick Rules

- **Max 2 fonts** — 1 display + 1 body
- **Hierarchy via size** — Not font changes
- **Line height** — 1.4-1.6 for body, 1.1-1.2 for headlines

### Safe Font Pairs

| Display | Body | Mood |
|---------|------|------|
| Montserrat Bold | Open Sans | Modern |
| Playfair Display | Lato | Elegant |
| **Kanit Bold** | **Sarabun** | Thai-friendly |

→ Full guide: [references/typography.md](references/typography.md)

---

## Layout

### 8px Spacing System

| Size | Use |
|------|-----|
| 8px | Within groups |
| 16px | Between elements |
| 24-32px | Sections |
| 48px | Page margins |

### Social Media Dimensions

| Platform | Ratio | Size |
|----------|-------|------|
| YouTube Thumbnail | 16:9 | 1280×720 |
| Instagram Post | 1:1 | 1080×1080 |
| Instagram Story | 9:16 | 1080×1920 |
| Facebook/LinkedIn | 1.91:1 | 1200×630 |

→ Layout templates: [references/layouts.md](references/layouts.md)

---

## Presentation Slides

### Core Rules

| Rule | Guideline |
|------|-----------|
| **One idea per slide** | Single focused message |
| **Rule of 4** | Max 4 bullets, 4 words each |
| **Don't compete** | Audience can't read AND listen |

### Font Sizes

| Context | Titles | Body | Captions |
|---------|--------|------|----------|
| **Large room** | 60pt+ | 40pt+ | 24pt+ |
| **Virtual** | 44pt+ | 32pt+ | 20pt+ |

→ Full guide: [references/presentation-design.md](references/presentation-design.md)

---

## YouTube Thumbnails

| Element | Recommendation |
|---------|----------------|
| **Faces** | Use expressive faces (+20-30% CTR) |
| **Text** | Minimal, bold, curiosity |
| **Colors** | High contrast, 3-4 max |
| **Mobile** | Readable at small size |

**Layout:** Face 40%+ height, eye contact, blur background

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Too many fonts | Max 2 |
| No hierarchy | Make #1 thing 2x bigger |
| Centered everything | Use left-align + proximity |
| Rainbow colors | Pick 1 accent color |
| Filled every space | Add 20% more white space |
| Text on busy photo | Add overlay or blur |
| Ignoring culture | Check color meanings |

---

## Checklists

### Before Designing

- [ ] What's the ONE message?
- [ ] Who's the audience? (culture, device)
- [ ] What emotion should it evoke?

### Quality Check

- [ ] Clear hierarchy? (squint test)
- [ ] Readable at target size?
- [ ] Max 3-4 colors, 2-3 fonts?
- [ ] Contrast 4.5:1+? (WCAG AA)
- [ ] Aligned to grid?
- [ ] Enough white space?

---

## Tools Integration

### /geometric-elements — Decorative Assets

```bash
python scripts/generate.py shape --style star --color "#D4A84B" --size 100
python scripts/generate.py corner-accent --color "#D4A84B" --size 150
python scripts/generate.py line-divider --color "#D4A84B" --width 800
```

### /art-director — Visual Impact (AI Image Prompts)

เมื่อต้องการรูปที่มี composition และ visual impact ดี:

```
1. Invoke /art-director พร้อมบอก context (slide theme, mood, brand)
2. ได้ prompt ที่พร้อมใช้กับ AI image generators
3. Gen รูปผ่าน /comfyui-user หรือ cloud API
```

### AI Slide Backgrounds (Best Practices)

**Workflow ที่ได้ผลดี:**

```
1. ขอดู REFERENCE — ให้ user แชร์ตัวอย่าง slides ที่ชอบ
2. วิเคราะห์ PATTERNS — สรุป style (colors, elements, layout)
3. Gen ทั้ง BACKGROUND — ไม่แยกชิ้น, ไม่มี text
4. ITERATE — ปรับ size/position ตาม feedback
5. User วาง TEXT เอง — ยืดหยุ่นกว่า
```

**✅ Do:**

| Technique | Why |
|-----------|-----|
| Gen complete background | ได้ภาพ cohesive สวยกว่าแยกชิ้น |
| ใช้ `--edit` กับ logo เป็น ref | AI เห็น shape จริง ไม่ต้องเดา |
| บอก "NO TEXT" | Text จาก AI มักผิด/ไม่สวย |
| White background | Nano Banana Pro ทำ transparent ไม่ได้ |
| เริ่ม simple | Logo เล็กมุมเดียว ดีกว่าเยอะทุกมุม |

**❌ Don't:**

| Technique | Problem |
|-----------|---------|
| "TRANSPARENT BACKGROUND" | ได้ checkerboard ปลอม |
| อธิบาย logo shape เอง | AI ตีความผิด ใช้ --edit แทน |
| Gen แยกชิ้นแล้วประกอบ | Elements ไม่ match กัน |
| Decoration เยอะ | รกเกินไป ไม่ professional |

**Prompt Template:**
```
Professional presentation [TYPE] slide background,
16:9 aspect ratio. NO TEXT. [STYLE] STYLE.
BACKGROUND: [color, grid, gradient]
DECORATIVE: [small/subtle elements, specific corners]
LAYOUT: Leave [area] empty for [content]
COLORS: [hex codes]
```

### /comfyui-user — Local Image Generation

สำหรับ gen รูปในเครื่องผ่าน ComfyUI:

```
1. Invoke /comfyui-user พร้อมบอกว่าต้องการรูปแบบไหน
2. เลือก workflow (turbo สำหรับ gen ใหม่, edit สำหรับแก้รูปเดิม)
3. ได้รูปพร้อมใช้ใน slides
```

### Related Skills

| Need | Skill | When to Use |
|------|-------|-------------|
| Decorative elements | `/geometric-elements` | corners, lines, patterns, shapes |
| AI image prompts | `/art-director` | hero images, backgrounds ที่ต้องการ composition ดี |
| Local image gen | `/comfyui-user` | gen รูปผ่าน ComfyUI server |
| PowerPoint slides | `/pptx` | สร้าง/แก้ไข PPTX files |
| ThepExcel brand | `/thepexcel-brand-guidelines` | brand colors, fonts, logo usage |

---

## References

| Topic | File |
|-------|------|
| Color theory | [references/color-theory.md](references/color-theory.md) |
| Typography | [references/typography.md](references/typography.md) |
| Layouts | [references/layouts.md](references/layouts.md) |
| Presentation design | [references/presentation-design.md](references/presentation-design.md) |
| Gestalt principles | [references/gestalt.md](references/gestalt.md) |
