---
name: feat
description: Orchestrate an AI coding feature workflow from lightweight requirement draft creation, clarification, PRD refinement, Feature DoR, vertical issue slicing, Issue DoR/DoD, implementation handoff, implementation notes, review result tracking, and final AI retrieval documentation. Use when the user mentions feat, feature workflow, continuing the next step, clarifying requirements, refining requirements, splitting issues, driving implementation, or archiving feature knowledge through this workflow.
---

# 1. 定位

本 Skill 是 AI Coding 主控工作流，不替代专用 Skill。用户只要点名 `feat` 或要求继续下一步，就由本 Skill 识别阶段、执行门禁、决定需要配合使用的专用 Skill。

如果进入某个阶段时存在更专用的 Skill，主动声明并使用它；用户不需要再次点名底层 Skill。

# 2. 前置检查

开始推进前先检查工作流必要条件。任一必要项不满足时中断当前流程。

| 检查项 | 失败处理 |
| --- | --- |
| 项目是否已完成 `mattpocock/skills` 初始化 | 提示用户运行 `/setup-matt-pocock-skills` |
| 当前会话是否可用 `grill-with-docs` | 提示用户添加或启用该 Skill |
| 当前会话是否可用 `to-prd` | 提示用户添加或启用该 Skill |
| 当前会话是否可用 `to-issues` | 提示用户添加或启用该 Skill |
| 当前会话是否可用 `read-project-docs` | 提示用户添加或启用该 Skill |
| 当前会话是否可用 `ai-retrieval-docs` | 提示用户添加或启用该 Skill |

不要把具体实现类 Skill 作为前置条件。

# 3. 阶段状态机

先读取用户指定的需求文档、Issue、实现记录或当前任务描述，再判断当前阶段：

| 当前状态 | 下一步 |
| --- | --- |
| 没有需求目录或需求文档 | 创建轻量需求草稿，读取 `references/requirement-template.md` |
| 需求文档仍有关键歧义 | 使用 `grill-with-docs` 澄清，并回写需求文档 |
| 需求澄清完成但需求文档未完善 | 参考 `to-prd` 的 PRD 结构，基于初版需求文档和澄清对话完善当前需求文档 |
| 需求文档已完善但未拆 Issue | 执行 Feature DoR，必要时读取 `references/readiness-checklists.md` |
| Feature DoR 通过 | 使用 `to-issues` 按垂直切片拆分 Issue |
| Issue 已拆分但未确认可开工 | 为每个 Issue 补齐 Issue DoR 和 Issue DoD |
| 某个 Issue 正在实现 | 使用 `read-project-docs` 定位并渐进读取相关需求、上下文入口、AI 检索文档或实现记录，再交接实现 |
| Issue 完成 | 执行 Issue DoD，并按需更新 `实现沉淀记录.md` |
| 全部 Issue 完成 | 使用 `ai-retrieval-docs` 生成或更新正式 AI 检索文档 |

如果无法判断阶段，先列出已知事实和缺失信息，只问一个最关键问题。

# 4. 文档权威边界

| 文档 | 权威范围 |
| --- | --- |
| 需求文档 | 目标、范围、非目标、业务规则、澄清结论、验收标准和验证建议 |
| `CONTEXT.md` | 稳定领域语言、核心模型、模块边界和长期系统事实 |
| ADR | 有长期影响的技术决策、被放弃方案和取舍理由 |
| Issue | 一个可执行垂直切片的目标、范围、非范围、验收标准、验证方式、依赖、DoR 和 DoD |
| `实现沉淀记录.md` | 已完成 Issue 产生的轻量实现事实，供后续归并 |
| AI 检索文档 | 最终已实现代码事实、入口、调用链、配置项、验证命令和排查关键词 |

不要把未实现设想写成 AI 检索文档事实。需求文档管「应该发生什么」，AI 检索文档管「代码现在怎么工作」。

# 5. 门禁和 Skill 编排

需求文档参考 `to-prd` 的 PRD 结构完善后执行 Feature DoR。未通过时先补需求文档，不要拆 Issue。

需求澄清完成后，必须把澄清结论回写到需求文档。若 `grill-with-docs` 判断需要维护 `CONTEXT.md` 或 ADR，按其规则同步更新。

Issue 拆分后为每个 Issue 补齐 Issue DoR 和 Issue DoD。Issue DoR 判断能否开工，Issue DoD 判断是否完成。

拆分 Issue 时必须按用户可感知或系统可验证的垂直切片拆分，不按 Controller、Service、Mapper、数据库表、测试等技术层拆分。

需要详细检查项时读取 `references/readiness-checklists.md`。

本 Skill 只显式关联工作流必要 Skill：

| 阶段 | 必要 Skill |
| --- | --- |
| 项目工作流初始化 | 必要时使用 `setup-matt-pocock-skills` |
| 需求澄清 | 使用 `grill-with-docs` |
| 需求文档完善 | 参考 `to-prd` 的 PRD 整理方式 |
| Issue 拆分 | 使用 `to-issues` |
| 实现阶段文档定位 | 使用 `read-project-docs` |
| 最终 AI 检索文档归档 | 使用 `ai-retrieval-docs` |

默认只参考 `to-prd` 的 PRD 模板和整理方式完善当前需求文档，不执行 `to-prd` 的发布流程，不创建独立 PRD Issue，也不创建第二份权威 PRD。只有用户明确要求发布或创建独立 PRD 时，才使用完整 `to-prd` 流程。

实现前先明确当前 Issue、来源需求文档、验收标准、预期验证方式和最小改动范围，并使用 `read-project-docs` 定位、渐进读取当前 Issue 相关的需求文档、上下文入口、AI 检索文档或实现记录。实现阶段不要硬编码具体语言、框架或实现类 Skill；具体实现方式由项目技术栈、用户偏好和当前任务决定。

专用 Skill 的规则优先处理具体执行细节；本 Skill 只保留阶段、门禁和交接约束。

# 6. 沉淀、Review 和反馈

每个 Issue 完成时，若新增或修改入口、调用链、配置项、数据结构、验证命令、排查关键词，或产生影响后续 AI 理解代码的实现事实，必须更新同需求目录下的 `实现沉淀记录.md`；如文件不存在，读取 `references/implementation-notes-template.md` 后创建。

如果没有产生需要沉淀的实现事实，完成说明中明确写：`无需更新实现沉淀记录`。

本 Skill 只检查外部 Review 结果是否已经回应：有问题则确认已修复或有明确解释，无问题则继续下一阶段。

本 Skill 不定义外部 Review 的轮次、范围、输入材料或退出标准。

用户说「使用 `feat` 对需求进行澄清」时，进入需求澄清阶段。

用户说「继续 `feat` 的下一步」时，先判断当前阶段，再执行下一项门禁或阶段任务。

每次阶段推进后，简短说明：

- 当前阶段；
- 读取或更新了哪些文档；
- 是否通过门禁；
- 下一步是什么。
