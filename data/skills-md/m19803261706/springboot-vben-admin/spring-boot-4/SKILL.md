---
name: spring-boot-4
description: Spring Boot 4 后端开发规范。当创建 Controller、Service、Entity、Repository 或后端 API 时自动使用。
---

# Spring Boot 4 开发规范

本项目使用 Spring Boot 4.0.1 + JPA + MySQL 8 技术栈。

## 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Spring Boot | 4.0.1 | Web 框架 |
| Spring Data JPA | 3.4.x | 数据访问 |
| Hibernate | 7.x | ORM |
| MySQL | 8.0 | 数据库 |
| JSpecify | 1.0.0 | Null 安全 |
| SpringDoc | 2.8.x | API 文档 |
| Lombok | - | 简化代码 |

## 目录结构

```
backend/src/main/java/com/taichu/yingjiguanli/
├── YingjiGuanliApplication.java    # 启动类
├── common/                          # 通用类
│   ├── ApiResponse.java            # 统一响应
│   ├── BusinessException.java      # 业务异常
│   └── PageResult.java             # 分页结果
├── config/                          # 配置类
│   ├── CorsConfig.java
│   ├── GlobalExceptionHandler.java
│   └── JpaConfig.java
├── modules/                         # 业务模块
│   └── {module}/                   # 模块名
│       ├── entity/                 # 实体类
│       ├── repository/             # 数据访问
│       ├── service/                # 服务层
│       │   └── impl/
│       ├── controller/             # 控制器
│       ├── dto/                    # 数据传输对象
│       └── vo/                     # 视图对象
└── resources/
    ├── application.yml
    └── db/migration/               # Flyway 迁移
```

## 代码模板

### Entity 实体类

```java
package com.taichu.yingjiguanli.modules.{module}.entity;

import jakarta.persistence.*;
import lombok.Data;
import org.hibernate.annotations.Comment;
import org.jspecify.annotations.Nullable;

import java.time.LocalDateTime;

/**
 * {实体描述}
 *
 * @author CX
 * @since {date}
 */
@Data
@Entity
@Table(name = "{table_name}")
@Comment("{表描述}")
public class {EntityName} {

    /**
     * 主键ID
     */
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Comment("主键ID")
    private Long id;

    /**
     * {字段描述}
     */
    @Column(nullable = false, length = 100)
    @Comment("{字段描述}")
    private String name;

    /**
     * 创建时间
     */
    @Column(nullable = false, updatable = false)
    @Comment("创建时间")
    private LocalDateTime createdAt;

    /**
     * 更新时间
     */
    @Column(nullable = false)
    @Comment("更新时间")
    private LocalDateTime updatedAt;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
    }

    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }
}
```

### Repository 数据访问

```java
package com.taichu.yingjiguanli.modules.{module}.repository;

import com.taichu.yingjiguanli.modules.{module}.entity.{EntityName};
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import org.springframework.stereotype.Repository;

import java.util.Optional;

/**
 * {实体}数据访问接口
 *
 * @author CX
 * @since {date}
 */
@Repository
public interface {EntityName}Repository extends JpaRepository<{EntityName}, Long>, JpaSpecificationExecutor<{EntityName}> {

    /**
     * 根据名称查询
     */
    Optional<{EntityName}> findByName(String name);
}
```

### Service 服务层

```java
package com.taichu.yingjiguanli.modules.{module}.service;

import com.taichu.yingjiguanli.modules.{module}.dto.{EntityName}DTO;
import com.taichu.yingjiguanli.modules.{module}.entity.{EntityName};
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import java.util.Optional;

/**
 * {实体}服务接口
 *
 * @author CX
 * @since {date}
 */
public interface {EntityName}Service {

    /**
     * 创建
     */
    {EntityName} create({EntityName}DTO dto);

    /**
     * 更新
     */
    {EntityName} update(Long id, {EntityName}DTO dto);

    /**
     * 删除
     */
    void delete(Long id);

    /**
     * 根据ID查询
     */
    Optional<{EntityName}> findById(Long id);

    /**
     * 分页查询
     */
    Page<{EntityName}> findAll(Pageable pageable);
}
```

### ServiceImpl 服务实现

