# Proposal: script-placement-rules

## Why

`AGENTS.md` requires maintained tools under `scripts/` and allows skill-owned script directories, but it does not state how to choose between them, nor when a `scripts/<area>/` collection has grown into something that should become a skill. The same gap left a stale skill skeleton behind: `.agents/skills/projflow-management/` contains no `SKILL.md` and only two compiled leftovers, while the owning scripts live in the `management` skill.

## What changes

- State the placement order in `AGENTS.md`: a workflow-owned script belongs in that skill's `scripts/` directory; a cross-skill or human-invoked tool belongs in a `scripts/<area>/` directory; one-off work belongs in a temporary directory; superseded tools belong in `scripts/archive/<area>/`.
- State the criteria for promoting a `scripts/<area>/` collection into a skill, and the requirement to propose the promotion to the user before creating one.
- Record the placement decision for `scripts/import_papers.py` with its reason.
- Remove the stale `.agents/skills/projflow-management/` skeleton, which has no manifest, no references, and no tracked files.

## Capabilities

Repository workflow and documentation change. No runtime specification is added or modified.

## Impact

`AGENTS.md` gains the placement rule and one recorded decision; one untracked dead directory is removed. No script changes behavior or location in this change. Downstream repository work, including its own script-subdirectory conventions and migration-script archival, is a separate change in that repository.
