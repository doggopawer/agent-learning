---
title: "AdDock API 명세"
type: "project-reference"
source_project: "markestream"
imported_from: "docs/04-api-spec.md"
imported_at: "2026-11-16"
source_sha256: "c378a5014c99ef2e8985d28ff080f99ea40490eee220aecc2e3c096d3a1f3a9f"
import_review: "not-reassessed"
tags: ["learning", "imported", "markestream"]
---

> [!info] 마케스트림 docs에서 이관한 기록
> 이전 경로: `docs/04-api-spec.md` · 이관일: 2026-11-16 · 원본 정리일: 2026-11-16. 이관 후 사용자의 요청으로 원본 파일을 정리했다. 본문 안의 날짜·구현·검증·학습 상태는 작성 당시의 기록이며, 이관·삭제만으로 현재 상태를 다시 검증한 것은 아니다.
> [이관 목차](../imported-learning.md) · [현재 대화·자기 언어 학습 방법](../../../learning-workflow.md)

# AdDock API 명세

**구현 계약 v0.4 · 2026-11-12**

관리자는 대행사 ID가 포함된 경로에서 작업하고, 방문자는 공개 랜딩 키로 문의를 보낸다. 관리자와 내부 요청은 서로 다른 토큰을 사용한다. 요청·응답 스키마는 [OpenAPI 3.1 파일](file:///Users/dhkim/Desktop/ml-project/markestream/contracts/openapi.yaml)에 정의했다. [OpenAPI 3.1.1 표준](https://spec.openapis.org/oas/v3.1.1.html)

## 인증과 접근 범위

/admin/v1은 계정 타입과 OIDC 클라이언트를 검증한 토큰을 사용한다. 회사·소속·담당·권한그룹의 현재 DB 상태로 매 요청을 판정한다. 시스템 계정은 모든 대행사 범위이며 실제 작업은 부여 권한으로 제한한다. /internal/v1은 별도 서비스 JWT의 actor_type·actor_id·agency_company_id를 검증하고 Inquiry가 현재 권한을 다시 확인한다. X-Actor-User-Id 헤더는 인증 근거로 사용하지 않는다.

ID는 십진 문자열이다. 기존 초안·문의 revision/version은 문자열이며 새 그룹·권한 정책의 version은 JSON 정수다. 그룹·정책 저장은 읽은 version을 보내고 충돌 시 409를 받는다. 구체적인 정책은 [권한 명세](07-permissions.md)를 따른다.

## 업무 API

다음 경로는 /admin/v1 기준이다. `{a}`는 /agency-companies/{agencyCompanyId}, `{l}`은 `{a}`/landings/{landingId}다. 기존 /workspaces/.../clients 경로는 호환 별칭이며 고정 role 요청은 더 이상 받지 않는다.

| 메서드·경로 | 필요 권한·동작 |
| --- | --- |
| PUT /me | 종류별 계정 초기화. userId/accountType/시스템 권한 목록. 시스템은 사전 등록 필수 |
| GET /agency-companies | 소속 대행사 목록. 시스템은 system.agency.read로 전체 조회 |
| POST /agency-companies | 대행사 계정만 가능. 기본 그룹 3개와 첫 팀장 소속을 원자적으로 생성 |
| GET {a}/memberships | member.read |
| PUT/DELETE {a}/memberships/{userId} | member.manage. PUT은 기존 활성 구성원의 permissionGroupId 변경만 허용. 신규·회수 소속은 초대 수락 필요. 마지막 관리자 보호 |
| GET/POST {a}/client-companies | client.read / client.create. 목록은 접근 회사 범위로 제한 |
| GET {a}/client-companies/work?section=... | 현재 업무의 회사 선택 목록. inquiries/landings/people/registration에 해당하는 권한과 회사 범위로 조회. client.read 불필요. 미배정 빈 배열, 다른 대행사 404, 업무 권한 없음 403 |
| PATCH {a}/client-companies/{clientCompanyId} | client.update |
| GET/POST {a}/client-companies/{clientCompanyId}/landings | landing.read / landing.create |
| GET/PUT {l}/draft | landing.read / landing.update. 기존 expectedRevision 유지 |
| POST {l}/publish-jobs | landing.publish, Idempotency-Key 및 draftRevision |
| GET {l}/publish-jobs/{jobId} | landing.read |
| DELETE {l}/publication | landing.unpublish |
| GET {a}/inquiries 및 /{inquiryId} | inquiry.read. Inquiry에서도 회사 범위 검사 |
| PATCH {a}/inquiries/{inquiryId}/status | inquiry.update. expectedVersion 유지 |
| GET {a}/access?clientCompanyId=... | 현재 회사에 적용되는 기능 권한 |

기존 랜딩·문의 응답의 clientId 및 문의 clientId 검색 인자는 호환을 위해 유지하며 광고주 회사 ID를 뜻한다. 모든 실제 DB 참조는 client_company_id다. 문의 목록은 clientId·landingId·status·assignment·assigneeId·keyword·fromDate·toDate·cursor·limit를 지원하며 최신순 커서를 유지한다.

## 권한·소속 관리 API

| 메서드·경로 | 권한·본문 |
| --- | --- |
| GET {a}/permission-groups | 그룹 조회 또는 그룹·계정 소속 관리 권한 |
| POST {a}/permission-groups | group.manage와 부여 가능 범위 검사 |
| PUT/DELETE {a}/permission-groups/{id} | group.manage, 현재 version 필요. 기본·참조 그룹 삭제 금지 |
| GET {a}/permission-catalog | group.read 또는 group.manage. 허용 대상 포함 |
| GET {a}/client-memberships | client_user.read |
| PUT {a}/client-companies/{client}/memberships/{user} | client_user.manage. 기존 소속 회수 또는 활성 소속의 그룹 변경. 신규·회수 계정의 active=true는 404 |
| GET {a}/client-assignments | assignment.manage |
| PUT {a}/client-companies/{client}/assignments/{user} | assignment.manage. active |
| GET/POST /system/permission-groups | 시스템 그룹 조회/생성. 생성은 system.group.manage |
| PUT/DELETE /system/permission-groups/{id} | system.group.manage, version |
| GET /system/permission-catalog | system.policy.manage 또는 system.group.manage |
| PUT /system/permission-catalog/{code}/targets | system.policy.manage. targets 목록, version. 관련 그룹 권한 회수와 마지막 관리자 검사 |
| GET /system/accounts/{type} | system.account.read. 계정 ID·종류·식별자·활성 상태·그룹 |
| POST /system/admin-users | system.account.manage. 같은 발급자의 issuer/subject/permissionGroupId |
| PUT /system/accounts/{type}/{id} | system.account.manage. active, 시스템 계정에 한해 permissionGroupId |
| PUT /system/agency-companies/{id}/active | system.agency.manage. active |

그룹 저장 본문은 targetType(AGENCY_USER/CLIENT_USER/ADMIN_USER), name, clientScope(ALL/LINKED), permissions(코드 배열), 수정 시 version이다. 대행사 그룹에 시스템 타입을 넣거나 다른 대행사 그룹을 배정하면 거절한다. 대상 축소는 기존 그룹의 해당 권한을 같은 트랜잭션에서 회수한다. 등록되지 않은 권한 코드를 UI에서 만들 수 없다.

초안에는 `content.schemaVersion`, `content.blocks`, `form.fields`, `form.consentText`가 들어간다. 문의폼 블록은 정확히 하나다. 필드 ID는 폼 안에서 유일하며, 라벨을 편집해도 동일 필드의 ID는 유지한다. 새 랜딩은 리비전 1과 기본 편집용 초안을 반환할 수 있도록 초기화한다. 기본 폼의 동의 문구는 비어 있으며 초안 저장은 허용한다. 게시 시 빈 문구와 이전 기본 작성 안내 문구는 `/form/consentText`의 `CONSENT_TEXT_REQUIRED`로 422 거절한다. 렌더러도 같은 검증을 적용한다.

게시 작업은 요청 본문의 `draftRevision`과 헤더의 `Idempotency-Key`를 받는다. 같은 키와 리비전으로 재요청하면 `202`로 기존 작업의 현재 상태를 반환한다. 실패한 작업을 새로 실행할 때는 새 키를 사용한다.

문의 목록·상세 요약은 `clientName`, `landingName`, `customer:{name,phone,email}`을 포함한다. 고객 요약은 접수 당시 폼의 PHONE/EMAIL 타입과 이름 필드에서만 추출하며 미입력은 null이다. 임의 TEXT 응답을 연락처로 추정하지 않는다. 전체 `answers`·폼 스키마·동의 원문·상담 메모는 목록에 포함하지 않는다. 기존 문의 조회 권한과 회사 범위를 동일하게 적용하며 중복 문의의 요약에는 `customer`를 넣지 않는다.

문의 목록의 정렬은 `submittedAt DESC, id DESC`다. `clientId`, `landingId`, `status`를 함께 적용할 수 있다. `limit` 기본값은 25이며 최대 100이다. 다음 페이지는 같은 대행사와 필터에 묶인 `nextCursor`를 넘겨 요청한다. 대행사나 필터가 다른 커서 또는 변조된 커서는 `400 INVALID_CURSOR`를 반환한다.

문의 상태 전이는 `NEW → IN_PROGRESS → CLOSED`와 `CLOSED → IN_PROGRESS`다. 예를 들어 신규 문의의 버전이 1이면 상태 변경 요청에 아래 본문을 보낸다. 서버는 현재 상태와 버전을 확인하고 변경 이력을 함께 남긴 뒤 버전 2인 문의 상세를 응답한다. 문의 원문은 상세 조회 및 상태 변경 응답에만 포함하며 캐시하지 않는다.

```json
{"status":"IN_PROGRESS","expectedVersion":"1"}
```

## 공개 랜딩과 문의 접수

`GET /p/{publicPageKey}/`는 활성 버전 HTML을 `200 text/html`로 제공한다. 활성 버전이 없으면 `404`다. HTML과 문의 API는 같은 공개 호스트에 배치한다.

```http
POST /api/public/v1/landings/31b0ec20-d25f-4f76-8da0-6b251403c9b3/inquiries HTTP/1.1
Host: pages.example.com
Content-Type: application/json
Idempotency-Key: 5dfb0e8a-3bf1-4a14-8c5e-9e6d6cbce220

{
  "releaseKey": "750b1b53-3c72-4011-9a06-ce0c87ddd4ce",
  "answers": {"email": "visitor@example.com"},
  "consentAccepted": true
}
```

```json
{"receiptCode":"7016846d-a21c-4d80-9dc8-cf85b086a2f2"}
```

최초 접수와 동일 요청 재전송 모두 `201`과 같은 접수 번호를 돌려준다. 동일성은 공개 랜딩, 요청 키, 릴리스 키와 필드 응답 및 동의값을 기준으로 판단한다. 네트워크 재시도에는 원래 요청 키와 본문을 사용한다. 내용을 수정해 새로 제출하면 새 키를 사용한다. 서버는 폼 필드 ID, 필수 필드, 형식, 길이, 동의값을 검증한다. 접수 성공 응답은 캐시하지 않는다.

## 내부 Inquiry API

관리자용 문의 목록, 상세, 상태 변경을 `/internal/v1/workspaces/{workspaceId}/inquiries` 아래 동일한 계약으로 제공한다. Inquiry API는 서비스와 행위자를 확인한 후 대행사 조건으로 쿼리한다. 사용자에게는 Admin API를 통해 같은 업무 오류가 전달된다.

로컬 내부 토큰과 운영 IdP 연계의 차이는 [ADR-004](../adr/004-mvp-runtime.md)에 기록한다. 공개 폼 스크립트는 `GET /assets/public-form.js`로 제공하며 HTML과 같은 원점을 사용한다. 공개 본문은 256KiB, 관리자 JSON은 1MiB까지 허용한다.

## 오류 응답

JSON 오류는 `application/problem+json`을 사용한다. `status`, `code`, `requestId`를 기준으로 화면 동작과 운영 로그를 연결한다. 필드 오류의 위치는 `/answers/email` 같은 JSON Pointer를 쓴다.

| HTTP | 업무 코드 예시 | 화면 동작 |
| --- | --- | --- |
| `400` | `INVALID_REQUEST`, `INVALID_CURSOR` | 형식을 고치거나 목록 첫 페이지로 이동 |
| `401` | `INVALID_TOKEN` | 토큰 갱신 또는 로그인 |
| `403` | `FORBIDDEN`, `ACCOUNT_NOT_INITIALIZED` | 권한 안내 또는 사용자 등록 완료 |
| `404` | `NOT_FOUND` | 찾을 수 없음 표시 |
| `409` | `STALE_RELEASE`, `REVISION_CONFLICT`, `VERSION_CONFLICT` | 현재 페이지나 데이터를 새로고침 |
| `409` | `PUBLISH_IN_PROGRESS`, `IDEMPOTENCY_KEY_REUSED`, `INVALID_TRANSITION`, `LAST_OWNER` | 충돌 원인을 표시하고 가능한 동작 안내 |
| `413`, `422` | `PAYLOAD_TOO_LARGE`, `VALIDATION_FAILED` | 입력 크기를 줄이거나 해당 필드 수정 |
| `429` | `RATE_LIMITED` | `Retry-After` 초가 지난 뒤 재시도 |
| `503` | `SERVICE_UNAVAILABLE` | 같은 요청 키가 필요한 작업은 원래 키를 유지해 재시도 |

[PRD](01-prd.md) · [시스템 아키텍처](02-system-architecture.md) · [ERD](03-erd.md)

## 회사 등록·검증·초대 v0.4

[등록 명세](08-registration.md)와 OpenAPI의 Registration/Invitation schema를 따른다. 아래도 /admin/v1 기준이며 `{a}`는 위 대행사 경로, `{c}`는 `{a}/client-companies/{clientCompanyId}`다. 신청 version은 JSON 정수다.

| 메서드·경로 | 동작 |
| --- | --- |
| GET/PUT {a}/registration | 대행사 회사·신청 이력 조회 / 초안 저장 |
| GET/PUT {c}/registration | 광고주 회사·신청 이력 조회 / 초안 저장 |
| GET /company-reviews/{id} | 현재 권한으로 신청 조회. 내부 확인 근거는 심사 권한 관리자만 반환 |
| POST /company-reviews/{id}/submit, /business-check, /withdraw | 제출·재조회·철회, 읽은 version 필수 |
| POST /company-reviews/{id}/documents | multipart file·version·documentType, 10MB 이하 PDF/PNG/JPEG |
| GET/DELETE /company-documents/{id} | 인증된 비공개 다운로드 / 수정 가능한 신청의 첨부 제거 |
| GET /system/company-reviews | system.company.review, status·before 커서, 최대 50개 |
| POST /system/company-reviews/{id}/decision | version·decision·note, 승인에는 verificationMethod·verificationNote 필수 |
| GET/POST {a}/invitations | 직원 초대 목록 / email·permissionGroupId로 초대 |
| GET/POST {c}/invitations | 광고주 회사 이용자 초대 목록 / 초대 |
| DELETE /invitations/{id} | 초대 취소 |
| GET /me/invitations | 현재 인증 이메일·종류로 받은 대기 초대. acceptToken은 이 응답만 포함 |
| GET /invitations/{token}/preview | 인증 이메일·종류가 일치하는 수신자의 초대 상세 |
| POST /invitations/{token}/accept | 검증 후 기존 memberships에 원자적 연결 |
| GET {c}/people | 회사 이름·승인·권한, 광고주 이용자·담당 직원·대행사 후보·선택 가능 그룹 |
| GET {a}/assignment-candidates | 현재 대행사 직원의 이름·이메일 선택 목록 |

기존 memberships API와 호환 경로는 활성 구성원의 그룹 변경·소속 회수에만 사용한다. 신규·회수 계정은 사용자 ID를 알아도 직접 연결할 수 없으며 이메일 초대 수락이 필요하다. assignments는 이름·이메일로 선택한 기존 직원의 담당 회사를 배정한다. 회사·회원 목록에 이름·이메일·승인/활성 상태가 추가된다. 409는 승인 미완료·진행 중 신청·오래된 버전·사용 불가 초대·재초대 대기 등 업무 충돌, 403은 현재 권한/메일 인증/수신자 불일치다. 파일 제한은 413이며 위장 파일은 400이다. 실제 오류 코드는 Problem의 code를 따른다.

대행사 이용 재개는 유효한 활성 관리자가 없으면 409다. 중지된 회사의 기존 직원 소속을 복구하며 재개하려면 `PUT /system/agency-companies/{id}/active`에 `active=true`, `managerUserId`, `managerPermissionGroupId`를 함께 보낸다. `system.agency.manage`와 `member.manage`, 대상 그룹의 위임 권한을 확인하고, 과거 소속·활성 계정·회사 일치 및 최종 관리자 조건을 한 트랜잭션에서 검사한다. 다른 회사 계정 연결이나 관리자 없는 재개는 롤백한다.

## 문의 상담 협업

- GET `{a}/inquiries`: `assignment=ALL|MINE|UNASSIGNED`. MINE은 CLIENT_USER만 가능하며 미배정은 재배정 필요도 포함한다. 서명 커서는 필터와 MINE 계정에 바인딩된다. 요약의 `assignee`는 직원 ID·이름·이메일·현재 배정 유효 여부이며 미배정은 null이다.
- GET `/{inquiryId}/assignee-candidates`: 문의 조회+`inquiry.assign` 필요. 같은 광고주 회사의 활성 직원 중 문의 조회·처리 권한이 모두 있는 사람만 반환한다.
- PUT `/{inquiryId}/assignee`: `{clientUserId: 문자열 또는 null, expectedVersion: 문자열}`. 명시적 null로 해제한다. 오래된 버전 또는 부적격 직원은 409다.
- GET `/{inquiryId}/notes`: 문의 조회+`inquiry.note.read` 필요. `before` ID와 `limit`(기본 25, 최대 50)로 최신 작성순 페이지를 반환한다. `{items,nextBefore}`.
- POST `/{inquiryId}/notes`: 문의 조회+`inquiry.note.create` 필요. `{body}`와 UUID `Idempotency-Key`를 받아 201을 반환한다. 앞뒤 공백 제거 후 Unicode 기준 1~2,000자다. 같은 요청자·내용·키는 같은 결과이며 키 재사용 충돌은 409다. 작성자 이름·시각은 서버에서 정한다. 상태 이력도 작성자 이름을 반환한다.

모든 경로에서 현재 회사 범위·권한을 Inquiry API가 재검사하며 배정·메모 저장은 정책 공유 잠금을 사용한다. 기존 `/workspaces` 별칭과 내부 전달 경로도 같은 계약을 제공한다.

## 문의 검색·상세 필터

기존 문의 목록 GET에 `keyword`, `fromDate`, `toDate`, `assigneeId`를 추가했다. 신규 독립 작업 권한을 만들지 않고 기존 `inquiry.read`와 조회 가능한 광고주 회사 범위를 동일하게 적용한다.

- `keyword`: 공백 제거·소문자 변환 후 최대 Unicode 100자. 접수번호와 접수 당시 응답 값의 부분 검색이며 JSON 항목 ID·폼 라벨은 검색하지 않는다. 필드 이름이 변경된 기존 문의도 같은 방식으로 검색된다. `%`, `_`, `!`는 와일드카드가 아닌 문자 그대로 처리한다. 숫자·전화번호 형식으로 입력하면 응답 값의 하이픈·공백·괄호·점·+를 무시한 검색도 함께 수행한다. 상담 메모는 검색 대상에 포함하지 않는다.
- `fromDate`/`toDate`: `YYYY-MM-DD`, 1900년 이후. 한국시간 시작일 00:00 이상·종료일 다음 날 00:00 미만을 UTC Instant로 변환한다. 한쪽만 지정할 수 있으며 역전·잘못된 날짜는 400이다.
- `assignment=SPECIFIC`에는 `assigneeId`가 필수다. 다른 배정 모드에서 직원 ID를 보내면 400이다. 특정 담당자 검색에는 소속·권한이 회수되어 재배정이 필요한 기존 문의도 포함한다.
- GET `/inquiries/assignees`: 문의 조회 권한만으로 현재 조회 가능한 문의에 지정된 광고주 직원의 ID·이름·이메일을 중복 없이 반환한다. 선택적 `clientId`로 범위를 좁힌다. 다른 회사 직원 목록을 배정 후보 API에서 가져오지 않는다.

조건은 SQL에서 권한·회사 범위와 함께 적용하며 검색 원문을 응답 목록에 추가하지 않는다. 커서는 검색어의 SHA-256 해시·날짜·배정 모드·직원에 바인딩하며 원문 이름·연락처를 커서에 넣지 않는다. 새 조건이 없는 기존 커서와 `/workspaces` 별칭은 유지한다. DB 스키마와 원문 데이터는 변경하지 않는다.

화면은 공통 TextField·Select·DateField를 조립한다. 입력 중에는 조회하지 않고 검색 버튼/Enter로 조건을 적용하며 첫 페이지로 이동한다. 기기 전환·조회 실패 시 입력한 조건을 유지하고 조건 초기화로 고정 광고주 범위만 남긴다.

JSON 값 검색의 패턴·escape 계약은 [MySQL JSON 검색 함수](https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html)를 기준으로 하며 실제 MySQL 8.4.11 통합 테스트로 확인한다. 확인일 2026-11-12.

## 상담 결과

PUT `{a}/inquiries/{inquiryId}/outcome`은 `{outcome,note,expectedVersion}`를 받는다. `outcome`은 UNRECORDED(미기록), CONTRACTED(계약 성사), NOT_INTERESTED(관심 없음), UNREACHABLE(연락 불가), OTHER(기타)다. `note`는 반드시 명시한 문자열 또는 null이며 공백 제거 후 Unicode 1,000자 이하이다. 미기록에는 null 또는 공백만 허용한다. 버전은 십진 문자열이다.

`inquiry.read`와 `inquiry.outcome.update`를 같은 광고주 회사 범위에서 재검사한다. 정책 공유 잠금과 문의 행 잠금으로 현재 권한·버전을 확인하고 결과·메모·변경 이력을 원자적으로 저장한다. 같은 버전의 같은 내용은 변경하지 않고, 오래된 버전은 409다. 상태·담당자 변경과 버전을 공유하며 메모 작성은 기존대로 문의 버전에 영향을 주지 않는다.

목록 요약은 결과 코드만 반환하고 결과 메모를 넣지 않는다. 상세에 `outcomeNote`와 `outcomeHistory`(버전·변경자 종류/ID/이름·전후 결과/메모·시각)를 추가한다. 기존 진행 상태는 결과와 독립적이며 상담 완료·재개로 결과를 바꾸거나 지우지 않는다. 결과·메모 초기화도 이력을 보존한다. 기존/신규 문의의 결과는 미기록이다.

목록 GET의 선택적 `outcome` 필터는 기존 검색·회사·기간·담당자·상태 조건과 AND로 적용된다. UNRECORDED는 미기록만 조회한다. 결과 조건은 서명 커서에 바인딩하며 결과 필터가 없는 기존 커서는 유지한다. `/workspaces` 호환 경로와 Inquiry 내부 전달 경로도 같은 계약이다. 기존 문의 응답 검색은 결과 메모를 검색하지 않는다.

## 문의 재연락 일정

`PUT /agency-companies/{agencyCompanyId}/inquiries/{inquiryId}/follow-up` (Admin `/admin/v1`, legacy workspaces 별칭 및 Inquiry 내부 `/internal/v1/workspaces` 동일). 요청은 `{status,date,task,expectedVersion}`이며 nullable인 date/task도 필드 존재가 필수다. ID·버전과 날짜·할 일은 엄격한 문자열이다. 날짜는 1900~9999년의 YYYY-MM-DD, 할 일은 앞뒤 공백 제거 후 Unicode code point 1~1,000자다. 과거 날짜 예약도 가능하다.

PENDING은 예약·변경·완료 후 다시 예약, COMPLETED는 저장된 예약의 날짜·할 일을 그대로 완료, NONE은 날짜·할 일을 NULL로 취소한다. 미예약에서 완료는 409, 완료 시 날짜/할 일 변조는 400이다. 현재 버전의 동일 값은 무변경이고 오래된 버전은 409다. 상태·담당자·상담 결과와 버전을 공유하고 메모 작성과는 독립적이다. 정책 공유 잠금·문의 행 잠금 안에서 현재 read/manage 권한과 회사 범위를 검사하며 이력·버전을 원자적으로 저장한다. 완료 시각은 서버 Clock에서 구한다.

목록은 `followUp=ALL|TODAY|OVERDUE|UPCOMING|COMPLETED|UNSCHEDULED`를 기존 조건과 AND로 적용한다. 오늘/기한 지남/예정은 PENDING만 한국시간 날짜로 비교한다. 서명 커서에 일정 필터·상대 기준일을 넣어 자정 이후 다음 페이지도 같은 날짜를 사용한다. 새 첫 페이지는 현재 한국시간 날짜를 사용한다. `followUpReferenceDate`로 기준일을 반환하며 Admin의 접근 회사 없는 빈 응답만 NULL이다. 요약에는 상태·날짜·완료 시각만, 상세에는 할 일과 전후 이력을 추가한다. 자동 알림·문자/메일 발송은 이번 범위에 없다.

## 문의 알림

Admin의 `/agency-companies/{agencyCompanyId}/inquiry-notifications`(workspaces 호환 별칭)와 Inquiry 내부 `/internal/v1/workspaces/{agencyCompanyId}/inquiry-notifications`에 GET 목록과 PUT `/{notificationId}/read`를 추가했다. GET 조건은 선택 clientId·before와 `read=ALL|UNREAD`, limit 기본 25·최대 50이며 반환은 `{items,nextBefore,unreadCount}`다. 순서는 이벤트 ID 내림차순이고 before는 엄격한 양의 10진 문자열이다. 현재 권한과 동일한 SQL 조건을 매번 사용하므로 커서를 바꿔도 다른 회사/계정의 알림에 접근하지 못한다. unreadCount는 같은 회사 범위의 전체 미확인 개수다. 모든 응답은 no-store다.

단건 읽음은 본문 없이 204이며 최초 읽음 시각을 보존하는 멱등 쓰기다. 정책 공유 잠금 안에서 현재 read/notification 권한과 이벤트 노출 조건을 검사한다. 다른 회사·지난 담당자의 배정·완료/취소/변경된 재연락 이벤트는 404다. 계정 종류+계정 ID가 다른 읽음 상태는 독립적이다. 접수번호·회사·랜딩·날짜와 이벤트 종류만 반환하고 문의 응답·연락처·메모·할 일 원문은 추가하지 않는다.

공개 접수와 새 담당자 배정은 원본·알림을 한 트랜잭션으로 저장하고 실패 시 함께 롤백한다. 공개 접수 재시도는 같은 키로 같은 접수/알림 한 건을 사용한다. 예정 알림은 서버 Clock의 한국시간 오전 9시부터 현재 날짜 이하의 PENDING 중 배정된 일정에 생성하며, 중단 기간의 기한 지난 일정도 복구한다. 최대 100건씩 조회하고 정책·문의 행 잠금 아래 일정 최신 버전·현재 담당자·UNIQUE 키로 중복을 방지한다. 일정 완료/취소/재예약 또는 담당자 변경 시 오래된 예정 알림은 현재 상태와 일치하지 않아 숨긴다. 앱은 보이는 탭에서 30초마다/창 복귀 시 갱신하며 알림 클릭은 해당 회사·문의 상세를 새로 읽는다. 외부 이메일·문자·브라우저 푸시는 연결하지 않았다.

## 같은 연락처의 이전 문의

`GET /agency-companies/{agencyCompanyId}/inquiries/{inquiryId}/duplicates`를 Admin `/admin/v1`, workspaces 호환 별칭과 Inquiry 내부 `/internal/v1/workspaces`에 제공한다. 같은 광고주 회사에서 전화번호 또는 이메일이 일치하고 현재 문의보다 (접수 시각, ID)가 앞선 접수만 대상으로 한다. 폼 필드명·레이블 대신 접수 당시 폼의 PHONE/EMAIL 타입을 사용하므로 버전·필드 ID가 바뀌어도 비교하며 TEXT/메모 값은 추정하지 않는다. 전체 개수는 연락처 일치 항목 개수가 아닌 문의 건수다.

`{indexing,contactTypes,total,items,nextBefore}`를 반환한다. items는 `{inquiry:InquirySummary,matchedBy:[PHONE,EMAIL]}`이며 비교 항목 종류는 중복 없이 PHONE/EMAIL 순서다. 원본 고객 연락처·응답·상담 메모·내부 해시는 추가하지 않는다. 실제 원문은 기존 권한을 검사하는 문의 상세를 연다. 전화번호는 구분 문자·+82/0082의 한국 국가번호를 정리하고 이메일은 앞뒤 공백·대소문자만 정리한다. 이메일 점/플러스 별칭과 서로 다른 연락처를 합치지 않는다. 현재 문의 이후의 접수는 이전 문의에 포함하지 않는다.

화면에서는 건수를 먼저 보여주고 목록은 사용자가 펼친다. 기본 10건·최대 25건, submittedAt DESC/id DESC다. before는 직전 nextBefore의 엄격한 양의 10진 문의 ID이며 같은 회사의 이전 일치 문의인지 검사한 후 해당 접수 시각·ID를 페이지 경계로 사용한다. 접수 시각이 같은 경우에도 빠짐·중복을 방지한다. 같은 회사의 조회/중복 확인 권한을 재검사하며 회수된 소속이나 대상 정책에 접근을 허용하지 않는다. 모든 응답은 no-store다.

미준비 문의나 이전 접수가 남아 있으면 indexing=true·total=null·items=[]를 반환하고 GET 안에서 색인 쓰기를 수행하지 않는다. 준비 완료 후 연락처가 없는 경우 contactTypes=[], total=0이다. 백그라운드 준비가 끝나면 UI가 자동 갱신한다. 원본 문의·상담 상태·결과·이력을 바꾸거나 접수를 합치지 않으며 문의 상세 간 이동에도 기존 입력 초안을 유지한다.


## 첫 사용 개선 (2026-11-13)

- 대행사 응답의 `clientScope: ALL|LINKED`는 현재 그룹의 실제 조회 범위다. 광고주 목록 배열과 권한 판정은 유지한다. LINKED의 빈 목록은 담당 배정 대기로 안내하며 전체 광고주 수를 노출하거나 권한을 넓히지 않는다.
- 회사 심사 응답은 `businessCheckReason`을 포함한다. 검증 실패의 원인을 분류한 값이며 인증키·외부 응답·예외 원문은 포함하지 않는다. 미설정·거절·일시 장애는 UNAVAILABLE이며 승인 조건을 바꾸지 않는다.
- 모바일 문의 검색은 상세 필터를 접고 선택 개수를 표시한다. 필터 값과 펼침 상태는 동일 업무 훅에서 유지한다. 고객 연락 정보·메모를 상세 상단에 두고 부가 이력·원문·설정은 공통 Disclosure로 조립한다.

## 회사별 업무 안내·등록 문의 보강 (2026-11-13)

- GET `/admin/v1/agency-companies/{agencyCompanyId}/permission-groups/{groupId}/usage`, GET `/admin/v1/system/permission-groups/{groupId}/usage`: 그룹 관리 권한으로 연결된 사람·회사·초대 기록을 조회한다. `{connections,referenceCount,truncated}`, 최대 100건 미리보기이며 전체 참조 수와 인원 수는 다르다. 타 대행사 그룹은 404다.
- 권한 정의 응답의 `delegable`은 현재 관리자가 부여할 수 있는지를 표시한다. 저장 시 실제 권한·범위를 다시 검사한다.
- GET `/admin/v1/agency-companies/{agencyCompanyId}/invitations/groups`, GET `/admin/v1/agency-companies/{agencyCompanyId}/client-companies/{clientCompanyId}/invitations/groups`: 현재 초대 관리·부여 범위에서 선택 가능한 그룹만 반환한다. 기존 초대 생성·수락 검사는 유지한다.
- GET `/admin/v1/company-reviews/{id}/messages?before=...`: 해당 신청 읽기 권한, `{items,nextBefore}`, 최신순 25건.
- POST 같은 `/messages`: 등록 관리 또는 시스템 심사 권한과 인증 이메일, `{body,requestKey}`. Unicode 1~2,000자, UUID 키, 200 응답. 동일 작성자·내용 재시도는 같은 결과, 다른 내용의 키 재사용은 400. 타 회사 신청은 404다.
- 랜딩 목록의 `activeDraftRevision`과 `publishedAt`은 현재 활성 공개본의 저장 버전과 게시 시각이며 공개본이 없으면 null이다. 저장 초안 리비전과 다를 수 있다.
- 문의 알림의 `customer`는 기존 접수 스냅샷에서 계산한 이름·연락처다. 알림 테이블에 답변·연락처를 복제하지 않으며 기존 문의 조회·알림 권한 교집합을 유지한다. 화면은 이름 또는 가린 연락처로 구별한다.

자세한 필드와 실제 경로는 [OpenAPI](file:///Users/dhkim/Desktop/ml-project/markestream/contracts/openapi.yaml)를 기준으로 한다.
