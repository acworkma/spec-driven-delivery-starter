#!/usr/bin/env python3
"""Spec gate for spec-driven delivery repositories.

Checks the artifacts under specs/ before they merge, using the rules in
docs/spec-conventions.md.

Usage:
  python tools/spec_lint.py                     # every folder under specs/
  python tools/spec_lint.py specs/001-example   # one or more feature folders
  python tools/spec_lint.py --report report.md  # also write a traceability summary

Exit code 1 when any ERROR is found. Warnings never fail the gate.

Banned terms (customer names, internal code names, people) come from the
SPEC_LINT_BANNED_TERMS environment variable, comma-separated. Keep that list in
a CI secret or variable group, never in the repository.

Runs on Python 3.9+ with the standard library only.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

TEXT_SUFFIXES = {".md", ".markdown", ".yml", ".yaml", ".json", ".txt", ".py",
                 ".ps1", ".sh", ".html", ".htm", ".csv", ".feature"}
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", ".pytest_cache"}

STORY_RE = re.compile(r"^### User Story (\d+)\s*[-\u2013\u2014]\s*(.+?)\s*\(Priority:\s*(P\d+)\)\s*$", re.M)
SCENARIO_RE = re.compile(
    r"^\s*\d+\.\s+\[US(\d+)-AS(\d+)\]\s*(\(exception\))?\s*\*\*Given\*\*.+?\*\*When\*\*.+?\*\*Then\*\*", re.M)
UNTAGGED_SCENARIO_RE = re.compile(r"^\s*\d+\.\s+(\(exception\)\s*)?\*\*Given\*\*", re.M)
FR_DEF_RE = re.compile(r"^\s*-\s+\*\*(FR-\d{3})\*\*\s*:", re.M)
SC_DEF_RE = re.compile(r"^\s*-\s+\*\*(SC-\d{3})\*\*\s*:", re.M)
STATUS_RE = re.compile(r"^\*\*Status\*\*:\s*(.+?)\s*$", re.M)
CLAR_RE = re.compile(r"^\s*-\s+Q:\s*.+?(?:\u2192|->)\s*A:\s*\S", re.M)
TASK_RE = re.compile(r"^\s*-\s+\[( |x|X)\]\s+(T\d{3})\b(.*)$", re.M)
CHECKBOX_RE = re.compile(r"^\s*-\s+\[( |x|X)\]\s+(.*)$", re.M)
FR_REF_RE = re.compile(r"\bFR-\d{3}\b")
SCEN_REF_RE = re.compile(r"\bUS(\d+)-AS(\d+)\b")
STORY_TAG_RE = re.compile(r"\[US(\d+)\]")
SSN_RE = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
TECH_RE = re.compile(
    r"(?<![A-Za-z0-9])(React|Angular|Vue\.js|\.NET|C#|Java|Spring Boot|Node\.js|TypeScript|Python|SQL Server|"
    r"PostgreSQL|Cosmos DB|MongoDB|Kubernetes|AKS|Azure Functions|App Service|Kafka|GraphQL|Redis)(?![A-Za-z0-9])")

REQUIRED_SECTIONS = [
    "## User Scenarios & Testing", "### Edge Cases", "## Requirements",
    "### Functional Requirements", "## Success Criteria", "### Measurable Outcomes", "## Assumptions",
]
STRICT_STATUSES = ("ready for planning", "in build")


@dataclass
class Finding:
    level: str
    path: str
    line: int
    message: str


@dataclass
class FeatureSummary:
    name: str
    status: str = "?"
    stories: int = 0
    scenarios: int = 0
    exceptions: int = 0
    frs: int = 0
    scs: int = 0
    tasks: int = 0
    fr_covered: int = 0
    errors: int = 0
    warnings: int = 0


@dataclass
class Gate:
    root: Path
    findings: list = field(default_factory=list)

    def add(self, level: str, path: Path, line: int, message: str) -> None:
        try:
            rel = path.resolve().relative_to(self.root.resolve()).as_posix()
        except ValueError:
            rel = path.as_posix()
        self.findings.append(Finding(level, rel, line, message))


def strip_fences(text: str) -> str:
    """Blank out fenced code blocks but keep line numbers stable."""
    out, inside = [], False
    for line in text.splitlines(keepends=True):
        if line.lstrip().startswith("```"):
            inside = not inside
            out.append("\n")
            continue
        out.append("\n" if inside else line)
    return "".join(out)


def line_of(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def story_blocks(text: str):
    matches = list(STORY_RE.finditer(text))
    for i, m in enumerate(matches):
        end = len(text)
        nxt = re.compile(r"^#{2,3} ", re.M).search(text, m.end())
        if nxt:
            end = nxt.start()
        if i + 1 < len(matches):
            end = min(end, matches[i + 1].start())
        yield m, text[m.end():end], m.end()


def check_feature(gate: Gate, folder: Path) -> FeatureSummary:
    summary = FeatureSummary(name=folder.name)
    before = len(gate.findings)
    spec_path = folder / "spec.md"
    if not spec_path.exists():
        gate.add("ERROR", spec_path, 1, "spec.md is missing")
        summary.errors = 1
        return summary

    raw = spec_path.read_text(encoding="utf-8")
    text = strip_fences(raw)

    m = STATUS_RE.search(text)
    status = m.group(1).strip() if m else ""
    summary.status = status or "?"
    strict = status.lower().startswith(STRICT_STATUSES)
    if not m:
        gate.add("ERROR", spec_path, 1, "header has no **Status**: line")

    for heading in REQUIRED_SECTIONS:
        if not re.search(rf"^{re.escape(heading)}\b", text, re.M):
            gate.add("ERROR", spec_path, 1, f"missing section '{heading}'")

    # User stories and acceptance scenarios
    story_ids = set()
    scenario_ids = {}
    for sm, block, offset in story_blocks(text):
        n = int(sm.group(1))
        story_line = line_of(text, sm.start())
        if n in story_ids:
            gate.add("ERROR", spec_path, story_line, f"duplicate User Story {n}")
        story_ids.add(n)
        found = list(SCENARIO_RE.finditer(block))
        untagged = list(UNTAGGED_SCENARIO_RE.finditer(block))
        if untagged:
            gate.add("ERROR", spec_path, line_of(text, offset + untagged[0].start()),
                     f"User Story {n}: scenarios need IDs, e.g. '1. [US{n}-AS1] **Given** ...'")
        exceptions = 0
        for sc in found:
            sid = f"US{sc.group(1)}-AS{sc.group(2)}"
            sline = line_of(text, offset + sc.start())
            if int(sc.group(1)) != n:
                gate.add("ERROR", spec_path, sline, f"{sid} sits under User Story {n}")
            if sid in scenario_ids:
                gate.add("ERROR", spec_path, sline, f"duplicate scenario ID {sid}")
            scenario_ids[sid] = sline
            if sc.group(3):
                exceptions += 1
        if len(found) < 2:
            gate.add("ERROR", spec_path, story_line,
                     f"User Story {n}: needs at least two acceptance scenarios (found {len(found)})")
        if exceptions == 0:
            gate.add("ERROR", spec_path, story_line,
                     f"User Story {n}: needs at least one scenario marked (exception)")
        summary.scenarios += len(found)
        summary.exceptions += exceptions
    summary.stories = len(story_ids)
    if not story_ids:
        gate.add("ERROR", spec_path, 1, "no user stories found ('### User Story N - Title (Priority: Pn)')")

    # Requirements and success criteria
    frs = {}
    for fm in FR_DEF_RE.finditer(text):
        fid = fm.group(1)
        if fid in frs:
            gate.add("ERROR", spec_path, line_of(text, fm.start()), f"duplicate requirement {fid}")
        frs[fid] = line_of(text, fm.start())
    scs = {}
    for cm in SC_DEF_RE.finditer(text):
        cid = cm.group(1)
        if cid in scs:
            gate.add("ERROR", spec_path, line_of(text, cm.start()), f"duplicate success criterion {cid}")
        scs[cid] = line_of(text, cm.start())
    summary.frs, summary.scs = len(frs), len(scs)
    if not frs:
        gate.add("ERROR", spec_path, 1, "no functional requirements ('- **FR-001**: ...')")
    if not scs:
        gate.add("ERROR", spec_path, 1, "no success criteria ('- **SC-001**: ...')")

    # Readiness
    for nm in re.finditer(r"\[NEEDS CLARIFICATION", text):
        gate.add("ERROR" if strict else "WARN", spec_path, line_of(text, nm.start()),
                 "open [NEEDS CLARIFICATION] marker" + (" in a spec marked Ready" if strict else ""))
    if strict and not CLAR_RE.search(text):
        gate.add("ERROR", spec_path, 1, "Ready spec has no '## Clarifications' answers ('- Q: ... -> A: ...')")
    checklist = folder / "checklists" / "requirements.md"
    if checklist.exists():
        ctext = strip_fences(checklist.read_text(encoding="utf-8"))
        for cb in CHECKBOX_RE.finditer(ctext):
            if cb.group(1) == " ":
                gate.add("ERROR" if strict else "WARN", checklist, line_of(ctext, cb.start()),
                         f"unchecked quality item: {cb.group(2).strip()[:80]}")
    elif strict:
        gate.add("ERROR", checklist, 1, "Ready spec has no checklists/requirements.md")

    for tm in TECH_RE.finditer(text):
        gate.add("WARN", spec_path, line_of(text, tm.start()),
                 f"'{tm.group(0)}' looks like a technology choice; keep the how in plan.md")

    # Tasks
    tasks_path = folder / "tasks.md"
    if tasks_path.exists():
        ttext = strip_fences(tasks_path.read_text(encoding="utf-8"))
        seen = {}
        referenced_frs, referenced_scen = set(), set()
        for tm in TASK_RE.finditer(ttext):
            tid, body = tm.group(2), tm.group(3)
            tline = line_of(ttext, tm.start())
            if tid in seen:
                gate.add("ERROR", tasks_path, tline, f"duplicate task ID {tid}")
            seen[tid] = tline
            for st in STORY_TAG_RE.finditer(body):
                if int(st.group(1)) not in story_ids:
                    gate.add("ERROR", tasks_path, tline, f"{tid} is tagged US{st.group(1)}, which is not in the spec")
            for fr in FR_REF_RE.findall(body):
                referenced_frs.add(fr)
                if fr not in frs:
                    gate.add("ERROR", tasks_path, tline, f"{tid} references {fr}, which is not in the spec")
            for sr in SCEN_REF_RE.finditer(body):
                sid = f"US{sr.group(1)}-AS{sr.group(2)}"
                referenced_scen.add(sid)
                if sid not in scenario_ids:
                    gate.add("ERROR", tasks_path, tline, f"{tid} references {sid}, which is not in the spec")
        summary.tasks = len(seen)
        for fid, fline in sorted(frs.items()):
            if fid not in referenced_frs:
                gate.add("ERROR", spec_path, fline, f"{fid} is not covered by any task in tasks.md")
        summary.fr_covered = len([f for f in frs if f in referenced_frs])
        for sid, sline in sorted(scenario_ids.items()):
            if sid not in referenced_scen:
                gate.add("WARN", spec_path, sline, f"{sid} is not referenced by any task")

    new = gate.findings[before:]
    summary.errors = sum(1 for f in new if f.level == "ERROR")
    summary.warnings = sum(1 for f in new if f.level == "WARN")
    return summary


def banned_terms() -> list:
    raw = os.environ.get("SPEC_LINT_BANNED_TERMS", "").strip()
    if not raw or raw.startswith("$(") or raw.startswith("${{"):
        return []  # unset, or an Azure Pipelines / Actions macro that did not expand
    return [t.strip() for t in raw.split(",") if t.strip()]


def scan_repository(gate: Gate) -> None:
    terms = banned_terms()
    patterns = [(t, re.compile(rf"(?<![A-Za-z0-9]){re.escape(t)}(?![A-Za-z0-9])", re.I)) for t in terms]
    for path in sorted(gate.root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(gate.root).parts):
            continue
        if path.name == "spec_lint.py":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for sm in SSN_RE.finditer(text):
            gate.add("ERROR", path, line_of(text, sm.start()), "SSN-like number; use synthetic identifiers only")
        for term, pat in patterns:
            for bm in pat.finditer(text):
                gate.add("ERROR", path, line_of(text, bm.start()), "banned term found (see SPEC_LINT_BANNED_TERMS)")


def emit(f: Finding) -> None:
    if os.environ.get("GITHUB_ACTIONS") == "true":
        kind = "error" if f.level == "ERROR" else "warning"
        print(f"::{kind} file={f.path},line={f.line}::{f.message}")
    elif os.environ.get("TF_BUILD"):
        kind = "error" if f.level == "ERROR" else "warning"
        print(f"##vso[task.logissue type={kind};sourcepath={f.path};linenumber={f.line}]{f.message}")
    print(f"{f.level:5} {f.path}:{f.line}  {f.message}")


def write_report(path: Path, summaries: list, findings: list) -> None:
    lines = ["# Spec gate report", "",
             "| Feature | Status | Stories | Scenarios (exceptions) | FRs | SCs | Tasks | FR coverage | Result |",
             "|---|---|---|---|---|---|---|---|---|"]
    for s in summaries:
        cov = f"{s.fr_covered}/{s.frs}" if s.tasks else "n/a"
        result = "FAIL" if s.errors else ("pass with warnings" if s.warnings else "pass")
        lines.append(f"| {s.name} | {s.status} | {s.stories} | {s.scenarios} ({s.exceptions}) | {s.frs} | "
                     f"{s.scs} | {s.tasks or '-'} | {cov} | {result} |")
    errs = [f for f in findings if f.level == "ERROR"]
    if errs:
        lines += ["", "## Errors", ""] + [f"- `{f.path}:{f.line}` {f.message}" for f in errs]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Spec gate for spec-driven delivery repositories")
    ap.add_argument("features", nargs="*", help="feature folders to check (default: every folder in specs/)")
    ap.add_argument("--root", default=".", help="repository root (default: current directory)")
    ap.add_argument("--report", help="write a Markdown traceability summary to this path")
    ap.add_argument("--no-repo-scan", action="store_true", help="skip the repository-wide data and term scan")
    args = ap.parse_args(argv)

    gate = Gate(root=Path(args.root))
    folders = [Path(p) for p in args.features] or sorted(
        p for p in (gate.root / "specs").glob("*") if p.is_dir())
    if not folders:
        print("No feature folders found under specs/.")
    summaries = [check_feature(gate, f) for f in folders]
    if not args.no_repo_scan:
        scan_repository(gate)

    for f in gate.findings:
        emit(f)
    errors = sum(1 for f in gate.findings if f.level == "ERROR")
    warns = sum(1 for f in gate.findings if f.level == "WARN")
    for s in summaries:
        cov = f", FR coverage {s.fr_covered}/{s.frs}" if s.tasks else ""
        print(f"{s.name}: {s.status}; {s.stories} stories, {s.scenarios} scenarios "
              f"({s.exceptions} exception), {s.frs} FRs, {s.scs} SCs{cov}")
    print(f"Spec gate: {errors} error(s), {warns} warning(s)")
    if args.report:
        write_report(Path(args.report), summaries, gate.findings)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
