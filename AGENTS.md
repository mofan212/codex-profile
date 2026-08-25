# 1. 项目定位

- 当前仓库是 Codex Profile 备份仓库，主要用于保存可迁移的 Codex 全局规则、共享 Skills 和收集的提示词，另附可公开同步的 OpenCode 配置
- 根目录 `AGENTS.md` 只约束 AI 在当前仓库中的行为，不是要安装到 Codex 全局目录的备份文件
- 要备份和安装的 Codex 全局规则是 `profile/AGENTS.md`，自定义 Skill 位于 `profile/skills/`；提示词位于 `prompts/`，不参与安装，维护规则见 `prompts/AGENTS.md`；OpenCode 公开配置位于 `opencode/opencode.jsonc`，详细说明位于 `opencode/README.md`

# 2. 默认修改目标

- 用户要求修改 Codex 全局规则时，默认修改 `profile/AGENTS.md`；要求修改、新增或调整 Skill 时，默认修改 `profile/skills/`；要求新增、修改或整理提示词时，默认修改 `prompts/`；要求修改 OpenCode 配置时，默认修改 `opencode/opencode.jsonc`
- 用户只说「修改 Skill」「改全局规则」「记提示词」「更新配置」时，先理解为修改当前仓库中的备份源码
- 只有目标位置互相冲突、用户语义明确指向本机已安装配置目录，或需要修改当前工作区之外的文件时，才先向用户确认
- 除非用户明确要求安装、同步到本机或修改本机已安装配置目录，否则不要修改 `~/.codex/AGENTS.md`、`~/.agents/skills/`、`~/.config/opencode/opencode.jsonc` 或其他已安装目录

# 3. Skill 编写规则

## 3.1 语言与格式

- 修改 `profile/skills/` 下的 Skill 内容时，`SKILL.md` 的 `description`、正文和 `agents/openai.yaml` 的 `default_prompt`、`short_description` 均优先使用中文，以保证 Skill 在中文语境下稳定触发和执行
- 如果需要兼容英文触发或跨语言工具链，可以在中文描述基础上补充英文短语，但不得牺牲中文触发准确性
- `SKILL.md` 的 `description` 和 `agents/openai.yaml` 的 `default_prompt` 必须保持 Agent 中立：描述任务能力、适用场景和触发条件时，不要把执行主体绑定到某个具体 AI Agent 或产品名；当任务对象本身是特定 Agent、产品或配置时，可以提及对应名称，但只能作为任务对象出现
- `SKILL.md` 的 `description` 使用中文描述触发条件时，优先使用「当...时，使用该 Skill。」句式
- `agents/openai.yaml` 的 `default_prompt` 应直接描述执行原则、边界和输出要求
- 修改或新增 Skill 表格时，表头语言按表格职责选择：执行契约、路由、门禁、输出字段和机器字段等结构化表格，优先使用英文短字段，例如 `trigger`、`condition`、`action`、`forbidden`、`skip_when`、`stop_when`、`reference`；解释型、示例型、写作说明、命名说明和面向人类阅读的检查表，优先使用中文表头，例如「章节」「用途」「规则」「正确」「错误」「说明」
- 不要在同一张表中混用中、英文表头；除非引用外部字段或代码标识，表头本身应保持同一种语言
- Skill 文档中引用当前 Skill 内真实存在、稳定可定位的文件时，优先使用相对路径链接
- 文件名模式、待创建路径、命令、环境路径、目标项目中的候选文件名或泛称路径使用反引号
- 需要说明 Markdown 链接语法时，可以在行内代码或代码块中展示 `[文件名](文件名)`，不要渲染成实际占位链接

## 3.2 结构与设计

