---
title: "마케스트림 기존 docs 이관 목차"
type: project-index
tags: [learning, imported, markestream]
---

# 마케스트림 기존 docs 이관 목차

[학습 홈](../../index.md) · [네트워크·요청 흐름 Canvas](../../maps/network-request-flow.canvas) · [전체 학습 Canvas](../../maps/learning-map.canvas)

기존 `markestream/docs`의 Markdown 문서 34개를 이 보관함으로 복사했다. 공통 개념 10개는 `notes/concepts/`에, 마케스트림 설계·ADR·실험·이전 안내는 프로젝트 자료로, 당시 세션은 학습 세션에 연결했다. 기존 본문과 자기 설명·미작성 상태를 보존하고 상대 링크를 새 위치에 맞췄다.

이관 문서는 이전 경로·당시 원본 SHA-256·이관일을 포함한다. 2026-11-16 사용자의 요청으로 기존 Markdown 원본을 삭제했으며, 이 문서들은 이 보관함에서 관리한다. 작성 당시의 구현·검증 기록을 현재 코드와 일치한다고 단정하거나 이번에 다시 실행한 결과로 취급하지 않는다. 이해도와 승인 상태는 유지했다.

## 대화로 이어가기

궁금하거나 헷갈리는 개념을 골라 질문을 주고받고, 한 주제가 정리되면 이해한 내용을 자기 말로 남긴다. [현재 학습 방법](../../learning-workflow.md)을 따른다. 이전 가이드의 실험 절차는 사용자가 원할 때만 참고한다.

## 공통 개념

| 분야 | 이관한 개념 | 원문 상태 |
| --- | --- | --- |
| 백엔드 구조·정책 | [API Gateway와 사용량 제한](../../concepts/backend/api-gateway.md) | 학습 중 · 자기 설명 미작성 상태 보존 |
| 백엔드 구조·정책 | [서비스 분리와 MSA](../../concepts/backend/msa.md) | 학습 중 · 자기 설명 미작성 상태 보존 |
| Kubernetes | [Control Plane](../../concepts/kubernetes/control-plane.md) | 학습 중 · 자기 설명 미작성 상태 보존 |
| Kubernetes | [Node와 Pod](../../concepts/kubernetes/node-pod.md) | 학습 중 · 자기 설명 미작성 상태 보존 |
| Kubernetes | [Service와 Ingress](../../concepts/kubernetes/service-ingress.md) | 학습 중 · 자기 설명 미작성 상태 보존 |
| 네트워크 | [NAT Gateway](../../concepts/networking/nat-gateway.md) | 학습 중 · 자기 설명 미작성 상태 보존 |
| 네트워크 | [Security Group](../../concepts/networking/security-group.md) | 학습 중 · 자기 설명 미작성 상태 보존 |
| 네트워크 | [VPC와 Subnet](../../concepts/networking/vpc-subnet.md) | 학습 중 · 자기 설명 미작성 상태 보존 |
| 요청 진입·라우팅 | [ALB](../../concepts/traffic/alb.md) | 학습 중 · 자기 설명 미작성 상태 보존 |
| 요청 진입·라우팅 | [Traefik](../../concepts/traffic/traefik.md) | 학습 중 · 자기 설명 미작성 상태 보존 |

## 시스템 구조와 설계 결정

- [ADR-001: 초기 데이터 저장소로 MySQL을 사용하는 현행 구성](adr/001-mysql.md)
- [ADR-002: 스테이징의 HTTP 진입점에 Traefik 사용 제안](adr/002-traefik.md)
- [ADR-003: 객체지향·함수형 구성과 JPA·Querydsl 접근 기준](adr/003-backend-code-conventions.md)
- [ADR-004: MVP의 실행 모듈과 로컬 게시·문의 경계](adr/004-mvp-runtime.md)
- [ADR-005: 회사·계정 분리와 공통 권한그룹](adr/005-account-permission-groups.md)
- [ADR-006: 회사 신청·승인과 이메일 초대](adr/006-company-registration.md)
- [현재 시스템과 요청 흐름](architecture/system-overview.md)

## 이관한 제품·개발 명세

- [AdDock 제품 요구사항](reference/01-prd.md)
- [AdDock 시스템 아키텍처](reference/02-system-architecture.md)
- [AdDock 데이터 모델과 ERD](reference/03-erd.md)
- [AdDock API 명세](reference/04-api-spec.md)
- [MarkeStream 프로젝트 구조와 CI/CD 설계](reference/05-project-cicd.md)
- [MVP 구현 및 검증 현황](reference/06-mvp-status.md)
- [AdDock 계정·회사·권한그룹](reference/07-permissions.md)
- [회사 등록·검증·초대](reference/08-registration.md)

## 기존 학습 세션과 선택 실험 기록

- [Lab: 로컬 광고주 등록 요청 따라가기](labs/local-request-flow.md)
- [Lab 계획: Pod 교체와 요청 처리 관찰](labs/pod-failover.md)
- [2026-11-11 — 마케스트림 학습 위키 시작](../../sessions/markestream/2026-11-11-learning-wiki.md)

## 이전 학습 안내

- [MarkeStream 기술 위키](imported-guides/README.md)
- [학습하고 기록하는 방법](imported-guides/learning-guide.md)

## 원본 양식

- [ADR-NNN: 결정 제목](imported-templates/adr.md)
- [개념 이름](imported-templates/concept.md)
- [실험 이름](imported-templates/lab.md)
- [YYYY-MM-DD — 학습 주제](imported-templates/session.md)

## 현재 학습과 연결

- [마케스트림 기능별 학습 순서](learning-roadmap.md): 기존 개념을 실제 기능과 연결해 질문할 때 참고한다.
- [광고주 회사 생성 대화](client-company-creation.md): 기존 로컬 요청 흐름 자료와 같은 업무를 다룬다.
- [계층별 책임과 요청 흐름](../../concepts/layered-request-flow.md): 모듈·역할 분리와 서비스 배포 분리의 차이를 함께 이야기할 수 있다.

## 원본 정리 결과

이관한 Markdown 원본 34개와 이전 위키 작성 규칙 `docs/AGENTS.md`는 삭제했다. 마케스트림의 루트·백엔드·프론트 `AGENTS.md`에서 해당 문서를 따르도록 한 참조를 제거하고 기존 개발 규칙은 유지했다. 제품 UI 점검 데이터 4개는 이관 대상이 아니므로 원본에 남겼다.

- [docs/ui/inquiry-alignment.json](file:///Users/dhkim/Desktop/ml-project/markestream/docs/ui/inquiry-alignment.json)
- [docs/ui/interaction-audit.json](file:///Users/dhkim/Desktop/ml-project/markestream/docs/ui/interaction-audit.json)
- [docs/ui/page-rollout.json](file:///Users/dhkim/Desktop/ml-project/markestream/docs/ui/page-rollout.json)
- [docs/ui/snowui-coverage.json](file:///Users/dhkim/Desktop/ml-project/markestream/docs/ui/snowui-coverage.json)

## 확인이 필요한 과거 코드 참조

`ADR-001`의 과거 `WorkspaceService.java` 경로는 현재 원본에 없다. 새 클래스로 임의 대응하지 않고 해당 참조를 당시 경로와 미확인 표시로 보존했다. 다른 문서·코드 링크는 이관 위치 또는 실제 원본으로 연결했다.

[파일별 출처·해시·이관 결과](file:///Users/dhkim/Desktop/ml-project/agent-learning/records/imports/markestream-docs-2026-11-16.json)
