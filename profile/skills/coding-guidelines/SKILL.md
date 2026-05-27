---
name: coding-guidelines
description: Coding-task execution guidelines that constrain Codex to explicit assumptions, minimal viable changes, KISS design, small scoped edits, and goal-driven verification. Use when implementing, debugging, fixing bugs, refactoring, adding tests, reviewing code, clarifying ambiguous requirements, avoiding opportunistic refactors, or when the user asks for small steps, minimal changes, assumption checks, or verification-focused delivery.
---

# Coding Guidelines

> Reference: https://linux.do/t/topic/1977532

## Overview

在开始实现前，先把任务收敛成清晰假设、最小方案和可验证目标。
在改动现有代码时，只触碰与需求直接相关的部分，不把「顺手优化」混进本次提交。

## Working Rules

### 1. Think Before Coding

- 先明确需求中的已知项、未知项和你的假设。
- 如果存在两种以上合理解释，先说明分歧点，不要静默选择其一。
- 如果更简单的方案可行，主动指出，不为了「未来扩展」增加复杂度。
- 如果关键信息缺失且误判风险高，先停下来澄清，再实现。

对外表达时，优先使用这种句式：

- 「我的理解是……」
- 「这里我先假设……」
- 「如果你希望的是另一种含义，我会改成……」

### 2. Simplicity First

- 只写完成当前目标所需的最少代码。
- 不提前抽象单次使用的逻辑。
- 不添加用户没要求的配置项、可扩展层或兜底分支。
- 不为了展示「健壮性」去处理实际上不可能发生的场景。
- 如果实现明显比需求更复杂，先回退并简化。

每次准备提交前，自查一句：
「这段代码是否会被资深工程师评价为过度设计？」

### 3. Surgical Changes

- 只修改与当前需求直接相关的文件和代码块。
- 不顺手整理无关格式、命名、注释或相邻模块。
- 不重构没坏的代码。
- 延续现有项目风格，除非用户明确要求统一或重构。
- 只删除因本次改动而新增的无用导入、变量、分支和函数。
- 发现既有死代码或历史问题时，可以提示，但不要擅自清理。

判断标准：
每一处改动都应当能直接追溯到用户请求，或者是让该请求成立所必需的配套改动。

### 4. Goal-Driven Execution

- 把模糊任务改写成可验证目标后再动手。
- 能写测试复现的，先写复现，再修复，再验证通过。
- 不能写测试的，也要给出明确检查点，例如页面行为、命令输出、接口返回或构建结果。
- 多步骤任务先写一个简短计划，每步都带验证方式。

使用这种格式组织执行：


1. [步骤] -> verify: [如何确认完成]
2. [步骤] -> verify: [如何确认完成]
3. [步骤] -> verify: [如何确认完成]


## Response Style

- 优先简短、直接、可执行的表达。
- 先说理解和假设，再说实现。
- 对风险、取舍和不确定性保持显式。
- 在完成后汇报：改了什么、如何验证、还有什么残余风险。

## Anti-Patterns

避免这些常见错误：

- 没确认需求边界就直接开写。
- 为了「以后可能会用到」加入抽象层。
- 把功能修复和无关重构混在一起。
- 没验证就宣布完成。
- 用很多代码掩盖对问题理解不清。

## Quick Checklist

开始前检查：

- 我是否写清了假设？
- 我是否选择了最简单可行方案？
- 我的计划是否有明确验证点？

提交前检查：

- 是否存在与需求无关的改动？
- 是否有更短、更直接的实现？
- 是否已经完成测试、构建或其他必要验证？
