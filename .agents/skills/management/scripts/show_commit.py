#!/usr/bin/env python3
"""快速查看任务进展中引用的 commit 的真实更改内容。

用法:
    # 直接看某个 commit（--stat 摘要，默认）
    python3 show_commit.py abc1234
    # 看完整 diff
    python3 show_commit.py abc1234 --diff
    # 列出某任务 progress 中引用的所有 commit 并逐个显示 --stat
    python3 show_commit.py --slug myproject --id t2-3 [--diff]

progress 记 commit 公约: note 末尾写 "(commit abc1234)"，多个逗号分隔，
如 "(commit abc1234, def5678)"。本脚本按此格式提取。

Self-locating: run from anywhere; resolves the repo root from its own path.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import mgmt_io

COMMIT_RE = re.compile(r"\(commit\s+([0-9a-fA-F, ]+)\)")


def extract_commits(note: str) -> list:
    hashes = []
    for m in COMMIT_RE.finditer(note or ""):
        for h in m.group(1).split(","):
            h = h.strip()
            if h and h not in hashes:
                hashes.append(h)
    return hashes


def git_show(commit: str, diff: bool) -> int:
    args = ["git", "-C", str(mgmt_io.REPO_ROOT), "--no-pager", "show", commit]
    if not diff:
        args.append("--stat")
    return subprocess.call(args)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("commit", nargs="?", default=None, help="commit hash（短/长均可）")
    ap.add_argument("--slug", default=None, help="project slug（配合 --id 用）")
    ap.add_argument("--id", default=None, help="task id：列出该任务 progress 引用的所有 commit")
    ap.add_argument("--diff", action="store_true", help="显示完整 diff（默认只显示 --stat 摘要）")
    args = ap.parse_args()

    if args.commit:
        return git_show(args.commit, args.diff)

    if not (args.slug and args.id):
        ap.error("需要 <commit>，或 --slug + --id")

    tree = mgmt_io.read_tasks(args.slug)
    _, _, task = mgmt_io.find_task_by_id(tree.get("tasks", []), args.id)
    if task is None:
        sys.exit(f"error: task {args.id!r} not found in project {args.slug!r}")

    entries = []
    for p in task.get("progress") or []:
        for h in extract_commits(p.get("note", "")):
            entries.append((p.get("date", ""), h))

    if not entries:
        print(f"任务 {args.id!r} 的 progress 中没有 (commit xxx) 引用。")
        return 0

    print(f"任务 {args.id!r}（{task.get('title', '')}）引用的 commit：\n")
    rc = 0
    for date, h in entries:
        print(f"===== {h}  (progress @ {date}) =====")
        if git_show(h, args.diff) != 0:
            print(f"warn: git show {h} 失败（commit 不存在或已被 rebase）", file=sys.stderr)
            rc = 1
        print()
    return rc


if __name__ == "__main__":
    sys.exit(main())
