#!/bin/bash
# Shared config for every remote-interaction script. Source this file; do not execute it.
#
# 本文件是**通用版**：不写死任何具体服务器。下游仓库按需覆盖下面两个变量
# （直接改默认值，或在 CI/本地环境里导出同名环境变量）：
#
#   REMOTE_SSH     ssh 别名（~/.ssh/config 里的 Host），默认 remote
#   REMOTE_ROOT    远端仓库根目录（可写代码/产物），默认 ~/workspace
#
# 若远端没有固定工作树，把 REMOTE_ROOT 设成远端某个 git checkout 的绝对路径即可。

REMOTE="${REMOTE_SSH:-remote}"
SSH_OPTS=(-o ConnectTimeout=10)
REMOTE_ROOT="${REMOTE_ROOT:-~/workspace}"
REMOTE_LOG_DIR="${REMOTE_ROOT}/results/.run_logs"

# 本文件位于 <repo>/.agents/skills/remote-ops/scripts/ → 仓根在四级之上
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"

# 内网/隧道类 SSH 目标常被本机全局代理破坏：默认绕过代理
export NO_PROXY='*'
unset ALL_PROXY all_proxy HTTP_PROXY HTTPS_PROXY http_proxy https_proxy 2>/dev/null || true

ssh_cmd() {
  ssh "${SSH_OPTS[@]}" "$REMOTE" "$1"
}

die() {
  echo "ERROR: $1" >&2
  exit 1
}

port_open() {
  nc -z -w 3 localhost "$1" >/dev/null 2>&1
}