```java
package com.taichu.yingjiguanli.modules.{module}.service.impl;

import com.taichu.yingjiguanli.common.BusinessException;
import com.taichu.yingjiguanli.modules.{module}.dto.{EntityName}DTO;
import com.taichu.yingjiguanli.modules.{module}.entity.{EntityName};
import com.taichu.yingjiguanli.modules.{module}.repository.{EntityName}Repository;
import com.taichu.yingjiguanli.modules.{module}.service.{EntityName}Service;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Optional;

/**
 * {实体}服务实现
 *
 * @author CX
 * @since {date}
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class {EntityName}ServiceImpl implements {EntityName}Service {

    private final {EntityName}Repository repository;

    @Override
    @Transactional
    public {EntityName} create({EntityName}DTO dto) {
        log.info("创建{实体}: {}", dto);
        {EntityName} entity = new {EntityName}();
        // 设置属性...
        return repository.save(entity);
    }

    @Override
    @Transactional
    public {EntityName} update(Long id, {EntityName}DTO dto) {
        log.info("更新{实体} ID={}: {}", id, dto);
        {EntityName} entity = repository.findById(id)
                .orElseThrow(() -> new BusinessException(404, "{实体}不存在"));
        // 更新属性...
        return repository.save(entity);
    }

    @Override
    @Transactional
    public void delete(Long id) {
        log.info("删除{实体} ID={}", id);
        if (!repository.existsById(id)) {
            throw new BusinessException(404, "{实体}不存在");
        }
        repository.deleteById(id);
    }

    @Override
    public Optional<{EntityName}> findById(Long id) {
        return repository.findById(id);
    }

    @Override
    public Page<{EntityName}> findAll(Pageable pageable) {
        return repository.findAll(pageable);
    }
}
```

### Controller 控制器

```java
package com.taichu.yingjiguanli.modules.{module}.controller;

import com.taichu.yingjiguanli.common.ApiResponse;
import com.taichu.yingjiguanli.common.BusinessException;
import com.taichu.yingjiguanli.modules.{module}.dto.{EntityName}DTO;
import com.taichu.yingjiguanli.modules.{module}.entity.{EntityName};
import com.taichu.yingjiguanli.modules.{module}.service.{EntityName}Service;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.web.bind.annotation.*;

/**
 * {实体}控制器
 *
 * @author CX
 * @since {date}
 */
@RestController
@RequestMapping("/api/{module}")
@RequiredArgsConstructor
@Tag(name = "{模块名称}", description = "{模块描述}")
public class {EntityName}Controller {

    private final {EntityName}Service service;

    /**
     * 创建
     */
    @PostMapping
    @Operation(summary = "创建{实体}")
    public ApiResponse<{EntityName}> create(@Valid @RequestBody {EntityName}DTO dto) {
        return ApiResponse.success(service.create(dto));
    }

    /**
     * 更新
     */
    @PutMapping("/{id}")
    @Operation(summary = "更新{实体}")
    public ApiResponse<{EntityName}> update(@PathVariable Long id, @Valid @RequestBody {EntityName}DTO dto) {
        return ApiResponse.success(service.update(id, dto));
    }

    /**
     * 删除
     */
    @DeleteMapping("/{id}")
    @Operation(summary = "删除{实体}")
    public ApiResponse<Void> delete(@PathVariable Long id) {
        service.delete(id);
        return ApiResponse.success();
    }

    /**
     * 查询详情
     */
    @GetMapping("/{id}")
    @Operation(summary = "查询{实体}详情")
    public ApiResponse<{EntityName}> getById(@PathVariable Long id) {
        return ApiResponse.success(service.findById(id)
                .orElseThrow(() -> new BusinessException(404, "{实体}不存在")));
    }

    /**
     * 分页查询
     */
    @GetMapping
    @Operation(summary = "分页查询{实体}")
    public ApiResponse<Page<{EntityName}>> list(Pageable pageable) {
        return ApiResponse.success(service.findAll(pageable));
    }
}
```

### DTO 数据传输对象

```java
package com.taichu.yingjiguanli.modules.{module}.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.Data;

/**
 * {实体}数据传输对象
 *
 * @author CX
 * @since {date}
 */
@Data
public class {EntityName}DTO {

    /**
     * 名称
     */
    @NotBlank(message = "名称不能为空")
    @Size(max = 100, message = "名称长度不能超过100")
    private String name;

    // 其他字段...
}
```

## Flyway 迁移脚本

```sql
-- V{n}__{description}.sql
-- 作者: CX
-- 日期: {date}
-- 描述: {description}

CREATE TABLE {table_name} (
    id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    name VARCHAR(100) NOT NULL COMMENT '名称',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='{表描述}';
```

## 命名规范

| 位置 | 规范 | 示例 |
|------|------|------|
| 包名 | 小写 | `com.taichu.yingjiguanli.modules.user` |
| 类名 | PascalCase | `UserController`, `UserService` |
| 方法名 | camelCase | `findById`, `createUser` |
| 变量名 | camelCase | `userName`, `createdAt` |
| 常量名 | UPPER_SNAKE | `MAX_PAGE_SIZE` |
| 表名 | snake_case | `sys_user`, `t_order` |
| 字段名 | snake_case | `user_name`, `created_at` |

## 最佳实践

1. **统一响应**: 所有接口返回 `ApiResponse<T>`
2. **业务异常**: 使用 `BusinessException` 抛出业务错误
3. **参数校验**: 使用 `@Valid` + `jakarta.validation`
4. **日志记录**: 关键操作使用 `@Slf4j` 记录日志
5. **事务管理**: Service 层使用 `@Transactional`
6. **中文注释**: 所有类、方法、字段必须有中文注释

---
> 项目: 应急管理系统 (yingjiguanli)
> 技术栈: Spring Boot 4.0.1 + JPA + MySQL 8
