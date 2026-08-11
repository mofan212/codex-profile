---
name: feat
description: 管理 feat 需求工作流，从需求草稿、澄清、Spec、Ticket 拆分到实现前检查、Review 门禁和最终归档。当用户通过 `$feat` 手动启动新需求或续跑既有工作流时，使用该 Skill。
---

# 1. 定位

本 Skill 是 AI Coding 主控工作流，不替代专用 Skill。收到新需求时创建草稿；收到既有工作流产物时识别阶段并续跑，同时执行门禁、决定需要配合使用的专用 Skill。

如果进入某个阶段时存在更专用的 Skill，主动声明并使用它；用户不需要再次点名底层 Skill。

# 2. 入口路由

只使用下表判定新建、续跑或补充上下文，按从上到下匹配。入口判定必须先于阶段状态机和 reference 读取。

| entry | condition | action | stop_when | forbidden |
| --- | --- | --- | --- | --- |
| `new_feat` | 用户描述新需求，且没有指定现成需求文档 | 进入 `draft_requirement`，读取 [references/draft-protocol.md](references/draft-protocol.md) 执行建档协议 | 需求草稿已创建；或无法确认文档目录、需求序号等建档必要信息 | 直接进入代码实现、需求澄清、Spec、Ticket 拆分 |
| `resume_feat` | 用户提供既有 `feat` 工作流产物目录、需求文档、Ticket 或 `.feat-tmp/` 产物，或要求继续这些产物 | 先定位并读取现有产物，按需求文档完整度、澄清结论、DoR / DoD、Ticket 列表、实现记录、Review 结果和归档状态判断当前阶段 | 无法确认任何可续跑产物位置 | 重新创建需求文档；猜测需求文档位置；跳过状态检测直接实现 |
| `missing_context` | 用户既没有描述新需求，也没有提供可续跑产物 | 🔴 CHECKPOINT：只问用户要新建什么需求，或既有需求文档、Ticket、`.feat-tmp/` 位于何处 | 用户提供新需求描述或可续跑产物位置前 | 猜测需求内容或产物位置；自动创建需求草稿 |

# 3. 前置检查

开始推进前按当前阶段检查必要条件。只检查当前阶段和下一步动作必需的 Skill；任一必需项不满足时中断该阶段，不要阻塞其他可独立完成的早期阶段。

判断 `mattpocock/skills` 工作流基础时，只看当前阶段需要的证据，不把固定目录、固定文件名或 `## Agent skills` 固定标题作为唯一通过条件。

| evidence | pass_when | fail_when |
| --- | --- | --- |
| Ticket tracker | 能确认 GitHub Issues、本地 `tickets.md`、用户提供的 Ticket 管理入口或等价承载位置 | 当前阶段需要拆分或续跑 Ticket，但完全无法确认 Ticket 承载位置 |
| Triage labels | 能确认标签词表、状态词表、优先级约定，或用户提供等价说明 | 当前阶段需要拆分或管理 Ticket，但没有任何分类、状态或优先级约定 |
| Domain docs | 能确认项目文档入口、领域上下文、`CONTEXT.md`、ADR 或等价资料入口 | 当前阶段需要澄清、拆分或实现前校验，但没有任何领域文档入口 |

通过条件：当前阶段需要的证据已确认，且缺失项不会阻塞当前动作。阻塞条件：当前阶段必须依赖某项证据，但该证据完全缺失且用户未提供替代产物。

| required_for_state | check_method | failure_action |
| --- | --- | --- |
| `clarify_requirement`、`refine_requirement`、`split_tickets` | 按上方证据表判断当前阶段所需的 Ticket tracker、Triage labels、Domain docs 或等价产物是否可确认 | 命中阻塞条件时提示用户运行 `/setup-matt-pocock-skills` 或提供等价产物；无法判断是否阻塞时只问一个最关键问题；非阻塞的路径或标题差异记录后继续 |
| `clarify_requirement` | 是否能调用 `grill-with-docs` 或读取其产物 | 无法调用时，提示用户运行 `/grill-with-docs`，或粘贴澄清结果供当前流程回写 |
| `refine_requirement` | 是否能调用 `to-spec` 或读取其产物 | 无法调用时，提示用户运行 `/to-spec`，或提供 Spec 整理结果供当前流程合并 |
| `split_tickets` | 是否能调用 `to-tickets` 或读取其产物 | 无法调用时，提示用户运行 `/to-tickets`，或提供拆分结果供当前流程补齐 Ticket DoR / DoD |
| `archive_ai_docs` | 当前会话是否可用 `maintain-ai-context-docs` | 提示用户添加或启用该 Skill |

