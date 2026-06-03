---
name: feat
description: 管理 feat 需求工作流，从需求草稿、澄清、PRD、Issue 拆分到实现前检查、Review 门禁和最终归档。适用于用户明确提到 `feat` 或 `$feat` 并提出新需求，或基于既有 feat 需求目录、需求文档、Issue、`.feat-tmp` 产物继续推进下一步的场景。对未显式调用但接近完整工作流的模糊请求，先向用户确认。
---

# 1. 定位

本 Skill 是 AI Coding 主控工作流，不替代专用 Skill。用户点名 `feat`、`$feat` 新建需求工作流，或在已有 `feat` 工作流产物中要求继续下一步时，由本 Skill 识别阶段、执行门禁、决定需要配合使用的专用 Skill。

如果进入某个阶段时存在更专用的 Skill，主动声明并使用它；用户不需要再次点名底层 Skill。

不要因为用户只说「需要开发一个需求」「需要实现一个需求」「新增一个功能」就自动进入本 Skill；这些普通自然语言请求只有在用户显式提到 `feat` 或 `$feat` 时才新建 `feat` 工作流。如果用户表达接近完整需求建档、澄清、拆分或实现门禁流程，但没有明确 `feat` / `$feat`，只问一个问题确认，不要先创建需求文档。

# 2. 触发入口

| trigger | action | forbidden |
| --- | --- | --- |
| 用户明确说 `feat` 或 `$feat`，并描述一个新需求，但没有指定现成需求文档 | 作为唯一新建入口，进入 `draft_requirement`，读取 [references/draft-protocol.md](references/draft-protocol.md) 执行建档协议 | 直接进入代码实现、需求澄清、PRD、Issue 拆分 |
| 用户在已有 `feat` 需求目录、需求文档、Issue 或 `.feat-tmp/` 上下文中说「下一步」「继续 feat」「需求文档已完善」 | 作为续跑入口，先定位并读取现有产物，再按 §4 状态检测表判断当前阶段；没有可确认的需求文档路径时先询问路径 | 重新创建需求文档；猜测需求文档位置 |
| 用户表达接近完整需求建档、澄清、拆分或实现门禁流程，但没有明确 `feat` / `$feat` | 只问一个问题确认是否使用 `feat` 工作流 | 未确认就创建需求文档或进入后续阶段 |
| 用户只要求修 Bug、改一处代码、解释代码、跑测试或做 Review，且没有显式 `feat` 工作流语义 | 不自动进入 `feat` | 为小任务强行创建需求文档 |

# 3. 前置检查

开始推进前按当前阶段检查必要条件。只检查当前阶段和下一步动作必需的 Skill；任一必需项不满足时中断该阶段，不要阻塞其他可独立完成的早期阶段。

| required_for_state | check_method | failure_action |
| --- | --- | --- |
| `clarify_requirement`、`refine_requirement`、`split_issues` | 判断项目是否已具备 `mattpocock/skills` 工作流基础：查找 Agent 指南、项目文档入口或用户提供的初始化产物，只要能确认存在 Issue tracker、Triage labels、Domain docs、需求澄清或 Issue 拆分入口即可通过；不要把固定目录、固定文件名或 `## Agent skills` 固定标题作为唯一通过条件。 | 如果能够明显判断出未初始化，直接阻塞并提示用户运行 `/setup-matt-pocock-skills`；如果无法判断是否已初始化，先询问用户；非阻塞的路径或标题差异记录后继续。 |
| `clarify_requirement` | 是否能调用 `grill-with-docs` 或读取其产物 | 无法调用时，提示用户运行 `/grill-with-docs`，或粘贴澄清结果供当前流程回写 |
| `refine_requirement` | 是否能调用 `to-prd` 或读取其产物 | 无法调用时，提示用户运行 `/to-prd`，或提供 PRD 整理结果供当前流程合并 |
| `split_issues` | 是否能调用 `to-issues` 或读取其产物 | 无法调用时，提示用户运行 `/to-issues`，或提供拆分结果供当前流程补齐 Issue DoR / DoD |
| `implement_issue` | 当前会话是否可用 `load-project-context` | 提示用户添加或启用该 Skill |
| `archive_ai_docs` | 当前会话是否可用 `ai-retrieval-docs` | 提示用户添加或启用该 Skill |

`draft_requirement` 阶段只需要当前任务描述、[references/draft-protocol.md](references/draft-protocol.md) 和 [references/requirement-template.md](references/requirement-template.md)，不要因为外部工作流 Skill 不可用而阻塞草稿创建。

