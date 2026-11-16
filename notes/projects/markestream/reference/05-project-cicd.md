---
title: "MarkeStream 프로젝트 구조와 CI/CD 설계"
type: "project-reference"
source_project: "markestream"
imported_from: "docs/05-project-cicd.md"
imported_at: "2026-11-16"
source_sha256: "9a36ab12c9595d0590c5034bcf8dbf495404bb00ce396d577192bc3dccf65f7e"
import_review: "not-reassessed"
tags: ["learning", "imported", "markestream"]
---

> [!info] 마케스트림 docs에서 이관한 기록
> 이전 경로: `docs/05-project-cicd.md` · 이관일: 2026-11-16 · 원본 정리일: 2026-11-16. 이관 후 사용자의 요청으로 원본 파일을 정리했다. 본문 안의 날짜·구현·검증·학습 상태는 작성 당시의 기록이며, 이관·삭제만으로 현재 상태를 다시 검증한 것은 아니다.
> [이관 목차](../imported-learning.md) · [현재 대화·자기 언어 학습 방법](../../../learning-workflow.md)

# MarkeStream 프로젝트 구조와 CI/CD 설계

**초안 v0.1 · 2026-11-10**

프론트엔드와 Java 서비스, API 계약, DB 변경, 배포 설정을 GitHub 모노레포에 둔다. 하나의 변경에서 API와 데이터 계약을 함께 검토하고, 실행 단위는 각각 컨테이너로 빌드하고 배포한다.

## 모노레포 구조

```text
markestream/
├── apps/
│   └── admin-web/                 # React · TypeScript · Vite
├── backend/
│   ├── admin-api/                 # Spring Boot · JPA
│   ├── inquiry-api/               # Spring Boot · JPA
│   └── publisher-worker/          # Spring Boot · 게시 작업자
├── contracts/
│   └── openapi.yaml
├── database/
│   ├── migrations/                # Flyway SQL
│   └── Dockerfile                 # 릴리스별 Flyway 실행 이미지
├── infra/
│   ├── compose.yaml
│   └── k8s/
│       ├── base/
│       └── overlays/
│           ├── staging/
│           └── production/
├── docs/
├── .github/workflows/
│   ├── ci.yml
│   └── release.yml
├── gradlew
├── gradlew.bat
├── gradle/wrapper/
├── settings.gradle.kts
└── build.gradle.kts
```

