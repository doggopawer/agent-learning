---
title: "AdDock 계정·회사·권한그룹"
type: "project-reference"
source_project: "markestream"
imported_from: "docs/07-permissions.md"
imported_at: "2026-11-16"
source_sha256: "3c2ba88fc33ad89f87d90e11123bcfa186714e8709fea1988dc49d4748049b46"
import_review: "not-reassessed"
tags: ["learning", "imported", "markestream"]
---

> [!info] 마케스트림 docs에서 이관한 기록
> 이전 경로: `docs/07-permissions.md` · 이관일: 2026-11-16 · 원본 정리일: 2026-11-16. 이관 후 사용자의 요청으로 원본 파일을 정리했다. 본문 안의 날짜·구현·검증·학습 상태는 작성 당시의 기록이며, 이관·삭제만으로 현재 상태를 다시 검증한 것은 아니다.
> [이관 목차](../imported-learning.md) · [현재 대화·자기 언어 학습 방법](../../../learning-workflow.md)

# AdDock 계정·회사·권한그룹

2026-11-13 현행 코드 기준. 변경 이력용 `audit_logs`는 이번 범위에 포함하지 않는다. 원격 운영 배포와 실제 고객 파일럿은 미실행이다.

## 회사와 계정

| 테이블 | 의미 |
| --- | --- |
| `agency_companies` | 대행사 회사 |
| `client_companies` | 광고주 회사. `agency_company_id`로 관리 대행사 한 곳에 연결 |
| `agency_users` | 대행사 직원 계정 |
| `client_users` | 광고주 측 계정 |
| `admin_users` | 시스템 운영 계정 |
| `agency_memberships` | 직원 계정의 대행사 소속과 권한그룹 |
| `client_memberships` | 광고주 계정의 회사 소속과 권한그룹 |
| `client_assignments` | 대행사 직원에게 배정한 담당 광고주 |

계정 ID는 종류별로 독립적이다. `(AGENCY_USER,1)`과 `(CLIENT_USER,1)`은 다른 계정이다. OIDC `issuer + subject`는 각 계정 테이블에서 유일하다. 비밀번호는 저장하지 않는다. 소속별 그룹은 하나이며, 같은 계정이 다른 회사 소속에서 다른 그룹을 사용할 수 있다. 여러 대행사에 연결되는 동일 광고주 회사의 다대다 모델은 이번 범위에 포함하지 않는다.

## 권한과 그룹

`permission_categories`는 분류·정렬, `permissions`는 구현된 기능의 코드·표시 이름·업무 영역, `permission_targets`는 제공 대상, `permission_groups`는 공통 그룹, `permission_group_permissions`는 실제 부여 권한이다. 대행사·광고주용 그룹은 `agency_company_id` 필수이며 시스템 그룹은 NULL이다. DB CHECK와 복합 FK가 그룹 대상과 소유 대행사를 제한한다. `permission_group_workspaces`는 없다.

| 기본 그룹 | 대상 | 데이터 범위 | 초기 기능 |
| --- | --- | --- | --- |
| 팀장 | 대행사 계정 | 대행사 전체 | 제공 대상이 허용하는 대행사 업무 권한 전체 |
| 마케터 | 대행사 계정 | 담당 광고주 | 회사 조회·등록·수정, 랜딩 조회·생성·편집·게시·중단, 문의 조회·상태 변경 |
| 광고주 | 광고주 계정 | 연결된 회사 | 회사·랜딩 조회, 문의 상담·담당자 배정·메모·결과·재연락·알림·중복 확인 |
| 시스템 관리자 | 시스템 계정 | 모든 대행사 | 제공 대상이 허용하는 전체 권한 |
| 시스템 운영자 | 시스템 계정 | 모든 대행사 | 전체 대행사 및 광고주·랜딩·문의 조회 |

