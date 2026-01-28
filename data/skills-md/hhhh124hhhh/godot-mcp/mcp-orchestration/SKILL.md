---
name: mcp-orchestration
description: 智能编排和协调多个MCP工具完成复杂开发任务，支持串行、并行、条件、循环等多种执行模式
version: 1.0.0
allowed-tools: Read, Write, Skill, Task
---

# MCP工具编排技能

## 指令

当用户需要执行复杂的开发任务或需要多个工具协作时，自动进行MCP工具编排：

### 触发条件
- 需要多步骤的复杂开发流程
- 涉及多个技术栈或工具链
- 需要性能分析、代码审查、文档查询等组合操作
- 项目设置、部署、优化等综合任务

## MCP工具使用说明

此技能主要使用以下MCP工具：
- **Chrome DevTools MCP** - Web开发和调试工具，用于性能分析和网络监控
- **Sequential Thinking MCP** - 逐步推理和问题分解工具，用于逻辑分析和步骤规划
- **Context7 MCP** - 自动文档研究和信息检索工具，用于获取技术文档和最佳实践
- **Godot MCP** - Godot引擎集成工具，用于场景编辑和脚本生成
- **Skill MCP** - 技能调用和管理工具，用于协调其他技能的执行

### MCP调用方式
```bash
# 并行调用多个MCP工具
const [performance, docs, thinking] = await Promise.all([
  chromeDevToolsMCP.analyze_performance(),
  context7MCP.search('best practices'),
  sequentialThinkingMCP.analyze_problem()
]);

# 串行调用MCP工具
const version = await godotMCP.detect_godot_version();
const analysis = await godotMCP.check_compatibility(code);
const fixes = await godotMCP.fix_issues(analysis.issues);

# 技能内调用其他技能
await useSkill('context7-auto-research', { query: 'user query' });
await useSkill('godot-compatibility-checker', { action: 'check_version' });
```

## 支持的MCP工具

### 已配置工具
1. **Chrome DevTools MCP** - Web开发和调试工具
2. **Sequential Thinking MCP** - 逐步推理和问题分解
3. **Context7 MCP** - 自动文档研究和信息检索
4. **Godot MCP** - Godot引擎集成工具

## 编排模式

### 1. 串行模式 - 逐步执行
适用于需要严格步骤顺序的任务，确保每步完成后再进行下一步。

**示例: Godot项目升级工作流**
```javascript
async function godotProjectUpgrade() {
  // 步骤1: 版本检测
  const version = await useSkill('godot-compatibility-checker', {
    action: 'detect_version'
  });

  // 步骤2: 兼容性分析
  const analysis = await useSkill('godot-compatibility-checker', {
    action: 'analyze_compatibility',
    targetVersion: '4.x'
  });

  // 步骤3: 自动修复
  const fixes = await useSkill('godot-compatibility-checker', {
    action: 'fix_issues',
    issues: analysis.criticalIssues
  });

  // 步骤4: 验证结果
  const validation = await useSkill('godot-compatibility-checker', {
    action: 'validate_fixes'
  });

  return validation;
}
```

### 2. 并行模式 - 同时执行
适用于可同时执行的独立任务，提高执行效率。

**示例: 项目综合分析**
```javascript
async function comprehensiveProjectAnalysis() {
  const [performance, security, documentation] = await Promise.all([
    useSkill('chrome-devtools', { action: 'analyze_performance' }),
    useSkill('context7-auto-research', {
      query: 'security best practices for web applications'
    }),
    useSkill('sequential-thinking', {
      task: 'analyze project architecture and suggest improvements'
    })
  ]);

  return {
    performance: performance.metrics,
    security: security.recommendations,
    architecture: documentation.suggestions
  };
}
```

### 3. 条件模式 - 智能分支
根据中间结果决定后续执行路径，实现智能决策。

**示例: 智能问题诊断**
```javascript
async function intelligentProblemDiagnosis(userIssue) {
  // 步骤1: 问题分类
  const classification = await useSkill('sequential-thinking', {
    task: 'classify_problem',
    description: userIssue
  });

  // 步骤2: 根据分类选择解决方案
  switch (classification.category) {
    case 'compatibility':
      return await handleCompatibilityIssue(userIssue);
    case 'performance':
      return await handlePerformanceIssue(userIssue);
    case 'documentation':
      return await useSkill('context7-auto-research', {
        query: userIssue.description
      });
    case 'architecture':
      return await handleArchitectureIssue(userIssue);
    default:
      return await handleGenericIssue(userIssue);
  }
}
```

### 4. 循环模式 - 迭代优化
适用于需要逐步改进和优化的场景。

