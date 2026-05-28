---
name: feat
description: Orchestrate an AI coding feature workflow from lightweight requirement draft creation, clarification, PRD refinement, Feature DoR, vertical issue slicing, Issue DoR/DoD, pre-implementation code fact checks, implementation handoff, implementation notes, review result tracking, and final AI retrieval documentation. Use only when the user explicitly mentions feat, $feat, or feature workflow; asks to continue the next step in an existing feat workflow; or works in a requirement directory that already contains feat workflow artifacts and asks to clarify, refine, split, implement, review, complete, or archive that workflow.
---

# 1. 定位

本 Skill 是 AI Coding 主控工作流，不替代专用 Skill。用户点名 `feat`、明确提到 feature workflow，或在已有 `feat` 工作流中要求继续下一步时，由本 Skill 识别阶段、执行门禁、决定需要配合使用的专用 Skill。

如果进入某个阶段时存在更专用的 Skill，主动声明并使用它；用户不需要再次点名底层 Skill。

# 2. 前置检查

开始推进前按当前阶段检查必要条件。只检查当前阶段和下一步动作必需的 Skill；任一必需项不满足时中断该阶段，不要阻塞其他可独立完成的早期阶段。

| required_for_state | check_method | failure_action |
| --- | --- | --- |
| `clarify_requirement`、`refine_requirement`、`split_issues` | 判断项目是否已具备 `mattpocock/skills` 工作流基础：查找 Agent 指南、项目文档入口或用户提供的初始化产物，只要能确认存在 Issue tracker、Triage labels、Domain docs、需求澄清或 Issue 拆分入口即可通过；不要把固定目录、固定文件名或 `## Agent skills` 固定标题作为唯一通过条件。 | 如果能够明显判断出未初始化，直接阻塞并提示用户运行 `/setup-matt-pocock-skills`；如果无法判断是否已初始化，先询问用户；非阻塞的路径或标题差异记录后继续。 |
| `clarify_requirement` | 是否能调用 `grill-with-docs` 或读取其产物 | 无法调用时，提示用户运行 `/grill-with-docs`，或粘贴澄清结果供当前流程回写 |
| `refine_requirement` | 是否能调用 `to-prd` 或读取其产物 | 无法调用时，提示用户运行 `/to-prd`，或提供 PRD 整理结果供当前流程合并 |
| `split_issues` | 是否能调用 `to-issues` 或读取其产物 | 无法调用时，提示用户运行 `/to-issues`，或提供拆分结果供当前流程补齐 Issue DoR / DoD |
| `implement_issue` | 当前会话是否可用 `read-project-docs` | 提示用户添加或启用该 Skill |
| `archive_ai_docs` | 当前会话是否可用 `ai-retrieval-docs` | 提示用户添加或启用该 Skill |

`draft_requirement` 阶段只需要当前任务描述和 [references/requirement-template.md](references/requirement-template.md)，不要因为外部工作流 Skill 不可用而阻塞草稿创建。

不要把具体实现类 Skill 作为前置条件。

# 3. 阶段状态机

先读取用户指定的需求文档、Issue、实现记录或当前任务描述，再按下表判断当前阶段。只执行匹配行的动作，不要跳过门禁直接进入后续阶段。

| state_id | enter_condition | next_state |
| --- | --- | --- |
| `draft_requirement` | 没有需求目录或需求文档 | `clarify_requirement` |
| `clarify_requirement` | 需求文档仍有关键歧义 | `refine_requirement` |
| `refine_requirement` | 需求澄清完成但需求文档未完善 | `feature_dor` |
| `feature_dor` | 需求文档已完善但未拆 Issue | `split_issues` |
| `split_issues` | Feature DoR 通过 | `issue_readiness` |
| `issue_readiness` | Issue 已拆分但未确认可开工 | `implement_issue` |
| `implement_issue` | 某个 Issue 正在实现 | `issue_done` |
| `issue_done` | Issue 完成 | `archive_ai_docs` 或 `implement_issue` |
| `archive_ai_docs` | 全部 Issue 完成 | 工作流完成 |

