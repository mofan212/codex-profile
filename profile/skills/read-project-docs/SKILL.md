---
name: read-project-docs
description: Read project documentation directories with progressive loading. Use when Codex needs to inspect a documentation directory, requirements directory, AI context-entry document, AI retrieval-entry document, README, index document, design document set, implementation notes, or mixed project docs before answering, designing, or modifying code. Do not use for ordinary source-code search that does not involve documentation directories.
---

# 1. 项目文档读取规则

使用本 Skill 读取项目文档目录、需求目录、设计文档目录、AI 上下文入口和 AI 检索入口。先定位入口和路由，再按需加载；不要因为文档位于同一目录，就一次性读取全部 Markdown。

# 2. 目录入口优先级

当任务需要读取文档目录时，必须先查看该目录下的文件列表和文件名，不要直接批量读取全部文档内容。

按以下顺序查找入口，优先读取第一个命中的入口：

1. `00-AI上下文入口.md` — 读取该入口，根据其中的加载路由、文档定位、适用场景或引用说明继续读取
2. `AI上下文入口.md` — 同上
3. `AI检索入口.md` — 同上
4. `README.md` — 没有 AI 入口，或已读取的 AI 入口不能覆盖当前任务时读取；如果 AI 入口已覆盖当前任务，跳过
5. `index.md` — 没有以上入口时读取，按索引继续读取

读取入口文档后，先按入口指向的相关文档继续加载。只有入口缺失、入口不能覆盖当前任务，或用户明确要求全量读取时，才继续读取其他入口或同目录文档。

# 3. 按需加载规则

用户明确要求全量审查、汇总、迁移或上下文重建时，可读取同目录下全部相关 Markdown，跳过文件名或入口说明表明与任务无关的文档，不再逐条判断下表场景。

其余情况按下表场景叠加执行：

| scenario | action | skip_when |
| --- | --- | --- |
| 目录下不存在入口文档 | 根据文件名、标题和目录结构判断最相关文档，再读取 | 仅因同目录就读取无关文档 |
| 需求文档、AI 检索说明、设计文档、实现记录同时存在 | 优先读取 AI 检索说明或上下文入口，按需补充原始需求或详细设计 | AI 检索说明已足以回答当前问题 |
| 多个文档存在明显新旧关系 | 优先读取最新的集成说明、AI 检索说明或上下文入口 | 旧版文档仅在追溯历史行为或兼容旧逻辑时读取 |
| 读取过程中发现引用了更合适的上下文文档 | 按引用继续读取被指向文档 | 引用文档只解释历史背景且当前任务不需要 |

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