- 判断用表格、无序列表还是有序列表时，先看信息结构，不追求全文形式统一。存在多列稳定对应关系或执行契约时用紧凑表格；只有一维规则、速查词表、字段候选、偏好、禁令或单句约束时用短句或无序列表；文本表达「按顺序」「步骤」「优先级」等先后关系时用有序列表。表格会增强契约感，也会增加阅读重量，只有能降低误读、保留对应关系或支撑执行判断时才使用
- Skill 文档和 `references/` 中不要添加只重复后续标题的目录小节；只有文件较长、章节较多，或目录本身承担读取路由、执行顺序、跳过条件或章节用途说明时，才保留目录。短引用文件优先依靠标题结构导航
- 优化 Skill 时，不要将缩短篇幅或结构化作为目标，必须优先保证触发准确、执行确定、上下文加载可控
- Skill 中涉及「是否继续执行」的规则，必须明确阻塞条件、非阻塞差异和处理动作，避免 AI 因轻微差异频繁询问用户，或在阻塞差异存在时继续实现
- 在 Skill 或项目规则中表达暂停/阻断语义时，区分使用 `🔴 CHECKPOINT` 和 `🛑 STOP`：`🔴 CHECKPOINT` 表示需要先向用户确认边界、事实、影响或选择，确认后可以继续；`🛑 STOP` 表示当前动作未满足继续条件，必须停止执行、补齐信息、切换流程或等待用户决策后才能继续。不要把两者合并写成 `CHECKPOINT · STOP`、`CHECKPOINT/STOP` 等混合标记；同一触发条件只能选择一个最准确的信号，并在后文说明继续条件
- 按需读取 `references/` 时，应写清楚读取触发条件、目标文件和跳过条件，不要只写「必要时读取」这类主观描述
- Skill 中跨文件引用 reference 时，优先只引用目标文件路径，并由被引用文件内部维护具体执行要求；引用应沿执行流程单向展开，跨 flow 跳转必须有明确条件，且不得形成循环引用

## 3.3 校验与保护

- 新增、修改或优化 Skill 后必须检查 `description`、正文语言、`agents/openai.yaml` 的字段完整性与语言规则、引用文件路径和 `README.md` 同步关系；能运行校验时优先运行校验
- 新增 Skill 或较大修改既有 Skill 后，须向用户呈现结构质量评审要点；脚本校验不能替代该复核，发现不符合项时必须继续修改并重新检查
- 在 Windows 中文环境运行 Skill 校验脚本读取中文 Markdown 时，如果遇到默认编码错误，优先使用 UTF-8 模式运行，例如设置 `PYTHONUTF8=1` 后再执行校验；不要把编码报错误判为 Skill 格式错误

# 4. 同步维护规则

| trigger | action |
| --- | --- |
| 新增、删除、重命名或调整 Skill 目录结构 | 同步 `scripts/install_codex_profile.py` 和 `README.md` 中的路径、Skill 列表与安装说明 |
| 维护 `README.md` 中的 Skill 列表 | 按 `README.md` 现有类别归入合适分类，必要时新增类别，不要合并回单一总表 |
| 修改 Skill 之间的软依赖、切换关系或协作边界 | 同步 `README.md` 中的 Skill 软依赖关系说明 |
| 新增或修改 feat 工作流的阶段、门禁、依赖、文档边界、实现沉淀规则或目录结构 | 同步 `README.md` 中的 feat 工作流说明、依赖声明和 Skill 列表 |
| 修改 OpenCode 配置的备份范围、安装路径或安装行为 | 同步 `opencode/install.py`、`opencode/README.md` 和 `CHANGELOG.md`；根目录 `README.md` 只保留简要说明 |

## 4.1 重要更新日志

`CHANGELOG.md` 面向人类读者，只记录用户在拉取、安装或使用新版本后需要感知或采取行动的重要变化，例如安装行为、能力增删、使用入口、外部依赖和兼容性变化。规则措辞、模型适配、内部执行策略、文档结构和排版优化由 Git 提交历史记录。

