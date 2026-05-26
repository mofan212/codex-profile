---
name: read-project-docs
description: Read project documentation directories with progressive loading. Use when Codex needs to inspect a documentation directory, requirements directory, AI context-entry document, AI retrieval-entry document, README, index document, design document set, implementation notes, or mixed project docs before answering, designing, or modifying code. Do not use for ordinary source-code search that does not involve documentation directories.
---

# 1. 项目文档读取规则

使用本 Skill 读取项目文档目录、需求目录、设计文档目录、AI 上下文入口和 AI 检索入口。目标是先定位入口和路由，再按需加载，避免把同一目录下的 Markdown 文档一次性全部读入上下文。

# 2. 目录入口优先级

当任务需要读取文档目录时，必须先查看该目录下的文件列表和文件名，不要直接批量读取全部文档内容。

如果目录下存在类似以下命名的入口文档，必须优先读取入口文档：

- `00-AI上下文入口.md`
- `AI上下文入口.md`
- `AI检索入口.md`
- `README.md`
- `index.md`

读取入口文档后，必须根据入口文档中的加载路由、文档定位、适用场景或引用说明，按需继续读取其他文档。

# 3. 按需加载规则

除非用户明确要求全量审查、全量汇总、完整迁移或上下文重建，否则不要一次性读取同一目录下的全部 Markdown 文档。

如果目录下不存在入口文档，应先根据文件名、标题和目录结构判断最相关的文档，再读取必要内容。读取过程中如发现文档引用了更合适的上下文文档，再继续按需加载。

对于需求文档、AI 检索说明、设计文档、实现记录同时存在的目录，应优先读取 AI 检索说明或上下文入口，再根据任务需要补充读取原始需求或详细设计。

如果多个文档存在明显的新旧关系，应优先读取最新的集成说明、AI 检索说明或上下文入口。只有在需要对齐历史行为、兼容旧逻辑或追溯设计原因时，才读取旧版文档。

# 4. 输出要求

在回答、设计方案或修改代码前，应能说明当前读取了哪些文档，以及为什么读取这些文档。

如果跳过了同目录下其他文档，应基于入口文档、文件名、标题或任务目标判断说明其暂时无关。
