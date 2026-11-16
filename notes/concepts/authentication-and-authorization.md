---
title: "인증과 인가"
type: concept
project_id: null
learning_status: not-started
experiment_status: not-run
created: "2026-11-16"
tags: [learning]
---

# 인증과 인가

[학습 목차](../index.md)

<!-- learning:auto:start -->
<!-- learning:context {"kind": "concept", "project_id": null} -->
확인일: 2026-11-16 · 이번 학습의 제품 실행 검증: 미실행

공통 개념 학습: 특정 프로젝트의 코드·비즈니스 이해를 검증한 기록이 아니다.

## 한 문장으로

사용자 신원 확인과 특정 대상에 대한 작업 허용 판단을 구분하는 학습 주제다.

## 왜 필요한가

로그인한 사용자가 어느 회사에 어떤 작업을 할 수 있는지 코드와 업무 규칙을 연결하기 위해 공부한다.

## 비즈니스 규칙

- 이 노트는 준비 자료이며 사용자 답변이나 이해도 통과 기록이 없다.
- MarkeStream의 회사 생성 사례에서는 회사 범위와 client.create 권한을 확인하는 현재 코드·명세를 함께 읽는다.

## 실제 처리 흐름

[광고주 회사 생성](../projects/markestream/client-company-creation.md)에서 요청 주체 → 대상 대행사 → 생성 권한 검사 → 저장 호출을 추적한다.

[진단 세션](../sessions/markestream/client-company-creation.md)에서 로그인 성공과 작업 허용 판단의 차이를 자신의 말로 설명한다.

## 설계 근거와 해석

[계층별 책임과 요청 흐름](layered-request-flow.md)과 연결하는 이유: 주체 정보와 권한 검사가 어떤 메서드를 거쳐 전달되는지 찾기 위해서다.

[트랜잭션 경계](transaction-boundaries.md)와 연결하는 이유: 이 업무에서 권한 확인과 데이터 변경의 위치·순서를 함께 보기 위해서다.

현재의 적용 근거는 연결한 프로젝트 노트에 있으며, 다른 프로젝트의 권한 규칙까지 같다고 일반화하지 않는다. [전체 학습 지도](../maps/learning-map.md)

## 문서를 덮고 답하기

1. 로그인이 성공했는데 회사 생성이 거절될 수 있는 조건을 설명할 수 있는가?
2. 실제 코드에서 작업 주체·대상 회사·생성 권한이 각각 어디에 전달되는가?
<!-- learning:auto:end -->

## 내 설명과 질문

아직 답변하지 않음. 이 영역은 자동 갱신 시 보존된다.
