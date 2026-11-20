#!/usr/bin/env python3
"""Turn a feature's tasks.md into GitHub issues or Azure Boards work items.

Dry run by default: prints the commands it would run and creates nothing.
Add --execute to run them with an authenticated `gh` or `az` CLI; it asks for
confirmation unless you also pass --yes.

  python tools/tasks_export.py specs/001-member-claim-status --target github --repo OWNER/REPO
  python tools/tasks_export.py specs/001-member-claim-status --target ado \
      --org https://dev.azure.com/ORG --project PROJECT [--story-type "Product Backlog Item"]

One parent item per user story (plus one for setup and cross-cutting tasks),
one child item per T### task. Each item carries the spec path, the task's FR and
scenario IDs, and tags/labels for the feature and story. After a real run, the
created IDs are saved to <feature>/.export-<target>.json and a second run is
refused unless --force is given, so you don't create duplicates.

Standard library only; Python 3.9+.
"""
from __future__ import annotations

import argparse
import json
import re
import shlex
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

STORY_RE = re.compile(r"^### User Story (\d+)\s*[-\u2013\u2014]\s*(.+?)\s*\(Priority:\s*(P\d+)\)\s*$", re.M)
SCENARIO_RE = re.compile(r"^\s*\d+\.\s+\[US(\d+)-AS(\d+)\]\s*(\(exception\))?\s*(.+)$", re.M)
TASK_RE = re.compile(r"^\s*-\s+\[( |x|X)\]\s+(T\d{3})\b(.*)$", re.M)
PHASE_RE = re.compile(r"^##\s+(Phase\s+\d+.*)$", re.M)
FR_RE = re.compile(r"\bFR-\d{3}\b")
SCEN_RE = re.compile(r"\bUS\d+-AS\d+\b")
STORY_TAG_RE = re.compile(r"\[US(\d+)\]")


@dataclass
class Task:
    tid: str
    done: bool
    parallel: bool
    story: int | None
    text: str
    phase: str
    frs: list = field(default_factory=list)
    scenarios: list = field(default_factory=list)


def parse(feature: Path):
    spec = (feature / "spec.md").read_text(encoding="utf-8")
    stories = {int(m.group(1)): (m.group(2).strip(), m.group(3)) for m in STORY_RE.finditer(spec)}
    scenarios = {}
    for m in SCENARIO_RE.finditer(spec):
        scenarios.setdefault(int(m.group(1)), []).append(
            f"US{m.group(1)}-AS{m.group(2)}{' (exception)' if m.group(3) else ''}: {m.group(4).strip()}")
    tasks_text = (feature / "tasks.md").read_text(encoding="utf-8")
    phases = [(m.start(), m.group(1).strip()) for m in PHASE_RE.finditer(tasks_text)]
    tasks = []
    for m in TASK_RE.finditer(tasks_text):
        phase = next((name for pos, name in reversed(phases) if pos < m.start()), "Tasks")
        body = m.group(3)
        tag = STORY_TAG_RE.search(body)
        clean = re.sub(r"\[(P|US\d+)\]\s*", "", body).strip()
        tasks.append(Task(
            tid=m.group(2), done=m.group(1).lower() == "x", parallel="[P]" in body,
            story=int(tag.group(1)) if tag else None, text=clean, phase=phase,
            frs=sorted(set(FR_RE.findall(body))), scenarios=sorted(set(SCEN_RE.findall(body)))))
    return stories, scenarios, tasks


def short(text: str, limit: int = 90) -> str:
    text = re.sub(r"\s*\((?:FR|US)\S.*\)\s*$", "", text)
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "\u2026"


def task_body(feature: Path, t: Task) -> str:
    lines = [f"Spec: `{feature.as_posix()}/spec.md`", f"Task {t.tid} from `{feature.as_posix()}/tasks.md` ({t.phase})", "",
             t.text, ""]
    if t.frs:
        lines.append("Requirements: " + ", ".join(t.frs))
    if t.scenarios:
        lines.append("Scenarios: " + ", ".join(t.scenarios))
    if t.parallel:
        lines.append("Can run in parallel with other [P] tasks in this phase.")
    return "\n".join(lines)


