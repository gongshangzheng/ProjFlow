# Web Search 论文检索流程改进

## Why

联网搜集指定主题论文时，需要先让用户确认检索词；同时应准确区分 OpenAlex 与 arXiv 的定位、覆盖范围、全文可用性，并避免根据代理端口监听状态或单一站点探测结果误判 OpenAlex 可用性。

## What Changes

- 在 `~/.agents/skills/web-search/SKILL.md` 整合论文主题检索的关键词确认门禁：确认核心概念、英文关键词/同义词、检索式和范围后才发起检索；仅用户明确授权直接检索时例外。
- 明确 OpenAlex 是跨来源学术作品索引，arXiv 是预印本仓库；两者覆盖范围不同，不能笼统断言 OpenAlex 一定更全。
- 明确 OpenAlex 检索返回记录/元数据不等同于全文下载；全文可用性取决于开放获取状态及记录链接。
- 记录 OpenAlex API 优先直连的本机经验，但将其表述为可变的环境观测；诊断时分别测试 API 直连和代理，不以 7890 监听或 Google 探测单独断定 OpenAlex 状态。
- 修正与上述规则冲突的旧网络策略描述，确保脚本、网络探测和论文检索说明前后一致。

## Impact

- 修改用户级 skill：`~/.agents/skills/web-search/SKILL.md`
- OpenSpec change artifacts：本目录
