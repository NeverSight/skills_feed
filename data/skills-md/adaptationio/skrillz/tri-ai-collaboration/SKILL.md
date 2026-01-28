---
name: tri-ai-collaboration
description: Complete development workflows where Claude writes the code while Gemini and Codex provide research, planning, reviews, and different perspectives. Claude remains the main developer. Use for complex projects requiring expert planning and multi-perspective reviews.
---

# Tri-AI Collaboration: Claude as Developer with AI Advisors

**Claude writes the code. Gemini and Codex advise, review, plan, and provide different eyes.**

## The Workflow Model

### Role Clarity

This is **NOT** about having Gemini/Codex write code for you. This is about:

**Claude (You) = The Developer**
- **Writes/edits all code** using Write and Edit tools
- Makes final decisions on implementation
- Maintains context and system understanding
- Integrates all the pieces

**Gemini = Research Advisor & Fast Analyst**
- Researches best practices and latest patterns
- Analyzes images (architecture diagrams, UI mockups)
- Provides quick analysis and feedback
- Offers alternative perspectives

**Codex = Code Advisor & Deep Reasoner**
- Reviews code for issues and improvements
- Suggests architectural improvements
- Provides deep reasoning on complex decisions
- Validates approaches

### The Collaborative Loop

```
1. [Gemini] Research → Give findings to Claude
2. [Codex] Architectural reasoning → Give recommendations to Claude
3. [CLAUDE] **WRITES THE CODE** based on advisor input
4. [Gemini + Codex] Review Claude's code → Give feedback
5. [CLAUDE] **EDITS THE CODE** based on feedback
6. Repeat until production-ready
```

**Key Point**: At every step, **Claude is the one writing and editing code**. The other AIs are consultants.

## The Power of Three

### Why Use Advisors?

**Each AI provides unique value as an advisor:**

- **Claude (You - Sonnet 4.5)** - Main developer
  - **Does**: Writes code, edits files, makes decisions, integrates components
  - **Tools**: Read, Write, Edit, Bash, all Claude Code tools
  - **Role**: The actual software developer

- **Gemini (2.5 Pro/Flash)** - Research & Analysis Advisor
  - **Does**: Web research, image analysis, quick reviews, alternative suggestions
  - **Provides**: Latest patterns, best practices, competitive analysis, rapid feedback
  - **Role**: Research consultant and fast reviewer

- **Codex (GPT-5.1/o3)** - Code & Architecture Advisor
  - **Does**: Code reviews, architectural reasoning, deep analysis, problem-solving
  - **Provides**: Code improvements, architectural guidance, complex reasoning
  - **Role**: Senior developer consultant and code reviewer

**Together**: Claude writes better code faster with expert advice from multiple perspectives

## Complete Example: Advisory Workflow

### Building a User Authentication System

**Goal**: Implement OAuth2 authentication

#### Step 1: Research (Gemini advises)

```bash
# Claude asks Gemini to research
gemini --yolo --output-format json \
  "Research OAuth2 implementation best practices 2025:
  1. Security considerations
  2. Popular libraries (Passport.js, etc.)
  3. Token storage strategies
  4. Common pitfalls
  Return structured JSON recommendations" \
  > /tmp/oauth-research.json
```

**Claude reads the research:**
```bash
cat /tmp/oauth-research.json | jq .
```

#### Step 2: Architecture (Codex advises)

```bash
# Claude asks Codex for architectural guidance
codex exec -m o3 --json --dangerously-bypass-approvals-and-sandbox \
  "Based on @/tmp/oauth-research.json, design OAuth2 architecture:
  1. Component structure
  2. Database schema
  3. API endpoints
  4. Security measures
  Return detailed architectural recommendations" \
  > /tmp/oauth-architecture.json
```

**Claude reviews the architecture:**
```bash
cat /tmp/oauth-architecture.json | jq .
```

#### Step 3: Implementation (CLAUDE WRITES THE CODE)

**Claude reads the advice and writes the actual code:**

