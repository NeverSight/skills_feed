---
name: deep-learner
description: Transform raw content (text/URL) into structured learning documents with 6-phase framework combining AI analysis + reflection prompts. Use when the user wants to deeply understand content, create study notes, or learn from articles/books/documents. Triggers on "learn this", "deep learn", "study this", "tạo tài liệu học", "phân tích nội dung", "hiểu sâu", or "deep learner".
---

# Deep Learner

Chuyển hóa nội dung thô thành tài liệu học có cấu trúc 6 phase. Kết hợp AI-analysis + reflection prompts, output tiếng Việt, giữ thuật ngữ gốc.

## Workflow

### Step 1: Detect Input

- If user provides a URL → use `WebFetch` to retrieve content
- If URL fails → ask user to paste text directly
- If user provides text → use directly

### Step 2: Choose Level

Use `AskUserQuestion` to ask:

```
Bạn muốn học ở mức độ nào?
- quick: Nắm nhanh ý chính (~2-3 trang)
- medium: Hiểu đủ sâu để áp dụng (~5-8 trang) (Recommended)
- deep: Hiểu thấu đáo, phản biện (~10-15 trang)
```

### Step 3: Choose Save Location

Use `AskUserQuestion` to ask save directory (default: `./learning-notes/`).

### Step 4: Analyze & Generate

Phân tích nội dung theo phases tương ứng level, follow [output-template.md](templates/output-template.md).

Mỗi khái niệm trọng tâm (Phase 2.1) dùng format What/Why/How/Example — xem [note-structure.md](templates/note-structure.md).

### Step 5: Save File

Tạo directory nếu chưa tồn tại. Save output markdown với naming: `{topic-slug}-{YYMMDD}-{HHMM}.md`

Ví dụ: `learning-notes/atomic-habits-chapter-1-260213-1430.md`

## Level → Phase Mapping

| Level  | Phases included  | Output       |
| ------ | ---------------- | ------------ |
| quick  | 1, 5.1, 5.2      | ~2-3 trang   |
| medium | 0, 1, 2, 5.1-5.3 | ~5-8 trang   |
| deep   | 0, 1, 2, 3, 4, 5 | ~10-15 trang |


## Phase Instructions

### Phase 0 — Chuẩn bị `[medium, deep]`

- AI gợi ý context dựa trên tiêu đề/chủ đề
- Tạo 2-3 reflection prompts với `> [Ghi câu trả lời của bạn ở đây]`
- Gợi ý: "Bạn đã biết gì về chủ đề này?", "Kỳ vọng gì khi đọc?"

### Phase 1 — Tổng quan `[quick, medium, deep]`

- Mục đích & bài toán nội dung giải quyết
- Cấu trúc nội dung (content map)
- Luồng logic của tác giả
- **Bản đồ vị trí**: Nội dung nằm ở đâu trong hệ thống kiến thức lớn hơn?
- Mối liên hệ giữa các phần

### Phase 2 — Đào sâu `[medium, deep]`

- **2.1 Khái niệm trọng tâm** — mỗi concept dùng What/Why/How/Example
- **2.2 Kết nối kiến thức** — AI gợi ý liên hệ + reflection prompts
- **2.3 Ứng dụng thực tế** — AI đề xuất ứng dụng + reflection prompts

### Phase 3 — Kiểm chứng `[deep]`

- Đánh giá bằng chứng/nguồn trích dẫn
- Phân tích độ tin cậy
- Flag thông tin cần fact-check
- Đánh giá tính thời sự

### Phase 4 — Góc nhìn đa chiều `[deep]`

- **4.1 Phản biện**: điểm yếu, thiên kiến tác giả
- **4.2 Góc nhìn khác**: chuyên gia phản biện, so sánh quan điểm
- **4.3 Giới hạn áp dụng**: khi nào KHÔNG phù hợp, điều kiện tiên quyết, rủi ro

### Phase 5 — Đúc kết `[quick, medium, deep]`

- **5.1 Tổng hợp**: tư tưởng cốt lõi, 3 keywords, giải thích cho người chưa biết
- **5.2 Sơ đồ hóa**: Mermaid diagram visualize cấu trúc ý chính
- **5.3 Cam kết hành động** `[medium, deep]`: reflection prompts với AI gợi ý

## Reflection Prompt Pattern

Mỗi reflection prompt gồm:

1. Câu hỏi AI gợi ý (in nghiêng)
2. Khoảng trống để user điền

```markdown
*AI gợi ý: Kiến thức này liên hệ thế nào với công việc hiện tại của bạn?*
> [Ghi câu trả lời của bạn ở đây]
```

## Edge Cases

- **Nội dung >10000 từ**: Recommend chia nhỏ theo chapter/section
- **Nội dung <500 từ**: Auto-suggest level quick
- **URL không fetch được**: Fallback yêu cầu paste text
- **Nội dung không phải text** (video/image): Suggest dùng transcript hoặc `ai-multimodal` trước

## Constraints

- Output tiếng Việt, giữ thuật ngữ gốc (technical terms)
- Template là guideline, AI tự adaptive theo nội dung
- Không thêm thông tin ngoài nội dung gốc (trừ context positioning ở Phase 1)
- Mermaid diagram phải đúng syntax, tối đa 10-15 nodes
- Reflection prompts: AI gợi ý hướng suy nghĩ, không trả lời thay user
