---
name: proslide
description: "Tạo slide chuyên nghiệp từ nội dung đầu vào. Sử dụng khi user yêu cầu tạo presentation, slide deck, hoặc gọi /proslide. Hỗ trợ 3 mức độ chi tiết và Slidev theme tùy chọn. Reuse outline để generate nhiều variants."
disable-model-invocation: true
---

# ProSlide - Professional Slide Generator

Tạo professional text-only slides từ content input. Vietnamese default. Activate `slidev` skill (built-in, cùng context) cho Slidev Markdown generation + PDF export.

## Output Folder Structure

Mỗi lần tạo presentation, output được lưu trong folder có cấu trúc:

```
output/
└── {slug}-{YYMMDD-HHmm}/
    ├── outline.md
    ├── content-map.md
    ├── coverage-report.md
    ├── research-notes.md
    └── slides/
        └── {slug}-{theme-name}/    # Slidev project
            ├── package.json
            ├── slides.md
            └── dist/               # After export (gitignored)
                └── {slug}.pdf
```

**Naming rules:**

* `{slug}`: kebab-case từ topic chính (max 30 chars)

* `{YYMMDD-HHmm}`: timestamp lúc tạo folder

* `{theme-name}`: tên Slidev theme đã chọn (VD: default, seriph, apple-basic)

* Khi reuse outline để generate thêm slide mới, folder mới được thêm vào `slides/` của folder đã có

## Step 0: Detect Mode (New / Reuse)

1. Kiểm tra input từ user:

   * Nếu user chỉ vào **folder output đã có** (chứa `outline.md`) → **Reuse mode**

   * Nếu user cung cấp **nội dung mới** (text, file path) → **New mode**

   * Nếu user nói "dùng lại outline", "reuse", "tạo thêm slide" + chỉ folder → **Reuse mode**

2. **Reuse mode** → nhảy thẳng tới **Step 2.5** (skip Step 1 & 2)

3. **New mode** → tiếp tục Step 1

## Step 1: Tiếp nhận nội dung & Cấu hình

1. Đọc input từ user: text trực tiếp hoặc file path (.md, .txt, .pdf)
2. Nếu input là file path, đọc nội dung file
3. Phân tích sơ bộ: topic, length, complexity
4. Hỏi user bằng AskUserQuestion (4 câu hỏi trong 1 lần):

**Câu hỏi 1 - Loại nội dung** (header: "Content type"):

* "Hướng dẫn/Giáo dục" - Giải thích khái niệm, tutorial, hướng dẫn học (Gagné + scaffolding)

* "Business/Báo cáo" - Phân tích, đề xuất, báo cáo kết quả (Pyramid Principle)

* "Thuyết phục/Pitch" - Bán ý tưởng, pitch sản phẩm, proposal (PAS + Sparkline)

* "Technical/Process" - Quy trình, kiến trúc, hệ thống, so sánh kỹ thuật (SCR + step-by-step)

**Câu hỏi 2 - Mức độ chi tiết** (header: "Detail level"):

* "L1 - Tổng quan" - Chỉ ý chính, bullet ngắn gọn (5+ slides)

* "L2 - Cân bằng" - Ý chính + giải thích + ví dụ minh họa (10+ slides)

* "L3 - Chi tiết" - Đầy đủ nội dung, deep dive, code examples (18+ slides)

**Câu hỏi 3 - Ngôn ngữ** (header: "Language"):

* "Tiếng Việt" - Toàn bộ nội dung tiếng Việt (Recommended)

* "English" - Toàn bộ nội dung tiếng Anh

* "Song ngữ" - Title tiếng Anh, body tiếng Việt (phù hợp technical/academic)

**Câu hỏi 4 - Research bổ sung** (header: "Research"):

* "Chỉ dùng source" - Tạo slide 100% từ nội dung đầu vào, không tìm thêm

* "Research thêm" - Tìm thêm data, statistics, examples từ web để bổ sung slide

* "Auto" - Tự động: research nếu source ít thông tin (<500 words hoặc thiếu data/metrics), skip nếu đủ

**Logic đánh dấu Recommended cho câu hỏi 4:**

* Nếu source < 500 words HOẶC source chỉ có bullet points không context HOẶC thiếu data/metrics/examples → đánh dấu "Research thêm" là (Recommended)