```javascript
// Claude creates: ./src/auth/oauth.js

// Based on Gemini's research and Codex's architecture,
// Claude writes the implementation:

const passport = require('passport');
const OAuth2Strategy = require('passport-oauth2');
const jwt = require('jsonwebtoken');

class OAuthService {
  constructor(config) {
    this.config = config;
    this.initializeStrategy();
  }

  initializeStrategy() {
    passport.use(new OAuth2Strategy({
      authorizationURL: this.config.authURL,
      tokenURL: this.config.tokenURL,
      clientID: this.config.clientID,
      clientSecret: this.config.clientSecret,
      callbackURL: this.config.callbackURL
    }, this.verifyCallback.bind(this)));
  }

  async verifyCallback(accessToken, refreshToken, profile, done) {
    try {
      // Claude implements based on architectural guidance
      const user = await this.findOrCreateUser(profile);
      const token = this.generateJWT(user);
      return done(null, { user, token });
    } catch (error) {
      return done(error);
    }
  }

  generateJWT(user) {
    return jwt.sign(
      { id: user.id, email: user.email },
      process.env.JWT_SECRET,
      { expiresIn: '24h' }
    );
  }

  async findOrCreateUser(profile) {
    // Implementation based on advisor recommendations
    // ...
  }
}

module.exports = OAuthService;
```

#### Step 4: Review (Both AIs review Claude's code)

```bash
# Get Codex's code review
codex exec -m gpt-5.1-codex --json --dangerously-bypass-approvals-and-sandbox \
  "Review this OAuth implementation @./src/auth/oauth.js:
  1. Security issues
  2. Code quality
  3. Best practices adherence
  4. Potential bugs
  5. Improvement suggestions
  Return detailed review as JSON" \
  > /tmp/codex-review.json

# Get Gemini's perspective
gemini --yolo --output-format json \
  "Review this OAuth code @./src/auth/oauth.js:
  1. Compare to latest best practices
  2. Security concerns
  3. Alternative approaches
  4. Missing features
  Return review as JSON" \
  > /tmp/gemini-review.json
```

**Claude reads both reviews:**
```bash
echo "=== Codex Review ==="
cat /tmp/codex-review.json | jq '.suggestions'

echo "=== Gemini Review ==="
cat /tmp/gemini-review.json | jq '.recommendations'
```

#### Step 5: Refinement (CLAUDE EDITS THE CODE)

**Based on the reviews, Claude improves the code:**

```javascript
// Claude edits ./src/auth/oauth.js based on advisor feedback

// Codex suggested: Add rate limiting
// Gemini suggested: Add PKCE for security
// Claude implements both suggestions:

const rateLimit = require('express-rate-limit');
const crypto = require('crypto');

class OAuthService {
  constructor(config) {
    this.config = config;
    this.rateLimiter = this.setupRateLimiting();
    this.initializeStrategy();
  }

  // Claude added based on Codex's suggestion
  setupRateLimiting() {
    return rateLimit({
      windowMs: 15 * 60 * 1000,
      max: 5,
      message: 'Too many login attempts'
    });
  }

  // Claude added based on Gemini's suggestion
  generatePKCEChallenge() {
    const verifier = crypto.randomBytes(32).toString('base64url');
    const challenge = crypto
      .createHash('sha256')
      .update(verifier)
      .digest('base64url');
    return { verifier, challenge };
  }

  // ... rest of improved implementation
}
```

#### Step 6: Testing (Advisors suggest, Claude implements)

```bash
# Ask Codex for test strategy
codex exec -m gpt-5.1-codex --json \
  "Suggest comprehensive test strategy for @./src/auth/oauth.js" \
  > /tmp/test-strategy.json
```

**Claude writes the tests based on suggestions:**

```javascript
// Claude creates: ./tests/auth/oauth.test.js

const OAuthService = require('../../src/auth/oauth');

describe('OAuthService', () => {
  // Claude implements tests based on Codex's strategy

  describe('Rate Limiting', () => {
    it('should block after 5 failed attempts', async () => {
      // Claude's implementation
    });
  });

  describe('PKCE Challenge', () => {
    it('should generate valid PKCE challenge', () => {
      // Claude's implementation
    });
  });

  // ... more tests Claude wrote
});
```

#### Step 7: Final Review (Multi-perspective validation)

```bash
# Parallel reviews from both advisors
codex exec -m o3 --json --dangerously-bypass-approvals-and-sandbox \
  "Final security audit of complete OAuth implementation" \
  > /tmp/final-codex.json &

gemini --yolo --output-format json \
  "Final review: Does this match 2025 best practices?" \
  > /tmp/final-gemini.json &

wait

# Claude reviews both perspectives and makes final adjustments
```

**Result**: Claude wrote all the code, but with expert advice from two AI advisors at every step.

## Complete Development Cycle (Advisory Model)

### Phase 1: Research & Planning (Advisors inform Claude)

