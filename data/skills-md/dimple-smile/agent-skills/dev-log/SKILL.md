---
name: dev-log
description: AI 调试协作方案。将 console.log 转为 HTTP 请求收集日志，用户操作完成后 AI 可自行查看分析，无需截图或复制控制台。支持 Claude Code、OpenCode、Cursor。
version: 1.0.0
tags:
  - debugging
  - frontend
  - developer-tools
---

# Dev Log

将前端代码的 console.log 输出通过 HTTP 接口实时发送，让 AI 能够自动获取运行时日志，无需用户手动复制控制台内容。

**核心理念：** 大多数 console.log 都是为了让 AI 查看结果，因此应该默认使用 dev-log 方式，除非是非常简单的临时调试。

## When to Use

**AI 应该主动判断并使用此技能的情况：**

1. **生成前端代码时** - 如果生成的代码可能需要调试/验证，默认使用 dev-log 收集日志
2. **用户说"帮我调试"、"有问题"、"看看为什么"** - 需要查看运行时状态时
3. **需要追踪异步流程** - fetch、Promise、async/await 的执行过程
4. **需要验证逻辑** - 表单验证、状态更新、条件判断等
5. **需要查看变量值** - 特别是动态生成或用户输入的值
6. **用户说"操作完成了"、"你看下"、"好了"** - 提示用户已完成操作，AI 应该读取日志

**不需要使用的情况：**
- 纯静态内容生成（如 HTML 模板）
- 非常简单的一次性验证
- 用户明确表示不需要调试
- 代码完全是后端的（Node.js 服务端）

## Examples

### Example 1: 主动启用 - AI 判断需要调试

```markdown
User: 写一个 React 计数器组件

Agent: 我来创建一个计数器组件，并添加日志以便验证功能正常。
[启动 dev-log 服务，生成 sessionId: sess_8x7k2p]

```jsx
function Counter() {
  const [count, setCount] = useState(0);
  const increment = () => {
    fetch('http://localhost:54321',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({sessionId:'sess_8x7k2p',time:new Date().toTimeString().split(' ')[0],type:'before-increment',data:{count}})}).catch(()=>{});
    setCount(c => c + 1);
  };
  return <button onClick={increment}>Count: {count}</button>;
}
```

请点击按钮几次，然后告诉我结果。

User: 点了3次

Agent: [读取日志]
从日志看到：
- count 从 0 → 1 → 2 → 3
- 每次 increment 都正确执行

计数器工作正常！
```

### Example 2: 追踪异步请求

```markdown
User: 这个异步函数有时候会失败，帮我看看

Agent: [uses dev-log skill] 启动日志服务...

```javascript
async function fetchData(userId) {
  fetch('http://localhost:54321',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({sessionId:'sess_a1b2c3',time:new Date().toTimeString().split(' ')[0],type:'fetch-start',data:{userId}})}).catch(()=>{});

  try {
    const response = await fetch(`/api/users/${userId}`);
    fetch('http://localhost:54321',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({sessionId:'sess_a1b2c3',time:new Date().toTimeString().split(' ')[0],type:'fetch-response',data:{status:response.status,ok:response.ok}})}).catch(()=>{});

    if (!response.ok) {
      fetch('http://localhost:54321',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({sessionId:'sess_a1b2c3',time:new Date().toTimeString().split(' ')[0],type:'fetch-error',data:{status:response.status}})}).catch(()=>{});
      throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();
    fetch('http://localhost:54321',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({sessionId:'sess_a1b2c3',time:new Date().toTimeString().split(' ')[0],type:'fetch-success',data:{hasData:!!data}})}).catch(()=>{});

    return data;
  } catch (error) {
    fetch('http://localhost:54321',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({sessionId:'sess_a1b2c3',time:new Date().toTimeString().split(' ')[0],type:'catch-error',data:{message:error.message}})}).catch(()=>{});
    throw error;
  }
}
```

操作一下，告诉我结果。

User: 还是失败

Agent: [读取日志]
日志显示：
- fetch-start ✓
- fetch-response {status: 404, ok: false}
- fetch-error

问题是返回 404，说明 API 端点 `/api/users/${userId}` 不存在。需要检查后端路由配置...
```

### Example 3: 表单验证追踪

