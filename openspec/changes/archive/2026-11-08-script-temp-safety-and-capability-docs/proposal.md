# Proposal: script-temp-safety-and-capability-docs

## Why

The archived `script-and-lib-lifecycle` change established `scripts/tmp/`, `scripts/archive/`, and user approval before consolidating recurring scripts. Follow-up review found that the implementation did not explicitly require checking the ignore rule and tracked-file state before moving temporary scripts, or screening scripts for sensitive content before archiving them into Git. The newly maintained tools under `scripts/check/` also have a README, but their supported interfaces and limitations need a complete, verifiable inventory.

## What changes

- Require operators to verify that the repository's `scripts/tmp/` is ignored and contains no tracked files before using it for a task.
- Require a sensitive-content review before archiving a temporary script. Do not automatically archive a script if sensitive content is found or cannot be ruled out.
- Clarify that scripts with lasting reference value, including confirmed obsolete scripts, are archived rather than deleted by guesswork. Confirmed sensitive content must not be committed to the archive.
- Complete the maintained utility inventory in `scripts/check/README.md`, including each utility's entry point, inputs and options, outputs, dependencies, behavior, and limitations.
- Update only the project guidance and skills that own these workflows.

## Capabilities

This is a repository workflow and documentation change. It does not add or modify runtime specifications.

## Impact

Expected changes include root `AGENTS.md`, the relevant script-using skills, and `scripts/check/README.md`. Implementation is limited to those safety and reference gaps. It does not add a new script, change existing utility behavior, or transfer work to downstream repositories.
