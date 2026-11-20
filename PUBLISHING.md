# Publishing checklist (maintainers)

Publish privately first, check everything, then make the repository public.

## 1. Before you start

- **Tools:** Git, [uv](https://docs.astral.sh/uv/getting-started/installation/) (it fetches Python for you), and VS Code with GitHub Copilot.
- **Commit email:** on GitHub, open Settings → Emails, turn on **Keep my email addresses private**, and commit with the noreply address shown there.
- **Your employer's rules:** if this was built at work, check your employer's open-source release rules before the repository goes public.

## 2. Create the repository (private)

Create an empty **private** repository with no README, .gitignore or license. Then clone it and set your commit email:

```bash
git clone https://github.com/OWNER/spec-driven-delivery-starter.git
cd spec-driven-delivery-starter
git config user.email "NOREPLY-ADDRESS"
```

## 3. Add the pinned Spec Kit scaffold, in its own commit

```bash
uvx --from git+https://github.com/github/spec-kit.git@v1.4.2 specify init --here --integration copilot --script ps
git add -A
git commit -m "Add Spec Kit v1.4.2 scaffold"
git branch -M main
```

- **The script type is baked into the template.** `--script ps` (PowerShell) suits Windows laptops; `--script sh` suits macOS and Linux. Match the machines your users have.
- If `init` warns that the folder isn't empty, answer **y**.

## 4. Lay this starter on top

```bash
tar -xf PATH/TO/spec-driven-delivery-starter.zip --strip-components=1 -C .
git status
```

- `tar` is built into Windows 10 and later, and into macOS.
- Expect the starter's files to show as new, and `.specify/memory/constitution.md` as modified. The starter constitution replaces Spec Kit's blank one.

## 5. Scan, commit and push

Run the gate. It must report `Spec gate: 0 error(s)`.

```bash
uv run tools/spec_lint.py
```

Then commit and push:

```bash
git add -A
git commit -m "Add spec-driven delivery starter"
git push -u origin main
```

## 6. Turn on the gate and smoke-test (still private)

1. **Run the gate.** Actions → **spec-gate** → **Run workflow**. It must pass.
2. **Check Copilot sees everything.** Open the repository in VS Code and type `/` in Copilot Chat. The `speckit-*` skills should be listed, along with `intent-brief`, `spec-review` and `retro-spec`. **spec-coach** should appear in the agent picker.
3. **Try a spec.** Run `/speckit-specify` with the prompt at the bottom of `specs/001-member-claim-status/intent-brief.md`, and confirm it creates a new folder under `specs/`.
4. **Throw the test away:** `git restore .` then `git clean -fd`.

## 7. Go public

1. **Make it public.** Settings → General → Danger Zone → **Change visibility** → Public.
2. **Make it a template.** Settings → General → tick **Template repository**.
3. **Add a license.** Add file → Create new file → name it `LICENSE` → **Choose a license template**.
4. **Tag a release.** Releases → **Draft a new release** → tag `v1.0`, and note the Spec Kit version (v1.4.2).
