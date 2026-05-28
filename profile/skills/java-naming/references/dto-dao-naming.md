# 1. Dto 命名边界

| suffix | use_when | examples | forbidden |
| --- | --- | --- | --- |
| `Dto` | 接口请求、接口响应、跨层调用或消息载荷等数据传输对象 | `OrderRequestDto`、`OrderResponseDto`、`PaymentCallbackDto` | 领域实体、数据库实体或承载业务行为的对象 |

# 2. Dao 命名边界

| suffix | use_when | examples | forbidden |
| --- | --- | --- | --- |
| `Dao` | 直接封装数据库访问的持久层协作者，例如直接使用 MyBatis、JPA、`JdbcTemplate` 执行实体查询、保存、更新或删除 | `OrderDao`、`PaymentRecordDao`、`UserAccountDao` | 普通业务服务，或只是协调多个持久层调用的流程编排类 |

# 3. 其他对象后缀

不要默认引入 `VO`、`DO`、`PO`、`BO`、`POJO` 等其他对象后缀命名体系，除非用户特别说明，或仓库里已经存在这类名称且需要兼容。

# 4. Dto 和 Dao 检查

| check_item | pass_condition |
| --- | --- |
| `Dto` 边界 | 目标对象只是数据传输对象 |
| `Dao` 边界 | 目标对象直接访问数据库 |
| 兼容后缀 | 只有仓库既有约定要求时才兼容其他对象后缀 |
| 误用排除 | 普通参数对象、领域对象或流程编排类没有被命名为 `Dto` 或 `Dao` |
