#!/usr/bin/env python3
"""Validate every skills/*/SKILL.md frontmatter.

The skills.sh indexer parses each SKILL.md's YAML frontmatter. A malformed
block (e.g. a bare ": " inside an unquoted description) raises a YAML
ScannerError and the indexer *silently skips the skill* — which is how the
finish-task skill once failed to install. This lint reproduces that parse
so the failure surfaces in CI instead of at install time.

Checks, per skills/*/SKILL.md:
  1. file opens with a `---` frontmatter delimiter and has a closing `---`;
  2. the frontmatter parses as YAML (the exact thing the indexer does);
  3. it is a mapping with non-empty string `name` and `description`;
  4. `name` matches the skill's directory name.

Exits non-zero if any file fails. Requires PyYAML.
"""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ModuleNotFoundError:
    sys.exit("error: PyYAML is required (pip install pyyaml)")

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
DELIMITER = "---"


def extract_frontmatter(text: str) -> str:
    """Return the YAML between the opening and closing `---`, or raise ValueError."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != DELIMITER:
        raise ValueError("file does not start with a `---` frontmatter delimiter")
    for end, line in enumerate(lines[1:], start=1):
        if line.strip() == DELIMITER:
            return "\n".join(lines[1:end])
    raise ValueError("frontmatter is not closed with a `---` delimiter")


def check(skill_md: Path) -> list[str]:
    """Return a list of error strings for one SKILL.md (empty == OK)."""
    errors: list[str] = []
    try:
        block = extract_frontmatter(skill_md.read_text(encoding="utf-8"))
    except ValueError as exc:
        return [str(exc)]

    try:
        data = yaml.safe_load(block)
    except yaml.YAMLError as exc:
        # This is the failure mode the indexer hits — report it verbatim.
        return [f"frontmatter is not valid YAML: {exc}"]

    if not isinstance(data, dict):
        return [f"frontmatter is not a YAML mapping (got {type(data).__name__})"]

    for key in ("name", "description"):
        value = data.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"missing or empty `{key}`")

    name = data.get("name")
    expected = skill_md.parent.name
    if isinstance(name, str) and name.strip() and name != expected:
        errors.append(f"`name` ({name!r}) does not match directory ({expected!r})")

    return errors


def main() -> int:
    skill_files = sorted(SKILLS_DIR.glob("*/SKILL.md"))
    if not skill_files:
        print(f"no SKILL.md files found under {SKILLS_DIR}", file=sys.stderr)
        return 1

    failed = 0
    for skill_md in skill_files:
        rel = skill_md.relative_to(REPO_ROOT)
        errors = check(skill_md)
        if errors:
            failed += 1
            print(f"FAIL  {rel}")
            for err in errors:
                print(f"      - {err}")
        else:
            print(f"ok    {rel}")

    print()
    if failed:
        print(f"{failed} of {len(skill_files)} SKILL.md file(s) failed validation")
        return 1
    print(f"all {len(skill_files)} SKILL.md file(s) valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
