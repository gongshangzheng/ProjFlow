# Tasks: add-experiment-report

> 状态标记：`[ ]` 待办 / `[x]` 完成 / `[-]` 跳过（附原因）。每完成一项即提交。

## 1. 约定与文档

- [ ] 1.1 `management/experiments/README.md`：目录约定（topic/slug 结构、四个文件、frontmatter 枚举、metrics.json schema、manifest.json schema、incomplete 语义），移植 CyberVerse 版并按 D7 换环境段字段、裁掉媒体目录部分
- [ ] 1.2 `.agents/skills/experiment/SKILL.md`：按 design D8 裁剪/改写（模块无关方法论 + 报告流程 + 与 evaluation skill 的边界表）
- [ ] 1.3 design D9 确认菜单归属：读 MainLayout 分组代码，定「项目管理」组具体插入位置；`HIDDEN_KEYS` 登记

## 2. 生成脚本（`.agents/skills/experiment/scripts/build_report.py`，纯标准库）

- [ ] 2.1 作者清单解析 + 校验：report 文字四项、evidence 六项、metrics 八字段、cases（id/kind=image/src/source_run/input/selection_reason）
- [ ] 2.2 报告组装：frontmatter（八个必填）、8 章节骨架、环境段必填字段检查（D7：模型/数据集/配置/时间戳/入口/seed）
- [ ] 2.3 案例图片复制进 `assets/`、sha256 计算、metrics.json（series/tables）透传写入
- [ ] 2.4 incomplete 推导与 diagnostics 写入 manifest；已有报告不覆盖（`--force` 显式覆盖）
- [ ] 2.5 脚本自测：空清单 → incomplete 草稿；补全 → complete；破坏 case 路径 → diagnostics 记缺失

## 3. 后端（只读）

- [ ] 3.1 `server/parsers/experiments_parser.py`：两级目录扫描、frontmatter/章节/evidence/cases 校验、incomplete 推导（常量与脚本对拍，注释互指）
- [ ] 3.2 `server/routers/management.py`：`GET /api/management/experiments`、`GET /api/management/experiments/{topic}/{slug}`、`GET /api/management/experiments/{topic}/{slug}/assets/{file}`（safe_resolve + 扩展名白名单）
- [ ] 3.3 pytest：用 2.5 生成的产物断言列表/详情/资产路由与 incomplete/invalid 标记（两套常量对拍测试落在这里）

## 4. 前端（`web/src/`）

- [ ] 4.1 `api/experiments.js`：列表/详情/资产 URL 封装
- [ ] 4.2 `views/management/ExperimentsPage.vue`：列表（topic 分组、status/verdict/incomplete 筛选）+ 详情（元信息条、MarkdownRenderer 正文、指标表、趋势 SVG、案例图集 A/B 并排/交替、pixelated 不缩放）；深链 `?topic=&slug=`
- [ ] 4.3 路由 `/management/experiments` + 菜单入口（按 1.3 结论）；遵循 web-a11y 既有标准（键盘可达、对比度、窄屏）
- [ ] 4.4 浏览器验收：筛选 → 详情 → A/B 交替 → 深浅色 + 窄屏

## 5. 首篇真实报告 + 收尾

- [ ] 5.1 用 `evaluation/results/` 现有数据 + SpeedRun 产物生成首篇报告（作者清单如实填写，含失败边界与结论上界）
- [ ] 5.2 AGENTS.md 目录结构图补 `management/experiments/`；evaluation/SKILL.md 加一行互链（报告走 experiment skill）
- [ ] 5.3 全链路自检（服务重启 → 列表/详情/资产/前端渲染）→ archive change
