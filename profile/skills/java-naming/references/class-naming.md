# 1. 类命名规则

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

需要选择或解释角色后缀时，读取 [role-suffixes.md](role-suffixes.md)。需要判断 `Dto` 或 `Dao` 边界时，读取 [dto-dao-naming.md](dto-dao-naming.md)。

# 2. 组合命名方式

类名应先表达业务对象，再表达动作、边界或角色。可以组合多个语义，但不要把后缀堆成难读的长串。

| pattern | example | use_when |
| --- | --- | --- |
| 业务对象 + 角色 | `PaymentHandler`、`InventoryTracker` | 类围绕单一业务对象承担稳定职责 |
| 动作 + 业务对象 + 角色 | `CreateOrderHandler`、`ValidatePaymentCommand` | 类表达一次明确动作或命令 |
| 边界对象 + 入出方向 | `OrderResponse`、`PaymentCallback` | 类位于接口、消息或外部系统边界 |
| 领域能力 + 基础设施角色 | `OrderMetricReporter`、`TraceContextPropagator`、`PaymentHandlerRegistrar` | 类连接领域能力和基础设施行为 |
| 执行链路 + 结构角色 | `AuthenticationFilterChain`、`RequestCodec`、`MessagePacket` | 类描述协议、链路或数据结构角色 |

当类名超过 4 个语义片段时，先检查是否承担了过多职责。优先拆分类职责，而不是继续追加后缀。

# 3. 抽象类、实现类和测试类

| 类型 | 命名规则 | 示例 | 禁止事项 |
| --- | --- | --- | --- |
| 抽象类 | 提供共享行为时使用 `Abstract` 或 `Base` 前缀 | `AbstractOrderCommandHandler`、`BasePaymentExecutor` | 没有共享行为时套抽象类前缀 |
| 实现类 | 说明差异点 | `DefaultValueResolver`、`ExpressionValueResolver` | 默认使用 `PaymentHandlerImpl` |
| `Impl` 后缀 | 仅在存在稳定接口且可能有多个实现，或仓库已有这种约定时使用 | `PaymentHandlerImpl` | 为所有接口实现机械追加 `Impl` |
| 接口 | 表达能力或契约 | `PaymentHandler`、`ValueResolver` | 机械添加 `I` 前缀 |
| 测试类 | `被测类名 + Test` | `PaymentHandlerTest` | 使用无法定位被测对象的测试名 |

# 4. 类命名禁区

| forbidden | reason | alternative |
| --- | --- | --- |
| 用 `Service`、`Manager`、`Helper`、`Utils` 掩盖真实职责 | 名称无法表达稳定责任 | 使用业务对象、动作和角色后缀组合 |
| 为了套设计模式后缀而改变语义 | 类名会误导使用者 | 只有承担对应模式职责时才使用模式后缀 |
| 用继承复用工具能力 | 没有真实 `is-a` 关系 | 使用组合、静态转发或工具方法 |
| 把临时需求名、页面文案、中文拼音或缩写写进稳定类名 | 名称容易随需求文案变化 | 使用稳定领域词 |
| 将对象传输、持久化、展示等分层后缀作为新增体系 | 容易引入 VO/DO/PO/BO/POJO 分类膨胀 | 涉及对象后缀边界时读取 [dto-dao-naming.md](dto-dao-naming.md) |

# 5. 类名检查

| check_item | pass_condition |
| --- | --- |
| 起始语义 | 类名以业务对象或动作开头 |
| 角色后缀 | 后缀描述这个类真正承担的职责 |
| 继承语义 | 类之间的继承关系表达真实 `is-a` 语义；兼容旧类时优先静态转发或组合 |
| 设计模式后缀 | 类确实承担对应模式职责 |
