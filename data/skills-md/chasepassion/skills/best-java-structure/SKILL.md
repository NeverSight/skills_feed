---
name: best-java-structure
description: Java Layered Architecture Design Pattern — A complete implementation guide for the classic five-layer architecture using Spring Boot + MyBatis-Plus. Suitable for bootstrapping new Java projects, refactoring existing architectures, establishing team development standards,and database migration scenarios.
---

# Java Layered Architecture Design Pattern (Spring Boot + MyBatis-Plus)
A practical guide to implementing a classic five-layer architecture with Spring Boot and MyBatis-Plus.

## When to Apply
Use this skill in the following scenarios:
- Creating a new Java Web project
- Refactoring an existing project architecture
- Designing a multi-module Java system
- Checking architectural compliance during code reviews
- Defining architectural standards for team development
- Database migration or technology stack migration

## Assumptions
- Spring Boot 3.x
- MyBatis-Plus for data access
- DTO/VO separation at API boundaries

## Quick Reference
| Priority | Category                  | Impact Area              | Prefix            |
| -------: | ------------------------- | ------------------------ | ----------------- |
|        1 | Separation of Concerns    | Architectural clarity    | -principle-       |
|        2 | Unidirectional Dependency | Dependency management    | -dependency-      |
|        3 | Interface Abstraction     | Replaceability           | -abstraction-     |
|        4 | Data Transfer             | API consistency          | -data-            |
|        5 | Exception Handling        | Error handling           | -exception-       |
|        6 | Cross-Layer Invocation    | Architectural compliance | -crosslayer-      |
|        7 | Reverse Dependency        | Architectural compliance | -reverse-         |
|        8 | Entity Exposure           | Security                 | -entity-exposure- |

## Core Principles
### 1. Separation of Concerns (SoC)
Each layer should solve one category of problems and must not take on responsibilities belonging to other layers.
```java
// Correct: clear responsibilities per layer
// Presentation layer: HTTP handling only
@RestController
public class ProjectController {
    private final ProjectService projectService;
    public ProjectController(ProjectService projectService) {
        this.projectService = projectService;
    }
    @GetMapping("/{id}")
    public ApiReturn<ProjectVo> getProject(@PathVariable Long id) {
        Project project = projectService.getProject(id);
        ProjectVo vo = new ProjectVo();
        BeanUtils.copyProperties(project, vo);
        return ApiReturn.of(vo);
    }
}
// Business logic layer: business rules only
@Service
public class ProjectService {
    private final ProjectMapper projectMapper;
    public ProjectService(ProjectMapper projectMapper) {
        this.projectMapper = projectMapper;
    }
    public Project getProject(Long id) {
        Project project = projectMapper.selectById(id);
        if (project == null) {
            throw new BusinessException(404, "Project does not exist");
        }
        return project;
    }
}
// Data access layer: data interfaces only
public interface ProjectMapper extends BaseMapper<Project> {
}
```

### 2. Unidirectional Dependency
Upper layers may call lower layers, but lower layers must not depend on upper layers.
```java
// Correct: depend on a lower layer abstraction
@Service
public class ProjectService {
    private final ProjectMapper projectMapper;
    public ProjectService(ProjectMapper projectMapper) {
        this.projectMapper = projectMapper;
    }
}
// Incorrect: cross-layer invocation
@RestController
public class ProjectController {
    private final ProjectMapper projectMapper;
    public ProjectController(ProjectMapper projectMapper) {
        this.projectMapper = projectMapper;
    }
}
```

### 3. Interface Abstraction
Layers should interact via interfaces, not concrete implementations.
```java
// Correct: mapper interface managed by MyBatis-Plus
public interface ProjectMapper extends BaseMapper<Project> {
}
// Incorrect: depending on a non-existent implementation class
public class ProjectService {
    private ProjectMapperImpl projectMapperImpl;
}
```

