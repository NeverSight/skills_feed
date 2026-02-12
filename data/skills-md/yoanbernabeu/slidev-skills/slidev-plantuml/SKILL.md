---
name: slidev-plantuml
description: Use PlantUML for UML diagrams in Slidev. Use this skill for complex UML diagrams, architecture visualizations, and technical documentation.
---

# PlantUML in Slidev

This skill covers using PlantUML for creating UML and technical diagrams in Slidev. PlantUML excels at creating standard UML diagrams with more detailed control than Mermaid.

## When to Use This Skill

- Creating standard UML diagrams
- Complex sequence diagrams with detailed notation
- Component and deployment diagrams
- Use case diagrams
- Activity diagrams with swimlanes
- C4 architecture diagrams

## Enabling PlantUML

PlantUML is supported via the `plantuml` code block:

````markdown
```plantuml
@startuml
Alice -> Bob: Hello
Bob --> Alice: Hi!
@enduml
```
````

## Sequence Diagrams

### Basic Sequence

````markdown
```plantuml
@startuml
participant User
participant "Web Server" as WS
participant Database as DB

User -> WS: HTTP Request
activate WS
WS -> DB: SQL Query
activate DB
DB --> WS: Result Set
deactivate DB
WS --> User: HTTP Response
deactivate WS
@enduml
```
````

### Participant Types

````markdown
```plantuml
@startuml
actor User
boundary "API Gateway" as API
control "Auth Service" as Auth
entity "User Entity" as UE
database "PostgreSQL" as DB
collections "Cache" as Cache
queue "Message Queue" as MQ

User -> API: Request
API -> Auth: Validate
Auth -> DB: Query
@enduml
```
````

### Grouping and Alternatives

````markdown
```plantuml
@startuml
actor User
participant Service

User -> Service: Login

alt Valid credentials
    Service --> User: Success
else Invalid credentials
    Service --> User: Error 401
end

group Optional
    User -> Service: Refresh Token
    Service --> User: New Token
end

loop Health Check
    Service -> Service: Ping
end
@enduml
```
````

### Notes

````markdown
```plantuml
@startuml
participant Alice
participant Bob

Alice -> Bob: Request
note left: This is a note\non the left

Bob --> Alice: Response
note right: This is a note\non the right

note over Alice, Bob: Note over both participants
@enduml
```
````

## Class Diagrams

### Basic Class

````markdown
```plantuml
@startuml
class User {
    -id: Long
    -email: String
    -password: String
    +login(): Boolean
    +logout(): void
}

class Order {
    -id: Long
    -total: BigDecimal
    +addItem(item: Item): void
    +removeItem(id: Long): void
    +checkout(): Boolean
}

User "1" --> "*" Order: places
@enduml
```
````

### Interfaces and Abstract Classes

````markdown
```plantuml
@startuml
interface Serializable {
    +serialize(): String
}

abstract class BaseEntity {
    #id: Long
    #createdAt: DateTime
    {abstract} +validate(): Boolean
}

class User extends BaseEntity implements Serializable {
    -name: String
    +serialize(): String
    +validate(): Boolean
}
@enduml
```
````

### Relationships

````markdown
```plantuml
@startuml
class A
class B
class C
class D
class E
class F

A --|> B : extends
C ..|> D : implements
E --* F : composition
G --o H : aggregation
I --> J : association
K ..> L : dependency
@enduml
```
````

### Packages

````markdown
```plantuml
@startuml
package "Domain Layer" {
    class User
    class Order
}

package "Infrastructure Layer" {
    class UserRepository
    class OrderRepository
}

package "Application Layer" {
    class UserService
    class OrderService
}

UserService --> User
UserService --> UserRepository
@enduml
```
````

## Use Case Diagrams

````markdown
```plantuml
@startuml
left to right direction

actor Customer
actor Admin

rectangle "E-Commerce System" {
    usecase "Browse Products" as UC1
    usecase "Add to Cart" as UC2
    usecase "Checkout" as UC3
    usecase "Manage Products" as UC4
    usecase "Process Orders" as UC5
}

Customer --> UC1
Customer --> UC2
Customer --> UC3
Admin --> UC4
Admin --> UC5

UC3 ..> UC2 : <<include>>
@enduml
```
````

## Activity Diagrams

### Basic Flow

````markdown
```plantuml
@startuml
start
:Receive Order;
if (Payment Valid?) then (yes)
    :Process Order;
    :Ship Items;
else (no)
    :Notify Customer;
    :Cancel Order;
endif
stop
@enduml
```
````

### Swimlanes

````markdown
```plantuml
@startuml
|Customer|
start
:Submit Order;
|Sales|
:Review Order;
if (Valid?) then (yes)
    |Warehouse|
    :Pick Items;
    :Pack Items;
    |Shipping|
    :Ship Package;
    |Customer|
    :Receive Package;
else (no)
    |Sales|
    :Reject Order;
    |Customer|
    :Receive Notification;
endif
stop
@enduml
```
````

### Parallel Processing