* Nếu source >= 500 words VÀ có đầy đủ data/context → đánh dấu "Chỉ dùng source" là (Recommended)

## Step 1.5: Research bổ sung (Optional)

Chạy sau Step 1, trước Step 2. Quyết định dựa trên câu hỏi 4 ở Step 1.

**Khi nào chạy:**

* User chọn "Research thêm" → luôn chạy

* User chọn "Auto" → chạy NẾU source < 500 words HOẶC source thiếu data/metrics/examples cụ thể

* User chọn "Chỉ dùng source" → SKIP hoàn toàn, nhảy tới Step 2

**Process:**

1. Extract 3-5 topic keywords từ source input (dựa trên content type đã chọn)

2. Tạo 2-3 search queries phù hợp:

   * Query 1: `"{topic chính}" statistics data {năm hiện tại}` (tìm số liệu mới nhất)

   * Query 2: `"{topic chính}" trends insights` (tìm xu hướng, insights)

   * Query 3: `"{topic chính}" examples best practices` (tìm ví dụ, case studies)

3. Chạy WebSearch cho mỗi query

4. Extract findings relevant: statistics, data points, examples, quotes, trends

5. Lưu kết quả vào `{output_folder}/research-notes.md` theo format:

```markdown
# Research Notes — [Topic]

## Search Queries

1. [query 1]
2. [query 2]
3. [query 3]

## Findings

### Statistics & Data

- [stat 1] — Source: [url/name]
- [stat 2] — Source: [url/name]

### Trends & Insights

- [insight 1]
- [insight 2]

### Examples & Case Studies

- [example 1]
- [example 2]

## Selected for Slides

Items below sẽ được đưa vào Content Map với tag [R]:

1. [item] — lý do chọn
2. [item] — lý do chọn
```

1. Append selected items vào Content Map (Step 2) với prefix `[R]` để phân biệt source gốc vs researched
2. Thông báo user: "Research xong: tìm thấy X data points, Y insights. Đã lưu tại research-notes.md"

**Quy tắc research:**

* Chỉ lấy thông tin factual, có nguồn rõ ràng

* Ưu tiên: số liệu cụ thể > xu hướng > ví dụ > quotes

* KHÔNG thay thế nội dung source, chỉ BỔ SUNG

* Max 10 items đưa vào Content Map (tránh overwhelming)

* Research items trong outline phải ghi rõ "(Nguồn: research)" trong speaker notes hoặc content

## Visual Patterns per Content Type

Khi tạo slides, áp dụng visual patterns phù hợp với content type đã chọn:

| Content Type       | Visual Patterns                                                     | Recommended Slide Types                           |
| ------------------ | ------------------------------------------------------------------- | ------------------------------------------------- |
| Hướng dẫn/Giáo dục | Numbered step indicators, before/after comparison, warm decorations | content, comparison, statement (cho key concepts) |
| Business/Báo cáo   | Accent bars, data callout slides, conservative decorations          | content, metric (cho KPIs), comparison, summary   |
| Thuyết phục/Pitch  | Bold statement slides, high contrast, CTA emphasis                  | statement (30%+), metric, content, cta            |
| Technical/Process  | Code blocks, process flow indicators, comparison tables             | content, comparison, code, transition             |

## Auto Theme Recommendation

Dựa trên content type, gợi ý Slidev theme (user có quyền chọn khác hoặc nhập tên theme bất kỳ):

| Content Type       | Primary Recommendation | Secondary   |
| ------------------ | ---------------------- | ----------- |
| Hướng dẫn/Giáo dục | seriph                 | default     |
| Business/Báo cáo   | default                | apple-basic |
| Thuyết phục/Pitch  | apple-basic            | seriph      |
| Technical/Process  | default                | seriph      |

## Slidev Theme List

Danh sách themes chính thức và community phổ biến, hiển thị cho user khi chọn:

**Official themes:**

| Theme         | Package                     | Mô tả                          |
| ------------- | --------------------------- | ------------------------------ |
| `default`     | `@slidev/theme-default`     | Minimalist, light/dark         |
| `seriph`      | `@slidev/theme-seriph`      | Serif-based formal, light/dark |
| `apple-basic` | `@slidev/theme-apple-basic` | Keynote-inspired, light/dark   |
| `bricks`      | `@slidev/theme-bricks`      | Playful blocks, light          |
| `shibainu`    | `@slidev/theme-shibainu`    | Cute dark theme                |

