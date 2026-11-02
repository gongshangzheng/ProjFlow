---
title: "评测管道验证：配置到报告的端到端链路"
date: "2026-11-02"
run_id: "demo-pipeline-20261102a"
status: "complete"
verdict: "inconclusive"
summary: "演示管道验证：评测→结果→报告链路跑通。mock-chat 在 mock-mini 上 accuracy 0.93（固定值），两次运行一致；数字无对照意义，verdict=inconclusive。"
source: "evaluation/results/demo-pipeline_mock-chat_mock-mini.json"
---

## 结论摘要

演示管道验证：评测→结果→报告链路跑通。mock-chat 在 mock-mini 上 accuracy 0.93（固定值），两次运行一致；数字无对照意义，verdict=inconclusive。

## 实验问题与假设

评测模块（配置→运行→结果落盘）与实验报告生成脚本（清单→报告→incomplete 推导）能否端到端跑通并稳定复现？

## 实验设置与环境

- 模型: mock-chat / v1 (internal://mock)
- 数据集: mock-mini / 3 条 QA
- 配置: demo-pipeline
- 运行时间戳: 2026-11-02T11:59:43
- 执行入口: python3 .agents/skills/evaluation/scripts/run_evaluation.py demo-pipeline
- 随机种子: 无（mock 输出固定）

## 指标结果

见下方指标表；单位、样本量与局限见 manifest 的 metrics 条目。

## 案例展示

案例由作者按选样规则显式选择，见 manifest 的 cases 条目。

## 失败案例与限制

模型与数据集均为 mock：accuracy 为脚本固定值（0.93），不反映任何真实模型能力；样本量 n=2（两次运行），仅验证可复现性，不构成质量结论。

## 结论与建议

链路完整跑通。评测结果 JSON、报告四件套、后端推导、前端渲染均符合约定；incomplete 推导两侧一致（对拍测试覆盖）。真实模型接入后可直接沿用本流程。

## 产物来源

- run 产物：evaluation/results/demo-pipeline_mock-chat_mock-mini.json
（详细来源见 manifest 各条目的 source 字段。）

