---
title: "ADR-001: 초기 데이터 저장소로 MySQL을 사용하는 현행 구성"
type: "adr-snapshot"
source_project: "markestream"
imported_from: "docs/adr/001-mysql.md"
imported_at: "2026-11-16"
source_sha256: "b4d5ae9cb4e7e699b7f6ca393af9eb980016564e0494bba65b44f13190bf05a6"
import_review: "not-reassessed"
tags: ["learning", "imported", "markestream"]
---

> [!info] 마케스트림 docs에서 이관한 기록
> 이전 경로: `docs/adr/001-mysql.md` · 이관일: 2026-11-16 · 원본 정리일: 2026-11-16. 이관 후 사용자의 요청으로 원본 파일을 정리했다. 본문 안의 날짜·구현·검증·학습 상태는 작성 당시의 기록이며, 이관·삭제만으로 현재 상태를 다시 검증한 것은 아니다.
> [이관 목차](../imported-learning.md) · [현재 대화·자기 언어 학습 방법](../../../learning-workflow.md)

# ADR-001: 초기 데이터 저장소로 MySQL을 사용하는 현행 구성

- 작성 / 갱신: 2026-11-11
- 상태: 현행 구현 기록
- 대상 환경: 로컬 개발, 기존 MVP 설계
- 검증: 코드·설정 확인 / 런타임 실험 미실행

## 배경

마케스트림은 사용자, 대행사 소속, 광고주 등의 관계를 저장하고 업무 단위로 변경을 처리한다. 기존 [ERD](../reference/03-erd.md)와 [시스템 설계](../reference/02-system-architecture.md)는 MySQL을 전제로 작성됐다.

## 확인한 선택

[Compose](file:///Users/dhkim/Desktop/ml-project/markestream/infra/compose.yaml)에 MySQL 서비스가 있고 [Admin API 설정](file:///Users/dhkim/Desktop/ml-project/markestream/backend/admin-api/src/main/resources/application.yml)에 MySQL 연결과 Flyway가 지정돼 있다. 현재 WorkspaceService (`이전 경로: ../../backend/admin-api/src/main/java/com/markestream/admin/workspace/application/WorkspaceService.java`; 이관 시 파일 없음)는 트랜잭션을, 업무별 Repository는 JPA·Querydsl과 필요한 native SQL을 담당한다. 코드 기준 변경은 [ADR-003](003-backend-code-conventions.md)에 기록했다.

이 문서는 이미 코드에 반영된 선택을 기록한다. PostgreSQL 등과 비교해 최종 선택했던 당시의 발언이나 승인 이력은 확인하지 못했다.

## 요구와 맞는 이유 — 현재 코드로부터의 해석

대행사와 소속, 광고주처럼 관계가 있는 데이터를 다루며 대행사 생성과 소유자 등록을 같은 트랜잭션으로 처리한다. 현재 구조는 관계형 DB와 맞는다. 다만 이것만으로 MySQL이 다른 관계형 DB보다 우월하다는 판단을 내리지는 않는다.

| 재검토할 대안 | 검토할 관점 | 비교 상태 |
| --- | --- | --- |
| 현재 MySQL 유지 | 기존 SQL·JPA·마이그레이션 활용 | 코드 사용 확인 |
| 다른 관계형 DB | SQL 호환성, 운영 경험, 이전 비용 | 비교 실험 없음 |
| 운영용 RDS MySQL | 운영 책임, 백업·복원, 가용성 요구 | 기존 설계의 후보 |

## 결과와 감수할 점

MySQL용 SQL과 마이그레이션에 의존한다. 기존 목표 설계는 서비스가 DB 하나를 공유하므로 쓰기 권한과 스키마 변경 순서를 조율해야 한다. 로컬 Compose 설정이 운영 DB 설계를 확정한 것은 아니다.

## 검증과 재검토 조건

첫 확인은 [로컬 요청 실험](../labs/local-request-flow.md)으로 진행한다. 이후 동시 요청, 마이그레이션, 백업·복원을 각각 검증한다. 운영 환경의 가용성·복구 요구가 정해지면 DB 배치 방식을 다시 결정한다.
