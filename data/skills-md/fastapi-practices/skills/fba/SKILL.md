---
name: fba
description: |
  FastAPI Best Architecture (fba) 项目开发指南。提供完整的架构规范、编码风格、插件开发指导。

  使用场景：
  - 在 fba 项目中开发新功能或模块
  - 创建或修改插件（应用级/扩展级）
  - 编写 API、Service、CRUD、Model、Schema
  - 数据库迁移和模型设计
  - JWT 认证和 RBAC 权限配置
  - 代码审查和风格检查
---

# FastAPI Best Architecture 开发技能

**官方文档**: https://fastapi-practices.github.io/fastapi_best_architecture_docs/

## 项目结构

```
backend/
├── main.py                     # 应用入口
├── run.py                      # 启动脚本（IDE 调试）
├── cli.py                      # CLI 命令行工具
├── app/                        # 核心业务模块
│   ├── router.py               # 主路由汇总
│   ├── admin/                  # 管理后台应用
│   │   ├── api/v1/             # API 路由
│   │   │   ├── auth/           # 认证模块
│   │   │   ├── sys/            # 系统模块
│   │   │   ├── log/            # 日志模块
│   │   │   └── monitor/        # 监控模块
│   │   ├── crud/               # 数据访问层
│   │   ├── model/              # 数据库模型
│   │   ├── schema/             # Pydantic 模型
│   │   ├── service/            # 业务逻辑层
│   │   └── tests/              # 单元测试
│   └── task/                   # 异步任务（Celery）
├── common/                     # 通用模块
│   ├── exception/              # 异常处理
│   ├── response/               # 响应模型
│   ├── security/               # 安全模块（JWT、RBAC）
│   ├── model.py                # 模型基类
│   └── schema.py               # Schema 基类
├── core/                       # 核心配置
│   ├── conf.py                 # 全局配置
│   └── registrar.py            # 应用注册
├── database/                   # 数据库配置
│   ├── db.py                   # SQLAlchemy
│   └── redis.py                # Redis
├── middleware/                 # 中间件
├── plugin/                     # 插件系统
├── utils/                      # 工具函数
├── locale/                     # 国际化语言包
├── alembic/                    # 数据库迁移
└── sql/                        # SQL 初始化脚本
```

## 核心架构

项目采用**伪三层架构**：

```
API → Service → CRUD → Model
        ↓
      Schema（数据传输）
```

| 层级      | 职责                                 |
|---------|------------------------------------|
| API     | 路由处理、参数验证、响应返回                     |
| Schema  | 数据传输对象，请求/响应数据结构定义                 |
| Service | 业务逻辑、数据处理、异常处理（静态方法 + `*` 强制关键字参数） |
| CRUD    | 数据库操作（继承 `CRUDPlus`）               |
| Model   | ORM 模型（继承 `Base`）                  |

## 开发流程

1. 定义数据库模型（model）
2. 定义数据验证模型（schema）
3. 定义路由（router）
4. 编写业务逻辑（service）
5. 编写数据库操作（crud）

## 详细指南

| 文档                                                       | 内容               |
|----------------------------------------------------------|------------------|
| [references/naming.md](references/naming.md)             | CRUD/Schema 命名规范 |
| [references/model.md](references/model.md)               | 数据库模型、字段类型、迁移    |
| [references/schema.md](references/schema.md)             | Schema 定义规范      |
| [references/api.md](references/api.md)                   | 路由组织、响应规范、认证权限   |
| [references/plugin.md](references/plugin.md)             | 插件开发完整指南         |
| [references/coding-style.md](references/coding-style.md) | 编码风格、文档、注释规范     |
| [references/config.md](references/config.md)             | 全局配置项说明          |

## 快速参考

### 事务处理

```python
# 只读查询
@router.get('/users')
async def get_users(db: CurrentSession): ...


# 增删改（自动事务）
@router.post('/users')
async def create_user(db: CurrentSessionTransaction, obj: CreateUserParam): ...
```

### 响应格式

```python
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base

return response_base.success()  # 无数据
return response_base.success(data=user)  # 带数据
```

### 异常处理

```python
from backend.common.exception import errors

raise errors.NotFoundError(msg='用户不存在')  # 404
raise errors.RequestError(msg='参数错误')  # 400
raise errors.ForbiddenError(msg='无权访问')  # 403
raise errors.ConflictError(msg='用户名已存在')  # 409
raise errors.ServerError(msg='服务异常')  # 500
```

### JWT 认证

```python
from backend.common.security.jwt import DependsJwtAuth


@router.get('/users', dependencies=[DependsJwtAuth])
async def get_users(): ...
```

### RBAC 权限

```python
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC


@router.post('/users', dependencies=[Depends(RequestPermission('sys:user:add')), DependsRBAC])
async def create_user(): ...
```

## 代码模板

### Schema 层模板

```python
from pydantic import Field

from backend.common.schema import SchemaBase


class ItemSchemaBase(SchemaBase):
    """基础模型"""

    name: str = Field(description='名称')
    status: int = Field(default=1, description='状态')


class CreateItemParam(ItemSchemaBase):
    """创建参数"""

    pass


class UpdateItemParam(SchemaBase):
    """更新参数"""

    name: str | None = Field(None, description='名称')
    status: int | None = Field(None, description='状态')


class GetItemDetail(ItemSchemaBase):
    """Xxx详情"""

    id: int = Field(description='ID')
```