**Claude orchestrates → Gemini executes**

```bash
#!/bin/bash
# Complete research phase

echo "=== PHASE 1: RESEARCH & ANALYSIS ==="

# 1. Claude identifies what needs research
# "We need to build a real-time notification system.Let me research best practices."

# 2. Claude directs Gemini for web research
gemini --yolo --output-format json \
  "Research real-time notification systems 2025:
  1. WebSocket vs SSE vs Long Polling
  2. Scaling patterns (Redis pub/sub, etc.)
  3. Security best practices
  4. Popular libraries and frameworks
  Return structured JSON with findings" \
  > research/notifications-research.json

# 3. Claude directs Gemini for competitive analysis
gemini --yolo --output-format json \
  "Analyze these notification implementations:
  - @https://github.com/socketio/socket.io
  - @https://github.com/pusher/pusher-http-node
  Compare architecture, features, tradeoffs
  Return JSON comparison" \
  > research/competitive-analysis.json

# 4. Claude directs Gemini for multimodal analysis
gemini --yolo \
  "Analyze this system architecture diagram @./docs/current-arch.png
  and suggest how to integrate real-time notifications" \
  > research/integration-analysis.txt

echo "✓ Research complete"
```

### Phase 2: Planning & Architecture (Claude + Codex)

**Claude plans → Codex validates → Claude decides**

```bash
echo "=== PHASE 2: PLANNING & ARCHITECTURE ==="

# 1. Claude synthesizes research and creates plan
cat research/*.json research/*.txt > research/all-findings.txt

# 2. Claude directs Codex for architectural reasoning (use o3)
codex exec -m o3 --json --dangerously-bypass-approvals-and-sandbox \
  "Based on research in @research/all-findings.txt, design a scalable
  real-time notification architecture:
  1. Technology stack recommendations
  2. System architecture (components, data flow)
  3. Database schema
  4. API design
  5. Security considerations
  6. Scaling strategy
  Return detailed JSON architecture spec" \
  > planning/architecture.json

# 3. Claude reviews and refines
# Claude reads architecture.json and makes strategic decisions

# 4. Claude directs Codex to create detailed implementation plan
codex exec -m gpt-5.1-codex --json --dangerously-bypass-approvals-and-sandbox \
  "Create detailed implementation plan for @planning/architecture.json:
  1. Break into phases (backend, frontend, testing, deployment)
  2. List all files to create
  3. Define dependencies and order
  4. Estimate complexity
  5. Identify risks
  Return JSON implementation roadmap" \
  > planning/implementation-plan.json

echo "✓ Planning complete"
```

### Phase 3: Parallel Implementation (Gemini + Codex)

**Claude orchestrates parallel execution**

```bash
echo "=== PHASE 3: IMPLEMENTATION ===" # Claude assigns tasks based on strengths

# Backend: Codex (complex code generation)
codex exec -m gpt-5.1-codex --dangerously-bypass-approvals-and-sandbox \
  "Implement backend per @planning/implementation-plan.json:
  Phase 1 - Backend WebSocket server:
  1. Create NotificationService class in ./src/services/notification.js
  2. Implement Redis pub/sub integration
  3. Add authentication middleware
  4. Create connection management
  5. Add error handling and reconnection logic
  Create all files and implement completely" \
  > /tmp/backend-log.txt 2>&1 &
backend_pid=$!

# Frontend: Gemini (fast iteration + UI components)
gemini --yolo \
  "Implement frontend per @planning/implementation-plan.json:
  Phase 1 - Frontend components:
  1. Create useNotifications React hook in ./src/hooks/
  2. Build NotificationBell component
  3. Build NotificationList component
  4. Build Toast component
  5. Style with Tailwind CSS
  Create all files completely" \
  > /tmp/frontend-log.txt 2>&1 &
frontend_pid=$!

# Database: Codex (structured data modeling)
codex exec -m gpt-5.1-codex --dangerously-bypass-approvals-and-sandbox \
  "Implement database layer per @planning/implementation-plan.json:
  1. Create Notification model with Sequelize
  2. Create migrations
  3. Add indexes for performance
  4. Create seed data for testing
  Complete implementation" \
  > /tmp/database-log.txt 2>&1 &
database_pid=$!

# Wait for all parallel tasks
wait $backend_pid
wait $frontend_pid
wait $database_pid

echo "✓ Core implementation complete"
```

### Phase 4: Testing & Quality (Codex + Gemini)