| state_id | required_input | action | gate_or_output |
| --- | --- | --- | --- |
| `draft_requirement` | 当前任务描述 | 创建轻量需求草稿，读取 [references/requirement-template.md](references/requirement-template.md) | 产出可继续澄清的需求草稿 |
| `clarify_requirement` | 需求文档、用户澄清上下文、必要领域文档 | 使用 `grill-with-docs` 澄清，并回写需求文档 | 关键歧义已消除；澄清结论已回写 |
| `refine_requirement` | 初版需求文档、澄清对话 | 参考 `to-prd` 的 PRD 结构完善当前需求文档 | 需求文档包含目标、范围、非目标、业务规则、验收和验证建议 |
| `feature_dor` | 完整需求文档、必要时 [references/readiness-checklists.md](references/readiness-checklists.md) | 执行 Feature DoR | Feature DoR 通过；未通过时先补需求文档 |
| `split_issues` | 通过 DoR 的需求文档 | 使用 `to-issues` 按垂直切片拆分 Issue | Issue 按用户可感知或系统可验证行为拆分 |
| `issue_readiness` | Issue 列表、来源需求文档 | 为每个 Issue 补齐 Issue DoR、Issue DoD 和代码事实校验要求 | 每个 Issue 的 DoR、DoD、依赖、验证方式和实现前校验要求明确 |
| `implement_issue` | 当前 Issue、来源需求文档、验收标准、验证方式 | 使用 `read-project-docs` 定位并渐进读取相关需求、上下文入口、AI 检索文档或实现记录；实现前执行代码事实校验，再交接实现 | 明确最小改动范围、相关文档上下文，以及 Issue 假设与当前代码事实是否一致 |
| `issue_done` | 当前 Issue、实现结果、验证结果、Review 结果 | 执行 Issue DoD，并按需更新 `.issue/*-实现沉淀.md` | Issue DoD 通过；沉淀记录已按需处理 |
| `archive_ai_docs` | 需求文档、全部 Issue、`.issue/` 实现沉淀文件、代码事实 | 使用 `ai-retrieval-docs` 生成或更新正式 AI 检索文档 | AI 检索文档反映最终已实现事实 |

如果无法判断阶段，先列出已知事实和缺失信息，只问一个最关键问题。

# 4. 文档权威边界

| document_type | authority_scope |
| --- | --- |
| 需求文档 | 目标、范围、非目标、业务规则、澄清结论、验收标准和验证建议 |
| `CONTEXT.md` | 稳定领域语言、核心模型、模块边界和长期系统事实 |
| ADR | 有长期影响的技术决策、被放弃方案和取舍理由 |
| Issue | 一个可执行垂直切片的目标、范围、非范围、验收标准、验证方式、依赖、DoR 和 DoD |
| `.issue/` | `feat` 工作流临时目录，保存每个 Issue 完成后的实现沉淀文件；归档为正式 AI 检索文档后，按安全审批和文件删除规则处理 |
| `*-实现沉淀.md` | 单个 Issue 完成后的实现事实记录，位于 `.issue/` 目录下，供最终归并到 AI 检索文档 |
| AI 检索文档 | 最终已实现代码事实、入口、调用链、配置项、验证命令和排查关键词 |

不要把未实现设想写成 AI 检索文档事实。需求文档管「应该发生什么」，AI 检索文档管「代码现在怎么工作」。

# 5. 门禁和 Skill 编排

| gate_id | condition | action | forbidden |
| --- | --- | --- | --- |
| `feature_dor_after_prd` | 需求文档已参考 `to-prd` 的 PRD 结构完善 | 执行 Feature DoR；未通过时先补需求文档 | 未通过 Feature DoR 就拆 Issue |
| `clarification_written_back` | 需求澄清完成 | 把澄清结论回写到需求文档；若 `grill-with-docs` 判断需要维护 `CONTEXT.md` 或 ADR，按其规则同步更新 | 只在对话中保留澄清结论 |
| `issue_dor_dod` | Issue 已拆分 | 为每个 Issue 补齐 Issue DoR 和 Issue DoD | 用未确认可开工的 Issue 直接进入实现 |
| `code_fact_check` | Issue 准备进入实现 | 对比 Issue / 需求文档中的技术假设与当前源码、测试、配置或调用入口；不一致处先记录并确认 | 未完成代码事实校验就改代码；发现阻塞级不一致仍继续实现 |
| `vertical_slice` | 拆分 Issue | 按用户可感知或系统可验证的垂直切片拆分 | 按 Controller、Service、Mapper、数据库表、测试等技术层拆分 |
| `detailed_checklist` | 需要详细检查项 | 读取 [references/readiness-checklists.md](references/readiness-checklists.md) | 凭印象补门禁 |

本 Skill 只显式关联工作流必要 Skill：

- 项目工作流初始化：必要时使用 `setup-matt-pocock-skills`。
- 需求澄清：使用 `grill-with-docs`。
- 需求文档完善：参考 `to-prd` 的 PRD 整理方式。
- Issue 拆分：使用 `to-issues`。
- 实现阶段文档定位：使用 `read-project-docs`。
- 最终 AI 检索文档归档：使用 `ai-retrieval-docs`。

按需读取以下引用文件：

| trigger | read | purpose | skip_when |
| --- | --- | --- | --- |
| 创建轻量需求草稿 | [references/requirement-template.md](references/requirement-template.md) | 生成可继续澄清的初版需求文档 | 已有可用需求草稿 |
| 执行 Feature DoR、Issue DoR、Issue DoD 或垂直切片检查 | [references/readiness-checklists.md](references/readiness-checklists.md) | 使用标准门禁检查项判断能否拆分、开工或完成 | 当前阶段不涉及门禁检查 |
| 收到外部 Review 结果，或需要对 Review 意见分类 | [references/readiness-checklists.md](references/readiness-checklists.md) | 使用 Review 结果处理规则判断阻塞级问题、非阻塞建议和不处理项 | 当前阶段没有 Review 结果 |
| Issue 完成且需要创建 `.issue/*-实现沉淀.md` | [references/implementation-notes-template.md](references/implementation-notes-template.md) | 记录单个 Issue 已完成的实现事实，供最终归档 | 没有产生需要沉淀的实现事实 |

