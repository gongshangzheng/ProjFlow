---
title: "评测管道验证：配置到报告的端到端链路"
date: "2026-11-02"
run_id: "demo-pipeline-20261102a"
status: "complete"
verdict: "inconclusive"
summary: "演示管道验证：评测→结果→报告链路跑通。mock-chat 在 mock-mini 上 accuracy 0.93（固定值），两次运行一致；数字无对照意义，verdict=inconclusive。"
source: "evaluation/results/demo-pipeline_mock-chat_mock-mini.json"
---

## 背景与目标

ProjFlow 的评测模块能跑评测、存结果，但实验结论此前没有可审阅的载体。本实验是一次管道验证：先确认「配置→运行→结果→报告」这条链路能否端到端跑通并稳定复现，再谈用它来回答真实问题。

## 当前问题

已有证据：评测模块的 CRUD 与结果落盘在既有页面可用。缺失证据：结果能否稳定复现、报告约定（frontmatter/章节/manifest/incomplete 推导）在生成脚本与后端两侧是否一致，都没有验证过。本实验只回答链路问题，不回答任何模型质量问题。

## 实验设计

用 mock 模型（返回固定 accuracy 0.93）与 3 条 mock 数据集，按同一配置 demo-pipeline 独立运行两次，比对两次结果是否一致；再用报告生成脚本按作者清单产出一篇完整报告，核对生成侧与解析侧的 incomplete 推导是否一致。判据是「两次运行结果相同 + 报告通过完整校验」，不涉及数值好坏。

## 结果与分析

两次独立运行 accuracy 均为 0.93，复现差为 0——链路可复现。报告侧：author 清单（叙述字段 background/problem/design/analysis/conclusion + evidence 六项 + metrics + cases）经 build_report.py 生成后，后端推导 incomplete=False、problems 为空，与生成器诊断一致。关键结论上界：两次一致的 0.93 是 mock 固定值注入，不代表模型能力。

## 结论与下一步

已验证事实：评测与报告链路可运行、可复现、两侧约定一致。未解决问题：真实模型接入后的指标含义、延迟采集（脚本 TODO 未实现）。下一步：接真实模型端点，把 accuracy 换成有意义的对照指标，并按本流程产出真实实验报告。

## 附录：配置与完整数据

### 环境与配置

- 模型: mock-chat / v1 (internal://mock)
- 数据集: mock-mini / 3 条 QA
- 配置: demo-pipeline
- 运行时间戳: 2026-11-02T11:59:43
- 执行入口: python3 .agents/skills/evaluation/scripts/run_evaluation.py demo-pipeline
- 随机种子: 无（mock 输出固定）

### 局限与边界

模型与数据集均为 mock：accuracy 为脚本固定值（0.93），不反映任何真实模型能力；样本量 n=2（两次运行 × 3 条 QA），仅验证可复现性，不构成质量结论。图片为纯色占位。

### 来源与核查

- run 产物：evaluation/results/demo-pipeline_mock-chat_mock-mini.json
- 详细来源见 manifest 各条目的 source 字段；单位、样本量与局限见 manifest 的 metrics 条目。
- 指标与趋势见 metrics.json（series 折线 + tables 指标表）。