def parent_body(feature: Path, number, title, scenario_lines) -> str:
    lines = [f"Spec: `{feature.as_posix()}/spec.md`", ""]
    if number is None:
        lines.append("Setup, foundational and cross-cutting tasks for this feature.")
    else:
        lines.append(f"User Story {number}: {title}")
        if scenario_lines:
            lines += ["", "Acceptance scenarios:"] + [f"- {s}" for s in scenario_lines]
    return "\n".join(lines)


class Runner:
    def __init__(self, execute: bool):
        self.execute = execute

    def run(self, cmd: list) -> str:
        print("$ " + shlex.join(cmd))
        if not self.execute:
            return ""
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            sys.exit(f"Command failed ({result.returncode}): {result.stderr.strip()}")
        return result.stdout.strip()


def write_temp(text: str) -> str:
    f = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8")
    f.write(text)
    f.close()
    return f.name


def export_github(args, feature, stories, scenarios, tasks, runner):
    created = {}
    feat_label = f"spec:{feature.name}"
    for label in [feat_label, "user-story", "task"] + [f"US{n}" for n in stories]:
        runner.run(["gh", "label", "create", label, "--repo", args.repo, "--force"])
    groups = {}
    for t in tasks:
        groups.setdefault(t.story, []).append(t)
    for story in sorted(groups, key=lambda s: (s is not None, s or 0)):
        if story is None:
            title = f"{feature.name}: setup and cross-cutting"
            labels = [feat_label]
        else:
            name, prio = stories.get(story, (f"User Story {story}", ""))
            title = f"US{story}: {name}" + (f" ({prio})" if prio else "")
            labels = [feat_label, "user-story", f"US{story}"]
        body = parent_body(feature, story, stories.get(story, ("", ""))[0], scenarios.get(story, []))
        cmd = ["gh", "issue", "create", "--repo", args.repo, "--title", title, "--body-file", write_temp(body)]
        for lb in labels:
            cmd += ["--label", lb]
        url = runner.run(cmd)
        parent = url.rsplit("/", 1)[-1] if url else f"<{'US' + str(story) if story else 'setup'}-issue>"
        created[title] = parent
        checklist = []
        for t in groups[story]:
            tb = task_body(feature, t) + f"\n\nParent: #{parent}"
            tcmd = ["gh", "issue", "create", "--repo", args.repo, "--title", f"{t.tid} {short(t.text)}",
                    "--body-file", write_temp(tb), "--label", feat_label, "--label", "task"]
            if story is not None:
                tcmd += ["--label", f"US{story}"]
            turl = runner.run(tcmd)
            num = turl.rsplit("/", 1)[-1] if turl else f"<{t.tid}-issue>"
            created[t.tid] = num
            checklist.append(f"- [ ] #{num} {t.tid}")
        runner.run(["gh", "issue", "edit", parent, "--repo", args.repo, "--body-file",
                    write_temp(body + "\n\nTasks:\n" + "\n".join(checklist))])
    return created


