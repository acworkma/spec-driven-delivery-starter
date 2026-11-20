# Guardrails for regulated work

These guardrails assume protected health information (PHI) is in play somewhere in the business. Your compliance team owns the final word. **Check current terms before relying on any statement below.**

## Data

- **No real personal data anywhere in the delivery system.** No PHI, member data, real names or real identifiers in prompts, specs, issues, work items, commits, test fixtures or screenshots.
- **Use synthetic data.** Generators such as [Synthea](https://synthetichealth.github.io/synthea/) produce realistic records with no real patients. Keep synthetic identifiers obviously fake, e.g. `CHP-0004417`.
- **The spec gate backs this up.** `tools/spec_lint.py` fails on SSN-like numbers anywhere in the repository.

## Platforms and agreements

As of November 2026:

- **Azure DevOps Services:** listed among the in-scope services in [Microsoft's HIPAA/HITECH documentation](https://learn.microsoft.com/en-us/compliance/regulatory/offering-hipaa-hitech).
- **GitHub and GitHub Copilot:** covered by GitHub's own terms. GitHub's Data Protection Agreement restricts sending PHI to GitHub without GitHub's prior written consent, and says preview features should not be used with regulated data.
- **Copilot Business and Enterprise data handling** (training, retention by surface): see the [GitHub Copilot Trust Center](https://copilot.github.trust.page/faq).

**The practical rule:** specs, plans and code are PHI-free by design, so they can live on any approved platform. Production data stays in systems approved to hold it.

## Agents and tools

- **Humans approve every gate.** AI output is a draft.
- **No auto-merge.** Coding-agent pull requests need a human merge.
- **Turn off Spec Kit's automatic tool approval.** Spec Kit's headless Copilot runs allow all tools by default. Set `SPECKIT_COPILOT_ALLOW_ALL_TOOLS=0`.
- **Connect MCP servers read-only first.** For example, the Azure DevOps Remote MCP server with the `X-MCP-Readonly` header. Enable writes deliberately.
- **Pin the Spec Kit version.** Spec Kit releases often, so pin it and review changes before upgrading. See `docs/spec-kit-setup.md`.
- **Treat community extensions as unreviewed code.** Read them before installing.
