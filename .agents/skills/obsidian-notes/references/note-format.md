# 노트 생성 입력

Python 3 표준 라이브러리 도구로 JSON 입력을 받아 `notes/projects/<project-id>/<slug>.md` 또는 `notes/concepts/<slug>.md`를 생성한다. 기본 작업공간은 스크립트가 속한 `agent-learning`이다. 검증용 `--workspace`는 분리된 임시 디렉터리에만 사용한다.

필수 필드:

| 필드 | 의미 |
| --- | --- |
| `kind` | 실제 적용은 `project`, 공통 개념은 `concept` |
| `project_id` | `projects.json`에 등록한 ID. 공통 개념이면 `null` |
| `slug` | 영문 소문자·숫자·하이픈으로 된 주제 ID |
| `title` | 노트 제목 |
| `summary` | 한 문장 설명 |
| `why` | 필요성과 문제 상황 |
| `business_rules` | 실제 업무 규칙 문자열 배열 |
| `flow` | 요청·처리·저장 흐름 Markdown. Mermaid도 가능 |
| `design_reasoning` | 출처가 있는 설계 이유와 별도로 표시한 해석 |
| `questions` | 복습 질문 배열 |
| `sources` | `path`(원본 기준 상대 경로), `symbol`(선택), `purpose`(이 근거로 확인한 내용), `role`(`code`, `design`, `business`) 객체 배열 |

프로젝트 노트는 `role: code` 근거를 최소 1개 포함한다. Python·Go·Rust·Java 등 언어를 확장자로 제한하지 않고 실제 UTF-8 파일을 읽는다. 관련 설계·명세 문서가 있으면 함께 넣고 없으면 `design_reasoning`에 문서 부재와 해석을 명시한다. 업무가 적용되지 않으면 `business_rules`에 이유를 적는다. 공통 개념은 `project_id: null`, `sources: []`이며 확인한 공식 출처·프로젝트 노트 링크를 본문 필드에 넣는다. 공통 노트가 특정 프로젝트 이해도 통과를 뜻하지 않는다. 소스 파일과 심볼은 존재해야 한다. 심볼 위치는 문자열 첫 출현 기준의 탐색 힌트이며 정적 분석으로 증명한 호출 관계가 아니다. 현재 프로젝트 ID·절대 경로·파일 SHA-256과 Git HEAD는 도구가 읽어서 기록한다. Git HEAD만으로 커밋되지 않은 소스까지 동일하다고 판단하지 않는다.

도구는 YAML 속성·본문·근거 표를 만들고 본문에서 `<!-- learning:auto:start -->`와 `<!-- learning:auto:end -->` 사이만 자동 갱신한다. 그 밖의 사용자 필기·속성은 유지한다. 자동 영역 안에 직접 쓴 필기는 다음 생성 때 바뀌므로 자신의 설명은 영역 밖에 기록한다.

처음 생성할 때 학습 상태는 `learning`이다. 입력으로 임의의 통과·승인 상태를 전달할 수 없다. 멘토가 검증된 대화 근거와 세션을 연결해 학습 상태를 갱신한다. 개발 승인은 별도의 gate 기록을 사용한다.

`check`는 생성 노트의 파일·심볼·지문을 재검증한다. 소스 변경은 실패로 보고하여 재검토를 유도한다. 내용의 사실성, Mermaid 렌더링, 사용자 이해도는 이 도구의 자동 검증 범위가 아니다.