**示例: 渐进式代码优化**
```javascript
async function iterativeCodeOptimization(code, targetQuality) {
  let currentCode = code;
  let currentQuality = await measureCodeQuality(currentCode);
  let iteration = 0;
  const maxIterations = 5;

  while (currentQuality < targetQuality && iteration < maxIterations) {
    iteration++;

    // 分析当前问题
    const analysis = await useSkill('sequential-thinking', {
      task: 'analyze_code_improvements',
      code: currentCode
    });

    // 查找最佳实践
    const bestPractices = await useSkill('context7-auto-research', {
      query: `${analysis.improvement_areas} best practices optimization`
    });

    // 应用改进
    const improvedCode = await applyCodeImprovements(currentCode, bestPractices);

    // 验证改进效果
    const newQuality = await measureCodeQuality(improvedCode);

    if (newQuality > currentQuality) {
      currentCode = improvedCode;
      currentQuality = newQuality;
      console.log(`迭代 ${iteration}: 质量提升 ${((newQuality - currentQuality) / currentQuality * 100).toFixed(2)}%`);
    } else {
      console.log(`迭代 ${iteration}: 无明显改进，停止优化`);
      break;
    }
  }

  return {
    optimizedCode: currentCode,
    finalQuality: currentQuality,
    iterations: iteration
  };
}
```

## 实际应用场景

### 场景1: Godot Web游戏完整开发
```javascript
async function developGodotWebGame(gameSpecification) {
  // 阶段1: 项目设置 (串行)
  await useSkill('godot-compatibility-checker', {
    action: 'setup_project',
    spec: gameSpecification
  });

  await useSkill('chrome-devtools', {
    action: 'setup_dev_server',
    port: 8080
  });

  // 阶段2: 功能开发 (并行 + 串行混合)
  const developmentResults = await Promise.all([
    // 核心功能开发
    developCoreFeatures(gameSpecification.coreFeatures),
    // 资源准备
    prepareAssets(gameSpecification.assets),
    // 文档准备
    prepareDocumentation(gameSpecification.documentation)
  ]);

  // 阶段3: 集成测试 (串行)
  await runIntegrationTests(developmentResults);

  // 阶段4: 性能优化 (循环)
  const optimizationResult = await optimizeForWeb(developmentResults);

  return {
    gamePath: gameSpecification.outputPath,
    performanceMetrics: optimizationResult.metrics,
    buildStatus: 'success'
  };
}
```

### 场景2: 智能代码审查工作流
```javascript
async function intelligentCodeReview(pullRequestContent) {
  // 步骤1: 并行分析
  const [staticAnalysis, securityCheck, bestPractices] = await Promise.all([
    useSkill('godot-compatibility-checker', {
      action: 'static_code_analysis',
      code: pullRequestContent.changes
    }),
    useSkill('context7-auto-research', {
      query: 'security vulnerabilities in Godot games web development'
    }),
    useSkill('context7-auto-research', {
      query: 'GDScript best practices code style 2024'
    })
  ]);

  // 步骤2: 逻辑分析
  const logicAnalysis = await useSkill('sequential-thinking', {
    task: 'analyze_code_logic_and_architecture',
    code: pullRequestContent.changes,
    context: staticAnalysis
  });

  // 步骤3: 生成审查报告
  const reviewReport = generateComprehensiveReview({
    static: staticAnalysis,
    security: securityCheck,
    practices: bestPractices,
    logic: logicAnalysis
  });

  return reviewReport;
}
```

## 错误处理和恢复

### 错误分类策略
```javascript
const errorRecoveryStrategies = {
  'network_error': {
    retry: true,
    maxRetries: 3,
    fallback: 'use_cached_result'
  },
  'api_limit_exceeded': {
    retry: false,
    fallback: 'use_alternative_tool'
  },
  'invalid_input': {
    retry: false,
    fallback: 'request_user_correction'
  },
  'tool_unavailable': {
    retry: true,
    fallback: 'manual_intervention'
  }
};
```

### 恢复执行
```javascript
async function handleWorkflowError(error, workflowContext) {
  const strategy = errorRecoveryStrategies[error.type];

  switch (strategy.fallback) {
    case 'use_cached_result':
      return await getCachedResult(workflowContext);
    case 'use_alternative_tool':
      return await tryAlternativeTool(workflowContext);
    case 'request_user_correction':
      return await requestUserInput(error, workflowContext);
    case 'manual_intervention':
      return await escalateToHuman(error, workflowContext);
  }
}
```

## 配置和优化

### 工作流配置示例
```yaml
# workflow-config.yaml
workflows:
  godot-development:
    mode: serial
    steps:
      - tool: godot-compatibility-checker
        action: detect_version
      - tool: context7-auto-research
        query: "Godot 4.x development best practices"
      - tool: godot-compatibility-checker
        action: implement_features

  web-optimization:
    mode: parallel
    steps:
      - tool: chrome-devtools
        action: analyze_performance
      - tool: context7-auto-research
        query: "web performance optimization techniques"
      - tool: sequential-thinking
        task: "analyze performance bottlenecks"

performance:
  default_timeout: 60000
  max_parallel_tasks: 3
  cache_enabled: true
  cache_ttl: 3600000
```

## 输出格式

1. **工作流概述** - 说明执行模式和步骤
2. **执行结果** - 每个步骤的详细结果
3. **性能指标** - 执行时间和资源使用情况
4. **问题诊断** - 遇到的问题和解决方案
5. **改进建议** - 优化工作流的建议

## 注意事项

- 根据任务特性选择最合适的执行模式
- 设置合理的超时时间避免单个步骤阻塞整个工作流
- 实施完善的错误恢复机制提高系统健壮性
- 监控工具性能识别瓶颈并进行优化
- 合理使用缓存减少重复的网络调用
- 在并行执行时注意资源竞争和依赖关系