# 1. 上下文路由驱动流程

当触发时指定了项目启动承载文档中的 AI 上下文路由段落，或指定了 AI 上下文入口文档，按本文件处理。

先读取 [routing-graph.md](routing-graph.md)，根据项目实际内容和引用关系判断当前目标是 `startup_carrier` 还是 `route_entry`，不要根据文件名假设项目采用某套固定文档体系。

# 2. 判断维护模式

| mode | condition | action |
| --- | --- | --- |
| `route_only` | 用户要求补充第一跳、下一入口、上下级路由、连通性、孤立节点、循环检查，或同步新增、删除、重命名、移动后的路由 | 只读取当前节点、直接上级、直接下级和确认实际路径所需的相关段落；不读取整个路由范围的 AI 检索文档 |
| `scope_maintenance` | 用户要求根据入口统一维护其路由范围内的 AI 检索文档，或当前变更需求需要同步维护长期事实 | 按后续章节检查变更需求文档和确认维护范围 |

`route_only` 模式读取 [writing-context-entry-doc.md](writing-context-entry-doc.md) 后执行最小修改，并按 [completion-checklist.md](completion-checklist.md) 完成路由校验；完成后不进入后续章节。

# 3. 先查变更需求文档

先识别入口所在项目，再搜索该项目是否存在变更的需求文档：

- 优先使用 `git status`、`git diff --name-only` 和文件名模式查找变更的需求文档
- 需求文档模式包括 `*需求文档*.md`、`*需求设计文档*.md`、`*PRD*.md`、`*需求说明*.md`
- 如果用户显式指定其他项目或多个项目，以用户指定范围为准

如果存在变更的需求文档，以这些需求文档为入口，逐个读取 [requirement-doc-flow.md](requirement-doc-flow.md) 并按需求文档驱动流程维护 AI 检索文档、需求目录入口和上层入口。

# 4. 没有变更需求文档

如果不存在变更的需求文档，不要默认向下读取所有内容。

🔴 CHECKPOINT：询问用户是否以指定路由节点为起点，读取其路由范围内所有 AI 检索文档，并结合内部需求文档进行统一维护。

继续条件：用户明确确认维护该入口路由范围。

🛑 STOP：用户未确认统一维护范围时，不读取入口范围内全部文档，不写文件。

# 5. 用户确认统一维护后

用户确认后，从该入口文档的加载路由向下读取：

- 能力域入口或需求目录入口
- 路由到的 AI 检索文档
- 与 AI 检索文档同主题的需求文档、设计文档和示例数据
- 相关代码变更、测试和检索结果

维护时不要机械重写所有文档。只更新稳定事实已变化、加载路由缺失或文档明显过时的部分。

更新项目启动路由或 AI 上下文入口前读取 [writing-context-entry-doc.md](writing-context-entry-doc.md)，完成后读取 [completion-checklist.md](completion-checklist.md)。
