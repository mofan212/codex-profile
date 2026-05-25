---
name: maintain-ai-retrieval-docs
description: Maintain Chinese AI retrieval docs, AI troubleshooting docs, AI context-entry docs, and AI retrieval-entry docs. Use when requirements, code changes, existing AI retrieval docs, or existing context-entry routes should update future-AI-readable code facts, execution paths, compatibility boundaries, validation commands, troubleshooting keywords, and progressive loading routes. Also use when the user asks to maintain project-level AI retrieval or context docs without specifying a document. Do not use for ordinary Markdown polishing, requirement design, implementation notes, Mermaid diagrams, or documents that are not meant for AI retrieval.
---

# 1. 快速路由

本 Skill 只维护 AI 检索文档和 AI 上下文入口文档。先判断输入类型，再只读取对应 reference；不要把它用于普通文档改写。

如果用户指定了文档，先读取必要文件名、路径、标题和少量内容，判定文档类型：

- 需求文档：文件名或标题包含 `需求文档`、`需求设计文档`、`PRD`、`需求说明`，且内容描述目标、范围、澄清结论、验收或设计约束。读取 `references/requirement-doc-flow.md`。
- AI 上下文入口文档：文件名为 `00-AI上下文入口.md`、`AI上下文入口.md`、`AI检索入口.md`，或内容主要描述加载规则、加载路由、核心事实和回答要求。读取 `references/context-entry-flow.md`。
- AI 检索文档：文件名包含 `AI检索说明`、`AI检索文档`、`AI排查文档`，或内容主要描述代码位置、执行链路、兼容边界、验证命令和检索关键词。读取 `references/retrieval-doc-flow.md`。
- 其他文档：读取 `references/input-routing.md` 中的错误触发处理，只询问用户，不直接生成文档。

如果一个文档同时符合多个类型，按「AI 上下文入口 > AI 检索文档 > 需求文档」判定，除非用户明确指定它的角色。

如果用户没有指定任何文档，读取 `references/input-routing.md`，先识别当前项目和候选文档目录，再询问用户是否维护该项目下所有 AI 上下文入口和 AI 检索文档。

# 2. 通用硬规则

先查看目录文件列表，不要直接批量读取同目录全部文档。读取入口文档后，按入口内的加载路由继续读取，不要绕开入口去全量扫描。

优先基于当前代码、测试和 diff 写事实；需求文档只作为目标和边界来源。发现需求与代码不一致时，以已实现事实为准，并只在影响后续排查时说明差异。

如果需求或文档引用当前项目外的模块，不要只在当前项目根目录内检索后断言不存在。先识别 workspace，再按模块名、包名、构建配置或文档路径定位兄弟项目。跨项目修改必须先说明范围并获得确认。

写入前必须先确认目标文件：

- AI 检索文档：优先更新同主题已有文档；不存在时按需求文档同级目录创建。
- 需求目录入口：只有目录存在多份需求、设计、示例或 AI 检索材料且容易混读时才创建或更新。
- 上层入口：只有文档树需要渐进加载路由，或已有入口需要补路由时才创建或更新。

写入 AI 检索文档前读取 `references/writing-ai-retrieval-doc.md`。写入 AI 上下文入口前读取 `references/writing-context-entry-doc.md`。写入或最终检查 Markdown 前读取 `references/markdown-and-checklist.md`。

# 3. 事实收集要求

维护文档前，优先收集能证明事实的上下文：

- 相关目录文件列表和入口文档；
- 用户指定的需求文档、AI 检索文档或入口文档；
- `git status`、`git diff --name-only` 和必要 diff；
- diff 涉及的源码、测试、配置和已有文档；
- 通过 `rg` 找到的入口类、处理器、常量、枚举、错误码、配置项、模板和测试。

不要把需求设想、临时讨论或推测写成已实现事实。不确定但重要的信息要标注为待确认。

# 4. 输出要求

完成后说明读取了哪些文档和代码、为什么读取、生成或更新了哪些文件、是否跳过了相关目录下其他文档，以及是否运行了校验。

如果最终决定不更新文件，也要说明依据，例如没有确认维护范围、输入文档类型不匹配、代码事实不足，或变更只影响普通说明文档。
