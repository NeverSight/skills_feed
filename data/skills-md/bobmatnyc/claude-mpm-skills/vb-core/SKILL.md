---
name: vb-core
description: Core VB.NET patterns, type safety, modern language features
version: 1.0.0
category: toolchain
author: Claude MPM Team
license: MIT
tags: [visualbasic, vb.net, dotnet, type-safety]
---

# Visual Basic .NET Core Patterns

Modern VB.NET (2019+) best practices with focus on type safety, LINQ, async/await, and .NET integration.

## Quick Start

```vb
' Always enable strict type checking
Option Strict On
Option Explicit On
Option Infer On

' Modern class definition
Public Class Customer
    Public Property Id As Integer
    Public Property Name As String
    Public Property Email As String

    ' Constructor
    Public Sub New(id As Integer, name As String, email As String)
        Me.Id = id
        Me.Name = name
        Me.Email = email
    End Sub
End Class

' Modern async method
Public Async Function GetCustomerAsync(id As Integer) As Task(Of Customer)
    Dim result = Await database.QueryAsync(Of Customer)(
        "SELECT * FROM Customers WHERE Id = @id",
        New With {.id = id}
    )
    Return result.FirstOrDefault()
End Function

' LINQ query
Dim activeCustomers = From c In customers
                      Where c.IsActive AndAlso c.Balance > 0
                      Order By c.Name
                      Select c
```

## Type Safety (Critical)

### Option Strict On

```vb
' ALWAYS at top of every file
Option Strict On
Option Explicit On
Option Infer On

' Why:
' - Option Strict: Prevents implicit narrowing conversions
' - Option Explicit: Requires variable declaration
' - Option Infer: Enables type inference (but still type-safe)
```

### Explicit Types vs Inference

```vb
' ✅ Good: Explicit when clarity helps
Dim customerName As String = GetCustomerName(id)
Dim count As Integer = GetCount()

' ✅ Good: Inference when type is obvious
Dim customer = New Customer(1, "John", "john@example.com")
Dim items = New List(Of String) From {"a", "b", "c"}

' ❌ Bad: Dim without type and no inference
Dim data = GetData()  ' What type is data?

' ✅ Better: Be explicit
Dim data As DataTable = GetData()
```

### Nullable Types

```vb
' Modern nullable syntax (VB 15.5+)
Dim middleName As String? = Nothing
Dim age As Integer? = Nothing

' Null-conditional operator
Dim length As Integer? = middleName?.Length

' Null-coalescing operator
Dim displayName As String = middleName If Nothing

' Check for null
If age IsNot Nothing Then
    Console.WriteLine($"Age: {age.Value}")
End If

' GetValueOrDefault
Dim years As Integer = age.GetValueOrDefault(0)
```

## Modern Language Features

### String Interpolation

```vb
' ✅ Modern (VB 14+)
Dim message = $"Customer {customer.Name} has balance {customer.Balance:C}"

' ❌ Old style (avoid)
Dim message = String.Format("Customer {0} has balance {1:C}", customer.Name, customer.Balance)

' ❌ Concatenation (avoid for complex strings)
Dim message = "Customer " & customer.Name & " has balance " & customer.Balance.ToString("C")
```

### Lambda Expressions

```vb
' Single-line lambda
Dim isAdult = Function(age As Integer) age >= 18

' Multi-line lambda
Dim calculateTax = Function(amount As Decimal) As Decimal
                       Dim rate = If(amount > 10000, 0.2D, 0.15D)
                       Return amount * rate
                   End Function

' Lambda in LINQ
Dim adults = customers.Where(Function(c) c.Age >= 18).ToList()

' Action lambda (Sub)
items.ForEach(Sub(item) Console.WriteLine(item))
```

### Collection Initializers

```vb
' List initialization
Dim numbers = New List(Of Integer) From {1, 2, 3, 4, 5}

' Dictionary initialization
Dim config = New Dictionary(Of String, String) From {
    {"ConnectionString", "Server=..."},
    {"Timeout", "30"},
    {"MaxRetries", "3"}
}

' Array initialization
Dim names As String() = {"Alice", "Bob", "Charlie"}
```

### Tuple Support

```vb
' Named tuples (VB 15.3+)
Function GetCustomerInfo(id As Integer) As (Name As String, Email As String)
    Return ("John Doe", "john@example.com")
End Function

' Usage
Dim info = GetCustomerInfo(1)
Console.WriteLine($"{info.Name}: {info.Email}")

' Deconstruction
Dim (customerName, customerEmail) = GetCustomerInfo(1)
```

## LINQ Patterns

### Query Syntax vs Method Syntax