대행사를 만들면 팀장·마케터·광고주 그룹을 준비하고 생성자를 팀장에 연결한다. 회사 등록 자체로 광고주 계정을 만들지는 않는다. 승인된 회사에 이메일로 초대하고, 광고주 이용자가 계정 가입·이메일 인증 후 초대를 수락하면 선택한 그룹을 사용한다. 기본 선택은 ‘광고주’다. 그룹 이름과 권한은 수정할 수 있다. 기본 그룹 및 소속·계정 참조가 남은 그룹은 삭제하지 않는다. 새 회사 생성자가 대행사 직원이면 그 회사의 담당자로 자동 연결한다.

## 권한 정책과 부여 권한

코드·업무 영역은 개발과 마이그레이션에서 정의한다. 시스템 관리자는 권한 정책 화면에서 대행사·광고주·시스템 중 제공할 대상을 설정한다. 각 대행사는 제공된 목록에서 그룹별 권한을 선택한다. 시스템 업무 영역은 시스템 계정에만 제공할 수 있다. 대상 축소는 영향 그룹의 해당 권한을 함께 제거하고 그룹 버전을 증가시킨다. 화면은 영향 그룹 수를 확인시킨다. 정책 복구가 이전 그룹 권한을 자동 복구하지는 않는다.

개인 실행 권한과 부여 권한은 다르다. `group.delegate_all`(대행사 전체 업무 권한 부여)은 해당 대행사의 허용된 업무 권한을 부여하는 권한이며 기본 팀장이 가진다. 시스템 `system.policy.manage`는 플랫폼 권한을 부여할 수 있는 운영 권한이다. 이 권한이 없는 제한 관리자는 자신이 보유한 기능·데이터 범위를 넘어 부여할 수 없다. 대행사 그룹에는 시스템 권한을 넣을 수 없다.

새 기능은 같은 변경에서 권한 코드·분류·대상 정책 마이그레이션·서버 검사·화면 검사·테스트를 추가한다. 기존 그룹에는 자동 부여하지 않는다. 기본 그룹 템플릿을 바꾸면 새 대행사부터 적용한다. 팀장의 명시적 권한 부여 기능으로 새 권한을 선택할 수 있다. 마케터의 초기 권한은 명시 목록으로 관리하며 접두사 전체를 허용하지 않는다.

## 서버 판정과 동시성

