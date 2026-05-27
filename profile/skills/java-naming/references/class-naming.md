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

类名应先表达业务对象，再表达动作、边界或角色。可以组合多个语义，但不要把后缀堆成难读的长串。常见组合方式：

```text
业务对象 + 角色：PaymentHandler、InventoryTracker
动作 + 业务对象 + 角色：CreateOrderHandler、ValidatePaymentCommand
边界对象 + 入出方向：OrderResponse、PaymentCallback
领域能力 + 基础设施角色：OrderMetricReporter、TraceContextPropagator、PaymentHandlerRegistrar
执行链路 + 结构角色：AuthenticationFilterChain、RequestCodec、MessagePacket
```

当类名超过 4 个语义片段时，先检查是否承担了过多职责。优先拆分类职责，而不是继续追加后缀。

# 3. 抽象类、实现类和测试类

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

# 4. 类命名禁区

避免以下做法：

- 用 `Service`、`Manager`、`Helper`、`Utils` 掩盖真实职责；
- 为了套设计模式后缀而改变语义；
- 用继承复用工具能力，除非存在真实 `is-a` 关系；
- 把临时需求名、页面文案、中文拼音或缩写写进稳定类名；
- 将对象传输、持久化、展示等分层后缀作为新增体系；涉及对象后缀边界时读取 [dto-dao-naming.md](dto-dao-naming.md)。

# 5. 类名检查

最终确定类名或后缀前，检查以下事项：

- 类名是否以业务对象或动作开头；
- 后缀是否描述了这个类真正承担的职责；
- 类之间的继承关系必须表达真实 `is-a` 语义；兼容旧类时优先静态转发或组合，不要用语义不成立的继承；
- 只有当类确实承担对应模式职责时，才使用设计模式类后缀。
