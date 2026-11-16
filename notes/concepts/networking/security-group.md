---
title: "Security Group"
type: "concept"
source_project: "markestream"
imported_from: "docs/concepts/networking/security-group.md"
imported_at: "2026-11-16"
source_sha256: "3641fc57646db1ca85caa7238928764620998023b2008e07dd979daa1e1ffe28"
import_review: "not-reassessed"
tags: ["learning", "imported", "markestream"]
learning_status: "learning"
---

> [!info] 마케스트림 docs에서 이관한 기록
> 이전 경로: `docs/concepts/networking/security-group.md` · 이관일: 2026-11-16 · 원본 정리일: 2026-11-16. 이관 후 사용자의 요청으로 원본 파일을 정리했다. 본문 안의 날짜·구현·검증·학습 상태는 작성 당시의 기록이며, 이관·삭제만으로 현재 상태를 다시 검증한 것은 아니다.
> [이관 목차](../../projects/markestream/imported-learning.md) · [현재 대화·자기 언어 학습 방법](../../learning-workflow.md)

# Security Group

- 갱신: 2026-11-11
- 학습 상태: 학습 중
- 프로젝트 적용: AWS 규칙은 저장소에서 미확인
- 실험 상태: 미실행

## 한 문장으로

Security Group은 연결된 AWS 리소스의 들어오고 나가는 트래픽을 허용 규칙으로 제어한다.

## 왜 필요한가?

네트워크 경로가 있다는 것과 특정 포트로 접근해도 된다는 것은 다르다. 공개 웹은 받을 수 있어도 DB 포트까지 누구에게나 열 필요는 없다.

## 어떻게 동작하는가?

Inbound는 출발지·프로토콜·포트를, Outbound는 목적지·프로토콜·포트를 기준으로 허용한다. Security Group은 상태를 추적하므로 허용된 연결의 응답은 반대 방향의 새 연결과 다르게 취급된다. [AWS Security Group 문서](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html)

| 학습용 통신 | 확인할 질문 |
| --- | --- |
| 방문자 → 공개 진입점 | 공개 서비스 포트로 들어오는 연결을 허용하는가? |
| 진입점 → API | 진입점에서 API의 수신 포트에 접근할 수 있는가? |
| API → DB | API 측 출발지에서 DB 포트로 접근하도록 허용했는가? |

이 표는 실제 적용된 AWS 규칙이 아니다. Kubernetes에서는 CNI와 실제 패킷 출발지에 따라 필요한 네트워크 설정을 추가로 확인한다.

## 헷갈린 점

Security Group은 경로를 만들어 주지 않는다. 접속 실패 시 DNS → 목적지 주소와 라우팅 → 통신 규칙 → 서버의 수신 주소·포트를 차례로 확인한다.

## 마케스트림에서는?

[Compose](file:///Users/dhkim/Desktop/ml-project/markestream/infra/compose.yaml)는 DB·Keycloak 포트를 `127.0.0.1`에 바인딩한다. 이는 로컬 포트 노출 설정이며 AWS Security Group과 같은 설정이 아니다. AWS 배포 때 별도 규칙이 필요하다.

## 실제로 검증했는가?

미실행. 실제 AWS 규칙을 수정하거나 접속을 시험하지 않았다.

## 문서를 덮고 답하기

1. 라우팅은 맞는데 연결이 거절되면 무엇을 살펴볼까?
2. 응답 트래픽과 반대편에서 새로 시작한 연결은 왜 다를까?

내 설명 / 복습 날짜: 아직 작성하지 않음.

[VPC와 Subnet](vpc-subnet.md) · [위키 목차](../../projects/markestream/imported-guides/README.md)

공식 자료 확인일: 2026-11-11.

## 공통 학습 보관함에서 이어가기

[네트워크·요청 흐름 Canvas](../../maps/network-request-flow.canvas) · [함께 이관한 개념과 프로젝트 자료](../../projects/markestream/imported-learning.md)

원문에 있는 내 설명·복습 기록을 유지한다. 아직 작성하지 않은 자기 설명을 이관 과정에서 대신 채우지 않았다. 앞으로의 대화에서 이해한 내용을 자기 말로 이어 적는다.
