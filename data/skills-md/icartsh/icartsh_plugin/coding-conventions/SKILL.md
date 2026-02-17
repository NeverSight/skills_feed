---
name: coding-conventions
description: .NET/C#의 코딩 규약, 명명 규칙, 레이아웃, C# 12/13/14의 최신 기능 활용 가이드라인을 정의합니다. C#/.NET 코드 작성 시, 클래스·메서드 명명 시, 코드 포맷팅 시, 또는 사용자가 코딩 규약, 명명 규칙, C# 모범 사례, Primary Constructors, Collection Expressions, field 키워드에 대해 언급했을 때 사용합니다.
---

# Coding Conventions

## 개요

이 SKILL은 개발되는 모든 .NET 프로젝트에 적용되는 코딩 규약을 정의합니다. .NET 8 이후의 최신 기능(C# 12/13/14, .NET 8/9/10)을 적극적으로 활용하여 가독성, 유지보수성, 성능이 높은 코드를 구현하는 것을 목적으로 합니다.

## 책임 범위

이 SKILL은 다음 범위를 다룹니다:

- .NET/C#의 최신 기능(C# 12/13/14, .NET 8/9/10) 활용 방침
- 명명 규칙 (Type, Member, Variable, Parameter)
- 코드 레이아웃 및 포맷
- 언어 기능 사용 방침 (Type inference, Collection, Exception handling)
- LINQ와 람다식의 모범 사례
- 모던 C# 구문의 권장 패턴

## 기본 방침

- .NET 8 이후의 최신 기능을 적극적으로 사용한다 (C# 12/13/14, .NET 8/9/10)
- 이전 버전과의 호환성이 필요한 경우를 제외하고 항상 최신 기능을 우선한다
- 오래된 언어 구문은 피한다
- **중요: 언더스코어 접두사(`_field`) 사용은 절대 금지한다**
- **중요: 중괄호 생략은 절대 금지한다 (1행으로 기술할 수 있는 경우에도 생략 불가)**
- Microsoft 공식 코딩 규약을 따른다
- 일관성을 유지하고 팀 전체에서 동일한 스타일을 적용한다

## .NET/C# 최신 기능 (버전별)

.NET 8 이후 각 버전에서 도입된 주요 기능을 적극적으로 활용합니다. 이전 버전과의 호환성이 필요한 경우를 제외하고 항상 최신 기능을 우선적으로 사용합니다.

### C# 12 (.NET 8) - 2023년 11월 공식 릴리스

#### Primary Constructors

- 클래스나 struct 선언에서 파라미터를 정의하고 클래스 전체에서 사용할 수 있음
- 명시적인 필드 선언을 줄이고 초기화를 간소화함

좋은 예:

```csharp
public class Person(string name, int age)
{
    public string Name => name;
    public int Age => age;

    public void Display()
    {
        Console.WriteLine($"{name} is {age} years old");
    }
}
```

나쁜 예:

```csharp
public class Person
{
    private string name;
    private int age;

    public Person(string name, int age)
    {
        this.name = name;
        this.age = age;
    }

    public string Name => name;
    public int Age => age;
}
```

#### Collection Expressions

- 대괄호와 스프레드 연산자를 사용하여 컬렉션을 간결하게 생성함
- 여러 컬렉션을 결합할 때 유용함

좋은 예:

```csharp
int[] array = [1, 2, 3, 4, 5];
List<string> list = ["one", "two", "three"];

int[] row0 = [1, 2, 3];
int[] row1 = [4, 5, 6];

// 스프레드 연산자로 결합
int[] combined = [..row0, ..row1];
```

#### Default Lambda Parameters

- 람다식에 기본 파라미터 값을 지정할 수 있음

좋은 예:

```csharp
var incrementBy = (int source, int increment = 1) => source + increment;

Console.WriteLine(incrementBy(5));
Console.WriteLine(incrementBy(5, 3));
```

#### Alias Any Type

- using 디렉티브로 복잡한 타입에 별칭을 붙일 수 있음

좋은 예:

```csharp
using Point = (int x, int y);
using ProductList = System.Collections.Generic.List<(string Name, decimal Price)>;

Point origin = (0, 0);
ProductList products = [("Product1", 100m), ("Product2", 200m)];
```

### C# 13 (.NET 9) - 2024년 11월 공식 릴리스

#### Params Collections

- `params` 수식어를 배열 외의 컬렉션 타입에서도 사용 가능해짐
- `List<T>`, `Span<T>`, `ReadOnlySpan<T>`, `IEnumerable<T>` 등에서 사용 가능

좋은 예:

```csharp
public void ProcessItems(params List<string> items)
{
    foreach (var item in items)
    {
        Console.WriteLine(item);
    }
}

// 메모리 효율이 중요한 경우
public void ProcessData(params ReadOnlySpan<int> data)
{
    foreach (var value in data)
    {
        Process(value);
    }
}
```

#### New Lock Type

- `System.Threading.Lock` 타입을 사용하여 더 빠른 스레드 동기화를 구현함
- 기존 `Monitor` 기반 락보다 빠름

좋은 예:

```csharp
private readonly Lock lockObject = new();

public void UpdateData()
{
    lock (lockObject)
    {
        // Critical section
    }
}
```

나쁜 예:

```csharp
// 기존 object 기반 락 (C# 13에서는 권장되지 않음)
private readonly object lockObject = new();

public void UpdateData()
{
    lock (lockObject)
    {
        // Critical section
    }
}
```

#### Partial Properties and Indexers

- partial 프로퍼티와 인덱서를 사용할 수 있게 됨
- 정의와 구현을 분리할 수 있음

좋은 예:

```csharp
// 정의 부분
public partial class DataModel
{
    public partial string Name { get; set; }
}

// 구현 부분
public partial class DataModel
{
    private string name;

    public partial string Name
    {
        get => name;
        set => name = value ?? throw new ArgumentNullException(nameof(value));
    }
}
```

#### Implicit Index Access

- 객체 이니셜라이저에서 `^` 연산자를 사용할 수 있게 됨

좋은 예:

```csharp
var countdown = new TimerBuffer
{
    buffer =
    {
        [^1] = 0,
        [^2] = 1,
        [^3] = 2
    }
};
```

#### Ref Struct Enhancements

- `ref struct` 타입이 인터페이스를 구현할 수 있게 됨
- 제네릭 타입에서 `ref struct`를 사용할 수 있게 됨 (`allows ref struct` 제약 조건)

좋은 예:

```csharp
public ref struct SpanWrapper<T> : IEnumerable<T>
{
    private Span<T> span;

    public IEnumerator<T> GetEnumerator()
    {
        foreach (var item in span)
        {
            yield return item;
        }
    }
}
```

### C# 14 (.NET 10) - 2025년 11월 릴리스 예정

#### Extension Members

- Extension Members를 활용하여 깔끔한 API 확장을 구현함
- 원래 타입을 오염시키지 않고 기능을 추가할 수 있음

좋은 예:

```csharp
extension<TSource>(IEnumerable<TSource> source)
{
    public bool IsEmpty => !source.Any();
    public int Count => source.Count();
}
```

#### Field-Backed Properties

- `field` 키워드를 사용하여 명시적인 backing field를 줄임
- 검증 로직을 간결하게 기술할 수 있음
- **언더스코어 접두사를 사용한 명시적인 backing field는 절대 금지**

좋은 예:

```csharp
// C# 14의 field 키워드 사용
public string Name
{
    get;
    set => field = value ?? throw new ArgumentNullException(nameof(value));
}

// 어쩔 수 없이 명시적인 backing field가 필요한 경우에도 언더스코어 없음
private string name;

public string Name
{
    get => name;
    set => name = value ?? throw new ArgumentNullException(nameof(value));
}
```

나쁜 예:

```csharp
// 언더스코어 접두사는 절대 금지
private string _name;

public string Name
{
    get => _name;
    set => _name = value ?? throw new ArgumentNullException(nameof(value));
}
```

#### Null-Conditional Assignment

- `?.`를 사용하여 null 체크를 간결하게 기술함
- 중복되는 null 체크를 줄임

좋은 예:

```csharp
customer?.Order = GetCurrentOrder();
```

나쁜 예:

```csharp
if (customer != null)
{
    customer.Order = GetCurrentOrder();
}
```

#### Implicit Span Conversions

- 성능 중시 코드에서는 `Span<T>`와 `ReadOnlySpan<T>`를 활용함
- 배열과 스팬 타입 간의 자동 변환을 이용함

## 명명 규칙 (Naming Conventions)

### Pascal Casing

- 타입 이름 (class, record, struct, interface, enum)
- 퍼블릭 멤버 (프로퍼티, 메서드, 이벤트)
- 네임스페이스

좋은 예:

```csharp
public class CustomerOrder
{
    public string OrderId { get; set; }
    public void ProcessOrder() { }
}
```

### Camel Casing

- 로컬 변수
- 메서드 파라미터
- 프라이빗 필드 (**언더스코어 접두사는 절대 사용하지 않음**)

좋은 예:

```csharp
public class OrderProcessor
{
    // 언더스코어 없음
    private string customerName;

    // 언더스코어 없음
    private int orderCount;

    public void ProcessOrder(string orderId)
    {
        var customerName = GetCustomerName(orderId);
        string processedResult = Process(customerName);
    }
}
```

나쁜 예:

```csharp
public class OrderProcessor
{
    // 언더스코어 접두사는 절대 금지
    private string _customerName;

    // 언더스코어 접두사는 절대 금지
    private int _orderCount;
}
```

### Interface 명명

- 접두사 `I`를 사용함

좋은 예:

```csharp
public interface IOrderProcessor
{
    void Process(Order order);
}
```

### 타입 파라미터 명명

- 접두사 `T`를 사용함
- 의미 있는 이름을 붙임

좋은 예:

```csharp
public class Repository<TEntity> where TEntity : class
{
    public void Add(TEntity entity) { }
}
```

## 코드 레이아웃 (Code Layout)

### 들여쓰기

- 공백(Space) 4개를 사용함
- 탭(Tab)은 사용하지 않음

### 중괄호 (Curly Braces)

- Allman 스타일 (시작 중괄호와 종료 중괄호를 별도의 행에 배치)
- **중괄호 생략은 절대 금지 (1행으로 기술할 수 있는 경우에도 반드시 중괄호 사용)**

좋은 예:

```csharp
public void ProcessOrder(Order order)
{
    if (order != null)
    {
        order.Process();
    }
}

// 1행이라도 중괄호를 사용함
if (isValid)
{
    Execute();
}

for (int i = 0; i < 10; i++)
{
    Process(i);
}
```

나쁜 예:

```csharp
// 중괄호 생략 금지
if (isValid)
    Execute();

// 중괄호 생략 금지
for (int i = 0; i < 10; i++)
    Process(i);

// 중괄호 생략 금지
if (order != null) order.Process();
```

### 행 기술

- 1행에 하나의 statement만 기술함
- 1행에 하나의 선언만 기술함
- 메서드 정의와 프로퍼티 정의 사이에 빈 행을 하나 넣음

좋은 예:

```csharp
public class Order
{
    public string OrderId { get; set; }

    public void Process()
    {
        var result = Validate();
        Execute(result);
    }

    private bool Validate()
    {
        return OrderId != null;
    }
}
```

### 네임스페이스

- 파일 스코프 네임스페이스(File-scoped namespace)를 사용함

좋은 예:

```csharp
namespace YourProject.Orders;

public class OrderProcessor
{
    // Implementation
}
```

나쁜 예:

```csharp
namespace YourProject.Orders
{
    public class OrderProcessor
    {
        // Implementation
    }
}
```

### using 디렉티브

- 네임스페이스 선언 바깥쪽에 배치함
- 알파벳 순으로 정렬함

좋은 예:

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

namespace YourProject.Orders;
```

## 타입과 변수

### 타입 지정

- 언어 키워드 (`string`, `int`, `bool`)를 사용함
- 런타임 타입 (`System.String`, `System.Int32`)은 사용하지 않음

좋은 예:

```csharp
string name = "John";
int count = 10;
bool isValid = true;
```

나쁜 예:

```csharp
String name = "John";
Int32 count = 10;
Boolean isValid = true;
```

### 타입 추론 (var)

- 타입이 할당되는 내용으로부터 명백한 경우에만 `var`를 사용함
- 기본 제공 타입(Built-in type)은 명시적으로 기술함

좋은 예:

```csharp
// 명백함
var orders = new List<Order>();

// 명백함
var customer = GetCustomer();

// 기본 타입은 명시
int count = 10;

// 기본 타입은 명시
string name = "John";
```

나쁜 예:

```csharp
// 기본 타입에서 var는 피함
var count = 10;

// 기본 타입에서 var는 피함
var name = "John";
```

## 문자열

### 문자열 보간 (String Interpolation)

- 짧은 문자열 결합에는 문자열 보간을 사용함

좋은 예:

```csharp
string message = $"Order {orderId} processed successfully";
```

나쁜 예:

```csharp
string message = "Order " + orderId + " processed successfully";
```

### StringBuilder

- 루프 내에서 대량의 텍스트를 추가하는 경우 `StringBuilder`를 사용함

좋은 예:

```csharp
var builder = new StringBuilder();
for (int i = 0; i < 1000; i++)
{
    builder.Append($"Line {i}\n");
}
```

### Raw String Literals

- 이스케이프 시퀀스보다 Raw String Literals를 우선함

좋은 예:

```csharp
string json = """
{
    "name": "John",
    "age": 30
}
""";
```

## 컬렉션과 객체 초기화

### 컬렉션 초기화

- C# 12 이후의 Collection Expressions를 사용함 (앞부분의 "C# 12 최신 기능" 참조)

### 객체 이니셜라이저 (Object Initializer)

- 객체 이니셜라이저를 사용하여 생성을 간소화함

좋은 예:

```csharp
var customer = new Customer
{
    Name = "John",
    Email = "john@example.com"
};
```

## 예외 처리 (Exception Handling)

### 구체적인 예외 캐치

- 일반적인 `System.Exception` 대신 구체적인 예외를 캐치함

좋은 예:

```csharp
try
{
    ProcessOrder(order);
}
catch (ArgumentNullException ex)
{
    Logger.Error("Order is null", ex);
}
```

나쁜 예:

```csharp
try
{
    ProcessOrder(order);
}
catch (Exception ex) // 너무 일반적임
{
    Logger.Error("Error", ex);
}
```

### using 문

- try-finally 대신 `using` 문을 사용함

좋은 예:

```csharp
using var connection = new SqlConnection(connectionString);
connection.Open();
// Process
```

나쁜 예:

```csharp
SqlConnection connection = null;
try
{
    connection = new SqlConnection(connectionString);
    connection.Open();
    // Process
}
finally
{
    connection?.Dispose();
}
```

## LINQ

### 의미 있는 변수명

- 쿼리 변수에는 의미 있는 이름을 사용함

좋은 예:

```csharp
var activeCustomers = from customer in customers
                      where customer.IsActive
                      select customer;
```

### 조기 필터링

- `where` 절을 사용하여 조기에 데이터를 필터링함

좋은 예:

```csharp
var result = customers
    .Where(c => c.IsActive)
    .Select(c => c.Name)
    .ToList();
```

### 암시적 타입 지정

- LINQ 선언에서는 암시적 타입 지정을 사용함

좋은 예:

```csharp
var query = from customer in customers
            where customer.IsActive
            select customer;
```

## 람다식 (Lambda Expressions)

### 이벤트 핸들러

- 삭제가 필요 없는 핸들러에는 람다식을 사용함

좋은 예:

```csharp
button.Click += (s, e) => ProcessClick();
```

### 파라미터 수식어

- C# 14 기능을 활용하여 타입 추론을 유지하면서 수식어를 사용함

좋은 예:

```csharp
TryParse<int> parse = (text, out result) => int.TryParse(text, out result);
```

## 주석 (Comments)

### 단일 행 주석

- 간결한 설명에는 `//`를 사용함
- 주석 구분자 뒤에 공백을 하나 넣음
- **주석은 반드시 단독 행에 기술함 (코드와 같은 행에 기술 금지)**
- 주석 앞에는 빈 행을 하나 넣음

좋은 예:

```csharp
// 고객 주문을 처리함
ProcessOrder(order);

var processor = new OrderProcessor();

// 주문을 실행함
var result = processor.ProcessOrder(order);
```

나쁜 예:

```csharp
ProcessOrder(order); // 고객 주문을 처리함 (코드와 같은 행은 금지)

var processor = new OrderProcessor();
// 이 행의 앞에 빈 행이 없음 (나쁜 예)
var result = processor.ProcessOrder(order);
```

### XML 문서

- 퍼블릭 멤버에는 XML 문서를 사용함

좋은 예:

```csharp
/// <summary>
/// 지정된 주문을 처리함
/// </summary>
/// <param name="order">처리할 주문</param>
/// <returns>처리 결과</returns>
public bool ProcessOrder(Order order)
{
    // Implementation
}
```

## 정적 멤버 (Static Members)

### 클래스 이름에 의한 호출

- 정적 멤버는 클래스 이름을 통해 호출함

좋은 예:

```csharp
var result = OrderProcessor.ProcessOrder(order);
```

나쁜 예:

```csharp
var processor = new OrderProcessor();

// 정적 메서드를 인스턴스를 통해 호출하는 것은 오해의 소지가 있음
var result = processor.ProcessOrder(order);
```

## 체크리스트 (Checklist)

### 코드 작성 전

- [ ] .NET/C#의 최신 기능 (C# 12/13/14)을 파악하고 있음
- [ ] 프로젝트의 타겟 프레임워크가 .NET 8 이후로 설정되어 있음
- [ ] 명명 규칙을 이해하고 있음

### 코드 작성 중

**필수 규칙:**

- [ ] **언더스코어 접두사를 절대 사용하지 않았음**
- [ ] **중괄호를 생략하지 않았음 (1행이라도 반드시 사용함)**
- [ ] **주석은 반드시 단독 행에 기술했음 (코드와 같은 행에 기술하지 않았음)**
- [ ] **주석 앞에 빈 행을 하나 넣었음**

**C# 12 이후 기능:**

- [ ] Primary Constructors를 사용하고 있음 (해당하는 경우)
- [ ] Collection Expressions를 사용하고 있음
- [ ] Default Lambda Parameters를 활용하고 있음 (해당하는 경우)
- [ ] Alias Any Type으로 복잡한 타입에 별칭을 붙였음 (해당하는 경우)

**C# 13 이후 기능:**

- [ ] Params Collections를 사용하고 있음 (해당하는 경우)
- [ ] New Lock Type을 사용하고 있음 (스레드 동기화가 필요한 경우)
- [ ] Partial Properties and Indexers를 활용하고 있음 (해당하는 경우)
- [ ] Implicit Index Access를 객체 이니셜라이저에서 사용하고 있음 (해당하는 경우)

**C# 14 이후 기능:**

- [ ] `field` 키워드를 사용하여 backing field를 간결하게 기술했음
- [ ] Extension Members를 활용하고 있음 (해당하는 경우)
- [ ] Null-Conditional Assignment를 활용하고 있음
- [ ] Lambda Parameters with Modifiers를 사용하고 있음 (해당하는 경우)

**기본 규칙:**

- [ ] 파일 스코프 네임스페이스를 사용하고 있음
- [ ] 언어 키워드 (`string`, `int`)를 사용하고 있음
- [ ] `var`를 적절히 사용하고 있음 (타입이 명백한 경우에만)
- [ ] 문자열 보간을 사용하고 있음
- [ ] Raw String Literals를 사용하고 있음 (해당하는 경우)
- [ ] Object Initializers를 사용하고 있음
- [ ] `using` 문을 사용하고 있음
- [ ] 구체적인 예외를 캐치하고 있음
- [ ] LINQ 식에서 조기 필터링을 실시하고 있음
- [ ] 의미 있는 변수명을 사용하고 있음
- [ ] 주석이 간결하고 명확함
- [ ] 퍼블릭 멤버에 XML 문서를 기술했음
- [ ] Allman 스타일로 중괄호를 배치했음
- [ ] 들여쓰기에 공백 4개를 사용하고 있음

### 코드 작성 후

- [ ] 코드가 일관된 스타일로 작성되었음
- [ ] .NET 8 이후의 최신 기능 (C# 12/13/14)을 활용하고 있음
- [ ] 명명 규칙을 따르고 있음
- [ ] 가독성이 높고 유지보수하기 쉬운 코드임
