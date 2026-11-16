---
title: "ADR-003: 객체지향·함수형 구성과 JPA·Querydsl 접근 기준"
type: "adr-snapshot"
source_project: "markestream"
imported_from: "docs/adr/003-backend-code-conventions.md"
imported_at: "2026-11-16"
source_sha256: "ecc22d1cc252132b120983eecc0dcee90fe892a345b300699975a33707e78d7e"
import_review: "not-reassessed"
tags: ["learning", "imported", "markestream"]
---

> [!info] 마케스트림 docs에서 이관한 기록
> 이전 경로: `docs/adr/003-backend-code-conventions.md` · 이관일: 2026-11-16 · 원본 정리일: 2026-11-16. 이관 후 사용자의 요청으로 원본 파일을 정리했다. 본문 안의 날짜·구현·검증·학습 상태는 작성 당시의 기록이며, 이관·삭제만으로 현재 상태를 다시 검증한 것은 아니다.
> [이관 목차](../imported-learning.md) · [현재 대화·자기 언어 학습 방법](../../../learning-workflow.md)

# ADR-003: 객체지향·함수형 구성과 JPA·Querydsl 접근 기준

- 작성 / 갱신: 2026-11-11
- 상태: 채택 및 Admin API 적용
- 대상 환경: 현재 백엔드 코드와 로컬 검증
- 관련 문서: [백엔드 작업 규칙](file:///Users/dhkim/Desktop/ml-project/markestream/backend/AGENTS.md), [개발 안내](file:///Users/dhkim/Desktop/ml-project/markestream/backend/README.md), [현재 시스템](../architecture/system-overview.md)

## 배경과 요구

기존 Admin API는 하나의 Controller와 Service에 계정·대행사·광고주 처리를 모으고, Service에서 EntityManager와 SQL을 직접 사용했다. 사용자는 사람이 읽기 쉬운 코드와 일관된 기술 스택·조회 방식이 유지되도록 규칙을 정하고, 현재 백엔드를 그 기준으로 정리하도록 요청했다.

## 검토한 대안

| 대안 | 특징 | 선택 |
| --- | --- | --- |
| 기존 단일 Service와 직접 SQL 유지 | 초기 코드가 적지만 권한·조회·업무 흐름이 한 클래스에 모임 | 업무별로 분리 |
| JPA와 Specification을 기본 조회로 사용 | 첫 규칙 초안의 동적 검색 기준 | 사용자와 협의해 Querydsl로 통일 |
| Spring Data JPA + Querydsl JPA | 기본 저장·조회와 복합 쿼리의 역할을 구분할 수 있음 | 채택 |
| 일반 조회까지 별도 SQL 프레임워크 병행 | 추가 쿼리 수단과 유지보수 기준이 생김 | 현재 도입하지 않음 |

## 결정과 적용

업무별 `api/application/domain/repository` 패키지와 객체지향·함수형 두 축을 사용한다. 객체가 업무 상태·불변 조건과 입출력 책임을 맡고, 계산·판정·변환은 외부 상태에 의존하지 않는 함수로 작성한다. Service는 명시적인 객체 협력과 트랜잭션 경계를 가진다.

단순 조회·저장은 Spring Data JPA로, 대행사 목록의 소속 조인과 공유 잠금 조회는 Querydsl로 구현했다. 동시 계정 초기화에 필요한 MySQL upsert는 사용자 정의 Repository의 native SQL로 유지한다. URL·응답·입력 검증·권한·DB 스키마는 구조 정리 과정에서 변경하지 않았다.

Querydsl 배포판은 `io.github.openfeign.querydsl`로 고정한다. **6.12를 선택한 이유는 해당 릴리스가 Spring Boot 3.5·Hibernate 6.6·Jakarta Persistence 3.1을 기준으로 하는 것이 공식 POM에서 확인되고, 현재 조합에서 실제 빌드·MySQL 테스트를 통과했기 때문이다.** 최신 릴리스를 일괄 선택한 결정은 아니다. Spring Data의 fork 연동 지원은 best-effort임을 감수한다.

입력에는 Bean Validation와 엄격한 문자열 역직렬화를 적용한다. 이름의 공백 제거와 Unicode code point 150개 제한을 유지한다. JWT는 웹 경계에서 불변 인증 주체로 바꾸고 application에는 `Clock`을 주입한다. 업무 오류에는 HTTP 타입을 넣지 않는다.

포맷터는 Spotless 8.11.0과 google-java-format 1.28.0 AOSP 설정으로 고정했다. 기존 4칸 들여쓰기 기준을 사용하고 Gradle `check`에 포맷 검사를 연결했다. 테스트는 Spring Boot BOM의 JUnit·Mockito·Testcontainers를 사용하며, 검증 당시 Testcontainers는 1.21.4였다.

## 검증과 감수할 점

정리 전 기존 코드에서 API 회귀 테스트 26개가 통과한 것을 확인했다. 정리 후 동일 테스트와 domain·서명·공유 잠금 테스트를 포함한 검증을 수행했다. MySQL 8.4.11 Testcontainers와 테스트 전용 OIDC discovery/JWKS 서버를 사용했으며, 실제 토큰 서명·issuer·audience·만료 검증을 거친다.

`./gradlew :backend:admin-api:clean :backend:admin-api:build`로 Q 클래스 재생성, 컴파일, 테스트, 포맷 검사, 실행 JAR 생성을 확인한다. 테스트 결과는 `backend/admin-api/build/reports/tests/test/index.html`에서 확인한다. 테스트용 DB는 개발 DB와 분리된다. 브라우저 수동 확인과 운영 배포 검증을 수행했다는 의미는 아니다.

패키지·DTO·Repository fragment가 추가되어 파일 수는 늘어난다. 단순 CRUD에는 빈 fragment를 만들지 않고, domain과 영속성 모델을 이중으로 만들지 않아 구조 비용을 제한한다. Querydsl/JPA의 한계를 넘는 DB 기능은 근거와 MySQL 검증을 갖춘 native SQL로 다룬다.

## 재검토 조건과 근거

Spring Boot/Hibernate 업그레이드, 복합 쿼리의 실제 성능 한계, Querydsl 유지보수 변화가 생기면 호환성과 실행 계획·테스트를 확인한 뒤 버전을 재검토한다. 외부 HTTP·Inquiry·Publisher는 아직 구현되지 않았으므로 이 기록에서 완성된 구성으로 취급하지 않는다.

선택 범위는 2026-11-11 이 채팅에서 사용자가 객체지향·함수형 구성, JPA·Querydsl 기준과 백엔드 정리를 요청한 내용에 근거한다. 아래 공식 자료는 같은 날짜에 확인했다.

- [Spring Data JPA 3.5 Querydsl 연동](https://docs.spring.io/spring-data/jpa/reference/3.5/repositories/core-extensions.html)
- [Spring Data Repository fragment](https://docs.spring.io/spring-data/jpa/reference/3.5/repositories/custom-implementations.html)
- [OpenFeign Querydsl 6.12 POM](https://github.com/OpenFeign/querydsl/blob/6.12/pom.xml)
- [Spotless Gradle 설정](https://github.com/diffplug/spotless/blob/main/plugin-gradle/README.md)
