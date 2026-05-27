# 1. 项目定位

- 当前仓库是 Codex Profile 备份仓库，用于保存可迁移的 Codex 配置源码
- 根目录 `AGENTS.md` 只约束 AI 在当前仓库中的行为，不是要安装到 Codex 全局目录的备份文件
- 要备份和安装的 Codex 全局规则位于 `profile/AGENTS.md`
- 要备份和安装的自定义 Skill 位于 `profile/skills/`

# 2. 修改边界

- 用户要求修改 Codex 全局规则时，默认修改 `profile/AGENTS.md`
- 用户要求修改 Skill、调整 Skill 文档或新增 Skill 时，默认修改 `profile/skills/` 下的内容
- 不要把备份用的 `profile/AGENTS.md` 或 `profile/skills/` 移回仓库根目录
- 除非用户明确要求安装、同步到本机或修改真实 Codex 配置目录，否则不要修改 `~/.codex/AGENTS.md`、`~/.codex/skills/` 或其他已安装目录
- 如果用户只说「修改 skill」「改全局规则」「更新配置」，必须先理解为修改当前仓库中的备份源码；如果仍然无法判断目标位置，先向用户确认
- 如果新增、删除、重命名或调整 `profile/skills/` 下的 Skill 目录结构，必须同步检查并按需维护 `install.py` 和 `README.md` 中的路径、Skill 列表与安装说明
- 如果修改 `profile/skills/` 下各 Skill 之间的软依赖、切换关系或协作边界，必须同步维护 `README.md` 中的 Skill 软依赖关系说明

# 3. 文档边界

- `README.md` 面向人类读者，不用于承载 AI 行为规则
- 项目级 AI 行为规则应写在根目录 `AGENTS.md`
- 除非用户明确要求更新面向人类的说明文档，否则不要为了约束 AI 行为而修改 `README.md`

# 4. 安装脚本边界

- `install.py` 应从 `profile/AGENTS.md` 和 `profile/skills/` 安装到目标 Codex 目录
- `install.py` 真实安装时会整体替换目标目录中同名 Skill，不会合并目录，也不会保留目标同名 Skill 目录中的额外文件
- 如果由 AI 执行 `python install.py` 进行真实安装，必须先向用户说明上述覆盖规则，并获得用户二次确认；`python install.py --dry-run` 不需要二次确认
- 调整备份目录结构时，必须同步检查并更新 `install.py`
- 验证安装行为时优先运行 `python install.py --dry-run`，确认来源和目标路径正确后再考虑真实安装
