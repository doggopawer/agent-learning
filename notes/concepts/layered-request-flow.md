---
title: "계층별 책임과 요청 흐름"
type: concept
project_id: null
learning_status: learning
experiment_status: not-run
created: "2026-11-16"
tags: [learning]
---

# 계층별 책임과 요청 흐름

[학습 목차](../index.md)

<!-- learning:auto:start -->
<!-- learning:context {"kind": "concept", "project_id": null} -->
확인일: 2026-11-16 · 이번 학습의 제품 실행 검증: 미실행

공통 개념 학습: 특정 프로젝트의 코드·비즈니스 이해를 검증한 기록이 아니다.

## 한 문장으로

요청 진입점, 업무 조율, 도메인과 저장 역할을 나누어 실제 호출 흐름을 따라 읽는 학습 주제다.

## 왜 필요한가

메서드 하나만 보면 권한 확인·저장·응답 중 무엇을 담당하는지 놓칠 수 있다. 먼저 한 요청이 지나가는 위치를 찾아본다.

## 비즈니스 규칙

- 화면→API→서버→DB의 큰 흐름에 대한 첫 사용자 답변이 있다. 서버 역할과 실제 코드 설명은 학습 중이며 이해도 통과 기록은 없다.
- 각 계층의 구체적인 책임은 프로젝트의 현재 코드·규칙으로 확인한다.

## 실제 처리 흐름

학습 순서: 요청 진입점 찾기 → 호출하는 업무 메서드 찾기 → 권한·도메인·저장 호출 찾기 → 응답 위치 찾기.

실제 적용은 [광고주 회사 생성](../projects/markestream/client-company-creation.md), 답변 기록은 [진단 세션](../sessions/markestream/client-company-creation.md)에서 연결한다.

## 객체 생성과 DB 저장

서버는 요청을 받은 뒤 입력·권한 규칙을 확인하고 저장할 데이터를 구성한다. 서버 메모리에 객체를 만드는 단계와 DB에 데이터를 저장하도록 요청하는 단계를 구분해 읽는다.

[회사 생성의 실제 두 줄](../projects/markestream/client-company-creation.md#이번에%20읽을%20두%20줄)과 [사용자 답변·재질문](../sessions/markestream/client-company-creation.md)을 연결한다. 실제 테스트·실행 검증은 하지 않았다.

## 설계 근거와 해석

[트랜잭션 경계](transaction-boundaries.md)와 함께 보기: 여러 저장 단계를 조율하는 위치를 찾기 위해 연결한다.

[인증과 인가](authentication-and-authorization.md)와 함께 보기: 요청 주체와 작업 허용 여부를 어디서 확인하는지 추적하기 위해 연결한다.

[전체 학습 지도](../maps/learning-map.md)에서 현재 위치를 확인한다.

## 문서를 덮고 답하기

1. Controller와 Service가 각각 무엇을 맡는지 실제 메서드를 찾아 설명할 수 있는가?
2. 권한 확인이나 저장 코드를 바꾸면 어느 호출 경로에 영향을 줄까?
<!-- learning:auto:end -->

## 내 설명과 질문

첫 실제 답변은 [진단 세션](../sessions/markestream/client-company-creation.md)에 원문으로 기록했다. 현재는 학습 중이며 추가 질문에 대한 답변을 기다린다. 이 영역의 사용자 필기는 자동 갱신 시 보존한다.