```vb
' Query syntax (more readable for complex queries)
Dim query = From c In customers
            Where c.IsActive
            Order By c.Name
            Select New With {
                .Name = c.Name,
                .Email = c.Email
            }

' Method syntax (more flexible)
Dim query = customers _
    .Where(Function(c) c.IsActive) _
    .OrderBy(Function(c) c.Name) _
    .Select(Function(c) New With {
        .Name = c.Name,
        .Email = c.Email
    })
```

### Common LINQ Operations

```vb
' Filtering
Dim activeCustomers = customers.Where(Function(c) c.IsActive).ToList()

' Projection
Dim names = customers.Select(Function(c) c.Name).ToList()

' Ordering
Dim sorted = customers.OrderBy(Function(c) c.Name).ThenBy(Function(c) c.Id)

' Grouping
Dim grouped = From c In customers
              Group c By c.City Into Group
              Select City, Customers = Group

' Aggregation
Dim total = orders.Sum(Function(o) o.Amount)
Dim average = orders.Average(Function(o) o.Amount)
Dim count = customers.Count(Function(c) c.IsActive)

' First/Single
Dim first = customers.FirstOrDefault(Function(c) c.Id = 1)
Dim single = customers.SingleOrDefault(Function(c) c.Email = email)

' Any/All
Dim hasActive = customers.Any(Function(c) c.IsActive)
Dim allActive = customers.All(Function(c) c.IsActive)
```

## Async/Await Patterns

### Async Method Declaration

```vb
' Return Task(Of T) for async methods with return value
Public Async Function GetDataAsync() As Task(Of String)
    Dim result = Await httpClient.GetStringAsync(url)
    Return result
End Function

' Return Task for async methods without return value
Public Async Function SaveDataAsync(data As String) As Task
    Await File.WriteAllTextAsync(filePath, data)
End Function

' Async Sub only for event handlers
Private Async Sub Button_Click(sender As Object, e As EventArgs) Handles Button.Click
    Await ProcessDataAsync()
End Sub
```

### Async Best Practices

```vb
' ✅ Good: Await all the way
Public Async Function ProcessOrderAsync(orderId As Integer) As Task(Of Boolean)
    Dim order = Await GetOrderAsync(orderId)
    Await ValidateOrderAsync(order)
    Await SaveOrderAsync(order)
    Return True
End Function

' ❌ Bad: Blocking on async (deadlock risk)
Public Function ProcessOrder(orderId As Integer) As Boolean
    Dim order = GetOrderAsync(orderId).Result  ' Can deadlock!
    Return True
End Function

' ✅ Good: ConfigureAwait(False) in libraries
Public Async Function GetDataAsync() As Task(Of String)
    Dim result = Await httpClient.GetStringAsync(url).ConfigureAwait(False)
    Return result
End Function

' Parallel async operations
Dim tasks = New List(Of Task(Of Customer)) From {
    GetCustomerAsync(1),
    GetCustomerAsync(2),
    GetCustomerAsync(3)
}
Dim customers = Await Task.WhenAll(tasks)
```

## Error Handling

### Try-Catch Patterns

```vb
' Modern structured exception handling
Try
    Dim result = Await ProcessDataAsync()
    Return result
Catch ex As ArgumentNullException
    ' Handle specific exception
    logger.LogError(ex, "Null argument in ProcessData")
    Throw
Catch ex As HttpRequestException
    ' Handle another specific exception
    logger.LogError(ex, "HTTP request failed")
    Return Nothing
Catch ex As Exception
    ' Catch-all (use sparingly)
    logger.LogError(ex, "Unexpected error")
    Throw
Finally
    ' Cleanup (always runs)
    connection?.Dispose()
End Try
```

### Exception Filters

```vb
' VB 14+ exception filters
Try
    ProcessData()
Catch ex As IOException When ex.Message.Contains("file not found")
    ' Handle specific IO error
    CreateDefaultFile()
Catch ex As IOException When ex.Message.Contains("access denied")
    ' Handle different IO error
    RequestPermissions()
End Try
```

### Custom Exceptions

```vb
' Define custom exception
Public Class CustomerNotFoundException
    Inherits Exception

    Public Property CustomerId As Integer

    Public Sub New(customerId As Integer)
        MyBase.New($"Customer {customerId} not found")
        Me.CustomerId = customerId
    End Sub

    Public Sub New(customerId As Integer, innerException As Exception)
        MyBase.New($"Customer {customerId} not found", innerException)
        Me.CustomerId = customerId
    End Sub
End Class

' Usage
If customer Is Nothing Then
    Throw New CustomerNotFoundException(customerId)
End If
```

## Property Patterns

