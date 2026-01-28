---
name: video-production
description: 端到端视频制作 playbook（策划→素材规范→剪辑→字幕→导出→发布→验收），强调可复现的交付流程。
---

# 视频制作（从 Brief 到交付）

## When to use this skill
- 需要把碎片素材（口播/B-roll/屏录/图片/字幕）剪成可验收的成片。  
- 需要适配多平台比例（16:9 / 9:16 / 1:1）并遵循导出规格。  
- 需要“可复现”的交付：素材清单、剪辑决策、导出参数、验收记录可追溯。

## 必备输入
1) **受众与目标**：希望观众做什么（了解/转化/培训/投放）？成功指标？  
2) **平台与比例**：YouTube / B 站 / TikTok / Reels / 内部培训；目标分辨率/帧率。  
3) **时长与结构**：开头 hook（前 3–10 秒）、主体、结尾 CTA；是否需要章节/时间轴。  
4) **品牌规范**：字体/色板/Logo/水印/片头片尾/字幕样式（字号/描边/阴影/高亮规则）。  
5) **音频要求**：是否降噪/配乐/旁白；响度与 true peak 目标（常用参考：-14 LUFS / -1 dBTP）。  
6) **交付物**：MP4 + 字幕（SRT/VTT）+ 封面图 + 变更说明；是否需要 fast start。

## 工作流
1. **预制作**：写脚本（旁白+强调词+停顿点）、镜头单（镜头类型/时长/所需素材）、资产清单（来源/授权）。  
2. **素材预检**：抽检分辨率、帧率、像素宽高比、时长、编码器/码率、音频采样率/声道、是否 VFR。  
3. **粗剪 → 精剪**：先跑通结构，再控节奏与信息密度（口播“可理解、可跟上、可复述”）。  
4. **声音优先**：人声明晰优先于画面高级感；配乐给人声留空间。  
5. **画面统一**：最小必要调色（统一曝光/白平衡/对比度）；避免每段素材像不同片子。  
6. **字幕与可访问性**：移动端优先（字号、对比度、安全边距）；关键术语一致；公开视频建议同时交付“烧录版+独立字幕文件版”。  
7. **导出**（YouTube SDR 参考）：容器 MP4；视频 H.264 progressive/high profile（常见 4:2:0）；音频 AAC 48kHz；fast start；1080p 约 8 Mbps（24/25/30fps）或 12 Mbps（48/50/60fps）；4K 约 35–68 Mbps；响度 -14 LUFS，true peak ≤ -1 dBTP。  
8. **发布与验收**：逐条勾验（画面无黑帧/比例正确、声音无爆音且响度达标、字幕对齐、导出帧率/码率符合平台、fast start 生效），记录变更与已知限制。

## 本仓库工具链说明
- 当前仓库不提供内建视频处理工具链；请根据团队规范选择并记录使用的外部工具与版本。

## 参考资料
- YouTube 上传建议：https://support.google.com/youtube/answer/1722171  
- Adobe 导出参数权衡：https://www.adobe.com/creativecloud/video/hub/guides/best-export-settings-for-premiere-pro.html  
- APU：YouTube 响度目标（-14 LUFS / -1 dBTP）：https://apu.software/youtube-audio-loudness-target/  
- APU：常见平台响度目标表（含 EBU R128）：https://apu.software/loudness-standards/  
- W3C WAI：字幕（Prerecorded）资源：https://www.w3.org/WAI/WCAG22/Understanding/captions-prerecorded.html
