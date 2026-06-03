# 1. 角色后缀选择

根据真实职责选择后缀。能用精确后缀时，不要退回到模糊的 `Service`、`Manager`、`Helper` 或工具类后缀。

# 2. 常见后缀

- `Engine`：核心执行或编排引擎，谨慎使用
- `Bootstrap` 或 `Starter`：程序、服务、框架或运行时组件的启动入口
- `Executor`：执行任务、命令、作业或运行时单元
- `Dispatcher`：按类型选择并分发到对应执行器或处理器
- `Handler`：承载动作、事件、请求或回调的具体处理逻辑
- `Processor`：处理一段流程或一批规则
- `Manager`：管理有状态资源或生命周期
- `Holder`：持有对象引用、全局集合、缓存容器或不易直接回收的资源
- `Registrar`：注册并维护一组资源、插件、处理器或扩展点
- `Context`：贯穿调用链传递执行状态
- `Propagator`：复制、注入、恢复、清理或传播 `Context` 中的值
- `Factory`：创建对象或策略；专门构造对象且无状态时，优先提供静态 `from(...)` 入口，内部辅助方法保持静态
- `Provider`：提供实现、策略或能力
- `Resolver`：解析表达式、值、变量或引用
- `Converter`：转换数据或类型结构
- `Parser`：解析结构化输入
- `Customizer`：对复杂对象执行专门配置或定制
- `Builder`：分步骤构建复杂对象
- `Proxy`：代理或委托外部系统
- `Listener`：观察事件或消息
- `Callback`：回调契约
- `Aware`：表示实现类可被容器回调并感知某个基础设施对象，例如上下文、事件发布器或环境
- `Trigger`：触发定时、规则或事件动作；仅在语义确实是触发器时使用
- `Task`：可运行任务或调度任务
- `Service`：业务服务或应用服务，不要作为模糊默认后缀
- `Controller`：HTTP 或 API 控制器
- `Request` 和 `Response`：网络、HTTP、RPC、消息或明确的调用边界上的入参和出参；不要把普通方法参数都命名为 `Request`
- `Constants`：常量持有类
- `Enum`：仅当仓库已有该风格时作为枚举后缀
- `Exception`：异常类型
- `Thrower`：集中抛出或构造领域异常
- `Utils` / `Util`：无状态工具类，通常使用静态方法
- `Helper`：辅助协作者；与 `Utils` / `Util` / `Support` 的边界见第 3 节
- `Support`：框架支撑、抽象基类、可继承公共能力，或特定包内的内部支撑类
- `Accessor`：对复杂结构做计算式或中介式访问
- `Generator`：生成代码、ID、Key 或产物
- `Formatter`：格式化字符串、日期、数字或展示值
- `Validator`：校验输入或状态
- `Filter`：过滤集合、文件、事件、请求或数据流
- `Interceptor`：拦截请求、调用、SQL、消息或执行链并在前后插入逻辑
- `Evaluator`：计算表达式、规则、条件或脚本的结果
- `Detector`：检测文件变化、手势、状态、特征或异常情况
- `Metric`：监控指标或度量数据
- `Estimator`：估算、采样或统计某类数值
- `Accumulator`：累加中间结果并提供读取入口
- `Tracker`：跟踪日志、监控值、位置、状态或生命周期变化
- `Cache`：缓存结构或缓存能力
- `Buffer`：缓冲区，通常用于读写过程中的临时数据承载
- `Pool`：可复用资源池，例如连接、线程、对象或内存
- `Allocator`：分配内存、缓冲区、对象槽位或其他可管理资源
- `Chunk`：一块内存、数据分片、文件分块或批量片段
- `Arena`：一组资源申请、释放和复用的管理区域；主要用于存储或内存管理语境
- `Pipeline` 或 `Chain`：按顺序组织过滤器、处理器、转换器或执行步骤
- `Composite`：组合多个同类对象，并以统一接口对外暴露
- `Wrapper`：包装已有对象以增加、裁剪或适配行为
- `Option`、`Param` 或 `Attribute`：配置项、参数对象或属性描述；粒度通常小于完整配置类
- `Tuple`：固定数量元素的轻量组合结构；仅在确实需要元组语义时使用
- `Aggregator`：聚合多个结果，例如求和、最大值、统计或跨分片合并
- `Iterator`：遍历集合、游标、流式数据或复杂结构
- `Batch`：批量请求、批量任务、批量载荷或批量处理单元
- `Limiter`：限流、限速、限并发或限制资源使用
- `Strategy`：可替换策略
- `Adapter`：适配一个接口或模型到另一个接口或模型
- `Command` 或 `Action`：可执行的用户动作或领域动作
- `Event`：事件对象
- `Delegate`：将职责委托给另一个对象或隔离平台、框架、兼容层差异
- `Template`：可复用的算法骨架
- `Packet`：网络或协议数据包
- `Protocol`：协议定义、协议适配或协议处理
- `Encoder`、`Decoder` 或 `Codec`：编码、解码或同时承担编码解码
- `Mode` 或 `Type`：模式、类型或枚举式分类；优先用于有限稳定集合
- `Invoker` 或 `Invocation`：封装方法调用、反射调用、远程调用或一次调用上下文
- `Initializer`：初始化组件、环境、上下文或框架扩展
- `Promise`：异步结果、延迟完成或回调衔接
- `Selector`：按条件选择目标、资源、服务实例、证书或策略
- `Reporter`：上报结果、报告、指标或诊断信息

# 3. `Utils` / `Util` / `Helper` / `Support` 边界

| suffix | use_when | avoid_when |
| --- | --- | --- |
| `Utils` / `Util` | 纯静态、无状态、无 Spring 依赖，提供可复用工具函数；无稳定项目风格时优先使用 `Utils`，`Util` 作为兼容备选 | 需要注入 Bean、持有运行时依赖、封装局部业务流程 |
| `Helper` | 带依赖、协调多个既有 API，或为一组局部业务处理器封装重复细节 | 实际是稳定领域服务、执行器、解析器、转换器时，不要用 `Helper` 掩盖更精确角色 |
| `Support` | 抽象基类、框架支撑、可被继承复用的公共能力，或明确的包内底层支撑 | 只是普通业务辅助协作者，且不被继承、不服务框架扩展点 |

判断顺序：

1. 如果类可以 `final + private constructor + static method`，并且没有外部依赖，优先按工具类后缀判断
2. 如果类需要注入 Spring Bean 或协调运行时依赖，优先考虑 `Helper`，或使用更精确的 `Resolver`、`Converter`、`Executor`、`Handler` 等后缀
3. 如果类承担抽象父类、框架扩展支撑或内部底层支撑职责，才考虑 `Support`
4. 如果只是因为「被多个类使用」而想命名为 `Support`，通常应重新判断职责，优先使用更具体的角色后缀
