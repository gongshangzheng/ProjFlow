# Design: script-placement-rules

## 1. Summary

Make the script home a decision, not a default. A script goes to the skill that owns its workflow; when no skill owns it, it goes to a `scripts/<area>/` directory; work that will not be kept goes to a temporary directory; superseded tools go to `scripts/archive/<area>/`. Promotion of an area directory into a skill is a proposal to the user, never a unilateral refactor.

## 2. Grounding

Upstream `scripts/` holds `import_papers.py` and the ignored `tmp/` and `archive/` directories. Script-bearing skills are `article-note`, `design-principles`, `documentation`, `evaluation`, `experiment`, `management`, `papers`, and `remote-ops`. `.agents/skills/projflow-management/` contains no `SKILL.md`, contains only `scripts/__pycache__/mgmt_io.cpython-313.pyc` and `task_schema.cpython-313.pyc`, has zero tracked files, and appears in no repository file. The two compiled modules it references are maintained in `.agents/skills/management/scripts/`.

## 3. Placement rule

Choose the first matching tier.

1. **Skill-owned.** A script that implements one skill's workflow and is meaningless outside it belongs in `.agents/skills/<skill>/scripts/`. Examples in this repository: `docs_order.py`, `build_report.py`, `preflight.sh`, and the management CRUD scripts.
2. **Repository tool.** A script that spans skills or modules, or that a person runs directly against the repository rather than through a skill workflow, belongs in `scripts/<area>/` and is documented by that directory's README.
3. **Temporary.** Work that exists for one task belongs in the ignored temporary directory and is deleted or archived when the task ends.
4. **Archived.** A superseded tool that still carries reference value belongs in `scripts/archive/<area>/`.

A script may move between tiers when its ownership changes. Moving it follows the same reference and sensitive-content checks already required for archival.

## 4. Promotion criteria

An area directory becomes a skill only when all of these hold: it has a distinct trigger, it carries its own step-by-step procedure rather than a list of independent commands, its scripts share criteria or state, and an agent must execute the procedure repeatedly rather than a person running one command occasionally.

A collection of independent one-purpose scripts that happen to share a directory, such as per-experiment verification scripts, fails this test and stays a repository tool directory. When the criteria are met, the promotion is proposed to the user with the target skill name, the scripts it would absorb, and the maintenance cost. No skill is created without that approval.

## 5. Recorded decision: `scripts/import_papers.py`

It stays at `scripts/import_papers.py`. It reads `data/extracted_papers.json`, enriches records from the arXiv API, clears the paper table, and imports the result; it depends on `server.db` rather than on the `papers` skill's workflow, and the papers skill already provides a separate path-based importer. Moving it into the skill would place a server-module dependency inside a skill bundle and overload one skill with two importers of different purpose.

## 6. Files and parallel plan

- `AGENTS.md`: extend `§脚本与库目录约定` with the placement order, the promotion criteria, and the recorded `import_papers.py` decision.
- `.agents/skills/projflow-management/`: delete the untracked skeleton directory.

Both edits touch independent targets, but they are small and share one evidence set, so this change is executed serially with no parallel dispatch.

## 7. Scope and non-goals

This change does not move, rename, or rewrite any maintained script. It does not create a skill, because no existing directory meets the promotion criteria. It does not touch the downstream repository: its different subdirectory conventions (`scripts/checks/`, `scripts/migration/`), its scattered root scripts, and its completed-migration scripts require separate decisions and a separate change in that repository.

## 8. Open questions

- Whether downstream should adopt this placement order verbatim, or keep its existing `scripts/checks/` and `scripts/migration/` areas with only the promotion criteria added, remains undecided and belongs to the downstream change.
- Whether downstream `scripts/migration/` should be archived is a downstream decision, not this change's.

## 9. Acceptance criteria

- `AGENTS.md` states the placement order, the promotion criteria, and the `import_papers.py` decision.
- Every maintained script in this repository maps to exactly one tier, and no skill directory is left without a `SKILL.md`.
- `.agents/skills/projflow-management/` no longer exists and no repository file references it.
- OpenSpec strict validation and `git diff --check` pass.