```markdown
User: 写一个登录表单的验证逻辑

Agent: [启动 dev-log，生成 sessionId: sess_valid9]

```javascript
function validateLoginForm(form) {
  const email = form.email.value;
  const password = form.password.value;

  fetch('http://localhost:54321',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({sessionId:'sess_valid9',time:new Date().toTimeString().split(' ')[0],type:'validate-input',data:{field:'email',value:email}})}).catch(()=>{});

  const errors = {};

  if (!email) {
    errors.email = '邮箱不能为空';
  }

  fetch('http://localhost:54321',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({sessionId:'sess_valid9',time:new Date().toTimeString().split(' ')[0],type:'validate-result',data:{field:'email',valid:!!email}})}).catch(()=>{});

  // ... 更多验证

  fetch('http://localhost:54321',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({sessionId:'sess_valid9',time:new Date().toTimeString().split(' ')[0],type:'final-result',data:{errorCount:Object.keys(errors).length}})}).catch(()=>{});

  return { valid: Object.keys(errors).length === 0, errors };
}
```

测试后告诉我结果，我会根据日志判断验证逻辑是否正确。
```

## Implementation

### 服务启动

**启动命令：**
```bash
cd skills/dev-log && ./start.sh
```

启动脚本会自动：
1. 检查现有服务状态（读取 `port.txt` 并测试连接）
2. 如果服务正常运行，则复用现有服务
3. 如果服务异常或不存在，则启动新服务
4. 服务启动后会记录端口到 `port.txt`，进程 ID 到 `pid.txt`

**文件结构：**
```
./skills/dev-log/
├── start.sh         # 启动脚本（检查/启动服务）
├── read-log.sh      # 读取日志脚本（支持过滤）
├── server.js        # HTTP 服务器（ESM 模块）
├── pid.txt          # 服务进程 ID
├── port.txt         # 服务端口
└── dev-logs.json    # 日志文件（JSON 格式）
```

### 日志读取

**读取所有日志：**
```bash
./skills/dev-log/read-log.sh
```

**按 sessionId 过滤日志：**
```bash
./skills/dev-log/read-log.sh "$SESSION_ID"
```

### 代码生成模板

**标准 fetch 请求模板：**
```javascript
fetch('http://localhost:PORT',{
  method:'POST',
  headers:{'Content-Type':'application/json'},
  body:JSON.stringify({
    sessionId:'SESSION_ID',
    time:'TIME',
    type:'TYPE',
    data:DATA
  })
}).catch(()=>{})
```

**单行简化版本：**
```javascript
fetch('http://localhost:PORT',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({sessionId:'SID',time:'TIME',type:'TYPE',data:DATA})}).catch(()=>{})
```

**模板变量说明：**
- `PORT`: 从 `skills/dev-log/port.txt` 读取的端口号
- `SESSION_ID`: AI 生成的会话 ID（格式：`sess_` + 8位随机字符）
- `TIME`: 时间戳（如 `14:23:05` 或 `new Date().toTimeString().split(' ')[0]`）
- `TYPE`: 日志类型（建议：`state`/`error`/`validation`/`request`/`response`/`fetch-start` 等）
- `DATA`: 要记录的任意数据对象

### 完整使用流程

1. **AI 判断需要调试** → 自动启动 dev-log 技能
2. **检查/启动服务** → 测试现有服务或启动新服务
3. **生成 sessionId** → 在内存中记住，格式 `sess_xxxxxxxx`
4. **清空日志** → 新一轮调试开始时
5. **读取端口号** → 从 `port.txt` 获取
6. **生成带日志的代码** → 在关键位置插入 fetch 语句
7. **提示用户操作** → "请操作一下，然后告诉我结果"
8. **用户告知完成** → "好了"、"操作完成了"
9. **读取并分析日志** → 按 sessionId 过滤，分析结果

### 多会话隔离

- 每个 AI 会话有独立的 sessionId（内存中）
- 日志都写入同一个 `dev-logs.json`
- AI 读取日志时用自己的 sessionId 过滤
- 格式：`{"sessionId":"sess_abc123","time":"14:23:05","type":"state","data":{...}}`

### 注意事项

1. **默认使用** - 生成前端代码时默认考虑使用 dev-log，除非非常简单
2. **清理时机** - 新一轮调试开始时清空日志
3. **生产环境** - 务必移除调试代码
4. **错误处理** - fetch 必须加 `.catch(()=>{})` 避免阻塞主逻辑
5. **单行插入** - 日志代码在用户代码的下一行插入，保持原代码结构
6. **本地开发** - 仅用于本地开发，不要暴露到公网