def export_ado(args, feature, stories, scenarios, tasks, runner):
    created = {}
    base = ["--org", args.org, "--project", args.project, "--output", "json"]
    extra = []
    if args.area:
        extra += ["--area", args.area]
    if args.iteration:
        extra += ["--iteration", args.iteration]
    groups = {}
    for t in tasks:
        groups.setdefault(t.story, []).append(t)
    for story in sorted(groups, key=lambda s: (s is not None, s or 0)):
        if story is None:
            title, tags = f"{feature.name}: setup and cross-cutting", f"spec-{feature.name}"
        else:
            name, prio = stories.get(story, (f"User Story {story}", ""))
            title, tags = f"US{story}: {name}" + (f" ({prio})" if prio else ""), f"spec-{feature.name}; US{story}"
        desc = parent_body(feature, story, stories.get(story, ("", ""))[0], scenarios.get(story, []))
        out = runner.run(["az", "boards", "work-item", "create", "--type", args.story_type, "--title", title,
                          "--description", desc.replace("\n", "<br>"), "--fields", f"System.Tags={tags}"]
                         + extra + base)
        parent = str(json.loads(out)["id"]) if out else f"<US{story or 0}-id>"
        created[title] = parent
        for t in groups[story]:
            ttags = f"{tags}; {t.tid}"
            tout = runner.run(["az", "boards", "work-item", "create", "--type", "Task",
                               "--title", f"{t.tid} {short(t.text)}",
                               "--description", task_body(feature, t).replace("\n", "<br>"),
                               "--fields", f"System.Tags={ttags}"] + extra + base)
            tid = str(json.loads(tout)["id"]) if tout else f"<{t.tid}-id>"
            created[t.tid] = tid
            runner.run(["az", "boards", "work-item", "relation", "add", "--id", tid, "--relation-type", "parent",
                        "--target-id", parent, "--org", args.org, "--output", "json"])
    return created


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Export tasks.md to GitHub issues or Azure Boards work items")
    ap.add_argument("feature", help="feature folder, e.g. specs/001-member-claim-status")
    ap.add_argument("--target", choices=["github", "ado"], required=True)
    ap.add_argument("--repo", help="GitHub OWNER/REPO (target github)")
    ap.add_argument("--org", help="Azure DevOps organization URL (target ado)")
    ap.add_argument("--project", help="Azure DevOps project (target ado)")
    ap.add_argument("--story-type", default="User Story",
                    help='parent work item type: "User Story" (Agile), "Product Backlog Item" (Scrum), '
                         '"Requirement" (CMMI) or "Issue" (Basic)')
    ap.add_argument("--area", help="Azure Boards area path")
    ap.add_argument("--iteration", help="Azure Boards iteration path")
    ap.add_argument("--include-done", action="store_true", help="also export tasks already checked off")
    ap.add_argument("--execute", action="store_true", help="actually create the items (default is a dry run)")
    ap.add_argument("--yes", action="store_true", help="skip the confirmation prompt with --execute")
    ap.add_argument("--force", action="store_true", help="export again even if a previous export is recorded")
    args = ap.parse_args(argv)

    feature = Path(args.feature)
    if args.target == "github" and not args.repo:
        ap.error("--repo OWNER/REPO is required for --target github")
    if args.target == "ado" and not (args.org and args.project):
        ap.error("--org and --project are required for --target ado")
    for needed in ("spec.md", "tasks.md"):
        if not (feature / needed).exists():
            ap.error(f"{feature / needed} not found")

    stories, scenarios, tasks = parse(feature)
    if not args.include_done:
        tasks = [t for t in tasks if not t.done]
    if not tasks:
        print("No open tasks to export.")
        return 0

    record = feature / f".export-{args.target}.json"
    if args.execute and record.exists() and not args.force:
        sys.exit(f"{record} shows this feature was already exported. Use --force to export again.")
    parents = len({t.story for t in tasks})
    print(f"{'EXECUTE' if args.execute else 'DRY RUN'}: {len(tasks)} tasks under {parents} parent items "
          f"for {feature.name} -> {args.target}\n")
    if args.execute and not args.yes:
        if input("Create these items now? [y/N] ").strip().lower() != "y":
            print("Cancelled.")
            return 1

    runner = Runner(args.execute)
    exporter = export_github if args.target == "github" else export_ado
    created = exporter(args, feature, stories, scenarios, tasks, runner)
    if args.execute:
        record.write_text(json.dumps(created, indent=2), encoding="utf-8")
        print(f"\nCreated {len(created)} items. Recorded in {record}.")
    else:
        print("\nDry run only. Add --execute to create these items.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
