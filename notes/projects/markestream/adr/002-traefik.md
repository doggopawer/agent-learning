---
title: "ADR-002: 스테이징의 HTTP 진입점에 Traefik 사용 제안"
type: "adr-snapshot"
source_project: "markestream"
imported_from: "docs/adr/002-traefik.md"
imported_at: "2026-11-16"
source_sha256: "219988890b7b31b2a6ea5e78b51b657a96fd2bce534ae2ca33f72c9768b6fe31"
import_review: "not-reassessed"
tags: ["learning", "imported", "markestream"]
---

> [!info] 마케스트림 docs에서 이관한 기록
> 이전 경로: `docs/adr/002-traefik.md` · 이관일: 2026-11-16 · 원본 정리일: 2026-11-16. 이관 후 사용자의 요청으로 원본 파일을 정리했다. 본문 안의 날짜·구현·검증·학습 상태는 작성 당시의 기록이며, 이관·삭제만으로 현재 상태를 다시 검증한 것은 아니다.
> [이관 목차](../imported-learning.md) · [현재 대화·자기 언어 학습 방법](../../../learning-workflow.md)

# ADR-002: 스테이징의 HTTP 진입점에 Traefik 사용 제안

- 작성 / 갱신: 2026-11-11
- 상태: 제안 — 기존 설계 초안의 내용을 기록
- 대상 환경: 스테이징
- 검증: 배포 설정 없음 / 실험 미실행

## 배경과 요구

[기존 아키텍처](../reference/02-system-architecture.md)와 [배포 설계](../reference/05-project-cicd.md)는 kubeadm 클러스터에서 관리자와 공개 요청을 각 API로 전달하는 Traefik 구성을 제안한다. 이 ADR은 그 방향을 추적하기 위한 기록이며 이번 문서 작성으로 도입을 확정하지 않는다.

## 대안

| 대안 | 검토할 점 | 현재 상태 |
| --- | --- | --- |
| Traefik을 Ingress Controller로 사용 | Kubernetes 라우팅, 직접 운영할 진입점과 TLS, 장애 대응 | 기존 설계의 제안 |
| AWS ALB를 활용한 진입점 | 대상 연결 방식, Kubernetes 연동, 운영 책임과 비용 | 비교 미실행 |
| 별도 API Gateway 추가 | 인증 연동·고객사 정책·사용량 관리 요구가 실제로 있는지 | 도입 필요성 미확정 |

이들은 기능이 일부 겹치며 조합할 수도 있다. 같은 위치의 완전히 동일한 제품이라는 전제로 비교하지 않는다. 원리는 [Traefik](../../../concepts/traffic/traefik.md), [ALB](../../../concepts/traffic/alb.md), [API Gateway](../../../concepts/backend/api-gateway.md)에 정리했다.

## 제안과 책임

Traefik은 호스트·경로 라우팅을 맡고, 대행사 소속과 업무 권한은 API에서 검사하는 안이다. 고객사별 일일 할당량은 별도 요구와 구현으로 판단한다.

## 구축 전에 결정할 것

- 사용할 버전과 설정 방식, Ingress 및 Service 설정
- 외부에서 Traefik까지 도달하는 경로와 단일 진입점 장애 대책
- 도메인·TLS 발급과 갱신, 관리자·공개 호스트 분리
- 복제본·노드 분산·readiness, Pod IP 직접 전달과 ClusterIP 경유 중 실제 설정
- 운영 비용과 유지보수 부담을 비교할 기준

## 검증과 채택 기준

관리·공개 경로 분리, 인증·인가 유지, 잘못된 호스트 처리, TLS, Pod 장애 시 동작을 확인한다. [Pod 복구 실험](../labs/pod-failover.md)은 준비 이후 수행할 항목이다. 채택하면 확인자·날짜·설정 경로·실험 결과를 추가한다.
