# 1. Dto 命名边界

`Dto` 仅用于数据传输对象，例如接口请求、接口响应、跨层调用或消息载荷。

可以使用：

```text
OrderRequestDto
OrderResponseDto
PaymentCallbackDto
```

不要把 `Dto` 用于领域实体、数据库实体或承载业务行为的对象。

# 2. Dao 命名边界

`Dao` 仅用于直接封装数据库访问的持久层协作者，例如直接使用 MyBatis、JPA、`JdbcTemplate` 执行实体查询、保存、更新或删除。

可以使用：

```text
OrderDao
PaymentRecordDao
UserAccountDao
```

不要把 `Dao` 用于普通业务服务，或只是协调多个持久层调用的流程编排类。

# 3. 其他对象后缀

不要默认引入 `VO`、`DO`、`PO`、`BO`、`POJO` 等其他对象后缀命名体系，除非用户特别说明，或仓库里已经存在这类名称且需要兼容。

# 4. Dto 和 Dao 检查

最终确定 `Dto` 或 `Dao` 名称前，检查以下事项：

- 使用 `Dto` 时，它是否只是数据传输对象；
- 使用 `Dao` 时，它是否直接访问数据库；
- 是否因为仓库既有约定需要兼容其他对象后缀；
- 是否误把普通参数对象、领域对象或流程编排类命名为 `Dto` 或 `Dao`。