不要把具体实现类 Skill 作为前置条件。

# 4. 阶段状态机

续跑时先按状态检测表定位当前阶段。读取用户指定的需求文档、Issue、`.feat-tmp/` 或实现记录，按产物模式匹配当前阶段：

| state_id | detect_by | verify_action |
| --- | --- | --- |
| `draft_requirement` | 用户显式调用 `feat` 且无现成需求文档 | 确认用户意图和需求描述 |
| `clarify_requirement` | 需求草稿存在但无澄清结论 | 检查需求文档中是否有澄清结论章节 |
| `refine_requirement` | 有澄清结论但缺少目标、非目标、验收标准等 Feature DoR 必需项 | 对照 Feature DoR 检查项逐项判断 |
| `feature_dor` | 需求文档内容完整，但未记录 Feature DoR 结果 | 确认需求文档或工作流产物中无 DoR 通过记录 |
| `split_issues` | 需求文档已记录 Feature DoR 通过，且未拆 Issue | 确认存在 DoR 通过记录且无 Issue 列表 |
| `issue_readiness` | Issue 已拆分但缺 DoR 或 DoD | 检查每个 Issue 的 DoR、DoD 和校验要求 |
| `implement_issue` | Issue DoR 通过，待实现或正在实现 | 检查是否有代码改动或实现记录 |
| `review_loop` | Issue 已实现但 Review 未完成、正在修复循环，或存在待处理 Review findings | 检查 Review 方式、轮次、待处理 findings、跳过原因和验证记录 |
| `issue_done` | Review 门禁已通过或用户明确跳过 Review 且已记录原因和风险，待执行 Issue DoD | 每条验收标准都有对应实现证据 |
| `archive_ai_docs` | 全部 Issue DoD 通过 | 所有 Issue 已完成且沉淀记录已处理 |

只执行匹配行的动作，不要跳过门禁直接进入后续阶段。

阶段跳转关系：

| state_id | enter_condition | next_state |
| --- | --- | --- |
| `draft_requirement` | 显式调用 `feat` 并描述新需求，且没有现成需求文档 | `clarify_requirement` |
| `clarify_requirement` | 用户说「下一步」「继续 feat」「需求文档已完善」或明确要求澄清，且存在可读取的需求文档；无可确认路径时先询问文档位置 | `refine_requirement` |
| `refine_requirement` | 需求澄清完成但需求文档未完善 | `feature_dor` |
| `feature_dor` | 需求文档已完善但未拆 Issue | `split_issues` |
| `split_issues` | Feature DoR 通过 | `issue_readiness` |
| `issue_readiness` | Issue 已拆分但未确认可开工 | `implement_issue` |
| `implement_issue` | 某个 Issue 正在实现 | `review_loop` |
| `review_loop` | Issue 实现完成，待 Review 或选择 Review 策略 | `issue_done` |
| `issue_done` | Issue 完成 | `archive_ai_docs` 或 `implement_issue` |
| `archive_ai_docs` | 全部 Issue 完成 | 工作流完成 |

每个阶段的输入、动作和门禁输出：

