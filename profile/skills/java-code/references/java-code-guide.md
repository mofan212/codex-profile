# 1. 目录

- 代码组织；
- 命名习惯；
- 方法实现；
- 注释风格；
- 常见代码形态；
- 单测风格；
- 代码评审清单。

# 2. 代码组织

## 2.1 类与职责

- 一个类只承担一个清晰职责，类名和后缀应直接表达用途；复杂命名、角色后缀、`Dto` / `Dao` 边界和变量常量命名优先使用 `$java-naming` 判断。
- Service、Domain、Controller、Mapper、Dto、Dao 等分层代码优先贴合当前项目已有调用链，不因为新增需求扩大接口行为面。
- 工具类通常使用 `final` 类加私有构造方法，方法以 `public static` 为主；如果当前项目已有其他约定，跟随项目约定。
- 需要封装构造过程的类可以使用私有构造方法加静态工厂方法，工厂方法命名优先贴合当前项目习惯，例如 `from`、`of`、`create`、`build`。
- Spring 组件保持轻量，使用当前项目已有注入方式和 Bean 组织方式，不主动混用不同注入风格。
- 修改 MyBatis 相关代码时，同步核对 Mapper 接口、XML、参数名、返回映射和调用方，避免只改一侧。

## 2.2 文件头与类注释

- 新建 Java 类时，按用户或仓库约定补充类级 JavaDoc。
- 如果已有类注释，不修改原来的作者、日期或格式。
- 类注释可以简洁；当类名和上下文已能说明职责时，不强行加冗长说明。

## 2.3 导入与格式

- 不使用通配符导入。
- 导入顺序遵循当前文件和 IDE 默认整理结果。
- 使用项目已有缩进、换行和格式化规则。
- 多参数方法调用换行时，保持可读性和局部一致。
- 避免无意义格式改动；只整理被修改文件必要范围。

# 3. 命名习惯

## 3.1 业务命名

- 名称直接体现业务概念，避免抽象、空泛或只描述技术实现的命名。
- 布尔方法优先使用 `is`、`has`、`can`、`should`、`check`、`require` 等表达判断语义的动词。
- 查找、转换、解析、构造类方法使用清晰动词，例如 `get`、`find`、`query`、`resolve`、`convert`、`build`、`create`、`dispatch`。
- 新增数据传输对象和直接数据库访问协作者的命名边界使用 `$java-naming` 判断；历史 `DTO`、`DAO`、`BO`、`VO`、`DO`、`Entity`、`Enum` 等后缀跟随当前项目，不主动更换领域模型命名体系。

## 3.2 常量与集合

- 常量名使用全大写下划线。
- 类内常量修饰符顺序跟随当前文件已有写法。
- 需要保序时显式使用 `LinkedHashMap`、`LinkedHashSet`；需要并发读写时使用并发集合。
- 枚举反查可以预构建 Map；规模很小且调用不频繁时，也可以保持简单遍历。

# 4. 方法实现

## 4.1 控制流

- 优先早返回处理空值、空集合、不满足条件的分支。
- 对递归、树结构、链式依赖等逻辑，先处理终止条件，再处理当前节点，再递归处理子节点。
- 循环适合有副作用、需要短路或需要维护上下文的场景；`stream` 适合简单映射、过滤和收集。
- 新增分支逻辑时，优先使用清晰的条件表达、枚举或策略映射；只有复杂度真实增长时才引入设计模式。
- 使用 Stream、Optional、lambda 等 Java8 特性时，确保可读性优于技巧展示。

## 4.2 空值与默认值

- 空值、集合、Map、字符串判断优先使用当前项目已有工具类和写法。
- 返回空结果时优先使用 `Collections.emptyList()`、`Collections.emptySet()`、`Collections.emptyMap()` 等不可变空集合。
- 可缺省单值可以返回 `Optional<T>`，但必须与现有接口契约兼容。
- 不为了消除 `null` 而改变调用方可观察行为。

## 4.3 异常和日志

- 异常处理优先复用项目已有异常类型、错误码、Thrower 或 BusinessException 工具，不随意引入新的异常体系。
- 可恢复的工具方法可以记录日志后返回空结果；业务失败应按项目统一异常机制抛出。
- 日志模板使用占位符，不拼接字符串。
- 不为每个分支都加防御性日志，只记录能帮助定位失败的异常或关键状态。
- 对兼容性要求明确的行为，保留原接口语义；不得为了局部代码简洁改变调用方可观察行为。

# 5. 注释风格

## 5.1 JavaDoc

- 非显而易见的 public 方法添加 JavaDoc，包含必要的 `@param`、`@return`、`@apiNote`。
- 私有方法只有在递归、反射、映射算法等不直观时才补充 JavaDoc。
- 字段、常量和复杂配置可以用短注释说明业务含义。

## 5.2 行内注释

- 注释解释为什么这样处理，而不是重复代码做了什么。
- 对复杂算法，优先在关键分支前写一句说明业务意图的注释。
- 不添加装饰性注释，不把每一行都翻译成中文。

# 6. 常见代码形态

## 6.1 工具类

```java
public final class XxxUtils {
    private XxxUtils() {
    }

    public static Optional<String> getStringValue(JsonNode jsonNode, String key) {
        if (jsonNode == null || StringUtils.isEmpty(key)) {
            return Optional.empty();
        }
        return Optional.ofNullable(jsonNode.get(key))
                .filter(JsonNode::isTextual)
                .map(JsonNode::asText);
    }
}
```

## 6.2 Support 类

```java
@RequiredArgsConstructor(access = AccessLevel.PRIVATE)
public class XxxSupport {

    private final Collection<?> sourceData;

    public static XxxSupport from(Collection<?> sourceData) {
        return new XxxSupport(sourceData);
    }

    public List<Map<String, Object>> mapping() {
        if (CollectionUtils.isEmpty(sourceData)) {
            return Collections.emptyList();
        }
        List<Map<String, Object>> result = new ArrayList<>();
        for (Object sourceDatum : sourceData) {
            // 逐条处理来源数据，保证处理顺序稳定
            result.add(singleMapping(sourceDatum));
        }
        return result;
    }

    private Map<String, Object> singleMapping(Object sourceDatum) {
        return new HashMap<>();
    }
}
```

# 7. 单测风格

## 7.1 测试框架

- 优先沿用当前模块已有测试框架。模块使用 JUnit4 就按 JUnit4 写；模块使用 JUnit5 就按 JUnit5 写。
- 断言优先使用 AssertJ；如果项目已有统一断言工具，跟随项目。
- Mock 使用 Mockito 或当前项目已有 Mock 工具，保持测试可读、稳定、聚焦。

## 7.2 测试命名

- 测试方法名应表达被测方法、业务场景和预期结果。
- 每个测试聚焦一个分支或一个异常场景。
- 测试内可以用短中文注释标记业务场景，但不要写成长篇说明。
- 测试重点覆盖新增行为、边界分支、异常路径和已有行为兼容性。

# 8. 代码评审清单

## 8.1 提交前检查

- 是否先读过同包或同类型样本，并保持局部一致。
- 是否避免过度设计，只解决当前需求。
- 是否使用早返回降低嵌套。
- 是否复用项目已有工具类、异常体系、领域模型和接口契约。
- 是否保留已有作者注释；新建类是否符合用户或仓库约定。
- 是否检查了相关配置、Mapper XML、调用方和测试覆盖。
- 是否补充了与行为变化相匹配的聚焦单测。
- 如果无法运行测试或编译，是否说明原因和已完成的静态核对范围。
