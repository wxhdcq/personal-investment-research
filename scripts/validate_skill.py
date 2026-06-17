#!/usr/bin/env python3
"""Validate the personal-investment-research Codex Skill package."""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_NAME = "personal-investment-research"


class Reporter:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.passes: list[str] = []

    def pass_(self, message: str) -> None:
        self.passes.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def fail(self, message: str) -> None:
        self.errors.append(message)

    def emit(self) -> int:
        for message in self.passes:
            print(f"PASS {message}")
        for message in self.warnings:
            print(f"WARN {message}")
        for message in self.errors:
            print(f"FAIL {message}")

        print(
            f"SUMMARY PASS={len(self.passes)} "
            f"WARN={len(self.warnings)} FAIL={len(self.errors)}"
        )
        return 1 if self.errors else 0


def load_yaml(text: str):
    try:
        import yaml  # type: ignore
    except Exception:
        return None
    return yaml.safe_load(text)


def parse_frontmatter(text: str, reporter: Reporter) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        reporter.fail("SKILL.md front matter must start with --- on its own line")
        return {}

    end_index = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_index = index
            break

    if end_index is None:
        reporter.fail("SKILL.md front matter must end with --- on its own line")
        return {}

    raw = "\n".join(lines[1:end_index])
    parsed = load_yaml(raw)
    if isinstance(parsed, dict):
        reporter.pass_("SKILL.md front matter parsed with PyYAML")
        return {str(key): "" if value is None else str(value) for key, value in parsed.items()}

    reporter.warn("PyYAML unavailable; using lightweight front matter parser")
    data: dict[str, str] = {}
    current_key: str | None = None
    block_lines: list[str] = []

    for line in raw.splitlines():
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if match:
            if current_key:
                data[current_key] = " ".join(part.strip() for part in block_lines).strip()
            key, value = match.groups()
            if value in {">-", "|", ">"}:
                current_key = key
                block_lines = []
            else:
                data[key] = value.strip().strip('"')
                current_key = None
                block_lines = []
        elif current_key and (line.startswith(" ") or line.startswith("\t")):
            block_lines.append(line)

    if current_key:
        data[current_key] = " ".join(part.strip() for part in block_lines).strip()

    if data:
        reporter.pass_("SKILL.md front matter parsed with lightweight parser")
    else:
        reporter.fail("SKILL.md front matter could not be parsed")
    return data


def validate_skill_md(reporter: Reporter) -> None:
    path = ROOT / "SKILL.md"
    if not path.exists():
        reporter.fail("SKILL.md is missing")
        return

    reporter.pass_("SKILL.md exists")
    text = path.read_text(encoding="utf-8")
    meta = parse_frontmatter(text, reporter)

    name = meta.get("name", "").strip()
    description = meta.get("description", "").strip()

    if not name:
        reporter.fail("SKILL.md front matter missing name")
    elif name != EXPECTED_NAME:
        reporter.fail(f"SKILL.md name must be {EXPECTED_NAME}, got {name}")
    else:
        reporter.pass_("SKILL.md name is correct")

    if not description:
        reporter.fail("SKILL.md front matter missing description")
    else:
        reporter.pass_("SKILL.md description exists")
        if len(description) > 800:
            reporter.warn(f"SKILL.md description is long ({len(description)} characters)")


def validate_openai_yaml(reporter: Reporter) -> None:
    path = ROOT / "agents" / "openai.yaml"
    if not path.exists():
        reporter.warn("agents/openai.yaml is missing")
        return

    text = path.read_text(encoding="utf-8")
    parsed = load_yaml(text)
    if isinstance(parsed, dict):
        reporter.pass_("agents/openai.yaml parsed with PyYAML")
        return

    reporter.warn("PyYAML unavailable; using lightweight agents/openai.yaml checks")
    required_patterns = [
        r"^interface:\s*$",
        r'^\s+display_name:\s+".+"\s*$',
        r'^\s+short_description:\s+".+"\s*$',
        r'^\s+brand_color:\s+"#[0-9A-Fa-f]{6}"\s*$',
        r'^\s+default_prompt:\s+".+"\s*$',
        r"^policy:\s*$",
        r"^\s+allow_implicit_invocation:\s+(true|false)\s*$",
    ]
    for pattern in required_patterns:
        if not re.search(pattern, text, flags=re.MULTILINE):
            reporter.fail(f"agents/openai.yaml missing pattern: {pattern}")
            return
    reporter.pass_("agents/openai.yaml passed lightweight checks")


def validate_prompts_csv(reporter: Reporter) -> None:
    path = ROOT / "evals" / "prompts.csv"
    if not path.exists():
        reporter.fail("evals/prompts.csv is missing")
        return

    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
    except Exception as exc:
        reporter.fail(f"evals/prompts.csv could not be read: {exc}")
        return

    expected_fields = [
        "id",
        "should_trigger",
        "prompt",
        "expected_behavior",
        "key_checks",
    ]
    if reader.fieldnames != expected_fields:
        reporter.fail(f"evals/prompts.csv headers must be {expected_fields}")
    else:
        reporter.pass_("evals/prompts.csv headers are correct")

    if len(rows) < 10:
        reporter.fail(f"evals/prompts.csv must contain at least 10 cases, found {len(rows)}")
    else:
        reporter.pass_(f"evals/prompts.csv contains {len(rows)} cases")

    values = {str(row.get("should_trigger", "")).strip().lower() for row in rows}
    if not {"true", "false"}.issubset(values):
        reporter.fail("evals/prompts.csv must include both should_trigger=true and false")
    else:
        reporter.pass_("evals/prompts.csv includes true and false cases")


def scan_markdown_lines(reporter: Reporter) -> None:
    found_warning = False
    for path in sorted(ROOT.rglob("*.md")):
        if ".git" in path.parts:
            continue
        rel = path.relative_to(ROOT)
        for index, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if len(line) > 2000:
                reporter.warn(f"{rel}:{index} line exceeds 2000 characters")
                found_warning = True
    if not found_warning:
        reporter.pass_("No Markdown line exceeds 2000 characters")


def main() -> int:
    reporter = Reporter()
    validate_skill_md(reporter)
    validate_openai_yaml(reporter)
    validate_prompts_csv(reporter)
    scan_markdown_lines(reporter)
    return reporter.emit()


if __name__ == "__main__":
    raise SystemExit(main())
