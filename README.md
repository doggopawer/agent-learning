# 공통 학습 작업공간

여러 프로젝트에서 배운 기술·비즈니스·코드 개념을 한곳에 정리한다. 특정 프로젝트에 종속되지 않으며 사용자가 명령을 실행할 때만 학습 세션을 연다.

## 실행 명령

학습할 프로젝트 폴더의 터미널에서 실행한다.

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

Codex에서 `agent-learning`을 작업공간으로 연 뒤에는 다음처럼 요청할 수 있다.

```text
$learning-mentor 프로젝트 ID markestream의 광고주 회사 생성 흐름부터 질문해 줘. $obsidian-notes로 학습 내용을 기록해 줘.
```

두 스킬은 `allow_implicit_invocation: false`로 설정했다. 원본 프로젝트의 자동 호출 문구·훅·전역 스킬·셸 별칭은 추가하지 않았다. 원본 프로젝트의 채팅에서 `$learning-mentor`만 입력하면 이 형제 폴더의 스킬이 발견된다고 가정하지 않는다.

## 노트와 평가

Obsidian에서 **`agent-learning/notes`**를 보관함으로 열고 `index.md`부터 읽는다.

| 위치 | 역할 |
| --- | --- |
| `AGENTS.md` | 선택한 원본 읽기 전용, 질문·교육·평가 규칙 |
| `projects.json` | 사용자가 선택한 프로젝트 ID와 경로 |
| `learn` | 현재 프로젝트로 수동 학습 세션 시작 |
| `notes/concepts/` | 여러 프로젝트에서 공유하는 개념 |
| `notes/projects/<project-id>/` | 실제 코드·업무 규칙·설계 근거 |
| `notes/sessions/<project-id>/` | 실제 질문·답변·평가 (`concepts/`는 공통 학습) |
| `records/notes/<project-id>/` | 재생성 가능한 노트 입력 (`concepts/`는 공통 학습) |
| `records/gates/<project-id>/` | 프로젝트·범위·코드에 묶인 평가·승인 기록 |

원본 프로젝트는 읽기 전용이다. 런처는 `workspace-write` 모드로 학습 폴더에서 시작하며 원본을 추가 쓰기 폴더로 지정하지 않는다. 이해도 통과 후에도 학습 에이전트는 제품을 구현하지 않는다. 개발 전달을 요청한 때만 세 영역 통과와 구체적 범위에 대한 명시적 승인 후 전달서를 작성한다. 기존 개발 에이전트에 학습 게이트를 강제하는 연결은 없다.

공통 개념 학습에는 불필요한 구현 승인을 요구하지 않는다. 공통 원리를 이해했다고 다른 프로젝트의 업무·코드 이해를 통과한 것으로 기록하지 않는다. 사용자 필기는 노트 자동 생성 영역 밖에 두면 재생성 시 보존된다.

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