### Auto-Implemented Properties

```vb
' Simple auto property
Public Property Name As String

' With default value
Public Property IsActive As Boolean = True

' Read-only auto property (VB 14+)
Public ReadOnly Property Id As Integer

' Can only be set in constructor
Public Sub New(id As Integer)
    Me.Id = id
End Sub
```

### Computed Properties

```vb
Public Class Customer
    Public Property FirstName As String
    Public Property LastName As String

    ' Computed property
    Public ReadOnly Property FullName As String
        Get
            Return $"{FirstName} {LastName}"
        End Get
    End Property

    ' Property with validation
    Private _age As Integer
    Public Property Age As Integer
        Get
            Return _age
        End Get
        Set(value As Integer)
            If value < 0 Or value > 150 Then
                Throw New ArgumentOutOfRangeException(NameOf(Age))
            End If
            _age = value
        End Set
    End Property
End Class
```

## Interfaces and Inheritance

### Interface Definition

```vb
Public Interface IRepository(Of T)
    Function GetByIdAsync(id As Integer) As Task(Of T)
    Function GetAllAsync() As Task(Of IEnumerable(Of T))
    Function AddAsync(entity As T) As Task
    Function UpdateAsync(entity As T) As Task
    Function DeleteAsync(id As Integer) As Task
End Interface

' Implementation
Public Class CustomerRepository
    Implements IRepository(Of Customer)

    Public Async Function GetByIdAsync(id As Integer) As Task(Of Customer) _
        Implements IRepository(Of Customer).GetByIdAsync

        Return Await dbContext.Customers.FindAsync(id)
    End Function

    ' ... other implementations
End Class
```

### Class Inheritance

```vb
' Base class
Public MustInherit Class BaseEntity
    Public Property Id As Integer
    Public Property CreatedAt As DateTime
    Public Property UpdatedAt As DateTime

    Public MustOverride Sub Validate()
End Class

' Derived class
Public Class Customer
    Inherits BaseEntity

    Public Property Name As String
    Public Property Email As String

    Public Overrides Sub Validate()
        If String.IsNullOrWhiteSpace(Name) Then
            Throw New ValidationException("Name is required")
        End If

        If Not Email.Contains("@") Then
            Throw New ValidationException("Invalid email format")
        End If
    End Sub
End Class
```

## Best Practices

### ✅ DO

```vb
' Always use Option Strict On
Option Strict On
Option Explicit On
Option Infer On

' Use modern syntax (LINQ, async/await, string interpolation)
Dim activeCustomers = Await customers.Where(Function(c) c.IsActive).ToListAsync()
Dim message = $"Found {activeCustomers.Count} active customers"

' Use meaningful names
Dim customerEmailAddress As String
Dim isCustomerActive As Boolean

' Use async/await for I/O operations
Public Async Function LoadDataAsync() As Task(Of Data)

' Use IDisposable pattern
Using connection = New SqlConnection(connectionString)
    ' Use connection
End Using

' Use XML comments for public APIs
''' <summary>
''' Gets a customer by their unique identifier.
''' </summary>
''' <param name="customerId">The customer ID to search for.</param>
''' <returns>The customer if found, Nothing otherwise.</returns>
Public Async Function GetCustomerAsync(customerId As Integer) As Task(Of Customer)
```

### ❌ DON'T

```vb
' Don't use On Error (use Try-Catch)
On Error Resume Next  ' Legacy VB6 style - AVOID

' Don't use late binding
Dim obj As Object = CreateObject("Excel.Application")  ' Use typed references

' Don't block on async
Dim result = GetDataAsync().Result  ' Can deadlock

' Don't use underscores in new code (legacy convention)
Private m_customerName As String  ' Use camelCase: _customerName

' Don't concatenate strings in loops
Dim result As String = ""
For Each item In items
    result &= item  ' Use StringBuilder or String.Join
Next

' Don't use Hungarian notation
Dim strName As String  ' Just use: Dim name As String
Dim intCount As Integer  ' Just use: Dim count As Integer
```

## Related Skills

When working with VB.NET core patterns, these skills enhance your workflow:
- **vb-winforms**: Windows Forms development patterns
- **vb-database**: ADO.NET and database integration patterns
- **testing-anti-patterns**: Testing best practices for VB.NET

## Remember

- **Option Strict On** is non-negotiable for type safety
- Use modern .NET features (LINQ, async/await, tuples)
- Avoid legacy VB6 patterns (On Error, late binding)
- Follow .NET naming conventions (PascalCase for public, camelCase for private)
- Use async/await for I/O operations
- Leverage LINQ for data queries
- Use structured exception handling (Try-Catch)
