# 1. 项目定位

- 当前仓库是 Codex Profile 备份仓库，用于保存可迁移的 Codex 配置源码
- 根目录 `AGENTS.md` 只约束 AI 在当前仓库中的行为，不是要安装到 Codex 全局目录的备份文件
- 要备份和安装的 Codex 全局规则位于 `profile/AGENTS.md`
- 要备份和安装的自定义 Skill 位于 `profile/skills/`

# 2. 修改目标

- 用户要求修改 Codex 全局规则时，默认修改 `profile/AGENTS.md`
- 用户要求修改 Skill、调整 Skill 文档或新增 Skill 时，默认修改 `profile/skills/` 下的内容
- 不要把备份用的 `profile/AGENTS.md` 或 `profile/skills/` 移回仓库根目录
- 除非用户明确要求安装、同步到本机或修改真实 Codex 配置目录，否则不要修改 `~/.codex/AGENTS.md`、`~/.codex/skills/` 或其他已安装目录
- 如果用户只说「修改 skill」「改全局规则」「更新配置」，必须先理解为修改当前仓库中的备份源码；如果仍然无法判断目标位置，先向用户确认

# 3. Skill 编写规则

- 修改 `profile/skills/` 下的 Skill 内容时，`SKILL.md` 的 `description` 必须使用英文，正文必须使用中文；`agents/openai.yaml` 的 `default_prompt` 必须使用英文，`short_description` 必须使用中文
- 修改或新增 Skill 文档中的规则表格时，表头优先使用英文短字段，例如 `trigger`、`action`、`requirement`、`forbidden`、`purpose`；表格内容和正文使用中文。纯面向人类展示的清单可以使用中文表头
- 修改或新增 `profile/skills/*/references/` 下的表格时，路由表、契约表和机器字段表优先使用英文短表头；检查清单、示例分类、写作指南和命名说明优先使用中文表头
- 不要在同一张表中混用英文表头和中文表头
- 编写或优化 Skill 规则时，不要把结构化作为目标；简单单维规则、偏好、禁令、候选字段清单优先使用短句或列表；只有存在必须一一对应的触发条件、动作、禁止项、通过条件、输出要求或交接上下文时，才优先使用紧凑表格
- 优化 Skill 时，不要以缩短篇幅作为唯一目标；必须优先保证触发准确、执行确定、上下文加载可控
- 门禁、路由、Skill 交接、输出要求和 Review 处理规则如果包含多列信息之间的稳定对应关系，必须优先使用紧凑表格；如果只是字段候选、简单检查项或单句约束，可以使用短句或列表，不要为了表格化牺牲简洁性
- 判断 Skill 优化是否违反结构规则时，先判断信息关系维度：列表化本身不构成冲突；只有列表化导致触发条件、动作、禁止项、停止条件、验证方式、输出要求或交接上下文之间的对应关系丢失时，才视为需要回补结构
- 工作流 Skill 中涉及「是否继续执行」的规则，必须明确阻塞条件、非阻塞差异和处理动作，避免 AI 因轻微差异频繁询问用户，或在阻塞差异存在时继续实现
- 按需读取 `references/` 时，应写清楚读取触发条件、目标文件和跳过条件；不要只写「必要时读取」这类不可执行描述
- Skill 文档中引用当前 Skill 内真实存在、稳定可定位的文件时，优先使用相对路径链接；文件名模式、待创建路径、命令、环境路径、目标项目中的候选文件名或泛称路径继续使用反引号。需要说明 Markdown 链接语法时，可以在行内代码或代码块中展示 `[文件名](文件名)`，不要渲染成实际占位链接。
- Skill 优化后必须检查 `description`、正文语言、`agents/openai.yaml`、引用文件路径和 `README.md` 同步关系；能运行校验时优先运行校验
- `write-a-skill` 只参与 Skill 修改完成后的检查：用它核对 Skill 是否符合结构、触发描述、渐进加载、引用深度、示例和脚本使用等要求
- 如果 `write-a-skill` 检查发现不符合项，必须继续修改并重新检查；不要让它参与编写或修改阶段
- 在 Windows 中文环境运行 Skill 校验脚本读取中文 Markdown 时，如果遇到默认编码错误，优先使用 UTF-8 模式运行，例如设置 `PYTHONUTF8=1` 后再执行校验；不要把编码报错误判为 Skill 格式错误
- `profile/skills/coding-guidelines/` 是成熟 Skill，后续进行 Skill 优化、批量润色、协作边界调整或规则沉淀时，默认排除该目录；除非用户明确点名要求修改它，否则不要修改此 Skill

# 4. 同步维护规则

- 如果新增、删除、重命名或调整 `profile/skills/` 下的 Skill 目录结构，必须同步检查并按需维护 `install.py` 和 `README.md` 中的路径、Skill 列表与安装说明
- 维护 `README.md` 中的 Skill 列表时，必须按职责拆分到不同类别：`feat` 和 `ai-retrieval-docs` 属于 Feat 工作流技能，`chinese-markdown` 和 `node-fetch-http` 属于通用技能，当前其他 Skill 属于编码技能；后续新增 Skill 必须归入合适类别，必要时新增类别，不要合并回单一总表
- 如果修改 `profile/skills/` 下各 Skill 之间的软依赖、切换关系或协作边界，必须同步维护 `README.md` 中的 Skill 软依赖关系说明
- 如果新增或修改 `feat` 工作流的阶段、门禁、依赖 Skill、文档边界、实现沉淀规则或目录结构，必须同步检查并按需维护 `README.md` 中的 Feat 工作流说明、依赖声明、软依赖关系和 Skill 列表

# 5. 文档边界

- `README.md` 面向人类读者，不用于承载 AI 行为规则
- 项目级 AI 行为规则应写在根目录 `AGENTS.md`
- 除非用户明确要求更新面向人类的说明文档，否则不要为了约束 AI 行为而修改 `README.md`

# 6. 安装脚本边界

- `install.py` 应从 `profile/AGENTS.md` 和 `profile/skills/` 安装到目标 Codex 目录
- `install.py` 真实安装时会整体替换目标目录中同名 Skill，不会合并目录，也不会保留目标同名 Skill 目录中的额外文件
- 如果由 AI 执行 `python install.py` 进行真实安装，必须先向用户说明上述覆盖规则，并获得用户二次确认；`python install.py --dry-run` 不需要二次确认
- 调整备份目录结构时，必须同步检查并更新 `install.py`
- 验证安装行为时优先运行 `python install.py --dry-run`，确认来源和目标路径正确后再考虑真实安装
