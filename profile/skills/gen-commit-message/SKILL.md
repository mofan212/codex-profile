---
name: gen-commit-message
description: 为当前项目的全部现有变更生成 commit message。
---

检查当前项目中的全部现有变更，不以当前会话为范围。当前目录不是 Git 仓库或没有变更时，停止并说明。

发现未追踪文件时，执行 `🔴 CHECKPOINT`：列出文件并询问哪些需要暂存、哪些仅在本次忽略。只在用户明确确认后暂存指定文件；本次忽略的文件不纳入 message，也不修改 `.gitignore`。

生成 message 时：

1. 先查找并遵循项目已明确的 commit message 规则
2. 项目无规则时，参考当前 Git 用户最近 5 条提交的格式
3. 无可参考记录时，用简洁单行概括主要变更

只输出一个可直接复制的 commit message，不执行 `git commit`。
