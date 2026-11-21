## 1. Upstream rename

- [x] 1.1 Move `.agents/skills/remote-ops/SKILL.md` to `.agents/skills/remote-runtime/SKILL.md`, set the registration name, and update `.agents/skills/experiment/SKILL.md`; verify one project candidate under the new name and no project candidate named `remote-ops`.
- [x] 1.2 Record the rollout boundary in `.agents/skills/upstream-sync/SKILL.md`; verify downstreams only adopt the local name if they own a project runbook, and no global skill or project scripts are copied.

## 2. Verification and delivery

- [x] 2.1 Compare `.agents/skills/remote-ops/scripts/` to the starting tree and run `bash -n`; verify paths and bytes are unchanged, the compatibility alias resolves, and strict OpenSpec validation passes. Record discovery evidence separately from static checks.
- [ ] 2.2 Prepare a ProjFlow topic branch from `origin/main`; verify its diff carries only the rename change, then push only that branch to `origin`. Record the ref and commit; do not update main or a deployment remote.
