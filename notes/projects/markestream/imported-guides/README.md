---
title: "MarkeStream 기술 위키"
type: "guide-archive"
source_project: "markestream"
imported_from: "docs/README.md"
imported_at: "2026-11-16"
source_sha256: "387472887c8508af14d7db4b0f4c44161b939d0ed67795bcd64aae47da201099"
import_review: "not-reassessed"
tags: ["learning", "imported", "markestream"]
---

> [!info] 마케스트림 docs에서 이관한 기록
> 이전 경로: `docs/README.md` · 이관일: 2026-11-16 · 원본 정리일: 2026-11-16. 이관 후 사용자의 요청으로 원본 파일을 정리했다. 본문 안의 날짜·구현·검증·학습 상태는 작성 당시의 기록이며, 이관·삭제만으로 현재 상태를 다시 검증한 것은 아니다.
> [이관 목차](../imported-learning.md) · [현재 대화·자기 언어 학습 방법](../../../learning-workflow.md)

> [!note] 이전 안내·양식 보관
> 원문에 남아 있는 명령·기록 위치·실습 권장은 이전 작업 방식의 기록이다. 현재 진행에는 위의 공통 학습 방법과 보관함 양식을 사용한다.

# MarkeStream 기술 위키

마케스트림을 만들며 배운 개념, 기술 선택의 이유, 실제 실험 결과를 코드와 함께 기록한다. 대화에서 이해한 내용을 내 말과 그림으로 정리하고, 구현에서 확인한 결과를 다시 문서에 반영한다.

**처음 시작한다면:** [학습·기록 방법](learning-guide.md) → [현재 시스템과 요청 흐름](../architecture/system-overview.md) → [로컬 요청 흐름 실험](../labs/local-request-flow.md) 순서로 읽는다.

## 어디에 기록할까?

| 위치 | 기록할 내용 | 시작 문서 |
| --- | --- | --- |
| `concepts/` | 왜 필요한지, 동작 흐름, 헷갈린 점, 내 말로 설명하기 | 아래 개념 목차 |
| `architecture/` | 현재 구현과 앞으로 구축할 구조, 코드 근거 | [시스템 개요](../architecture/system-overview.md) |
| `adr/` | 선택한 기술, 대안, 이유, 감수할 점 | [MySQL 현행 기록](../adr/001-mysql.md) · [Traefik 제안](../adr/002-traefik.md) · [백엔드 코드 기준](../adr/003-backend-code-conventions.md) · [MVP 실행 경계](../adr/004-mvp-runtime.md) |
| `labs/` | 재현 절차, 예상, 실제 결과, 증거, 다음 실험 | [로컬 흐름](../labs/local-request-flow.md) · [Pod 복구](../labs/pod-failover.md) |
| `sessions/` | 그날 질문과 관련 문서 링크, 남은 질문 | [첫 기록](../../../sessions/markestream/2026-11-11-learning-wiki.md) |
| `templates/` | 새 문서를 만들 때 복사할 양식 | [개념](../imported-templates/concept.md) · [ADR](../imported-templates/adr.md) · [실험](../imported-templates/lab.md) · [학습 세션](../imported-templates/session.md) |

## 첫 번째 학습 챕터: 네트워크와 요청 흐름

모든 개념 노트는 **학습 중**, 모든 실험은 **미실행**으로 시작한다. 문서를 작성했다는 이유만으로 이해나 실험 완료를 표시하지 않는다. 상태의 기준은 [학습 가이드](learning-guide.md)에 있다.

| 순서 | 읽을 노트 | 스스로 설명해 볼 질문 |
| --- | --- | --- |
| 1 | [VPC와 Subnet](../../../concepts/networking/vpc-subnet.md) | Public과 Private은 무엇으로 나뉘나? |
| 2 | [NAT Gateway](../../../concepts/networking/nat-gateway.md) | 서버가 외부 API를 호출하는 것과 외부 사용자가 서버에 접속하는 것은 어떻게 다른가? |
| 3 | [Security Group](../../../concepts/networking/security-group.md) | 경로가 있는데도 접속이 안 되는 이유는 무엇일까? |
| 4 | [Node와 Pod](../../../concepts/kubernetes/node-pod.md) | EC2, Node, Pod, Container는 어떻게 연결되나? |
| 5 | [Control Plane](../../../concepts/kubernetes/control-plane.md) | 사용자 요청마다 제어 노드를 통과할까? |
| 6 | [Service와 Ingress](../../../concepts/kubernetes/service-ingress.md) | Pod가 교체돼도 같은 이름으로 요청하려면? |
| 7 | [ALB](../../../concepts/traffic/alb.md) | 요청 분산과 Pod 복구는 누가 담당하나? |
| 8 | [Traefik](../../../concepts/traffic/traefik.md) | Ingress 규칙을 실제 요청 전달로 연결하는 것은 무엇인가? |
| 9 | [API Gateway와 사용량 제한](../../../concepts/backend/api-gateway.md) | 마지막 1회가 남았을 때 동시 요청 둘을 어떻게 처리할까? |
| 10 | [서비스 분리와 MSA](../../../concepts/backend/msa.md) | 폴더 분리와 독립적으로 배포하는 서비스는 어떻게 다른가? |

## 기존 제품·개발 설계

기존 문서는 제품 범위와 목표 설계를 담는다. 실제 구현 여부는 [현재 시스템 개요](../architecture/system-overview.md)의 코드 근거와 함께 확인한다.

- [01. PRD](../reference/01-prd.md)
- [02. 시스템 아키텍처 초안](../reference/02-system-architecture.md)
- [03. ERD](../reference/03-erd.md)
- [04. API 명세](../reference/04-api-spec.md) · [OpenAPI 계약](file:///Users/dhkim/Desktop/ml-project/markestream/contracts/openapi.yaml)
- [05. 프로젝트 구조와 CI/CD 설계](../reference/05-project-cicd.md)
- [06. MVP 구현 및 검증 현황](../reference/06-mvp-status.md)
- [07. 계정·회사·권한그룹](../reference/07-permissions.md) · [ADR-005](../adr/005-account-permission-groups.md)
- [08. 회사 등록·검증·초대](../reference/08-registration.md) · [ADR-006](../adr/006-company-registration.md)
- [프로젝트 실행 안내](file:///Users/dhkim/Desktop/ml-project/markestream/README.md)

## 다음에 할 일

1. 시스템 개요를 읽고 현재 로컬 환경의 요청 흐름을 문서를 보지 않고 설명한다.
2. 로컬 요청 흐름 실험을 수행한 뒤 실제 결과를 기록한다.
3. 학습 중 생긴 질문은 해당 개념 노트에 추가하고, 그날 세션에는 링크만 남긴다.
4. Kubernetes 실험은 클러스터와 배포 설정을 마련한 뒤 진행한다.

초기 작성: 2026-11-11. 「마케팅 플랫폼 이름 제안」 채팅의 마지막 학습 방법 제안과 확인 가능한 최근 대화, 현재 저장소를 바탕으로 시작했다. 전체 과거 대화를 빠짐없이 옮긴 기록은 아니다.
