---
name: feat
description: 管理 feat 需求工作流，从需求草稿、澄清、PRD、Issue 拆分到实现前检查、Review 门禁和最终归档。当用户明确提到 `feat` 或 `$feat` 并提出新需求，或基于既有 feat 工作流产物目录、需求文档、Issue、`.feat-tmp` 产物继续推进下一步时，使用该 Skill。对未显式调用但接近完整工作流的模糊请求，先向用户确认。
---

# 1. 定位

本 Skill 是 AI Coding 主控工作流，不替代专用 Skill。用户点名 `feat`、`$feat` 新建需求工作流，或在已有 `feat` 工作流产物中要求继续下一步时，由本 Skill 识别阶段、执行门禁、决定需要配合使用的专用 Skill。

如果进入某个阶段时存在更专用的 Skill，主动声明并使用它；用户不需要再次点名底层 Skill。

不要因为用户只说「需要开发一个需求」「需要实现一个需求」「新增一个功能」就自动进入本 Skill；这些普通自然语言请求只有在用户显式提到 `feat` 或 `$feat` 时才新建 `feat` 工作流。如果用户表达接近完整需求建档、澄清、拆分或实现门禁流程，但没有明确 `feat` / `$feat`，只问一个问题确认，不要先创建需求文档。

# 2. 触发入口

入口判定只使用下表，按从上到下匹配。入口判定必须先于阶段状态机和 reference 读取。判断是否显式调用 `feat` / `$feat` 时，只看用户原始请求；系统、测试、调试或外层编排要求读取本 Skill，不算用户显式调用。

| entry | condition | action | stop_when | forbidden |
| --- | --- | --- | --- | --- |
| `explicit_new_feat` | 用户明确说 `feat` 或 `$feat`，并描述新需求，且没有指定现成需求文档 | 进入 `draft_requirement`，读取 [references/draft-protocol.md](references/draft-protocol.md) 执行建档协议 | 需求草稿已创建；或无法确认文档目录、需求序号等建档必要信息 | 直接进入代码实现、需求澄清、PRD、Issue 拆分 |
| `explicit_resume_feat` | 用户提供既有 `feat` 工作流产物目录、需求文档、Issue 或 `.feat-tmp/` 产物，或在这些上下文中说「下一步」「继续 feat」「需求文档已完善」 | 先定位并读取现有产物，按需求文档完整度、澄清结论、DoR / DoD、Issue 列表、实现记录、Review 结果和归档状态判断当前阶段 | 无法确认任何可续跑产物位置 | 重新创建需求文档；猜测需求文档位置；跳过状态检测直接实现 |
| `implicit_workflow_request` | 用户没有明确 `feat` / `$feat`，也没有提供既有 `feat` 产物，但要求完整需求流程、建档、澄清、拆 Issue 或实现门禁 | 🔴 CHECKPOINT：只问「是否启用 feat 工作流？」 | 用户确认启用前 | 读取建档 reference；命名需求目录；创建需求草稿；标记为 `draft_requirement` |
| `ordinary_task` | 用户只是要求开发、修 Bug、解释、测试、Review 或局部实现 | 不进入本 Skill 后续流程 | 无 | 为小任务强行创建需求文档或要求用户走完整流程 |

# 3. 前置检查

开始推进前按当前阶段检查必要条件。只检查当前阶段和下一步动作必需的 Skill；任一必需项不满足时中断该阶段，不要阻塞其他可独立完成的早期阶段。

判断 `mattpocock/skills` 工作流基础时，只看当前阶段需要的证据，不把固定目录、固定文件名或 `## Agent skills` 固定标题作为唯一通过条件。

| evidence | pass_when | fail_when |
| --- | --- | --- |
| Issue tracker | 能确认 GitHub Issues、本地 Issue 文档目录、用户提供的 Issue 管理入口或等价承载位置 | 当前阶段需要拆分或续跑 Issue，但完全无法确认 Issue 承载位置 |
| Triage labels | 能确认标签词表、状态词表、优先级约定，或用户提供等价说明 | 当前阶段需要拆分或管理 Issue，但没有任何分类、状态或优先级约定 |
| Domain docs | 能确认项目文档入口、领域上下文、`CONTEXT.md`、ADR 或等价资料入口 | 当前阶段需要澄清、拆分或实现前校验，但没有任何领域文档入口 |

通过条件：当前阶段需要的证据已确认，且缺失项不会阻塞当前动作。阻塞条件：当前阶段必须依赖某项证据，但该证据完全缺失且用户未提供替代产物。

