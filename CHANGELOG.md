# 1. 记录范围

`CHANGELOG.md` 只记录用户在拉取、安装或使用新版本后需要感知或采取行动的重要变化，例如安装行为、能力增删、使用入口、外部依赖和兼容性变化。规则措辞、模型适配、内部执行策略、文档结构和排版优化由 Git 提交历史记录。

本文件自 2026-07-16 起维护；此前变化以 Git 提交历史为准。

# 2. 更新记录

日期节点按倒序排列。当天日期节点已存在时，将新变更追加到该节点的列表末尾；当天日期节点不存在时，在本节开头新增日期节点。

> 2026-08-25

- Codex 全局规则备份从 `profile/AGENTS.md` 更名为 `profile/codex-global-rules.md`，避免从 `profile/` 启动 Codex 时被误识别为项目规则；安装目标仍为 `~/.codex/AGENTS.md`

> 2026-08-24

- Skills 安装目录从 `~/.codex/skills/` 改为 `~/.agents/skills/`（Codex 和 OpenCode 共用）；`install.py` 新增 `--agents-home` 参数，用于指定 `.agents` 目录（默认 `~/.agents`），Skills 会安装到该目录下的 `skills/` 子目录
- 新增 `scripts/cleanup_legacy_codex_skills.py`，曾用旧版安装过的用户需运行一次，清理 `~/.codex/skills/` 中的旧安装
- 新增可公开同步的 OpenCode 配置和独立安装脚本，安装时从 `OPENCODE_CUSTOM_BASE_URL` 或交互输入注入实际 provider 地址，详见 [OpenCode 配置同步说明](opencode/README.md)

> 2026-08-14

- 新增 `goal-prompt`，可通过 `$goal-prompt` 手动生成用于新会话的 Goal 提示词
- 新增 `gen-commit-message`，可通过 `$gen-commit-message` 手动为当前项目变更生成 commit message
- `goal-prompt` 更名为 `gen-goal-prompt`，重新运行 `python install.py` 后会移除旧名称并安装新名称

> 2026-08-11

- 移除 `load-project-context`，重新运行 `python install.py` 后会移除已安装版本
- `ai-retrieval-docs` 更名为 `maintain-ai-context-docs`，并新增项目上下文路由维护与连通性检查，重新安装后生效

> 2026-08-04

- `feat` Skill 改为仅支持 `$feat` 手动调用，并禁用隐式调用

> 2026-07-16

- 删除 `coding-guidelines` Skill，并移除 `README.md` 中的对应条目
