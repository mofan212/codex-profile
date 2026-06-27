# 1. 方法命名规则

方法名使用小驼峰，优先使用动词或动词短语，并让参数名共同补全语义。推荐结构：

```text
动词 + 业务对象或结果
```

示例：

```text
createOrder
findOrderById
validatePaymentRequest
convertJsonToMap
sendAsync
getOrDefault
```

方法名应直接表达行为。不要为了显得抽象而使用 `process`、`handle`、`doWork` 之类无法说明对象和结果的名称，除非所在接口或框架约定已经固定。

# 2. 布尔方法

返回布尔值的方法优先使用能表达判断语义的前缀：

- `is`：判断对象状态，例如 `isValid`
- `can`：判断能否执行动作，例如 `canRemove`
- `has`：判断是否持有数据、属性或关系，例如 `hasObservers`
- `should`：判断是否应该执行动作，例如 `shouldRetry`
- `needs`：判断是否需要执行动作，例如 `needsRefresh`

# 3. 检查和条件执行方法

检查类方法根据失败行为选择动词：

- `validate`：校验输入、请求或状态，不合法时返回错误或抛出异常
- `ensure`：确保满足前置条件，不满足时抛出异常、扩容或修复状态
- `check`：通用检查；语义不如 `validate` 和 `ensure` 精确，优先少用

按需执行或带默认值的方法使用稳定搭配：

- `tryXxx`：尝试执行，失败时返回失败结果或抛出可预期异常
- `forceXxx`：强制执行，忽略普通保护条件或触发更强副作用
- `xxxIfNeeded`：只在需要时执行
- `getOrDefault`：失败或缺失时返回默认值
- `getOrElse`：失败或缺失时返回调用方给定的替代值

# 4. 异步、回调和生命周期方法

异步方法要在名称中暴露执行方式或结果边界：

- `xxxAsync`：异步执行
- `xxxSync`：与已有异步方法对应的同步执行
- `blockingXxx`：会阻塞当前线程
- `schedule`、`post`、`execute`、`start`、`cancel`、`stop`：用于任务、作业或异步执行单元

回调和生命周期方法使用事件时序前缀：

- `onXxx`：事件发生时
- `beforeXxx`、`preXxx` 或 `willXxx`：事件发生前
- `afterXxx`、`postXxx` 或 `didXxx`：事件发生后
- `initialize`、`pause`、`stop`、`destroy`、`dispose`：对象生命周期动作

# 5. 集合和数据方法

集合操作使用能体现数据结构语义的动词：

- `contains`：是否包含
- `add` 或 `append`：添加元素
- `insert`：插入到指定位置
- `put`：按 Key 写入映射
- `remove`：移除元素
- `enqueue` 和 `dequeue`：队列入队和出队
- `push`、`pop` 和 `peek`：栈压入、弹出和查看
- `find`：按条件查找

数据操作动词要区分来源、边界和副作用：

- `create` 或 `newXxx`：创建新对象
- `fromXxx`：从已有对象、配置或数据构造
- `toXxx`：转换成另一种表示
- `load`：从本地、内存、文件或已知存储读取
- `fetch`：从远程服务、网络或外部系统读取
- `save`、`store`、`commit` 或 `apply`：保存、持久化、提交或应用变更
- `delete` 或 `remove`：删除或移除
- `clear` 或 `reset`：清空或恢复初始状态

# 6. 成对动词

同一语义域中尽量使用稳定的成对动词，不要混用相近但不成对的词：

```text
get/set
add/remove
create/destroy
start/stop
open/close
read/write
load/save
begin/end
backup/restore
import/export
split/merge
attach/detach
bind/unbind
encode/decode
encrypt/decrypt
compress/decompress
connect/disconnect
send/receive
download/upload
lock/unlock
expand/collapse
enter/exit
push/pull
```

# 7. 方法名检查

最终确定方法名前，检查以下事项：

- 方法名是否以准确动词开头
- 方法名和参数是否共同组成清晰语义
- 布尔方法是否使用 `is`、`can`、`has`、`should`、`needs` 等判断前缀
- 数据操作动词是否准确表达来源、边界和副作用
- 同一语义域中的成对动词是否稳定一致
