#!/usr/bin/env python3
"""Validate Agent Skills structure and minimum publication metadata."""
from pathlib import Path
import re
import yaml

root = Path(__file__).resolve().parents[1]
entry = (root / "SKILL.md").read_text(encoding="utf-8")
match = re.match(r"\A---\s*\n(.*?)\n---\s*\n(.*)", entry, re.S)
assert match, "Missing YAML frontmatter"
meta = yaml.safe_load(match.group(1))
assert meta["name"] == root.name
assert re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", meta["name"])
assert 0 < len(meta["description"]) <= 1024
for phrase in ("先解原题", "独立验算", "同构训练", "巧思强化", "命题预测", "给我提示", "批改我的解答"):
    assert phrase in entry, phrase
for path in ("agents/openai.yaml", "README.md", "references/quality-rubric.md",
             "references/domain-checks.md", "references/input-and-style.md",
             "assets/private-solution-checklist.md", "scripts/verify_cases.py", "tests/casebook.md",
             "scripts/organize_questions.py", "references/question-organization.md"):
    assert (root / path).is_file(), path
assert yaml.safe_load((root / "agents/openai.yaml").read_text(encoding="utf-8"))["interface"]["display_name"] == "ZJU-845-Creator"
print("PASS Skill frontmatter, trigger instructions and directory structure")
