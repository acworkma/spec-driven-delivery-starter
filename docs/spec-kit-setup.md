# Spec Kit setup

This starter was built against **Spec Kit v1.4.2** (November 2026). Spec Kit releases often, so pin a version and upgrade deliberately.

## You may not need to install anything

The worked examples, skills, templates and spec gate in this repository work in VS Code with GitHub Copilot as they are. Install Spec Kit when you want its `/speckit-*` commands in your own repository.

## Install, pinned

Spec Kit needs Python 3.11+, [uv](https://docs.astral.sh/uv/), and an AI coding agent such as GitHub Copilot.

```bash
# Install the CLI at a pinned version
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v1.4.2

# Or run it once without installing
uvx --from git+https://github.com/github/spec-kit.git@v1.4.2 specify init --here --integration copilot --script sh
```

- **Windows:** use `--script ps` for the PowerShell helper scripts.
- **No internet access:** Spec Kit's docs describe installing from a locally built wheel.

## What `specify init` adds for Copilot

- **Skills.** `.github/skills/speckit-<command>/SKILL.md`, used in chat as `/speckit-constitution`, `/speckit-specify`, `/speckit-clarify`, `/speckit-plan`, `/speckit-checklist`, `/speckit-tasks`, `/speckit-analyze`, `/speckit-implement` and `/speckit-converge`.
- **The `.specify/` folder:**
  - `memory/constitution.md`
  - `templates/`, where local changes go under `templates/overrides/`
  - helper `scripts/`
- **Older command and prompt files** are installed only with `--integration-options="--commands"`. VS Code runs prompt files only in its deprecated Local harness.

**Existing repository:** run `init` with `--here` on a clean branch, and review the diff before committing. Use `--force` only if you mean to replace files at conflicting paths.

**Watch the agent context file.** Spec Kit's planning step can add technology notes to the agent context file, `.github/copilot-instructions.md`. Review that diff in the plan's pull request so the standing rules in this repository stay intact.

## Optional extensions

- `specify extension add github` turns tasks into GitHub issues. It needs a GitHub remote and the GitHub MCP server.
- **Azure DevOps:** use `tools/tasks_export.py --target ado` from this repository. Community Spec Kit extensions for Azure DevOps also exist, but treat them as unreviewed code.

## Known differences from older tutorials

- **Command names changed.** Older posts and labs use `/speckit.specify`-style names and a `/speckit.taskstoissues` command; that command was removed in Spec Kit 1.3.0. Translate them to `/speckit-*`, or install with `--commands`.
- **Turn off automatic tool approval in headless runs.** Set `SPECKIT_COPILOT_ALLOW_ALL_TOOLS=0`.

## References

- [Spec Kit repository and releases](https://github.com/github/spec-kit)
- [Spec Kit and GitHub Copilot](https://github.com/github/spec-kit/blob/main/docs/integrations/copilot.md)
- [Using Spec Kit in an existing project](https://github.com/github/spec-kit/blob/main/docs/how-to/existing-projects.md)
- [Microsoft Learn: Implement spec-driven development using GitHub Spec Kit](https://learn.microsoft.com/en-us/training/modules/spec-driven-development-github-spec-kit-enterprise-developers/)
