# 1. Review Loop 定位

`review_loop` 是 `implement_issue` 和 `issue_done` 之间的质量门禁，用于让实现结果经过独立 Review 或明确的替代策略后再执行 Issue DoD。

Main Agent 永远负责阶段状态、Review 结论复核、修复决策、Issue DoD 和最终汇报。Review Subagents 只负责审查，不直接修改代码、不推进阶段、不更新工作流状态。

# 2. 触发和降级

| trigger | action | forbidden |
| --- | --- | --- |
| Issue 已实现且涉及代码、测试、配置、接口、数据结构、长期文档或 AI 检索事实 | 进入 `review_loop` | 未经过 Review 或明确替代策略就执行 Issue DoD |
| 当前会话支持启动独立 Subagents，且用户明确选择 Subagents Review | 启动 Review Subagents，传入 §3 上下文，要求按 §4 输出 Review 结果 | 未经用户明确选择就启动 Subagents Review；让 Subagents 修改代码或裁决 DoD |
| 当前会话不支持 Subagents，或用户未选择 Subagents Review | 暂停并说明可用 Review 策略；询问用户选择 Main Agent 自审、提供外部 Review 结果，或跳过 Review 并记录原因 | 静默降级为 Main Agent 自审；把 Main Agent 自审称为独立 Review |
| 用户提供外部 Review 结果 | 读取 [readiness-checklists.md](readiness-checklists.md) 的「Review 结果处理规则」分类并处理 | 要求外部 Review 必须使用固定格式后才处理 |
| 用户明确选择跳过 Review | 记录跳过原因和风险，继续执行 Issue DoD 的其他检查 | 未记录原因就通过 Review 门禁 |

如果用户选择 Main Agent 自审，完成说明和工作流产物中必须写明 `Review 方式：Main Agent 自审`。

如果用户选择跳过 Review，完成说明和工作流产物中必须写明 `Review 方式：跳过 Review`、跳过原因和风险；不要把跳过 Review 称为独立 Review 或无阻塞 Review。

# 3. Review 输入

启动 Review Subagents 前，Main Agent 必须提供最小但完整的上下文：

- 当前 Issue 目标、范围、非范围、验收标准和验证方式
- 来源需求文档路径和必要业务规则摘要
- 本轮实现 diff、关键文件路径、测试或构建结果
- 已知限制、无法运行的验证项和替代核对方式
- Review 范围：只审当前 Issue 相关改动，不要求无关重构
- 二次及后续循环时，补充上一轮 findings、Main Agent 复核决策、已修复项、本轮新增 diff 和最新验证结果；明确要求 Review Subagents 只复查修复效果和可能新增的回归风险，不重复审查已确认的 `non_blocking` 或 `ignore` 项。已确认包括已处理和已记录不处理理由两种情况

不要把 Main Agent 的预期结论、已怀疑的问题或想让 Subagents 复述的答案传给 Subagents；需要让 Review 保持独立视角。

# 4. Review 输出格式

要求 Review Subagents 只输出 findings。每条 finding 使用以下字段：

| field | requirement |
| --- | --- |
| `finding` | 明确问题，不写泛泛建议 |
| `severity` | `blocking`、`non_blocking` 或 `ignore` |
| `evidence` | 文件、行号、代码事实、验收标准或验证结果 |
| `impact` | 说明会导致什么真实风险 |
| `suggestion` | 给出最小修复方向，不扩大 Issue 范围 |

没有发现问题时，输出 `无阻塞问题`，并简要说明 Review 覆盖范围。

# 5. Main Agent 复核

Main Agent 收到 Review 结果后必须逐条复核：

| decision | action |
| --- | --- |
| 采纳 | 修复问题，并说明对应 finding |
| 降级为非阻塞 | 记录降级理由，必要时处理或说明不处理 |
| 不采纳 | 记录事实依据，说明为什么不影响当前 Issue |

只有 `blocking` finding 必须进入修复循环。`non_blocking` finding 可以处理，也可以记录不处理理由。`ignore` finding 不修改代码，只保留判断依据。

# 6. 循环和停止条件

Review 循环流程：

1. Main Agent 完成实现和必要验证
2. 向 Review Subagents 提交最新 diff、验证结果和必要上下文
3. Review Subagents 返回 findings
4. Main Agent 逐条复核 findings
5. 判断通过条件或暂停条件
6. 修复被采纳的 `blocking` findings
7. 重新运行受影响验证
8. 回到步骤 2

通过条件全部满足时结束循环并进入 Issue DoD：

- 最近一轮 Review 或 Main Agent 复核结论没有 `blocking` finding
- 所有 `non_blocking` 和 `ignore` findings 已处理或记录理由
- 受影响验证已重新运行；无法运行时已说明原因和替代核对范围

满足任一暂停条件时立即暂停，不得进入 Issue DoD：

- 任一 `blocking` finding 确认无法在当前 Issue 范围内修复
- 已达到 3 轮 Review，仍有争议或反复未解决的 `blocking` findings
- 修复需要扩大 Issue 范围、改变需求、修改跨项目文件或引入新依赖

每轮修复后只要求复查最新 diff、已修复 finding 和可能新增的回归风险；不要让二次 Review 无限制扩散到无关范围。

# 7. 记录要求

Review 摘要写入对应 Issue 文档末尾，或写入 `.feat-tmp/issues/*-实现沉淀.md` 的验证 / Review 摘要部分；只记录结论摘要，不记录完整 Review 中间流水。

阶段推进说明或工作流产物中记录：

- Review 方式：Subagents Review、外部 Review、Main Agent 自审或跳过 Review
- Review 轮次和最近一轮结果
- 阻塞问题的修复结论
- 非阻塞建议的处理或不处理理由
- 跳过 Review 时的原因和风险
- 无法执行 Subagents Review、验证或修复时的原因
