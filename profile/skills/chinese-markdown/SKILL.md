---
name: chinese-markdown
description: Write, edit, format, or review Chinese Markdown documents with strict typography and heading rules. Use when creating or modifying Chinese Markdown articles, requirements, README files, design docs, AI docs, Skill docs, checklists, or any Markdown content that should follow Chinese spacing, quote, inline syntax, and numbered heading conventions.
---

# 1. 中文 Markdown 编写规则

使用本 Skill 编写、修改、格式化或审查中文 Markdown 文档。优先保证标题层级稳定、编号连续、内容层次清楚，并保持标点、空格和 Markdown 行内语法间距一致。

# 2. 标点和间距

- 中文引号使用 `「」`，不要使用中文弯引号
- 中文与英文、数字或代码词相邻时，中间使用一个半角空格隔开
- Markdown 行内代码、链接、强调等语法与中文内容相邻时，两侧留一个半角空格
- Markdown 行内语法与中文标点相邻时，不强制在标点前后加空格；行内代码后接顿号、逗号、句号、分号、冒号、问号或感叹号时，通常保持紧邻

示例：

```markdown
正确：运行 `example --help` 查看可用参数
错误：运行`example --help`查看可用参数

正确：不要引入 `Spec`、`Options`、`Config`。
错误：不要引入 `Spec` 、 `Options` 、 `Config` 。

正确：配置项包括 `timeout`、`retry`；默认值使用 `false`。
错误：配置项包括`timeout`、`retry`；默认值使用`false`。

正确：请 **先确认范围** 再继续修改
错误：请**先确认范围**再继续修改

正确：参考 [使用说明](guide.md) 完成配置
错误：参考[使用说明](guide.md)完成配置
```

# 3. 标题规则

文章内容最多只使用 1 级标题和 2 级标题。2 级标题必须属于前一个 1 级标题。

每个标题前都要指定序号，并按层级连续递增，例如：

```markdown
# 1. 标题
## 1.1 标题

# 2. 标题
```

不要只保留一个 1 级标题并把所有内容塞进 2 级标题。需要更细层级时，优先使用引用块或列表，不要继续新增 3 级或更深标题。

示例：

```markdown
正确：
# 1. 背景
## 1.1 当前问题

# 2. 方案
## 2.1 实施步骤

错误：
# 1. 项目说明
## 1.1 背景
## 1.2 当前问题
## 1.3 方案
## 1.4 实施步骤
```

需要表达更细层级时：

```markdown
正确：
## 2.1 实施步骤

> 准备配置文件

准备配置文件的内容...

> 运行校验命令

运行校验命令的内容...

> 根据结果进行调整

根据结果进行调整的内容...

错误：
## 2.1 实施步骤
### 2.1.1 准备配置文件

准备配置文件的内容...

### 2.1.2 运行校验命令

运行校验命令的内容...

### 2.1.3 根据结果进行调整

根据结果进行调整的内容...
```

# 4. 输出和最终检查

交付前检查：

- 不存在中文弯引号，必要时已替换为 `「」`
- 中文与英文、数字或代码词之间已留空格
- Markdown 行内语法两侧与中文内容留有一个半角空格
- Markdown 行内语法与中文标点紧邻时没有误判为缺少空格
- 标题只使用 1 级和 2 级
- 标题编号连续且层级正确
