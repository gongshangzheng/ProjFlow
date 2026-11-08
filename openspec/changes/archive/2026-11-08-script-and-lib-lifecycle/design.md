# Design: script-and-lib-lifecycle

## 1. Summary

Adopt separate homes for maintained command-line utilities, temporary scripts, and archived one-off scripts. Treat `lib/` as implementation code for repeatable steps inside project workflows, not as an alternative command directory. Before consolidating similar temporary scripts into a permanent utility, show the candidate grouping and options to the user and wait for their choice.

## 2. Grounding

The current root-level inventory found `scripts/import_papers.py`. The project guide describes it as the paper JSON import utility. Existing skills also provide their own scripts, including management CRUD utilities, documentation-order maintenance, experiment-report generation, and remote-operation guards. Those skill-owned scripts serve their corresponding workflows and are not automatically root `scripts/` utilities.

The inventory has not established that any current root script is obsolete or temporary. The implementation must inspect script contents and references before making any move. Existing uncommitted `tmp/` content must not be swept into this change without identifying its owner and purpose.

### Inventory evidence

- `git ls-files 'scripts/**' '.agents/skills/**/scripts/**' 'evaluation/scripts/**' 'papers/scripts/**' 'web/scripts/**'` shows one tracked root utility, `scripts/import_papers.py`, plus tracked skill-owned tools, web build hooks, and `.gitkeep` placeholders. It shows no tracked root temporary or archived scripts.
- `rg --files --hidden` confirms the root utility file and the skill-owned script groups. The `tmp/audit/` directory contains browser audit shell scripts, contrast-analysis JavaScript, JSON, images, and reports, but these files are untracked and remain untouched. This is existing temporary work, not evidence that its contents should be archived by this change.
- `scripts/import_papers.py` reads `data/extracted_papers.json`, fetches arXiv metadata, initializes the paper database, clears existing paper rows, and imports the records. Its only current project-guide references are in `AGENTS.md` at the directory tree, paper-module description, and troubleshooting section. A history lookup shows it was introduced in the initial repository commit. Running `python3 scripts/import_papers.py --help` did not display help; it stopped with `FileNotFoundError` for the absent `data/extracted_papers.json` before reaching database operations.
- The separate skill-owned `.agents/skills/papers/scripts/import_papers.py` accepts a JSON input path and imports it. Running it with `--help` treated `--help` as the input filename and stopped with `FileNotFoundError`; it did not modify the database. Similar names do not establish equivalent behavior or make either script obsolete.
- Skill-owned tools are organized by owner and workflow: article-note extraction and validation, design-principles cover extraction, documentation ordering, evaluation model/dataset/result operations, experiment report generation, management Markdown CRUD, papers search/import, and remote resource checks. No task-scoped script cluster with a shared recurring purpose was identified from the existing tracked inventory, so there is no current consolidation candidate to present.
- `web/scripts/build-docs-data.mjs` and `web/scripts/copy-404.mjs` are package build hooks declared by `web/package.json`, not ad hoc root utilities.
- Several guidance references need review in later tasks: `design-principles/SKILL.md` names `scripts/extract_covers.py` while the implementation is skill-owned; `documentation/SKILL.md` has a stale `./scripts/docs_order.py` lead-in followed by correct skill paths; `remote-ops/SKILL.md` references `scripts/_remote_common.sh` without the skill prefix and uses example root-script paths for generic task commands. These were recorded as inventory findings and have not been changed in task 1.

Evidence commands: `git ls-files --stage ...`, `rg --files --hidden ...`, repository-wide `rg` searches for script paths, and `--help` invocations for selected maintained utilities. The review was read-only apart from commands that wrote only to stdout/stderr.

### User-approved implementation correction

During task 2, the user selected the three untracked ad hoc scripts in `tmp/audit/` for relocation to `scripts/tmp/`, while retaining the audit outputs in place. The move exposed a missing repository rule: `scripts/tmp/` was not ignored, so temporary scripts would appear as untracked Git changes. Before changing `.gitignore`, the agent proposed recording this issue in the change and adding `/scripts/tmp/` to the ignore rules. The user approved. The implementation must verify the three moved files are ignored and that retained `tmp/audit/` outputs remain untouched. Completed task 2: moved `scan.sh`, `scan2.sh`, and `contrast.js` into `scripts/tmp/`; added `/scripts/tmp/` at `.gitignore:12`; `git check-ignore -v` reports all three matched by that rule. Confirmed the three files exist at their new paths and representative audit outputs (`report.md`, `speedrun-390.png`, `contrast-final.json`) remain in `tmp/audit/`. A content hash was captured for the retained audit tree before the `.gitignore` edit; no files under `tmp/audit/` were modified. Repository search found no references to the moved paths outside this change's task text.

## 3. Proposed directory contract

