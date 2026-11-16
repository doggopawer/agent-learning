# 공통 학습 작업공간

여러 프로젝트에서 배운 기술·비즈니스·코드 개념을 한곳에 정리한다. 특정 프로젝트에 종속되지 않으며 사용자가 명령을 실행할 때만 학습 세션을 연다.

## 모든 프로젝트 채팅에서 시작하기

현재 프로젝트의 Codex 채팅에 아래 한 줄만 입력한다. 터미널 명령이 아니다.

```text
$learning-mentor
```

멘토가 현재 프로젝트를 선택하고 먼저 질문한다. 현재 대화에 작업 주제가 있으면 활용하며, 없으면 무엇을 만들거나 배우려는지 묻는다. 긴 프롬프트·프로젝트 경로·두 번째 노트 스킬 호출을 준비할 필요가 없다. 학습 기록은 항상 이 `agent-learning/notes` 보관함에 모인다.

학습은 **기술 목표 → 원리 설명·시연 → 실제 코드와 값 추적 → 작은 구현 → 조건을 바꾼 실험 → 도움을 줄인 변형 과제**로 진행한다. 기존 답변을 활용해 기초 확인 질문의 반복을 줄이고, 멘토가 실행 골격을 제공하면 사용자가 핵심 부분을 작성한다. 실제 코드·관찰 결과·그 이유를 노트와 Canvas에 연결한다. 이론 학습만 원하는 경우에는 추적·예측·설계 비교로 조정한다.

어느 프로젝트에서든 스킬을 찾도록 **한 번만** 사용자 스킬 경로에 연결한다. 이 컴퓨터에는 연결을 완료했다. 새 컴퓨터에서는 이 저장소를 복제한 뒤 저장소 루트에서 실행한다.

```bash
python3 -B scripts/install_skills.py
```

설치기는 `~/.agents/skills/learning-mentor`, `~/.agents/skills/obsidian-notes`를 이 저장소의 스킬에 연결한다. 기존에 같은 이름의 다른 스킬이 있으면 보존하고 중단한다. 저장소를 이동하면 링크 위치를 확인해야 한다. 스킬 목록에 표시되지 않으면 Codex를 한 번 재시작한다. 이 설정은 해당 컴퓨터의 로컬 Codex에 적용되며 다른 컴퓨터·클라우드에는 각각 설치해야 한다.

## 실행 명령

별도 터미널 학습 세션을 열고 싶으면 학습할 프로젝트 폴더에서 실행한다.

```bash
~/Desktop/ml-project/agent-learning/learn "오늘 작업한 코드의 핵심 개념을 질문부터 시작해 줘"
```

주제를 생략하면 멘토가 먼저 묻는다. 현재 폴더가 Git 저장소 안이면 저장소 루트를 선택하고, 그 밖에서는 현재 폴더를 선택한다. 새 프로젝트는 이 작업공간의 `projects.json`에만 등록된다. 같은 이름의 다른 경로는 별도 ID로 구분한다.

다른 위치에서 프로젝트를 지정하거나, 특정 프로젝트 없이 개념만 공부할 수도 있다.

```bash
~/Desktop/ml-project/agent-learning/learn --project /path/to/project "트랜잭션을 공부하고 싶어"
~/Desktop/ml-project/agent-learning/learn --project markestream "광고주 회사 생성 흐름"
~/Desktop/ml-project/agent-learning/learn --concept "의존성 주입"
```

`learn`은 Codex CLI의 별도 대화형 터미널 세션을 열며 작업 디렉터리를 `agent-learning`으로 지정한다. `python3`(3.9 이상), `git`, `codex`가 PATH에 있어야 한다. 기존 개발 채팅이나 다른 ChatGPT 대화 내용을 자동으로 가져오지 않는다. 현재 코드·Git 변경 내역 또는 사용자가 제공한 맥락으로 공부한다.

실행 없이 확인하려면 `--dry-run`, 옵션 안내는 `--help`를 사용한다. `--dry-run`은 프로젝트를 등록하거나 AI 세션을 시작하지 않는다. `agent-learning` 안에서 실행할 때는 `--project` 또는 `--concept`로 대상을 지정한다.

## 직접 스킬 호출

현재 프로젝트 채팅에서도 주제를 붙여 호출할 수 있다. 주제는 선택 사항이다.

```text
$learning-mentor 광고주 회사 생성 흐름을 공부하고 싶어.
```

두 스킬은 `allow_implicit_invocation: false`로 설정했다. 전역 연결로 어느 프로젝트에서나 발견되지만 사용자가 호출할 때만 학습 역할로 진행한다. 원본 프로젝트에 자동 호출 문구·훅·셸 별칭은 추가하지 않는다. 멘토 호출 안에서 노트 정리도 처리한다. 노트만 정리하려면 `$obsidian-notes`를 직접 호출한다.

