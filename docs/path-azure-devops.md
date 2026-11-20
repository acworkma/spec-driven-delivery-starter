# Path B: Azure DevOps

## Set up (once)

1. **Import the starter.** In Azure Repos, go to **Repos → Import repository** and paste this repository's clone URL. If your network blocks GitHub, ask for a zip and push it instead.
2. **Open it** in VS Code with GitHub Copilot signed in. Copilot reads `.github/copilot-instructions.md` and `.github/skills/` from your local clone, wherever the repository is hosted.
3. **Optional: add Spec Kit's commands.** See `docs/spec-kit-setup.md`.
4. **Replace the starter constitution.** Edit `.specify/memory/constitution.md` so it holds only rules that are already true for you. Merge it through a pull request approved by your architecture and security leads.
5. **Create the spec-gate pipeline** from `pipelines/spec-gate.yml`.
   - Optional: a variable group named `spec-gate` with the secret `SPEC_LINT_BANNED_TERMS`. Uncomment the group in the YAML.
6. **Set branch policies on `main`:**
   - **Required reviewers.** Product owners on `/specs/*`, engineering leads on everything.
   - **Required linked work items:** `az repos policy work-item-linking create --blocking true --enabled true --branch main --repository-id <id>`.
   - **Build validation.** The spec-gate pipeline, with path filter `/specs/*; /.specify/*; /tools/spec_lint.py`. YAML `pr:` triggers don't apply to Azure Repos, so this policy is what runs the gate.
7. **Pull request template.** `.azuredevops/pull_request_template.md` is applied automatically. It is advisory; the branch policies are the real gate.

## Each feature

1. **Frame the intent.** Use the `intent-brief` skill, or create a User Story or Product Backlog Item with the four boxes in the description.
2. **Write the spec.** Run `/speckit-specify`, then `/speckit-clarify` and `/speckit-checklist`, on a branch named `NNN-name`.
3. **Review it.** Open a pull request linked to the work item. The product owner and engineering lead approve, and the spec gate passes. The spec is now Ready.
4. **Plan the build.** Run `/speckit-plan`, `/speckit-tasks` and `/speckit-analyze`, then review the plan in a pull request.
5. **Turn tasks into work items:** `python tools/tasks_export.py specs/NNN-name --target ado --org https://dev.azure.com/ORG --project PROJECT`. It is a dry run by default; add `--execute` to create them. It creates one User Story per spec user story and one Task per `T###`, as child items, tagged with the spec and story.
   - **Process templates:** use `--story-type "Product Backlog Item"` for Scrum, `"Requirement"` for CMMI and `"Issue"` for Basic.
6. **Build.**
   - Branches and pull requests cite FR, scenario and task IDs, and link their work items.
   - Copilot code review in Azure Repos reads `.azuredevops/copilot-instructions.md` from the target branch, where it's available to your organization.
7. **Close the loop.** Run `/speckit-converge` after each phase. Behavior changes update `spec.md` in the same pull request.

## Optional: Azure DevOps MCP server for Copilot

The Azure DevOps Remote MCP server lets Copilot read work items and, if you allow it, write them.

- **Requirements:** your organization must use Microsoft Entra ID.
- **Start read-only.** Example workspace configuration in `.mcp.json` (check the [current documentation](https://learn.microsoft.com/en-us/azure/devops/mcp-server/remote-mcp-server?view=azure-devops) for the exact format):

```json
{
  "mcpServers": {
    "ado": {
      "type": "http",
      "url": "https://mcp.dev.azure.com/<your-org>",
      "headers": { "X-MCP-Readonly": "true" }
    }
  }
}
```
