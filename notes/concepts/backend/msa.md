---
title: "서비스 분리와 MSA"
type: "concept"
source_project: "markestream"
imported_from: "docs/concepts/backend/msa.md"
imported_at: "2026-11-16"
source_sha256: "c142c4b2562e9d6ca56edbaeb841650fa6c9719b4c2b5a7b09991fcb58791144"
import_review: "not-reassessed"
tags: ["learning", "imported", "markestream"]
learning_status: "learning"
---

> [!info] 마케스트림 docs에서 이관한 기록
> 이전 경로: `docs/concepts/backend/msa.md` · 이관일: 2026-11-16 · 원본 정리일: 2026-11-16. 이관 후 사용자의 요청으로 원본 파일을 정리했다. 본문 안의 날짜·구현·검증·학습 상태는 작성 당시의 기록이며, 이관·삭제만으로 현재 상태를 다시 검증한 것은 아니다.
> [이관 목차](../../projects/markestream/imported-learning.md) · [현재 대화·자기 언어 학습 방법](../../learning-workflow.md)

# 서비스 분리와 MSA

- 갱신: 2026-11-11
- 학습 상태: 학습 중
- 프로젝트 적용: Admin API 구현, 나머지 서비스는 후속 범위
- 실험 상태: 미실행

## 한 문장으로

서비스를 나눈다는 것은 업무 책임과 배포·실행 경계를 정한다는 뜻이다. 폴더가 여러 개라는 사실만으로 독립적인 서비스 운영이 완성되지는 않는다.

## 왜 필요한가?

관리자 업무, 공개 문의 접수, 오래 걸리는 게시 작업은 요청 특성과 장애 영향이 다를 수 있다. 각각의 책임과 확장 필요를 따로 생각할 수 있다.

## 마케스트림 설계에서의 흐름

| 실행 단위 | 목표 책임 | 현재 코드에서 확인한 범위 |
| --- | --- | --- |
| Admin API | 대행사·광고주·랜딩 관리 | 사용자 등록, 대행사 생성·조회, 광고주 생성·조회 |
| Inquiry API | 공개 페이지·문의 접수·문의 상태 | 모듈 자리와 README |
| Publisher Worker | 게시 스냅샷을 HTML로 렌더링 | 모듈 자리와 README |

근거: [Admin API 구조](file:///Users/dhkim/Desktop/ml-project/markestream/backend/README.md), [Inquiry API](file:///Users/dhkim/Desktop/ml-project/markestream/backend/inquiry-api/README.md), [Publisher](file:///Users/dhkim/Desktop/ml-project/markestream/backend/publisher-worker/README.md).

## 헷갈린 점

모노레포는 코드를 관리하는 방식이다. 같은 저장소에 있어도 별도 프로세스로 배포할 수 있고, 여러 폴더에 나눠도 하나의 프로세스로 실행할 수 있다. 현재 설계는 초기 MySQL을 공유하므로 스키마 변경과 권한 관리에서 서비스 간 조율이 필요하다.

## 마케스트림에서는?

[시스템 설계](../../projects/markestream/reference/02-system-architecture.md)에 업무 책임과 쓰기 권한 경계가 있다. 서비스 간 호출, 게시 작업 재시도, 공유 스키마 변경의 영향을 구현과 실험으로 확인해야 한다. 설계 문서에 있는 전체 흐름을 현재 구현 완료로 읽지 않는다.

## 실제로 검증했는가?

미실행. 현재는 [로컬 Admin 요청 흐름](../../projects/markestream/labs/local-request-flow.md)부터 확인하고, Inquiry·Publisher가 구현되면 각각의 장애와 재시도를 실험한다.

## 문서를 덮고 답하기

1. 코드를 한 저장소에 둔다는 것과 서비스를 하나로 실행한다는 것은 같은가?
2. 서비스를 분리해도 DB를 공유하면 어떤 변경을 함께 조율해야 할까?

내 설명 / 복습 날짜: 아직 작성하지 않음.

[현재 시스템 개요](../../projects/markestream/architecture/system-overview.md) · [위키 목차](../../projects/markestream/imported-guides/README.md)

근거 확인일: 2026-11-11. 이 노트의 적용 내용은 현재 코드와 기존 프로젝트 설계를 기준으로 정리했다.

## 공통 학습 보관함에서 이어가기

[네트워크·요청 흐름 Canvas](../../maps/network-request-flow.canvas) · [함께 이관한 개념과 프로젝트 자료](../../projects/markestream/imported-learning.md)

원문에 있는 내 설명·복습 기록을 유지한다. 아직 작성하지 않은 자기 설명을 이관 과정에서 대신 채우지 않았다. 앞으로의 대화에서 이해한 내용을 자기 말로 이어 적는다.