`draft_requirement` 阶段只需要当前任务描述、[references/draft-protocol.md](references/draft-protocol.md) 和 [references/requirement-template.md](references/requirement-template.md)，不要因为外部工作流 Skill 不可用而阻塞草稿创建。

不要把具体实现类 Skill 作为前置条件。

# 4. 阶段状态机

续跑时先读取需求文档和 Ticket 列表，按需扫描 `.feat-tmp/tickets/` 的实现沉淀，结合 DoR / DoD、最近验证结果、Review 结果、归档状态和必要代码事实，按下表定位当前阶段。只执行匹配行的动作；`gate_id` 详见 §6 门禁表，`read_key` 详见 §6 引用文件路由。

| state_id | detect_by | required_input | action | gate_id | read_key | next_state |
| --- | --- | --- | --- | --- | --- | --- |
| `draft_requirement` | 入口匹配 `new_feat` | 当前任务描述 | 执行建档协议；草稿创建后立即暂停，只输出文档路径、当前阶段和下一步提示 | - | `draft_protocol`、`requirement_template` | `clarify_requirement` |
| `clarify_requirement` | 需求草稿存在但无澄清结论 | 需求文档、用户澄清上下文、必要领域文档 | 使用 `grill-with-docs` 澄清，并回写需求文档 | `clarification_written_back` | - | `refine_requirement` |
| `refine_requirement` | 有澄清结论但缺少目标、非目标、验收标准等 Feature DoR 必需项 | 初版需求文档、澄清对话 | 参考 `to-spec` 的 Spec 结构完善当前需求文档 | - | - | `feature_dor` |
| `feature_dor` | 需求文档内容完整，但未记录 Feature DoR 结果 | 完整需求文档 | 执行 Feature DoR；未通过时先补需求文档 | `feature_dor_after_spec` | `readiness_checklists` | `split_tickets` |
| `split_tickets` | 需求文档已记录 Feature DoR 通过，且未拆 Ticket | 通过 DoR 的需求文档 | 使用 `to-tickets` 按垂直切片拆分 Ticket | `vertical_slice`、`feature_size_review` | `readiness_checklists` | `ticket_readiness` |
| `ticket_readiness` | Ticket 已拆分但缺 DoR 或 DoD | Ticket 列表、来源需求文档 | 为每个 Ticket 补齐 Ticket DoR、Ticket DoD 和代码事实校验要求 | `ticket_dor_dod` | `readiness_checklists` | `implement_ticket` |
| `implement_ticket` | Ticket DoR 通过，待实现或正在实现 | 当前 Ticket、来源需求文档、验收标准、验证方式 | 按项目既有规则和入口渐进读取必要上下文；不存在结构化路由时使用普通文档和源码搜索；执行代码事实校验后再交接实现 | `code_fact_check` | `code_fact_check` | `review_loop` |
| `review_loop` | Ticket 已实现但 Review 未完成、正在修复循环，或存在待处理 Review findings | 当前 Ticket、实现结果、验证结果、Review 结果或 Review 策略选择 | 执行 Review 策略选择和修复循环 | `review_loop` | `review_loop`、`review_classification` | `ticket_done` |
| `ticket_done` | Review 门禁已通过，或用户明确跳过 Review 且已记录原因和风险，待执行 Ticket DoD | 当前 Ticket、实现结果、验证结果、Review 门禁结果 | 执行 Ticket DoD，并按需更新 `.feat-tmp/tickets/*-实现沉淀.md` | `ticket_dod` | `readiness_checklists`、`implementation_notes_template` | `archive_ai_docs` 或 `implement_ticket` |
| `archive_ai_docs` | 全部 Ticket DoD 通过 | 需求文档、全部 Ticket、`.feat-tmp/tickets/` 实现沉淀文件、代码事实 | 使用 `maintain-ai-context-docs` 生成或更新正式 AI 检索文档 | `archive_ai_docs` | `readiness_checklists` | 工作流完成 |

