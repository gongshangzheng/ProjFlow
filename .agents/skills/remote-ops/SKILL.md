---
name: remote-ops
description: |
  与远端共享机器（GPU/CPU 多人共用）交互的统一指引：容量预检、资源守卫（nice + 线程上限 + 看门狗）、
  代码静态审计与降规模冒烟、部署与代码流转纪律。凡是要在远端跑命令、判断机器是否空闲、
  或在共享机上跑任何超过几秒的任务时使用。其他 skill 只引用这里，不各自重复。
  通用版：不写死任何具体服务器（连接名与仓库根目录见 §1）。
---

# 远端交互与资源护栏（通用版）

> **本 skill 存在的原因（真实事故）**：一次 4K 逐帧解码 + 大模型前向的全量标注任务，在十六人共用的
> GPU 机器上跑起来后，主机 **load average 冲到 103**、**内网隧道两度中断**（SSH 从 banner 超时到
> `Connection refused`，最长 >10 分钟）。当时的脚本没有预检、没有线程上限、没有看门狗——
> 因为项目里只有「跑前 `nvidia-smi` 看一眼」的人工纪律。**从那次起，共享机上的重活必须走本 skill 的三道闸。**

## 1. 配置（每个下游仓库自己填，不写在本 skill 里）

脚本从两个环境变量/默认值取配置，见 `scripts/_remote_common.sh`：

| 变量 | 含义 | 默认 |
|---|---|---|
| `REMOTE_SSH` | `~/.ssh/config` 里的 Host 别名 | `remote` |
| `REMOTE_ROOT` | 远端 git checkout 的绝对路径（脚本在该目录下执行） | `~/workspace` |

把默认值改成你仓库的实际值即可；**不要**在脚本里写死 IP、账号、口令。

**代码只能经 git 流动**：本地 commit → `git push <alias> <branch>` → 远端校验 `git log -1`
与 `git status`。禁止用 rsync/scp 覆盖远端 tracked 文件；一次性脚本放远端 `tmp/`（gitignored）。

## 2. 三道闸

```bash
SD=.agents/skills/remote-ops/scripts

# ① 容量预检（跑任何东西之前）：GPU 是否有人真占显存、load/core、可用内存、磁盘
bash $SD/preflight.sh --gpu-index 0
bash $SD/preflight.sh --gpu-index 0 --json .run/preflight.json   # 顺带落盘证据

# ② 跑任何超过几秒的命令：包在守卫里（nice + 线程上限 + 看门狗）
bash $SD/remote_run.sh --gpu-index 0 --max-cpu-pct 350 --max-rss-mb 24000 --timeout-s 3600 \
  -- python3 scripts/<your_task>.py --flag

# ③ 环境核验（跑之前）：远端跑的是不是评审过的那份代码 + 那个环境
bash $SD/env_check.sh --env <name> --expect-commit <sha> --json results/<topic>/<run-id>/env.json

# ④ 跑之前审代码：静态扫描 + 降规模冒烟（峰值 RSS 外推）
python3 $SD/code_audit.py audit scripts/<your_task>.py
python3 $SD/code_audit.py smoke --cap-mb 2000 -- python3 scripts/<your_task>.py --frames {n}
```

### 退出码表（照此处置，不许绕过）

| 码 | 含义 | 处置 |
|---|---|---|
| 0 | 通过 | 开跑 |
| 1 | 硬阻塞（连不上、环境缺失） | 修好再跑 |
| 2 | **容量被占**（GPU 有人占显存、load 高、内存/磁盘紧） | **停下来问用户，不许抢** |
| 3 | CPU/内存/磁盘压力 / 静态审计有 high 级发现 | 等或降规模；high 级发现先修 |
| 4 | 看门狗按上限终止了命令 | 看采样日志定位哪个上限；降规模或调参后重跑 |
| 5 | 命令自己失败 | 修代码 |

**判 GPU 忙不忙看「有没有进程实际占着显存」（≥500 MiB 即判忙），不看瞬时利用率**——训练任务可能在
20% util 下握着 8 GB，采样窗口也可能正好落在 0%。

### 守卫默认上限（`resource_guard.sh run`）

| 项 | 默认 | 说明 |
|---|---|---|
| `--max-cpu-pct` | 350 | 进程树 CPU 上限（约 3.5 核） |
| `--max-rss-mb` | 24000 | 进程树内存上限 |
| `--max-gpu-mem-pct` | 90 | 单卡显存占比上限 |
| `--timeout-s` | 3600 | 墙钟上限 |
| `--threads` | 8 | `OMP/MKL/OPENBLAS/NUMEXPR_NUM_THREADS` 上限 |
| `--nice` | 10 | 降权运行 |

采样间隔 5 s，写入远端 `.run/guard/run-<ts>.log`。

## 3. 执行纪律（都是踩出来的）

- **解码型任务要额外压低 CPU 上限**：逐帧解 4K/HEVC + 大模型前向时，传 `--max-cpu-pct 250`。
- **禁止**在单次 `ssh 'cmd'` 里用 `nohup … & disown` 起后台任务——会话关闭会把它杀掉。
  用 `setsid nohup … &`，**或**直接用 `remote_run.sh`（推荐：带守卫与日志）。
- 长任务必须有日志 + 进度打印（每 25–200 条一次），否则无法判断是在跑还是卡住。
- 收工前核对：GPU 显存回到基线、自己没有残留进程。
- 内网/隧道式 SSH 目标常被本机全局代理破坏：脚本已 `export NO_PROXY='*'` 并清空 `*_proxy`。

## 4. 与其他 skill 的分工

| 事项 | 去哪 |
|---|---|
| 怎么连、怎么预检、怎么守、怎么部署 | **本 skill** |
| 实验方法论（假设/对照/留痕/evidence） | `experiment` |
| 训练/测试/评测的操作步骤 | 各自的领域 skill |
| 数据集与权重位置 | `datasets` |