| state_id | required_input | action | gate_or_output |
| --- | --- | --- | --- |
| `draft_requirement` | 当前任务描述 | 读取 [references/draft-protocol.md](references/draft-protocol.md) 执行建档协议 | 需求草稿已创建；立即暂停本轮，只输出文档路径、当前阶段和下一步提示，不自动进入澄清 |
| `clarify_requirement` | 需求文档、用户澄清上下文、必要领域文档 | 使用 `grill-with-docs` 澄清，并回写需求文档 | 关键歧义已消除；澄清结论已回写 |
| `refine_requirement` | 初版需求文档、澄清对话 | 参考 `to-prd` 的 PRD 结构完善当前需求文档 | 需求文档包含目标、范围、非目标、业务规则、验收和验证建议 |
| `feature_dor` | 完整需求文档、必要时 [references/readiness-checklists.md](references/readiness-checklists.md) | 执行 Feature DoR | Feature DoR 结果已写回需求文档或工作流产物；通过后进入 Issue 拆分，未通过时先补需求文档 |
| `split_issues` | 通过 DoR 的需求文档 | 使用 `to-issues` 按垂直切片拆分 Issue | Issue 按用户可感知或系统可验证行为拆分 |
| `issue_readiness` | Issue 列表、来源需求文档 | 为每个 Issue 补齐 Issue DoR、Issue DoD 和代码事实校验要求 | 每个 Issue 的 DoR、DoD、依赖、验证方式和实现前校验要求明确 |
| `implement_issue` | 当前 Issue、来源需求文档、验收标准、验证方式 | 使用 `load-project-context` 定位并渐进读取相关文档；读取 [references/code-fact-check.md](references/code-fact-check.md) 执行代码事实校验，再交接实现 | 明确最小改动范围、相关文档上下文，以及 Issue 假设与当前代码事实是否一致 |
| `review_loop` | 当前 Issue、实现结果、验证结果、Review 结果或 Review 策略选择 | 读取 [references/review-loop.md](references/review-loop.md) 执行 Review 修复循环；仅在当前会话支持且用户明确选择 Subagents Review 时启动 Review Subagents，否则提示用户选择 Main Agent 自审、提供外部 Review 结果或跳过 Review | Review 门禁通过，或用户明确跳过 Review 且已记录原因和风险 |
| `issue_done` | 当前 Issue、实现结果、验证结果、Review 门禁结果 | 执行 Issue DoD，并按需更新 `.feat-tmp/issues/*-实现沉淀.md` | Issue DoD 通过；沉淀记录已按需处理 |
| `archive_ai_docs` | 需求文档、全部 Issue、`.feat-tmp/issues/` 实现沉淀文件、代码事实 | 使用 `ai-retrieval-docs` 生成或更新正式 AI 检索文档 | AI 检索文档反映最终已实现事实 |

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

| gate_id | condition | action | forbidden |
| --- | --- | --- | --- |
| `feature_dor_after_prd` | 需求文档已参考 `to-prd` 的 PRD 结构完善 | 执行 Feature DoR；未通过时先补需求文档 | 未通过 Feature DoR 就拆 Issue |
| `clarification_written_back` | 需求澄清完成 | 把澄清结论回写到需求文档；若 `grill-with-docs` 判断需要维护 `CONTEXT.md` 或 ADR，按其规则同步更新 | 只在对话中保留澄清结论 |
| `issue_dor_dod` | Issue 已拆分 | 为每个 Issue 补齐 Issue DoR 和 Issue DoD | 用未确认可开工的 Issue 直接进入实现 |
| `code_fact_check` | Issue 准备进入实现 | 读取 [references/code-fact-check.md](references/code-fact-check.md) 执行校验；不一致处按阻塞/非阻塞分级处理 | 未完成代码事实校验就改代码；发现阻塞级不一致仍继续实现 |
| `review_loop` | Issue 实现完成，准备进入 Issue DoD | 读取 [references/review-loop.md](references/review-loop.md) 执行 Review 修复循环；仅在当前会话支持且用户明确选择 Subagents Review 时启动独立 Review Subagents；否则暂停说明，并询问用户选择 Main Agent 自审、提供外部 Review 结果或跳过 Review 并记录原因 | 未经用户确认就跳过 Review；未经用户明确选择就启动 Subagents Review；把 Main Agent 自审伪装成独立 Review；未处理阻塞级问题就通过 Issue DoD |
| `vertical_slice` | 拆分 Issue | 按用户可感知或系统可验证的垂直切片拆分 | 按 Controller、Service、Mapper、数据库表、测试等技术层拆分 |
| `feature_size_review` | `split_issues` 后 Issue 数量较多或依赖关系复杂 | 先复核 Feature 是否过大；能拆成多个独立 Feature 时优先拆分 Feature | 用临时文件掩盖 Feature 边界过大 |
| `detailed_checklist` | 需要详细检查项 | 读取 [references/readiness-checklists.md](references/readiness-checklists.md) | 凭印象补门禁 |

本 Skill 只显式关联工作流必要 Skill：

- 项目工作流初始化：必要时使用 `setup-matt-pocock-skills`。
- 需求澄清：使用 `grill-with-docs`。
- 需求文档完善：参考 `to-prd` 的 PRD 整理方式。
- Issue 拆分：使用 `to-issues`。
- 实现阶段上下文加载：使用 `load-project-context`。
- 最终 AI 检索文档归档：使用 `ai-retrieval-docs`。

按需读取以下引用文件：

