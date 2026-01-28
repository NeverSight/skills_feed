---
name: vm-dev
description: 虚拟机开发专家，专注于字节码、指令、栈帧、内存管理和垃圾回收。
version: v1.0
tags: [vm, bytecode, execution, stack, memory, gc]
allowed-tools: mcp__serena__find_symbol, mcp__serena__replace_symbol_body, Read, Bash
requires-skills: [ep-navigator, compiler-dev]
---

# 虚拟机开发

## 🎯 垂直职责
**单一职责**: 虚拟机实现 - 字节码执行、指令集、栈帧、内存管理、垃圾回收

## 📦 核心能力

### 1. 字节码设计 (EP13-EP15)
- **定义**: `BytecodeDefinition.java`
- **指令集**: IADD, ISUB, IMUL, IDIV, LOAD, STORE, CALL, RET, JMP
- **操作数栈**: 后进先出 (LIFO)

### 2. 栈式虚拟机 (EP18)
- **位置**: `ep18/src/main/java/org/teachfx/antlr4/ep18/stackvm/`
- **核心**: `CymbolStackVM.java`
- **栈帧**: `StackFrame.java` (局部变量 + 操作数栈 + 返回地址)

### 3. 寄存器虚拟机 (EP18R)
- **位置**: `ep18r/src/main/java/org/teachfx/antlr4/ep18r/regvm/`
- **核心**: `CymbolRegisterVM.java`
- **寄存器分配**: 基于ABI约定的寄存器使用

### 4. 内存管理 (EP18/EP18R)
- **堆内存**: `HeapMemory.java`
- **GC**: 标记-清除算法
- **对象布局**: 类型信息 + 字段数据

## 🔗 关系图
→ **ep-navigator** (识别EP范围)
→ **compiler-dev** (IR → 字节码)

## 🚀 快速开始

### 添加新指令
```bash
# 1. 定义操作码
vim ep18/src/main/java/.../BytecodeDefinition.java
// enum OpCode { ..., NEW_OP(0x20); }

# 2. 实现指令类
vim ep18/src/main/java/.../instruction/NewOpInstruction.java
public class NewOpInstruction extends Instruction {
    @Override
    public void execute(ExecutionContext ctx) {
        // 实现逻辑
    }
}

# 3. 注册指令
vim ep18/src/main/java/.../InstructionFactory.java

# 4. 测试
mvn test -pl ep18 -Dtest="*NewOpInstruction*"
```

### 实现垃圾回收
```bash
# 1. 定义对象头
class ObjectHeader {
    Type type;
    boolean marked;
    int size;
}

# 2. 实现标记阶段
void mark(VarSlot root) {
    Object obj = heap.get(root);
    if (obj != null && !obj.header.marked) {
        obj.header.marked = true;
        for (VarSlot field : obj.getReferences()) {
            mark(field);
        }
    }
}

# 3. 实现清除阶段
void sweep() {
    heap.removeIf(obj -> !obj.header.marked);
}
```

## 📊 栈帧结构

```
┌─────────────────────────────────┐
│     返回地址 (Return Address)    │
├─────────────────────────────────┤
│     局部变量区 (Locals)          │
│     [0] [1] [2] [3] ...         │
├─────────────────────────────────┤
│     操作数栈 (Operand Stack)     │
│     [...] [...] [...]           │
└─────────────────────────────────┘
```

## 🛠️ 常用命令

```bash
# 虚拟机相关
mvn compile -pl ep18                         # 编译EP18
mvn test -pl ep18 -Dtest="*Instruction*"     # 测试指令
mvn test -pl ep18 -Dtest="*VM*"              # 测试VM
mvn test -pl ep18 -Dtest="*GC*"              # 测试GC

# 运行程序
mvn exec:java -pl ep18 -Dexec.args="program.cx"
```

## 📐 指令格式速查

| 指令 | 操作码 | 操作数 | 栈效果 | 描述 |
|------|--------|--------|--------|------|
| ICONST | 0x01 | value | → value | 加载整数常量 |
| IADD | 0x10 | - | a,b → a+b | 整数加法 |
| ISUB | 0x11 | - | a,b → a-b | 整数减法 |
| LOAD | 0x20 | index | → value | 加载局部变量 |
| STORE | 0x21 | index | value → | 存储局部变量 |
| CALL | 0x30 | addr | args... → | 调用函数 |
| RET | 0x31 | - | value → | 返回函数 |
| JMP | 0x40 | offset | → | 无条件跳转 |
| CONDJMP | 0x41 | offset | cond → | 条件跳转 |

## ⚠️ 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 栈溢出 | 操作数栈超限 | 检查指令栈平衡 |
| 栈下溢 | 弹出空栈 | 验证指令前置条件 |
| 类型错误 | 操作数类型不匹配 | 添加类型检查 |
| 内存泄漏 | GC未正确标记 | 检查根集完整性 |

---
*版本: v1.0 | 垂直职责: 虚拟机实现 | 2025-12-23*