## Architecture Layers
### Classic Five-Layer Architecture
```
Presentation Layer → Business Logic Layer → Data Access Layer → Persistence Layer → Database Layer
```
| Layer                    | Spring Stack        | Common Names       | Core Responsibilities                  |
| ------------------------ | ------------------- | ------------------ | -------------------------------------- |
| **Presentation Layer**   | @Controller         | Controller, API    | Handle HTTP requests and responses     |
| **Business Logic Layer** | @Service            | Service            | Implement business rules and workflows |
| **Data Access Layer**    | @Mapper             | Mapper, DAO        | Define DB access interfaces            |
| **Persistence Layer**    | MyBatis XML, Entity | Mapper XML, Entity | SQL mapping and entity definitions     |
| **Database Layer**       | MySQL               | Database           | Store and retrieve data                |

## Layer Definitions
### Presentation Layer
**Responsibilities**:
* Handle HTTP requests and responses
* Receive and validate parameters
* Routing and dispatching
* Data format transformation (DTO ↔ Entity ↔ VO)
* Exception handling and HTTP status mapping
**Template**:
```java
@RestController
@RequestMapping("/api/projects")
public class ProjectController {
    private final ProjectService projectService;
    public ProjectController(ProjectService projectService) {
        this.projectService = projectService;
    }
    @GetMapping("/{id}")
    public ApiReturn<ProjectVo> getProject(@PathVariable Long id) {
        Project project = projectService.getProject(id);
        ProjectVo vo = new ProjectVo();
        BeanUtils.copyProperties(project, vo);
        return ApiReturn.of(vo);
    }
    @PostMapping
    public ApiReturn<ProjectVo> createProject(@Valid @RequestBody ProjectCreateRequest request) {
        Project project = new Project();
        BeanUtils.copyProperties(request, project);
        Project created = projectService.createProject(project);
        ProjectVo vo = new ProjectVo();
        BeanUtils.copyProperties(created, vo);
        return ApiReturn.of(vo);
    }
}
```
**Design notes**:
* Keep it thin: HTTP-related logic only
* Use DTO/VO for data transfer
* Centralize validation with Bean Validation and global exception handling
* No business logic
* No direct database access

### Business Logic Layer
**Responsibilities**:
* Implement business rules and workflows
* Data validation and business checks
* Authorization and access control
* Transaction management (boundary here)
* Coordinate multiple services and mappers
* Call the data access layer
**Template**:
```java
@Service
public class ProjectService {
    private final ProjectMapper projectMapper;
    public ProjectService(ProjectMapper projectMapper) {
        this.projectMapper = projectMapper;
    }
    public Project getProject(Long id) {
        if (id == null || id <= 0) {
            throw new BusinessException(400, "Invalid project ID");
        }
        Project project = projectMapper.selectById(id);
        if (project == null) {
            throw new BusinessException(404, "Project does not exist");
        }
        return project;
    }
    @Transactional
    public Project createProject(Project project) {
        if (project.getCustomerId() == null) {
            throw new BusinessException(400, "Customer ID must not be null");
        }
        project.setCreatedTime(LocalDateTime.now());
        project.setStatus(ProjectStatus.CREATED);
        projectMapper.insert(project);
        return project;
    }
}
```
**Design notes**:
* Contains core business logic
* Use `@Transactional` for transactions
* Perform business validations
* Orchestrate multiple services and mappers
* No HTTP concerns
* No direct DB connection handling
* Service should not return DTO (DTO is an input model). Return Entity/Domain or VO consistently.

### Data Access Layer (MyBatis-Plus)
**Responsibilities**:
* Define DB access interfaces
* Provide CRUD abstractions
* Encapsulate persistence details
* Provide aggregate query interfaces when needed
**Template**:
```java
public interface ProjectMapper extends BaseMapper<Project> {
}
```
**Design notes**:
* Interfaces only; no concrete implementations
* Method names clearly express intent
* No SQL statements here (use XML for complex SQL)
* No business logic
* No transaction management
* Must not depend on the Service layer

### Persistence Layer
**Responsibilities**:
* SQL mapping and result mapping
* Entity definitions
* Database-specific SQL fragments (when needed)
**Template (MyBatis-Plus XML)**:
```xml
<mapper namespace="com.example.mapper.ProjectMapper">
    <select id="selectActive" resultType="com.example.entity.Project">
        SELECT * FROM project WHERE status = 'CREATED'
    </select>
</mapper>
```
**Design notes**:
* Focus on SQL authoring and optimization
* Result mapping and type conversion
* Use SQL fragments for reusability
* No business logic
* No business validations
* Connection management and transaction boundaries are handled by Spring and DataSource