默认只参考 `to-prd` 的 PRD 模板和整理方式完善当前需求文档，不执行 `to-prd` 的发布流程，不创建独立 PRD Issue，也不创建第二份权威 PRD。只有用户明确要求发布或创建独立 PRD 时，才使用完整 `to-prd` 流程。

实现前先明确当前 Issue、来源需求文档、验收标准、预期验证方式和最小改动范围，并使用 `read-project-docs` 定位、渐进读取当前 Issue 相关的需求文档、上下文入口、AI 检索文档或实现记录。

代码事实校验必须在改代码前完成：读取相关源码、测试、配置或调用入口，确认 Issue / 需求文档中的技术假设与当前代码事实一致；如果发现会影响实现边界、验收标准、数据兼容或发布风险的阻塞级不一致，先停止实现并向用户确认。非阻塞差异要记录到当前 Issue 或实现说明中，作为后续实现依据。

| mismatch | level | action |
| --- | --- | --- |
| Issue 假设的入口、配置、表结构或核心接口不存在 | 阻塞 | 停止实现并确认需求或当前代码事实 |
| Issue 的验收标准依赖尚未实现的上游能力 | 阻塞 | 确认是否需要先拆分或完成前置 Issue |
| 类名、包名、方法名或文档称呼不同，但职责能对应 | 非阻塞 | 记录映射关系后继续实现 |
| 测试位置、验证命令或配置位置与文档不同 | 非阻塞 | 使用当前项目实际路径或命令，并说明差异 |

实现阶段不要硬编码具体语言、框架或实现类 Skill；具体实现方式由项目技术栈、用户偏好和当前任务决定。

专用 Skill 的规则优先处理具体执行细节；本 Skill 只保留阶段、门禁和交接约束。

# 6. 沉淀、Review 和反馈

Issue 完成后，如果新增或修改入口、调用链、配置项、数据结构、验证命令、排查关键词，或产生影响后续 AI 理解代码的实现事实，在需求文档同级目录下创建或更新 `.issue/<需求序号>-<Issue序号>-<Issue简述>-实现沉淀.md`；文件不存在时读取 [references/implementation-notes-template.md](references/implementation-notes-template.md) 后创建。

`.issue/` 是 `feat` 工作流临时目录，只保存最终归档前的 Issue 实现沉淀材料，不是最终权威文档。如果没有产生需要沉淀的实现事实，不更新 `.issue/`，并在完成说明中写明 `无需更新 Issue 实现沉淀`。

全部 Issue 完成后，`archive_ai_docs` 阶段必须使用 `ai-retrieval-docs` 读取需求文档、`.issue/` 下的实现沉淀文件、实际代码 diff、相关源码、测试、配置和已有 AI 检索文档，生成或更新正式 AI 检索文档。确认 AI 检索文档已反映最终实现事实后，按当前运行环境的文件删除、安全审批和跨项目修改规则，删除需求文档同级目录下的 `.issue/` 临时目录；如果需要审批，先请求确认。

当需求文档命名为 `<需求序号>-<需求简述>-需求文档.md` 时，最终 AI 检索文档由 `ai-retrieval-docs` 默认生成或更新为相邻编号的 `<相邻序号>-<需求简述>-AI检索说明.md`，例如 `10-订单超时处理-需求文档.md` 对应 `11-订单超时处理-AI检索说明.md`。

存在外部 Review 结果时，只处理 Codex 收到 Review 结果后的门禁。外部 Review 规则不明确时，不定义外部 Agent 的评审轮次、范围或输入材料。

如果外部 Review 结果没有明确标注严重级别，先按影响范围分类，再决定处理方式。不要把所有 Review 意见都当成必须修改，也不要跳过可能影响验收、回归风险或数据正确性的意见。Review 分类标准和处理门禁详见 [references/readiness-checklists.md](references/readiness-checklists.md) 中的「Review 结果处理规则」。

Issue DoD 只要求最近一轮 Review 没有阻塞级问题；非阻塞建议已处理或已有明确不处理理由即可。

用户说「使用 `feat` 对需求进行澄清」时，进入 `clarify_requirement` 阶段。用户说「继续 `feat` 的下一步」时，先判断当前阶段，再执行下一项门禁或阶段任务。

每次阶段推进后，按下表简短说明：

| field | requirement |
| --- | --- |
| `current_stage` | 当前阶段 |
| `documents` | 读取或更新了哪些文档 |
| `gate_result` | 是否通过门禁；未通过时说明阻塞原因 |
| `next_step` | 下一步动作，或需要用户确认的最关键问题 |
