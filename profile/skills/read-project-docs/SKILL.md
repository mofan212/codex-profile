---
name: read-project-docs
description: Read project documentation directories with progressive loading. Use when Codex needs to inspect a documentation directory, requirements directory, AI context-entry document, AI retrieval-entry document, README, index document, design document set, implementation notes, or mixed project docs before answering, designing, or modifying code. Do not use for ordinary source-code search that does not involve documentation directories.
---

# 1. 项目文档读取规则

使用本 Skill 读取项目文档目录、需求目录、设计文档目录、AI 上下文入口和 AI 检索入口。先定位入口和路由，再按需加载；不要因为文档位于同一目录，就一次性读取全部 Markdown。

# 2. 目录入口优先级

当任务需要读取文档目录时，必须先查看该目录下的文件列表和文件名，不要直接批量读取全部文档内容。

如果目录下存在多个入口候选，按下表从高到低选择：

| priority | file_signal | action | next_action | skip_when |
| --- | --- | --- | --- | --- |
| 1 | `00-AI上下文入口.md` | 先读取该入口 | 根据入口中的加载路由、文档定位、适用场景或引用说明继续读取 | 文件名不匹配或明显不属于当前任务范围 |
| 2 | `AI上下文入口.md` | 先读取该入口 | 根据入口中的加载路由、文档定位、适用场景或引用说明继续读取 | 已读取更高优先级入口 |
| 3 | `AI检索入口.md` | 先读取该入口 | 根据入口中的加载路由、文档定位、适用场景或引用说明继续读取 | 已读取更高优先级入口 |
| 4 | `README.md` | 没有 AI 入口时读取 | 按 README 中的目录说明、索引或链接继续读取 | 已读取 AI 入口且入口能覆盖当前任务 |
| 5 | `index.md` | 没有 AI 入口或 README 时读取 | 按索引继续读取 | 已读取更高优先级入口 |

读取入口文档后，只按入口指向的相关文档继续加载，不要绕开入口全量读取同目录 Markdown。

# 3. 按需加载规则

| scenario | action | skip_when |
| --- | --- | --- |
| 用户明确要求全量审查、全量汇总、完整迁移或上下文重建 | 可以读取同一目录下的全部相关 Markdown | 文件名或入口说明表明文档与任务无关 |
| 目录下不存在入口文档 | 先根据文件名、标题和目录结构判断最相关文档，再读取必要内容 | 仅因同目录存在而读取无关文档 |
| 读取过程中发现文档引用了更合适的上下文文档 | 按引用继续读取被指向文档 | 引用文档只解释历史背景且当前任务不需要 |
| 需求文档、AI 检索说明、设计文档、实现记录同时存在 | 优先读取 AI 检索说明或上下文入口，再根据任务需要补充读取原始需求或详细设计 | AI 检索说明已足以回答当前代码事实问题 |
| 多个文档存在明显新旧关系 | 优先读取最新的集成说明、AI 检索说明或上下文入口 | 旧版文档仅在对齐历史行为、兼容旧逻辑或追溯设计原因时读取 |

# 4. Skill 切换交接

| condition | target_skill | carry_context | stop_rule |
| --- | --- | --- | --- |
| 任务从读取文档转为维护 AI 检索文档、AI 排查文档、AI 上下文入口或 AI 检索入口 | `$ai-retrieval-docs` | 已读取的入口文档、路由依据、相关文档路径、跳过依据、仍需确认的问题 | 停止按本 Skill 扩大读取范围，由 `$ai-retrieval-docs` 判断写入边界、事实依据和是否需要询问用户 |
| 用户只要求理解、定位、汇总或基于文档回答问题，没有要求维护 AI 检索或入口文档 | 保持本 Skill | 已读取文档、读取理由、可选的下一步上下文 | 不写入 AI 检索文档或入口文档 |

# 5. 输出要求

| field | requirement |
| --- | --- |
| `read_docs` | 在回答、设计方案或修改代码前，说明当前读取了哪些文档 |
| `read_reason` | 说明为什么读取这些文档 |
| `skipped_docs` | 如果跳过同目录下其他文档，基于入口文档、文件名、标题或任务目标说明其暂时无关 |
| `next_context` | 如果仍需补充上下文，说明下一步应该读取什么以及触发条件 |