# 5. 文档权威边界

| document_type | authority_scope |
| --- | --- |
| 需求文档 | 目标、范围、非目标、业务规则、澄清结论、验收标准和验证建议 |
| `CONTEXT.md` | 稳定领域语言、核心模型、模块边界和长期系统事实 |
| ADR | 有长期影响的技术决策、被放弃方案和取舍理由 |
| Ticket | 一个可执行垂直切片的目标、范围、非范围、验收标准、验证方式、依赖、DoR 和 DoD |
| `.feat-tmp/` | `feat` 工作流临时工作区，只保存最终归档前的临时材料；归档为正式 AI 检索文档后，按安全审批和文件删除规则处理 |
| `.feat-tmp/tickets/` | `feat` 工作流临时实现沉淀目录，保存每个 Ticket 完成后的实现沉淀文件 |
| `*-实现沉淀.md` | 单个 Ticket 完成后的实现事实记录，位于 `.feat-tmp/tickets/` 目录下，供最终归并到 AI 检索文档 |
| AI 检索文档 | 最终已实现代码事实、入口、调用链、配置项、验证命令和排查关键词 |

不要把未实现设想写成 AI 检索文档事实。需求文档管「应该发生什么」，AI 检索文档管「代码现在怎么工作」。

# 6. 门禁与编排

| gate_id | condition | action | continue_when | forbidden |
| --- | --- | --- | --- | --- |
| `feature_dor_after_spec` | 需求文档已参考 `to-spec` 的 Spec 结构完善 | 执行 Feature DoR；未通过时先补需求文档 | Feature DoR 通过且结果已写回需求文档或工作流产物 | 未通过 Feature DoR 就拆 Ticket |
| `clarification_written_back` | 需求澄清完成 | 把澄清结论回写到需求文档；若 `grill-with-docs` 判断需要维护 `CONTEXT.md` 或 ADR，按其规则同步更新 | 澄清结论已回写；必要的 `CONTEXT.md` 或 ADR 同步已完成或记录跳过原因 | 只在对话中保留澄清结论 |
| `ticket_dor_dod` | Ticket 已拆分 | 为每个 Ticket 补齐 Ticket DoR 和 Ticket DoD | 每个 Ticket 的 DoR、DoD、依赖、验证方式和实现前校验要求明确 | 用未确认可开工的 Ticket 直接进入实现 |
| `code_fact_check` | Ticket 准备进入实现 | 读取 [references/code-fact-check.md](references/code-fact-check.md) 执行校验；命中阻塞级不一致时 🛑 STOP，先处理差异 | 无阻塞级不一致；非阻塞差异已记录影响和继续依据 | 未完成代码事实校验就改代码；发现阻塞级不一致仍继续实现 |
| `review_loop` | Ticket 实现完成，准备进入 Ticket DoD | 🔴 CHECKPOINT：读取 [references/review-loop.md](references/review-loop.md)，询问用户选择 Main Agent 自审、提供外部 Review 结果、跳过 Review 并记录原因，或在环境支持时明确选择 Subagents Review | 用户明确选择 Review 策略，且 Review 无阻塞级问题；如果选择跳过 Review，必须记录原因和风险 | 未经用户确认就跳过 Review；未经用户明确选择就启动 Subagents Review；把 Main Agent 自审伪装成独立 Review；未处理阻塞级问题就通过 Ticket DoD |
| `ticket_dod` | Review 门禁已通过，或用户明确跳过 Review 且已记录原因和风险 | 对照 [references/readiness-checklists.md](references/readiness-checklists.md) 执行 Ticket DoD；产生长期实现事实时按需更新 `.feat-tmp/tickets/*-实现沉淀.md` | Ticket DoD 通过；沉淀记录已按需处理，或完成说明写明 `无需更新 Ticket 实现沉淀` | 未完成 Ticket DoD 就进入下一 Ticket 或最终归档 |
| `archive_ai_docs` | 全部 Ticket DoD 通过 | 使用 `maintain-ai-context-docs` 生成或更新正式 AI 检索文档；确认覆盖 `.feat-tmp/` 中需长期保留的信息后再处理临时目录 | AI 检索文档反映最终已实现事实；`.feat-tmp/` 清理符合当前环境审批和删除规则 | 把未实现设想写入 AI 检索文档；未归档就清理 `.feat-tmp/` |
| `vertical_slice` | 拆分 Ticket | 按用户可感知或系统可验证的垂直切片拆分 | 每个 Ticket 都能独立验收，或依赖关系已明确记录 | 按 Controller、Service、Mapper、数据库表、测试等技术层拆分 |
| `feature_size_review` | `split_tickets` 后 Ticket 数量较多或依赖关系复杂 | 先复核 Feature 是否过大；能拆成多个独立 Feature 时优先拆分 Feature | Feature 边界已确认；需要拆分时先回到需求文档更新范围 | 用临时文件掩盖 Feature 边界过大 |
| `detailed_checklist` | 需要详细检查项 | 读取 [references/readiness-checklists.md](references/readiness-checklists.md) | 对应门禁检查项已逐项完成并记录结论 | 凭印象补门禁 |

