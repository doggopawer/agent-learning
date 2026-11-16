---
title: "공통 학습 공간과 수동 실행 명령 검증"
type: setup-report
assessment_status: not-assessed
approval_status: setup-only
tags: [learning, verification]
---

# 2026-11-16 — 공통 학습 공간과 수동 명령

[학습 홈](../index.md) · [진행 방법과 실행 명령](../learning-workflow.md)

사용자는 특정 프로젝트에 종속되지 않는 학습 공간으로 전환하고, 자동 실행 프롬프트 대신 직접 실행하는 명령을 만들도록 승인했다.

## 적용

- 작업공간을 `markestream-learning`에서 `agent-learning`으로 이동했다.
- `learn`이 현재 프로젝트 또는 지정한 프로젝트를 선택해 별도 Codex CLI 학습 세션을 연다. 프로젝트 없는 공통 개념 모드도 지원한다.
- 두 스킬은 명시적 호출 전용이다. 원본 개발 프로젝트에 자동 호출 문구·훅·전역 스킬·셸 설정을 추가하지 않았다.
- 기존 실제 노트·미응답 진단·평가를 `markestream` 프로젝트 아래 보존했다. 사용자 필기와 기존 승인 대기 상태를 유지했다.
- 공통 개념과 프로젝트 적용을 분리하고 평가 범위 지문에 프로젝트 ID·절대 경로를 포함했다.

## 실행 검증

| 항목 | 관찰 |
| --- | --- |
| 단위·런처 통합 검증 | 20개 합성 사례 통과 |
| 스킬 형식 | 두 스킬 모두 `quick_validate.py` 통과 |
| 호출 정책 | 두 `openai.yaml` 모두 `allow_implicit_invocation: false` |
| 실제 프로젝트 `learn --dry-run` | MarkeStream을 읽기 대상으로 선택하고 `agent-learning`을 쓰기 작업공간으로 지정 |
| 노트 근거 | 노트 1개·근거 9개 오류 없음 |
| 기존 사용자 필기 | 자동 생성 영역 밖 텍스트 동일 |
| 미응답 실제 평가 | `eligible: false`, 종료 코드 2 |
| 문서 링크·JSON | 검사 통과 |

런처의 실제 프로세스 교체는 임시 가짜 `codex` 실행 파일로 인자 전달을 검증했다. 공백·셸 특수문자가 포함된 주제도 한 인자로 전달되고 원본 폴더에 쓰기가 없었다. 실제 AI 세션·로그인·모델 응답은 이번 설정 검증에서 실행하지 않았다.

## 원본의 동시 변경

작업 전후 비교에서 Git HEAD는 같았고 추적 파일 937개 중 다음 3개의 동시 변경이 감지됐다. 이번 작업의 파일 수정 대상은 학습 작업공간뿐이며 아래 변경을 되돌리거나 덮어쓰지 않았다.

- `apps/admin-web/AGENTS.md`
- `infra/keycloak/themes/README.md`
- `infra/keycloak/themes/addock/login/resources/css/addock-login.css`

따라서 원본 전체 상태가 작업 전과 같다고 주장하지 않는다. 해당 변경 외 추적 파일 934개는 비교 시 해시가 같았다. 학습 도구가 참조한 코드·설계 근거 9개는 지문 검사에 통과했다. 제품 빌드·테스트·DB·인프라 작업은 수행하지 않았다.