| required_for_state | check_method | failure_action |
| --- | --- | --- |
| `clarify_requirement`、`refine_requirement`、`split_issues` | 按上方证据表判断当前阶段所需的 Issue tracker、Triage labels、Domain docs 或等价产物是否可确认 | 命中阻塞条件时提示用户运行 `/setup-matt-pocock-skills` 或提供等价产物；无法判断是否阻塞时只问一个最关键问题；非阻塞的路径或标题差异记录后继续 |
| `clarify_requirement` | 是否能调用 `grill-with-docs` 或读取其产物 | 无法调用时，提示用户运行 `/grill-with-docs`，或粘贴澄清结果供当前流程回写 |
| `refine_requirement` | 是否能调用 `to-prd` 或读取其产物 | 无法调用时，提示用户运行 `/to-prd`，或提供 PRD 整理结果供当前流程合并 |
| `split_issues` | 是否能调用 `to-issues` 或读取其产物 | 无法调用时，提示用户运行 `/to-issues`，或提供拆分结果供当前流程补齐 Issue DoR / DoD |
| `implement_issue` | 当前会话是否可用 `load-project-context` | 提示用户添加或启用该 Skill |
| `archive_ai_docs` | 当前会话是否可用 `ai-retrieval-docs` | 提示用户添加或启用该 Skill |

`draft_requirement` 阶段只需要当前任务描述、[references/draft-protocol.md](references/draft-protocol.md) 和 [references/requirement-template.md](references/requirement-template.md)，不要因为外部工作流 Skill 不可用而阻塞草稿创建。

不要把具体实现类 Skill 作为前置条件。

# 4. 阶段状态机

续跑时读取用户指定的需求文档、Issue、`.feat-tmp/` 或实现记录，按下表定位当前阶段。只执行匹配行的动作；`gate_id` 详见 §6 门禁表，`read_key` 详见 §6 引用文件路由。

| state_id | detect_by | required_input | action | gate_id | read_key | next_state |
| --- | --- | --- | --- | --- | --- | --- |
| `draft_requirement` | 用户显式调用 `feat` 且无现成需求文档 | 当前任务描述 | 执行建档协议；草稿创建后立即暂停，只输出文档路径、当前阶段和下一步提示 | - | `draft_protocol`、`requirement_template` | `clarify_requirement` |
| `clarify_requirement` | 需求草稿存在但无澄清结论 | 需求文档、用户澄清上下文、必要领域文档 | 使用 `grill-with-docs` 澄清，并回写需求文档 | `clarification_written_back` | - | `refine_requirement` |
| `refine_requirement` | 有澄清结论但缺少目标、非目标、验收标准等 Feature DoR 必需项 | 初版需求文档、澄清对话 | 参考 `to-prd` 的 PRD 结构完善当前需求文档 | - | - | `feature_dor` |
| `feature_dor` | 需求文档内容完整，但未记录 Feature DoR 结果 | 完整需求文档 | 执行 Feature DoR；未通过时先补需求文档 | `feature_dor_after_prd` | `readiness_checklists` | `split_issues` |
| `split_issues` | 需求文档已记录 Feature DoR 通过，且未拆 Issue | 通过 DoR 的需求文档 | 使用 `to-issues` 按垂直切片拆分 Issue | `vertical_slice`、`feature_size_review` | `readiness_checklists` | `issue_readiness` |
| `issue_readiness` | Issue 已拆分但缺 DoR 或 DoD | Issue 列表、来源需求文档 | 为每个 Issue 补齐 Issue DoR、Issue DoD 和代码事实校验要求 | `issue_dor_dod` | `readiness_checklists` | `implement_issue` |
| `implement_issue` | Issue DoR 通过，待实现或正在实现 | 当前 Issue、来源需求文档、验收标准、验证方式 | 使用 `load-project-context` 渐进读取上下文并执行代码事实校验，再交接实现 | `code_fact_check` | `code_fact_check` | `review_loop` |
| `review_loop` | Issue 已实现但 Review 未完成、正在修复循环，或存在待处理 Review findings | 当前 Issue、实现结果、验证结果、Review 结果或 Review 策略选择 | 执行 Review 策略选择和修复循环 | `review_loop` | `review_loop`、`review_classification` | `issue_done` |
| `issue_done` | Review 门禁已通过，或用户明确跳过 Review 且已记录原因和风险，待执行 Issue DoD | 当前 Issue、实现结果、验证结果、Review 门禁结果 | 执行 Issue DoD，并按需更新 `.feat-tmp/issues/*-实现沉淀.md` | `issue_dod` | `readiness_checklists`、`implementation_notes_template` | `archive_ai_docs` 或 `implement_issue` |
| `archive_ai_docs` | 全部 Issue DoD 通过 | 需求文档、全部 Issue、`.feat-tmp/issues/` 实现沉淀文件、代码事实 | 使用 `ai-retrieval-docs` 生成或更新正式 AI 检索文档 | `archive_ai_docs` | `readiness_checklists` | 工作流完成 |