[권한 이전 SQL](file:///Users/dhkim/Desktop/ml-project/markestream/database/migrations/V3__accounts_and_permission_groups.sql)의 `effective_access_grants` 뷰는 활성 계정·소속·그룹·대상 정책·담당 관계를 조합한다. 0 범위 ID는 뷰 안에서만 전체 범위를 뜻하며 실제 업무 ID로 받지 않는다. Admin과 Inquiry는 각자 소유한 읽기 전용 JPA 모델과 Repository로 같은 뷰를 조회한다. 다른 모듈의 JPA 엔티티를 공유하지 않는다. 목록은 조회 단계에서 회사 ID 조건을 적용한다.

업무 쓰기는 정책 분류 행을 일정한 순서로 공유 잠금하고 현재 권한을 확인한다. 그룹·정책·소속·담당·활성 상태 변경은 같은 행을 배타 잠금한다. READ_COMMITTED로 잠금 획득 후의 현재 정책을 확인한다. 권한 변경은 빈도가 낮으므로 현재 MVP는 하나의 짧은 정책 변경 경계를 사용한다. 외부 HTTP 호출 중에는 잠금을 유지하지 않는다.

대행사에는 `member.manage`·`group.manage`·`group.delegate_all`을 가진 활성 관리자가 최소 한 명 있어야 한다. 시스템에는 `system.account.manage`·`system.group.manage`·`system.policy.manage`를 가진 활성 운영자가 최소 한 명 있어야 한다. 이름이나 기본 그룹 키로 관리자 여부를 판단하지 않는다. 의도적으로 중지한 대행사는 활성 관리자 검사 대상에서 제외하지만 재개할 때는 다시 검사한다. 관리자가 없으면 재개를 거절한다. 시스템은 중지된 회사의 기존 구성원과 같은 회사의 권한그룹을 지정하여 관리자 소속 복구와 재개를 원자적으로 처리할 수 있다. 이 복구에는 직원 관리와 그룹 위임 권한도 필요하며 신규 계정을 연결하지 않는다.

그룹과 대상 정책 변경은 현재 `version`을 받으며 오래된 값은 409다. Admin → Inquiry 토큰은 `actor_type`·`actor_id`·`agency_company_id`를 서명에 포함한다. Inquiry는 대상 대행사와 현재 권한을 다시 검사하며 브라우저의 행위자 헤더를 사용하지 않는다.

## 로그인과 초기 운영 계정

일반 로그인·회원가입은 `/` 하나로 제공한다. `?account=agency`, `?account=client`는 이전 링크 호환용으로만 받아들이며 로그인 종류 선택에 사용하지 않는다. 시스템 운영 진입은 기존 `/?account=admin`을 유지한다.

인증 뒤 GET `/admin/v1/me/session`이 서명된 issuer·subject로 본인의 활성 회사 소속을, 인증 이메일로 본인이 받은 초대를 조회한다. 이 조회는 계정·소속을 생성하거나 권한을 부여하지 않는다. 회사가 하나면 바로 연결하고, 여러 회사 또는 확인할 초대가 있으면 회사 이름으로 선택한다. 초대 링크는 해당 초대의 수신 이메일과 유효성을 먼저 확인한다.

직원·광고주 계정과 기존 OIDC 클라이언트는 내부적으로 유지한다. 필요한 경우 기존 SSO로 적합한 클라이언트의 토큰을 다시 받아 연결하므로 사용자에게 계정 종류를 고르게 하지 않는다. 서명된 account_type·azp 조합과 실제 업무 API의 계정·소속·권한 검사는 유지한다. 회사 선택 키와 브라우저 저장값은 권한 근거가 아니다. 시스템 권한은 공통 회사 목록에 표시하거나 자동 선택하지 않는다.

OIDC 콜백은 등록된 루트 `/`를 사용한다. 초대 복귀 경로와 내부 인증 클라이언트 선택은 브라우저 세션에 유지하고, 회사 선택은 issuer·subject별로 기억하되 매번 서버 목록과 대조한다. 로그아웃 시 현재 회사 선택과 내부 클라이언트 기억을 초기화한다. 광고주와 직원 소속을 서로 합치거나 기본 그룹을 복사하지 않는다.

운영 최초 계정은 검증한 OIDC issuer/subject를 `MARKESTREAM_BOOTSTRAP_ADMIN_ISSUER`, `MARKESTREAM_BOOTSTRAP_ADMIN_SUBJECT`에 전달해 시스템 계정 테이블이 비어 있을 때만 생성한다. 이후 계정은 시스템 관리 화면에서 등록·그룹 변경·비활성화한다. 일반 직원이나 기존 OWNER를 시스템 운영자로 자동 승격하지 않는다. 로컬 개발용은 `node scripts/run-admin-dev.mjs`가 realm의 개발 계정 식별자를 사용한다.

## 기존 데이터 이전

V1·V2는 변경하지 않는다. V3는 회사·계정 이름과 외래키를 바꾸면서 ID를 보존한다. OWNER는 팀장, OPERATOR는 기존 전체 광고주 범위를 유지하는 마케터, VIEWER는 읽기 전용 보존 그룹으로 이전한다. VIEWER가 있는 대행사에만 보존 그룹을 만든다. OPERATOR가 없는 기존 대행사의 기본 마케터는 담당 범위를 사용한다.

게시 요청·문의 상태 이력은 `agency_user`·`client_user`·`admin_user` 참조 중 정확히 하나를 갖는다. 기존 행위자는 agency 참조로 이전한다. 게시 스냅샷 JSON의 기존 `workspaceId`·`clientId` 키는 Jackson 명시 매핑으로 유지한다. 새 API 경로는 회사 용어를 사용하며 기존 `/workspaces/.../clients` 경로는 저장된 링크의 호환 별칭이다.

## 구현 근거와 확인

- [권한 판정](file:///Users/dhkim/Desktop/ml-project/markestream/backend/admin-api/src/main/java/com/markestream/admin/permission/application/PermissionAccessService.java), [그룹·정책 관리](file:///Users/dhkim/Desktop/ml-project/markestream/backend/admin-api/src/main/java/com/markestream/admin/permission/application/PermissionService.java)
- [계정](file:///Users/dhkim/Desktop/ml-project/markestream/backend/admin-api/src/main/java/com/markestream/admin/account/application/AccountService.java), [시스템 계정](file:///Users/dhkim/Desktop/ml-project/markestream/backend/admin-api/src/main/java/com/markestream/admin/account/application/SystemAccountService.java)
- [기존 데이터 이전 테스트](file:///Users/dhkim/Desktop/ml-project/markestream/backend/admin-api/src/test/java/com/markestream/admin/PermissionMigrationTest.java), [권한 통합 테스트](file:///Users/dhkim/Desktop/ml-project/markestream/backend/admin-api/src/test/java/com/markestream/admin/PermissionIntegrationTest.java), [서비스 연결 테스트](file:///Users/dhkim/Desktop/ml-project/markestream/backend/admin-api/src/test/java/com/markestream/admin/MvpIntegrationTest.java)
- [프론트 업무 훅](file:///Users/dhkim/Desktop/ml-project/markestream/apps/admin-web/src/features/permissions/usePermissionManagement.ts), [API 계약](04-api-spec.md)

[OWASP 권한 검증](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)의 매 요청 검사·기본 거절과 [대행사 간 격리 지침](https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html)을 참고했다. 확인일 2026-11-11. 구현 검증 결과는 [MVP 현황](06-mvp-status.md)에 기록한다.

## 회사 등록과 초대

V4의 신규 회사 등록·심사 권한과 승인 단계는 [등록·초대 명세](08-registration.md)를 따른다. 기존 그룹에는 자동 부여하지 않는다. 회사가 미승인인 대행사는 회사 등록 외 업무를 사용할 수 없고 광고주 미승인은 게시·수집·광고주 초대를 제한한다. 이메일 초대 수락도 현재 위임 권한과 회사 범위를 다시 검사한다. 이름·이메일 프로필은 서명된 로그인 정보에서 갱신한다.

대행사 선택과 목록 화면의 기능 제공 여부는 현재 그룹·대상 정책으로 확인하고, 실제 회사 데이터 범위는 effective_access_grants로 제한한다. 담당 회사가 아직 없는 마케터는 회사 목록을 빈 결과로 열 수 있으며, 새 회사를 만들면 생성자 담당 배정 후 그 회사만 표시된다. 기능 코드가 있다는 이유로 미배정 회사의 상세를 열 수는 없다.

구성원 변경 API는 기존 활성 소속의 그룹 변경과 회수만 담당한다. 직원·광고주의 신규 소속과 회수 후 재참여는 이메일 초대의 명시적 수락으로 만든다. 대행사 목록은 소속 그룹과 현재 권한을 일괄 조회하며, 담당 회사가 없는 마케터에게도 기능 목록을 제공하되 실제 회사 범위는 기존 권한 검사로 제한한다.

## 문의 상담 권한 (V5)

`inquiry.assign`(담당자 배정), `inquiry.note.read`(상담 메모 조회), `inquiry.note.create`(상담 메모 작성)는 문의 분류·CLIENT 영역이며 세 계정 종류 모두 대상 정책으로 제공할 수 있다. 실제 사용에는 `inquiry.read`와 같은 회사 범위가 함께 필요하다. 배정 후보는 CLIENT_USER이며 해당 회사의 활성 소속과 `inquiry.read`·`inquiry.update`가 필요하다. 담당 배정으로 권한이 생기지는 않는다.

기존 그룹에는 세 권한을 자동으로 부여하지 않는다. 권한그룹 화면에서 필요한 항목을 명시적으로 선택한다. 새 대행사의 팀장은 모두, 마케터는 메모 조회·작성만 기본으로 받으며 담당자 배정은 별도로 허용한다. 2026-11-13부터 새 대행사의 기본 광고주 그룹에는 문의 상담 권한도 포함한다. 기존 대행사의 광고주 그룹은 자동 갱신하지 않으므로 상담을 맡길 직원의 권한을 명시적으로 확인해야 한다.

문의 키워드·기간·특정 담당자 검색과 `/inquiries/assignees`는 기존 문의 조회의 조건 확장이므로 `inquiry.read`를 적용한다. 담당자 필터 목록에는 조회 가능한 문의에 지정된 광고주 직원만 제공하며 `inquiry.assign`을 요구하거나 소속·회사 범위를 늘리지 않는다. 기존 그룹·제공 대상 정책은 변경하지 않는다.

## 상담 결과 권한 (V6)

`inquiry.outcome.update`(상담 결과 변경)는 문의 분류·CLIENT 범위이며 대행사·광고주·시스템 계정에 제공할 수 있다. 결과·메모와 변경 이력 조회는 기존 `inquiry.read`에 포함하며, 변경에는 두 권한과 같은 회사 범위가 필요하다. 진행 상태 변경 권한 `inquiry.update`와는 독립적이다.

기존 그룹에는 자동 부여하지 않는다. 새 대행사의 팀장·마케터에는 결과 변경을 기본으로 제공하고 새 대행사의 기본 광고주 그룹에도 결과 변경을 제공한다. 기존 그룹은 권한그룹 화면에서 ‘상담 결과 변경’을 명시적으로 허용해야 한다. 결과 변경으로 소속·담당·다른 업무 권한을 부여하지 않는다.

## 재연락 일정 관리

`inquiry.follow_up.manage`(재연락 일정 관리)는 문의 분류·CLIENT 범위이며 대행사·광고주·시스템 계정에 제공할 수 있다. 조회는 기존 `inquiry.read`, 예약·변경·완료·취소는 두 권한을 같은 광고주 범위에서 요구한다. `inquiry.update`, `inquiry.assign`, `inquiry.outcome.update`와 독립적이다. 기존 그룹은 자동 갱신하지 않는다. 새 대행사의 팀장·마케터·광고주 템플릿에 포함한다. 기존 광고주 직원에게 일정 관리를 맡기려면 해당 그룹에 명시적으로 허용한다.

## 문의 알림

`inquiry.notification.receive`(문의 알림 받기)는 문의 분류·CLIENT 범위이며 세 계정 종류에 제공할 수 있다. 알림 조회·읽음 처리는 같은 회사의 `inquiry.read`와 이 권한의 교집합을 사용한다. 새 접수 알림은 현재 권한 범위에 공유하며, 배정·재연락 알림은 현재 담당 광고주 직원에게만 보인다. 대행사 직원·시스템 계정에는 배정된 직원의 개인 알림이 표시되지 않는다. 서버에서 목록·전체 안 읽은 개수·단건 읽음 처리마다 권한, 현재 회사 운영 상태와 대상 조건을 확인한다. 소속/제공 대상 회수·회사 비활성화 시 더 이상 접근할 수 없다.

기존 그룹에 자동 부여하지 않는다. 새 대행사의 팀장·마케터·광고주 템플릿에 포함한다. 기존 광고주 직원에게 알림을 제공하려면 해당 그룹에 명시적으로 허용한다. 알림 받기는 상담 변경 권한을 부여하지 않으며 개인별 읽음은 다른 사람의 알림을 변경하지 않는다.

## 중복 문의 확인

`inquiry.duplicate.read`(중복 문의 확인)는 문의 분류·CLIENT 범위이며 세 계정 종류에 제공할 수 있다. 현재 문의와 같은 광고주 회사의 `inquiry.read`와 이 권한을 함께 요구한다. 목록·전체 개수·페이지 경계와 이전 상세 조회에서 현재 회사 범위를 다시 확인한다. 다른 회사·대행사나 소속 회수, 제공 대상 회수는 기존 403/404 정책을 유지한다. 이 권한은 접수·답변·담당자·상태를 변경하지 않는다.

기존 그룹에 자동 부여하지 않는다. 신규 대행사 팀장·마케터·광고주 템플릿에 포함한다. 기존 광고주 직원도 필요하면 해당 그룹에 명시적으로 부여한다. 비교 항목 종류·이전 접수 요약만 추가 제공하며 고객 연락처 원문이나 비교용 해시는 반환하지 않는다.

## 회사별 화면·위임 안내 (2026-11-13)

광고주 메뉴는 선택한 자기 회사의 문의·랜딩·구성원·회사 정보 중 실제 허용된 기능만 직접 제공한다. 첫 진입은 문의 → 랜딩 → 구성원 → 회사 정보 순이며 미승인 회사의 신청 권한이 있으면 등록 상태로 안내한다. 같은 대행사의 여러 광고주 회사에 참여해도 각 회사의 현재 권한을 별도로 조회한다. 이전 전체 문의 주소도 광고주는 선택한 회사로 제한하고, 다른 회사 상세 링크에는 회사 전환을 안내한다. 받은 초대는 개인 계정 메뉴이며 회사 설정이 아니다.

신규 기본 광고주 그룹의 정확한 코드는 `client.read`, `landing.read`, `inquiry.read`, `inquiry.update`, `inquiry.assign`, `inquiry.note.read`, `inquiry.note.create`, `inquiry.outcome.update`, `inquiry.follow_up.manage`, `inquiry.notification.receive`, `inquiry.duplicate.read`다. 기존 그룹·소속을 확대하는 데이터 마이그레이션은 없다.

권한 카탈로그의 `delegable`은 현재 행위자의 부여 가능 여부다. 그룹 편집에서 선택 불가능한 항목을 비활성화하고 조회 권한 의존성을 안내한다. 초대 그룹 선택은 전용 `/invitations/groups` 조회를 사용해 현재 부여 가능한 그룹만 제공한다. 저장·수락 시 서버 재검사는 유지한다. 그룹의 `/usage`는 사람 이름·이메일·회사·활성/회수/만료 상태와 참조 기록 수를 최대 100건 표시한다. 참조 수에는 과거 소속과 초대가 포함되므로 인원수와 다르다. 기존 그룹 저장 전 변경 권한·회사 범위·연결 기록 수를 다시 확인한다.

시스템 계정 화면은 이름·이메일·계정 종류로 식별한다. 운영 계정 추가도 이미 가입한 사용자를 선택하며 OIDC 식별자를 직접 입력받지 않는다. 기능 권한은 기존 서버 검사를 따르고 시스템 설정은 ‘시스템 전체 · 모든 대행사’ 범위로 표시한다. 대행사 이용 관리는 계정 관리와 별도 메뉴다.

대행사 직원·시스템 계정은 문의 관리·랜딩페이지·광고주 구성원·광고주 회사 정보의 각 메뉴에서 회사를 선택한다. 선택 목록은 `/client-companies/work?section=...`에서 현재 업무 권한과 effective_access_grants의 회사 범위를 적용하며 별도 `client.read`를 요구하지 않는다. 문의는 `inquiry.read`, 랜딩은 `landing.read`, 구성원은 `client_user.read/manage` 또는 `assignment.manage`, 회사 정보는 `client.registration.read/manage` 중 허용된 코드의 회사 범위 합집합을 사용한다. 담당 회사가 없는 유효 대행사 직원은 빈 목록으로 안내하며 회사 상세 권한 검사는 유지한다. 이용 중지 회사는 회사 정보 목록에서만 조회할 수 있다.

기본 메뉴는 대행사 권한, 실제 업무·버튼은 선택한 회사의 현재 권한으로 판단한다. 회사 변경은 현재 업무를 유지하며 다른 업무로 대체하지 않는다. 메뉴 변경 시 마지막 회사를 현재 업무 목록에서 다시 확인하고, 불가하면 첫 허용 회사를 선택한다. 선택 기억은 권한 근거가 아니다. 회사 내부 탭과 전체 회사 문의 화면은 제공하지 않는다. 대행사 설정에는 광고주 선택을 적용하지 않고 광고주 계정에는 대행사용 회사 목록을 추가하지 않는다.
