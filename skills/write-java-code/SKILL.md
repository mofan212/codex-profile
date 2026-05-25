---
name: write-java-code
description: Write, modify, refactor, and test Java backend code. Use only when Codex needs to implement or change Java 8, Spring, Spring Boot, Spring MVC, MyBatis, Jackson, or Lombok backend code or tests, including service, domain, controller, mapper, DTO, utility, enum, exception-handling, logging, compatibility adjustments, and focused verification. Do not use for pure bug analysis, log analysis, root-cause investigation, general code review, or design discussion unless the user asks for Java code or test changes.
---

# 1. 工作流程

## 1.1 先建立事实

- 先读取相关源码、测试、配置、接口定义、调用方、同包类、父类或接口，再设计方案或修改代码。
- 使用 `rg` 或同类快速搜索工具定位类、方法、Bean、Mapper、DTO、枚举、异常和测试覆盖。
- 优先贴合当前代码库已有架构、命名、分层、异常处理和测试风格；当前上下文缺少明确模式时，再使用本 Skill 的默认规范。
- 如果需求、输入输出、兼容性或业务边界不明确，先向用户确认；如果事实与用户表述冲突，直接指出并给出依据。

## 1.2 小步实现

- 遵循 KISS 原则，只实现当前目标需要的最小改动，不做非必要封装、抽象或模式化设计。
- 优先复用现有工具类、领域模型、接口契约、配置项和项目内通用写法。
- 保持实现简单直接，用早返回减少嵌套，用项目已有工具类表达常见空值、集合和缺省值处理。
- 不回滚用户未要求回滚的改动；遇到无关工作区变更时，只处理当前任务相关文件。

# 2. Java 实现规则

## 2.1 结构与命名

- 让类、方法和参数名称表达业务含义，职责保持单一，避免扩大接口行为面。
- 任务类、调度类和入口类优先只做流程编排；复杂对象构造、字段填充和分组转换下沉到专门构造类或工厂类。
- 只有存在真实 `is-a` 语义时才使用继承；不要为了复用静态工具能力引入语义不成立的继承关系。
- 除非存在同名类冲突，Java 正文中不要书写类的全限定名，统一在文件头部使用 `import`。

## 2.2 兼容与依赖

- 新代码不要依赖已废弃类或职责偏移的历史工具类；需要兼容旧调用点时，让旧类静态转发到新的稳定入口。
- 发现新增代码直接依赖 `@Deprecated` 类、方法或职责明显偏移的历史工具类时，必须作为问题反馈；除非该依赖是旧兼容入口，且旧类只做静态转发。
- 如果必须复用已废弃类中的常量、判断逻辑或命名规则，先抽取到非废弃的稳定领域工具类；新代码依赖稳定入口，旧类只保留兼容转发。
- 使用 Stream、Optional、lambda 等 Java8 特性时，确保可读性优于技巧展示。

## 2.3 Web、MyBatis 与日志

- 编写 Web 层接口时，如果项目已有扩展业务注解、权限注解或参数描述注解，优先沿用既有约定；不要在没有现有模式的项目中主动引入。
- 修改 MyBatis 相关代码时，同步检查 Mapper 接口、XML、参数名、返回映射和调用方。
- 有日志需求时优先沿用项目已有日志方案；项目使用 Lombok 时可优先使用 `@Slf4j`。打印异常时必须保留完整异常堆栈和必要上下文变量，禁止使用标准控制台输出替代日志。

## 2.4 类注释和作者

- 新建 `.java` 类文件时，按用户或仓库约定补充类级文档注释；如果已有类似注释，不修改其内容。
- 新建 `.java` 类文件且需要生成作者注释时，优先读取当前目标仓库生效的 Git 用户名：`git config user.name`。如果无法获取 `user.name`，不要写死默认作者名，先询问用户或省略 `@author`。日期使用当前系统时间，精确到分钟。

# 3. 测试与验证

## 3.1 测试策略

- 优先运行与修改范围最相关的单元测试、模块测试或编译命令。
- 涉及行为变化时补充聚焦单测，沿用当前模块已有测试框架和断言风格。
- Mock 范围聚焦外部依赖，断言优先使用 AssertJ；如果项目已有统一断言工具，跟随项目。

## 3.2 验证反馈

- 如果无法运行测试或编译，说明原因，并列出已经完成的静态检查或人工核对范围。
- 回复用户时使用中文，简明说明修改了什么、验证了什么、是否存在未完成风险。
- 如果用户请求 Git commit，commit message 要准确、精简，且不超过 30 字。

# 4. 按需读取参考

## 4.1 详细 Java 规范

需要生成新类、重构较大方法、补单测，或拿不准命名、结构、异常处理和测试风格时，读取 [references/java-code-guide.md](references/java-code-guide.md)。