如果无法判断阶段，先列出已知事实和缺失信息，只问一个最关键问题。

续跑时先读取需求文档和 Issue 列表，按需扫描 `.feat-tmp/issues/` 已有实现沉淀；结合 Issue DoR / DoD、最近验证结果和必要代码事实判断当前阶段与下一执行项。

# 5. 文档权威边界

| document_type | authority_scope |
| --- | --- |
| 需求文档 | 目标、范围、非目标、业务规则、澄清结论、验收标准和验证建议 |
| `CONTEXT.md` | 稳定领域语言、核心模型、模块边界和长期系统事实 |
| ADR | 有长期影响的技术决策、被放弃方案和取舍理由 |
| Issue | 一个可执行垂直切片的目标、范围、非范围、验收标准、验证方式、依赖、DoR 和 DoD |
| `.feat-tmp/` | `feat` 工作流临时工作区，只保存最终归档前的临时材料；归档为正式 AI 检索文档后，按安全审批和文件删除规则处理 |
| `.feat-tmp/issues/` | `feat` 工作流临时实现沉淀目录，保存每个 Issue 完成后的实现沉淀文件 |
| `*-实现沉淀.md` | 单个 Issue 完成后的实现事实记录，位于 `.feat-tmp/issues/` 目录下，供最终归并到 AI 检索文档 |
| AI 检索文档 | 最终已实现代码事实、入口、调用链、配置项、验证命令和排查关键词 |

不要把未实现设想写成 AI 检索文档事实。需求文档管「应该发生什么」，AI 检索文档管「代码现在怎么工作」。

# 6. 门禁与编排

| gate_id | condition | action | continue_when | forbidden |
| --- | --- | --- | --- | --- |
| `feature_dor_after_prd` | 需求文档已参考 `to-prd` 的 PRD 结构完善 | 执行 Feature DoR；未通过时先补需求文档 | Feature DoR 通过且结果已写回需求文档或工作流产物 | 未通过 Feature DoR 就拆 Issue |
| `clarification_written_back` | 需求澄清完成 | 把澄清结论回写到需求文档；若 `grill-with-docs` 判断需要维护 `CONTEXT.md` 或 ADR，按其规则同步更新 | 澄清结论已回写；必要的 `CONTEXT.md` 或 ADR 同步已完成或记录跳过原因 | 只在对话中保留澄清结论 |
| `issue_dor_dod` | Issue 已拆分 | 为每个 Issue 补齐 Issue DoR 和 Issue DoD | 每个 Issue 的 DoR、DoD、依赖、验证方式和实现前校验要求明确 | 用未确认可开工的 Issue 直接进入实现 |
| `code_fact_check` | Issue 准备进入实现 | 读取 [references/code-fact-check.md](references/code-fact-check.md) 执行校验；命中阻塞级不一致时 🛑 STOP，先处理差异 | 无阻塞级不一致；非阻塞差异已记录影响和继续依据 | 未完成代码事实校验就改代码；发现阻塞级不一致仍继续实现 |
| `review_loop` | Issue 实现完成，准备进入 Issue DoD | 🔴 CHECKPOINT：读取 [references/review-loop.md](references/review-loop.md)，询问用户选择 Main Agent 自审、提供外部 Review 结果、跳过 Review 并记录原因，或在环境支持时明确选择 Subagents Review | 用户明确选择 Review 策略，且 Review 无阻塞级问题；如果选择跳过 Review，必须记录原因和风险 | 未经用户确认就跳过 Review；未经用户明确选择就启动 Subagents Review；把 Main Agent 自审伪装成独立 Review；未处理阻塞级问题就通过 Issue DoD |
| `issue_dod` | Review 门禁已通过，或用户明确跳过 Review 且已记录原因和风险 | 对照 [references/readiness-checklists.md](references/readiness-checklists.md) 执行 Issue DoD；产生长期实现事实时按需更新 `.feat-tmp/issues/*-实现沉淀.md` | Issue DoD 通过；沉淀记录已按需处理，或完成说明写明 `无需更新 Issue 实现沉淀` | 未完成 Issue DoD 就进入下一 Issue 或最终归档 |
| `archive_ai_docs` | 全部 Issue DoD 通过 | 使用 `ai-retrieval-docs` 生成或更新正式 AI 检索文档；确认覆盖 `.feat-tmp/` 中需长期保留的信息后再处理临时目录 | AI 检索文档反映最终已实现事实；`.feat-tmp/` 清理符合当前环境审批和删除规则 | 把未实现设想写入 AI 检索文档；未归档就清理 `.feat-tmp/` |
| `vertical_slice` | 拆分 Issue | 按用户可感知或系统可验证的垂直切片拆分 | 每个 Issue 都能独立验收，或依赖关系已明确记录 | 按 Controller、Service、Mapper、数据库表、测试等技术层拆分 |
| `feature_size_review` | `split_issues` 后 Issue 数量较多或依赖关系复杂 | 先复核 Feature 是否过大；能拆成多个独立 Feature 时优先拆分 Feature | Feature 边界已确认；需要拆分时先回到需求文档更新范围 | 用临时文件掩盖 Feature 边界过大 |
| `detailed_checklist` | 需要详细检查项 | 读取 [references/readiness-checklists.md](references/readiness-checklists.md) | 对应门禁检查项已逐项完成并记录结论 | 凭印象补门禁 |

