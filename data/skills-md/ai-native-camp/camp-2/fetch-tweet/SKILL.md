---
name: fetch-tweet
description: This skill should be used when the user asks to "트윗 가져와", "트윗 번역", "X 게시글 읽어줘", "tweet fetch", "트윗 내용", "트윗 원문", or provides an X/Twitter URL (x.com, twitter.com) and wants to read, translate, or analyze the tweet content. Also useful when other skills need to fetch tweet text programmatically.
---

# Fetch Tweet

X/Twitter URL에서 트윗 원문, 작성자 정보, 인게이지먼트 데이터를 가져오는 스킬.
FxEmbed 오픈소스 프로젝트의 API (`api.fxtwitter.com`)를 활용하여 JavaScript 없이 트윗 데이터를 추출한다.

## How It Works

X/Twitter URL의 도메인을 `api.fxtwitter.com`으로 변환하면 JSON으로 트윗 전체 데이터를 반환한다.

```
https://x.com/user/status/123456
  → https://api.fxtwitter.com/user/status/123456
```

## Script

`scripts/fetch_tweet.py` - 표준 라이브러리만 사용, 외부 의존성 없음.

```bash
# 기본 사용 (포맷팅된 출력)
python scripts/fetch_tweet.py https://x.com/garrytan/status/2020072098635665909

# JSON 출력 (프로그래밍 활용)
python scripts/fetch_tweet.py https://x.com/garrytan/status/2020072098635665909 --json
```

지원 URL 형식: `x.com`, `twitter.com`, `fxtwitter.com`, `fixupx.com`

## API Response Fields

| 필드 | 설명 |
|------|------|
| `tweet.text` | 트윗 본문 (URL 확장됨) |
| `tweet.author` | 작성자 (name, screen_name, bio, followers) |
| `tweet.likes/retweets/replies/bookmarks/views` | 인게이지먼트 |
| `tweet.created_at` | 작성 일시 |
| `tweet.media` | 첨부 미디어 (photos, videos) |
| `tweet.quote` | 인용 트윗 (동일 구조) |
| `tweet.lang` | 언어 코드 |

## Workflow

### 단일 트윗 가져오기

1. URL에서 screen_name과 status_id를 추출
2. `scripts/fetch_tweet.py <url>` 실행
3. 결과를 사용자에게 표시하거나 번역

### 번역 요청 시

1. 스크립트로 원문 fetch
2. 가져온 텍스트를 한국어로 번역하여 제공
3. 인게이지먼트 수치도 함께 표시

### 다른 스킬과 연동

Contents Hub 등에서 수집한 X URL 목록을 일괄 처리할 때:

```bash
# JSON 출력으로 파이프라인 연동
python scripts/fetch_tweet.py <url> --json | python3 -c "import sys,json; print(json.load(sys.stdin)['tweet']['text'])"
```

## WebFetch Fallback

스크립트 실행이 어려운 경우 WebFetch 도구로 직접 API 호출 가능:

```
URL: https://api.fxtwitter.com/{screen_name}/status/{status_id}
Prompt: "Extract the full tweet text and author name"
```

## Limitations

- 비공개 계정 트윗은 조회 불가
- 삭제된 트윗은 조회 불가
- API rate limit은 FxEmbed 서버 정책에 따름 (일반 사용 수준에서는 문제 없음)
