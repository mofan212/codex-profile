# OpenCode 配置同步

本目录保存可公开同步的 OpenCode 全局配置，需独立安装，根目录 `install.py` 不处理。

## 配置文件

`opencode.jsonc` 包含全局指令位置和候选模型配置。其中 `instructions` 使用 `~/.codex/AGENTS.md`，`~` 由 OpenCode 展开为当前用户主目录，不写死用户名。

模型统一配置在逻辑 provider `custom` 下。仓库不保存真实提供商名称和地址，`baseURL` 使用环境变量占位符 `{env:OPENCODE_CUSTOM_BASE_URL}`。

配置文件的真实安装会整体覆盖 `~/.config/opencode/opencode.jsonc`，不会合并本机已有内容。安装脚本按以下顺序获取实际 `baseURL`：

1. 优先读取环境变量 `OPENCODE_CUSTOM_BASE_URL`
2. 环境变量不存在时，在交互终端提示输入
3. 非交互环境缺少该变量时停止安装

输入值必须是包含主机名的 HTTP 或 HTTPS URL。脚本只将实际地址写入目标配置，不修改仓库中的占位符，也不会在输出中显示地址。

`--dry-run` 不会请求输入，只报告环境变量是否已配置以及预计写入路径。先预演确认目标路径和覆盖范围，再执行安装：

```powershell
python opencode/install.py --dry-run
python opencode/install.py
```

真实安装会在覆盖配置前要求确认。需要非交互执行时传入 `--yes`。

安装后需要重启 OpenCode，配置才会生效。

## 不同步内容

真实 provider 地址、API 密钥、数据库、快照和工具输出不纳入本目录备份，例如 `auth.json`、`opencode.db`、`snapshot/` 和 `tool-output/`。不要把安装后包含真实地址的目标配置复制回仓库。
