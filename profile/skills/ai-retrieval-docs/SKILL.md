---
name: ai-retrieval-docs
description: Maintain Chinese AI retrieval docs, AI troubleshooting docs, AI context-entry docs, and AI retrieval-entry docs. Use when requirements, code changes, existing AI retrieval docs, or existing context-entry routes should update future-AI-readable code facts, execution paths, compatibility boundaries, validation commands, troubleshooting keywords, and progressive loading routes. Also use when the user asks to maintain project-level AI retrieval or context docs without specifying a document. Do not use for ordinary Markdown polishing, requirement design, implementation notes, Mermaid diagrams, or documents that are not meant for AI retrieval.
---

# 1. 快速路由

本 Skill 只维护 AI 检索文档和 AI 上下文入口文档。先判断输入类型，再只读取对应 reference；不要把它用于普通文档改写。

先判断用户是否指定了文档。用户指定文档时，读取必要文件名、路径、标题和少量内容后按下表判定文档类型；用户未指定文档时，直接匹配 `no_document`。只读取匹配行指定的 reference，不要一次加载全部流程文件。

**输入判定与加载路由：**

| input_type | match_signal | load_reference |
| --- | --- | --- |
| `requirement_doc` | 文件名或标题包含 `需求文档`、`需求设计文档`、`PRD`、`需求说明`，且内容描述目标、范围、澄清结论、验收或设计约束。 | [requirement-doc-flow.md](references/requirement-doc-flow.md) |
| `context_entry_doc` | 文件名为 `00-AI上下文入口.md`、`AI上下文入口.md`、`AI检索入口.md`，或内容主要描述加载规则、加载路由、核心事实和回答要求。 | [context-entry-flow.md](references/context-entry-flow.md) |
| `retrieval_doc` | 文件名包含 `AI检索说明`、`AI检索文档`、`AI排查文档`，或内容主要描述代码位置、执行链路、兼容边界、验证命令和检索关键词。 | [retrieval-doc-flow.md](references/retrieval-doc-flow.md) |
| `other_doc` | 不符合以上类型，或主要是普通说明、实现计划、会议记录、临时讨论、Markdown 排版问题。 | [input-routing.md](references/input-routing.md) |
| `no_document` | 用户没有提供文件、路径、标题或文档内容，只要求维护项目级 AI 检索或上下文文档。 | [input-routing.md](references/input-routing.md) |

如果一个文档同时符合多个类型，按「AI 上下文入口 > AI 检索文档 > 需求文档」判定，除非用户明确指定它的角色。

**行为权限与阻塞条件：**

| input_type | allowed_write | ask_user_when | stop_when |
| --- | --- | --- | --- |
| `requirement_doc` | 同目录 AI 检索文档、必要的需求目录入口、必要的上层入口。 | 需求文档所属项目或文档根无法判断；跨项目写入未确认。 | 只能证明需求设想，缺少可验证事实来源。 |
| `context_entry_doc` | 当前入口、入口路由范围内确认需要维护的 AI 检索文档、必要的上层入口。 | 没有变更需求文档，且用户未确认按入口路由范围统一维护。 | 用户只要求查看入口，未要求维护文档。 |
| `retrieval_doc` | 当前 AI 检索文档、必要的同级入口或上层入口。 | 需要扩大到入口路由范围维护，但用户未确认。 | 用户明确只要求分析当前文档且不改文件。 |
| `other_doc` | 默认不写文件。 | 总是先询问用户是否要转为 AI 检索文档维护任务。 | 用户没有确认维护范围或输入文档类型不匹配。 |
| `no_document` | 用户确认维护范围前默认不写文件；确认后按候选入口和 AI 检索文档范围写入。 | 总是先识别当前项目和候选文档目录，再询问用户是否维护该项目下所有 AI 上下文入口和 AI 检索文档。 | 用户没有确认维护范围，或当前项目没有可判断的文档根目录。 |

# 2. 流程级联关系

各 flow 文件在执行过程中可能按条件跳转到其他 flow。进入分支前先确认当前路径的最大加载深度。

| flow | 可能跳转 | 终端 |
| --- | --- | --- |
| `retrieval-doc-flow.md` | 找到上层入口时跳转 `context-entry-flow.md` | 否 |
| `context-entry-flow.md` | 存在变更需求文档时跳转 `requirement-doc-flow.md` | 否 |
| `requirement-doc-flow.md` | — | 是 |
| `input-routing.md` | — | 是 |

最长级联路径：`retrieval-doc-flow → context-entry-flow → requirement-doc-flow`（3 层）。每层 flow 内部还会按「按需读取参考」加载写作参考。

# 3. 通用硬规则

