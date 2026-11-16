---
title: "모든 프로젝트에서 학습 멘토 한 줄 호출"
type: setup-report
assessment_status: not-assessed
approval_status: setup-only
tags: [learning, verification]
---

# 모든 프로젝트에서 학습 시작하기

[학습 홈](../index.md) · [진행 방법](../learning-workflow.md)

사용자는 앞으로 모든 프로젝트에서 복잡한 질문이나 터미널 프롬프트를 준비하지 않고 학습을 시작하고자 했다. 현재 컴퓨터의 사용자 스킬 경로에 두 스킬을 연결했다. 이전 설치 보고서에서 “전역 스킬을 추가하지 않음”은 당시 상태이며 이번 요청으로 변경됐다.

```text
$learning-mentor
```

현재 프로젝트의 Codex 채팅에 입력한다. 멘토는 현재 프로젝트를 선택하고 주제가 없으면 먼저 묻는다. 학습 노트는 공통 보관함에 기록한다. 자동 실행 정책은 두 스킬 모두 `allow_implicit_invocation: false`다.

검증에서 Codex app-server의 `skills/list`를 사용해 MarkeStream, 프로젝트 상위 폴더, 별도 임시 폴더 모두에서 두 스킬이 `scope: user`, `enabled: true`로 발견됨을 확인했다. AI 세션이나 제품 구현은 실행하지 않았다.

24개 도구 검증이 통과했다. 추가 검증은 현재 Git 하위 폴더에서 저장소 루트 선택, 공통 보관함 유지, 전역 심볼릭 링크에서 실제 스크립트 위치 해석, 기존 동명 스킬 보존과 설치 충돌 시 부분 설치 방지를 확인한다. 실제 사용자의 이해도·개발 승인은 여전히 별도 평가 대상이다.

새 컴퓨터에서는 저장소 루트의 `python3 -B scripts/install_skills.py`로 연결한다. 목록에 보이지 않으면 Codex를 재시작한다. [공식 스킬 문서](https://learn.chatgpt.com/docs/build-skills)의 사용자 스킬 경로·심볼릭 링크·명시적 호출 정책을 따른다.
