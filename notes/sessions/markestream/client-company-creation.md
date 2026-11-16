---
title: "광고주 회사 생성 — 첫 이해도 진단"
type: session
project_id: markestream
assessment_status: pending
approval_status: pending
tags: [markestream, learning, assessment]
---

# 광고주 회사 생성 — 첫 이해도 진단

[학습 홈](../../index.md) · [학습 진행 방법](../../learning-workflow.md)

지금은 학습 시스템의 설치만 승인되었다. 아래 질문에 대한 실제 사용자 답변은 없으며, 제품 변경 요청·평가 통과·구현 승인도 없다.

## 먼저 답해 볼 질문

1. **기술:** 회사 저장과 생성자 담당 배정을 하나의 트랜잭션에서 처리하는 이유는 무엇일까? 배정 중 오류가 나면 어떤 결과를 기대하는가?
2. **비즈니스:** 광고주 회사를 생성하면 광고주 로그인 계정도 생성되는가? 이 동작을 누가 수행할 수 있고 어느 대행사에 속한 회사가 되는가?
3. **코드:** `ClientCompanyController.registerClientCompany`에서 시작해 권한 확인, 저장, 담당 배정까지 담당 파일과 메서드를 찾아 설명해 볼 수 있는가?

| 영역 | 실제 답변 | 상태 |
| --- | --- | --- |
| 기술 | 미응답 | pending |
| 비즈니스 | 미응답 | pending |
| 코드 | 미응답 | pending |

## 답변 후 사용할 참고 노트

[광고주 회사 생성과 권한 경계](../../projects/markestream/client-company-creation.md). 멘토는 사용자의 설명을 먼저 듣고 필요한 부분만 보충한다.

## 연결된 개념과 학습 순서

1. [계층별 책임과 요청 흐름](../../concepts/layered-request-flow.md): 실제 호출 경로를 먼저 찾는다.
2. [트랜잭션 경계](../../concepts/transaction-boundaries.md): 여러 저장 단계의 범위와 실패 시 예상 결과를 설명한다.
3. [인증과 인가](../../concepts/authentication-and-authorization.md): 요청 주체·대상 회사·작업 권한을 구분한다.

[학습 연결 지도](../../maps/learning-map.md)에서 각 개념과 이 세션의 관계를 볼 수 있다. 위 항목은 준비된 학습 경로이며 실제 학습 완료를 뜻하지 않는다.

## 평가와 승인

구조화된 기록은 학습 작업공간의 `records/gates/markestream/client-company-creation.json`에 있다. 구현 범위는 아직 정하지 않았다. 학습 자료를 만들었다는 이유로 통과시키지 않는다.