按需读取以下引用文件。阶段状态机只引用 `read_key`，具体路径和跳过条件由下表维护：

| read_key | read | purpose | skip_when |
| --- | --- | --- | --- |
| `draft_protocol` | [references/draft-protocol.md](references/draft-protocol.md) | 按标准协议定位目录、命名需求目录、计算序号并创建需求草稿 | 已有可用需求草稿 |
| `requirement_template` | [references/requirement-template.md](references/requirement-template.md) | 生成可继续澄清的初版需求文档 | 已有可用需求草稿 |
| `readiness_checklists` | [references/readiness-checklists.md](references/readiness-checklists.md) | 使用 Feature DoR、Ticket DoR、Ticket DoD、垂直切片和归档检查项判断能否继续 | 当前阶段不涉及对应门禁检查 |
| `review_loop` | [references/review-loop.md](references/review-loop.md) | 执行 Review 策略选择、Subagents Review 协议和修复循环 | 当前 Ticket 不涉及代码、测试、配置、接口、数据结构、长期文档或 AI 检索事实 |
| `review_classification` | [references/readiness-checklists.md](references/readiness-checklists.md) | 收到外部 Review 结果或需要分类 Review 意见时，判断阻塞级问题、非阻塞建议和不处理项 | 当前阶段没有 Review 结果 |
| `code_fact_check` | [references/code-fact-check.md](references/code-fact-check.md) | 校验 Ticket 技术假设与当前代码事实的一致性，按阻塞/非阻塞分级处理 | 当前 Ticket 不涉及代码改动 |
| `implementation_notes_template` | [references/implementation-notes-template.md](references/implementation-notes-template.md) | 记录单个 Ticket 完成后的实现事实，供最终归档 | 没有产生需要沉淀的实现事实 |

默认只参考 `to-spec` 的 Spec 模板和整理方式完善当前需求文档，不执行 `to-spec` 的发布流程，不创建独立 Spec Ticket，也不创建第二份权威 Spec。只有用户明确要求发布或创建独立 Spec 时，才使用完整 `to-spec` 流程。

实现阶段不要硬编码具体语言、框架或实现类 Skill；具体实现方式由项目技术栈、用户偏好和当前任务决定。

专用 Skill 的规则优先处理具体执行细节；本 Skill 只保留阶段、门禁和交接约束。

# 7. 失败处理