### CRUD 层模板

```python
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy_crud_plus import CRUDPlus


class CRUDItem(CRUDPlus[Item]):
    """Xxx 数据库操作类"""

    async def get(self, db: AsyncSession, pk: int) -> Item | None:
        """
        获取 Xxx

        :param db: 数据库会话
        :param pk: Xxx ID
        :return:
        """
        return await self.select_model(db, pk)

    async def get_select(self, name: str | None, status: int | None) -> Select:
        """
        获取 Xxx 列表查询表达式

        :param name: 名称
        :param status: 状态
        :return:
        """
        filters = {}
        if name is not None:
            filters['name__like'] = f'%{name}%'
        if status is not None:
            filters['status'] = status
        return await self.select_order('id', 'desc', **filters)

    async def create(self, db: AsyncSession, obj: CreateItemParam) -> None:
        """
        创建 Xxx

        :param db: 数据库会话
        :param obj: 创建 Xxx 参数
        :return:
        """
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateItemParam) -> int:
        """
        更新 Xxx

        :param db: 数据库会话
        :param pk: Xxx ID
        :param obj: 更新 Xxx 参数
        :return:
        """
        return await self.update_model(db, pk, obj)

    async def delete(self, db: AsyncSession, pk: int) -> int:
        """
        删除 Xxx

        :param db: 数据库会话
        :param pk: Xxx ID
        :return:
        """
        return await self.delete_model(db, pk)


item_dao: CRUDItem = CRUDItem(Item)
```

### Service 层模板

```python
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from backend.common.exception import errors
from backend.common.pagination import paging_data


class ItemService:
    """Xxx 服务类"""

    @staticmethod
    async def get(*, db: AsyncSession, pk: int) -> Item:
        """
        获取 Xxx

        :param db: 数据库会话
        :param pk: Xxx ID
        :return:
        """
        item = await item_dao.get(db, pk)
        if not item:
            raise errors.NotFoundError(msg='记录不存在')
        return item

    @staticmethod
    async def get_list(*, db: AsyncSession, name: str | None, status: int | None) -> dict[str, Any]:
        """
        获取 Xxx 列表

        :param db: 数据库会话
        :param name: 名称
        :param status: 状态
        :return:
        """
        select = await item_dao.get_select(name, status)
        return await paging_data(db, select)

    @staticmethod
    async def create(*, db: AsyncSession, obj: CreateItemParam) -> None:
        """
        创建 Xxx

        :param db: 数据库会话
        :param obj: 创建 Xxx 参数
        :return:
        """
        await item_dao.create(db, obj)

    @staticmethod
    async def update(*, db: AsyncSession, pk: int, obj: UpdateItemParam) -> int:
        """
        更新 Xxx

        :param db: 数据库会话
        :param pk: Xxx ID
        :param obj: 更新 Xxx 参数
        :return:
        """
        item = await item_dao.get(db, pk)
        if not item:
            raise errors.NotFoundError(msg='记录不存在')
        count = await item_dao.update(db, pk, obj)
        return count

    @staticmethod
    async def delete(*, db: AsyncSession, pk: int) -> int:
        """
        删除 Xxx

        :param db: 数据库会话
        :param pk: Xxx ID
        :return:
        """
        item = await item_dao.get(db, pk)
        if not item:
            raise errors.NotFoundError(msg='记录不存在')
        count = await item_dao.delete(db, pk)
        return count


item_service: ItemService = ItemService()
```

### API 层模板

```python
from typing import Annotated

from fastapi import APIRouter, Path, Query

from backend.common.pagination import DependsPagination, PageData
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.database.db import CurrentSession, CurrentSessionTransaction

router = APIRouter()


@router.get(
    '',
    summary='分页获取列表',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_items_paginated(
    db: CurrentSession,
    name: Annotated[str | None, Query(description='名称')] = None,
    status: Annotated[int | None, Query(description='状态')] = None,
) -> ResponseSchemaModel[PageData[GetItemDetail]]:
    page_data = await item_service.get_list(db=db, name=name, status=status)
    return response_base.success(data=page_data)


@router.get('/{pk}', summary='获取详情', dependencies=[DependsJwtAuth])
async def get_item(
    db: CurrentSession,
    pk: Annotated[int, Path(description='ID')],
) -> ResponseSchemaModel[GetItemDetail]:
    item = await item_service.get(db=db, pk=pk)
    return response_base.success(data=item)


@router.post('', summary='创建', dependencies=[DependsJwtAuth])
async def create_item(
    db: CurrentSessionTransaction,
    obj: CreateItemParam,
) -> ResponseModel:
    await item_service.create(db=db, obj=obj)
    return response_base.success()


@router.put('/{pk}', summary='更新', dependencies=[DependsJwtAuth])
async def update_item(
    db: CurrentSessionTransaction,
    pk: Annotated[int, Path(description='ID')],
    obj: UpdateItemParam,
) -> ResponseModel:
    count = await item_service.update(db=db, pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete('/{pk}', summary='删除', dependencies=[DependsJwtAuth])
async def delete_item(
    db: CurrentSessionTransaction,
    pk: Annotated[int, Path(description='ID')],
) -> ResponseModel:
    count = await item_service.delete(db=db, pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()
```

## CLI 命令

```bash
# 启动服务
fba run

# 数据库迁移
alembic revision --autogenerate -m "描述"
alembic upgrade head

# 代码质量
prek run --all-files
```
