---
title: "2026-11-11 — 마케스트림 학습 위키 시작"
type: "imported-session"
source_project: "markestream"
imported_from: "docs/sessions/2026-11-11-learning-wiki.md"
imported_at: "2026-11-16"
source_sha256: "3b08924d671566501523b49d93cc371e9219f0b927233fc43c582efe7d939a3c"
import_review: "not-reassessed"
tags: ["learning", "imported", "markestream"]
---

> [!info] 마케스트림 docs에서 이관한 기록
> 이전 경로: `docs/sessions/2026-11-11-learning-wiki.md` · 이관일: 2026-11-16 · 원본 정리일: 2026-11-16. 이관 후 사용자의 요청으로 원본 파일을 정리했다. 본문 안의 날짜·구현·검증·학습 상태는 작성 당시의 기록이며, 이관·삭제만으로 현재 상태를 다시 검증한 것은 아니다.
> [이관 목차](../../projects/markestream/imported-learning.md) · [현재 대화·자기 언어 학습 방법](../../learning-workflow.md)

# 2026-11-11 — 마케스트림 학습 위키 시작

## 오늘의 요청

「마케팅 플랫폼 이름 제안」 채팅에서 추천받은 학습 방법을 실제 `docs` 폴더로 만들어, 개발·구축·실험 중 배운 내용을 계속 정리하고 싶다.

확인한 범위는 해당 채팅의 마지막 학습 방법 제안과 최근 API Gateway 관련 대화, 현재 마케스트림 저장소다. 전체 과거 대화를 읽고 모든 기술 결정을 복원한 기록은 아니다.

## 정리한 내용

| 내용 | 문서 | 확인 수준 |
| --- | --- | --- |
| 개념·ADR·Lab을 나눠 기록하는 방법 | [학습 가이드](../../projects/markestream/imported-guides/learning-guide.md) | 작업 방식 정리 |
| 현재 로컬 요청 흐름과 목표 구조 | [시스템 개요](../../projects/markestream/architecture/system-overview.md) | 코드·설정 확인 |
| VPC·Subnet·NAT·Security Group | [네트워크 시작 노트](../../concepts/networking/vpc-subnet.md) | 공식 자료와 개념 정리 |
| Node·Pod·Control Plane·Service·Ingress | [Node와 Pod](../../concepts/kubernetes/node-pod.md) | 공식 자료와 개념 정리 |
| ALB·Traefik·API Gateway | [API Gateway](../../concepts/backend/api-gateway.md) | 최근 질문·공식 자료 정리 |
| 현재 MySQL 사용과 Traefik 제안 | [ADR-001](../../projects/markestream/adr/001-mysql.md) · [ADR-002](../../projects/markestream/adr/002-traefik.md) | 현행 코드 / 설계 제안 구분 |
| 바로 할 실험과 준비 후 할 실험 | [로컬 흐름](../../projects/markestream/labs/local-request-flow.md) · [Pod 복구](../../projects/markestream/labs/pod-failover.md) | 절차 작성, 미실행 |

## 내 말로 설명하기

아직 작성하지 않음. 학습자가 설명한 내용과 복습 날짜를 여기에 기록한다.

## 실행과 결정

이번에는 문서 구조와 초기 노트를 만들었다. 애플리케이션·인프라 실험은 실행하지 않았고, 새로운 기술 도입을 채택하지 않았다. 기존 코드의 MySQL 사용은 현행 구현 기록으로 남겼다.

## 다음 질문

- [ ] 현재 광고주 등록 요청이 어디에서 인증과 대행사 권한을 확인하는지 설명하기
- [ ] 로컬 요청 흐름 실험을 하고 예상과 실제 결과를 비교하기
- [ ] NAT를 제외하려는 테스트 환경에서 외부 통신은 어떤 경로로 처리할지 정하기
- [ ] Kubernetes 구축 때 Traefik까지의 외부 진입 경로와 노드 배치를 정하기
- [ ] 학습 중 새로 알게 된 내용을 기존 개념 노트에 반영하기
