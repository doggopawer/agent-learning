---
title: "Lab 계획: Pod 교체와 요청 처리 관찰"
type: "lab-record"
source_project: "markestream"
imported_from: "docs/labs/pod-failover.md"
imported_at: "2026-11-16"
source_sha256: "da276308cf81ad3a3022a5ad19e23cdbfa7ecc93de7b1ca7320fbd4d89e43c8d"
import_review: "not-reassessed"
tags: ["learning", "imported", "markestream"]
---

> [!info] 마케스트림 docs에서 이관한 기록
> 이전 경로: `docs/labs/pod-failover.md` · 이관일: 2026-11-16 · 원본 정리일: 2026-11-16. 이관 후 사용자의 요청으로 원본 파일을 정리했다. 본문 안의 날짜·구현·검증·학습 상태는 작성 당시의 기록이며, 이관·삭제만으로 현재 상태를 다시 검증한 것은 아니다.
> [이관 목차](../imported-learning.md) · [현재 대화·자기 언어 학습 방법](../../../learning-workflow.md)

# Lab 계획: Pod 교체와 요청 처리 관찰

[위키 목차](../imported-guides/README.md) · [Node와 Pod](../../../concepts/kubernetes/node-pod.md) · [Service와 Ingress](../../../concepts/kubernetes/service-ingress.md)

- 작성 / 갱신: 2026-11-11
- 상태: 미실행 — 클러스터·배포 설정 준비 전
- 실행 환경 / 대상 / 실행일: 미확정

## 확인할 질문과 가설

API Pod 하나를 제거하면 다른 정상 Pod로 신규 요청이 전달되고, Deployment가 원하는 복제본 수를 회복하는가?

가설은 “복제본과 readiness, 정상 진입점과 여유 자원이 갖춰졌다면 서비스가 복구될 수 있다”이다. 요청 실패가 0건이거나 일정 시간 안에 반드시 복구된다고 가정하지 않는다.

## 실행 전 준비

- [ ] 데이터와 트래픽이 분리된 학습용 클러스터·네임스페이스 지정
- [ ] 배포 매니페스트와 이미지·Kubernetes·Traefik 버전 기록
- [ ] API 복제본 2개 이상, 실제 Node 배치·여유 용량 확인
- [ ] readiness와 정상 엔드포인트 확인
- [ ] 정상 진입점과 DB, 인증을 포함한 읽기 전용 요청 준비
- [ ] 요청 시각·응답 코드·지연을 기록할 방법 준비
- [ ] 제거할 Pod와 실험 중지·복구 담당 및 절차 확정

현재 저장소에는 이 준비를 완료한 근거가 없다. 따라서 실제 클러스터 이름이나 Pod 이름을 추측한 실행 명령을 넣지 않았다.

## 준비 후 실행할 순서

1. 실험 대상 컨텍스트와 네임스페이스를 확인하고, Deployment·Pod·Node·EndpointSlice의 시작 상태를 저장한다.
2. 인증된 읽기 요청을 일정 간격으로 보내 기준 상태를 관찰한다. 캐시된 화면이 아니라 API 응답을 측정한다.
3. 학습용으로 지정한 API Pod 하나를 제거하고 시각을 기록한다.
4. 요청 실패·지연, 엔드포인트 변경, 대체 Pod 생성과 Ready 전환을 관찰한다.
5. 원하는 복제본 수와 요청 성공이 회복됐는지 확인한다. 회복되지 않으면 이벤트·리소스·readiness·DB 접근을 확인한다.

Pod 삭제는 Node 전체 장애와 다르다. Node 종료, Control Plane 장애, DB 장애, Traefik 진입점 장애는 별도 실험으로 분리한다.

## 예상과 통과 기준

제거된 Pod가 전달 대상에서 빠지고 대체 Pod가 Ready가 되며, 요청 처리가 회복될 것으로 예상한다. 진행 중 연결이나 반영 지연으로 일부 요청은 실패할 수 있다.

실제 결과에서 복구 여부와 걸린 시간을 확인하고, 무엇이 요청 전달을 담당하고 무엇이 Pod를 다시 생성했는지 설명할 수 있어야 한다. 수치 기준이 필요하면 실행 전에 실험 목표에 맞춰 정한다.

## 실제 결과

미실행.

| 항목 | 관찰 결과 |
| --- | --- |
| 시작 복제본과 Node 배치 | 미실행 |
| 제거 시각 / 엔드포인트 변화 | 미실행 |
| 실패한 요청 수와 오류 | 미실행 |
| 대체 Pod Ready 시각 | 미실행 |
| 요청 처리 회복 시각 | 미실행 |

## 복구와 후속 기록

테스트용 요청 발생을 중단하고 원래 복제본·Ready 상태가 유지되는지 확인한다. 해결되지 않은 장애는 완료로 표시하지 않는다. 이 결과를 바탕으로 [Control Plane](../../../concepts/kubernetes/control-plane.md), [Traefik ADR](../adr/002-traefik.md), 시스템 개요의 확인 상태를 갱신한다.

## 현재 학습과의 연결

이 문서는 기존 실험 기록·계획을 보존한 것이다. 실습은 선택 사항이며 이관 과정에서 실행하지 않았다. [회사 생성에 대한 현재 대화 노트](../client-company-creation.md) · [이관 목차](../imported-learning.md)
