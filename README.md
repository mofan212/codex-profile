# 1. Codex Profile

这个仓库用于同步个人 Codex 全局配置，只保存可迁移的配置源码。

当前包含：

- `AGENTS.md`：个人全局规则
- `skills/`：个人自定义 Skills
- `install.py`：Windows、macOS、Linux 通用安装脚本

# 2. 使用方式

在新机器上 clone 本仓库后，执行：

```bash
python3 install.py
```

Windows 环境如果命令名是 `python`，执行：

```powershell
python install.py
```

脚本会把 `AGENTS.md` 和 `skills/` 复制到当前用户的 `~/.codex` 目录。

# 3. 预演安装

如果想先确认会写入哪些文件，可以执行：

```bash
python3 install.py --dry-run
```

Windows PowerShell：

```powershell
python install.py --dry-run
```

# 4. 指定 Codex 目录

默认安装目录是当前用户的 `~/.codex`。如需指定目录：

```bash
python3 install.py --codex-home /path/to/.codex
```

Windows PowerShell：

```powershell
python install.py --codex-home C:\Users\YourName\.codex
```

# 5. 不同步内容

不要把 Codex 运行时状态放进本仓库，例如：

- `sessions/`
- `archived_sessions/`
- `log/`
- `tmp/`
- `sqlite/`
- `plugins/`
- `*.sqlite`
- `history.jsonl`

这些内容通常和本机状态、缓存、会话历史或安装环境相关，不适合跨机器共享。

# 6. 日常流程

修改配置后提交：

```bash
git add .
git commit -m "更新 Codex 配置"
git push
```

另一台机器同步：

```bash
git pull
python3 install.py
```

Windows PowerShell 如果使用 `python` 命令名：

```powershell
git pull
python install.py
```