## 노트와 평가

Obsidian에서 **`agent-learning/notes`**를 보관함으로 열고 `index.md`부터 읽는다.

[카드형 학습 지도](notes/maps/learning-map.canvas)에 개념·프로젝트 적용·학습 세션을 색과 그룹으로 연결한다. 카드를 직접 이동·확대하고 링크에서 실제 노트로 갈 수 있다. [연결 목록과 상태](notes/maps/learning-map.md)도 함께 유지한다. 학습 기록을 남길 때 멘토가 지도도 갱신하며 사용자 배치는 보존한다. Obsidian의 전체 그래프나 로컬 그래프에서는 실제 노트 링크를 따라 탐색할 수 있다. 현재 연결한 첫 사례와 개념들은 아직 사용자 답변이 없는 준비 자료다.

| 위치 | 역할 |
| --- | --- |
| `AGENTS.md` | 선택한 원본 읽기 전용, 질문·교육·평가 규칙 |
| `projects.json` | 사용자가 선택한 프로젝트 ID와 경로 |
| `learn` | 현재 프로젝트로 수동 학습 세션 시작 |
| `scripts/install_skills.py` | 모든 로컬 프로젝트에서 직접 호출할 수 있도록 전역 연결 |
| `notes/concepts/` | 여러 프로젝트에서 공유하는 개념 |
| `notes/maps/learning-map.canvas` | 색·그룹·연결선으로 배치한 기본 학습 지도 |
| `notes/maps/learning-map.md` | 연결 이유·학습 상태·문서 안의 요약 그림 |
| `notes/projects/<project-id>/` | 실제 코드·업무 규칙·설계 근거 |
| `notes/sessions/<project-id>/` | 실제 질문·답변·평가 (`concepts/`는 공통 학습) |
| `records/notes/<project-id>/` | 재생성 가능한 노트 입력 (`concepts/`는 공통 학습) |
| `records/gates/<project-id>/` | 프로젝트·범위·코드에 묶인 평가·승인 기록 |
| `labs/<project-id>/<topic>/` | 수업에서 필요한 경우 만드는 독립 학습 예제·테스트 |

원본 프로젝트는 읽기 전용이다. 런처는 `workspace-write` 모드로 학습 폴더에서 시작하며 원본을 추가 쓰기 폴더로 지정하지 않는다. 이해도 통과 후에도 학습 에이전트는 제품을 구현하지 않는다. 개발 전달을 요청한 때만 세 영역 통과와 구체적 범위에 대한 명시적 승인 후 전달서를 작성한다. 기존 개발 에이전트에 학습 게이트를 강제하는 연결은 없다.

공통 개념 학습에는 불필요한 구현 승인을 요구하지 않는다. 공통 원리를 이해했다고 다른 프로젝트의 업무·코드 이해를 통과한 것으로 기록하지 않는다. 사용자 필기는 노트 자동 생성 영역 밖에 두면 재생성 시 보존된다.

학습용 예시·골격·실험은 이 작업공간의 `labs/`에서 별도 학습 데이터·실행 환경으로 진행할 수 있다. 원본 프로젝트의 설정·인증정보·실제 데이터를 사용하지 않는다. 학습용 실습과 제품 개발 전달의 이해도·승인 gate는 구분한다. 이번 지침 변경만으로 실습이 생성·실행되거나 기존 이해도가 통과한 것은 아니다.

## 로컬 검증

아래는 `agent-learning` 폴더에서 실행한다. 도구는 Python 표준 라이브러리를 사용한다.

```bash
python3 .agents/skills/obsidian-notes/scripts/notes.py upsert --input records/notes/markestream/client-company-creation.json
python3 .agents/skills/obsidian-notes/scripts/notes.py check
python3 .agents/skills/learning-mentor/scripts/check_handoff.py records/gates/markestream/client-company-creation.json
python3 -B -m unittest discover -s tests -v
```

실제 첫 평가 기록은 미응답·미승인 상태이므로 `eligible: false`, 종료 코드 2가 정상이다. 검증기는 사용자 이해도나 승인 진위를 판단하지 않고 기록의 일관성을 확인한다. 멘토는 실제 대화와 대조한다. 프로젝트 위치가 바뀌면 등록 경로와 노트 링크를 확인하고 해당 프로젝트의 평가·승인 유효성을 재검토한다.

참고: [Codex 스킬과 명시적 호출](https://learn.chatgpt.com/docs/build-skills), [AGENTS.md 적용 범위](https://learn.chatgpt.com/docs/agent-configuration/agents-md). 최초 설치 당시 기록은 [설치 검증](notes/sessions/2026-11-16-system-setup.md)에 보존했다.