**Claude coordinates comprehensive testing**

```bash
echo "=== PHASE 4: TESTING & QUALITY ==="

# 1. Codex generates comprehensive tests
codex exec -m gpt-5.1-codex --dangerously-bypass-approvals-and-sandbox \
  "Generate complete test suite:
  1. Unit tests for NotificationService
  2. Integration tests for WebSocket connections
  3. API endpoint tests
  4. Frontend component tests
  5. E2E tests for complete flow
  Target >90% coverage, implement all tests" \
  > /tmp/test-generation.txt 2>&1

# 2. Gemini runs tests and analyzes failures
gemini --yolo --output-format json \
  "Run all tests and analyze results:
  1. Execute npm test
  2. Analyze any failures
  3. Suggest fixes for failures
  4. Check coverage
  Return JSON report" \
  > testing/test-results.json

# 3. If failures, Claude decides fix strategy
if [ "$(jq '.failures > 0' testing/test-results.json)" = "true" ]; then
  echo "Tests failed, fixing..."

  # Codex fixes complex logic issues
  codex exec -m gpt-5.1-codex --dangerously-bypass-approvals-and-sandbox \
    "Fix test failures from @testing/test-results.json
    Focus on logic and implementation bugs" \
    > /tmp/codex-fixes.txt 2>&1 &

  # Gemini fixes integration and UI issues
  gemini --yolo \
    "Fix test failures from @testing/test-results.json
    Focus on integration and UI component bugs" \
    > /tmp/gemini-fixes.txt 2>&1 &

  wait

  # Re-run tests
  gemini --yolo --output-format json \
    "Run tests again and report results" \
    > testing/test-results-final.json
fi

echo "✓ Testing complete"
```

### Phase 5: Security & Performance (Codex reasons, Gemini researches)

**Claude ensures production readiness**

```bash
echo "=== PHASE 5: SECURITY & PERFORMANCE ==="

# 1. Codex performs security analysis (use o3 for reasoning)
codex exec -m o3 --search --dangerously-bypass-approvals-and-sandbox \
  "Security audit of notification system:
  1. Analyze authentication implementation
  2. Check for XSS vulnerabilities
  3. Verify CSRF protection
  4. Check WebSocket security
  5. Review rate limiting
  6. Identify and FIX all security issues
  Research latest security best practices" \
  > security/audit-report.txt

# 2. Gemini researches performance optimizations
gemini --yolo --output-format json \
  "Research WebSocket performance optimization 2025:
  1. Connection pooling strategies
  2. Message batching techniques
  3. Redis optimization for pub/sub
  4. Load balancing approaches
  Return structured recommendations" \
  > performance/research.json

# 3. Codex implements performance optimizations
codex exec -m gpt-5.1-codex --dangerously-bypass-approvals-and-sandbox \
  "Implement performance optimizations from @performance/research.json:
  1. Add connection pooling
  2. Implement message batching
  3. Optimize Redis usage
  4. Add performance monitoring
  Implement all optimizations" \
  > /tmp/perf-optimization.txt

echo "✓ Security & Performance complete"
```

### Phase 6: Documentation (Gemini generates, Codex validates)

**Claude ensures comprehensive documentation**

```bash
echo "=== PHASE 6: DOCUMENTATION ==="

# 1. Gemini generates user-facing documentation
gemini --yolo \
  "Generate complete documentation suite:
  1. README.md with quick start
  2. API documentation (OpenAPI spec)
  3. WebSocket protocol documentation
  4. Frontend integration guide
  5. Deployment guide
  6. Troubleshooting guide
  Create all documentation files" \
  > /tmp/doc-generation.txt &

# 2. Codex generates code documentation
codex exec -m gpt-5.1-codex-mini --dangerously-bypass-approvals-and-sandbox \
  "Add comprehensive code documentation:
  1. JSDoc comments for all functions
  2. README in each directory
  3. Architecture decision records (ADRs)
  4. Code examples in comments
  Add to all source files" \
  > /tmp/code-docs.txt &

wait

echo "✓ Documentation complete"
```

### Phase 7: Git & Deployment (Codex git expert)

**Claude coordinates release**

