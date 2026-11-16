---
title: "마케스트림 기존 기능 학습 순서"
type: project
project_id: "markestream"
learning_status: not-started
experiment_status: not-run
created: "2026-11-16"
tags: [learning]
---

# 마케스트림 기존 기능 학습 순서

[학습 목차](../../index.md)

<!-- learning:auto:start -->
<!-- learning:context {"kind": "project", "project_id": "markestream"} -->
확인일: 2026-11-16 · 이번 학습의 제품 실행 검증: 미실행

프로젝트: `markestream` · 코드 읽기 확인 · Git HEAD: `37a6dea3d9f39332de128912b62e45039a0ceb86`. 개별 해시는 커밋되지 않은 파일 내용도 포함한다.

## 한 문장으로

기존에 구현한 기능을 한 가지씩 골라 화면·서버·DB까지 따라가고, 그 과정에서 필요한 문법·기술·업무 규칙을 연결한다.

## 왜 필요한가

익숙한 화면의 기능에서 출발하면 코드가 필요한 이유를 붙잡기 쉽다. 첫 기능에서 익힌 요청 흐름·권한·저장 개념을 다음 기능에서 다시 사용하도록 멘토가 제안한 순서다. 사용자의 답변에 따라 난도·순서를 조정한다.

## 비즈니스 규칙

- 사용자는 기존 MarkeStream 기능과 내용을 학습하고 싶다고 요청했다. 이번 요청에는 제품 구현·변경 요청이 없다.
- 기술·업무 시작 질문에 대한 첫 사용자 답변을 받았다. 현재 학습 중이며 실제 코드 읽기 재질문과 이해도 통과는 아직 대기 중이다.
- 현재 코드와 구현 현황 문서로 학습 대상을 정했다. 이번 학습에서 제품 서버·빌드·테스트·DB 작업은 실행하지 않았다.
- 방문 분석·광고 플랫폼 연동·커스텀 도메인·결제 및 운영 인프라는 현행 MVP와 계획을 구분해 후속으로 읽는다.

## 실제 처리 흐름

| 순서 | 기능 | 따라갈 동작 | 필요한 개념 | 상태 |
| --- | --- | --- | --- | --- |
| 1 | 광고주 회사 추가 | 화면 입력 → API 요청 → 서버 처리 → DB 저장 | HTTP 요청, 함수·타입, Controller·Service·Repository | 학습 중 |
| 2 | 로그인과 권한 | 로그인한 사람과 작업 허용 범위를 구분 | 세션·토큰, 인증·인가, 회사 범위 | 예정 |
| 3 | 회사 등록과 초대 | 회사 정보·심사와 사람의 소속 연결을 구분 | 업무 상태 전이, 입력 검증, 초대 수락 | 예정 |
| 4 | 랜딩 편집과 저장 | 입력·초안·미리보기·저장 관계를 추적 | React 상태·훅, 문서 구조, 리비전 충돌 | 예정 |
| 5 | 게시와 공개 페이지 | 저장한 초안이 공개 HTML이 되는 길을 추적 | 작업 큐, 비동기 Worker, 스냅샷·버전 | 예정 |
| 6 | 문의 접수와 상담 | 공개 폼의 입력이 관리자 업무로 연결되는 길을 추적 | 검증, 멱등성, 서비스 간 호출, 상태·이력 | 예정 |

첫 주제는 [광고주 회사 생성](client-company-creation.md), 질문·답변은 [첫 학습 세션](../../sessions/markestream/client-company-creation.md)에 이어 기록한다.

## 기능마다 반복할 방식

1. 화면에서 무슨 일을 하는 기능인지 자신의 말로 설명한다.
2. 현재 이해를 짧게 묻고 필요한 설명을 한다.
3. 화면의 입력·이벤트 → API 요청 → 서버 메서드 → 저장·응답을 짧은 코드 조각으로 따라간다.
4. 그 코드에서 만난 문법·기술 원리·업무 규칙을 연결한다.
5. 다른 조건의 질문으로 이해를 확인하고 노트·Canvas에 연결한다.

## 실제 코드 진입점

아래는 후속 학습에서 읽을 위치다. 파일의 존재와 현재 기능 명세를 확인했으며, 각 기능의 모든 분기·실행 결과를 이번에 검증했다는 뜻은 아니다.

### 1. 광고주 회사 추가

