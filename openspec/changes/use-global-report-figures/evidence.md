## Verification

- Moved the project asset placement rules to `documentation`; removed only 21 tracked files from the duplicate `report-figures` package. No active callers of the old local paths were found; project figures and reports are unchanged.
- Six implementation and configuration files are byte-identical to the global distribution. Shell syntax, compatibility link, static discovery, `git diff --check` and OpenSpec strict passed.
- No live rediscovery or rendering run. Matplotlib is not installed in the checked Python environments; no dependencies were installed.

## Release baseline

The release branch starts at ProjFlow `origin/main` (`10fe93d`). Only files present in that baseline were removed. The two local figure commits were not included.
