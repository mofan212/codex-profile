# 失败处理与反例

仅在阶段无法推进、验证缺失、Review 失败或需要解释反模式时读取本文件。正常阶段判断以 `SKILL.md` 的入口、状态机和门禁表为准。

## 失败处理

| failure | first_action | fallback | stop_when |
| --- | --- | --- | --- |
| 续跑时找不到需求文档路径 | 🔴 CHECKPOINT：只问一个问题确认需求文档、Ticket 或 `.feat-tmp/` 位置 | 如果用户只提供 Ticket 或实现沉淀，先用其反查来源需求文档 | 无法确认来源需求文档时，不创建新需求文档 |
| 无法判断当前阶段 | 列出已读产物、匹配到的状态信号和缺失信息 | 只问一个最关键问题，例如需求文档路径、Ticket 编号或 Review 策略 | 阶段仍不明时，不跳到后续阶段 |
| 外部工作流 Skill 不可用 | 判断当前阶段是否必须依赖该 Skill 或其产物 | 允许用户粘贴对应产物，由当前流程只做回写、门禁检查或状态判断 | 必需产物缺失且无法替代时停止该阶段 |
| 需求文档与代码事实冲突 | 读取 [code-fact-check.md](code-fact-check.md)，按 `code_fact_check` 门禁处理 | 允许用户修正需求、调整 Ticket 或确认当前代码事实 | 阻塞级差异未解决时不进入实现 |
| Ticket 已实现但缺少验证记录 | 🔴 CHECKPOINT：要求补充最近验证命令、输出或可复现检查结果 | 无法运行时记录静态核对范围、未验证项和风险 | 没有任何验证依据时不关闭 Ticket |
| Review 存在阻塞级问题 | 🛑 STOP：先修复阻塞问题并重新验证 | 非阻塞建议可处理或记录不处理理由 | 阻塞级问题未处理时不进入 Ticket DoD |

## 反例黑名单

| anti_pattern | risk | canonical_rule | required_action |
| --- | --- | --- | --- |
| 没有 Feature DoR 就拆 Ticket | Ticket 目标、非目标、验收和依赖不稳定 | `feature_dor_after_spec` | 回到 `feature_dor` 阶段执行门禁 |
| 按 Controller、Service、Mapper、数据库表或测试层拆 Ticket | Ticket 不能独立交付或验收 | `vertical_slice` | 回到 `split_tickets` 阶段按垂直切片拆分 |
| 实现完成或测试通过后直接关闭 Ticket | 跳过 Review、验证复核、Ticket DoD 和实现沉淀 | `review_loop`、`ticket_dod` | 先进入 `review_loop`，通过后再执行 Ticket DoD |
| 把需求设想写入 AI 检索文档 | 长期检索文档污染代码事实 | `archive_ai_docs` | 只把已实现的代码事实归档到 AI 检索文档 |
| 用 `.feat-tmp/` 掩盖长期事实或未完成决策 | 后续会话无法判断权威来源 | `archive_ai_docs` | 阶段结论写回权威产物；最终归档后再按规则处理 `.feat-tmp/` |
| AI 检索文档归档后直接宣布 Feature 完成 | 需求文档继续混入门禁、Ticket 状态和实施过程 | `requirement_doc_convergence` | 先执行需求文档职责检查和临时内容清理 |