- [apps/admin-web/src/features/clients/useClientManagement.ts](file:///Users/dhkim/Desktop/ml-project/markestream/apps/admin-web/src/features/clients/useClientManagement.ts)
- [backend/admin-api/src/main/java/com/markestream/admin/clientcompany/application/ClientCompanyService.java](file:///Users/dhkim/Desktop/ml-project/markestream/backend/admin-api/src/main/java/com/markestream/admin/clientcompany/application/ClientCompanyService.java)

### 2. 로그인과 권한

- [apps/admin-web/src/features/session/useSession.ts](file:///Users/dhkim/Desktop/ml-project/markestream/apps/admin-web/src/features/session/useSession.ts)
- [backend/admin-api/src/main/java/com/markestream/admin/permission/application/PermissionAccessService.java](file:///Users/dhkim/Desktop/ml-project/markestream/backend/admin-api/src/main/java/com/markestream/admin/permission/application/PermissionAccessService.java)

### 3. 회사 등록과 초대

- [backend/admin-api/src/main/java/com/markestream/admin/registration/api/RegistrationController.java](file:///Users/dhkim/Desktop/ml-project/markestream/backend/admin-api/src/main/java/com/markestream/admin/registration/api/RegistrationController.java)
- [backend/admin-api/src/main/java/com/markestream/admin/invitation/api/InvitationController.java](file:///Users/dhkim/Desktop/ml-project/markestream/backend/admin-api/src/main/java/com/markestream/admin/invitation/api/InvitationController.java)

### 4. 랜딩 편집과 저장

- [apps/admin-web/src/features/landing-editor/useLandingEditor.ts](file:///Users/dhkim/Desktop/ml-project/markestream/apps/admin-web/src/features/landing-editor/useLandingEditor.ts)
- [backend/admin-api/src/main/java/com/markestream/admin/landing/application/LandingService.java](file:///Users/dhkim/Desktop/ml-project/markestream/backend/admin-api/src/main/java/com/markestream/admin/landing/application/LandingService.java)

### 5. 게시와 공개 페이지

- [backend/admin-api/src/main/java/com/markestream/admin/landing/application/PublicationService.java](file:///Users/dhkim/Desktop/ml-project/markestream/backend/admin-api/src/main/java/com/markestream/admin/landing/application/PublicationService.java)
- [backend/publisher-worker/src/main/java/com/markestream/publisher/publication/application/PublisherRunner.java](file:///Users/dhkim/Desktop/ml-project/markestream/backend/publisher-worker/src/main/java/com/markestream/publisher/publication/application/PublisherRunner.java)

### 6. 문의 접수와 상담

- [backend/inquiry-api/src/main/java/com/markestream/inquiry/inquiry/api/PublicInquiryController.java](file:///Users/dhkim/Desktop/ml-project/markestream/backend/inquiry-api/src/main/java/com/markestream/inquiry/inquiry/api/PublicInquiryController.java)
- [apps/admin-web/src/features/inquiries/useInquiryManagement.ts](file:///Users/dhkim/Desktop/ml-project/markestream/apps/admin-web/src/features/inquiries/useInquiryManagement.ts)

## 설계 근거와 해석

학습 순서에 대한 멘토의 제안: 비교적 짧은 회사 추가 흐름에서 [계층별 책임](../../concepts/layered-request-flow.md), [트랜잭션 경계](../../concepts/transaction-boundaries.md), [인증과 인가](../../concepts/authentication-and-authorization.md)를 만난 뒤 편집·비동기 게시·공개 접수로 범위를 넓힌다.

이 순서는 개발자가 실제로 구현한 시간 순서나 과거 대화 내용의 복원이 아니다. 업무 기능 위치는 현재 소스·명세를 근거로 한다. 배포·인프라는 코드 구현과 설계 예정 사항을 분리해 다룬다.

[학습 Canvas](../../maps/learning-map.canvas) · [연결 목록과 상태](../../maps/learning-map.md)

이관 후 설계 자료: [docs/06-mvp-status.md](reference/06-mvp-status.md), [docs/02-system-architecture.md](reference/02-system-architecture.md). 기존 문서를 이관한 위치에서 참고하며, 당시 내용과 현재 구현의 일치 여부는 별도로 확인한다.

## 실제 코드와 설계 근거

외부 파일 링크는 원본 파일을 여는 용도다. 경로·심볼은 원본 저장소 기준이고, 행은 심볼의 첫 출현 위치를 찾는 힌트다.

- [apps/admin-web/src/features/clients/useClientManagement.ts](file:///Users/dhkim/Desktop/ml-project/markestream/apps/admin-web/src/features/clients/useClientManagement.ts) · `async function submit()` · 59행 부근
  - 근거: 이름 입력 검증, 회사 생성 POST 요청, 저장 성공·오류 처리의 첫 학습 위치
  - SHA-256: `2e2ce802b4dc73429b7625c44f6c86ec9c7da34b50dc23d9ce8bb3f00c57b53f`
<!-- learning:source {"path": "apps/admin-web/src/features/clients/useClientManagement.ts", "symbol": "async function submit()", "sha256": "2e2ce802b4dc73429b7625c44f6c86ec9c7da34b50dc23d9ce8bb3f00c57b53f", "project_id": "markestream", "project_root": "/Users/dhkim/Desktop/ml-project/markestream"} -->

- [backend/admin-api/src/main/java/com/markestream/admin/clientcompany/api/ClientCompanyController.java](file:///Users/dhkim/Desktop/ml-project/markestream/backend/admin-api/src/main/java/com/markestream/admin/clientcompany/api/ClientCompanyController.java) · `registerClientCompany` · 62행 부근
  - 근거: 첫 기능의 HTTP 요청·주체·입력 처리와 서비스 호출 위치
  - SHA-256: `bff107ba428db8005c479034074d7065f156f88d468a4b34915cef0c0c88de3d`
<!-- learning:source {"path": "backend/admin-api/src/main/java/com/markestream/admin/clientcompany/api/ClientCompanyController.java", "symbol": "registerClientCompany", "sha256": "bff107ba428db8005c479034074d7065f156f88d468a4b34915cef0c0c88de3d", "project_id": "markestream", "project_root": "/Users/dhkim/Desktop/ml-project/markestream"} -->

- [backend/admin-api/src/main/java/com/markestream/admin/clientcompany/application/ClientCompanyService.java](file:///Users/dhkim/Desktop/ml-project/markestream/backend/admin-api/src/main/java/com/markestream/admin/clientcompany/application/ClientCompanyService.java) · `registerClientCompany` · 126행 부근
  - 근거: 회사 생성 권한 확인·생성·저장·담당 배정을 조율하는 메서드
  - SHA-256: `c0e59ded655f84d3e492e837674e4a747f47c8de12d288cec993bee5fab0e92e`
<!-- learning:source {"path": "backend/admin-api/src/main/java/com/markestream/admin/clientcompany/application/ClientCompanyService.java", "symbol": "registerClientCompany", "sha256": "c0e59ded655f84d3e492e837674e4a747f47c8de12d288cec993bee5fab0e92e", "project_id": "markestream", "project_root": "/Users/dhkim/Desktop/ml-project/markestream"} -->

- [backend/admin-api/src/test/java/com/markestream/admin/clientcompany/domain/ClientCompanyTest.java](file:///Users/dhkim/Desktop/ml-project/markestream/backend/admin-api/src/test/java/com/markestream/admin/clientcompany/domain/ClientCompanyTest.java) · `rejectsOversizedNamesAndInvalidAgencyCompanyEvenWithoutHttpValidation` · 33행 부근
  - 근거: 이름 길이·대행사 ID 경계를 읽을 테스트. 이 학습에서는 실행하지 않음
  - SHA-256: `a515acefb1451b44cbf24ba37bd0d466fac6022b2bf8c5784a57c9df7f70053c`
<!-- learning:source {"path": "backend/admin-api/src/test/java/com/markestream/admin/clientcompany/domain/ClientCompanyTest.java", "symbol": "rejectsOversizedNamesAndInvalidAgencyCompanyEvenWithoutHttpValidation", "sha256": "a515acefb1451b44cbf24ba37bd0d466fac6022b2bf8c5784a57c9df7f70053c", "project_id": "markestream", "project_root": "/Users/dhkim/Desktop/ml-project/markestream"} -->

## 문서를 덮고 답하기

1. 광고주 회사 추가가 끝나면 어떤 정보가 생겨야 한다고 생각하는가? 로그인 계정이나 운영 승인까지 생기는지도 예상해 본다.
2. 저장 버튼을 누른 뒤 데이터가 DB에 남기까지 화면·서버·DB가 각각 무엇을 한다고 생각하는가? 낯선 단어부터 말해도 된다.
<!-- learning:auto:end -->

## 내 설명과 질문

아직 답변하지 않음. 이 영역은 자동 갱신 시 보존된다.
