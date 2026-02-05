---
name: paper-digest
description: Generate shareable paper summaries for Discord/Slack/Twitter. Use when user provides arxiv paper(s) and wants a digestible summary to share. Triggers on phrases like "논문 요약", "paper summary", "share this paper", "디스코드에 공유", "summarize for sharing". Produces insight-centered single-paragraph summaries that explain WHY research matters, not just WHAT it does.
---

# Paper Digest

Single-paragraph summaries optimized for social sharing. Insight over information.

## Structure

1. **Context**: What's the problem?
2. **Insight**: What did they realize that others missed?
3. **Solution**: How does insight → method? (should feel natural)
4. **Evidence**: Concrete comparison showing it works

Then: Implication line + 📎 arxiv link

## Key Rules

* Explain like reader is smart but unfamiliar with the domain
* Use concrete examples/analogies (e.g., "쓰레기통 역할" >> "특정 토큰에 집중")
* Show cause-and-effect chains explicitly
* Compare/contrast with alternatives ("X failed while Y succeeded")
* Bold 2-4 key concepts
* Match user's language (Korean/English)

## Example

**Input**: arXiv 2601.15380

**Output**:

Transformer의 attention은 "어떤 토큰을 얼마나 볼지"를 결정하는데, 이 논문은 softmax attention을 **Entropic Optimal Transport(EOT)**라는 최적화 문제의 해로 재해석한다. 이 관점이 주는 통찰은: attention 계산에는 암묵적으로 "모든 위치가 동등하게 중요하다"는 uniform prior가 숨어있다는 것이다. 이게 왜 문제인가? LLM에서 첫 번째 토큰이 의미와 무관하게 엄청난 attention을 받는 attention sink 현상이 있다. Softmax는 합이 1인 확률을 출력해야 하므로, query가 마땅히 볼 토큰이 없을 때 attention을 "버릴 곳"이 필요한데, uniform prior 하에서 이를 구현하려면 첫 토큰의 key vector가 "나는 쓰레기통이야"라는 구조적 정보까지 담아야 한다—원래 semantic content만 표현해야 할 key의 표현력이 낭비되는 것이다. EOT 해석이 이 문제를 드러내주었으므로, 해결책도 자연스럽다: prior를 uniform에서 learnable로 바꾸면 된다. 이 논문이 제안하는 GOAT은 "각 위치의 기본 중요도"를 별도의 학습 가능한 항으로 분리해서, key vector는 순수하게 의미만, 위치 정보는 prior가 담당하게 한다. 실험에서 기존 방법들이 훈련 길이 초과 시 급격히 실패한 반면, GOAT은 긴 문맥에서도 정보 검색 성능을 유지했다.

**Implication**: EOT 관점은 attention의 숨겨진 가정을 드러내고, 그 가정을 바꿀 수 있다는 설계 자유도를 열어준다—attention sink는 uniform prior의 부산물이며, prior를 명시적으로 모델링하면 해결된다.

📎 https://arxiv.org/abs/2601.15380

## Avoid

* Jargon without intuition
* Findings without comparison to alternatives
* Method description without motivation ("왜 이렇게 했는지" 없이 "이렇게 했다"만)

## Multiple Papers

When summarizing multiple papers:
* Lead with the unifying theme/problem
* Contrast what each paper realized differently
* Synthesize implications across papers

## Language

Match the user's language (Korean/English). Maintain the same insight-first structure regardless of language.
