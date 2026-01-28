---
name: java-best-practices
description: Comprehensive Java development best practices covering SOLID principles, DRY, Clean Code, Java-specific patterns (Optional, immutability, streams, lambdas), exception handling, collections, concurrency, testing with JUnit 5 and Mockito, code organization, performance optimization, and common anti-patterns. Essential reference for uncle-duke-java agent during code reviews and architecture guidance.
allowed-tools: Read, Grep, Glob
---

# Java Best Practices

## Purpose

This skill provides comprehensive best practices for Java development, serving as a reference guide during code reviews and architectural decisions. It covers SOLID principles, DRY, Clean Code, Java-specific patterns, testing strategies, and common anti-patterns.

**When to use this skill:**
- Conducting code reviews of Java projects
- Writing new Java code
- Refactoring existing Java code
- Evaluating architecture and design decisions
- Teaching Java best practices to team members
- Working with Spring Framework applications

## Context

High-quality Java code is essential for building maintainable, scalable, and robust applications. This skill documents industry-standard practices that emphasize:

- **SOLID Principles**: Foundation for well-designed object-oriented code
- **Clean Code**: Readable, maintainable, and self-documenting code
- **Java-Specific Features**: Proper use of modern Java features (8+)
- **Testability**: Code that's easy to test and verify
- **Performance**: Efficient use of Java language and JVM features
- **Spring Framework**: Best practices for Spring-based applications

This skill is designed to be referenced by the `uncle-duke-java` agent during code reviews and by developers when writing Java code.

## Prerequisites

**Required Knowledge:**
- Java fundamentals (Java 8+)
- Object-oriented programming concepts
- Basic understanding of design patterns
- Familiarity with Spring Framework (for Spring-specific sections)

**Required Tools:**
- JDK 8 or higher (11, 17, or 21 recommended)
- Maven or Gradle for build management
- JUnit 5 for testing
- Mockito for mocking
- IDE with Java support (IntelliJ IDEA, Eclipse, VS Code)

**Expected Project Structure:**
```
project/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/example/
│   │   │       ├── model/
│   │   │       ├── service/
│   │   │       ├── repository/
│   │   │       ├── controller/
│   │   │       └── util/
│   │   └── resources/
│   │       └── application.properties
│   └── test/
│       └── java/
│           └── com/example/
├── pom.xml (or build.gradle)
└── README.md
```

---

## SOLID Principles in Java

### Single Responsibility Principle (SRP)

**Rule:** A class should have only one reason to change. Each class should have a single, well-defined responsibility.

**Why it matters:** Classes with multiple responsibilities are harder to understand, test, and maintain. Changes to one responsibility can affect the others.

#### SRP in Practice

❌ **Bad - Multiple Responsibilities:**
```java
// This class violates SRP: it handles user data, validation, persistence, and email
public class User {
    private String email;
    private String password;

    // Responsibility 1: Data validation
    public boolean isValid() {
        return email != null && email.contains("@")
            && password != null && password.length() >= 8;
    }

    // Responsibility 2: Database operations
    public void save() {
        Connection conn = DriverManager.getConnection("jdbc:...");
        PreparedStatement ps = conn.prepareStatement("INSERT INTO users...");
        ps.setString(1, email);
        ps.setString(2, password);
        ps.executeUpdate();
    }

    // Responsibility 3: Email operations
    public void sendWelcomeEmail() {
        EmailService.send(email, "Welcome!", "Welcome to our app");
    }

    // Responsibility 4: Password encryption
    public void encryptPassword() {
        this.password = BCrypt.hashpw(password, BCrypt.gensalt());
    }
}
```

**Issues:**
- User class has 4 responsibilities: data, validation, persistence, email
- Changes to validation logic affect the User class
- Changes to database schema affect the User class
- Changes to email templates affect the User class
- Difficult to test individual responsibilities

✅ **Good - Single Responsibility:**
```java
// Responsibility: Hold user data
public class User {
    private final String email;
    private final String passwordHash;

    public User(String email, String passwordHash) {
        this.email = email;
        this.passwordHash = passwordHash;
    }

    public String getEmail() { return email; }
    public String getPasswordHash() { return passwordHash; }
}

// Responsibility: Validate user data
public class UserValidator {
    public ValidationResult validate(String email, String password) {
        List<String> errors = new ArrayList<>();

        if (email == null || !email.contains("@")) {
            errors.add("Invalid email format");
        }
        if (password == null || password.length() < 8) {
            errors.add("Password must be at least 8 characters");
        }

        return new ValidationResult(errors.isEmpty(), errors);
    }
}

// Responsibility: Persist user data
public class UserRepository {
    private final DataSource dataSource;

    public UserRepository(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    public void save(User user) {
        try (Connection conn = dataSource.getConnection();
             PreparedStatement ps = conn.prepareStatement(
                 "INSERT INTO users (email, password_hash) VALUES (?, ?)")) {
            ps.setString(1, user.getEmail());
            ps.setString(2, user.getPasswordHash());
            ps.executeUpdate();
        } catch (SQLException e) {
            throw new DataAccessException("Failed to save user", e);
        }
    }
}

// Responsibility: Send emails
public class EmailService {
    public void sendWelcomeEmail(User user) {
        send(user.getEmail(), "Welcome!", "Welcome to our app");
    }

    private void send(String to, String subject, String body) {
        // Email sending logic
    }
}

// Responsibility: Hash passwords
public class PasswordEncoder {
    public String encode(String rawPassword) {
        return BCrypt.hashpw(rawPassword, BCrypt.gensalt());
    }

    public boolean matches(String rawPassword, String encodedPassword) {
        return BCrypt.checkpw(rawPassword, encodedPassword);
    }
}
```

**Benefits:**
- Each class has one clear responsibility
- Easy to test each responsibility in isolation
- Changes to one concern don't affect others
- Classes are small and focused

### Open/Closed Principle (OCP)

**Rule:** Software entities (classes, modules, functions) should be open for extension but closed for modification.

**Why it matters:** You should be able to add new functionality without changing existing code, reducing the risk of breaking existing features.

#### OCP in Practice

❌ **Bad - Violates OCP:**
```java
public class PaymentProcessor {
    public void processPayment(String paymentType, double amount) {
        if (paymentType.equals("CREDIT_CARD")) {
            // Process credit card payment
            System.out.println("Processing credit card payment: $" + amount);
        } else if (paymentType.equals("PAYPAL")) {
            // Process PayPal payment
            System.out.println("Processing PayPal payment: $" + amount);
        } else if (paymentType.equals("BITCOIN")) {
            // Process Bitcoin payment
            System.out.println("Processing Bitcoin payment: $" + amount);
        }
        // Adding new payment method requires modifying this class!
    }
}
```

**Issues:**
- Must modify PaymentProcessor to add new payment types
- Violates OCP (not closed for modification)
- Growing if-else chain
- Hard to test individual payment types

✅ **Good - Follows OCP:**
```java
// Abstract payment interface
public interface PaymentMethod {
    void process(double amount);
}

// Concrete implementations
public class CreditCardPayment implements PaymentMethod {
    @Override
    public void process(double amount) {
        System.out.println("Processing credit card payment: $" + amount);
        // Credit card specific logic
    }
}

public class PayPalPayment implements PaymentMethod {
    @Override
    public void process(double amount) {
        System.out.println("Processing PayPal payment: $" + amount);
        // PayPal specific logic
    }
}

public class BitcoinPayment implements PaymentMethod {
    @Override
    public void process(double amount) {
        System.out.println("Processing Bitcoin payment: $" + amount);
        // Bitcoin specific logic
    }
}

// Processor delegates to payment method
public class PaymentProcessor {
    public void processPayment(PaymentMethod paymentMethod, double amount) {
        paymentMethod.process(amount);
    }
}

// Usage
PaymentProcessor processor = new PaymentProcessor();
processor.processPayment(new CreditCardPayment(), 100.0);
processor.processPayment(new PayPalPayment(), 50.0);

// Adding new payment method: just create new class, no modification needed!
public class ApplePayPayment implements PaymentMethod {
    @Override
    public void process(double amount) {
        System.out.println("Processing Apple Pay payment: $" + amount);
    }
}
```

**Benefits:**
- New payment methods added without modifying existing code
- Each payment type is independently testable
- Follows OCP: open for extension, closed for modification
- Clear separation of concerns

#### OCP with Strategy Pattern

✅ **Advanced Example - Discount Strategies:**
```java
// Strategy interface
public interface DiscountStrategy {
    double applyDiscount(double price);
}

// Concrete strategies
public class NoDiscount implements DiscountStrategy {
    @Override
    public double applyDiscount(double price) {
        return price;
    }
}

public class PercentageDiscount implements DiscountStrategy {
    private final double percentage;

    public PercentageDiscount(double percentage) {
        this.percentage = percentage;
    }

    @Override
    public double applyDiscount(double price) {
        return price * (1 - percentage / 100);
    }
}

public class FixedAmountDiscount implements DiscountStrategy {
    private final double amount;

    public FixedAmountDiscount(double amount) {
        this.amount = amount;
    }

    @Override
    public double applyDiscount(double price) {
        return Math.max(0, price - amount);
    }
}

// Context uses strategy
public class PriceCalculator {
    private final DiscountStrategy discountStrategy;

    public PriceCalculator(DiscountStrategy discountStrategy) {
        this.discountStrategy = discountStrategy;
    }

    public double calculateFinalPrice(double originalPrice) {
        return discountStrategy.applyDiscount(originalPrice);
    }
}

// Usage
PriceCalculator calc1 = new PriceCalculator(new PercentageDiscount(10));
double price1 = calc1.calculateFinalPrice(100); // 90.0

PriceCalculator calc2 = new PriceCalculator(new FixedAmountDiscount(15));
double price2 = calc2.calculateFinalPrice(100); // 85.0
```

### Liskov Substitution Principle (LSP)

**Rule:** Objects of a superclass should be replaceable with objects of a subclass without breaking the application. Subtypes must be substitutable for their base types.

**Why it matters:** Violating LSP leads to unexpected behavior and breaks polymorphism.

#### LSP in Practice

❌ **Bad - Violates LSP:**
```java
public class Rectangle {
    protected int width;
    protected int height;

    public void setWidth(int width) {
        this.width = width;
    }

    public void setHeight(int height) {
        this.height = height;
    }

    public int getArea() {
        return width * height;
    }
}

// Square violates LSP because it changes behavior of setters
public class Square extends Rectangle {
    @Override
    public void setWidth(int width) {
        this.width = width;
        this.height = width; // Side effect!
    }

    @Override
    public void setHeight(int height) {
        this.width = height; // Side effect!
        this.height = height;
    }
}

// This test works for Rectangle but fails for Square
public void testRectangle(Rectangle rect) {
    rect.setWidth(5);
    rect.setHeight(4);
    assertEquals(20, rect.getArea()); // Fails for Square! (25 instead of 20)
}
```

**Issues:**
- Square changes the behavior of Rectangle methods
- Cannot substitute Square for Rectangle
- Violates LSP and breaks polymorphism

✅ **Good - Follows LSP:**
```java
// Common interface for shapes
public interface Shape {
    int getArea();
}

// Rectangle implementation
public class Rectangle implements Shape {
    private final int width;
    private final int height;

    public Rectangle(int width, int height) {
        this.width = width;
        this.height = height;
    }

    @Override
    public int getArea() {
        return width * height;
    }

    public int getWidth() { return width; }
    public int getHeight() { return height; }
}

// Square implementation (no inheritance from Rectangle)
public class Square implements Shape {
    private final int side;

    public Square(int side) {
        this.side = side;
    }

    @Override
    public int getArea() {
        return side * side;
    }

    public int getSide() { return side; }
}

// Works for any Shape
public int calculateTotalArea(List<Shape> shapes) {
    return shapes.stream()
                 .mapToInt(Shape::getArea)
                 .sum();
}
```