| trigger | action | skip_when |
| --- | --- | --- |
| 新增、删除或重命名 Skill，或改变安装、卸载行为 | 按日期倒序分点列举变更 | 仅修改 Skill 内部规则、文案或结构 |
| 改变用户使用入口、必要操作、外部依赖或兼容要求 | 直接列举用户需要感知的入口、操作、依赖或兼容性变更 | 用户无需感知或采取行动 |
| 新增日志条目 | 使用无字段标签的无序列表直接列举变更，不拆分 `变更`、`原因`、`影响` | 不为普通提交补充流水记录 |
| 当天日期节点已存在 | 将新变更追加到该日期节点现有列表末尾 | 不新增相同日期节点 |
| 当天日期节点不存在 | 在「更新记录」章节开头新增日期节点，保持日期倒序 | 不在旧日期节点之后追加新日期 |

# 5. 文档边界

- `README.md` 面向人类读者，不承载 AI 行为规则；项目级 AI 行为规则写在根目录 `AGENTS.md`
- 除非用户明确要求，或满足同步维护规则，否则不要修改 `README.md`；需要更新时，只维护其中面向人类读者的事实说明、Skill 列表、依赖关系和安装说明

# 6. 安装脚本边界

- 根目录 `install.py` 是 Codex 安装入口，实际实现位于 `scripts/install_codex_profile.py`；真实安装会把 `profile/AGENTS.md` 写入 `~/.codex/`，并整体替换 `~/.agents/skills/` 中的同名 Skill 目录，不做合并，也不保留其中的额外文件
- `opencode/install.py` 是独立的配置安装脚本，会根据 `opencode/opencode.jsonc` 生成并整体覆盖 `~/.config/opencode/opencode.jsonc`，不会合并内容；真实安装优先读取 `OPENCODE_CUSTOM_BASE_URL`，缺失时仅在交互终端请求输入，将实际地址写入目标配置但不得写回仓库或回显
- `scripts/cleanup_legacy_codex_skills.py` 是一次性清理脚本，会删除旧版本安装到 `~/.codex/skills/` 的 Skill 和旧 manifest，清理完成后无需再运行
- 如果由 AI 执行上述脚本写入本机已安装目录，必须先向用户说明对应覆盖或删除规则，并获得用户二次确认；使用 `--dry-run` 预演不需要二次确认
- 验证安装行为时优先运行 `--dry-run`，确认来源和目标路径正确后再考虑真实安装

# 7. Git 提交信息规则

为当前仓库生成 Git commit message 时，使用 `<scope>: <中文变更摘要>` 格式，并按主要变更对象选择 `scope`。

| 主要变更对象 | 作用域 | 示例 |
| --- | --- | --- |
| 单个 Skill | 与 Skill 目录名一致 | `chinese-markdown: 完善 Mermaid 流程图规则` |
| 备份的 Codex 全局规则 `profile/AGENTS.md` | `global-rules` | `global-rules: 完善本地文件链接引用规则` |
| 备份的 OpenCode 全局配置 `opencode/opencode.jsonc` | `opencode-config` | `opencode-config: 新增 glm-5.3 模型配置` |
| 根目录规则、安装脚本、仓库文档和版本控制配置等仓库自身内容 | `repo` | `repo: 规范 Git 提交信息作用域` |
| 多个不可拆分的 Skill | `skills` | `skills: 统一跨 Skill 的路由规则` |

- `scope` 按提交的主要目的确定，不按发生改动的文件数量确定
- Skill 变更引起的 `README.md`、`install.py`、`scripts/install_codex_profile.py` 或 `CHANGELOG.md` 配套同步，仍使用对应 Skill 名称
- 全局规则变更引起的仓库说明同步，仍使用 `global-rules`
- OpenCode 配置变更引起的 `opencode/install.py`、`opencode/README.md` 或仓库说明同步，仍使用 `opencode-config`
- 一个提交包含多个相互独立的主要目的时，优先拆分提交
