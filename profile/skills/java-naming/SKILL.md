---
name: java-naming
description: Design and review Java backend naming for packages, classes, role suffixes, methods, fields, variables, and constants. Use for package hierarchy, class/interface/implementation names, Dto and Dao boundaries, method verbs, boolean/collection/data operation names, constants, local consistency checks, and avoiding VO/DO/PO/BO/POJO suffix taxonomies unless explicitly requested or required by existing convention.
---

# 1. Java 命名入口规则

使用本 Skill 为 Java 后端代码选择包路径、类名、方法名、字段名、变量名、常量名和角色后缀。

命名前先阅读当前代码上下文，优先遵循所在仓库、模块、同级包和相邻类的既有风格。不要在职责没有确定前先套后缀。

可以在语义明确时引入 `Dto` 和 `Dao` 后缀；涉及这两个后缀时读取 [dto-dao-naming.md](references/dto-dao-naming.md)。不要默认引入 `VO`、`DO`、`PO`、`BO`、`POJO` 等其他对象后缀命名体系，除非用户特别说明，或仓库里已经存在这类名称且需要兼容。

# 2. 按需加载规则

只读取当前任务需要的引用文件，避免一次加载全部命名规则：

| when | read | purpose |
| --- | --- | --- |
| 需要设计或评审包路径 | [package-naming.md](references/package-naming.md) | 判断包层级、职责包和拆分边界 |
| 需要设计或评审普通类、接口、抽象类、异常、测试类、配置类、工具类 | [class-naming.md](references/class-naming.md) | 判断类名组合、抽象类、实现类、测试类和类名禁区 |
| 需要选择或解释类角色后缀 | [role-suffixes.md](references/role-suffixes.md) | 判断角色后缀是否表达真实职责 |
| 需要判断是否使用 `Dto` 或 `Dao` | [dto-dao-naming.md](references/dto-dao-naming.md) | 判断数据传输对象和持久层协作者边界 |
| 需要设计或评审方法名、布尔方法、集合操作、异步方法、生命周期方法、成对动词 | [method-naming.md](references/method-naming.md) | 判断方法动词、返回语义和操作方向 |
| 需要设计或评审字段、参数、局部变量、布尔字段、常量 | [variable-constant-naming.md](references/variable-constant-naming.md) | 判断变量语义、布尔命名和常量命名 |

如果用户的问题同时涉及多个命名对象，只读取对应的多个引用文件。例如只问类名时，不要读取方法、变量和常量命名规则。

# 3. 工作流程

- 先明确要命名的是包、类、接口、方法、字段、变量还是常量。
- 识别当前模块、业务域和职责边界；查看同级包名、相邻类名、相邻方法名或字段名。
- 沿用仓库内已经稳定的领域词拼写，例如 `OrderId` 和 `OrderID` 之间不要随意切换。
- 检查是否已有同职责包、类、接口、抽象基类、测试类、方法或常量。
- 不要为了统一风格而主动重命名既有代码，不要凭通用偏好改名。
- 如果只是评审命名，说明当前命名是否可接受、更推荐的命名、推荐理由，以及需要保留现名时的兼容理由。

# 4. 决策原则

## 4.1 优先级

命名优先级从高到低为：

1. 仓库或模块已有强约定。
2. 同级包、相邻类和相邻成员的稳定风格。
3. 本 Skill 的通用规则和对应引用文件。

当本 Skill 与仓库既有风格冲突时，优先保留本地一致性，并在回答中说明这是兼容决策。

## 4.2 通用禁区

避免以下命名：

- 使用拼音，或把拼音和英文混用。
- 用难以理解的缩写替代清晰单词。
- 使用特殊字符，常量中的下划线除外。
- 使用 Java 关键字、JDK 类名或主流框架核心类名作为自定义类型名。
- 为了追求短名称牺牲业务含义。
- 用 `for`、`to`、`from`、`with`、`of` 等介词时写成 `4`、`2` 这类谐音缩写。

# 5. 输出格式

如果需要给出结果，优先使用简短列表，只包含本次任务相关字段，例如 `package`、`class`、`method`、`field`、`constant`、`reason` 和 `compatibility`。