### Database Layer
**Responsibilities**:
* Persistent storage
* Data integrity constraints
* Indexes and performance optimization
* Transaction support
**Template (MySQL)**:
```sql
CREATE TABLE project (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    created_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    customer_id BIGINT NOT NULL,
    status VARCHAR(50) DEFAULT 'CREATED'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

## Data Transfer Patterns
### Using DTO, VO, and Entity
```
Frontend → Controller → Service → Mapper → Database
           DTO        Entity    Entity
           VO         Entity
```
### Conversion Example
```java
@PostMapping("/projects")
public ApiReturn<ProjectVo> createProject(@Valid @RequestBody ProjectCreateRequest request) {
    Project project = new Project();
    BeanUtils.copyProperties(request, project);
    Project created = projectService.createProject(project);
    ProjectVo vo = new ProjectVo();
    BeanUtils.copyProperties(created, vo);
    return ApiReturn.of(vo);
}
```

## Exception Handling
### Centralized Exception Handling
```java
public class BusinessException extends RuntimeException {
    private final int code;
    public BusinessException(int code, String message) {
        super(message);
        this.code = code;
    }
    public int getCode() {
        return code;
    }
}

@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(BusinessException.class)
    public ApiReturn<Void> handleBusinessException(BusinessException e) {
        return ApiReturn.error(e.getCode(), e.getMessage());
    }
    @ExceptionHandler(Exception.class)
    public ApiReturn<Void> handleException(Exception e) {
        return ApiReturn.error(500, "Internal server error");
    }
}
```

## Transaction Guidelines
- Transaction boundaries belong to Service methods.
- Use `@Transactional(readOnly = true)` for read-only queries.
- Rollback on RuntimeException by default; document checked-exception rollbacks if needed.
- Avoid transactions in Controller, Mapper, or XML.

## Common Pitfalls
### Pitfall 1: Cross-Layer Calls
```java
// Incorrect: Controller directly calls Mapper
@RestController
public class ProjectController {
    private final ProjectMapper projectMapper;
    public ProjectController(ProjectMapper projectMapper) {
        this.projectMapper = projectMapper;
    }
    public List<Project> getProjects() {
        return projectMapper.selectList(null);
    }
}
```
### Pitfall 2: Reverse Dependency
```java
// Incorrect: Service depends on Controller
@Service
public class ProjectService {
    private ProjectController projectController;
}
```
### Pitfall 3: Business Logic in SQL
```xml
<!-- Incorrect: business logic embedded in SQL -->
<select id="getById" resultMap="BaseResultMap">
    SELECT * FROM project
    WHERE id = #{id}
      AND is_deleted = 0
      AND has_permission(#{currentUserId}, id) = 1
</select>
```
### Pitfall 4: Returning Entity Directly from Controller
```java
// Incorrect: Controller returns Entity directly
@GetMapping("/projects/{id}")
public Project getProject(@PathVariable Long id) {
    return projectService.getProject(id);
}
```

## Project Structure Template (Recommended)
```
src/main/java/com/xdyai/backend/
  controller/
    internal/
    request/
  service/
    common/
    context/
    integration/
  mapper/
  entity/
    enumeration/

src/main/resources/
  application.yml
  application-dev.yml
  mapper/
  db/
  validation/
  integration/
```

## Best Practices Summary
### Presentation Layer
* Keep it thin: HTTP logic only
* Use DTO/VO for data transfer
* Centralized exception handling
* No business logic
* No direct Mapper access
### Business Logic Layer
* Contains core business logic
* Use `@Transactional` to manage transactions
* Orchestrate multiple services
* No HTTP concerns
* No direct database connection handling
### Data Access Layer
* Interfaces only
* Clear method naming
* CRUD via MyBatis-Plus
* No SQL statements here
* No business logic
### Persistence Layer
* Focus on SQL authoring
* Use SQL fragments
* Use dynamic SQL for complex queries
* No business logic
* No business validations
### Cross-Layer Communication
* Controller ← DTO
* Service ← Entity
* Mapper ← Entity
* Controller ← VO
* Avoid cross-layer calls
* Avoid reverse dependencies
