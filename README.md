# humanizer (humanize-kr) — 한국어 AI 티 제거 윤문 스킬 (v3.0)

한국어 글에서 AI가 쓴 티를 지우는 윤문 스킬입니다. 글의 성격에 맞춰 **세 가지 모드(레지스터)** 로 고칩니다.
Claude Code·Codex·Google Antigravity에서 같은 스킬로 씁니다.

| 모드 | 이런 글에 | 특징 |
|---|---|---|
| **일반** | 칼럼·에세이·블로그·논설 산문 | 현학적인 한자 추상어·설명 없는 은유·감동 마무리를 걷어냄 |
| **techdoc** | 수업 슬라이드 원고·실습 지도안·매뉴얼·기술 문서 | 전문 용어를 지키고, 개조식 끝맺음(~함/~임)·상투 비유 금지 |
| **공문** (v3.0 신규) | 공문·기안문·보고서·계획서·결과/성과보고서·회의자료 | **한 항목 120자 초과**와 **개조식 항목의 '-다/-습니다' 종결**을 반드시 고침 |

작업량은 따로 고릅니다: **가볍게(light)** · **기본(standard)** · **정밀(heavy)**. 말하지 않으면 글을 분석해 자동으로 정합니다.

## 설치

Python 3.10 이상이 필요합니다(표준 라이브러리만 사용).

```bash
git clone https://github.com/roughkyo/humanizer.git
cd humanizer
python install.py
```

`install.py`는 아래 세 위치에 스킬을 복사합니다. 이미 설치된 것이 있으면 `~/.humanize-kr-backups/`로 옮겨 둔 뒤 교체합니다.

| 위치 | 쓰는 도구 |
|---|---|
| `~/.claude/skills/humanize-kr` | Claude Code (CLI, 데스크탑 앱 Code 탭) |
| `~/.agents/skills/humanize-kr` | Codex, Antigravity |
| `~/.gemini/config/skills/humanize-kr` | Antigravity |

- 미리 보기만: `python install.py --dry-run`
- 설치된 버전 확인: `python install.py --check`
- 일부만 설치: `python install.py --only claude agents`
- claude.ai(웹·데스크탑 채팅)에 올릴 zip: `python install.py --zip` → `dist/humanize-kr-v3.0.zip`을 claude.ai의 스킬 설정에서 업로드

설치 후 **새 세션(또는 앱 재시작)** 부터 적용됩니다.

## 사용법

채팅에 자연어로 요청합니다.

```text
이 글 윤문해줘
이 성과보고서 공문 형식으로 윤문해줘
수업 슬라이드 원고야, 정밀하게 윤문해줘
이 보고서 고치지 말고 검토만 해줘
```

- 모드를 직접 정하려면: `레지스터: 공문` / `레지스터: 기술문서` / `레지스터: 일반`
- 작업량을 정하려면: "가볍게", "정밀하게"
- 결과는 작업 폴더의 `_workspace/<날짜-번호>/final.md`에 저장됩니다. 원본 파일은 고치지 않습니다.

### 공문 모드가 하는 일

1. 원문을 검사기(`scripts/check_gongmun.py`)로 먼저 훑어 120자 넘는 항목과 '-다/-습니다'로 끝나는 항목을 찾습니다.
2. 윤문하면서 긴 항목을 연도별·기능별 하위 항목으로 나누고, 말끝을 ~함·~임·명사형으로 맞춥니다.
3. 결과를 다시 검사해 남은 것이 있으면 그 자리만 한 번 더 고칩니다.
4. 수치·고유명사·인용·표·URL·날짜 표기는 바꾸지 않습니다. 규범과 다른 표기는 '작성자 확인'으로 알려만 줍니다.

검사기만 따로 돌릴 수도 있습니다.

```bash
python -X utf8 humanize-kr/scripts/check_gongmun.py 내문서.md
```

## 유의점

- **원문을 미리 다듬지 말고** 그대로 넣으세요. 스킬이 고칠 거리를 찾지 못합니다.
- 공문 모드는 문장을 나누기 때문에 원문의 5~25%가 바뀌는 것이 정상입니다. 나눈 뒤 **역접·조건('~하되', '다만')이나 따옴표 안 글자가 빠지지 않았는지** 꼭 확인하세요.
- 학생 실명·연락처 같은 개인정보는 지우고 넣으세요. 원고는 AI 서비스로 전송됩니다.
- 작업 폴더에 생기는 `_workspace/`에는 원고 원문이 들어 있습니다. 저장소에 올리지 마세요.
- Codex·Antigravity처럼 서브에이전트 도구가 없는 환경에서는 같은 단계를 한 대화 안에서 차례로 진행합니다. 결과는 같고 시간이 조금 더 걸릴 수 있습니다.

## 폴더 구조

| 경로 | 내용 |
|---|---|
| `humanize-kr/SKILL.md` | 스킬 본체(모드·경로·절차) |
| `humanize-kr/agents/` | 진단·윤문·마무리 점검 담당 지침 |
| `humanize-kr/references/` | 룰북, 공문 가이드(`gongmun-guide.md`) |
| `humanize-kr/scripts/` | 사전 점수, 변경률 게이트, 공문 검사기 |
| `install.py` | 세 도구 설치 스크립트 |

## 출처와 라이선스

- 원작: [im-not-ai / humanize-korean](https://github.com/epoko77-ai/im-not-ai) (epoko77-ai, MIT)
- 공문 모드: [slop-rewrite](https://github.com/byungjunjang/slop-rewrite)의 개조식 보고서 가이드·검사기 (Byungjun Jang, MIT)
- 자세한 고지: [`humanize-kr/THIRD_PARTY_NOTICES.md`](humanize-kr/THIRD_PARTY_NOTICES.md)

© Made By [Yangphago](https://yangphago.oopy.io/)
