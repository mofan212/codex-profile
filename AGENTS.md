# 1. 项目定位

- 当前仓库是 Codex Profile 备份仓库，用于保存可迁移的 Codex 配置源码
- 根目录 `AGENTS.md` 只约束 AI 在当前仓库中的行为，不是要安装到 Codex 全局目录的备份文件
- 要备份和安装的 Codex 全局规则位于 `profile/AGENTS.md`
- 要备份和安装的自定义 Skill 位于 `profile/skills/`

# 2. 默认修改目标

- 用户要求修改 Codex 全局规则时，默认修改 `profile/AGENTS.md`
- 用户要求修改 Skill、调整 Skill 文档或新增 Skill 时，默认修改 `profile/skills/` 下的内容
- 用户只说「修改 Skill」「改全局规则」「更新配置」时，先理解为修改当前仓库中的备份源码
- 只有目标位置互相冲突、用户语义明确指向本机已安装 Codex 配置目录，或需要修改当前工作区之外的文件时，才先向用户确认
- 不要把备份用的 `profile/AGENTS.md` 或 `profile/skills/` 移回仓库根目录
- 除非用户明确要求安装、同步到本机或修改本机已安装 Codex 配置目录，否则不要修改 `~/.codex/AGENTS.md`、`~/.codex/skills/` 或其他已安装目录

# 3. Skill 编写规则

## 3.1 语言与格式

- 修改 `profile/skills/` 下的 Skill 内容时，`SKILL.md` 的 `description` 必须使用英文，正文必须使用中文；`agents/openai.yaml` 的 `default_prompt` 必须使用英文，`short_description` 必须使用中文
- 修改或新增 Skill 文档中的规则表格时，表头优先使用英文短字段，例如 `trigger`、`action`、`requirement`、`forbidden`、`purpose`；表格内容和正文使用中文。纯面向人类展示的清单可以使用中文表头
- 修改或新增 `profile/skills/*/references/` 下的表格时，路由表、契约表和机器字段表优先使用英文短表头；检查清单、示例分类、写作指南和命名说明优先使用中文表头
- 不要在同一张表中混用英文表头和中文表头
- Skill 文档中引用当前 Skill 内真实存在、稳定可定位的文件时，优先使用相对路径链接
- 文件名模式、待创建路径、命令、环境路径、目标项目中的候选文件名或泛称路径继续使用反引号
- 需要说明 Markdown 链接语法时，可以在行内代码或代码块中展示 `[文件名](文件名)`，不要渲染成实际占位链接

## 3.2 结构与设计

- 判断用表格还是列表的核心标准：**是否存在多列信息之间的稳定对应关系**。门禁、路由、Skill 交接、输出要求、Review 处理等包含触发条件-动作-禁止项等多列对应关系时，优先使用紧凑表格；字段候选、简单检查项、单句约束、偏好、禁令等单维信息优先使用短句或列表。列表化本身不构成违规，只有导致对应关系丢失时才需要回补结构
- 优化 Skill 时，不要以缩短篇幅或结构化作为目标；必须优先保证触发准确、执行确定、上下文加载可控
- 工作流 Skill 中涉及「是否继续执行」的规则，必须明确阻塞条件、非阻塞差异和处理动作，避免 AI 因轻微差异频繁询问用户，或在阻塞差异存在时继续实现
- 按需读取 `references/` 时，应写清楚读取触发条件、目标文件和跳过条件；不要只写「必要时读取」这类不可执行描述

## 3.3 校验与保护

- Skill 优化后必须检查 `description`、正文语言、`agents/openai.yaml`、引用文件路径和 `README.md` 同步关系；能运行校验时优先运行校验
- `write-a-skill` 只参与 Skill 修改完成后的检查：用它核对 Skill 是否符合结构、触发描述、渐进加载、引用深度、示例和脚本使用等要求
- 修改或新增 `profile/skills/` 下的 Skill 后，最终回复前必须完成 `write-a-skill` 检查；脚本校验不能替代该检查
- 如果 `write-a-skill` 检查发现不符合项，必须继续修改并重新检查
- 不要让 `write-a-skill` 参与 Skill 编写或修改阶段
- 在 Windows 中文环境运行 Skill 校验脚本读取中文 Markdown 时，如果遇到默认编码错误，优先使用 UTF-8 模式运行，例如设置 `PYTHONUTF8=1` 后再执行校验；不要把编码报错误判为 Skill 格式错误
- `profile/skills/coding-guidelines/` 是成熟 Skill，默认不要对此目录下的任何文件做任何调整；除非用户显式点名要求修改它，否则必须排除该目录

# 4. 同步维护规则

| trigger | action |
| --- | --- |
| 新增、删除、重命名或调整 Skill 目录结构 | 同步 `install.py` 和 `README.md` 中的路径、Skill 列表与安装说明 |
| 维护 `README.md` 中的 Skill 列表 | 按 `README.md` 现有类别归入合适分类，必要时新增类别，不要合并回单一总表 |
| 修改 Skill 之间的软依赖、切换关系或协作边界 | 同步 `README.md` 中的 Skill 软依赖关系说明 |
| 新增或修改 feat 工作流的阶段、门禁、依赖或文档边界 | 同步 `README.md` 中的 Feat 工作流说明、依赖声明和 Skill 列表 |
| 新增或修改 feat 工作流的实现沉淀规则或目录结构 | 同步 `README.md` 中的 Feat 工作流说明、依赖声明和 Skill 列表 |

# 5. 文档边界

- `README.md` 面向人类读者，不用于承载 AI 行为规则
- 项目级 AI 行为规则应写在根目录 `AGENTS.md`
- 除非用户明确要求更新面向人类的说明文档，否则不要为了约束 AI 行为而修改 `README.md`

# 6. 安装脚本边界

- `install.py` 应从 `profile/AGENTS.md` 和 `profile/skills/` 安装到目标 Codex 目录
- `install.py` 写入本机 Codex 目录的真实安装会整体替换目标目录中同名 Skill，不会合并目录，也不会保留目标同名 Skill 目录中的额外文件
- 如果由 AI 执行 `python install.py` 写入本机 Codex 目录，必须先向用户说明上述覆盖规则，并获得用户二次确认；`python install.py --dry-run` 不需要二次确认
- 调整备份目录结构时，必须同步检查并更新 `install.py`
- 验证安装行为时优先运行 `python install.py --dry-run`，确认来源和目标路径正确后再考虑真实安装
