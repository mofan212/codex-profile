# 1. Issue 实现沉淀模板

~~~markdown
# 1. Issue 实现沉淀

## 1.1 记录规则

本文只记录单个 Issue 完成后产生的实现事实，供后续 `ai-retrieval-docs` 归并为正式 AI 检索文档。

不要记录未实现设想、讨论过程、临时猜测、Review 各轮中间讨论或调试流水。

## 1.2 Issue 信息

```yaml
requirement_doc: ""
issue: ""
completed_at: ""
changed_files:
  - ""
```

## 1.3 实现事实

- ""

## 1.4 验证记录

```yaml
validation_commands:
  - ""
validation_results:
  - ""
```

## 1.5 Review 摘要

```yaml
review_method: ""
review_rounds: 0
last_round_result: ""
blocking_findings_resolved:
  - ""
non_blocking_decisions:
  - ""
skip_reason: ""
```

## 1.6 AI 检索提示

```yaml
retrieval_keywords:
  - ""
```

~~~

# 2. 使用规则

每个 Issue 完成时，如果产生需要后续 AI 理解的实现事实，在需求文档同级目录下创建或更新 `.feat-tmp/issues/<需求序号>-<Issue序号>-<Issue简述>-实现沉淀.md`。

`.feat-tmp/` 是临时工作区。正式归档时，使用 `ai-retrieval-docs` 读取需求文档、`.feat-tmp/issues/` 下的实现沉淀文件、实际代码 diff、相关源码、测试、配置和已有 AI 检索文档后，生成或更新最终 AI 检索文档。

确认 AI 检索文档已经覆盖 `.feat-tmp/` 中需要长期保留的入口、调用链、配置项、数据结构、验证命令和排查关键词后，按当前运行环境的文件删除、安全审批和跨项目修改规则处理 `.feat-tmp/` 临时目录；如果需要审批，先请求确认。