**Community themes (phổ biến):**

| Theme      | Package                 | Mô tả                            |
| ---------- | ----------------------- | -------------------------------- |
| `geist`    | `slidev-theme-geist`    | Vercel design system, light/dark |
| `academic` | `slidev-theme-academic` | Formal academic, light/dark      |
| `dracula`  | `slidev-theme-dracula`  | Vibrant dark theme               |

User cũng có thể nhập tên bất kỳ Slidev theme từ npm.

## Step 2: Phân tích nội dung & Tạo outline (New mode)

1. Tạo output folder: `output/{slug}-{YYMMDD-HHmm}/` và subfolder `slides/`

2. Đọc `references/outline-rules.md` (relative to this skill folder) để nắm quy tắc outline

3. Áp dụng framework tương ứng với content type đã chọn ở Step 1 (xem Content Type → Framework Mapping trong outline-rules.md)

4. **Content Map** (xem "Content Map Rules" trong outline-rules.md):

   * Parse source → extract topics → assign priority (`must`/`should`/`nice`) theo detail level

   * Nếu Step 1.5 đã chạy → append research items vào Content Map với prefix `[R]` (xem outline-rules.md)

   * Lưu Content Map ra file `{output_folder}/content-map.md`

5. Phân tích nội dung theo detail level đã chọn (xem Detail Level Mapping + Content Selection Criteria trong outline-rules.md)

6. Tạo outline theo cấu trúc bắt buộc: Opening > Body > Closing. **Cross-check** với Content Map: mọi `must` topics phải xuất hiện, `should`/`nice` theo threshold

7. **Lưu outline** ra file `{output_folder}/outline.md` với metadata header (xem Outline File Format trong outline-rules.md)

8. Hiển thị outline cho user review (numbered list với slide titles + brief content description)

9. **Coverage Report** (xem "Coverage Report Rules" trong outline-rules.md):

   * Generate file `{output_folder}/coverage-report.md` mapping source topics → slides + omission justification

   * Thông báo cho user: tóm tắt 1 dòng coverage % + mention report file path

10. **Feedback loop**: Hỏi user "Outline OK? Bạn có muốn chỉnh sửa gì không?" bằng AskUserQuestion (header: "Outline review"):

* "OK, tiếp tục" - Chấp nhận outline, chuyển sang chọn theme

* "Chỉnh sửa" - User sẽ mô tả thay đổi → cập nhật outline file + re-check coverage → show lại → hỏi lại

## Step 2.5: Reuse mode (khi đã có outline)

1. Đọc `{output_folder}/outline.md` — parse metadata header để lấy: content\_type, detail\_level, language, slug
2. Hiển thị tóm tắt cho user: "Reuse outline: {title}, {detail\_level}, {language}, {N} slides"
3. Tiếp tục chọn theme ở Step 2.6

## Step 2.6: Chọn Slidev theme (cả New và Reuse mode)

1. Hiển thị bảng **Slidev Theme List** (xem section ở trên)
2. Kiểm tra `{output_folder}/slides/` xem đã có Slidev project folder nào chưa → show user "(đã tạo)" bên cạnh theme đã dùng
3. Hỏi user bằng AskUserQuestion (header: "Theme"): "Chọn Slidev theme:" + đánh dấu recommended theme dựa trên bảng Auto Theme Recommendation + cho phép nhập tên theme khác qua "Other"

## Step 3: Tạo slide (Slidev)

1. Xác định theme package name:

   * Official themes: `@slidev/theme-{name}` (VD: `@slidev/theme-seriph`)

   * Community themes: `slidev-theme-{name}` (VD: `slidev-theme-geist`)

   * Nếu user nhập custom name → dùng nguyên tên

2. Đọc `references/slide-templates.md` (relative to this skill folder) để nắm Slidev Markdown patterns cho từng slide type

3. Đọc outline từ `{output_folder}/outline.md` (nếu Reuse mode) hoặc từ context (nếu vừa tạo)

