---
name: chinese-markdown
description: Write, edit, format, or review Chinese Markdown documents with strict typography and heading rules. Use when Codex creates or modifies Chinese Markdown articles, requirements, README files, design docs, AI docs, Skill docs, checklists, or any Markdown content that should follow Chinese spacing, quote, inline syntax, and numbered heading conventions.
---

# 1. 中文 Markdown 编写规则

使用本 Skill 编写、修改、格式化或审查中文 Markdown 文档。优先保证标题层级稳定、编号连续、内容层次清楚，并保持标点、空格和 Markdown 行内语法间距一致。

# 2. 标点和间距

- 中文引号使用 `「」`，不要使用中文弯引号。
- 中文与英文、数字或代码词相邻时，中间使用空格隔开。
- Markdown 行内代码、链接、强调等语法与中文内容相邻时，两侧留空格。

# 3. 标题规则

文章内容最多只使用 1 级标题和 2 级标题。2 级标题必须属于前一个 1 级标题。

每个标题前都要指定序号，并按层级连续递增，例如：

```markdown
# 1. 标题
## 1.1 标题

# 2. 标题
```

不要只保留一个 1 级标题并把所有内容塞进 2 级标题。需要更细层级时，优先使用引用块或列表，不要继续新增 3 级或更深标题。

# 4. 输出和最终检查

交付前检查：

- 不存在中文弯引号，必要时已替换为 `「」`。
- 中文与英文、数字或代码词之间已留空格。
- Markdown 行内语法两侧与中文内容留有空格。
- 标题只使用 1 级和 2 级。
- 标题编号连续且层级正确。