| trigger | read | purpose | skip_when |
| --- | --- | --- | --- |
| 进入 `draft_requirement`，执行建档协议 | [references/draft-protocol.md](references/draft-protocol.md) | 按标准协议定位目录、命名需求目录、计算序号并创建需求草稿 | 已有可用需求草稿 |
| 创建轻量需求草稿 | [references/requirement-template.md](references/requirement-template.md) | 生成可继续澄清的初版需求文档 | 已有可用需求草稿 |
| 执行 Feature DoR、Issue DoR、Issue DoD 或垂直切片检查 | [references/readiness-checklists.md](references/readiness-checklists.md) | 使用标准门禁检查项判断能否拆分、开工或完成 | 当前阶段不涉及门禁检查 |
| 进入 `review_loop`，需要执行 Review 修复循环，或需要选择 Review 策略 | [references/review-loop.md](references/review-loop.md) | 在用户明确选择且环境支持时执行 Subagents Review；否则提示用户选择 Main Agent 自审、外部 Review 结果、跳过 Review | 当前 Issue 不涉及代码、测试、配置、接口、数据结构、长期文档或 AI 检索事实 |
| 收到外部 Review 结果，或需要对 Review 意见分类 | [references/readiness-checklists.md](references/readiness-checklists.md) | 使用 Review 结果处理规则判断阻塞级问题、非阻塞建议和不处理项 | 当前阶段没有 Review 结果 |
| 进入 `implement_issue`，执行 `code_fact_check` 门禁 | [references/code-fact-check.md](references/code-fact-check.md) | 校验 Issue 技术假设与当前代码事实的一致性，按阻塞/非阻塞分级处理 | 当前 Issue 不涉及代码改动 |
| Issue 完成且需要创建 `.feat-tmp/issues/*-实现沉淀.md` | [references/implementation-notes-template.md](references/implementation-notes-template.md) | 记录单个 Issue 已完成的实现事实，供最终归档 | 没有产生需要沉淀的实现事实 |

默认只参考 `to-prd` 的 PRD 模板和整理方式完善当前需求文档，不执行 `to-prd` 的发布流程，不创建独立 PRD Issue，也不创建第二份权威 PRD。只有用户明确要求发布或创建独立 PRD 时，才使用完整 `to-prd` 流程。

实现阶段不要硬编码具体语言、框架或实现类 Skill；具体实现方式由项目技术栈、用户偏好和当前任务决定。

专用 Skill 的规则优先处理具体执行细节；本 Skill 只保留阶段、门禁和交接约束。

# 7. 沉淀与报告

Issue 完成后，如果新增或修改入口、调用链、配置项、数据结构、验证命令、排查关键词，或产生影响后续 AI 理解代码的实现事实，在需求文档同级目录下创建或更新 `.feat-tmp/issues/<需求序号>-<Issue序号>-<Issue简述>-实现沉淀.md`；文件不存在时读取 [references/implementation-notes-template.md](references/implementation-notes-template.md) 后创建。没有产生需要沉淀的实现事实时，在完成说明中写明 `无需更新 Issue 实现沉淀`。

全部 Issue 完成后，`archive_ai_docs` 阶段的归档和 `.feat-tmp/` 清理规则详见 [references/readiness-checklists.md](references/readiness-checklists.md) 中的「`.feat-tmp/` 临时工作区归档规则」。当需求文档命名为 `<需求序号>-<需求简述>-需求文档.md` 时，最终 AI 检索文档由 `ai-retrieval-docs` 默认生成或更新为相邻编号的 `<相邻序号>-<需求简述>-AI检索说明.md`，例如 `10-订单超时处理-需求文档.md` 对应 `11-订单超时处理-AI检索说明.md`。

Review 修复循环详见 [references/review-loop.md](references/review-loop.md)。Review 分类标准和处理规则详见 [references/readiness-checklists.md](references/readiness-checklists.md) 中的「Review 结果处理规则」。Issue DoD 要求最近一轮 Review 没有阻塞级问题且非阻塞建议已处理或已有明确不处理理由；用户明确跳过 Review 时，必须记录跳过原因和风险，且不能伪装成独立 Review 或无阻塞 Review。

阶段推进后的关键结论必须落到对应工作流产物中，使后续会话能从需求文档、Issue、`.feat-tmp/` 或 AI 检索文档恢复当前阶段；不要只依赖聊天上下文保存阶段状态。

每次阶段推进后，按下表简短说明：

| field | requirement |
| --- | --- |
| `current_stage` | 当前阶段 |
| `documents` | 读取或更新了哪些文档 |
| `gate_result` | 是否通过门禁；未通过时说明阻塞原因 |
| `next_step` | 下一步动作，或需要用户确认的最关键问题 |
