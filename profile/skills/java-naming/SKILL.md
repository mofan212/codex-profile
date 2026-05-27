---
name: java-naming
description: Design, review, rename, and place Java backend package paths and class names. Use when Codex needs package hierarchy decisions, domain or responsibility package selection, class role suffix selection, interface and implementation naming, consistency checks against nearby Java code, or guidance to avoid DTO/VO/DAO/DO/PO/BO/POJO suffix taxonomies except when preserving existing repository compatibility.
---

# 1. Java 结构命名规则

使用本 Skill 为 Java 后端代码选择包路径、类名和角色后缀。命名前先阅读当前代码上下文，优先遵循所在仓库、模块、同级包和相邻类的既有风格。

不要引入 `DTO`、`VO`、`DAO`、`DO`、`PO`、`BO`、`POJO` 等对象后缀命名体系。如果仓库里已经存在这类名称，可以为了兼容继续保留，但不要把它们作为新增命名规则的依据。

# 2. 工作流程

## 2.1 先确定命名对象

先明确要命名的是包、普通类、接口、抽象类、异常、测试类、工具类还是配置类。不要在职责没有确定前先套后缀。

如果需求只是评审命名，输出应包含：

- 当前命名是否可接受；
- 更推荐的命名；
- 推荐理由和需要保留现名的兼容理由。

## 2.2 再阅读局部代码

命名包或类之前，先检查相关上下文，不要凭通用偏好改名：

- 识别当前模块、业务域和职责边界；
- 查看同级包名和相邻类名后缀；
- 沿用仓库内已经稳定的领域词拼写，例如 `OrderId` 和 `OrderID` 之间不要随意切换；
- 检查是否已有同职责类、接口、抽象基类、测试类或常量类；
- 不要为了统一风格而主动重命名既有代码。

## 2.3 选择包路径

包路径用于表达归属、模块、业务域和职责：

```text
com.company.project.module.domain.responsibility
```

各层含义：

- `company/project`：组织和项目归属；
- `module`：可部署模块或主要技术模块；
- `domain`：业务域或能力边界；
- `responsibility`：该包内类的主要职责。

包名全部小写，语义层级之间使用点号分隔，不使用下划线或中划线。优先使用单数形式，例如 `executor`、`context`、`resolver`、`helper`、`util`、`constant`、`exception`。

## 2.4 选择职责包

根据真实职责选择最窄的包名：

- `appservice`：面向应用层的服务入口；
- `controller`：Web 或 API 入口；
- `executor`：执行任务、命令、作业或运行时单元；
- `handler`：处理特定事件、动作、请求或回调；
- `context`：贯穿调用链传递执行状态；
- `resolver`：解析值、表达式、变量、类型或引用；
- `converter`：转换数据结构或类型体系；
- `parser`：解析文本、表达式、协议或元数据；
- `proxy`：代理或适配外部系统、远程能力；
- `listener`：监听事件或消息；
- `component`：可复用运行时组件或描述结构；
- `constant`：常量；
- `enums`：枚举；
- `exception`：异常；
- `helper`：辅助协作者，通常需要依赖注入或协调既有 API；
- `util`：无状态工具方法；
- `support`：某个更具体父包下的内部支撑类。

当某个职责包变大时，继续按业务对象、业务场景或稳定子域拆分：

```text
handler.order
handler.payment
handler.inventory
handler.notification
handler.notification.support
```

# 3. 类命名规则

## 3.1 基本结构

类名使用大驼峰。优先使用名词或名词短语，并让业务对象或动作在前、角色在后。推荐结构：

```text
业务对象或动作 + 角色后缀
```

示例：

```text
OrderPaymentExecutor
CreateOrderHandler
PaymentHandlerDispatcher
RequestContext
ExpressionValueResolver
OrderOperationHelper
OrderProcessingException
OrderServiceConstants
```

## 3.2 角色后缀选择

根据真实职责选择后缀。能用精确后缀时，不要退回到模糊的 `Service`、`Manager`、`Helper` 或 `Utils`。