| trigger | action | forbidden |
| --- | --- | --- |
| 读取文档目录前 | 先查看目录文件列表，再读取入口文档和必要文档 | 直接批量读取同目录全部文档 |
| 已读取入口文档 | 按入口内加载路由继续读取 | 绕开入口全量扫描 |
| 写入 AI 检索事实 | 优先基于当前代码、测试和 diff 写事实；需求文档只作为目标和边界来源 | 把需求设想写成已实现事实 |
| 需求与代码不一致 | 以已实现事实为准，并只在影响后续排查时说明差异 | 为迎合需求文档改写代码事实 |
| 需求或文档引用当前项目外模块 | 先识别 workspace，再按模块名、包名、构建配置或文档路径定位兄弟项目 | 只在当前项目根目录内检索后断言不存在 |
| 需要跨项目修改文档 | 先说明范围并获得确认 | 未确认就跨项目写入 |
| 缺少可验证事实来源 | 不写入 AI 检索文档中的长期事实；事实来源包括代码、测试、diff、已有文档或用户明确结论 | 基于需求设想或推测生成已实现事实 |
| 未确认维护范围 | 不默认全量扫描或重写；先询问用户 | 默认读取入口范围内所有文档或默认重写全部已有文档 |

以上禁令在所有分支流程中均适用。reference 文件中的停止条件是对应分支的补充，不引入新的全局禁令。

写入前必须先按下表确认目标文件：

| target_type | create_when | update_when | ask_user_when | skip_when |
| --- | --- | --- | --- | --- |
| `retrieval_doc` | 同主题 AI 检索文档不存在，且已有可验证事实来源支撑已实现事实 | 同主题 AI 检索文档已存在，且稳定代码事实、验证方式或排查关键词变化 | 需求文档所属项目或文档根无法判断；跨项目写入未确认 | 只能证明需求设想，缺少可验证事实来源 |
| `requirement_dir_entry` | 目录存在多份需求、设计、示例或 AI 检索材料且容易混读 | 已有入口缺少当前主题路由、文件改名或新增相关文档 | 需要扩大到需求目录范围但用户只指定单个文档 | 同目录材料单一，入口不会降低误读风险 |
| `upper_entry` | 文档树需要渐进加载路由且当前层级最适合作为入口 | 已有上层入口缺少当前目录或能力域路由 | 跨项目或跨文档树维护范围未确认 | 上层入口已经能准确路由当前任务 |

# 4. 按需读取参考

flow 文件执行过程中，按下表在对应时机读取写作参考。只读取当前需要的参考，不要一次加载全部。

| load_trigger | target_reference | skip_when |
| --- | --- | --- |
| 准备写入 AI 检索文档 | [writing-ai-retrieval-doc.md](references/writing-ai-retrieval-doc.md) | 本次只维护入口，不涉及 AI 检索文档写入 |
| 准备写入 AI 上下文入口 | [writing-context-entry-doc.md](references/writing-context-entry-doc.md) | 本次只维护 AI 检索文档，不涉及入口写入 |
| 最终检查 Markdown | [markdown-and-checklist.md](references/markdown-and-checklist.md) | 本次未写入或更新任何文件 |
| 需要完整 AI 检索文档模板 | [document-template.md](references/document-template.md) | 已有同项目高质量参考文档，或只做局部更新 |

# 5. 事实收集要求

维护文档前，优先收集能证明事实的上下文：

| fact_source | collect_when | purpose |
| --- | --- | --- |
| 相关目录文件列表和入口文档 | 每次维护文档前 | 判断文档树、入口路由和跳过依据 |
| 用户指定的需求文档、AI 检索文档或入口文档 | 用户提供文件或路径时 | 判断输入类型、目标范围和已有事实 |
| `git status`、`git diff --name-only` 和必要 diff | 维护内容与当前变更相关时 | 确认实际改动文件和待沉淀事实 |
| diff 涉及的源码、测试、配置和已有文档 | diff 显示相关文件变化时 | 验证入口、执行链路、配置、测试和兼容边界 |
| `rg` 找到的入口类、处理器、常量、枚举、错误码、配置项、模板和测试 | 需要补全代码事实或调用链时 | 避免只基于需求文档写推测 |

不要把需求设想、临时讨论或推测写成已实现事实。不确定但重要的信息要标注为待确认。

# 6. 输出要求

| output_field | requirement |
| --- | --- |
| `read_scope` | 说明读取了哪些文档和代码，以及为什么读取 |
| `written_files` | 如果生成或更新了文件，说明文件路径和主要变化 |
| `skipped_docs` | 如果跳过相关目录下其他文档，说明跳过依据 |
| `validation` | 说明是否运行校验；未运行时说明原因 |
| `no_write_reason` | 如果最终不更新文件，说明依据，例如没有确认维护范围、输入文档类型不匹配、代码事实不足，或变更只影响普通说明文档 |
