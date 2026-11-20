# Path A: GitHub

## Set up (once)

1. **Create your repository.** Select **Use this template** on this repository and create a **private** repository in your organization. Real work never goes in a public fork.
2. **Open it** in VS Code with GitHub Copilot signed in. Agent mode and skills must be allowed by your organization's Copilot policy.
3. **Optional: add Spec Kit's commands.** See `docs/spec-kit-setup.md`.
4. **Replace the starter constitution.** Edit `.specify/memory/constitution.md` so it holds only rules that are already true for you. Merge it through a pull request approved by your architecture and security leads.
5. **Turn on the spec gate.**
   - Actions runs `.github/workflows/spec-gate.yml` on pull requests that touch `specs/**`.
   - Add a repository secret named `SPEC_LINT_BANNED_TERMS` holding the names that must never appear in the repository.
   - Make the check required in a branch protection rule or ruleset.

## Each feature

1. **Frame the intent.** Use the **Intent brief** issue form or the `intent-brief` skill.
2. **Write the spec.** Run `/speckit-specify`, then `/speckit-clarify` and `/speckit-checklist`. The spec lands in `specs/NNN-name/`.
3. **Review it.** Open a pull request with the template. The product owner and engineering lead both approve, and the spec gate passes. The spec is now Ready.
4. **Plan the build.** Run `/speckit-plan`, `/speckit-tasks` and `/speckit-analyze`, then review the plan in a pull request.
5. **Turn tasks into issues** in one of two ways:
   - `specify extension add github`, which needs the GitHub MCP server;
   - `python tools/tasks_export.py specs/NNN-name --target github --repo OWNER/REPO`, a dry run by default.
6. **Build.**
   - Assign issues to people or to the Copilot coding agent.
   - Every pull request cites its FR, scenario and task IDs.
   - Copilot code review runs as a first pass; a person merges.
7. **Close the loop.** Run `/speckit-converge` after each phase. Behavior changes update `spec.md` in the same pull request.

## Mixed setups

If planning lives in Azure Boards and code lives in GitHub, the Copilot coding agent can be started from Azure Boards work items. This needs a GitHub repository; Azure Repos isn't supported. See [Microsoft Learn](https://learn.microsoft.com/en-us/azure/devops/boards/github/work-item-integration-github-copilot?view=azure-devops).
