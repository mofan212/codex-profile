---
name: write-chinese-markdown
description: Write, edit, format, or review Chinese Markdown documents with strict typography and heading rules. Use when Codex creates or modifies Chinese Markdown articles, requirements, README files, design docs, AI docs, Skill docs, checklists, or any Markdown content that should follow Chinese spacing, quote, inline syntax, and numbered heading conventions.
---

# 1. 中文 Markdown 编写规则

使用本 Skill 编写、修改或审查中文 Markdown 文档。优先保证文档结构清晰、标题层级稳定、中文排版一致。

# 2. 标点和间距

内容中不要使用中文弯引号，使用 `「」` 代替。

中英文之间使用空格隔开。

Markdown 行内语法与中文内容使用空格隔开。

# 3. 标题规则

文章内容中优先使用 1 级标题，2 级标题必须被包含在 1 级标题下，且每个标题前都要指定序号，并依次增加，例如：

```markdown
# 1. xxx
## 1.1 xxx

# 2. xxx
## 2.1 xxx
```

文章内容中最多只能包含 1 级标题和 2 级标题。如果有需要，可以使用 `>` 语法代替 3 级标题。

文章内容中不能只包含 1 个 1 级标题，然后将其他标题都用 2 级标题展示。下面是不推荐的做法：

```markdown
# 1. xxx
## 1.1 aaa
## 1.2 bbb
## 1.3 ccc
```

# 4. 最终检查

交付前检查：

- 是否存在中文双引号；
- 中英文之间是否缺少空格；
- Markdown 行内语法两侧是否与中文内容留有空格；
- 标题是否只使用 1 级和 2 级；
- 标题编号是否连续且层级正确。
