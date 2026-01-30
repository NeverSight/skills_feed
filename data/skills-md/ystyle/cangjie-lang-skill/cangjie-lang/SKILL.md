---
name: cangjie-lang
description: Cangjie programming language code generation and analysis expert. Use this when users need to write or analyze Cangjie code.
---

# 仓颉语言代码生成与分析工作手册

---

## 目录

- [第1章：语言基础定义](#第1章语言基础定义)
- [第2章：核心语法规则](#第2章核心语法规则)
  - [2.1 变量声明](#21-变量声明)
  - [2.2 基础类型](#22-基础类型)
  - [2.3 表达式与控制流](#23-表达式与控制流)
  - [2.4 函数](#24-函数)
  - [2.5 枚举类型](#25-枚举类型)
  - [2.6 模式匹配](#26-模式匹配)
  - [2.7 Option类型](#27-option类型)
  - [2.8 class类型](#28-class类型)
  - [2.9 单元测试](#29-单元测试)
  - [2.10 错误处理](#210-错误处理)
  - [2.11 速查手册](#211-速查手册)
- [第3章：任务处理流程](#第3章任务处理流程)
  - [3.1 代码生成流程](#31-代码生成流程)
  - [3.2 代码分析流程](#32-代码分析流程)
- [第4章：19个⚠️易错点检查清单](#第4章19个易错点检查清单)
- [第5章：示例与模板参考](#第5章示例与模板参考)
- [第6章：质量控制标准](#第6章质量控制标准)
- [第7章：MCP文档集成](#第7章mcp文档集成)

---

## 第1章：语言基础定义

### 1.1 文件与后缀

- **文件后缀**：`.cj`
- **语言简称**：`cj`（Cangjie）
- **入口函数**：`main()`

### 1.2 注释

```cj
// 单行注释

/*
 * 多行注释
 */

/**
 * 文档注释
 */
```

### 1.3 代码块结构

```cj
main() {
    // 代码主体
    let a: Int64 = 20
    var b: Int64 = 12
    println("${a}${b}")
}
```

---

## 第2章：核心语法规则

### 2.1 变量声明

#### 语法格式

```cj
修饰符 变量名: 变量类型 = 初始值
```

#### 可变性修饰符

- `let` - **不可变变量**（只能赋值一次，初始化后不可修改）
- `var` - **可变变量**（可以被多次赋值）

⚠️ **易错点1**：`let` 不支持变量遮蔽（shadowing），不能在同一作用域内重新定义同名变量。

#### 可见性修饰符

| 修饰符 | 范围 | 默认值 |
|--------|------|--------|
| `private` | class定义内可见 | ❌ |
| `public` | 模块内外均可见 | ❌ |
| `protected` | 当前模块及当前类的子类可见 | ❌ |
| `internal` | 仅当前包及子包内可见 | ✅ **默认** |

#### 静态性修饰符

- `static` - 影响成员变量的存储和引用方式

#### 示例代码

```cj
main() {
    let a: Int64 = 20      // 不可变变量
    var b: Int64 = 12      // 可变变量
    b = 23                // 可以修改var变量
    println("${a}${b}")
}
```

**示例参考**：`examples/01_variable_declaration.cj`

---

### 2.2 基础类型

#### 数值类型

**有符号整数**：`Int8`、`Int16`、`Int32`、`Int64`、`IntNative`

**无符号整数**：`UInt8`、`UInt16`、`UInt32`、`UInt64`、`UIntNative`

**浮点类型**：`Float16`、`Float32`、`Float64`

**布尔类型**：`true`、`false`

#### 字符类型（Rune）

- 使用 `Rune` 表示，可以表示 Unicode 字符集中的所有字符
- **Rune → UInt32**：`UInt32(e)` - 获取 Unicode scalar value
- **整数 → Rune**：`Rune(num)` - 值必须在有效 Unicode 范围内
  - 有效范围：`[0x0000, 0xD7FF]` 或 `[0xE000, 0x10FFFF]`

⚠️ **易错点2**：Rune 转整数时需确保在有效 Unicode 范围内，否则会编译错误或运行时抛异常。

#### 转义字符

```cj
let slash: Rune = r'\\'
let newLine: Rune = r'\n'
let tab: Rune = r'\t'
```

#### Unicode 字面量

```cj
let he: Rune = r'\u{4f60}'   // 你
let llo: Rune = r'\u{597d}'   // 好
```

#### 字符串类型（String）

仓颉支持**三种字符串字面量**：

**1. 单行字符串字面量**

内容定义在一对单引号或双引号内，只能写在同一行：

```cj
let s1: String = ""
let s2 = 'Hello Cangjie Lang'
let s3 = "\"Hello Cangjie Lang\""
let s4 = 'Hello Cangjie Lang\n'  // \n 是转义字符，表示换行
```

**2. 多行字符串字面量**

开头结尾需各存在三个双引号（`"""`）或三个单引号（`'''`），内容从开头的三个引号**换行后**的第一行开始：

```cj
// 三个双引号
let s1: String = """
    """  // 空字符串（换行后才开始）

// 三个单引号
let s2: String = '''
    Hello,
    Cangjie Lang'''
```

**3. 多行原始字符串字面量**

以一个或多个井号（`#`）和一个单引号或双引号开头，**转义规则不适用**，**不支持插值**：

```cj
let s1: String = #""#                    // 空字符串
let s2 = ##'#'\n'##                     // \n 不是换行符，是 \ 和 n 两个字符
let s3 = ###"
    Hello,
    Cangjie
    Lang"###                            // 保留换行和缩进
```

⚠️ **易错点4**：在多行原始字符串字面量中，转义字符（如 `\n`、`\t`）**不会被转义**，字面量中的内容会维持原样。

⚠️ **易错点5**：多行原始字符串字面量**不支持插值**，不要使用 `${}` 语法。

#### 插值字符串

⚠️ **易错点3**：插值字符串中使用 `${}` 表达式

```cj
let fruit = "apples"
let count = 10
let s = "There are ${count * count} ${fruit}"
```

**适用范围**：插值字符串仅适用于**单行字符串字面量**和**多行字符串字面量**，**不适用于多行原始字符串字面量**。

#### 元组（Tuple）

- **类型表示**：`(T1, T2, ..., TN)`
- **至少二元**：`(Int64, Float64)`、`(Int64, Float64, String)`
- **索引访问**：`tuple[0]`、`tuple[1]`

```cj
var tuple = (true, false)
println(tuple[0])
```

#### 数组类型

```cj
Array<T>  // T 是元素类型，可以是任意类型
```

#### 区间类型（Range）

- **类型表示**：`Range<T>`（泛型）
- **包含三个值**：`start`、`end`、`step`
- **约束**：
  - `start` 和 `end` 类型相同（T）
  - `step` 类型是 `Int64`
  - `step` 值不能等于 0

#### Unit 类型

- **唯一值**：`()`
- **支持操作**：仅赋值、判等、判不等
- ⚠️ **不支持**：其他所有操作

**示例参考**：`examples/02_basic_types.cj`

---

### 2.3 表达式与控制流

#### 条件表达式

⚠️ **易错点5**：条件表达式的括号不能省略，这是与很多语言的差异。

```cj
if (条件) {        // ✅ 必须有括号
    分支 1
} else {
    分支 2
}
```

#### if 表达式

**基本形式**：
```cj
if (条件) {
    分支 1
} else {
    分支 2
}
```

**if 作为表达式**（返回值）：

```cj
let a = 10
let result = if (a > 5) {
    "greater than 5"
} else {
    "5 or less"
}
// result = "greater than 5"
```

**模式匹配（let pattern）**：

```cj
let a = Some(3)
let d = Some(1)
if (let Some(e) <- a && let Some(f) <- d) {  // 两个模式都匹配
    println("${e} ${f}")  // 输出: 3 1
}
```

#### while 表达式

```cj
while (条件) {
    循环体
}

// do-while 形式
do {
    循环体
} while (条件)
```

#### for-in 表达式

```cj
for (迭代变量 in 序列) {
    循环体
}
```

**元组遍历**：
```cj
let array = [(1, 2), (3, 4), (5, 6)]
for ((x, y) in array) {
    println("${x}, ${y}")
}
```

**区间遍历**：
```cj
main() {
    var sum = 0
    for (i in 1..=100) {    // 1 到 100（包含）
        sum += i
    }
    println(sum)
}
```

#### 跳转控制

- 支持 `break`、`continue`
- ⚠️ **易错点6**：不支持标签跳转
- ⚠️ **易错点7**：完全不支持 `goto`

**示例参考**：`examples/03_control_flow.cj`

---

### 2.4 函数

#### 函数是一等公民

- 可以作为函数的参数或返回值
- 可以赋值给变量
- 函数本身也有类型

#### 函数类型

**语法**：`(参数类型) -> 返回类型`

- 参数类型用 `()` 括起，多个参数用 `,` 分隔
- 参数类型和返回类型用 `->` 连接

```cj
func add(a: Int64, b: Int64): Int64 {
    return a + b
}

type FnType = (Int64) -> Unit

func display(a: Int64): Unit {
    println(a)
}

// 命名参数
func name(name!:String)

// 命名参数还可以设置默认值
func name(name!:String = "小王")
```

#### 函数参数

⚠️ **易错点8**：函数参数默认是 `let` 定义的不可变变量

```cj
// a 和 b 默认是 let 不可变的（不能显式写 let 或 var）
func add(a: Int64, b: Int64): Int64 {
    return a + b
}
```

⚠️ **重要**：
- **函数参数不能显式使用 `let` 或 `var` 修饰符**（包括顶层函数、class成员方法、struct成员方法等所有函数）
- 参数默认就是 `let` 不可变的

如果需要修改参数值，应该使用局部变量：

```cj
func modify(a: Int64): Int64 {
    var result = a
    result = result + 1  // 修改局部变量
    return result
}
```

#### 返回值简写

```cj
func add(a: Int64, b: Int64): Int64 {
    a + b  // 最后一个表达式自动作为返回值
}

func returnAdd(): (Int64, Int64) -> Int64 {
    add  // 可以直接返回函数
}
```

#### Lambda 表达式

**语法**：
```cj
{ p1: T1, ..., pn: Tn => expressions | declarations }
```

**示例**：
```cj
// 完整类型声明
let f1 = { a: Int64, b: Int64 => a + b }

// 无参 Lambda
var display = { =>
    println("Hello")
    println("World")
}

// 类型推断
var sum1: (Int64, Int64) -> Int64 = { a, b => a + b }
var sum2: (Int64, Int64) -> Int64 = { a: Int64, b => a + b }

// Lambda 作为参数
func f(a1: (Int64) -> Int64): Int64 {
    a1(1)
}

main(): Int64 {
    f({ a2 => a2 + 10 })  // 参数类型推断
}
```

**Lambda 立即调用**：

⚠️ **易错点9**：Lambda 表达式可以立即调用

```cj
let r2 = { => 123 }()  // r2 = 123，立即执行
var g = { x: Int64 => println("x = ${x}") }
g(2)  // 调用 Lambda
```

**示例参考**：`examples/04_functions.cj`

---

### 2.5 枚举类型

#### 定义语法

- 以 `enum` 开头
- 构造器之间使用 `|` 分隔
- **至少存在一个有名字的构造器**
- 第一个构造器之前的 `|` 是可选的

```cj
enum RGBColor {
    | Red(UInt8) | Green(UInt8) | Blue(UInt8)
}
```

#### 构造器类型

- **无参构造器**：`C`
- **有参构造器**：`C(p1, p2, ..., pn)`

**示例参考**：`examples/05_enum.cj`

---

### 2.6 模式匹配

#### match 表达式

**基本语法**：

⚠️ **重要**：case 后的语句**不需要 `{}` 括号**，多行语句直接换行即可

```cj
match (待匹配值) {
    case 模式1 => 处理1
    case 模式2 => 处理2
    case _ => 默认处理  // 通配符
}
```

**多行语句**：直接换行，不需要 `{}`

```cj
match (value) {
    case 1 => println("one")
    case 2 => println("two")
               println("second number")  // ✅ 多行直接换行
    case _ => println("other")
}
```

**示例**：
```cj
main() {
    let x = 0
    match (x) {
        case 1 => print("x = 1")
        case 0 => print("x = 0")        // 匹配
        case 2 | 3 | 4 => print("other")  // 多值匹配
        case _ => print("其他")
    }
}
```

#### 模式类型详解

##### 1. 常量模式

支持：整数字面量、浮点数字面量、字符字面量、布尔字面量、字符串字面量、Unit 字面量

⚠️ **易错点10**：不支持字符串插值

##### 2. 通配符模式

使用 `_` 表示，匹配任意值，通常作为最后一个 case

##### 3. 绑定模式

使用标识符，匹配并绑定值

```cj
main() {
    let x = -10
    let y = match (x) {
        case 0 => "zero"
        case n => "x is not zero and x = ${n}"  // n 绑定匹配的值
    }
    println(y)
}
```

##### 4. Tuple 模式

用于匹配元组值

```cj
main() {
    let tv = ("Alice", 24)
    let s = match (tv) {
        case ("Bob", age) => "Bob is ${age} years old"
        case ("Alice", age) => "Alice is ${age} years old"  // age 是绑定模式
        case (name, 100) => "${name} is 100 years old"
        case (_, _) => "someone"
    }
    println(s)
}
```

##### 5. 类型模式

判断运行时类型是否是某个类型的子类型

```cj
main() {
    var d = Derived()
    var r = match (d) {
        case b: Base => b  // b 是类型模式，匹配 Base 类型
        case _ => 0
    }
    println("r = ${r}")
}
```

##### 6. enum 模式

用于匹配 enum 类型的实例

```cj
enum TimeUnit {
    | Year(UInt64)
    | Month(UInt64)
}

main() {
    let x = Year(2)
    let s = match (x) {
        case Year(n) => "x has ${n * 12} months"      // 匹配
        case TimeUnit.Month(n) => "x has ${n} months"  // TimeUnit.Month 是完整路径
    }
    println(s)
}
```

#### 模式嵌套

⚠️ **重要**：Tuple 模式和 enum 模式可以嵌套任意模式

```cj
enum TimeUnit {
    | Year(UInt64)
    | Month(UInt64)
}

enum Command {
    | SetTimeUnit(TimeUnit)
    | GetTimeUnit
    | Quit
}

main() {
    let command = (SetTimeUnit(Year(2022)), SetTimeUnit(Year(2024)))
    match (command) {
        case (SetTimeUnit(Year(year)), _) => println("Set year ${year}")
        case (_, SetTimeUnit(Month(month))) => println("Set month ${month}")
        case _ => ()
    }
}
```

#### Pattern Guard（守卫）

在 case 的模式之后，可以使用 `where` 子句添加额外的条件判断（称为 pattern guard）。

**语法**：`case 模式 where 条件 => 处理`

⚠️ **重要**：使用 `where` 关键字，**不是** `if`

**示例**：

```cj
enum RGBColor {
    | Red(Int16)
    | Green(Int16)
    | Blue(Int16)
}

main() {
    let c = RGBColor.Green(-100)
    let cs = match (c) {
        case Red(r) where r < 0 => "Red = 0"
        case Red(r) => "Red = ${r}"
        case Green(g) where g < 0 => "Green = 0"     // 匹配（因为 -100 < 0）
        case Green(g) => "Green = ${g}"
        case Blue(b) where b < 0 => "Blue = 0"
        case Blue(b) => "Blue = ${b}"
    }
    println(cs)  // 输出：Green = 0
}
```

**注意事项**：
- `where` 后的条件表达式必须是 `Bool` 类型
- pattern guard 在模式匹配成功后再进行条件判断
- 多个 case 可以按顺序排列，从上到下匹配
- ⚠️ **易错点**：不要使用 `if`，应该使用 `where`

**错误示例**：
```cj
match (value) {
    case n if n > 0 => println("positive")  // ❌ 编译错误：不是 if
    case _ => println("other")
}
```

**正确写法**：
```cj
match (value) {
    case n where n > 0 => println("positive")  // ✅ 使用 where
    case _ => println("other")
}
```

**示例参考**：`examples/06_pattern_matching.cj`

---

### 2.7 Option类型

#### 定义

```cj
enum Option<T> {
    | Some(T)   // 有值
    | None      // 无值
}
```

#### 使用场景

当需要表示某个类型可能有值，也可能没有值的时候使用。

#### 常用方法

##### 1. 空合并运算符 `??`

```cj
let optA: Option<Int64> = Option<Int64>.Some(42)
let a: Int64 = optA ?? 0  // 如果 optA 是 None，则使用默认值 0
```

##### 2. 检查是否有值

```cj
let optA: Option<Int64> = Option<Int64>.Some(42)

if (optA.isSome()) {
    println("有值")
}

if (optA.isNone()) {
    println("无值")
}
```

##### 3. 模式匹配提取值

```cj
let optA: Option<Int64> = Option<Int64>.Some(42)

if (let Option<Int64>.Some(a) <- optA) {
    println("值是: ${a}")
} else {
    println("无值")
}
```

##### 4. 短路返回

```cj
func getValue(): Option<Int64> {
    // ... 一些逻辑
    return Option<Int64>.None
}

func process(): Int64 {
    let optA = getValue()
    let a = optA ?? return 0  // 如果是 None，直接返回 0
    // 继续处理 a
    a + 1
}
```

##### 5. 短路抛出异常

```cj
func getValue(): Option<Int64> {
    return Option<Int64>.None
}

func processOrThrow(): Int64 {
    let optA = getValue()
    let a = optA ?? throw Exception("值不存在")
    // 继续处理 a
    a
}
```

##### 6. match 表达式处理

```cj
let optA: Option<Int64> = Option<Int64>.Some(42)

let result = match (optA) {
    case Option<Int64>.Some(value) => "值是: ${value}"
    case Option<Int64>.None => "无值"
}
```

**示例参考**：`examples/07_option_type.cj`

---

### 2.8 class类型

#### 定义语法

```cj
class ClassName {
    // 成员变量
    // 成员属性
    // 静态初始化器
    // 构造函数
    // 成员函数
    // 操作符函数
}
```

#### 示例

```cj
class Rectangle {
    let width: Int64
    let height: Int64

    public init(width: Int64, height: Int64) {
        this.width = width
        this.height = height
    }

    public func area() {
        width * height
    }
}

let rec = Rectangle(10, 20)
let l = rec.height  // l = 20
```

#### 访问修饰符

对于 class 的成员（变量、属性、构造函数、函数）：

| 修饰符 | 含义 | **默认** |
|--------|------|---------|
| `private` | class 定义内可见 | ❌ |
| `internal` | 当前包及子包（含子包的子包）内可见 | ✅ **默认** |
| `protected` | 当前模块及当前类的子类可见 | ❌ |
| `public` | 模块内外均可见 | ❌ |

⚠️ **易错点11**：成员的默认访问修饰符是 `internal`，不是 `private` 或 `public`。

**示例参考**：`examples/08_class.cj`

---

### 2.9 单元测试

#### 测试宏

- `@Test` - 应用于顶级函数或类，转换为单元测试类
- `@TestCase` - 标记测试类内的函数为测试用例
- `@Fail` - 标记测试失败

#### 断言宏

##### Assert 断言（失败停止用例）

```cj
@Assert(leftExpr, rightExpr)      // 判断相等
@Assert(condition: Bool)          // 判断条件
```

##### Expect 断言（失败继续执行）

```cj
@Expect(leftExpr, rightExpr)      // 判断相等
@Expect(condition: Bool)          // 判断条件
```

#### 完整示例

```cj
@Test
class LexerTest {
    @TestCase
    func test() {
        let a = 1

        // 方式一：手动判断
        if (a != 1) {
            @Fail("a is not 1")
        }

        // 方式二：Assert 条件
        @Assert(a != 1)

        // 方式三：Assert 相等
        @Assert(a, 1)
    }
}
```

**示例参考**：`examples/09_unit_test.cj`

---

### 2.10 错误处理

#### 基础异常处理

```cj
// 抛出异常
throw Exception("错误信息")

// 捕获异常
try {
    // 可能抛出异常的代码
} catch (e: ExceptionType) {
    // 处理异常
}
```

**示例参考**：`examples/10_error_handling.cj`

---

### 2.11 速查手册

#### 代码块结构

```cj
main() {
    // 条件判断（必须有括号）
    if (条件) {
        // ...
    } else {
        // ...
    }

    // 循环
    while (条件) { }
    do { } while (条件)
    for (变量 in 序列) { }

    // 模式匹配
    match (值) {
        case 模式 => 处理
        case _ => 默认
    }
}
```

#### 类型后缀速查

| 类型 | 后缀 |
|------|------|
| 整数 | `Int8`, `Int16`, `Int32`, `Int64`, `IntNative` |
| 无符号整数 | `UInt8`, `UInt16`, `UInt32`, `UInt64`, `UIntNative` |
| 浮点 | `Float16`, `Float32`, `Float64` |
| 字符 | `Rune` |
| 字符串 | `String` |
| 元组 | `(T1, T2, ...)` |
| 数组 | `Array<T>` |
| 区间 | `Range<T>` |
| 函数 | `(T1, T2) -> Rt` |

**示例参考**：`examples/11_quick_reference.cj`

---

### 2.12 集合

仓颉提供了多种集合类型，适用于不同的使用场景：

#### 集合类型

**1. Array** - 固定大小数组
- **使用场景**：不需要增加和删除元素，但需要修改元素
- **字面量**：`let arr: Array<String> = ["A", "B", "C"]`
- **特点**：大小固定，内存连续，访问速度快

```cj
main() {
    // 创建 Array
    let arr: Array<String> = ["A", "B", "C"]

    // 访问元素（使用下标）
    println(arr[0])  // 输出: A

    // 修改元素
    arr[0] = "X"
    println(arr[0])  // 输出: X

    // 获取大小
    println(arr.size)  // 输出: 3
}
```

**2. ArrayList** - 动态数组
- **使用场景**：需要频繁对元素增删查改
- **特点**：大小可变，支持动态添加和删除元素

```cj
import std.collection.ArrayList

main() {
    // 创建 ArrayList
    let list = ArrayList<Int64>()

    // 添加元素（使用 add 方法）
    list.add(1, at: 0)  // 在位置 0 添加 1
    list.add(2, at: 1)  // 在位置 1 添加 2

    // 或使用 add 添加整个数组
    let arr = [3, 4, 5]
    list.add(all: arr)  // list: [1, 2, 3, 4, 5]

    // 访问元素（使用 get 方法，返回 Option）
    let value = list.get(0)
    match (value) {
        case Option<Int64>.Some(v) => println("First: ${v}")
        case Option<Int64>.None => println("Not found")
    }

    // 或使用下标访问
    println(list[0])  // 输出: 1

    // 修改元素
    list[0] = 10

    // 删除元素
    list.remove(at: 0)  // 移除第一个元素

    // 获取大小
    println(list.size)
}
```

**3. HashSet** - 哈希集合
- **使用场景**：希望每个元素都是唯一的
- **特点**：元素唯一，快速查找

```cj
import std.collection.HashSet

main() {
    // 创建 HashSet
    let set = HashSet<Int64>()

    // 添加元素
    set.add(1)
    set.add(2)
    set.add(3)
    set.add(1)  // 重复元素不会被添加

    // 检查是否包含
    if (set.contains(2)) {
        println("包含 2")
    }

    // 获取大小
    println(set.size)  // 输出: 3

    // 删除元素
    set.remove(2)
}
```

**4. HashMap** - 哈希映射
- **使用场景**：希望存储一系列的映射关系（键值对）
- **字面量**：`let map: HashMap<String, Int> = HashMap(("A", 1), ("B", 2))` 或 `HashMap([("A", 1), ("B", 2)])`
- **特点**：键值对存储，快速查找

```cj
import std.collection.HashMap

main() {
    // 创建 HashMap（使用字面量）
    let map: HashMap<String, Int64> = HashMap(
        ("A", 1),
        ("B", 2),
        ("C", 3)
    )

    // 或者使用方括号
    let map2: HashMap<String, Int64> = HashMap([
        ("A", 1),
        ("B", 2),
        ("C", 3)
    ])

    // 或者空 HashMap
    let emptyMap = HashMap<String, Int64>()

    // 添加元素（使用 add 方法）
    emptyMap.add("D", 4)

    // 访问元素（使用 get 方法，返回 Option）
    let value = map.get("A")
    match (value) {
        case Option<Int64>.Some(v) => println("A = ${v}")
        case Option<Int64>.None => println("Not found")
    }

    // 或使用下标访问
    println(map["A"])  // 输出: 1

    // 修改元素
    map["A"] = 10

    // 检查是否包含键
    if (map.contains("B")) {
        println("包含键 B")
    }

    // 删除元素
    map.remove("C")

    // 获取大小
    println(map.size)
}
```

#### 集合常用方法

**添加元素**：
- Array：不能添加（大小固定）
- ArrayList：`add(element, at: index)` 或 `add(all: array)`
- HashSet：`add(element)`
- HashMap：`add(key, value)` 或 `map[key] = value`

**访问元素**：
- Array：`array[index]` 或 `array.get(index)`
- ArrayList：`list[index]` 或 `list.get(index)`（返回 Option）
- HashMap：`map[key]` 或 `map.get(key)`（返回 Option）

**修改元素**：
- 所有集合都支持 `[]` 下标方式修改

**删除元素**：
- Array：不能删除
- ArrayList：`remove(at: index)`
- HashSet：`remove(element)`
- HashMap：`remove(key)`

**其他常用方法**：
- `size` - 获取元素个数（属性）
- `clear()` - 清空所有元素（ArrayList, HashSet, HashMap）
- `contains(element)` - 检查是否包含（HashSet, HashMap）
- `get(index)` - 获取元素（ArrayList, HashMap，返回 Option）

**示例参考**：`examples/12_collections.cj`

---

### 2.13 包

仓颉使用包（package）来组织代码，提供模块化和命名空间管理。

#### 包声明

**基本语法**：
```cj
package package.name
```

**目录结构与包声明对应**：

```
src
└── directory_0
    ├── directory_1
    │   ├── a.cj          // package demo.directory_0.directory_1
    │   └── b.cj          // package demo.directory_0.directory_1
    └── c.cj              // package demo.directory_0
└── main.cj              // package demo
```

**示例**：
```cj
// a.cj
package demo.directory_0.directory_1

public func funcA() {
    println("Function A")
}

// b.cj
package demo.directory_0.directory_1

public func funcB() {
    println("Function B")
}

// c.cj
package demo.directory_0

public func funcC() {
    println("Function C")
}

// main.cj
package demo

import demo.directory_0.directory_1.{funcA, funcB}
import demo.directory_0.funcC

main() {
    funcA()  // 调用 demo.directory_0.directory_1.funcA
    funcB()  // 调用 demo.directory_0.directory_1.funcB
    funcC()  // 调用 demo.directory_0.funcC
}
```

#### 导入（import）

**基本语法**：
```cj
package currentPackage

import std.math.*              // 导入 std.math 的所有内容
import package1.foo            // 导入 package1.foo
import {package1.foo, package2.bar, package1.MyClass}  // 导入多个
```

**使用示例**：
```cj
package demo

import std.math.*
import package1.helper
import {package1.MyClass, package2.Utils}

main() {
    // 直接使用导入的方法和类型
    let result = pow(2, 3)    // std.math.pow
    helper()                  // package1.helper
    let obj = MyClass()       // package1.MyClass
    Utils.doSomething()       // package2.Utils
}
```

#### 导入方式

**1. 导入所有（通配符）**：
```cj
import std.math.*
// 可以直接使用 std.math 中的所有内容
let value = sqrt(16)
```

**2. 导入特定项**：
```cj
import std.math.pi
// 只能使用 pi
println(pi)
```

**3. 导入多个项**：
```cj
import {std.math.sin, std.math.cos}
// 可以使用 sin 和 cos
```

**4. 重命名导入**：
```cj
import std.math as math
let value = math.sqrt(16)
```

#### 访问修饰符与包

- **private**：仅当前文件可见
- **internal**：当前包及子包可见（**默认**）
- **public**：模块内外均可见

**示例**：
```cj
package demo.math

// 默认为 internal，仅 demo.math 及其子包可见
func internalFunc() {
    println("internal")
}

// public，任何地方都可访问
public func publicFunc() {
    println("public")
}

// private，仅当前文件可见
private func privateFunc() {
    println("private")
}
```

**示例参考**：`examples/13_package_import.cj`

---

## 第3章：任务处理流程

### 3.1 代码生成流程

#### 场景1：基础代码生成

**需求识别**：
- 识别变量类型（let/var）
- 确定数据类型（Int64, String, Rune等）
- 判断是否需要类型标注

**生成步骤**：
1. 加载对应模板（从 `templates/` 目录）
2. 应用语法规则（对照第2章）
3. ⚠️ **检查19个易错点**
4. 生成最终代码

**示例模板**：
```cj
// templates/basic/variable_declaration.cj.template
{{MODIFIER}} {{VARIABLE_NAME}}: {{TYPE}} = {{INIT_VALUE}}
```

#### 场景2：函数定义生成

**需求识别**：
- 函数名和参数列表
- 参数类型和返回类型
- 是否需要命名参数
- 是否需要默认值

**生成步骤**：
1. 加载函数定义模板
2. 确定参数是否需要 `var` 修饰（默认let）
3. 检查返回值类型
4. 应用⚠️易错点8（函数参数默认不可变）

#### 场景3：控制流生成

**需求识别**：
- 条件判断/循环/模式匹配
- 是否需要括号（⚠️必须加括号）
- 是否需要模式匹配

**生成步骤**：
1. 选择合适的控制结构
2. ⚠️确保条件表达式有括号（易错点5）
3. 检查是否需要 `break`/`continue`（不支持标签，易错点6/7）
4. 生成代码

#### 场景4：class定义生成

**需求识别**：
- 类名和成员变量
- 构造函数
- 成员函数
- 访问修饰符

**生成步骤**：
1. 加载class模板
2. ⚠️应用默认访问修饰符 `internal`（易错点11）
3. 生成构造函数
4. 生成成员函数

#### 场景5：模式匹配生成

**需求识别**：
- match表达式或if模式匹配
- 模式类型（常量/通配符/绑定/Tuple/enum/类型）
- 是否需要模式嵌套

**生成步骤**：
1. 选择匹配模式
2. ⚠️检查case顺序（按顺序匹配）
3. ⚠️确保通配符在最后（易错点9）
4. 生成匹配代码

#### 场景6：单元测试生成

**需求识别**：
- 测试类和测试用例
- 断言类型（Assert/Expect）
- 测试数据

**生成步骤**：
1. 加载测试模板
2. 添加 `@Test` 和 `@TestCase` 宏
3. 选择断言类型
4. 生成测试代码

---

### 3.2 代码分析流程

#### 场景1：语法正确性分析

**分析步骤**：
1. 解析代码结构
2. 对照第2章11个语法模块检查
3. ⚠️对照19个易错点清单（第4章）
4. 提供修正建议

**检查项**：
- 变量声明是否正确（let/var）
- 类型标注是否正确或可推断
- 条件表达式是否有括号⚠️
- 字符串插值是否使用 `${}`⚠️
- 函数参数是否被修改（或明确使用var）⚠️
- 访问修饰符是否符合需求（默认internal）⚠️

#### 场景2：潜在错误检测

**分析步骤**：
1. 识别可能触发19个⚠️易错点的代码模式
2. 分析运行时行为
3. 提供具体修正建议

**重点检测**：
- let变量遮蔽⚠️
- Rune转换范围⚠️
- 原始字符串转义⚠️
- break/continue标签跳转⚠️
- Unit类型非法操作⚠️
- match case顺序⚠️

#### 场景3：代码优化建议

**分析步骤**：
1. 检查代码风格和最佳实践
2. 提供优化建议
3. 推荐使用合适的模板和示例

**优化项**：
- 是否可以使用Lambda简化代码
- 是否可以使用模式匹配替代复杂的if-else
- 是否应该使用Option类型处理可能的空值
- 是否应该使用enum提高类型安全性

---

## 第4章：19个⚠️易错点检查清单

### 变量相关

1. ⚠️ **`let` 不支持变量遮蔽**
   - 错误：在同一作用域重新定义同名let变量
   - 修正：使用不同的变量名或使用var
   - 参考：第2.1节

2. ⚠️ **函数参数默认是 `let` 不可变的**
   - 错误：在函数内修改参数值
   - 修正：使用 `var` 显式声明可变参数
   - 参考：第2.4节

3. ⚠️ **成员变量默认访问修饰符是 `internal`**
   - 错误：误认为默认是 `private`
   - 修正：根据需求显式声明访问修饰符
   - 参考：第2.8节

### 控制流相关

4. ⚠️ **所有条件表达式必须有括号**
   - 错误：`if x > 0 { }`
   - 修正：`if (x > 0) { }`
   - 参考：第2.3节

5. ⚠️ **不支持 `goto`**
   - 错误：使用goto语句
   - 修正：重构代码结构，使用函数或循环控制
   - 参考：第2.3节

6. ⚠️ **`break`/`continue` 不支持标签跳转**
   - 错误：`break outerLoop;`
   - 修正：重构嵌套循环逻辑
   - 参考：第2.3节

### 类型转换相关

7. ⚠️ **Rune 转整数需确保在有效 Unicode 范围**
   - 错误：`Rune(0xD800)` （代理区字符）
   - 修正：确保值在 `[0x0000, 0xD7FF]` 或 `[0xE000, 0x10FFFF]`
   - 参考：第2.2节

8. ⚠️ **原始字符串字面量中转义字符不会被转义**
   - 错误：认为 `##"\n"##` 会产生换行符
   - 修正：使用普通字符串 `"\\n"` 或理解原始字符串特性
   - 参考：第2.2节

### 模式匹配相关

9. ⚠️ **match 表达式的 case 按顺序匹配**
   - 错误：将具体case放在通配符之后
   - 修正：将具体case放在前面，通配符 `_` 放在最后
   - 参考：第2.6节

10. ⚠️ **常量模式不支持字符串插值**
    - 错误：在match的case中使用 `"Hello ${name}"`
    - 修正：使用绑定模式或运行时计算
    - 参考：第2.6节

### 字符串相关

11. ⚠️ **插值字符串使用 `${}` 而非 `{}`**
    - 错误：`"Hello {name}"`
    - 修正：`"Hello ${name}"`
    - 参考：第2.2节

### 函数相关

12. ⚠️ **Lambda 表达式可以立即调用**
    - 说明：`{ => 123 }()` 是合法语法，立即执行Lambda
    - 参考：第2.4节

### 类型系统相关

13. ⚠️ **Unit 类型只支持赋值、判等、判不等操作**
    - 错误：对 `()` 进行其他操作（如算术运算）
    - 修正：理解Unit类型的限制
    - 参考：第2.2节

### 其他

14. ⚠️ **元组至少需要两个元素**
    - 错误：定义单元素元组
    - 修正：使用具体类型或添加第二个元素
    - 参考：第2.2节

15. ⚠️ **区间类型的 step 不能等于 0**
    - 错误：`Range(1, 10, 0)`
    - 修正：确保step非零
    - 参考：第2.2节

16. ⚠️ **enum 至少存在一个有名字的构造器**
    - 错误：定义空enum
    - 修正：至少添加一个构造器
    - 参考：第2.5节

17. ⚠️ **match 表达式的 case 不需要 `{}` 括号**
    - 错误：`case 1 => { println("1") }`
    - 修正：`case 1 => println("1")`
    - 参考：第2.6节

18. ⚠️ **Option 类型用于表示可能有值或无值**
    - 说明：不是所有情况都需要Option，仅当需要明确表示可能无值时使用
    - 参考：第2.7节

19. ⚠️ **Duration 和 sleep 在 `std.core` 里不需导入**
    - 说明：这些是内置类型和函数，可直接使用
    - 参考：第2.10节

---

## 第5章：示例与模板参考

### 5.1 代码示例（examples/）

共39个示例，按难度和语法模块分类：

**基础示例（01-15）**：
- 01_variable_declaration.cj - 变量声明
- 02_basic_types.cj - 基础类型
- 03_control_flow.cj - 控制流
- 04_functions.cj - 函数
- 05_enum.cj - 枚举
- 06_pattern_matching.cj - 模式匹配
- 07_option_type.cj - Option类型
- 08_class.cj - class类型
- 09_unit_test.cj - 单元测试
- 10_error_handling.cj - 错误处理
- 11_quick_reference.cj - 速查手册
- 12-15：更多基础示例

**中级示例（16-27）**：
- Lambda表达式和高阶函数
- 复杂模式匹配
- class继承和多态
- 集合操作
- 异常处理
- 测试用例编写

**高级示例（28-39）**：
- 综合应用案例
- 性能优化技巧
- 最佳实践展示

### 5.2 代码模板（templates/）

按场景组织：

**basic/**：
- hello_world.cj.template
- package_structure.cj.template
- main_function.cj.template

**functions/**：
- function_definition.cj.template
- lambda.cj.template
- higher_order_function.cj.template

**control_flow/**：
- conditional_logic.cj.template
- loops.cj.template
- error_handling.cj.template

**data_structures/**：
- class_definition.cj.template
- enum_definition.cj.template
- collection_operations.cj.template

**testing/**：
- unit_test.cj.template
- test_case.cj.template

---

## 第6章：质量控制标准

### 6.1 代码生成质量检查

生成代码时必须确保：

- [ ] ⚠️条件表达式都有括号
- [ ] ⚠️字符串插值使用 `${}`
- [ ] ⚠️函数参数未被修改（或明确使用 var）
- [ ] ⚠️访问修饰符符合需求（默认internal）
- [ ] 类型标注正确或可推断
- [ ] 模式匹配覆盖所有情况
- [ ] ⚠️未触犯19个易错点

### 6.2 代码分析质量检查

分析代码时必须提供：

- [ ] 对照11个语法模块检查
- [ ] ⚠️对照19个易错点检查
- [ ] 类型系统一致性验证
- [ ] 提供具体修正建议
- [ ] 标注易错点编号（如 ⚠️易错点5）

### 6.3 响应质量标准

- **准确性**：语法规则必须正确
- **完整性**：覆盖所有相关语法点
- **实用性**：提供可执行的代码示例
- **可读性**：添加清晰的注释和说明
- **⚠️易错点标注**：明确标注19个易错点

---

## 第7章：MCP文档集成

### 7.1 MCP工具使用策略

**优先级**：
1. **本SKILL.md**（核心语法手册）
2. **reference/**（详细参考手册）
3. **MCP文档**（官方完整文档）

**触发条件**：
- 查询标准库API（std、stdx）
- 查询高级特性（泛型、并发、宏等）
- 查询官方文档中的最新特性
- 需要更详细的说明和示例

### 7.2 MCP工具列表

当前可用的MCP工具：

1. **search_documents** - 搜索仓颉文档
   - 用途：根据关键词搜索相关文档
   - 示例：查询"lambda closure 高阶函数"

2. **get_document_content** - 获取文档内容
   - 用途：获取指定文档的完整内容
   - 支持按章节获取（section参数）

3. **list_documents** - 列出文档
   - 用途：浏览文档结构
   - 支持路径导航（类似ls命令）

4. **get_document_overview** - 获取文档总览
   - 用途：查看分类结构和导航树
   - 支持树形视图（view_type="tree"）

### 7.3 使用示例

```python
# 查询lambda相关文档
search_documents(query="lambda closure")

# 获取某个文档的特定章节
get_document_content(
    doc_id="manual_source_zh_cn_functions",
    section="lambda"
)

# 浏览标准库结构
list_documents(category="libs", subcategory="std")
```

### 7.4 文档分类

- **manual** - 基础手册
- **libs** - 标准库（std、stdx）
- **ohos** - OpenHarmony文档
- **tools** - 开发工具
- **extra** - 额外内容

---

## 附录A：快速参考

### A.1 关键字

`let`、`var`、`if`、`else`、`while`、`do`、`for`、`match`、`case`、`func`、`class`、`enum`、`init`、`return`、`package`、`import`、`public`、`private`、`protected`、`internal`、`static`

### A.2 操作符

- 算术：加 +、减 -、乘 *、除 /、取模 %
- 比较：相等 ==、不等 !=、小于 <、大于 >、小于等于 <=、大于等于 >=
- 逻辑：与 &&、或 ||、非 !
- 范围：.. 半开区间、..= 闭区间
- 模式匹配：模式绑定 <-、case 分隔 =>

### A.3 常用标准库

- `std.core` - 核心类型和函数
- `std.io` - 输入输出
- `std.collection` - 集合类型
- `std.time` - 时间和日期

---

## 附录B：版本历史

- **v1.0.0** (2025-01-07) - 初始版本
  - 包含11个核心语法模块
  - 39个代码示例
  - 19个⚠️易错点
  - 完整的代码生成和分析流程

---

## 附录C：贡献指南

欢迎贡献新的示例、模板和改进建议！

**贡献方式**：
1. Fork仓库
2. 创建feature分支
3. 提交改动
4. 发起Pull Request

**质量要求**：
- 代码必须符合仓颉语法规范
- 示例必须有清晰注释
- 模板必须有使用说明
- 文档必须标注相关语法模块和易错点

---

## 附录D：许可证

MIT License

---

**结束**

**文档维护**：仓颉语言社区
**最后更新**：2025-01-07
**版本**：v1.0.0
