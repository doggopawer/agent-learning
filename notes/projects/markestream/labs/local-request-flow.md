---
title: "Lab: 로컬 광고주 등록 요청 따라가기"
type: "lab-record"
source_project: "markestream"
imported_from: "docs/labs/local-request-flow.md"
imported_at: "2026-11-16"
source_sha256: "66bf15954a1baed56734ecd6634785ca98e7e25c3e0c794cfbf72276be51d774"
import_review: "not-reassessed"
tags: ["learning", "imported", "markestream"]
---

> [!info] 마케스트림 docs에서 이관한 기록
> 이전 경로: `docs/labs/local-request-flow.md` · 이관일: 2026-11-16 · 원본 정리일: 2026-11-16. 이관 후 사용자의 요청으로 원본 파일을 정리했다. 본문 안의 날짜·구현·검증·학습 상태는 작성 당시의 기록이며, 이관·삭제만으로 현재 상태를 다시 검증한 것은 아니다.
> [이관 목차](../imported-learning.md) · [현재 대화·자기 언어 학습 방법](../../../learning-workflow.md)

# Lab: 로컬 광고주 등록 요청 따라가기

[위키 목차](../imported-guides/README.md) · [시스템 개요](../architecture/system-overview.md)

- 작성 / 갱신: 2026-11-11
- 상태: 미실행
- 실행일 / 실행 환경: 미기록
- 코드 기준: 절차 작성 시 로컬 작업 트리 확인. 실험 시 커밋과 변경 상태를 다시 기록한다.

## 확인할 질문

브라우저의 광고주 등록 요청이 Vite 프록시, JWT 검증, 대행사 권한 확인, DB 저장을 거쳐 응답하는가?

## 준비와 영향 범위

[프로젝트 README](file:///Users/dhkim/Desktop/ml-project/markestream/README.md)의 순서로 로컬 MySQL·Keycloak, Admin API, 관리자 웹을 실행한다. 이번 실험은 로컬 개발 데이터에 테스트 대행사와 광고주를 추가한다. 이름에 `학습실험-날짜` 접두사를 붙여 구분한다.

작업 디렉터리는 `markestream/`이다. 실험 환경을 기록한다.

```bash
git rev-parse HEAD
git status --short
docker compose -f infra/compose.yaml ps
```

## 절차 1: 인증이 없는 요청

```bash
curl --silent --show-error --include http://127.0.0.1:8081/admin/v1/workspaces
curl --silent --show-error --include http://127.0.0.1:5173/admin/v1/workspaces
```

예상: API 직접 요청과 Vite 프록시 요청 모두 `401`과 `INVALID_TOKEN`을 반환한다. `Connection refused`는 인증 결과가 아니라 서버 실행·주소·포트부터 확인할 신호다.

근거: [SecurityConfiguration](file:///Users/dhkim/Desktop/ml-project/markestream/backend/admin-api/src/main/java/com/markestream/admin/common/security/SecurityConfiguration.java), [Vite 설정](file:///Users/dhkim/Desktop/ml-project/markestream/apps/admin-web/vite.config.ts).

## 절차 2: 로그인과 등록

1. `http://127.0.0.1:5173/`에서 README의 개발 계정 `demo-owner`로 로그인한다.
2. 브라우저 개발자 도구의 Network에서 `/admin/v1` 요청을 관찰한다.
3. 테스트 대행사를 생성하고 그 대행사에 테스트 광고주를 등록한다.
4. `PUT /me`, `POST /workspaces`, `POST /workspaces/{workspaceId}/clients`의 경로·상태 코드·순서를 기록한다.
5. 페이지를 새로 고침하고 등록한 광고주가 다시 조회되는지 확인한다.

예상: 사용자 초기화 후 생성 요청은 `201`, 조회는 `200`이다. 브라우저에는 `:5173` 요청이 보이고 프록시의 실제 대상은 Vite 설정에서 확인한다. 토큰 값과 개인 데이터는 기록하지 않는다.

## 절차 3: 저장 확인

로컬 개발 DB에 읽기 전용으로 접속한다. 비밀번호는 프로젝트의 개발용 설정을 확인하고 프롬프트에서 입력한다.

```bash
docker compose -f infra/compose.yaml exec mysql mysql -u markestream -p markestream
```

```sql
SELECT id, workspace_id, name
FROM clients
WHERE name LIKE '학습실험-%'
ORDER BY id DESC
LIMIT 10;
```

예상: 방금 만든 광고주와 해당 대행사 ID가 조회된다. 결과에는 테스트 데이터만 남긴다.

## 절차 4: 계정에 따른 목록 차이

다른 브라우저 프로필 또는 시크릿 창에서 `demo-other`로 로그인한다. 첫 계정의 테스트 대행사가 목록에 없는지 확인한다. 이 단계는 화면의 목록 범위만 확인한다. ID를 바꾼 직접 API 호출까지 검사한 것으로 기록하지 않는다.

## 실제 결과

아직 실행하지 않았다. 아래 표는 실행 후 채운다.

| 관찰 | 예상 | 실제 결과 / 근거 |
| --- | --- | --- |
| 직접 / 프록시 비인증 요청 | 모두 401 | 미실행 |
| 광고주 생성 | 201 | 미실행 |
| 새로 고침 후 재조회 | 생성 데이터 표시 | 미실행 |
| DB 조회 | 해당 광고주·대행사 관계 확인 | 미실행 |
| 다른 계정의 목록 | 첫 계정의 대행사가 표시되지 않음 | 미실행 |

## 통과 기준과 남는 범위

표의 모든 관찰이 근거와 함께 확인되면 이 실험을 실제 검증 완료로 바꾼다. 직접 API의 교차 대행사 접근 거절, 동시 요청, 운영 환경, Kubernetes 장애 복구는 별도 실험이다.

## 정리

이 실험은 의도적으로 테스트 데이터를 남긴다. 현재 공개된 API에 삭제 기능은 없다. 브라우저의 실험 계정에서 로그아웃하고 데이터 정리가 필요하면 별도 절차를 정한다. 전체 개발 DB 볼륨을 지우는 방식으로 정리하지 않는다.

## 현재 학습과의 연결

이 문서는 기존 실험 기록·계획을 보존한 것이다. 실습은 선택 사항이며 이관 과정에서 실행하지 않았다. [회사 생성에 대한 현재 대화 노트](../client-company-creation.md) · [이관 목차](../imported-learning.md)
