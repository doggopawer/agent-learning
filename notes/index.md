---
title: "공통 학습 홈"
type: index
tags: [learning]
---

# 공통 학습 홈

에이전트로 작업하는 여러 프로젝트에서 배운 개념을 모으는 공간이다. 공통 원리는 개념 노트에, 실제 코드·업무·설계는 프로젝트별 노트에 기록해 서로 연결한다.

[학습 진행 방법과 실행 명령](learning-workflow.md)

**[카드형 학습 지도](maps/learning-map.canvas)**에서 개념·프로젝트 적용·학습 세션을 펼쳐 본다. [연결 목록과 학습 상태](maps/learning-map.md)도 함께 확인할 수 있다.

어느 프로젝트의 Codex 채팅에서든 **`$learning-mentor`** 한 줄로 시작한다. 멘토가 현재 프로젝트를 확인하고 필요한 질문을 먼저 한다.

## 마케스트림 docs에서 이관한 학습

**[기존 학습 자료 이관 목차](projects/markestream/imported-learning.md)** · **[네트워크·요청 흐름 Canvas](maps/network-request-flow.canvas)**

VPC·Subnet·NAT·Security Group, Node·Pod·Control Plane·Service·Ingress, ALB·Traefik·API Gateway·MSA의 개념 노트 10개를 공통 개념 폴더에 이관했다. 시스템 구조·ADR·제품 명세·당시 세션·실험 계획·기존 안내와 양식을 포함해 Markdown 문서 34개를 연결했다. 원문과 당시 상태를 보존한 이관 자료이며 새 이해도 평가나 실험 완료를 뜻하지 않는다.

## 공통 개념

`concepts/`에 주제별 원리·적용 조건·복습 질문을 쌓는다. 프로젝트별 사례를 연결하되 프로젝트 이해도 평가나 승인을 공유하지 않는다. [개념 양식](templates/concept.md)을 참고한다.

요청 흐름과 광고주 회사 생성은 첫 답변을 받아 학습 중이다. 트랜잭션·권한의 상세 학습은 준비 단계이며 이해도 통과 기록은 아직 없다.

- [계층별 책임과 요청 흐름](concepts/layered-request-flow.md)
- [트랜잭션 경계](concepts/transaction-boundaries.md)
- [인증과 인가](concepts/authentication-and-authorization.md)

## 프로젝트 사례

**진행할 학습: [마케스트림 기존 기능 학습 순서](projects/markestream/learning-roadmap.md)**. 첫 주제는 광고주 회사 추가이며 현재는 회사·계정·운영 승인, 객체 생성·DB 저장의 차이를 보충하고 재질문 답변을 기다리는 단계다.

| 프로젝트 | 코드·업무 노트 | 학습 세션 |
| --- | --- | --- |
| AdDock / MarkeStream (`markestream`) | [광고주 회사 생성과 권한 경계](projects/markestream/client-company-creation.md) | [첫 진단 질문](sessions/markestream/client-company-creation.md) |

MarkeStream은 **학습 중**이다. 기술·업무 첫 답변을 기록했고 코드 읽기 재질문은 답변 대기다. 전체 이해도 통과·구현 승인은 없다. 새로운 학습은 명령에서 선택한 프로젝트와 주제로 시작한다.

## 양식과 시스템 기록

- [질문·답변·평가 양식](templates/session.md)
- [개발 전달서 양식](templates/handoff.md)
- [최초 설치 검증](sessions/2026-11-16-system-setup.md)
- [공통 학습 전환과 수동 명령 검증](sessions/2026-11-16-manual-launch.md)
- [모든 프로젝트에서 한 줄 호출 검증](sessions/2026-11-16-global-invocation.md)

원본 코드는 보관함 밖의 파일 링크와 저장소 기준 경로·심볼·해시로 연결한다. Obsidian 그래프에는 보관함 내부 노트 관계가 표시된다.
