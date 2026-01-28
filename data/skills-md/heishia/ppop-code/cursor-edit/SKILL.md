---
name: cursor-edit
description: Cursor CLI를 통해 실제 코드 수정 수행. 분석/계획 결과를 받아 cursor-agent에게 전달하여 코드 편집을 위임한다. 코드 수정, 리팩토링, 기능 추가, 버그 수정 등 실제 파일 변경이 필요할 때 사용.
---

# Cursor Edit Skill

실제 코드 수정을 Cursor CLI에게 위임한다.

## 실행 방법

1. 입력받은 변경 명세를 임시 파일로 저장
2. scripts/apply.ps1 실행
3. cursor-agent 호출
4. 결과 반환

## 사용 시나리오

- 코드 리팩토링이 필요할 때
- 새 기능 구현이 필요할 때
- 버그 수정이 필요할 때
- 테스트 코드 작성이 필요할 때

## 입력

- prompt: 변경 요청 사항 (자연어)
- target_path: 대상 파일/폴더 경로 (선택)

## 에러 처리

- Cursor 연결 실패: 재시도 2회
- 타임아웃 (300초): 사용자에게 확인 요청
- 권한 오류: 사용자에게 알림

## 스크립트

scripts/apply.ps1 참조