**Benefits:**
- Square and Rectangle are independent
- Both implement Shape contract correctly
- Can substitute any Shape implementation
- No unexpected behavior

#### LSP - Pre and Post Conditions

✅ **Good - Maintains Contracts:**
```java
public interface BankAccount {
    // Precondition: amount > 0
    // Postcondition: balance increased by amount
    void deposit(double amount);

    // Precondition: amount > 0 and amount <= balance
    // Postcondition: balance decreased by amount
    void withdraw(double amount) throws InsufficientFundsException;

    double getBalance();
}

public class SavingsAccount implements BankAccount {
    private double balance;

    @Override
    public void deposit(double amount) {
        if (amount <= 0) {
            throw new IllegalArgumentException("Amount must be positive");
        }
        balance += amount;
    }

    @Override
    public void withdraw(double amount) throws InsufficientFundsException {
        if (amount <= 0) {
            throw new IllegalArgumentException("Amount must be positive");
        }
        if (amount > balance) {
            throw new InsufficientFundsException();
        }
        balance -= amount;
    }

    @Override
    public double getBalance() {
        return balance;
    }
}

// Subclass maintains contracts (LSP)
public class CheckingAccount implements BankAccount {
    private double balance;
    private final double overdraftLimit;

    public CheckingAccount(double overdraftLimit) {
        this.overdraftLimit = overdraftLimit;
    }

    @Override
    public void deposit(double amount) {
        if (amount <= 0) {
            throw new IllegalArgumentException("Amount must be positive");
        }
        balance += amount; // Same postcondition
    }

    @Override
    public void withdraw(double amount) throws InsufficientFundsException {
        if (amount <= 0) {
            throw new IllegalArgumentException("Amount must be positive");
        }
        // Can weaken precondition (allow overdraft) but not strengthen
        if (amount > balance + overdraftLimit) {
            throw new InsufficientFundsException();
        }
        balance -= amount; // Same postcondition
    }

    @Override
    public double getBalance() {
        return balance;
    }
}
```

### Interface Segregation Principle (ISP)

**Rule:** Clients should not be forced to depend on interfaces they don't use. Many specific interfaces are better than one general-purpose interface.

**Why it matters:** Large interfaces force implementations to provide methods they don't need, leading to empty implementations and tight coupling.

#### ISP in Practice

❌ **Bad - Fat Interface:**
```java
// Fat interface forces all implementations to provide all methods
public interface Worker {
    void work();
    void eat();
    void sleep();
    void getSalary();
    void attendMeeting();
}

// Robot doesn't eat or sleep but is forced to implement these methods
public class RobotWorker implements Worker {
    @Override
    public void work() {
        System.out.println("Robot working");
    }

    @Override
    public void eat() {
        // Doesn't make sense for robots!
        throw new UnsupportedOperationException("Robots don't eat");
    }

    @Override
    public void sleep() {
        // Doesn't make sense for robots!
        throw new UnsupportedOperationException("Robots don't sleep");
    }

    @Override
    public void getSalary() {
        throw new UnsupportedOperationException("Robots don't get paid");
    }

    @Override
    public void attendMeeting() {
        System.out.println("Robot attending meeting");
    }
}
```

**Issues:**
- Robot forced to implement biological methods
- Throwing UnsupportedOperationException is a code smell
- Violates ISP
- Tight coupling to irrelevant methods

✅ **Good - Segregated Interfaces:**
```java
// Segregated interfaces - clients depend only on what they need
public interface Workable {
    void work();
}

public interface Eatable {
    void eat();
}

public interface Sleepable {
    void sleep();
}

public interface Payable {
    void getSalary();
}

public interface MeetingAttendee {
    void attendMeeting();
}

// Human implements relevant interfaces
public class HumanWorker implements Workable, Eatable, Sleepable, Payable, MeetingAttendee {
    @Override
    public void work() {
        System.out.println("Human working");
    }

    @Override
    public void eat() {
        System.out.println("Human eating");
    }

    @Override
    public void sleep() {
        System.out.println("Human sleeping");
    }

    @Override
    public void getSalary() {
        System.out.println("Human receiving salary");
    }

    @Override
    public void attendMeeting() {
        System.out.println("Human attending meeting");
    }
}

// Robot only implements relevant interfaces
public class RobotWorker implements Workable, MeetingAttendee {
    @Override
    public void work() {
        System.out.println("Robot working");
    }

    @Override
    public void attendMeeting() {
        System.out.println("Robot attending meeting");
    }
}
```

**Benefits:**
- Implementations only provide methods that make sense
- No UnsupportedOperationException needed
- Clear separation of concerns
- Flexible composition

### Dependency Inversion Principle (DIP)

**Rule:** High-level modules should not depend on low-level modules. Both should depend on abstractions. Abstractions should not depend on details. Details should depend on abstractions.

**Why it matters:** DIP decouples code, making it more flexible, testable, and maintainable.

#### DIP in Practice

❌ **Bad - High-level depends on low-level:**
```java
// Low-level module
public class MySQLDatabase {
    public void save(String data) {
        System.out.println("Saving to MySQL: " + data);
    }
}

// High-level module depends on concrete low-level module
public class UserService {
    private MySQLDatabase database; // Concrete dependency!

    public UserService() {
        this.database = new MySQLDatabase(); // Tight coupling!
    }

    public void createUser(String userData) {
        // Business logic
        database.save(userData);
    }
}
```

