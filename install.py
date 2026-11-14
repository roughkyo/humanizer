#!/usr/bin/env python3
"""humanize-kr installer — 정본 폴더의 스킬을 Claude Code·Codex·Antigravity 설치 위치로 복사한다.

사용법 (이 파일이 있는 폴더에서):
    python install.py                 # 세 위치 모두 설치(기존 설치는 백업 후 교체)
    python install.py --dry-run       # 무엇을 할지 출력만
    python install.py --check         # 설치된 버전만 비교
    python install.py --only claude agents
    python install.py --zip           # claude.ai 스킬 업로드용 zip 만들기(dist/)

설치 위치
    claude       ~/.claude/skills/humanize-kr          Claude Code (CLI·데스크탑 Code 탭)
    agents       ~/.agents/skills/humanize-kr          Codex, Antigravity(공용 스킬 경로)
    antigravity  ~/.gemini/config/skills/humanize-kr   Antigravity 전역 스킬

기존 설치는 ~/.humanize-kr-backups/<위치>-<시각>/ 으로 옮긴다. 스킬 폴더 안에 백업을 두지 않는다
(스킬 폴더 안의 백업은 같은 이름의 스킬로 중복 인식될 수 있다).
표준 라이브러리만 쓴다.
"""
from __future__ import annotations

import argparse
import datetime
import os
import re
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKILL = ROOT / "humanize-kr"
HOME = Path.home()
TARGETS = {
    "claude": HOME / ".claude" / "skills" / "humanize-kr",
    "agents": HOME / ".agents" / "skills" / "humanize-kr",
    "antigravity": HOME / ".gemini" / "config" / "skills" / "humanize-kr",
}
BACKUP_ROOT = HOME / ".humanize-kr-backups"
IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store")


def version_of(skill_md: Path) -> str:
    if not skill_md.is_file():
        return "-"
    m = re.search(r"\(v(\d+(?:\.\d+)*)\)", skill_md.read_text(encoding="utf-8", errors="replace"))
    return m.group(1) if m else "?"


def install(name: str, dst: Path, stamp: str, dry: bool) -> None:
    src_ver, dst_ver = version_of(SKILL / "SKILL.md"), version_of(dst / "SKILL.md")
    print(f"[{name}] {dst}  설치본 v{dst_ver} → 정본 v{src_ver}")
    if os.path.isjunction(dst) or dst.is_symlink():
        print("  연결(junction)로 정본을 가리키고 있어 복사가 필요 없음 — 건너뜀")
        return
    if dry:
        return
    if dst.exists():
        backup = BACKUP_ROOT / f"{name}-{stamp}"
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(dst), str(backup))
        print(f"  백업: {backup}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SKILL, dst, ignore=IGNORE)
    print(f"  설치 완료 (v{version_of(dst / 'SKILL.md')})")


def build_zip() -> Path:
    ver = version_of(SKILL / "SKILL.md")
    out = ROOT / "dist" / f"humanize-kr-v{ver}.zip"
    out.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(SKILL.rglob("*")):
            if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc":
                z.write(p, Path("humanize-kr") / p.relative_to(SKILL))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="humanize-kr 설치")
    ap.add_argument("--only", nargs="+", choices=sorted(TARGETS), help="설치할 위치만 지정")
    ap.add_argument("--dry-run", action="store_true", help="출력만 하고 복사하지 않음")
    ap.add_argument("--check", action="store_true", help="설치된 버전만 비교")
    ap.add_argument("--zip", action="store_true", help="claude.ai 업로드용 zip 생성")
    a = ap.parse_args()

    if not (SKILL / "SKILL.md").is_file():
        print(f"정본 스킬 폴더를 찾지 못했다: {SKILL}", file=sys.stderr)
        return 2
    if a.zip:
        print(f"zip: {build_zip()}")
        return 0

    names = a.only or list(TARGETS)
    if a.check:
        src = version_of(SKILL / "SKILL.md")
        for n in names:
            v = version_of(TARGETS[n] / "SKILL.md")
            print(f"[{n}] v{v} {'= 최신' if v == src else f'(정본 v{src})'}  {TARGETS[n]}")
        return 0

    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    for n in names:
        install(n, TARGETS[n], stamp, a.dry_run)
    if not a.dry_run:
        print("\n새 세션(또는 앱 재시작)부터 적용된다.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