本 Skill 只显式关联工作流必要 Skill：

- 项目工作流初始化：必要时使用 `setup-matt-pocock-skills`
- 需求澄清：使用 `grill-with-docs`
- 需求文档完善：参考 `to-prd` 的 PRD 整理方式
- Issue 拆分：使用 `to-issues`
- 实现阶段上下文加载：使用 `load-project-context`
- 最终 AI 检索文档归档：使用 `ai-retrieval-docs`

按需读取以下引用文件。阶段状态机只引用 `read_key`，具体路径和跳过条件由下表维护：

| read_key | read | purpose | skip_when |
| --- | --- | --- | --- |
| `draft_protocol` | [references/draft-protocol.md](references/draft-protocol.md) | 按标准协议定位目录、命名需求目录、计算序号并创建需求草稿 | 已有可用需求草稿 |
| `requirement_template` | [references/requirement-template.md](references/requirement-template.md) | 生成可继续澄清的初版需求文档 | 已有可用需求草稿 |
| `readiness_checklists` | [references/readiness-checklists.md](references/readiness-checklists.md) | 使用 Feature DoR、Issue DoR、Issue DoD、垂直切片和归档检查项判断能否继续 | 当前阶段不涉及对应门禁检查 |
| `review_loop` | [references/review-loop.md](references/review-loop.md) | 执行 Review 策略选择、Subagents Review 协议和修复循环 | 当前 Issue 不涉及代码、测试、配置、接口、数据结构、长期文档或 AI 检索事实 |
| `review_classification` | [references/readiness-checklists.md](references/readiness-checklists.md) | 收到外部 Review 结果或需要分类 Review 意见时，判断阻塞级问题、非阻塞建议和不处理项 | 当前阶段没有 Review 结果 |
| `code_fact_check` | [references/code-fact-check.md](references/code-fact-check.md) | 校验 Issue 技术假设与当前代码事实的一致性，按阻塞/非阻塞分级处理 | 当前 Issue 不涉及代码改动 |
| `implementation_notes_template` | [references/implementation-notes-template.md](references/implementation-notes-template.md) | 记录单个 Issue 完成后的实现事实，供最终归档 | 没有产生需要沉淀的实现事实 |

默认只参考 `to-prd` 的 PRD 模板和整理方式完善当前需求文档，不执行 `to-prd` 的发布流程，不创建独立 PRD Issue，也不创建第二份权威 PRD。只有用户明确要求发布或创建独立 PRD 时，才使用完整 `to-prd` 流程。

实现阶段不要硬编码具体语言、框架或实现类 Skill；具体实现方式由项目技术栈、用户偏好和当前任务决定。

专用 Skill 的规则优先处理具体执行细节；本 Skill 只保留阶段、门禁和交接约束。

# 7. 失败处理