| failure | first_action | fallback | stop_when |
| --- | --- | --- | --- |
| 续跑时找不到需求文档路径 | 🔴 CHECKPOINT：只问一个问题确认需求文档、Ticket 或 `.feat-tmp/` 位置 | 如果用户只提供 Ticket 或实现沉淀，先用其反查来源需求文档 | 无法确认来源需求文档时，不创建新需求文档 |
| 无法判断当前阶段 | 列出已读产物、匹配到的状态信号和缺失信息 | 只问一个最关键问题，例如需求文档路径、Ticket 编号或 Review 策略 | 阶段仍不明时，不跳到后续阶段 |
| 外部工作流 Skill 不可用 | 判断当前阶段是否必须依赖该 Skill 或其产物 | 允许用户粘贴对应产物，由当前流程只做回写、门禁检查或状态判断 | 必需产物缺失且无法替代时停止该阶段 |
| 需求文档与代码事实冲突 | 读取 [references/code-fact-check.md](references/code-fact-check.md)，按 `code_fact_check` 门禁处理 | 允许用户修正需求、调整 Ticket 或确认当前代码事实 | 阻塞级差异未解决时不进入实现 |
| Ticket 已实现但缺少验证记录 | 🔴 CHECKPOINT：要求补充最近验证命令、输出或可复现检查结果 | 无法运行时记录静态核对范围、未验证项和风险 | 没有任何验证依据时不关闭 Ticket |
| Review 存在阻塞级问题 | 🛑 STOP：先修复阻塞问题并重新验证 | 非阻塞建议可处理或记录不处理理由 | 阻塞级问题未处理时不进入 Ticket DoD |

# 8. 反例与黑名单

| anti_pattern | risk | canonical_rule | required_action |
| --- | --- | --- | --- |
| 没有 Feature DoR 就拆 Ticket | Ticket 目标、非目标、验收和依赖不稳定 | `feature_dor_after_spec` | 回到 `feature_dor` 阶段执行门禁 |
| 按 Controller、Service、Mapper、数据库表或测试层拆 Ticket | Ticket 不能独立交付或验收 | `vertical_slice` | 回到 `split_tickets` 阶段按垂直切片拆分 |
| 实现完成或测试通过后直接关闭 Ticket | 跳过 Review、验证复核、Ticket DoD 和实现沉淀 | `review_loop`、`ticket_dod` | 先进入 `review_loop`，通过后再执行 Ticket DoD |
| 把需求设想写入 AI 检索文档 | 长期检索文档污染代码事实 | `archive_ai_docs` | 只把已实现的代码事实归档到 AI 检索文档 |
| 用 `.feat-tmp/` 掩盖长期事实或未完成决策 | 后续会话无法判断权威来源 | `archive_ai_docs` | 阶段结论写回权威产物；最终归档后再按规则处理 `.feat-tmp/` |

# 9. 沉淀与报告

Ticket 完成后，如果新增或修改入口、调用链、配置项、数据结构、验证命令、排查关键词，或产生影响后续 AI 理解代码的实现事实，在需求文档同级目录下创建或更新 `.feat-tmp/tickets/<需求序号>-<Ticket序号>-<Ticket简述>-实现沉淀.md`；文件不存在时读取 [references/implementation-notes-template.md](references/implementation-notes-template.md) 后创建。没有产生需要沉淀的实现事实时，在完成说明中写明 `无需更新 Ticket 实现沉淀`。

全部 Ticket 完成后，`archive_ai_docs` 阶段的归档和 `.feat-tmp/` 清理规则详见 [references/readiness-checklists.md](references/readiness-checklists.md) 中的「`.feat-tmp/` 临时工作区归档规则」。当需求文档命名为 `<需求序号>-<需求简述>-需求文档.md` 时，最终 AI 检索文档由 `maintain-ai-context-docs` 默认生成或更新为相邻编号的 `<相邻序号>-<需求简述>-AI检索说明.md`，例如 `10-订单超时处理-需求文档.md` 对应 `11-订单超时处理-AI检索说明.md`。

阶段推进后的关键结论必须落到对应工作流产物中，使后续会话能从需求文档、Ticket、`.feat-tmp/` 或 AI 检索文档恢复当前阶段；不要只依赖聊天上下文保存阶段状态。

每次阶段推进后，按下表简短说明：

| field | requirement |
| --- | --- |
| `current_stage` | 当前阶段 |
| `documents` | 读取或更新了哪些文档 |
| `gate_result` | 是否通过门禁；未通过时说明阻塞原因 |
| `next_step` | 下一步动作，或需要用户确认的最关键问题 |
