# 1. 包命名规则

包路径用于表达归属、模块、业务域和职责：

```text
com.company.project.module.domain.responsibility
```

各层含义：

- `company/project`：组织和项目归属
- `module`：可部署模块或主要技术模块
- `domain`：业务域或能力边界
- `responsibility`：该包内类的主要职责

包名全部小写，语义层级之间使用点号分隔，不使用下划线或中划线。多个英文单词优先自然连接，例如 `springframework`、`deepspace`；不要写成 `spring_framework` 或 `deep-space`。优先使用单数形式，例如 `executor`、`context`、`resolver`、`helper`、`util`、`constant`、`exception`。

包名前缀根据项目归属确定：公司项目优先使用反向域名和公司、项目、模块层级；团队或个人项目优先沿用仓库既有前缀。无法从仓库确认组织、团队或个人标识时，不要臆造个人姓名、账号、邮箱或机器路径。

# 2. 职责包选择

根据真实职责选择最窄的包名：

- `appservice`：面向应用层的服务入口
- `controller`：Web 或 API 入口
- `dto`：数据传输对象，例如接口请求、接口响应、跨层调用或消息载荷
- `dao`：直接使用 MyBatis、JPA、`JdbcTemplate` 等框架访问数据库的持久层协作者
- `executor`：执行任务、命令、作业或运行时单元
- `handler`：处理特定事件、动作、请求或回调
- `filter`：过滤输入、请求、事件或数据集
- `interceptor`：拦截请求、调用或执行链
- `context`：贯穿调用链传递执行状态
- `resolver`：解析值、表达式、变量、类型或引用
- `converter`：转换数据结构或类型体系
- `parser`：解析文本、表达式、协议或元数据
- `codec`：编码、解码或序列化协议数据
- `proxy`：代理或适配外部系统、远程能力
- `listener`：监听事件或消息
- `metric`：监控指标、统计数据或观测结果
- `config`：配置对象、配置装配或配置项
- `component`：可复用运行时组件或描述结构
- `constant`：常量
- `enums`：枚举
- `exception`：异常
- `helper`：辅助协作者职责包；不要在包名规则中展开类后缀边界
- `util`：无状态工具方法
- `support`：某个更具体父包下的内部支撑类

选择职责包时按类的角色归类，而不是只按「谁在调用」归类。比如 `handler` / `executor` 包主要放具体处理器或执行器；可复用辅助协作者优先放到项目已有 `helper`、`service` 或 `component` 包。只有确实是某个包内私有实现细节时，才把辅助类留在调用方所在包。

当某个职责包变大时，继续按业务对象、业务场景或稳定子域拆分：

```text
handler.order
handler.payment
handler.inventory
handler.notification
handler.notification.support
```

# 3. 包路径检查

最终确定包路径前，检查以下事项：

- 包路径是否表达了模块、业务域和职责
- 是否复用了仓库已有前缀和模块层级
- 是否为了一个类新增了过深包层级
- 新增层级是否表达稳定边界，而不是临时需求名