| failure | first_action | fallback | stop_when |
| --- | --- | --- | --- |
| 续跑时找不到需求文档路径 | 🔴 CHECKPOINT：只问一个问题确认需求文档、Issue 或 `.feat-tmp/` 位置 | 如果用户只提供 Issue 或实现沉淀，先用其反查来源需求文档 | 无法确认来源需求文档时，不创建新需求文档 |
| 未显式调用 `feat` / `$feat`，但请求接近完整需求流程 | 🔴 CHECKPOINT：只问是否启用 `feat` 工作流 | 用户确认后再进入 `draft_requirement` 或续跑状态检测 | 未确认前不读取 [references/draft-protocol.md](references/draft-protocol.md) 或创建需求草稿 |
| 无法判断当前阶段 | 列出已读产物、匹配到的状态信号和缺失信息 | 只问一个最关键问题，例如需求文档路径、Issue 编号或 Review 策略 | 阶段仍不明时，不跳到后续阶段 |
| 外部工作流 Skill 不可用 | 判断当前阶段是否必须依赖该 Skill 或其产物 | 允许用户粘贴对应产物，由当前流程只做回写、门禁检查或状态判断 | 必需产物缺失且无法替代时停止该阶段 |
| 需求文档与代码事实冲突 | 读取 [references/code-fact-check.md](references/code-fact-check.md)，按 `code_fact_check` 门禁处理 | 允许用户修正需求、调整 Issue 或确认当前代码事实 | 阻塞级差异未解决时不进入实现 |
| Issue 已实现但缺少验证记录 | 🔴 CHECKPOINT：要求补充最近验证命令、输出或可复现检查结果 | 无法运行时记录静态核对范围、未验证项和风险 | 没有任何验证依据时不关闭 Issue |
| Review 存在阻塞级问题 | 🛑 STOP：先修复阻塞问题并重新验证 | 非阻塞建议可处理或记录不处理理由 | 阻塞级问题未处理时不进入 Issue DoD |

# 8. 反例与黑名单

| anti_pattern | risk | canonical_rule | required_action |
| --- | --- | --- | --- |
| 用户只说「开发一个需求」就创建 `feat` 文档 | 把普通开发任务强行流程化，增加无关产物 | `explicit_new_feat` | 回到 §2 入口判定；未显式调用 `feat` / `$feat` 时不新建工作流 |
| 没有 Feature DoR 就拆 Issue | Issue 目标、非目标、验收和依赖不稳定 | `feature_dor_after_prd` | 回到 `feature_dor` 阶段执行门禁 |
| 按 Controller、Service、Mapper、数据库表或测试层拆 Issue | Issue 不能独立交付或验收 | `vertical_slice` | 回到 `split_issues` 阶段按垂直切片拆分 |
| 实现完成或测试通过后直接关闭 Issue | 跳过 Review、验证复核、Issue DoD 和实现沉淀 | `review_loop`、`issue_dod` | 先进入 `review_loop`，通过后再执行 Issue DoD |
| 把需求设想写入 AI 检索文档 | 长期检索文档污染代码事实 | `archive_ai_docs` | 只把已实现的代码事实归档到 AI 检索文档 |
| 用 `.feat-tmp/` 掩盖长期事实或未完成决策 | 后续会话无法判断权威来源 | `archive_ai_docs` | 阶段结论写回权威产物；最终归档后再按规则处理 `.feat-tmp/` |

# 9. 沉淀与报告

Issue 完成后，如果新增或修改入口、调用链、配置项、数据结构、验证命令、排查关键词，或产生影响后续 AI 理解代码的实现事实，在需求文档同级目录下创建或更新 `.feat-tmp/issues/<需求序号>-<Issue序号>-<Issue简述>-实现沉淀.md`；文件不存在时读取 [references/implementation-notes-template.md](references/implementation-notes-template.md) 后创建。没有产生需要沉淀的实现事实时，在完成说明中写明 `无需更新 Issue 实现沉淀`。

全部 Issue 完成后，`archive_ai_docs` 阶段的归档和 `.feat-tmp/` 清理规则详见 [references/readiness-checklists.md](references/readiness-checklists.md) 中的「`.feat-tmp/` 临时工作区归档规则」。当需求文档命名为 `<需求序号>-<需求简述>-需求文档.md` 时，最终 AI 检索文档由 `ai-retrieval-docs` 默认生成或更新为相邻编号的 `<相邻序号>-<需求简述>-AI检索说明.md`，例如 `10-订单超时处理-需求文档.md` 对应 `11-订单超时处理-AI检索说明.md`。

Review 修复循环由 `review_loop` 门禁和 `review_loop` / `review_classification` 引用文件维护；Issue DoD 由 `issue_dod` 门禁维护。不要在沉淀与报告阶段重新解释 Review 策略或 DoD 细节。

阶段推进后的关键结论必须落到对应工作流产物中，使后续会话能从需求文档、Issue、`.feat-tmp/` 或 AI 检索文档恢复当前阶段；不要只依赖聊天上下文保存阶段状态。

每次阶段推进后，按下表简短说明：

| field | requirement |
| --- | --- |
| `current_stage` | 当前阶段 |
| `documents` | 读取或更新了哪些文档 |
| `gate_result` | 是否通过门禁；未通过时说明阻塞原因 |
| `next_step` | 下一步动作，或需要用户确认的最关键问题 |
