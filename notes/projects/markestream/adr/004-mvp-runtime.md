---
title: "ADR-004: MVP의 실행 모듈과 로컬 게시·문의 경계"
type: "adr-snapshot"
source_project: "markestream"
imported_from: "docs/adr/004-mvp-runtime.md"
imported_at: "2026-11-16"
source_sha256: "fe2913ea6ccf314fb60e7bb1035713eecf18ba6dcbc8a6a190e1d898434a0466"
import_review: "not-reassessed"
tags: ["learning", "imported", "markestream"]
---

> [!info] 마케스트림 docs에서 이관한 기록
> 이전 경로: `docs/adr/004-mvp-runtime.md` · 이관일: 2026-11-16 · 원본 정리일: 2026-11-16. 이관 후 사용자의 요청으로 원본 파일을 정리했다. 본문 안의 날짜·구현·검증·학습 상태는 작성 당시의 기록이며, 이관·삭제만으로 현재 상태를 다시 검증한 것은 아니다.
> [이관 목차](../imported-learning.md) · [현재 대화·자기 언어 학습 방법](../../../learning-workflow.md)

# ADR-004: MVP의 실행 모듈과 로컬 게시·문의 경계

- 작성: 2026-11-11
- 상태: 현행 구현 기록. 사용자의 남은 MVP 개발 요청에 따라 적용
- 대상: 로컬 실행 및 자동 검증. 운영 배포 완료를 뜻하지 않음
- 관련: [PRD](../reference/01-prd.md), [아키텍처](../reference/02-system-architecture.md), [백엔드 규칙](file:///Users/dhkim/Desktop/ml-project/markestream/backend/AGENTS.md)

## 배경과 구현 선택

기존 로그인·대행사·광고주 기능에 MS-01~07의 팀원, 랜딩 편집·게시, 공개 접수, 문의 상담 흐름을 연결했다. 기존 설계의 Admin API → Inquiry API 호출과 별도 Publisher Worker 경계를 유지한다.

문서 규칙·HTML 렌더링·파일 저장소·공개 스크립트는 세 모듈이 실제 사용하는 `landing-core`에 둔다. 업무 엔티티와 Repository는 공유하지 않는다. Admin의 초안·게시 요청은 같은 `landing` 업무 안에 둔다. 서비스별 영속 모델은 자신이 쓰는 테이블과 필요한 읽기 모델만 정의한다.

로컬에서 실행을 완성하기 위해 HTML 저장소는 공유 디렉터리의 불변 파일로 구현했다. DB의 활성 버전을 바꾸기 전에 세대별 파일을 생성하며, 작업 임대와 세대가 맞는 완료만 허용한다. 24시간 지난 미참조 HTML은 정리한다. 운영 오브젝트 저장소 어댑터와 배포 볼륨 구성은 후속 배포 작업이다.

내부 토큰은 Admin이 별도 issuer의 60초 HS256 서비스 JWT로 발급한다. Inquiry가 issuer·만료·audience·azp·scope·서비스 grant를 검증하고 행위자 DB 권한을 다시 확인한다. 기존 로컬 Realm에 서비스 클라이언트가 없으므로 실행 가능한 내부 신원을 별도 키로 구성한 선택이다. Keycloak client credentials 토큰 엔드포인트 호출을 구현했다고 표현하지 않는다. 외부 OIDC 사용자 인증은 기존 Keycloak 검증을 유지한다. 배포 환경에서는 키 주입·서비스 계정 연계·TLS·네트워크 경계를 함께 구성해야 한다.

공개 요청 제한은 Redis를 추가하지 않고 MySQL 원자적 카운터를 사용한다. 주소 원문 대신 SHA-256 키와 분 단위 창만 보관하고 오래된 창은 정리한다. 프록시 뒤 방문자 주소를 정하는 운영 설정은 별도다.

## 계약과 화면

[OpenAPI](file:///Users/dhkim/Desktop/ml-project/markestream/contracts/openapi.yaml)는 0.2.0으로 갱신했다. 문의 요약에 `clientName`, `landingName`을 추가해 목록이 식별자 대신 업무 이름을 표시한다. 문의 응답 원문은 상세에만 포함한다. 기존 계정·대행사·광고주 API의 응답 형태와 정렬은 보존한다.

프론트는 라우트 → 업무 훅 → 데스크톱·모바일 독립 페이지를 유지한다. 조립 화면에 API 값과 동작을 주입하고 공통 UI에는 업무 의존성을 추가하지 않는다. 편집 중인 콘텐츠는 사용자·대행사·랜딩별 세션 초안으로 보존하며 문의 원문은 브라우저 저장소에 남기지 않는다.

## 검증 근거

- 독립 MySQL·테스트용 OIDC·실제 Inquiry HTTP·Worker를 연결한 통합 테스트
- 리비전·버전·멱등성 충돌, 테넌트 격리, 마지막 OWNER 동시 변경, 게시 실패·임대 교체 검증
- 공개 요청 제한과 미참조 파일 정리, HTML 이스케이프·입력 검증
- 개발용 Keycloak 로그인부터 브라우저 편집·게시·접수·상담 상태 변경까지 로컬 실행 확인

실제 고객 파일럿, 원격 배포, 운영 데이터 보관·삭제 절차는 이 검증에 포함되지 않는다.
