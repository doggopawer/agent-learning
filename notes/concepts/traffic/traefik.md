---
title: "Traefik"
type: "concept"
source_project: "markestream"
imported_from: "docs/concepts/traffic/traefik.md"
imported_at: "2026-11-16"
source_sha256: "3a1e48594c8346f949f9928ec195ea629b375d7655bc52f8fe5b41dc1c8fd91b"
import_review: "not-reassessed"
tags: ["learning", "imported", "markestream"]
learning_status: "learning"
---

> [!info] 마케스트림 docs에서 이관한 기록
> 이전 경로: `docs/concepts/traffic/traefik.md` · 이관일: 2026-11-16 · 원본 정리일: 2026-11-16. 이관 후 사용자의 요청으로 원본 파일을 정리했다. 본문 안의 날짜·구현·검증·학습 상태는 작성 당시의 기록이며, 이관·삭제만으로 현재 상태를 다시 검증한 것은 아니다.
> [이관 목차](../../projects/markestream/imported-learning.md) · [현재 대화·자기 언어 학습 방법](../../learning-workflow.md)

# Traefik

- 갱신: 2026-11-11
- 학습 상태: 학습 중
- 프로젝트 적용: 기존 아키텍처의 제안, 배포 미구현
- 실험 상태: 미실행

## 한 문장으로

Traefik은 요청을 백엔드로 전달하는 리버스 프록시이며, Kubernetes에서는 Ingress Controller로 사용할 수 있다.

## 왜 필요한가?

여러 서비스의 주소와 경로를 한 진입점에서 관리하고, Kubernetes의 서비스 정보가 바뀔 때 라우팅에 반영하고 싶기 때문이다.

## 어떻게 동작하는가?

호스트·경로 규칙으로 목적지를 찾고, 설정된 미들웨어를 거쳐 백엔드로 요청을 전달한다. Kubernetes의 Service 정보를 사용하며, Pod IP로 직접 전달하거나 설정에 따라 ClusterIP를 경유할 수 있다. [Traefik Kubernetes Ingress 라우팅](https://doc.traefik.io/traefik/reference/routing-configuration/kubernetes/ingress/)

## 헷갈린 점

Traefik을 설치해도 광고주 등록, 대행사 권한 검사, DB 저장이 자동으로 생기지는 않는다. 고객사별 일일 API 할당량 역시 별도의 정책·저장소·구현이 필요한지 확인해야 한다.

“Traefik을 쓰면 ALB가 언제나 불필요하다”는 결론도 피한다. 외부에서 Traefik까지 어떻게 도달하고 그 진입점에 장애가 생기면 어떻게 복구할지는 별도 설계 문제다.

## 마케스트림에서는?

[기존 아키텍처](../../projects/markestream/reference/02-system-architecture.md)는 관리 호스트와 공개 호스트를 구분하는 진입점으로 제안한다. 현재는 [Vite 프록시](file:///Users/dhkim/Desktop/ml-project/markestream/apps/admin-web/vite.config.ts)가 로컬 API 요청을 전달한다. [ADR-002](../../projects/markestream/adr/002-traefik.md)에 실제 구축 전에 확정할 항목을 기록했다.

## 실제로 검증했는가?

미실행. 먼저 호스트·경로 라우팅, TLS, readiness 반영, 실제 Pod 연결 경로를 확인하고 그 다음 복구 실험을 한다.

## 문서를 덮고 답하기

1. Traefik과 Spring Boot의 책임은 어디에서 나뉘는가?
2. API Pod가 둘이어도 Traefik 진입점 하나가 죽으면 무엇이 문제일까?

내 설명 / 복습 날짜: 아직 작성하지 않음.

[Service와 Ingress](../kubernetes/service-ingress.md) · [API Gateway](../backend/api-gateway.md) · [위키 목차](../../projects/markestream/imported-guides/README.md)

공식 자료 확인일: 2026-11-11.

## 공통 학습 보관함에서 이어가기

[네트워크·요청 흐름 Canvas](../../maps/network-request-flow.canvas) · [함께 이관한 개념과 프로젝트 자료](../../projects/markestream/imported-learning.md)

원문에 있는 내 설명·복습 기록을 유지한다. 아직 작성하지 않은 자기 설명을 이관 과정에서 대신 채우지 않았다. 앞으로의 대화에서 이해한 내용을 자기 말로 이어 적는다.