Gradle은 `:backend:admin-api`, `:backend:inquiry-api`, `:backend:publisher-worker`를 하위 프로젝트로 포함한다. 루트는 플러그인과 Java 도구 체인 정책을 관리하며 각 모듈은 자체 엔티티와 서비스 구현을 소유한다. HTTP 계약은 `contracts/openapi.yaml`, SQL은 `database/migrations/`에서 관리한다. 이 설계 패키지의 [OpenAPI](file:///Users/dhkim/Desktop/ml-project/markestream/contracts/openapi.yaml)와 [V1 SQL](file:///Users/dhkim/Desktop/ml-project/markestream/database/migrations/V1__create_markestream_mvp.sql)을 각각 초기 파일로 옮긴다.

웹, Admin API, Inquiry API, Publisher는 각 모듈의 멀티스테이지 Dockerfile로 빌드한다. 환경 설정은 실행 시점에 주입한다. 프론트엔드는 같은 호스트의 상대 경로를 사용하고 OIDC 설정은 공개 런타임 설정으로 받는다. 환경별 자격 증명은 서버와 작업자에만 주입한다.

## 개발 환경과 스테이징

| 환경 | 구성 | 검증 |
| --- | --- | --- |
| 로컬 | Compose의 MySQL 8.4, 로컬 파일 저장소, 개발용 OIDC 환경 | 초안 저장부터 상태 변경까지 시드 계정으로 실행 |
| 스테이징 | EC2 3대 kubeadm 초안, Traefik, 테스트 MySQL StatefulSet 1개와 EBS PVC, 비공개 오브젝트 저장소, 별도 OIDC 클라이언트 | 애플리케이션 배포, EBS 재연결, 백업 복원, 공개 흐름 및 대행사 격리 |
| 운영 | 별도 배포 환경과 비밀, 관리형 MySQL 후보인 RDS, 실제 도메인과 TLS | 가용성 목표, 복구 목표, 보관 정책, 배포 승인자 확정 후 사용 |

스테이징의 노드 3대는 제어 노드 1대와 워커 2대로 시작하는 안이다. Admin·Inquiry는 각각 복제본 2개로 검증하고 Publisher는 1개부터 실행한다. 단일 제어 노드와 단일 DB 구성은 운영 가용성 목표와 별도로 검증한다. EBS CSI, 같은 가용 영역에서 볼륨을 다시 붙일 수 있는 워커 용량, Traefik 진입점, TLS 발급 방식을 구성 전에 확인한다.

Kubernetes에는 웹과 API 및 Publisher용 Deployment, 내부 ClusterIP Service, 공개·관리 호스트별 Ingress를 둔다. API readiness는 신규 요청을 처리할 수 있는지 확인하고 liveness는 프로세스 상태를 검사한다. 종료 시 API는 진행 중 요청을 마치고 Publisher는 새 작업을 받지 않는다. 복구된 작업은 임대가 만료된 뒤 재선점한다.

| 매니페스트 | 배치 기준 |
| --- | --- |
| `base/` | 웹과 API 및 작업자의 Deployment, 웹과 두 API의 ClusterIP Service, 관리·공개 Ingress, 서비스별 ServiceAccount와 NetworkPolicy |
| `overlays/staging/` | 스테이징 호스트와 복제본, 테스트 MySQL StatefulSet·Service·EBS StorageClass와 PVC 설정, 개발 계정용 환경 변수 참조 |
| `overlays/production/` | 운영 호스트와 복제본, 운영 DB 연결 설정과 별도 자격 증명 참조 |
| 릴리스별 마이그레이션 Job | 릴리스 digest의 Flyway 이미지, 환경별 DB 주소와 DDL 계정 참조, 실행 제한 시간 및 재시도 정책 |

환경별 오버레이에 릴리스의 이미지 digest를 넣어 배포 결과를 재현한다. Ingress는 관리 호스트와 공개 호스트에 각각 지정된 경로를 제공한다. `/internal/v1/**` 접근은 Admin API에서 Inquiry API로 제한한다. MySQL, 오브젝트 저장소, OIDC 자격 증명은 서비스별 Secret 또는 연동된 비밀 저장소에서 가져온다.

## CI와 배포

| 트리거 | 순서 | 통과 조건 |
| --- | --- | --- |
| PR | 웹 검사와 빌드, Gradle 검증, MySQL 8.4에서 Flyway 적용과 통합 테스트, OpenAPI 검증, 매니페스트 렌더링 | 기존 계약과 기능을 확인하고, 스키마와 API가 함께 바뀌면 한 PR에서 리뷰 |
| 기본 브랜치 병합 | 각 실행 단위와 마이그레이션 이미지 빌드, 커밋 SHA 기록, 레지스트리 푸시 | 이미지별 불변 digest가 릴리스에 기록됨 |
| 스테이징 배포 | 해당 환경의 동시 배포 제어, 마이그레이션 Job 완료, Deployment 갱신, smoke test | 앱 준비 상태와 공개 HTML, 문의 접수·관리자 조회 확인 |
| 운영 배포 | 스테이징 통과 릴리스 승인, 같은 digest를 운영에 배포, 검증 | 변경한 릴리스에 대해 헬스와 핵심 흐름 확인 |

CI에서는 PR 검증과 배포의 자격 증명을 분리한다. 서드파티 GitHub Actions는 전체 커밋 SHA에 고정한다. 스테이징과 운영은 GitHub Environment 및 환경별 권한으로 분리한다. kubeadm API에 사설 접근이 필요하면 신뢰된 배포 작업 전용 러너를 검토하고 PR 코드는 GitHub 호스팅 러너에서 검사한다. 레지스트리 후보는 ECR이며, 선택 시 AWS 접근에 GitHub OIDC와 대상 저장소 전용 역할을 사용한다. [GitHub Actions 보안 지침](https://docs.github.com/en/actions/reference/security/secure-use)

## 데이터 변경과 복구

1. 릴리스별 Flyway Kubernetes Job을 먼저 실행한다. Job 계정만 DDL을 수행한다. 서비스는 별도 MySQL 계정을 사용하고 JPA는 `ddl-auto: validate`로 맞춘다.
2. 적용할 변경은 이전 애플리케이션 버전과 공존해야 한다. 필드 추가, 데이터 이관, 기존 필드 제거를 서로 다른 릴리스로 나눈다. Job이 실패하면 애플리케이션 배포를 멈추고 적용된 변경과 Flyway 이력을 확인한다.
3. 마이그레이션이 끝나면 이전·신규 Pod가 공존하는 롤링 배포를 진행한다. Smoke test에 실패하면 이전 이미지 digest로 되돌린다. 이미 적용한 DB 변경의 복구는 별도 전진 수정 또는 백업 복원 절차로 다룬다.
4. 백업은 운영 DB와 분리된 저장소에 보관하고, 복원 테스트에서 문의 원문과 폼 버전의 관계, 활성 HTML 접근을 확인한다. 복구 시간과 허용 가능한 데이터 손실 목표는 파일럿 전에 확정한다.

마이그레이션 Job은 단일 작업으로 구성하고 재실행 가능한 Flyway 명령을 사용한다. Kubernetes Job은 동일 작업을 다시 시작할 수 있으므로 중복 실행 가능성을 반영한다. [Kubernetes Job](https://kubernetes.io/docs/concepts/workloads/controllers/job/)

## 구현 순서와 검증 항목

| 순서 | 구현 단위 | 확인할 결과 |
| --- | --- | --- |
| 1 | OIDC 등록, 대행사 소속, 광고주 | 동일 사용자의 대행사별 권한 차이와 교차 대행사 접근 거절 |
| 2 | 랜딩 편집, 스냅샷, 게시 작업자 | 리비전 충돌, 재시도, 이전 작업자의 임대 만료, 게시 실패 후 기존 공개 화면 유지 |
| 3 | 공개 접수, 목록·상세, 상태 변경 | 같은 요청의 동시 재전송, 이전 폼 거절, 게시 중단, 상태 변경 경쟁과 이력 보존 |
| 4 | 스테이징 배포와 복원 | 실제 MySQL 8.4 마이그레이션, 스모크 테스트, 이미지 복구와 DB 복원 |

애플리케이션 구현에서 JUnit과 Testcontainers로 DB 통합 테스트를 구성한다. 게시 전환과 문의 접수가 같은 랜딩 행을 잠그므로, 트래픽이 큰 랜딩의 접수 지연과 잠금 대기 시간을 부하 테스트로 확인한다. 확정할 항목은 Java·Spring Boot·Gradle 버전, 실제 IdP, 레지스트리, 오브젝트 저장소, EC2 사양과 가용 영역, 운영 DB와 복구 목표다.

[시스템 아키텍처](02-system-architecture.md) · [ERD](03-erd.md) · [API 명세](04-api-spec.md)