4. **Activate** **`slidev`** **skill** trong cùng agent context. Cung cấp:

   * **Headmatter config**:

     ```yaml
     theme: { theme-name }
     fonts:
       sans: Tahoma
       serif: Arial
       mono: Fira Code
       provider: none
     ```

   * **Layout mapping table** cho mỗi slide type:

     | Slide Type | Slidev Layout   |
     | ---------- | --------------- |
     | title      | cover           |
     | agenda     | default         |
     | content    | default         |
     | comparison | two-cols-header |
     | summary    | default         |
     | cta        | end             |
     | transition | section         |
     | statement  | statement       |
     | metric     | fact            |
     | code       | default         |

   * **Nội dung từng slide** theo outline (title, body content, slide type → layout)

   * **Slidev Markdown templates** từ `references/slide-templates.md`

   * **Vietnamese fonts requirement**: `Tahoma, Arial, sans-serif` qua fonts config

   * **Output path**: `{output_folder}/slides/{slug}-{theme-name}/`

5. Slidev skill tạo Slidev project:

   * **`package.json`**:

     ```json
     {
       "name": "{slug}-{theme-name}",
       "private": true,
       "scripts": {
         "dev": "slidev",
         "build": "slidev build",
         "export": "slidev export --output dist/{slug}.pdf --timeout 60000"
       },
       "dependencies": {
         "@slidev/cli": "latest",
         "{theme-package}": "latest"
       },
       "devDependencies": {
         "playwright-chromium": "latest"
       }
     }
     ```

   * **`slides.md`**: Headmatter + all slides theo Slidev Markdown format

6. **Install dependencies**: `pnpm install` trong Slidev project folder

7. **Export PDF**: `npx slidev export --output dist/{slug}.pdf --timeout 60000`

8. Thông báo output:

   * Slidev project path

   * PDF path (nếu export thành công)

   * Output folder path (nhắc user có thể reuse outline: `/proslide` + chỉ folder path)

   * Hướng dẫn: `cd {project-path} && pnpm dev` để xem slides trong browser

## Slidev Constraints (CRITICAL)

Khi activate slidev skill, PHẢI tuân thủ các constraints sau:

* **Vietnamese fonts**: Dùng `Tahoma, Arial, sans-serif` qua fonts config trong headmatter với `provider: none` (system fonts, không fetch từ Google Fonts). KHÔNG dùng Impact, Courier New (Vietnamese rendering kém)

* **Text-only**: Không dùng image layouts, không embed images. Chỉ text, bullets, code blocks

* **Speaker notes**: Dùng HTML comments `<!-- notes -->` sau content mỗi slide

* **Code blocks**: Dùng native Markdown fenced blocks với language tag (`python, `  javascript, etc.). Slidev tự động syntax highlight. Max 10-15 dòng/slide. Dùng line highlighting `{2,3}` để nhấn mạnh dòng quan trọng, hoặc click-based highlighting `{1|3-4|all}` để walkthrough từng phần (xem templates trong `references/slide-templates.md`)

* **Nested lists**: Slidev Markdown hỗ trợ nested lists tốt (indent 2 spaces). Dùng thoải mái cho L2/L3 sub-bullets

* **Max content per slide**: Tuân theo rules từ `outline-rules.md`:

  * L1: 2-3 bullets, <8 words/bullet

  * L2: 3-5 bullets + 1-2 sub-bullets

  * L3: 3-5 bullets + 2-3 sub-bullets, max 100 words/slide

* **Slide separator**: Dùng `---` giữa các slides (Slidev convention)

* **Layout front matter**: Mỗi slide PHẢI có layout specification trong front matter block

* **Projector contrast**: Đảm bảo text/background contrast ratio >= 4.5:1 (WCAG AA). Theme đã chọn sẽ handle phần lớn, nhưng vẫn cần verify

## Important Notes

* Chỉ tạo text-only slides, không hình ảnh

* Vietnamese fonts: `Tahoma, Arial, sans-serif` (qua Slidev fonts config, `provider: none`)

* Chi tiết quy tắc outline: xem `references/outline-rules.md`

* Slidev Markdown templates cho slide types: xem `references/slide-templates.md`

* Theme do user chọn từ Slidev ecosystem, không cần custom CSS

* Slidev project có thể chạy local bằng `pnpm dev` để preview slides trong browser

* PDF export dùng Playwright (cần `playwright-chromium` dependency)