**Issues:**
- UserService tightly coupled to MySQLDatabase
- Cannot switch to PostgreSQL without modifying UserService
- Hard to test (can't mock database)
- Violates DIP

✅ **Good - Both depend on abstraction:**
```java
// Abstraction
public interface Database {
    void save(String data);
}

// Low-level modules depend on abstraction
public class MySQLDatabase implements Database {
    @Override
    public void save(String data) {
        System.out.println("Saving to MySQL: " + data);
    }
}

public class PostgreSQLDatabase implements Database {
    @Override
    public void save(String data) {
        System.out.println("Saving to PostgreSQL: " + data);
    }
}

public class MongoDatabase implements Database {
    @Override
    public void save(String data) {
        System.out.println("Saving to MongoDB: " + data);
    }
}

// High-level module depends on abstraction
public class UserService {
    private final Database database; // Abstraction!

    // Dependency injected through constructor
    public UserService(Database database) {
        this.database = database;
    }

    public void createUser(String userData) {
        // Business logic
        database.save(userData);
    }
}

// Usage - client chooses implementation
Database db = new MySQLDatabase();
UserService service = new UserService(db);
service.createUser("John Doe");

// Easy to switch implementations
Database postgresDb = new PostgreSQLDatabase();
UserService postgresService = new UserService(postgresDb);

// Easy to test with mock
Database mockDb = mock(Database.class);
UserService testService = new UserService(mockDb);
```

**Benefits:**
- UserService decoupled from database implementation
- Easy to switch database implementations
- Easy to test with mocks
- Follows DIP

### SOLID Principles in Spring Framework

Spring Framework is built on SOLID principles, particularly Dependency Inversion.

#### Dependency Injection in Spring

✅ **Spring DI Example:**
```java
// Abstraction
public interface UserRepository {
    User findById(Long id);
    void save(User user);
}

// Implementation
@Repository
public class JpaUserRepository implements UserRepository {
    @PersistenceContext
    private EntityManager entityManager;

    @Override
    public User findById(Long id) {
        return entityManager.find(User.class, id);
    }

    @Override
    public void save(User user) {
        entityManager.persist(user);
    }
}

// Service depends on abstraction
@Service
public class UserService {
    private final UserRepository userRepository;

    // Constructor injection (recommended)
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public User getUser(Long id) {
        return userRepository.findById(id);
    }
}

// Controller depends on service abstraction
@RestController
@RequestMapping("/users")
public class UserController {
    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping("/{id}")
    public ResponseEntity<User> getUser(@PathVariable Long id) {
        User user = userService.getUser(id);
        return ResponseEntity.ok(user);
    }
}
```

**Spring DI Best Practices:**
- Use constructor injection (required dependencies, immutability)
- Prefer field injection only for optional dependencies
- Depend on interfaces, not concrete classes
- Use `@Qualifier` when multiple implementations exist

---

## DRY (Don't Repeat Yourself)

**Rule:** Every piece of knowledge must have a single, unambiguous, authoritative representation within a system.

**Why it matters:** Duplication leads to inconsistencies, harder maintenance, and more bugs.

### Identifying Code Duplication

❌ **Bad - Obvious Duplication:**
```java
public class OrderService {
    public void processOnlineOrder(Order order) {
        // Validate
        if (order == null) {
            throw new IllegalArgumentException("Order cannot be null");
        }
        if (order.getItems().isEmpty()) {
            throw new IllegalArgumentException("Order must have items");
        }
        if (order.getTotalAmount() <= 0) {
            throw new IllegalArgumentException("Order total must be positive");
        }

        // Process
        System.out.println("Processing online order: " + order.getId());
        order.setStatus(OrderStatus.PROCESSING);
        saveOrder(order);
    }

    public void processPhoneOrder(Order order) {
        // Same validation - DUPLICATION!
        if (order == null) {
            throw new IllegalArgumentException("Order cannot be null");
        }
        if (order.getItems().isEmpty()) {
            throw new IllegalArgumentException("Order must have items");
        }
        if (order.getTotalAmount() <= 0) {
            throw new IllegalArgumentException("Order total must be positive");
        }

        // Process
        System.out.println("Processing phone order: " + order.getId());
        order.setStatus(OrderStatus.PROCESSING);
        saveOrder(order);
    }
}
```

✅ **Good - Extract Common Logic:**
```java
public class OrderService {
    public void processOnlineOrder(Order order) {
        validateOrder(order);
        processOrder(order, "online");
    }

    public void processPhoneOrder(Order order) {
        validateOrder(order);
        processOrder(order, "phone");
    }

    private void validateOrder(Order order) {
        if (order == null) {
            throw new IllegalArgumentException("Order cannot be null");
        }
        if (order.getItems().isEmpty()) {
            throw new IllegalArgumentException("Order must have items");
        }
        if (order.getTotalAmount() <= 0) {
            throw new IllegalArgumentException("Order total must be positive");
        }
    }

    private void processOrder(Order order, String type) {
        System.out.println("Processing " + type + " order: " + order.getId());
        order.setStatus(OrderStatus.PROCESSING);
        saveOrder(order);
    }
}
```

### Utility Classes and Helper Methods

✅ **Create Utility Classes for Reusable Logic:**
```java
public final class StringUtils {
    private StringUtils() {
        // Prevent instantiation
    }

    public static boolean isBlank(String str) {
        return str == null || str.trim().isEmpty();
    }

    public static String capitalize(String str) {
        if (isBlank(str)) {
            return str;
        }
        return str.substring(0, 1).toUpperCase() + str.substring(1).toLowerCase();
    }

    public static String truncate(String str, int maxLength) {
        if (str == null || str.length() <= maxLength) {
            return str;
        }
        return str.substring(0, maxLength) + "...";
    }
}

// Usage
if (StringUtils.isBlank(username)) {
    throw new ValidationException("Username is required");
}

String displayName = StringUtils.capitalize(name);
```

### Generics for Reusability

✅ **Use Generics to Avoid Duplication:**
```java
// Instead of creating separate classes for different types
public class GenericRepository<T, ID> {
    private final Class<T> entityClass;

    @PersistenceContext
    private EntityManager entityManager;

    public GenericRepository(Class<T> entityClass) {
        this.entityClass = entityClass;
    }

    public Optional<T> findById(ID id) {
        T entity = entityManager.find(entityClass, id);
        return Optional.ofNullable(entity);
    }

    public List<T> findAll() {
        CriteriaQuery<T> query = entityManager.getCriteriaBuilder()
            .createQuery(entityClass);
        query.select(query.from(entityClass));
        return entityManager.createQuery(query).getResultList();
    }

    public void save(T entity) {
        entityManager.persist(entity);
    }

    public void delete(T entity) {
        entityManager.remove(entity);
    }
}

// Concrete repositories extend generic repository
@Repository
public class UserRepository extends GenericRepository<User, Long> {
    public UserRepository() {
        super(User.class);
    }

    // Add User-specific queries
    public Optional<User> findByEmail(String email) {
        // Custom query
    }
}
```

---

## Clean Code Principles

### Meaningful Names

**Rule:** Names should reveal intent, be pronounceable, and be searchable.

❌ **Bad Names:**
```java
int d; // elapsed time in days
String yyyymmdd;
List<int[]> list1;

public void getData() {
    // What data?
}
```

✅ **Good Names:**
```java
int elapsedTimeInDays;
String formattedDate;
List<Customer> activeCustomers;

public Customer getCustomerById(Long customerId) {
    // Clear what this method does
}
```

#### Naming Conventions

```java
// Classes: PascalCase, nouns
public class CustomerService { }
public class OrderRepository { }

// Interfaces: PascalCase, often adjectives or nouns
public interface Serializable { }
public interface UserRepository { }

// Methods: camelCase, verbs
public void calculateTotal() { }
public Customer findCustomerById(Long id) { }

// Variables: camelCase, nouns
String customerName;
int orderCount;
boolean isActive;

// Constants: UPPER_SNAKE_CASE
public static final int MAX_RETRY_COUNT = 3;
public static final String DEFAULT_ENCODING = "UTF-8";

// Packages: lowercase, periods
package com.example.service;
package com.example.repository;

// Boolean methods/variables: is, has, can
boolean isValid();
boolean hasPermission();
boolean canExecute();
```

### Function Size and Complexity

**Rule:** Functions should be small and do one thing. Aim for 5-20 lines per method.

❌ **Bad - Large, Complex Method:**
```java
public void processOrder(Order order) {
    // Validation
    if (order == null) throw new IllegalArgumentException();
    if (order.getItems().isEmpty()) throw new IllegalArgumentException();

    // Calculate total
    double total = 0;
    for (OrderItem item : order.getItems()) {
        double itemPrice = item.getPrice();
        int quantity = item.getQuantity();
        double discount = item.getDiscount();
        total += (itemPrice * quantity) * (1 - discount);
    }
    order.setTotal(total);

    // Apply coupon
    if (order.getCoupon() != null) {
        String couponCode = order.getCoupon().getCode();
        if (couponCode.startsWith("SAVE")) {
            total *= 0.9;
        } else if (couponCode.startsWith("BIG")) {
            total *= 0.8;
        }
        order.setTotal(total);
    }

    // Check inventory
    for (OrderItem item : order.getItems()) {
        int available = inventoryService.getAvailableQuantity(item.getProductId());
        if (available < item.getQuantity()) {
            throw new InsufficientInventoryException();
        }
    }

    // Save order
    orderRepository.save(order);

    // Send email
    emailService.send(order.getCustomer().getEmail(), "Order Confirmation",
        "Your order " + order.getId() + " has been confirmed");

    // Update inventory
    for (OrderItem item : order.getItems()) {
        inventoryService.decrementQuantity(item.getProductId(), item.getQuantity());
    }
}
```

✅ **Good - Small, Focused Methods:**
```java
public void processOrder(Order order) {
    validateOrder(order);
    calculateOrderTotal(order);
    applyCouponDiscount(order);
    checkInventoryAvailability(order);
    saveOrder(order);
    sendConfirmationEmail(order);
    updateInventory(order);
}

private void validateOrder(Order order) {
    if (order == null) {
        throw new IllegalArgumentException("Order cannot be null");
    }
    if (order.getItems().isEmpty()) {
        throw new IllegalArgumentException("Order must contain items");
    }
}

private void calculateOrderTotal(Order order) {
    double total = order.getItems().stream()
        .mapToDouble(this::calculateItemTotal)
        .sum();
    order.setTotal(total);
}

private double calculateItemTotal(OrderItem item) {
    return item.getPrice() * item.getQuantity() * (1 - item.getDiscount());
}

private void applyCouponDiscount(Order order) {
    if (order.getCoupon() == null) {
        return;
    }

    double discountMultiplier = getDiscountMultiplier(order.getCoupon());
    order.setTotal(order.getTotal() * discountMultiplier);
}

private double getDiscountMultiplier(Coupon coupon) {
    String code = coupon.getCode();
    if (code.startsWith("SAVE")) return 0.9;
    if (code.startsWith("BIG")) return 0.8;
    return 1.0;
}

private void checkInventoryAvailability(Order order) {
    for (OrderItem item : order.getItems()) {
        int available = inventoryService.getAvailableQuantity(item.getProductId());
        if (available < item.getQuantity()) {
            throw new InsufficientInventoryException(
                "Product " + item.getProductId() + " has insufficient inventory");
        }
    }
}

private void saveOrder(Order order) {
    orderRepository.save(order);
}

private void sendConfirmationEmail(Order order) {
    String email = order.getCustomer().getEmail();
    String subject = "Order Confirmation";
    String body = String.format("Your order %s has been confirmed", order.getId());
    emailService.send(email, subject, body);
}

private void updateInventory(Order order) {
    order.getItems().forEach(item ->
        inventoryService.decrementQuantity(item.getProductId(), item.getQuantity())
    );
}
```

**Benefits:**
- Each method has a clear, single purpose
- Easy to understand and test
- Main method reads like a table of contents
- Reusable helper methods

### Comment Best Practices

**Rule:** Code should be self-explanatory. Comments should explain WHY, not WHAT.

❌ **Bad Comments:**
```java
// Set the flag to true
isActive = true;

// Loop through users
for (User user : users) {
    // Check if user is active
    if (user.isActive()) {
        // Add to list
        activeUsers.add(user);
    }
}

// This is the UserService class
public class UserService {
}
```

✅ **Good Comments:**
```java
// No comment needed - code is self-explanatory
isActive = true;

List<User> activeUsers = users.stream()
    .filter(User::isActive)
    .collect(Collectors.toList());

// Good: Explains WHY, not WHAT
// We use exponential backoff to avoid overwhelming the external API
// after multiple failures (circuit breaker pattern)
private int calculateRetryDelay(int attemptNumber) {
    return (int) Math.pow(2, attemptNumber) * 1000;
}

// Good: JavaDoc for public API
/**
 * Transfers funds between accounts atomically.
 *
 * @param fromAccount source account (must have sufficient balance)
 * @param toAccount destination account
 * @param amount amount to transfer (must be positive)
 * @throws InsufficientFundsException if source account lacks funds
 * @throws IllegalArgumentException if amount is negative or zero
 */
public void transferFunds(Account fromAccount, Account toAccount, double amount)
    throws InsufficientFundsException {
    // Implementation
}

// Good: Explains non-obvious business rule
// Tax calculation excludes shipping but includes discount adjustments
// per IRS regulation 2024-15
double taxableAmount = subtotal - discount;
```

**When to Comment:**
- Public APIs (JavaDoc)
- Complex algorithms (explain approach)
- Business rules (regulatory requirements)
- Workarounds (why the workaround is needed)
- TODO/FIXME (with ticket numbers)

**When NOT to Comment:**
- Obvious code
- Commented-out code (delete it, use version control)
- Change logs (use git)

### Error Handling

**Rule:** Use exceptions for exceptional cases. Don't use exceptions for control flow.

❌ **Bad Error Handling:**
```java
// Using exceptions for control flow
public User findUser(Long id) {
    try {
        return userRepository.findById(id);
    } catch (NotFoundException e) {
        return null; // Swallowing exception
    }
}

// Catching generic Exception
public void processData(String data) {
    try {
        // Complex logic
    } catch (Exception e) {
        // Too broad!
    }
}

// Empty catch block
try {
    riskyOperation();
} catch (IOException e) {
    // Ignored - NEVER DO THIS
}
```

✅ **Good Error Handling:**
```java
// Use Optional for "not found" scenarios
public Optional<User> findUser(Long id) {
    return userRepository.findById(id);
}

// Catch specific exceptions
public void processData(String data) {
    try {
        parseAndValidate(data);
        saveToDatabase(data);
    } catch (JsonParseException e) {
        log.error("Failed to parse JSON data: {}", data, e);
        throw new DataProcessingException("Invalid JSON format", e);
    } catch (DataAccessException e) {
        log.error("Database error while saving data", e);
        throw new DataProcessingException("Failed to save data", e);
    }
}

// Always handle or rethrow exceptions
try {
    riskyOperation();
} catch (IOException e) {
    log.error("Operation failed", e);
    throw new ApplicationException("Failed to perform operation", e);
}

// Use try-with-resources for auto-closeable resources
public String readFile(String path) throws IOException {
    try (BufferedReader reader = new BufferedReader(new FileReader(path))) {
        return reader.lines().collect(Collectors.joining("\n"));
    }
    // Reader automatically closed, even if exception occurs
}
```

### Code Organization

**Rule:** Organize code logically within classes. Related methods should be close together.

✅ **Good Class Organization:**
```java
public class UserService {
    // 1. Constants
    private static final int MAX_LOGIN_ATTEMPTS = 3;
    private static final long LOCKOUT_DURATION_MINUTES = 30;

    // 2. Static fields
    private static final Logger log = LoggerFactory.getLogger(UserService.class);

    // 3. Instance fields
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final EmailService emailService;

    // 4. Constructors
    public UserService(UserRepository userRepository,
                       PasswordEncoder passwordEncoder,
                       EmailService emailService) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.emailService = emailService;
    }

    // 5. Public methods (grouped by functionality)

    // User creation methods
    public User registerUser(UserRegistrationDto dto) {
        validateRegistration(dto);
        User user = createUser(dto);
        sendWelcomeEmail(user);
        return user;
    }

    // User authentication methods
    public AuthToken login(String email, String password) {
        User user = findUserByEmail(email);
        validatePassword(user, password);
        return generateAuthToken(user);
    }

    // 6. Private helper methods (near methods that use them)

    private void validateRegistration(UserRegistrationDto dto) {
        // Validation logic
    }

    private User createUser(UserRegistrationDto dto) {
        // Creation logic
    }

    private void sendWelcomeEmail(User user) {
        emailService.send(user.getEmail(), "Welcome!", getWelcomeEmailBody());
    }

    private User findUserByEmail(String email) {
        return userRepository.findByEmail(email)
            .orElseThrow(() -> new UserNotFoundException(email));
    }

    private void validatePassword(User user, String password) {
        if (!passwordEncoder.matches(password, user.getPasswordHash())) {
            throw new AuthenticationException("Invalid password");
        }
    }

    private AuthToken generateAuthToken(User user) {
        // Token generation logic
    }

    private String getWelcomeEmailBody() {
        return "Welcome to our application!";
    }
}
```

---

## Java-Specific Best Practices

### Using Optional Instead of Null

**Rule:** Use `Optional<T>` to represent values that may be absent. Never return null for collections.

❌ **Bad - Returning Null:**
```java
public User findUser(Long id) {
    User user = database.find(id);
    return user; // May return null!
}

// Caller must remember to check null
User user = findUser(123L);
if (user != null) {
    // Use user
}
```

✅ **Good - Using Optional:**
```java
public Optional<User> findUser(Long id) {
    User user = database.find(id);
    return Optional.ofNullable(user);
}

// Caller forced to handle absence
Optional<User> userOpt = findUser(123L);

// Method 1: ifPresent
userOpt.ifPresent(user -> System.out.println(user.getName()));

// Method 2: orElse
User user = userOpt.orElse(createDefaultUser());

// Method 3: orElseThrow
User user = userOpt.orElseThrow(() ->
    new UserNotFoundException("User 123 not found"));

// Method 4: map/flatMap
String email = userOpt
    .map(User::getEmail)
    .orElse("unknown@example.com");
```

**Optional Best Practices:**
- Return `Optional<T>` from methods that may not find a value
- Never use `Optional` for fields
- Never pass `Optional` as method parameters
- Never return null from `Optional`-returning methods
- Use `Optional.empty()` instead of `Optional.ofNullable(null)`

❌ **Bad Optional Usage:**
```java
// Don't use Optional as field
public class User {
    private Optional<String> middleName; // BAD!
}

// Don't use Optional as parameter
public void setEmail(Optional<String> email) { // BAD!
}

// Don't call get() without checking
Optional<User> userOpt = findUser(id);
User user = userOpt.get(); // May throw NoSuchElementException!
```

✅ **Good Optional Usage:**
```java
// Use null for optional fields (or use proper null handling)
public class User {
    private String middleName; // Can be null

    public Optional<String> getMiddleName() {
        return Optional.ofNullable(middleName);
    }
}

// Use regular parameter with @Nullable annotation
public void setEmail(@Nullable String email) {
    this.email = email;
}

// Always check before get(), or use other methods
Optional<User> userOpt = findUser(id);
if (userOpt.isPresent()) {
    User user = userOpt.get();
    // Use user
}

// Or use orElse/orElseThrow/ifPresent
User user = userOpt.orElseThrow(() -> new NotFoundException());
```

### Prefer Composition Over Inheritance

**Rule:** Favor composition (has-a) over inheritance (is-a) unless there's a true is-a relationship.

❌ **Bad - Inheritance Abuse:**
```java
// Inheritance used just to reuse code (wrong!)
public class Stack extends ArrayList<Object> {
    public void push(Object item) {
        add(item);
    }

    public Object pop() {
        return remove(size() - 1);
    }
}

// Problems:
// 1. Stack exposes all ArrayList methods (add, remove, clear, etc.)
// 2. Stack IS-NOT-A ArrayList semantically
// 3. Breaks encapsulation
```

✅ **Good - Composition:**
```java
public class Stack<T> {
    private final List<T> elements = new ArrayList<>();

    public void push(T item) {
        elements.add(item);
    }

    public T pop() {
        if (elements.isEmpty()) {
            throw new EmptyStackException();
        }
        return elements.remove(elements.size() - 1);
    }

    public T peek() {
        if (elements.isEmpty()) {
            throw new EmptyStackException();
        }
        return elements.get(elements.size() - 1);
    }

    public boolean isEmpty() {
        return elements.isEmpty();
    }

    public int size() {
        return elements.size();
    }
}
```

**When to Use Inheritance:**
- True is-a relationship exists
- Subclass is a specialized version of superclass
- Liskov Substitution Principle holds

**When to Use Composition:**
- Reusing functionality
- Has-a relationship
- Need flexibility to change implementation
- Multiple behaviors needed (can compose many, inherit one)

### Immutability with Final

**Rule:** Make classes and variables immutable when possible. Use `final` extensively.

✅ **Immutable Class:**
```java
public final class Money {
    private final double amount;
    private final String currency;

    public Money(double amount, String currency) {
        if (amount < 0) {
            throw new IllegalArgumentException("Amount cannot be negative");
        }
        this.amount = amount;
        this.currency = currency;
    }

    public double getAmount() {
        return amount;
    }

    public String getCurrency() {
        return currency;
    }

    // Return new instance instead of modifying
    public Money add(Money other) {
        if (!this.currency.equals(other.currency)) {
            throw new IllegalArgumentException("Currency mismatch");
        }
        return new Money(this.amount + other.amount, this.currency);
    }

    public Money multiply(double multiplier) {
        return new Money(this.amount * multiplier, this.currency);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Money)) return false;
        Money money = (Money) o;
        return Double.compare(money.amount, amount) == 0
            && currency.equals(money.currency);
    }

    @Override
    public int hashCode() {
        return Objects.hash(amount, currency);
    }
}
```

**Benefits of Immutability:**
- Thread-safe by default
- Can be safely shared
- Simpler to reason about
- No defensive copying needed
- Safe to use as HashMap keys

✅ **Using Final for Variables:**
```java
public void processOrder(Order order) {
    final double total = order.getTotal();
    final List<OrderItem> items = order.getItems();

    // Compiler prevents reassignment
    // total = 100; // Compilation error
    // items = new ArrayList<>(); // Compilation error

    // Note: final prevents reassignment, not mutation
    items.add(new OrderItem()); // This is allowed!

    // For true immutability, use Collections.unmodifiableList
    final List<OrderItem> immutableItems =
        Collections.unmodifiableList(new ArrayList<>(items));
}
```

### Stream API Usage

**Rule:** Use Stream API for collection operations. It's more readable, functional, and can be parallelized.

❌ **Bad - Imperative Style:**
```java
List<User> activeUsers = new ArrayList<>();
for (User user : users) {
    if (user.isActive()) {
        activeUsers.add(user);
    }
}

List<String> emails = new ArrayList<>();
for (User user : activeUsers) {
    emails.add(user.getEmail());
}

Collections.sort(emails);
```

✅ **Good - Declarative with Streams:**
```java
List<String> emails = users.stream()
    .filter(User::isActive)
    .map(User::getEmail)
    .sorted()
    .collect(Collectors.toList());
```

✅ **Common Stream Patterns:**
```java
// Filtering
List<Order> largeOrders = orders.stream()
    .filter(order -> order.getTotal() > 1000)
    .collect(Collectors.toList());

// Mapping
List<String> customerNames = orders.stream()
    .map(order -> order.getCustomer().getName())
    .collect(Collectors.toList());

// FlatMap (flatten nested collections)
List<OrderItem> allItems = orders.stream()
    .flatMap(order -> order.getItems().stream())
    .collect(Collectors.toList());

// Reduce (sum, average, etc.)
double totalRevenue = orders.stream()
    .mapToDouble(Order::getTotal)
    .sum();

Optional<Order> maxOrder = orders.stream()
    .max(Comparator.comparing(Order::getTotal));

// Grouping
Map<String, List<Order>> ordersByStatus = orders.stream()
    .collect(Collectors.groupingBy(Order::getStatus));

// Partitioning (special case of grouping - boolean)
Map<Boolean, List<Order>> ordersByShipped = orders.stream()
    .collect(Collectors.partitioningBy(Order::isShipped));

// Find first/any
Optional<User> firstAdmin = users.stream()
    .filter(User::isAdmin)
    .findFirst();

// Distinct
List<String> uniqueCities = users.stream()
    .map(User::getCity)
    .distinct()
    .collect(Collectors.toList());

// Limit and skip
List<User> firstTenUsers = users.stream()
    .limit(10)
    .collect(Collectors.toList());

// Combining operations
double averageOrderValueForActiveCustomers = orders.stream()
    .filter(order -> order.getCustomer().isActive())
    .mapToDouble(Order::getTotal)
    .average()
    .orElse(0.0);
```

**Stream Best Practices:**
- Don't reuse streams (create new stream for each pipeline)
- Avoid side effects in stream operations
- Use method references when possible
- Consider parallel streams for large datasets (but measure!)
- Streams are lazy - terminal operation triggers execution

❌ **Bad Stream Usage:**
```java
// Don't modify external state in streams
List<String> results = new ArrayList<>();
users.stream()
    .forEach(user -> results.add(user.getName())); // Side effect!

// Use collect instead
List<String> results = users.stream()
    .map(User::getName)
    .collect(Collectors.toList());

// Don't reuse streams
Stream<User> userStream = users.stream();
long count = userStream.count(); // OK
List<User> list = userStream.collect(Collectors.toList()); // IllegalStateException!
```

### Lambda Expressions

**Rule:** Use lambda expressions for functional interfaces. Prefer method references when applicable.

✅ **Lambda Best Practices:**
```java
// Lambda expression
List<User> sorted = users.stream()
    .sorted((u1, u2) -> u1.getName().compareTo(u2.getName()))
    .collect(Collectors.toList());

// Better: Method reference
List<User> sorted = users.stream()
    .sorted(Comparator.comparing(User::getName))
    .collect(Collectors.toList());

// Lambda with multiple statements
users.forEach(user -> {
    user.setLastLoginTime(LocalDateTime.now());
    user.incrementLoginCount();
    userRepository.save(user);
});

// Custom functional interface
@FunctionalInterface
public interface OrderProcessor {
    void process(Order order);
}

OrderProcessor processor = order -> {
    validateOrder(order);
    calculateTotal(order);
    saveOrder(order);
};
```

### Method References

**Rule:** Use method references instead of lambda expressions when possible. They're more concise.

```java
// Lambda vs Method Reference

// Lambda: user -> user.getName()
// Method reference: User::getName
users.stream().map(User::getName);

// Lambda: user -> System.out.println(user)
// Method reference: System.out::println
users.forEach(System.out::println);

// Lambda: () -> new ArrayList<>()
// Method reference: ArrayList::new
Supplier<List<String>> supplier = ArrayList::new;

// Lambda: str -> str.length()
// Method reference: String::length
strings.stream().map(String::length);
```

**Types of Method References:**
1. Static method: `ClassName::staticMethod`
2. Instance method of particular object: `object::instanceMethod`
3. Instance method of arbitrary object: `ClassName::instanceMethod`
4. Constructor: `ClassName::new`

### Try-With-Resources

**Rule:** Always use try-with-resources for AutoCloseable resources.

❌ **Bad - Manual Resource Management:**
```java
BufferedReader reader = null;
try {
    reader = new BufferedReader(new FileReader("file.txt"));
    String line = reader.readLine();
    // Process line
} catch (IOException e) {
    log.error("Error reading file", e);
} finally {
    if (reader != null) {
        try {
            reader.close();
        } catch (IOException e) {
            log.error("Error closing reader", e);
        }
    }
}
```

✅ **Good - Try-With-Resources:**
```java
try (BufferedReader reader = new BufferedReader(new FileReader("file.txt"))) {
    String line = reader.readLine();
    // Process line
} catch (IOException e) {
    log.error("Error reading file", e);
}
// Reader automatically closed, even if exception occurs

// Multiple resources
try (FileInputStream fis = new FileInputStream("input.txt");
     FileOutputStream fos = new FileOutputStream("output.txt")) {
    // Use streams
} catch (IOException e) {
    log.error("Error processing files", e);
}
// Both streams automatically closed in reverse order
```

### StringBuilder vs String Concatenation

**Rule:** Use `StringBuilder` for multiple string concatenations in loops. Use `+` for simple concatenations.

❌ **Bad - String Concatenation in Loop:**
```java
String result = "";
for (int i = 0; i < 1000; i++) {
    result += i + ","; // Creates 1000 new String objects!
}
```

✅ **Good - StringBuilder:**
```java
StringBuilder builder = new StringBuilder();
for (int i = 0; i < 1000; i++) {
    builder.append(i).append(",");
}
String result = builder.toString();

// Or use String.join for collections
List<String> items = Arrays.asList("apple", "banana", "cherry");
String result = String.join(", ", items);

// Or use Streams
String result = IntStream.range(0, 1000)
    .mapToObj(String::valueOf)
    .collect(Collectors.joining(","));
```

✅ **Simple Concatenation - Use + is Fine:**
```java
// OK for simple cases (compiler optimizes)
String fullName = firstName + " " + lastName;
String message = "Hello, " + name + "!";

// Not OK in loops
for (String item : items) {
    result = result + item; // BAD!
}
```

### Enum Usage

**Rule:** Use enums for fixed sets of constants. Enums can have fields, methods, and constructors.

✅ **Basic Enum:**
```java
public enum OrderStatus {
    PENDING,
    PROCESSING,
    SHIPPED,
    DELIVERED,
    CANCELLED
}

// Usage
Order order = new Order();
order.setStatus(OrderStatus.PENDING);

if (order.getStatus() == OrderStatus.DELIVERED) {
    // Process delivery
}
```

✅ **Enum with Fields and Methods:**
```java
public enum PaymentMethod {
    CREDIT_CARD("Credit Card", 2.9),
    DEBIT_CARD("Debit Card", 1.5),
    PAYPAL("PayPal", 3.5),
    BITCOIN("Bitcoin", 1.0);

    private final String displayName;
    private final double transactionFeePercent;

    PaymentMethod(String displayName, double transactionFeePercent) {
        this.displayName = displayName;
        this.transactionFeePercent = transactionFeePercent;
    }

    public String getDisplayName() {
        return displayName;
    }

    public double calculateFee(double amount) {
        return amount * (transactionFeePercent / 100);
    }

    public double calculateTotal(double amount) {
        return amount + calculateFee(amount);
    }
}

// Usage
PaymentMethod method = PaymentMethod.CREDIT_CARD;
double total = method.calculateTotal(100.0); // 102.90
System.out.println("Paying with: " + method.getDisplayName());
```

✅ **Enum with Abstract Methods (Strategy Pattern):**
```java
public enum Operation {
    PLUS {
        @Override
        public double apply(double x, double y) {
            return x + y;
        }
    },
    MINUS {
        @Override
        public double apply(double x, double y) {
            return x - y;
        }
    },
    MULTIPLY {
        @Override
        public double apply(double x, double y) {
            return x * y;
        }
    },
    DIVIDE {
        @Override
        public double apply(double x, double y) {
            if (y == 0) throw new ArithmeticException("Division by zero");
            return x / y;
        }
    };

    public abstract double apply(double x, double y);
}

// Usage
double result = Operation.PLUS.apply(5, 3); // 8.0
```

---

## Exception Handling

### Checked vs Unchecked Exceptions

**Rule:** Use checked exceptions for recoverable conditions, unchecked for programming errors.

**Checked Exceptions:**
- Extend `Exception` (not `RuntimeException`)
- Must be declared in method signature or caught
- Use for conditions caller can reasonably handle

**Unchecked Exceptions:**
- Extend `RuntimeException`
- Don't need to be declared or caught
- Use for programming errors

✅ **When to Use Each:**
```java
// Checked exception - caller can handle
public User findUserById(Long id) throws UserNotFoundException {
    return userRepository.findById(id)
        .orElseThrow(() -> new UserNotFoundException("User not found: " + id));
}

// Unchecked exception - programming error
public void setAge(int age) {
    if (age < 0) {
        throw new IllegalArgumentException("Age cannot be negative");
    }
    this.age = age;
}

// Checked exception - I/O operation
public String readFile(String path) throws IOException {
    return Files.readString(Paths.get(path));
}

// Unchecked exception - null argument (programming error)
public void processOrder(Order order) {
    Objects.requireNonNull(order, "Order cannot be null");
    // Process order
}
```

### When to Catch vs Throw

**Rule:** Catch exceptions only if you can handle them meaningfully. Otherwise, let them propagate.

❌ **Bad - Catching and Rethrowing:**
```java
public void processData(String data) throws DataProcessingException {
    try {
        // Process data
    } catch (JsonParseException e) {
        throw new DataProcessingException(e); // Unnecessary try-catch
    }
}

// Better: Let it propagate
public void processData(String data) throws JsonParseException {
    // Process data
}
```

✅ **Good - Catch When You Can Handle:**
```java
public void processDataWithRetry(String data) {
    int maxAttempts = 3;
    for (int attempt = 1; attempt <= maxAttempts; attempt++) {
        try {
            processData(data);
            return; // Success
        } catch (TransientException e) {
            if (attempt == maxAttempts) {
                log.error("Failed after {} attempts", maxAttempts, e);
                throw new DataProcessingException("Processing failed", e);
            }
            log.warn("Attempt {} failed, retrying...", attempt);
            sleep(1000 * attempt); // Exponential backoff
        }
    }
}
```

### Custom Exception Design

✅ **Well-Designed Custom Exception:**
```java
public class InsufficientFundsException extends Exception {
    private final double requestedAmount;
    private final double availableBalance;

    public InsufficientFundsException(double requestedAmount, double availableBalance) {
        super(String.format("Insufficient funds: requested %.2f, available %.2f",
            requestedAmount, availableBalance));
        this.requestedAmount = requestedAmount;
        this.availableBalance = availableBalance;
    }

    public double getRequestedAmount() {
        return requestedAmount;
    }

    public double getAvailableBalance() {
        return availableBalance;
    }

    public double getShortfall() {
        return requestedAmount - availableBalance;
    }
}

// Usage
try {
    account.withdraw(500);
} catch (InsufficientFundsException e) {
    log.error("Withdrawal failed: {}", e.getMessage());
    notifyUser(String.format("You need $%.2f more", e.getShortfall()));
}
```

### Logging Exceptions

✅ **Exception Logging Best Practices:**
```java
public void processOrder(Order order) {
    try {
        validateOrder(order);
        saveOrder(order);
        sendConfirmation(order);
    } catch (ValidationException e) {
        // Log with context
        log.error("Order validation failed for order {}: {}",
            order.getId(), e.getMessage(), e);
        throw e;
    } catch (DataAccessException e) {
        // Log with different level based on recoverability
        log.error("Failed to save order {}", order.getId(), e);
        throw new OrderProcessingException("Failed to save order", e);
    } catch (EmailException e) {
        // Non-critical error - log warning
        log.warn("Failed to send confirmation email for order {}",
            order.getId(), e);
        // Don't rethrow - order was saved successfully
    }
}
```

### Never Swallow Exceptions

❌ **Bad - Swallowing Exceptions:**
```java
try {
    riskyOperation();
} catch (Exception e) {
    // Silent failure - NEVER DO THIS!
}

try {
    closeResource();
} catch (Exception e) {
    e.printStackTrace(); // Insufficient - use logging!
}
```

✅ **Good - Proper Exception Handling:**
```java
try {
    riskyOperation();
} catch (Exception e) {
    log.error("Operation failed", e);
    throw new ApplicationException("Failed to perform operation", e);
}

// Or if truly acceptable to ignore
try {
    closeResource();
} catch (IOException e) {
    log.warn("Failed to close resource (non-critical)", e);
    // OK to continue without rethrowing in cleanup scenarios
}
```

---

## Collections and Generics

### Choosing the Right Collection

**Guide to Collection Selection:**

```java
// List - Ordered collection, allows duplicates
// Use ArrayList for random access, LinkedList for frequent insertions/deletions
List<String> names = new ArrayList<>();
List<Task> taskQueue = new LinkedList<>();

// Set - No duplicates, no guaranteed order
// Use HashSet for general use, TreeSet for sorted, LinkedHashSet for insertion order
Set<String> uniqueEmails = new HashSet<>();
Set<Integer> sortedNumbers = new TreeSet<>();
Set<String> insertionOrderSet = new LinkedHashSet<>();

// Map - Key-value pairs, no duplicate keys
// Use HashMap for general use, TreeMap for sorted keys, LinkedHashMap for insertion order
Map<Long, User> userCache = new HashMap<>();
Map<String, Integer> sortedMap = new TreeMap<>();
Map<String, String> orderedMap = new LinkedHashMap<>();

// Queue - FIFO operations
// Use LinkedList or ArrayDeque for general queue
Queue<Task> taskQueue = new LinkedList<>();
Deque<String> deque = new ArrayDeque<>();

// Stack operations - Use Deque instead of Stack class
Deque<String> stack = new ArrayDeque<>();
stack.push("item");
String item = stack.pop();
```

**Performance Characteristics:**
```java
// ArrayList
// - Get by index: O(1)
// - Add at end: O(1) amortized
// - Insert/remove at position: O(n)
// - Search: O(n)

// LinkedList
// - Get by index: O(n)
// - Add/remove at beginning/end: O(1)
// - Insert/remove at position: O(n)
// - Search: O(n)

// HashSet/HashMap
// - Add/remove/contains: O(1) average
// - Iteration: O(capacity + size)

// TreeSet/TreeMap
// - Add/remove/contains: O(log n)
// - Iteration in sorted order: O(n)
```

### Immutable Collections

✅ **Creating Immutable Collections:**
```java
// Java 9+ factory methods (preferred)
List<String> immutableList = List.of("a", "b", "c");
Set<String> immutableSet = Set.of("x", "y", "z");
Map<String, Integer> immutableMap = Map.of(
    "one", 1,
    "two", 2,
    "three", 3
);

// For more than 10 entries in Map
Map<String, Integer> largeMap = Map.ofEntries(
    Map.entry("key1", 1),
    Map.entry("key2", 2),
    Map.entry("key3", 3)
);

// Pre-Java 9 - Collections.unmodifiableXxx
List<String> list = new ArrayList<>();
list.add("a");
list.add("b");
List<String> immutableList = Collections.unmodifiableList(list);

// Guava (if available)
ImmutableList<String> immutableList = ImmutableList.of("a", "b", "c");
ImmutableSet<String> immutableSet = ImmutableSet.of("x", "y", "z");
ImmutableMap<String, Integer> immutableMap = ImmutableMap.of("one", 1, "two", 2);
```

### Generic Type Safety

✅ **Proper Generic Usage:**
```java
// Generic class
public class Box<T> {
    private T content;

    public void set(T content) {
        this.content = content;
    }

    public T get() {
        return content;
    }
}

// Multiple type parameters
public class Pair<K, V> {
    private final K key;
    private final V value;

    public Pair(K key, V value) {
        this.key = key;
        this.value = value;
    }

    public K getKey() { return key; }
    public V getValue() { return value; }
}

// Bounded type parameters
public class NumberBox<T extends Number> {
    private T number;

    public void set(T number) {
        this.number = number;
    }

    public double getDoubleValue() {
        return number.doubleValue(); // Can call Number methods
    }
}

// Generic method
public <T> List<T> createList(T... elements) {
    return Arrays.asList(elements);
}

// Wildcard usage
public void processList(List<? extends Number> numbers) {
    for (Number num : numbers) {
        System.out.println(num.doubleValue());
    }
}

public void addToList(List<? super Integer> list) {
    list.add(42); // Can add Integer
}
```

### Diamond Operator Usage

✅ **Use Diamond Operator (Java 7+):**
```java
// Before Java 7
Map<String, List<String>> map = new HashMap<String, List<String>>();

// Java 7+ with diamond operator
Map<String, List<String>> map = new HashMap<>();

// Works with anonymous classes (Java 9+)
List<String> list = new ArrayList<>() {
    {
        add("item");
    }
};
```

---

## Concurrency

### Thread Safety

**Rule:** Design for thread safety from the start. Assume multi-threaded access unless documented otherwise.

✅ **Thread-Safe Patterns:**
```java
// 1. Immutable objects (inherently thread-safe)
public final class ImmutableUser {
    private final String name;
    private final String email;

    public ImmutableUser(String name, String email) {
        this.name = name;
        this.email = email;
    }

    public String getName() { return name; }
    public String getEmail() { return email; }
}

// 2. Synchronized methods
public class Counter {
    private int count = 0;

    public synchronized void increment() {
        count++;
    }

    public synchronized int getCount() {
        return count;
    }
}

// 3. Concurrent collections
private final Map<String, User> userCache = new ConcurrentHashMap<>();
private final List<String> logMessages = new CopyOnWriteArrayList<>();

// 4. Atomic variables
private final AtomicInteger counter = new AtomicInteger(0);

public void incrementCounter() {
    counter.incrementAndGet();
}

public int getCounter() {
    return counter.get();
}

// 5. ThreadLocal for thread-specific data
private static final ThreadLocal<SimpleDateFormat> dateFormat =
    ThreadLocal.withInitial(() -> new SimpleDateFormat("yyyy-MM-dd"));

public String formatDate(Date date) {
    return dateFormat.get().format(date);
}
```

### ExecutorService Usage

✅ **Using ExecutorService:**
```java
// Fixed thread pool
ExecutorService executor = Executors.newFixedThreadPool(10);

// Submit tasks
for (int i = 0; i < 100; i++) {
    final int taskId = i;
    executor.submit(() -> {
        processTask(taskId);
    });
}

// Shutdown gracefully
executor.shutdown();
try {
    if (!executor.awaitTermination(60, TimeUnit.SECONDS)) {
        executor.shutdownNow();
    }
} catch (InterruptedException e) {
    executor.shutdownNow();
    Thread.currentThread().interrupt();
}

// Try-with-resources (Java 19+)
try (ExecutorService executor = Executors.newFixedThreadPool(10)) {
    // Submit tasks
} // Auto-shutdown

// Custom thread pool for better control
ExecutorService customExecutor = new ThreadPoolExecutor(
    5,  // core pool size
    10, // maximum pool size
    60L, TimeUnit.SECONDS, // keep alive time
    new LinkedBlockingQueue<>(100), // work queue
    new ThreadPoolExecutor.CallerRunsPolicy() // rejection policy
);
```

### CompletableFuture Patterns

✅ **Asynchronous Programming with CompletableFuture:**
```java
// Simple async task
CompletableFuture<String> future = CompletableFuture.supplyAsync(() -> {
    // Long-running task
    return fetchDataFromApi();
});

// Chain operations
CompletableFuture<UserDto> userFuture = CompletableFuture
    .supplyAsync(() -> fetchUserFromDatabase(userId))
    .thenApply(user -> mapToDto(user))
    .thenApply(dto -> enrichWithAdditionalData(dto));

// Combine multiple futures
CompletableFuture<User> userFuture = fetchUserAsync(userId);
CompletableFuture<List<Order>> ordersFuture = fetchOrdersAsync(userId);

CompletableFuture<UserWithOrders> combined = userFuture
    .thenCombine(ordersFuture, (user, orders) ->
        new UserWithOrders(user, orders));

// Handle errors
CompletableFuture<String> result = CompletableFuture
    .supplyAsync(() -> riskyOperation())
    .exceptionally(ex -> {
        log.error("Operation failed", ex);
        return "default value";
    });

// Multiple async operations
List<CompletableFuture<String>> futures = ids.stream()
    .map(id -> CompletableFuture.supplyAsync(() -> fetchData(id)))
    .collect(Collectors.toList());

// Wait for all to complete
CompletableFuture<Void> allOf = CompletableFuture.allOf(
    futures.toArray(new CompletableFuture[0]));

allOf.thenRun(() -> {
    List<String> results = futures.stream()
        .map(CompletableFuture::join)
        .collect(Collectors.toList());
    processResults(results);
});
```

### Avoiding Deadlocks

✅ **Deadlock Prevention:**
```java
// 1. Always acquire locks in the same order
public class BankAccount {
    private final Object lock = new Object();
    private double balance;

    public static void transfer(BankAccount from, BankAccount to, double amount) {
        // Always lock accounts in consistent order (by hashCode)
        BankAccount first = from.hashCode() < to.hashCode() ? from : to;
        BankAccount second = from.hashCode() < to.hashCode() ? to : from;

        synchronized (first.lock) {
            synchronized (second.lock) {
                if (from == first) {
                    from.withdraw(amount);
                    to.deposit(amount);
                } else {
                    from.deposit(amount);
                    to.withdraw(amount);
                }
            }
        }
    }
}

// 2. Use tryLock with timeout
Lock lock1 = new ReentrantLock();
Lock lock2 = new ReentrantLock();

try {
    if (lock1.tryLock(1, TimeUnit.SECONDS)) {
        try {
            if (lock2.tryLock(1, TimeUnit.SECONDS)) {
                try {
                    // Critical section
                } finally {
                    lock2.unlock();
                }
            }
        } finally {
            lock1.unlock();
        }
    }
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();
}

// 3. Use higher-level concurrency utilities
ConcurrentHashMap<String, Account> accounts = new ConcurrentHashMap<>();
accounts.compute("account1", (key, account) -> {
    account.withdraw(100);
    return account;
});
```

### Atomic Classes

✅ **Using Atomic Classes:**
```java
public class Statistics {
    private final AtomicLong totalRequests = new AtomicLong(0);
    private final AtomicLong successfulRequests = new AtomicLong(0);
    private final AtomicLong failedRequests = new AtomicLong(0);

    public void recordSuccess() {
        totalRequests.incrementAndGet();
        successfulRequests.incrementAndGet();
    }

    public void recordFailure() {
        totalRequests.incrementAndGet();
        failedRequests.incrementAndGet();
    }

    public double getSuccessRate() {
        long total = totalRequests.get();
        if (total == 0) return 0.0;
        return (double) successfulRequests.get() / total;
    }

    // Atomic update with compareAndSet
    private final AtomicReference<Config> config =
        new AtomicReference<>(new Config());

    public void updateConfig(Config newConfig) {
        Config current;
        do {
            current = config.get();
        } while (!config.compareAndSet(current, newConfig));
    }
}
```

---

## Testing (TDD)

### Unit Testing with JUnit 5

✅ **JUnit 5 Best Practices:**
```java
@DisplayName("User Service Tests")
class UserServiceTest {

    private UserService userService;
    private UserRepository userRepository;
    private PasswordEncoder passwordEncoder;

    @BeforeEach
    void setUp() {
        userRepository = mock(UserRepository.class);
        passwordEncoder = mock(PasswordEncoder.class);
        userService = new UserService(userRepository, passwordEncoder);
    }

    @Test
    @DisplayName("Should create user with valid data")
    void shouldCreateUserWithValidData() {
        // Arrange
        String email = "test@example.com";
        String password = "SecurePass123!";
        String encodedPassword = "encoded_password";

        when(passwordEncoder.encode(password)).thenReturn(encodedPassword);
        when(userRepository.existsByEmail(email)).thenReturn(false);

        // Act
        User user = userService.createUser(email, password);

        // Assert
        assertNotNull(user);
        assertEquals(email, user.getEmail());
        assertEquals(encodedPassword, user.getPasswordHash());
        verify(userRepository).save(any(User.class));
    }

    @Test
    @DisplayName("Should throw exception when email already exists")
    void shouldThrowExceptionWhenEmailExists() {
        // Arrange
        String email = "existing@example.com";
        when(userRepository.existsByEmail(email)).thenReturn(true);

        // Act & Assert
        assertThrows(DuplicateEmailException.class, () ->
            userService.createUser(email, "password"));

        verify(userRepository, never()).save(any());
    }

    @ParameterizedTest
    @ValueSource(strings = {"", "  ", "invalid-email", "@example.com"})
    @DisplayName("Should throw exception for invalid email formats")
    void shouldThrowExceptionForInvalidEmail(String invalidEmail) {
        assertThrows(ValidationException.class, () ->
            userService.createUser(invalidEmail, "password"));
    }

    @ParameterizedTest
    @CsvSource({
        "test@example.com, short, 'Password too short'",
        "test@example.com, nodigits, 'Password must contain digits'",
        "invalid, ValidPass123!, 'Invalid email format'"
    })
    @DisplayName("Should validate user input correctly")
    void shouldValidateUserInput(String email, String password, String expectedError) {
        ValidationException exception = assertThrows(ValidationException.class, () ->
            userService.createUser(email, password));

        assertTrue(exception.getMessage().contains(expectedError));
    }

    @Test
    @DisplayName("Should handle repository exception gracefully")
    void shouldHandleRepositoryException() {
        // Arrange
        when(userRepository.save(any())).thenThrow(new DataAccessException("DB error"));

        // Act & Assert
        assertThrows(UserCreationException.class, () ->
            userService.createUser("test@example.com", "password"));
    }

    @Nested
    @DisplayName("User Authentication Tests")
    class UserAuthenticationTests {

        @Test
        @DisplayName("Should authenticate user with correct password")
        void shouldAuthenticateWithCorrectPassword() {
            // Arrange
            User user = new User("test@example.com", "encoded_pass");
            when(userRepository.findByEmail("test@example.com"))
                .thenReturn(Optional.of(user));
            when(passwordEncoder.matches("password", "encoded_pass"))
                .thenReturn(true);

            // Act
            boolean authenticated = userService.authenticate("test@example.com", "password");

            // Assert
            assertTrue(authenticated);
        }

        @Test
        @DisplayName("Should reject authentication with wrong password")
        void shouldRejectWithWrongPassword() {
            // Arrange
            User user = new User("test@example.com", "encoded_pass");
            when(userRepository.findByEmail("test@example.com"))
                .thenReturn(Optional.of(user));
            when(passwordEncoder.matches("wrong", "encoded_pass"))
                .thenReturn(false);

            // Act
            boolean authenticated = userService.authenticate("test@example.com", "wrong");

            // Assert
            assertFalse(authenticated);
        }
    }
}
```

### Mocking with Mockito

✅ **Mockito Best Practices:**
```java
public class OrderServiceTest {

    @Mock
    private OrderRepository orderRepository;

    @Mock
    private PaymentService paymentService;

    @Mock
    private EmailService emailService;

    @InjectMocks
    private OrderService orderService;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    void shouldProcessOrderSuccessfully() {
        // Arrange
        Order order = new Order();
        order.setId(1L);
        order.setTotal(100.0);

        when(paymentService.charge(any(), anyDouble())).thenReturn(true);
        when(orderRepository.save(any(Order.class))).thenReturn(order);

        // Act
        orderService.processOrder(order);

        // Assert
        verify(paymentService).charge(order, 100.0);
        verify(orderRepository).save(order);
        verify(emailService).sendConfirmation(order);

        assertEquals(OrderStatus.COMPLETED, order.getStatus());
    }

    @Test
    void shouldHandlePaymentFailure() {
        // Arrange
        Order order = new Order();
        when(paymentService.charge(any(), anyDouble())).thenReturn(false);

        // Act & Assert
        assertThrows(PaymentFailedException.class, () ->
            orderService.processOrder(order));

        verify(emailService, never()).sendConfirmation(any());
        assertEquals(OrderStatus.PAYMENT_FAILED, order.getStatus());
    }

    @Test
    void shouldRetryOnTransientFailure() {
        // Arrange
        Order order = new Order();

        // First two calls fail, third succeeds
        when(paymentService.charge(any(), anyDouble()))
            .thenThrow(new TransientException())
            .thenThrow(new TransientException())
            .thenReturn(true);

        // Act
        orderService.processOrderWithRetry(order);

        // Assert
        verify(paymentService, times(3)).charge(any(), anyDouble());
    }

    @Test
    void shouldCaptureArgumentValues() {
        // Arrange
        ArgumentCaptor<Order> orderCaptor = ArgumentCaptor.forClass(Order.class);
        Order order = new Order();
        order.setTotal(100.0);

        // Act
        orderService.processOrder(order);

        // Assert
        verify(orderRepository).save(orderCaptor.capture());
        Order savedOrder = orderCaptor.getValue();
        assertEquals(OrderStatus.COMPLETED, savedOrder.getStatus());
        assertNotNull(savedOrder.getProcessedAt());
    }
}
```

### Test Organization

**Package Structure:**
```
src/
├── main/
│   └── java/
│       └── com/example/
│           ├── model/
│           │   └── User.java
│           └── service/
│               └── UserService.java
└── test/
    └── java/
        └── com/example/
            ├── model/
            │   └── UserTest.java
            └── service/
                └── UserServiceTest.java
```

### AAA Pattern (Arrange-Act-Assert)

✅ **Clear Test Structure:**
```java
@Test
void shouldCalculateDiscountCorrectly() {
    // Arrange - Set up test data and expectations
    Product product = new Product("Laptop", 1000.0);
    Discount discount = new Discount(10); // 10%
    PriceCalculator calculator = new PriceCalculator();

    // Act - Execute the behavior being tested
    double finalPrice = calculator.calculateFinalPrice(product, discount);

    // Assert - Verify the expected outcome
    assertEquals(900.0, finalPrice, 0.01);
}
```

### Testing Private Methods

**Rule:** Don't test private methods directly. Test them through public methods.

❌ **Bad:**
```java
@Test
void testPrivateMethod() {
    // Using reflection to test private method - BAD!
    Method method = UserService.class.getDeclaredMethod("validateEmail", String.class);
    method.setAccessible(true);
    boolean result = (boolean) method.invoke(userService, "test@example.com");
    assertTrue(result);
}
```

✅ **Good:**
```java
@Test
void shouldRejectInvalidEmailDuringUserCreation() {
    // Test private validateEmail() through public createUser()
    assertThrows(ValidationException.class, () ->
        userService.createUser("invalid-email", "password"));
}
```

### Test Coverage Goals

**Recommended Coverage Targets:**
- **Critical business logic**: 100%
- **Service layer**: 90-100%
- **Controller layer**: 80-90%
- **Utility classes**: 90-100%
- **Overall project**: 80% minimum

**Tools:**
- JaCoCo for coverage reporting
- SonarQube for code quality analysis

```xml
<!-- Maven JaCoCo Plugin -->
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <version>0.8.10</version>
    <executions>
        <execution>
            <goals>
                <goal>prepare-agent</goal>
            </goals>
        </execution>
        <execution>
            <id>report</id>
            <phase>test</phase>
            <goals>
                <goal>report</goal>
            </goals>
        </execution>
        <execution>
            <id>coverage-check</id>
            <goals>
                <goal>check</goal>
            </goals>
            <configuration>
                <rules>
                    <rule>
                        <element>PACKAGE</element>
                        <limits>
                            <limit>
                                <counter>LINE</counter>
                                <value>COVEREDRATIO</value>
                                <minimum>0.80</minimum>
                            </limit>
                        </limits>
                    </rule>
                </rules>
            </configuration>
        </execution>
    </executions>
</plugin>
```

---

## Code Organization

### Package Structure

✅ **Layered Architecture:**
```
com.example.myapp/
├── controller/          # REST controllers
│   ├── UserController.java
│   └── OrderController.java
├── service/            # Business logic
│   ├── UserService.java
│   └── OrderService.java
├── repository/         # Data access
│   ├── UserRepository.java
│   └── OrderRepository.java
├── model/             # Domain models
│   ├── User.java
│   └── Order.java
├── dto/               # Data transfer objects
│   ├── UserDto.java
│   └── OrderDto.java
├── exception/         # Custom exceptions
│   ├── UserNotFoundException.java
│   └── ValidationException.java
├── config/           # Configuration classes
│   ├── SecurityConfig.java
│   └── DatabaseConfig.java
└── util/            # Utility classes
    ├── DateUtils.java
    └── StringUtils.java
```

✅ **Feature-Based Structure (for larger apps):**
```
com.example.myapp/
├── user/
│   ├── User.java
│   ├── UserController.java
│   ├── UserService.java
│   ├── UserRepository.java
│   └── UserDto.java
├── order/
│   ├── Order.java
│   ├── OrderController.java
│   ├── OrderService.java
│   ├── OrderRepository.java
│   └── OrderDto.java
└── common/
    ├── exception/
    ├── config/
    └── util/
```

### Class Naming Conventions

```java
// Controllers: Noun + Controller
public class UserController { }
public class OrderController { }

// Services: Noun + Service
public class UserService { }
public class PaymentService { }

// Repositories: Noun + Repository
public class UserRepository { }
public class OrderRepository { }

// DTOs: Noun + Dto
public class UserDto { }
public class CreateOrderDto { }

// Exceptions: Description + Exception
public class UserNotFoundException extends RuntimeException { }
public class InvalidEmailException extends ValidationException { }

// Utilities: Plural noun + Utils
public class StringUtils { }
public class DateUtils { }

// Interfaces: Adjective or Noun
public interface Serializable { }
public interface PaymentProcessor { }
```

### Method Naming Conventions

```java
// Getters/Setters
public String getName() { }
public void setName(String name) { }

// Boolean getters: is/has/can
public boolean isActive() { }
public boolean hasPermission() { }
public boolean canExecute() { }

// Actions: verb + noun
public void createUser() { }
public void processPayment() { }
public void calculateTotal() { }

// Queries: get/find/search + noun
public User getUser(Long id) { }
public List<User> findActiveUsers() { }
public List<Order> searchByDate(LocalDate date) { }

// Validators: validate + noun
public void validateEmail(String email) { }
public boolean isValidPassword(String password) { }
```

### Constants and Configuration

✅ **Constants:**
```java
public class ApplicationConstants {
    // Public constants: public static final
    public static final int MAX_RETRY_ATTEMPTS = 3;
    public static final String DEFAULT_ENCODING = "UTF-8";
    public static final Duration CONNECTION_TIMEOUT = Duration.ofSeconds(30);

    // Private constructor to prevent instantiation
    private ApplicationConstants() {
        throw new AssertionError("Cannot instantiate constants class");
    }
}

// Or use enums for related constants
public enum HttpStatus {
    OK(200, "OK"),
    NOT_FOUND(404, "Not Found"),
    INTERNAL_SERVER_ERROR(500, "Internal Server Error");

    private final int code;
    private final String message;

    HttpStatus(int code, String message) {
        this.code = code;
        this.message = message;
    }

    public int getCode() { return code; }
    public String getMessage() { return message; }
}
```

### Builder Pattern

✅ **Builder for Complex Objects:**
```java
public class User {
    private final String email;
    private final String firstName;
    private final String lastName;
    private final LocalDate dateOfBirth;
    private final String phoneNumber;
    private final Address address;

    private User(Builder builder) {
        this.email = builder.email;
        this.firstName = builder.firstName;
        this.lastName = builder.lastName;
        this.dateOfBirth = builder.dateOfBirth;
        this.phoneNumber = builder.phoneNumber;
        this.address = builder.address;
    }

    public static Builder builder() {
        return new Builder();
    }

    public static class Builder {
        private String email;
        private String firstName;
        private String lastName;
        private LocalDate dateOfBirth;
        private String phoneNumber;
        private Address address;

        public Builder email(String email) {
            this.email = email;
            return this;
        }

        public Builder firstName(String firstName) {
            this.firstName = firstName;
            return this;
        }

        public Builder lastName(String lastName) {
            this.lastName = lastName;
            return this;
        }

        public Builder dateOfBirth(LocalDate dateOfBirth) {
            this.dateOfBirth = dateOfBirth;
            return this;
        }

        public Builder phoneNumber(String phoneNumber) {
            this.phoneNumber = phoneNumber;
            return this;
        }

        public Builder address(Address address) {
            this.address = address;
            return this;
        }

        public User build() {
            validateRequired();
            return new User(this);
        }

        private void validateRequired() {
            if (email == null) throw new IllegalStateException("Email is required");
            if (firstName == null) throw new IllegalStateException("First name is required");
        }
    }

    // Getters
    public String getEmail() { return email; }
    public String getFirstName() { return firstName; }
    public String getLastName() { return lastName; }
    public LocalDate getDateOfBirth() { return dateOfBirth; }
    public String getPhoneNumber() { return phoneNumber; }
    public Address getAddress() { return address; }
}

// Usage
User user = User.builder()
    .email("john@example.com")
    .firstName("John")
    .lastName("Doe")
    .dateOfBirth(LocalDate.of(1990, 1, 1))
    .phoneNumber("555-1234")
    .build();
```

### Factory Pattern

✅ **Factory for Object Creation:**
```java
public interface PaymentProcessor {
    void processPayment(double amount);
}

public class CreditCardProcessor implements PaymentProcessor {
    @Override
    public void processPayment(double amount) {
        System.out.println("Processing credit card payment: $" + amount);
    }
}

public class PayPalProcessor implements PaymentProcessor {
    @Override
    public void processPayment(double amount) {
        System.out.println("Processing PayPal payment: $" + amount);
    }
}

public class PaymentProcessorFactory {
    public static PaymentProcessor create(PaymentMethod method) {
        switch (method) {
            case CREDIT_CARD:
                return new CreditCardProcessor();
            case PAYPAL:
                return new PayPalProcessor();
            case BITCOIN:
                return new BitcoinProcessor();
            default:
                throw new IllegalArgumentException("Unknown payment method: " + method);
        }
    }
}

// Usage
PaymentProcessor processor = PaymentProcessorFactory.create(PaymentMethod.CREDIT_CARD);
processor.processPayment(100.0);
```

---

## Performance

### String Optimization

✅ **String Performance Tips:**
```java
// Use String.format() sparingly (it's slow)
// OK for occasional use
String message = String.format("User %s logged in at %s", username, timestamp);

// For frequent formatting, use StringBuilder
StringBuilder builder = new StringBuilder();
for (int i = 0; i < 1000; i++) {
    builder.append("Item ").append(i).append("\n");
}
String result = builder.toString();

// Use String.join() for collections
List<String> items = Arrays.asList("apple", "banana", "cherry");
String joined = String.join(", ", items);

// Avoid string concatenation in loops
String result = "";
for (String item : items) {
    result += item; // BAD - creates many String objects
}

// Use StringBuilder instead
StringBuilder result = new StringBuilder();
for (String item : items) {
    result.append(item);
}

// String interning for frequently used strings
String s1 = new String("hello").intern();
String s2 = "hello";
assert s1 == s2; // Same reference
```

### Collection Performance

```java
// ArrayList vs LinkedList
List<String> arrayList = new ArrayList<>(); // Fast random access O(1)
List<String> linkedList = new LinkedList<>(); // Fast insertion/deletion at ends O(1)

// HashSet vs TreeSet
Set<String> hashSet = new HashSet<>(); // O(1) add/contains, no order
Set<String> treeSet = new TreeSet<>(); // O(log n) add/contains, sorted

// HashMap vs TreeMap vs LinkedHashMap
Map<String, Integer> hashMap = new HashMap<>(); // O(1) get/put, no order
Map<String, Integer> treeMap = new TreeMap<>(); // O(log n) get/put, sorted by key
Map<String, Integer> linkedHashMap = new LinkedHashMap<>(); // O(1) get/put, insertion order

// Pre-size collections when size is known
List<String> list = new ArrayList<>(1000); // Avoids resizing
Map<String, String> map = new HashMap<>(1000);

// Use EnumSet for enum values
Set<DayOfWeek> weekdays = EnumSet.of(
    DayOfWeek.MONDAY, DayOfWeek.TUESDAY, DayOfWeek.WEDNESDAY,
    DayOfWeek.THURSDAY, DayOfWeek.FRIDAY
);
```

### Stream vs Loop Performance

**Rule:** Streams are readable but may have overhead for small collections. Measure performance for critical paths.

```java
// For small collections (<100 items), loops may be faster
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);

// Loop (slightly faster for small collections)
int sum = 0;
for (int num : numbers) {
    sum += num;
}

// Stream (more readable, negligible overhead)
int sum = numbers.stream()
    .mapToInt(Integer::intValue)
    .sum();

// For large collections or parallel processing, streams shine
List<Integer> largeList = IntStream.range(0, 1_000_000)
    .boxed()
    .collect(Collectors.toList());

// Parallel stream for CPU-intensive operations
int sum = largeList.parallelStream()
    .mapToInt(Integer::intValue)
    .sum();
```

### Memory Management

✅ **Memory Best Practices:**
```java
// Close resources to free memory
try (FileInputStream fis = new FileInputStream("file.txt");
     BufferedInputStream bis = new BufferedInputStream(fis)) {
    // Use streams
} // Automatically closed

// Avoid memory leaks with listeners
public class EventSource {
    private final List<EventListener> listeners = new ArrayList<>();

    public void addListener(EventListener listener) {
        listeners.add(listener);
    }

    public void removeListener(EventListener listener) {
        listeners.remove(listener); // Important: allow garbage collection
    }
}

// Use weak references for caches
Map<String, WeakReference<User>> cache = new WeakHashMap<>();

// Clear collections when done
List<LargeObject> objects = new ArrayList<>();
// ... use objects
objects.clear(); // Allow garbage collection

// Avoid string concatenation creating many objects
String result = "Hello" + " " + "World"; // OK - compiler optimizes
String result = str1 + str2 + str3; // OK - compiler uses StringBuilder

// Not OK in loops - use StringBuilder explicitly
for (String item : items) {
    result = result + item; // Creates new String each iteration
}
```

---

## Common Anti-Patterns

### God Objects

❌ **Anti-Pattern - God Object:**
```java
// One class doing everything - AVOID!
public class OrderManager {
    // User management
    public void createUser() { }
    public void deleteUser() { }

    // Order processing
    public void createOrder() { }
    public void processOrder() { }

    // Payment processing
    public void processPayment() { }

    // Email sending
    public void sendConfirmation() { }

    // Reporting
    public void generateReport() { }

    // Database operations
    public void saveToDatabase() { }

    // Logging
    public void logActivity() { }

    // 50+ more methods...
}
```

✅ **Solution - Single Responsibility:**
```java
public class UserService {
    public void createUser() { }
    public void deleteUser() { }
}

public class OrderService {
    public void createOrder() { }
    public void processOrder() { }
}

public class PaymentService {
    public void processPayment() { }
}

public class EmailService {
    public void sendConfirmation() { }
}
```

### Primitive Obsession

❌ **Anti-Pattern - Primitive Obsession:**
```java
public class Order {
    private double price; // What currency?
    private double weight; // What unit?
    private String phoneNumber; // No validation!
    private String email; // No validation!
}
```

✅ **Solution - Value Objects:**
```java
public class Money {
    private final double amount;
    private final Currency currency;

    public Money(double amount, Currency currency) {
        this.amount = amount;
        this.currency = currency;
    }
    // Methods for money operations
}

public class Weight {
    private final double value;
    private final WeightUnit unit;

    public Weight(double value, WeightUnit unit) {
        this.value = value;
        this.unit = unit;
    }
}

public class Email {
    private final String value;

    public Email(String value) {
        if (!isValid(value)) {
            throw new IllegalArgumentException("Invalid email");
        }
        this.value = value;
    }

    private boolean isValid(String email) {
        return email.contains("@"); // Simplified
    }
}

public class Order {
    private Money price;
    private Weight weight;
    private Email customerEmail;
}
```

### Long Parameter Lists

❌ **Anti-Pattern - Long Parameter Lists:**
```java
public void createUser(
    String firstName,
    String lastName,
    String email,
    String phoneNumber,
    String addressLine1,
    String addressLine2,
    String city,
    String state,
    String zipCode,
    String country
) {
    // Too many parameters!
}
```

✅ **Solution - Parameter Object:**
```java
public class UserRegistration {
    private final String firstName;
    private final String lastName;
    private final String email;
    private final String phoneNumber;
    private final Address address;

    // Constructor, getters, builder
}

public class Address {
    private final String line1;
    private final String line2;
    private final String city;
    private final String state;
    private final String zipCode;
    private final String country;

    // Constructor, getters, builder
}

public void createUser(UserRegistration registration) {
    // Clean method signature
}
```

### Magic Numbers

❌ **Anti-Pattern - Magic Numbers:**
```java
public void processOrder(Order order) {
    if (order.getTotal() > 100) { // What is 100?
        applyDiscount(order, 0.1); // What is 0.1?
    }

    if (order.getItems().size() > 5) { // What is 5?
        // Free shipping
    }
}
```

✅ **Solution - Named Constants:**
```java
private static final double FREE_SHIPPING_THRESHOLD = 100.0;
private static final double BULK_DISCOUNT_RATE = 0.1;
private static final int BULK_ORDER_ITEM_COUNT = 5;

public void processOrder(Order order) {
    if (order.getTotal() > FREE_SHIPPING_THRESHOLD) {
        applyDiscount(order, BULK_DISCOUNT_RATE);
    }

    if (order.getItems().size() > BULK_ORDER_ITEM_COUNT) {
        // Free shipping
    }
}
```

### Nested Conditionals

❌ **Anti-Pattern - Deeply Nested Conditionals:**
```java
public void processPayment(Order order) {
    if (order != null) {
        if (order.getCustomer() != null) {
            if (order.getCustomer().hasPaymentMethod()) {
                if (order.getTotal() > 0) {
                    if (inventory.isAvailable(order)) {
                        // Process payment
                    } else {
                        throw new InsufficientInventoryException();
                    }
                } else {
                    throw new InvalidAmountException();
                }
            } else {
                throw new NoPaymentMethodException();
            }
        } else {
            throw new NoCustomerException();
        }
    } else {
        throw new NullOrderException();
    }
}
```

✅ **Solution - Guard Clauses:**
```java
public void processPayment(Order order) {
    // Guard clauses - fail fast
    if (order == null) {
        throw new NullOrderException();
    }
    if (order.getCustomer() == null) {
        throw new NoCustomerException();
    }
    if (!order.getCustomer().hasPaymentMethod()) {
        throw new NoPaymentMethodException();
    }
    if (order.getTotal() <= 0) {
        throw new InvalidAmountException();
    }
    if (!inventory.isAvailable(order)) {
        throw new InsufficientInventoryException();
    }

    // Happy path at the end
    processPaymentInternal(order);
}
```

### Returning Null

❌ **Anti-Pattern - Returning Null:**
```java
public User findUser(Long id) {
    // May return null
    return database.find(id);
}

// Caller must remember null check
User user = findUser(123L);
if (user != null) {
    String email = user.getEmail(); // NullPointerException risk
}
```

✅ **Solution - Return Optional:**
```java
public Optional<User> findUser(Long id) {
    return Optional.ofNullable(database.find(id));
}

// Caller forced to handle absence
Optional<User> userOpt = findUser(123L);
String email = userOpt
    .map(User::getEmail)
    .orElse("unknown@example.com");
```

### Not Closing Resources

❌ **Anti-Pattern - Resource Leaks:**
```java
public String readFile(String path) {
    FileReader reader = new FileReader(path);
    BufferedReader br = new BufferedReader(reader);
    return br.readLine(); // Resources never closed!
}
```

✅ **Solution - Try-With-Resources:**
```java
public String readFile(String path) throws IOException {
    try (BufferedReader reader = new BufferedReader(new FileReader(path))) {
        return reader.readLine();
    } // Automatically closed
}
```

---

## Checklist

Use this checklist during code reviews to verify Java code quality:

### SOLID Principles
- [ ] Each class has a single, well-defined responsibility
- [ ] Classes are open for extension, closed for modification
- [ ] Subclasses can be substituted for base classes
- [ ] Interfaces are small and focused
- [ ] Dependencies are inverted (depend on abstractions)

### DRY Principle
- [ ] No obvious code duplication
- [ ] Common logic extracted to utility methods/classes
- [ ] Generics used where appropriate

### Clean Code
- [ ] Class, method, and variable names are meaningful
- [ ] Methods are small (5-20 lines ideally)
- [ ] Comments explain WHY, not WHAT
- [ ] Proper exception handling (no swallowed exceptions)
- [ ] Code is properly organized

### Java-Specific
- [ ] Optional used instead of null for absent values
- [ ] Composition preferred over inheritance
- [ ] Immutability used where appropriate (final fields/classes)
- [ ] Stream API used for collection operations
- [ ] Lambda expressions and method references used
- [ ] Try-with-resources used for AutoCloseable resources
- [ ] StringBuilder used for string concatenation in loops
- [ ] Enums used for fixed sets of constants

### Exception Handling
- [ ] Appropriate exception types (checked vs unchecked)
- [ ] Exceptions are caught only when they can be handled
- [ ] Custom exceptions are well-designed
- [ ] Exceptions are logged with context
- [ ] No empty catch blocks

### Collections
- [ ] Appropriate collection type chosen
- [ ] Immutable collections used where appropriate
- [ ] Generic type parameters specified
- [ ] Diamond operator used (Java 7+)

### Concurrency
- [ ] Thread safety considered
- [ ] Appropriate synchronization mechanisms used
- [ ] ExecutorService used for thread pools
- [ ] CompletableFuture used for async operations
- [ ] Deadlock prevention considered
- [ ] Atomic classes used for simple atomic operations

### Testing
- [ ] Unit tests exist for business logic
- [ ] Tests follow AAA pattern
- [ ] Mocking used appropriately
- [ ] Tests are isolated and independent
- [ ] Test coverage meets standards (80%+)

### Code Organization
- [ ] Proper package structure
- [ ] Naming conventions followed
- [ ] Constants properly defined
- [ ] Builder/Factory patterns used appropriately

### Performance
- [ ] String operations optimized
- [ ] Appropriate collection types for use case
- [ ] Resources properly managed
- [ ] No obvious performance issues

### Anti-Patterns
- [ ] No God objects
- [ ] No primitive obsession
- [ ] No long parameter lists
- [ ] No magic numbers
- [ ] No deeply nested conditionals
- [ ] No null returns where Optional is appropriate
- [ ] No resource leaks

---

## Related Skills

- **uncle-duke-java**: Java code review agent that uses this skill as reference

---

## References

### Java Documentation
- [Java SE Documentation](https://docs.oracle.com/en/java/javase/)
- [Java Language Specification](https://docs.oracle.com/javase/specs/)
- [Java API Documentation](https://docs.oracle.com/en/java/javase/17/docs/api/)

### Spring Framework
- [Spring Framework Documentation](https://spring.io/projects/spring-framework)
- [Spring Boot Documentation](https://spring.io/projects/spring-boot)
- [Spring Data JPA](https://spring.io/projects/spring-data-jpa)

### Best Practices
- [Effective Java (Joshua Bloch)](https://www.oreilly.com/library/view/effective-java/9780134686097/)
- [Clean Code (Robert C. Martin)](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
- [Java Design Patterns](https://refactoring.guru/design-patterns/java)

### Testing
- [JUnit 5 User Guide](https://junit.org/junit5/docs/current/user-guide/)
- [Mockito Documentation](https://javadoc.io/doc/org.mockito/mockito-core/latest/org/mockito/Mockito.html)

### Tools
- [Maven Documentation](https://maven.apache.org/guides/)
- [Gradle Documentation](https://docs.gradle.org/)
- [SonarQube](https://www.sonarqube.org/)

---

**Version:** 1.0
**Last Updated:** 2025-12-24
**Maintainer:** Development Team
