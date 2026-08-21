---
name: chinese-markdown
description: 处理以中文为主要内容的 Markdown / `.md` 文档排版，以及 Markdown 内 Mermaid `flowchart` 源码整理。当用户要求新增、修改、格式化或审查中文 Markdown 的排版与结构，或明确要求整理 Markdown 内 Mermaid `flowchart` 时，使用该 Skill。不适用于纯英文 Markdown 的普通排版、通用 Mermaid 设计、业务事实或观点改写、需求设计、文章内容润色或非排版任务。
---

# 1. 执行流程

| step | action | completion_criterion |
| --- | --- | --- |
| 1 | 确认目标是中文 Markdown，或用户明确要求处理 Markdown 内的 Mermaid `flowchart` | 不匹配时选择 `non_markdown` 并退出 |
| 2 | 依次选择目标类型、操作模式和检查范围 | 确定一个 `target_type`、一个 `operation_mode` 和一个或多个 `content_scope` |
| 3 | 在起草或修改前，按检查范围读取对应 reference；Mermaid 范围继续确定图类型和处理深度 | 当前 `content_scope` 对应的规则已加载，且只加载本次需要、真实存在的文件 |
| 4 | 按「格式基线优先级」确定本次可应用的规则 | 用户约束、完整文档习惯、片段边界或新文档默认基线已明确 |
| 5 | 在选定范围内执行最小充分改动；提交或差异任务只处理触碰的行 | 产出修改内容或问题清单，且未推断缺失上下文或扩大语义 |
| 6 | 输出前执行已加载 reference 的适用检查清单，通过完成门禁后按输出契约汇报 | 适用项已处理或报告，跳过项、语义变化和未执行验证均已说明 |

# 2. 输入路由与格式基线

必须先选择 `target_type`。`SKILL.md` 等 Skill 文档优先选择更具体的 `skill_markdown`；只有 Markdown 目标才能继续选择操作模式和检查范围，`non_markdown` 立即退出。

| axis | value | match_signal | action |
| --- | --- | --- | --- |
| `target_type` | `markdown_document` | 以中文为主要内容的 Markdown / `.md` 文档或明确片段，或包含用户明确要求处理的 Mermaid `flowchart` | 继续选择操作模式和检查范围 |
| `target_type` | `skill_markdown` | `SKILL.md` 或其他 Skill 文档，且任务涉及 Markdown 格式或中文排版 | 只处理格式；Skill 设计由对应创建、优化或维护流程负责 |
| `target_type` | `non_markdown` | 非 Markdown、纯英文 Markdown 的普通排版，或主要目标是事实改写、需求设计、文章润色、通用 Mermaid 设计 | 不使用本 Skill |
| `operation_mode` | `edit` | 用户明确要求新增、修改、格式化、排版或修正 | 在选定范围内落地修改 |
| `operation_mode` | `review_only` | 用户只要求审查、指出问题或给修正方向 | 输出问题、依据和修正方向，不修改文件或直接给出修订版本 |
| `content_scope` | `full_document` | 用户要求处理中文 Markdown，且未限定检查项 | 读取 [markdown-examples.md](references/markdown-examples.md) 和 [chinese-copywriting.md](references/chinese-copywriting.md) |
| `content_scope` | `markdown_limited_check` | 用户只要求检查标题、表格、链接、列表、行内语法等 Markdown 项 | 读取 [markdown-examples.md](references/markdown-examples.md)，只处理指定项目 |
| `content_scope` | `copywriting_limited_check` | 用户只要求检查中英空格、中文标点、全角半角、专有名词等 | 读取 [chinese-copywriting.md](references/chinese-copywriting.md)，只处理指定项目 |
| `content_scope` | `mermaid_diagram` | 用户明确要求整理 Markdown 内的 Mermaid，或明确要求修改当前差异触碰的 Mermaid 源码 | 将代码块第一条非空、非注释语句识别为图声明；`flowchart` 读取 [mermaid-flowchart.md](references/mermaid-flowchart.md)，其他图类型保留源码并说明未处理 |

`content_scope` 可以组合。用户限定范围高于内容命中；用户未要求处理 Mermaid 时，不因文档中存在 Mermaid 代码块而追加整理。

按下表从上到下选择首个匹配的格式基线：

| priority | baseline | condition | action |
| --- | --- | --- | --- |
| 1 | `user_explicit` | 用户明确指定标题、编号、列表、表格、引号、标点或 Mermaid 源码组织方式 | 按用户约束执行，仍保持语义、技术内容和技术符号不变 |
| 2 | `existing_document` | 已读取完整文档，且既有格式合法、一致 | 沿用既有标题深度、编号起点和局部习惯 |
| 3 | `fragment` | 只提供片段，无法确认片段外结构 | 保留标题层级和编号；只修复不依赖外部上下文的机械问题，并报告不确定项 |
| 4 | `new_document` | 新建或空文档，没有既有格式 | 默认使用无编号标题和任务所需的最少层级；不自动套用两级标题或连续编号约定 |

[markdown-examples.md](references/markdown-examples.md) 中的「两级连续编号约定」只在用户明确要求启用该约定，或完整文档已经稳定采用该约定时生效。其他情况下，只报告不依赖缺失上下文即可确认的结构问题。

## 2.1 新文档首稿门禁

当 `operation_mode=edit` 且 `baseline=new_document` 时，依次通过以下门禁：

