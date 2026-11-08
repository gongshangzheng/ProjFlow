# Design: script-temp-safety-and-capability-docs

## 1. Summary

Add explicit pre-use checks for `scripts/tmp/`, a sensitive-content gate before archiving, and a complete operator-facing reference for maintained check utilities. Keep changes to repository guidance and documentation; do not change the utilities' behavior unless verification reveals a specific discrepancy that blocks accurate documentation.

## 2. Grounding

The preceding archived change established the directory lifecycle and recorded that `/scripts/tmp/` was added to `.gitignore`. The current worktree confirms that `git check-ignore -v` matches the three local temporary scripts and `git ls-files scripts/tmp` returns no tracked entries. The previous `scripts/check/README.md` describes purpose and basic use but omits a complete option-by-option and limitation inventory for the scanner.

The tracked check-utility sources are `scripts/check/scan_ui.sh` and `scripts/check/check_contrast.js`. Their current contents and the Impeccable detector's `--help` output are the sources of truth for the utility reference. This change does not claim that an automated secret scanner can prove content safe; if a review finds a possible secret or credential, stop and ask the user rather than archiving it. Task 2 review found no credential-like strings in the two utility sources. It also found a detector default tied to the author's home directory and a browser example tied to one macOS installation. The user decided these machine-specific paths must not be committed. The scanner will resolve its default detector from `PATH`, while preserving explicit `IMPECCABLE_BIN` and `--detector` overrides. The README will use a generic browser executable placeholder and describe environment configuration without including an installed-machine path.

## 3. Temporary script safety contract

Before creating task-scoped files, confirm that the current repository's `/scripts/tmp/` ignore rule applies and that `git ls-files scripts/tmp` returns no entries. If either condition fails, stop before placing temporary content there and resolve the repository rule first.

After temporary use, inspect the exact script contents and relevant history or invocation context for credentials, tokens, private endpoints, user-specific paths, or other content that should not enter version control. If the content is safe and worth retaining, archive it under `scripts/archive/`. If it is confirmed obsolete but still useful as historical evidence, archive it rather than deleting it by assumption. If sensitive content is found or the review is inconclusive, do not copy or move it into a tracked archive; ask the user how to proceed. Disposable material may be deleted only when its owner and purpose are known and the user or task scope authorizes deletion.

## 4. Maintained utility reference

The README is the single operator-facing index for `scripts/check/`. For each utility, document its path, purpose, exact invocation, every option and default, environment inputs, dependencies, output location or return value, exit behavior, and known limitations. Verify each entry against the current source and a safe command invocation. Keep implementation facts in the README rather than duplicating a separate capability inventory in skills; relevant skills should link to the README.

## 5. Guidance ownership

- `AGENTS.md` owns the repository-wide temporary script safety and archive policy.
- `experiment` owns where experiment scripts and run outputs live and when temporary experiment scripts are retired.
- `remote-ops` owns the special case for temporary scripts executed on a remote checkout and the code transfer boundary.
- `scripts/check/README.md` owns the maintained check utility interface and limitations.
- Other skills change only if they directly instruct users to create, move, archive, or use scripts in a way that conflicts with this policy.

## 6. Scope and non-goals

This change closes documentation and workflow safety gaps. It does not move, archive, or delete any existing script. It does not scan or modify the pre-existing `tmp/audit/` artifacts. It does not expand checks to the downstream worktree, rewrite existing script implementations, or create automated secret scanning infrastructure.

## 7. Open questions

- Whether future archive operations should add a dedicated secret-scanning tool is not decided here. Manual content review is the proposed minimum; tool selection is out of scope unless the user requests it.
- Whether the large pre-existing `tmp/audit/` directory should be cleaned or archived is not established by this change and remains untouched.

## 8. Acceptance criteria

- The temporary script policy requires checking ignore behavior and tracked-file state before use.
- The archive policy requires reviewing content for sensitive material and prohibits automatic archival when a concern is found or unresolved.
- The maintained check README documents all supported inputs, options, outputs, dependencies, exit behavior, and limitations, and each item matches the implementation.
- Relevant skills link to the README or state their temporary-script lifecycle consistently with the project policy.
- No files under existing `tmp/audit/` are moved or modified.
- OpenSpec strict validation and applicable documentation and script checks pass.