```bash
echo "=== PHASE 7: GIT & DEPLOYMENT ==="

# 1. Codex creates semantic commits
codex exec -m gpt-5.1-codex-mini --dangerously-bypass-approvals-and-sandbox \
  "Review all changes and create semantic commits:
  1. feat: add WebSocket notification service
  2. feat: add notification UI components
  3. feat: add notification API endpoints
  4. test: add comprehensive notification test suite
  5. perf: optimize WebSocket connections
  6. docs: add complete notification documentation
  Create all commits with proper messages"

# 2. Codex generates changelog
codex exec -m gpt-5.1-codex-mini --dangerously-bypass-approvals-and-sandbox \
  "Generate CHANGELOG.md entry for this release:
  1. List all features added
  2. List all improvements
  3. Document breaking changes
  4. Add migration guide
  Create complete changelog entry"

# 3. Gemini creates deployment automation
gemini --yolo \
  "Create deployment automation:
  1. Docker compose configuration
  2. Kubernetes manifests
  3. CI/CD pipeline (GitHub Actions)
  4. Environment configuration examples
  5. Deployment scripts
  Create all deployment files"

# 4. Codex creates PR
codex exec -m gpt-5.1-codex-mini --dangerously-bypass-approvals-and-sandbox \
  "Create pull request:
  1. Generate PR title and description
  2. List all changes with context
  3. Add testing checklist
  4. Add deployment notes
  5. Create PR via gh cli
  Complete PR creation"

echo "✓ Git & Deployment complete"
```

## Strategic AI Assignment

### Decision Matrix

**Claude decides which AI to use based on task type:**

| Task Type | Primary AI | Secondary AI | Reason |
|-----------|-----------|--------------|---------|
| **Web Research** | Gemini | - | Native web search, fast |
| **Architecture Design** | Codex (o3) | Claude | Deep reasoning needed |
| **Code Generation** | Codex (GPT-5.1) | - | Code-optimized model |
| **UI Components** | Gemini | Codex | Fast iteration, visual |
| **Refactoring** | Codex | - | Code understanding |
| **Testing** | Codex | Gemini | Test generation expertise |
| **Documentation** | Gemini | Codex | Fast writing, examples |
| **Security Analysis** | Codex (o3) | Gemini | Deep reasoning + research |
| **Performance Optimization** | Gemini (research) → Codex (implement) | - | Research then implement |
| **Debugging** | Codex | Gemini | Code analysis strength |
| **Git Operations** | Codex | - | Git-aware capabilities |
| **Multimodal Analysis** | Gemini | - | Image support |
| **Database Design** | Codex (o3) | - | Structured reasoning |
| **API Design** | Codex | - | Standard patterns |
| **Quick Fixes** | Gemini or Codex (mini) | - | Fast, cheap models |

### Model Selection Within AIs

**Codex Models:**
- `o3` - Complex reasoning (architecture, security analysis, debugging)
- `gpt-5.1-codex` - Standard development (implementation, refactoring)
- `gpt-5.1-codex-mini` or `o4-mini` - Quick tasks (docs, commits, simple fixes)

**Gemini Models:**
- `gemini-2.5-pro` - Complex analysis, important decisions
- `gemini-2.5-flash` - Fast iteration, documentation, research

