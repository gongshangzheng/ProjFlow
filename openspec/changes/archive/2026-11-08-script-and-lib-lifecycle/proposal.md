# Proposal: script-and-lib-lifecycle

## Why

The repository has several script homes with different purposes, including root `scripts/`, module-specific directories, and scripts bundled with skills. Without a clear rule for one-off work, scripts can accumulate in permanent locations even when they were only needed temporarily. The root `scripts/` inventory currently contains `scripts/import_papers.py`; it does not by itself establish whether any existing script is obsolete. The repository also has no stated convention for a root-level `lib/` directory.

## What changes

- Define a lifecycle for root-level temporary scripts: create them under `scripts/tmp/`, keep them only for the current task, then move useful historical one-offs to `scripts/archive/` when the work is done. Do not treat an unreviewed script as obsolete based on its age or filename alone.
- During implementation, inventory the existing root `scripts/` files and identify temporary scripts that solve substantially similar problems. Present proposed reusable capabilities and their trade-offs to the user before turning any cluster into a maintained utility under a focused directory such as `scripts/check/`.
- Document the purpose and boundaries of root `scripts/`, `scripts/tmp/`, `scripts/archive/`, and focused permanent utility directories in the relevant project guidance and skills. List concrete maintained capabilities only after verifying the scripts that provide them.
- Define `lib/` as a home for code that implements reusable steps in concrete project workflows, distinct from command-line entry points in `scripts/`. Decide during implementation whether a root `lib/` is appropriate for this repository, and update `AGENTS.md` and the relevant skills only where they own the convention or workflow.
- Clarify repository data-directory responsibilities in `AGENTS.md`, distinguishing general application data (`data/`), dataset definitions or assets (`datasets/` or module-owned equivalents), and generated results (`results/`). Verify actual contents before documenting each directory; do not infer that a directory stores raw dataset files from its name alone.

## Capabilities

This is a repository workflow and directory-convention change. It does not add or modify a runtime capability specification.

## Impact

Expected documentation and workflow changes include root `AGENTS.md` and relevant skills that create, maintain, or use project scripts. The implementation must inspect the existing script inventory before deciding whether any files should move or whether a maintained `scripts/<area>/` capability should be introduced. It must also inspect current data-related directories and document their actual roles in `AGENTS.md`. No existing script is moved or archived by this proposal alone.
