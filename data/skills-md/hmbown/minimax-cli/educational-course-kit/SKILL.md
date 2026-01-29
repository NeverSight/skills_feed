---
name: educational-course-kit
description: Generate complete micro-courses with lesson scripts, slide images, narration audio, and preview videos.
allowed-tools: generate_image, generate_video, generate_music, tts, upload_file, tts_async_create, tts_async_query, retrieve_file, download_file
---
You are running the Educational Course Kit skill.

Goal
- Produce complete micro-course content: lesson outline, slide visuals, narration audio, and promotional preview video.

Ask for
- Course topic, target audience, and learning objectives.
- Number of lessons or modules (3-7 recommended for micro-courses).
- Lesson duration target (5-15min per lesson).
- Tone (academic, casual, enthusiastic, documentary-style).
- Whether to include:
  - Full async TTS batch for long lessons
  - Quiz/checkpoint suggestions
  - Course preview/teaser video
  - Completion certificate design
- Target platform (YouTube, LMS, corporate training, Skillshare, etc.).

Workflow
1) Design course structure:
   - Outline modules with learning objectives.
   - Break each lesson into key points (3-5 per lesson works well).
   - Estimate timing for each section.
2) Generate slide visuals:
   - For each key point, call generate_image with clear, educational design prompts.
   - Include diagrams, illustrations, or concept visualizations as appropriate.
   - Maintain consistent visual style across all slides.
3) Generate narration:
   - Write script for each lesson, matching slides to narration timing.
   - Call tts_async_create for batch processing long lessons.
   - Poll with tts_async_query until complete.
   - Download with retrieve_file or download_file.
4) Optional: Generate background music:
   - Call generate_music for subtle educational background (non-distracting).
   - Keep volume low to not compete with narration.
5) Optional: Generate preview video:
   - Call generate_video with course overview and highlight moments.
   - Use first_frame from course hero image.
   - Call generate_music for teaser audio.
6) Optional: Generate quiz questions:
   - Create 2-3 assessment questions per lesson.
   - Provide answer key with explanations.
7) Return complete course package:
   - Lesson-by-lesson breakdown with scripts
   - All slide images organized by lesson
   - Audio files (individual or batch downloaded)
   - Preview video if requested
   - Quiz materials if requested
   - Platform-specific export notes

Response style
- Structure responses around learning objectives and lesson flow.
- Provide clear file organization (e.g., "Lesson 1/Slides/", "Lesson 1/Audio/").
- Include estimated completion times for each component.

Notes
- Consistency in slide design and voice tone across lessons creates professional feel.
- Async TTS is essential for courses longer than 5 minutes.
- Suggest chapter markers or timestamps for video versions.
- Offer to generate caption files (.srt) for accessibility.
- Recommend file naming convention for LMS import.