| gate | action | failure_handling |
| --- | --- | --- |
| `before_draft` | 起草前逐个加载当前 `content_scope` 对应的 reference | 任一应读文件未加载时执行 `🛑 STOP`，按 reference 读取失败流程处理；加载完成前不得起草 |
| `first_draft` | 第一稿直接遵守已加载规则，并按第 4 节交付格式直接呈现；只有「外层围栏」条件成立时才增加围栏 | 不得先生成违规内容，再等待用户要求格式化或修正 |
| `before_delivery` | 输出前执行 [chinese-copywriting.md](references/chinese-copywriting.md) 的适用检查清单 | 中文正文出现 `“”` 且不属于非阻塞例外时，完成门禁失败；交付前改为 `「」`，嵌套引号使用 `『』`，然后重新检查 |

用户明确指定其他引号风格，或 `“”` 位于行内代码、代码块、JSON、YAML、命令、字符串字面量等技术内容时，属于非阻塞例外：保留原文并继续检查其他适用项，不询问、不阻塞，不做全局或机械替换。

# 3. 失败处理与检查点

| trigger | action | continue_when |
| --- | --- | --- |
| 用户要求处理既有文件，但目标不存在、不可读或内容为空且并非新建任务 | 🛑 STOP：说明无法建立目标范围和格式基线 | 用户提供可读内容、正确路径，或确认转为新建任务 |
| 用户只提供片段，无法判断完整文档格式 | 保留标题层级和编号，只处理片段内可确定的机械问题 | 已在结果中说明不能保证片段外结构 |
| 已选择的 reference 无法读取 | 🛑 STOP：说明读取失败，不凭记忆替代规则 | 用户提供规则内容，或确认跳过对应 `content_scope` |
| 用户要求新建 Mermaid 代码块但未指定图类型 | 🔴 CHECKPOINT：请求用户明确图类型，不提供候选业务内容 | 用户明确图类型后重新路由 |
| 用户限定范围外存在可定位问题 | 保持原文，在结果中单列未处理的问题类型 | 选定范围已处理完成 |
| 文档既有习惯与 reference 不同 | 按格式基线优先级判断；合法一致的既有习惯优先 | 已确定哪些 reference 规则适用；只有修复会扩大结构或语义范围时再确认 |
| 格式处理需要改变业务含义、术语、事实、结论或 Mermaid 图示语义 | 🔴 CHECKPOINT：停止语义改写并说明影响 | 用户明确授权对应语义变化 |
| 用户未明确要求结构调整，但完成任务需要重排标题层级、拆分章节或合并大段内容 | 🛑 STOP：说明结构影响和预计范围 | 用户确认结构调整 |

# 4. 输出契约

| item | requirement |
| --- | --- |
| 粘贴内容 | `edit` 按用户要求直接呈现修订稿 |
| 真实文件 | `edit` 只报告文件和改动，不重复粘贴全文 |
| 审查结果 | `review_only` 对每个问题依次给出原文、可直接替换的完整局部修正和简短依据，不输出整篇修订稿 |
| 外层围栏 | 默认不给整个文档增加外层代码围栏；只有用户明确要求可复制源码，或直接呈现会破坏嵌套围栏时，才使用更长的外层围栏 |
| 处理范围 | 说明处理了全文、指定章节、粘贴片段还是限定项目 |
| 修正类型 | 概括实际修正的 Markdown、中文排版或 Mermaid 源码类型 |
| 跳过项 | 选择限定范围时，单列目标中实际存在但未处理的范围；使用「未检查」或「未处理」，不要将未审查范围表述为「无需调整」或「没有问题」 |
| 语义变化 | 默认说明无业务或图示语义变化；发生变化时说明用户确认结果 |
| 校验结果 | 说明已完成哪些 reference 检查清单，以及未执行的解析或渲染验证 |

# 5. 禁止行为

| anti_pattern | required_behavior |
| --- | --- |
| 将中文排版任务扩大为内容编辑 | 只处理格式和选定的 Mermaid 源码范围；事实、观点和文章内容交给对应任务流程 |
| 从片段推断完整文档结构 | 保留片段中的标题层级和编号，只报告需要完整上下文才能确认的问题 |
| 用 reference 覆盖合法一致的既有风格 | 先执行格式基线优先级，只应用当前基线允许的规则 |
| 忽略用户限定范围或扩大提交修复范围 | 只处理选定 `content_scope` 和当前差异触碰的行 |
| 将第一稿当作可暂时违反规则的草稿 | 起草前加载当前范围的规则，让第一稿直接符合规则，不把格式修正推迟到用户再次要求 |
| 对所有 `“”` 执行全局替换 | 只修正适用规则覆盖的中文正文；保留用户指定风格和技术内容中的原始字符 |
| 将未审查范围断言为没有问题 | 明确说明对应范围未检查或未处理，只对已加载规则覆盖的范围下结论 |
| 为整理 Mermaid 执行超过用户要求的重构 | 先选择处理深度，只做达到用户目标所需的最小改动 |
| 猜测不存在、无法识别或未加载的规则 | 保持原文并报告边界；reference 读取失败时执行 `🛑 STOP` |
| 为排版改写字段名、参数、链接目标或技术符号 | 只调整符号外侧排版和已确认的源码组织 |

# 6. 完成条件

- 已通过目标门禁并完成三轴路由
- 已按优先级确定格式基线，且没有从片段推断完整文档结构
- 新建文档已在起草前加载当前 `content_scope` 对应的 reference，第一稿直接符合已加载规则和交付格式
- 已逐项执行所有已加载 reference 的适用检查清单；编辑模式下适用项通过，审查模式下每个问题均包含原文、可直接替换的完整局部修正和简短依据
- 已在交付前检查中文正文引号：默认使用 `「」`，嵌套使用 `『』`；用户指定风格和技术内容作为非阻塞例外保持不变
- 已采用最小充分改动，用户限定范围、历史残留和未执行验证均已说明
- 业务事实、技术符号和 Mermaid 图示语义保持不变，或已有用户确认
- 输出覆盖交付格式、处理范围、修正类型、跳过项、语义变化和校验结果