- `scripts/` contains maintained, user-invoked project utilities with a clear purpose and a documented way to run them.
- `scripts/<area>/` contains maintained utilities grouped by a stable capability when the root would otherwise become a flat or ambiguous collection. For example, `scripts/check/` is appropriate only if inspection identifies a coherent set of recurring checks.
- `scripts/tmp/` contains task-scoped scripts that are still being developed or used. Create it when needed. Do not commit temporary scripts as maintained utilities. At task completion, delete disposable files or move a useful historical one-off to `scripts/archive/`.
- `scripts/archive/` contains retained historical scripts that are not part of the supported routine workflow. Archive is not a substitute for determining whether a script is still used; check references and explain the reason for retaining it.
- `.agents/skills/<skill>/scripts/` remains the home for utilities that only implement that skill's workflow. Do not move them to root `scripts/` merely because they are scripts.
- `lib/` contains importable implementation code used by concrete project workflows. It should not be used for user-facing entry points, ad hoc experiments, or unrelated shared code. Place a helper near its owning module when that makes ownership clearer. Add a root `lib/` only if the inspected code has a concrete cross-workflow need for it.
- Data directory names express different roles and must be grounded in their contents. Use `data/` for general application data, `datasets/` or module-owned dataset directories for dataset definitions or assets, and `results/` for generated outputs. Do not assume that every `datasets/` directory contains raw dataset files. For this repository, verify the existing `data/papers.db` and `evaluation/datasets/` contents before recording their precise roles in `AGENTS.md`.

> **Why & What - keep entry points separate from workflow code**
>
> **What:** Keep maintained commands in `scripts/` and reusable workflow implementation in the owning module or, when justified, `lib/`.
>
> **Why:** This makes it clear what an operator can run and where workflow logic belongs. It does not by itself define package boundaries or justify moving existing code.
>
> **Alternatives considered:** Putting all code in `scripts/` keeps discovery simple, but blurs runnable commands and imported implementation. Putting all helpers in a root `lib/` gives a single home, but weakens ownership for module-specific logic.
>
> **Fallback:** If a workflow has no shared implementation, keep its logic beside its module or inside its skill rather than creating a speculative `lib/` package.

## 4. Temporary script lifecycle and consolidation gate

For each task that needs an ad hoc script, create it under `scripts/tmp/` and name it for its purpose. Before finishing the task, classify it as disposable, historically useful, or a candidate for recurring use. Delete disposable files. Move historical one-offs to `scripts/archive/` only when retention is useful and their references have been checked.

When multiple temporary scripts appear to solve substantially similar recurring problems, do not independently combine them into a permanent utility. Prepare a short decision brief that names the candidate scripts, their overlapping inputs and outputs, the proposed shared command, maintenance cost, and alternatives. Ask the user whether to create a permanent utility, and where it belongs. Until they choose, keep the scripts temporary or archive them individually; do not present an unapproved utility as an established capability.

## 5. Guidance ownership

- Root `AGENTS.md` owns the repository-wide directory contract, names the actual maintained root-script capabilities, and describes data-related directories based on verified contents.
- A skill owns the instructions for scripts that implement its workflow. Update only skills whose script lifecycle or invocation guidance changes. In particular, inspect experiment and remote-ops guidance for consistency with the root temporary/archive convention, and inspect other script-bearing skills before editing them.
- Do not add capability lists to a skill by inference from directory names. Verify the script, its current behavior, and invocation before documenting it.
- A root `lib/` convention belongs in `AGENTS.md`. Update a skill only if that skill's workflow uses or creates code there. Do not add a generic `lib/` rule to every skill.

## 6. Scope and non-goals

This change establishes repository workflow and documentation conventions. It does not require creating `scripts/tmp/`, `scripts/archive/`, `scripts/check/`, or `lib/` when no current need justifies them. It does not authorize deletion, relocation, or consolidation of existing scripts without content and reference checks. It does not alter skill-owned script locations or runtime behavior.

## 7. Benefits and costs

The convention gives temporary work a predictable home and makes supported commands easier to distinguish from historical artifacts and implementation helpers. It also creates a user review point before repeated ad hoc work becomes a maintenance commitment.

The cost is an extra classification step at task completion. An archive can still become a dumping ground if scripts are moved without checking references and recording why they remain. The inventory and documentation must therefore stay evidence-based, and the user decision gate must not be bypassed.

## 8. Acceptance criteria

- `AGENTS.md` states the distinct purpose and lifecycle of maintained root scripts, temporary scripts, archived scripts, and `lib/` code, and describes `data/`, `datasets/`, and `results/` according to verified repository usage.
- Every changed skill has a demonstrated relationship to root scripts or `lib/`, and its durable capabilities are described with verified paths and invocation guidance.
- The existing script inventory and repository references are checked before any move, deletion, or new permanent utility.
- Similar temporary scripts result in a decision brief and explicit user choice before consolidation.
- No unsupported or obsolete status is asserted for a script based only on its location or age.
- Relevant links and documented command paths resolve after the changes.

---

This design distinguishes verified repository inventory from proposed conventions. The user decision on any proposed reusable utility remains open until implementation presents the candidate options.