- `Engine`：核心执行或编排引擎，谨慎使用；
- `Executor`：执行任务、命令、作业或运行时单元；
- `Dispatcher`：按类型选择并分发到对应执行器或处理器；
- `Handler`：承载动作、事件、请求或回调的具体处理逻辑；
- `Processor`：处理一段流程或一批规则；
- `Manager`：管理有状态资源或生命周期；
- `Context`：贯穿调用链传递执行状态；
- `Factory`：创建对象或策略；专门构造对象且无状态时，优先提供静态 `from(...)` 入口，内部辅助方法保持静态；
- `Provider`：提供实现、策略或能力；
- `Resolver`：解析表达式、值、变量或引用；
- `Converter`：转换数据或类型结构；
- `Parser`：解析结构化输入；
- `Builder`：分步骤构建复杂对象；
- `Proxy`：代理或委托外部系统；
- `Listener`：观察事件或消息；
- `Callback`：回调契约；
- `Task`：可运行任务或调度任务；
- `Service`：业务服务或应用服务，不要作为模糊默认后缀；
- `Controller`：HTTP 或 API 控制器；
- `Constants`：常量持有类；
- `Enum`：仅当仓库已有该风格时作为枚举后缀；
- `Exception`：异常类型；
- `Thrower`：集中抛出或构造领域异常；
- `Utils`：无状态工具类；稳定公共工具能力优先使用该后缀，不要让旧工具类通过继承获得工具能力；
- `Helper`：辅助协作者，适合需要依赖或协调既有 API 的类；
- `Support`：特定包内的内部支撑类；仅在语义明确且比 `Utils`、`Factory`、`Helper` 更准确时使用，避免作为模糊默认后缀；
- `Accessor`：对复杂结构做计算式或中介式访问；
- `Generator`：生成代码、ID、Key 或产物；
- `Formatter`：格式化字符串、日期、数字或展示值；
- `Validator`：校验输入或状态；
- `Strategy`：可替换策略；
- `Adapter`：适配一个接口或模型到另一个接口或模型；
- `Command` 或 `Action`：可执行的用户动作或领域动作；
- `Event`：事件对象；
- `Template`：可复用的算法骨架。

## 3.3 抽象类、实现类和测试类

抽象类在提供共享行为时使用 `Abstract` 或 `Base` 前缀：

```text
AbstractOrderCommandHandler
BasePaymentExecutor
```

只有在存在稳定接口且可能有多个实现，或仓库已有这种约定时，才使用 `Impl` 后缀。

接口不要机械添加 `I` 前缀。优先让接口表达能力或契约，例如 `PaymentHandler`、`ValueResolver`。实现类应说明差异点，例如 `DefaultValueResolver`、`ExpressionValueResolver`，而不是默认使用 `PaymentHandlerImpl`。

测试类使用：

```text
被测类名 + Test
```

# 4. 决策原则

## 4.1 优先级

按以下顺序决策：

1. 仓库或模块已有强约定。
2. 同级包和相邻类的稳定风格。
3. 本 Skill 的通用规则。

当本 Skill 与仓库既有风格冲突时，优先保留本地一致性，并在回答中说明这是兼容决策。

## 4.2 命名禁区

避免以下做法：

- 用 `Service`、`Manager`、`Helper`、`Utils` 掩盖真实职责；
- 为一个类新增过深包层级；
- 为了套设计模式后缀而改变语义；
- 用继承复用工具能力，除非存在真实 `is-a` 关系；
- 把临时需求名、页面文案、中文拼音或缩写写进稳定类名；
- 将对象传输、持久化、展示等分层后缀作为新增体系。

# 5. 决策检查

最终确定名称前，检查以下事项：

- 包路径是否表达了模块、业务域和职责；
- 类名是否以业务对象或动作开头；
- 后缀是否描述了这个类真正承担的职责；
- 类之间的继承关系必须表达真实 `is-a` 语义；兼容旧类时优先静态转发或组合，不要用语义不成立的继承；
- 不要为了一个类新增包层级，除非该层级表达稳定边界；
- 只有当类确实承担对应模式职责时，才使用设计模式类后缀。

如果需要给出结果，优先使用简短列表：

- `package`：推荐包路径；
- `class`：推荐类名；
- `reason`：关键理由；
- `compatibility`：需要兼容既有命名时说明依据。