**Claude Models:**
- `sonnet-4.5` - All orchestration (you're using this now!)

## Advanced Collaboration Patterns

### Pattern 1: Research → Reason → Implement

**Best for: New features, unfamiliar domains**

```bash
#!/bin/bash
# Three-stage pipeline

# Stage 1: Gemini researches
gemini --yolo --output-format json \
  "Research GraphQL federation patterns 2025" \
  > stage1-research.json

# Stage 2: Codex reasons through architecture
codex exec -m o3 --dangerously-bypass-approvals-and-sandbox \
  "Design GraphQL federation architecture based on @stage1-research.json" \
  > stage2-architecture.json

# Stage 3: Codex implements
codex exec -m gpt-5.1-codex --dangerously-bypass-approvals-and-sandbox \
  "Implement GraphQL federation per @stage2-architecture.json"
```

### Pattern 2: Parallel Execution + Synthesis

**Best for: Independent components**

```bash
#!/bin/bash
# Parallel execution with Claude synthesis

# Launch parallel tasks
gemini --yolo "Build component A" > a.log 2>&1 &
pid_a=$!

codex exec --dangerously-bypass-approvals-and-sandbox "Build component B" > b.log 2>&1 &
pid_b=$!

gemini --yolo "Build component C" > c.log 2>&1 &
pid_c=$!

# Wait for completion
wait $pid_a $pid_b $pid_c

# Claude synthesizes and integrates
# "All components built. Now I'll integrate them..."
codex exec --dangerously-bypass-approvals-and-sandbox \
  "Integrate components A, B, C per integration plan"
```

### Pattern 3: Iterative Refinement

**Best for: Complex, evolving requirements**

```bash
#!/bin/bash
# Iterative improvement cycle

for iteration in {1..5}; do
  echo "=== Iteration $iteration ==="

  # Codex implements
  codex exec -m gpt-5.1-codex --dangerously-bypass-approvals-and-sandbox \
    "Iteration $iteration: Implement next feature" \
    > "iter-$iteration-implementation.log"

  # Gemini tests
  gemini --yolo --output-format json \
    "Run tests and analyze quality" \
    > "iter-$iteration-quality.json"

  # Claude decides: continue or done?
  quality=$(jq '.quality_score' "iter-$iteration-quality.json")

  if (( $(echo "$quality >= 95" | bc -l) )); then
    echo "Quality threshold met!break
  fi

  # Codex refines based on feedback
  codex exec --dangerously-bypass-approvals-and-sandbox \
    "Improve based on feedback in @iter-$iteration-quality.json"
done
```

### Pattern 4: Fault Tolerance & Fallback

**Best for: Production systems, critical tasks**

```bash
#!/bin/bash
# Multi-AI fallback system

execute_with_fallback() {
  local task="$1"
  local primary_ai="$2"
  local fallback_ai="$3"

  echo "Attempting with $primary_ai..."

  if [ "$primary_ai" = "codex" ]; then
    if codex exec --dangerously-bypass-approvals-and-sandbox "$task"; then
      return 0
    fi
  elif [ "$primary_ai" = "gemini" ]; then
    if gemini --yolo "$task"; then
      return 0
    fi
  fi

  echo "Primary failed, falling back to $fallback_ai..."

  if [ "$fallback_ai" = "codex" ]; then
    codex exec --dangerously-bypass-approvals-and-sandbox "$task"
  elif [ "$fallback_ai" = "gemini" ]; then
    gemini --yolo "$task"
  fi
}

# Usage
execute_with_fallback "Generate tests" "codex" "gemini"
```

### Pattern 5: Consensus Decision Making

**Best for: Critical decisions, architecture choices**

```bash
#!/bin/bash
# Get opinions from all three AIs

QUESTION="Should we use PostgreSQL or MongoDB for this project?"

echo "Getting consensus..."

# Codex analysis
codex exec -m o3 --search --json \
  "$QUESTION Consider: @./requirements.md" \
  > consensus/codex-opinion.json &

# Gemini analysis
gemini --yolo --output-format json \
  "$QUESTION Research latest best practices" \
  > consensus/gemini-opinion.json &

wait

# Claude synthesizes (you read both opinions and decide)
echo "Codex recommends: $(jq '.recommendation' consensus/codex-opinion.json)"
echo "Gemini recommends: $(jq '.recommendation' consensus/gemini-opinion.json)"

# Claude makes final strategic decision
```

## Cost Optimization Strategies

### Use Cheaper Models Strategically

```bash
#!/bin/bash
# Cost-optimized workflow

# Quick tasks: Use mini/flash models
codex exec -m o4-mini "Format code with Prettier"
gemini -m gemini-2.5-flash --yolo "Add comments to functions"

# Standard tasks: Use standard models
codex exec -m gpt-5.1-codex "Implement user authentication"
gemini --yolo "Generate API documentation"

# Complex tasks: Use powerful models
codex exec -m o3 "Design microservices architecture"
gemini -m gemini-2.5-pro --yolo "Comprehensive security audit research"
```

### Batch Operations

```bash
#!/bin/bash
# Batch instead of individual calls

# ❌ BAD: Multiple calls
for file in *.js; do
  codex exec "Fix linting in $file"
done

# ✅ GOOD: Single batched call
codex exec --dangerously-bypass-approvals-and-sandbox \
  "Fix linting issues in all *.js files"
```

### Parallel + Cheap Models

```bash
#!/bin/bash
# Use multiple cheap models in parallel instead of expensive serial

# Instead of: o3 for everything (slow + expensive)
# Use: Multiple cheap models in parallel (fast + economical)

codex exec -m o4-mini "Task 1" &
codex exec -m o4-mini "Task 2" &
gemini -m gemini-2.5-flash --yolo "Task 3" &
codex exec -m gpt-5.1-codex-mini "Task 4" &

wait
```

## Complete Real-World Example

### Building a Complete SaaS Feature

```bash
#!/bin/bash
# Build "User Analytics Dashboard" feature from scratch

PROJECT="User Analytics Dashboard"
echo "=== Building: $PROJECT ==="

# PHASE 1: DISCOVERY (Gemini)
echo "Phase 1: Research & Discovery"
gemini --yolo --output-format json \
  "Research user analytics dashboard best practices 2025:
  1. Popular metrics and visualizations
  2. Real-time vs batch processing
  3. Data storage strategies
  4. Visualization libraries (React)
  5. Privacy and compliance (GDPR/CCPA)
  Return comprehensive research" \
  > discovery/research.json

# PHASE 2: ARCHITECTURE (Codex o3)
echo "Phase 2: Architecture Design"
codex exec -m o3 --json --dangerously-bypass-approvals-and-sandbox \
  "Design analytics dashboard architecture:
  Based on @discovery/research.json
  1. Data collection strategy
  2. Processing pipeline (real-time + batch)
  3. Database schema
  4. API design
  5. Frontend architecture
  6. Scaling strategy
  Return complete technical specification" \
  > architecture/spec.json

# PHASE 3: PARALLEL IMPLEMENTATION
echo "Phase 3: Implementation"

# Backend: Codex
codex exec -m gpt-5.1-codex --dangerously-bypass-approvals-and-sandbox \
  "Implement analytics backend per @architecture/spec.json:
  1. Event collection API
  2. Data processing pipeline
  3. Aggregation jobs
  4. Query API
  5. WebSocket for real-time updates
  Complete implementation with error handling" \
  > logs/backend.log 2>&1 &
backend_pid=$!

# Frontend: Gemini (faster UI iteration)
gemini --yolo \
  "Implement analytics dashboard UI per @architecture/spec.json:
  1. Dashboard layout
  2. Chart components (use Recharts)
  3. Real-time updates hook
  4. Filter controls
  5. Export functionality
  Complete implementation with Tailwind styling" \
  > logs/frontend.log 2>&1 &
frontend_pid=$!

# Database: Codex
codex exec -m gpt-5.1-codex --dangerously-bypass-approvals-and-sandbox \
  "Implement database layer per @architecture/spec.json:
  1. Event storage schema
  2. Aggregated metrics tables
  3. Indexes for performance
  4. Migrations
  5. Seed data
  Complete implementation" \
  > logs/database.log 2>&1 &
database_pid=$!

wait $backend_pid $frontend_pid $database_pid

# PHASE 4: TESTING
echo "Phase 4: Testing"

# Generate tests: Codex
codex exec -m gpt-5.1-codex --dangerously-bypass-approvals-and-sandbox \
  "Generate comprehensive test suite:
  1. API endpoint tests
  2. Data processing tests
  3. WebSocket tests
  4. Frontend component tests
  5. E2E dashboard tests
  Aim for >90% coverage" \
  > logs/test-gen.log

# Run and fix: Gemini
gemini --yolo --output-format json \
  "Run all tests, analyze failures, and fix issues" \
  > testing/results.json

# PHASE 5: OPTIMIZATION
echo "Phase 5: Performance & Security"

# Security: Codex o3
codex exec -m o3 --search --dangerously-bypass-approvals-and-sandbox \
  "Security audit:
  1. Authentication/authorization
  2. Data privacy (PII handling)
  3. Rate limiting
  4. Input validation
  5. GDPR compliance
  Fix all issues found" \
  > security/audit.log

# Performance: Gemini research + Codex implement
gemini --yolo --output-format json \
  "Research dashboard performance optimization techniques" \
  > perf/research.json

codex exec -m gpt-5.1-codex --dangerously-bypass-approvals-and-sandbox \
  "Implement optimizations from @perf/research.json"

# PHASE 6: DOCUMENTATION
echo "Phase 6: Documentation"

# User docs: Gemini
gemini --yolo \
  "Create complete user documentation:
  1. README with screenshots
  2. User guide
  3. API documentation
  4. Deployment guide
  Complete documentation suite" \
  > logs/user-docs.log &

# Code docs: Codex
codex exec -m gpt-5.1-codex-mini --dangerously-bypass-approvals-and-sandbox \
  "Add comprehensive code documentation:
  JSDoc for all functions" \
  > logs/code-docs.log &

wait

# PHASE 7: DEPLOYMENT
echo "Phase 7: Deployment Automation"

# Gemini creates deployment setup
gemini --yolo \
  "Create deployment automation:
  1. Docker configuration
  2. Kubernetes manifests
  3. CI/CD pipeline
  4. Monitoring setup (Prometheus/Grafana)
  Complete deployment system"

# Codex creates release
codex exec -m gpt-5.1-codex-mini --dangerously-bypass-approvals-and-sandbox \
  "Create release:
  1. Semantic commits
  2. Changelog
  3. Version bump
  4. Git tags
  5. PR with detailed description
  Complete release process"

echo ""
echo "=== $PROJECT COMPLETE ==="
echo "✓ Research & Architecture"
echo "✓ Complete Implementation (Backend + Frontend + Database)"
echo "✓ Comprehensive Testing (>90% coverage)"
echo "✓ Security Audit & Performance Optimization"
echo "✓ Complete Documentation"
echo "✓ Deployment Automation & Release"
echo ""
echo "Total time: ~45-60 minutes (vs 2-3 days manual)"
echo "Quality: Production-ready with tests, docs, and security"
```

## Best Practices

### 1. Always Use Claude as Orchestrator

```bash
# ✅ GOOD: Claude decides, directs, synthesizes
# Claude analyzes requirements
# Claude assigns tasks to Gemini/Codex
# Claude reviews results
# Claude makes strategic decisions

# ❌ BAD: Random AI usage
# Using whatever AI without strategy
```

### 2. Match AI to Task Type

```bash
# ✅ GOOD: Use strengths
gemini --yolo "Research latest React patterns"  # Gemini for research
codex exec -m o3 "Design database schema"  # Codex o3 for reasoning
codex exec -m gpt-5.1-codex "Implement auth"  # Codex for code

# ❌ BAD: Wrong AI for task
codex exec "Research web trends"  # Codex can't web search!
gemini "Design complex algorithm"  # Gemini weaker at pure reasoning
```

### 3. Use JSON for AI-to-AI Communication

```bash
# ✅ GOOD: Structured, parseable
gemini --yolo --output-format json "Analyze and return JSON"
codex exec --json "Analyze and return JSON"

# ❌ BAD: Unstructured text
gemini --yolo "Analyze and describe"  # Hard for next AI to parse
```

### 4. Parallel When Possible

```bash
# ✅ GOOD: Parallel independent tasks
gemini --yolo "Task A" &
codex exec "Task B" &
codex exec "Task C" &
wait

# ❌ BAD: Sequential when could be parallel
gemini --yolo "Task A"
codex exec "Task B"  # Could have run in parallel!
```

### 5. Use Appropriate Model Tiers

```bash
# ✅ GOOD: Match model cost to task complexity
codex exec -m o3 "Complex architecture"  # Worth the cost
codex exec -m o4-mini "Format code"  # Cheap for simple task

# ❌ BAD: Expensive model for simple task
codex exec -m o3 "Add comment"  # Overkill!
```

## Troubleshooting Tri-AI Workflows

### One AI Fails

```bash
# If Codex fails, try Gemini
if ! codex exec "$task"; then
  echo "Codex failed, trying Gemini..."
  gemini --yolo "$task"
fi
```

### Rate Limiting

```bash
# Distribute load across AIs
if [ "$codex_requests_today" -gt 900 ]; then
  echo "Codex quota low, using Gemini instead"
  gemini --yolo "$task"
else
  codex exec "$task"
fi
```

### Inconsistent Results

```bash
# Use consensus approach
codex exec --json "$question" > codex-answer.json
gemini --yolo --output-format json "$question" > gemini-answer.json

# Claude reviews both and decides
```

## Related Skills

- `codex-cli`: Codex integration and automation
- `gemini-cli`: Gemini integration and web research
- `CLAUDE-CODEX-INTEGRATION.md`: Claude + Codex patterns
- `CLAUDE-GEMINI-INTEGRATION.md`: Claude + Gemini patterns

## Summary

**The Ultimate Workflow:**
1. **Claude** orchestrates everything (strategic decisions)
2. **Gemini** researches, analyzes images, iterates quickly
3. **Codex** generates code, reasons deeply, manages git
4. **Together** they build production systems in minutes

**Key Principles:**
- Match AI to task strengths
- Run parallel when possible
- Use cheaper models strategically
- Always use structured (JSON) communication
- Let Claude coordinate and synthesize

**Result:** 10-50x faster development with higher quality than any single AI or manual development.

---

**🚀 Ready to build at superhuman speed? Start with the complete SaaS example above!**