````markdown
```plantuml
@startuml
start
:Initialize;
fork
    :Process A;
fork again
    :Process B;
fork again
    :Process C;
end fork
:Merge Results;
stop
@enduml
```
````

## Component Diagrams

````markdown
```plantuml
@startuml
package "Frontend" {
    [React App] as Web
    [Mobile App] as Mobile
}

package "Backend" {
    [API Gateway]
    [Auth Service]
    [User Service]
    [Order Service]
}

package "Data Layer" {
    database "PostgreSQL" as DB
    database "Redis" as Cache
    queue "RabbitMQ" as MQ
}

Web --> [API Gateway]
Mobile --> [API Gateway]
[API Gateway] --> [Auth Service]
[API Gateway] --> [User Service]
[API Gateway] --> [Order Service]
[User Service] --> DB
[Order Service] --> DB
[Order Service] --> MQ
[Auth Service] --> Cache
@enduml
```
````

## Deployment Diagrams

````markdown
```plantuml
@startuml
node "AWS Cloud" {
    node "VPC" {
        node "Public Subnet" {
            [Load Balancer] as LB
        }

        node "Private Subnet" {
            node "ECS Cluster" {
                [API Container] as API
                [Worker Container] as Worker
            }
        }

        node "Data Subnet" {
            database "RDS PostgreSQL" as DB
            database "ElastiCache Redis" as Cache
        }
    }
}

actor User
User --> LB
LB --> API
API --> DB
API --> Cache
Worker --> DB
@enduml
```
````

## State Diagrams

````markdown
```plantuml
@startuml
[*] --> Draft

Draft --> Submitted : submit()
Submitted --> UnderReview : startReview()
UnderReview --> Approved : approve()
UnderReview --> Rejected : reject()
Rejected --> Draft : revise()
Approved --> Published : publish()
Published --> [*]

Draft : entry / loadDraft()
Draft : exit / saveDraft()

state UnderReview {
    [*] --> Reviewing
    Reviewing --> WaitingForInfo : requestInfo()
    WaitingForInfo --> Reviewing : infoProvided()
}
@enduml
```
````

## Styling

### Skinparams

````markdown
```plantuml
@startuml
skinparam backgroundColor #f8fafc
skinparam roundCorner 10
skinparam shadowing false

skinparam class {
    BackgroundColor #e0f2fe
    BorderColor #0284c7
    FontColor #0c4a6e
}

skinparam sequence {
    ArrowColor #0284c7
    LifeLineBorderColor #64748b
    ParticipantBackgroundColor #e0f2fe
}

class User {
    +name: String
}
@enduml
```
````

### Themes

````markdown
```plantuml
@startuml
!theme cerulean

class MyClass {
    +attribute: String
}
@enduml
```
````

Available themes: `cerulean`, `materia`, `minty`, `sandstone`, `sketchy-outline`, and more.

## C4 Model Diagrams

### Context Diagram

````markdown
```plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml

Person(user, "Customer", "A user of our system")
System(system, "E-Commerce", "Online shopping platform")
System_Ext(payment, "Payment Gateway", "Handles payments")
System_Ext(shipping, "Shipping Provider", "Delivers packages")

Rel(user, system, "Uses")
Rel(system, payment, "Processes payments via")
Rel(system, shipping, "Ships orders via")
@enduml
```
````

### Container Diagram

````markdown
```plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

Person(user, "Customer")

System_Boundary(system, "E-Commerce Platform") {
    Container(web, "Web App", "React", "User interface")
    Container(api, "API", "Node.js", "Business logic")
    ContainerDb(db, "Database", "PostgreSQL", "Stores data")
    Container(queue, "Queue", "RabbitMQ", "Async processing")
}

Rel(user, web, "Uses")
Rel(web, api, "API calls")
Rel(api, db, "Reads/Writes")
Rel(api, queue, "Publishes")
@enduml
```
````

## Configuration

### setup/plantuml.ts

```typescript
import { definePlantUmlSetup } from '@slidev/types'

export default definePlantUmlSetup(() => {
  return {
    // Server URL (default uses public server)
    server: 'https://www.plantuml.com/plantuml',
  }
})
```

## Mermaid vs PlantUML

| Feature | Mermaid | PlantUML |
|---------|---------|----------|
| Syntax | Simpler | More verbose |
| UML compliance | Partial | Full |
| Rendering | Client-side | Server-side |
| C4 diagrams | No | Yes |
| Swimlanes | No | Yes |
| Customization | Limited | Extensive |

## Best Practices

1. **Use PlantUML for**: Standard UML, C4, complex diagrams
2. **Use Mermaid for**: Simple flowcharts, quick visualizations
3. **Add skinparams**: Customize for your presentation theme
4. **Keep diagrams focused**: One concept per diagram
5. **Use proper UML notation**: Follow standards for clarity

## Output Format

When creating PlantUML diagrams:

```
DIAGRAM TYPE: [sequence/class/component/etc.]
PURPOSE: [What it illustrates]

```plantuml
@startuml
[skinparams if needed]

[diagram content]

@enduml
```

KEY ELEMENTS:
- [Element]: [What it represents]

NOTES:
- [Any additional context]
```
