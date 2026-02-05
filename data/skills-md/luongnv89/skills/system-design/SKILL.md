---
name: system-design
description: Generate Technical Architecture Documents (TAD) from PRD files. Use when users ask to "design the architecture", "create a TAD", "system design", or want to define how a product will be built. Creates tad.md with modular architecture optimized for startups.
---

# System Design

Generate comprehensive Technical Architecture Documents with modular design for startups.

## Design Principles

- **Modularity**: Separated concerns for independent testing and development
- **Simplicity**: Minimal complexity appropriate for startup resources
- **Scalability**: Designed to grow with user base
- **Cost-effectiveness**: Optimized for startup budget

## Input

Project folder path in `$ARGUMENTS` containing:
- `prd.md` - Product requirements (required)
- `idea.md`, `validate.md` - Additional context (optional)

## Workflow

### Phase 1: Setup & Validation

1. Verify `prd.md` exists
2. Read supporting docs if present
3. Read [references/tech-stack.md](references/tech-stack.md) for technology recommendations
4. Backup existing `tad.md` if present

### Phase 2: Extract Context

From PRD extract:
- Product name and vision
- Core features and requirements
- User flows
- Non-functional requirements
- Third-party integrations
- Analytics requirements

### Phase 3: Clarify Architecture

Ask user (if not clear):

| Decision | Options |
|----------|---------|
| Deployment | Vercel/Netlify (recommended), AWS, GCP, Self-hosted |
| Database | PostgreSQL, MongoDB, Supabase/Firebase, Multiple |
| Auth | Social (OAuth), Email/password, Magic links, Enterprise SSO |
| Budget | Free tier, <$50/mo, <$200/mo, Flexible |

### Phase 4: Research & Validation

Conduct 5 research rounds:
1. **Technology Stack**: Validate choices against industry standards
2. **Infrastructure**: Compare hosting for cost and scalability
3. **Security**: Review OWASP guidelines for chosen stack
4. **Risk Assessment**: Identify bottlenecks, vendor lock-in
5. **Holistic Review**: Ensure PRD alignment and startup feasibility

### Phase 5: Generate TAD

Create `tad.md` with sections:

1. **System Overview** - Purpose, scope, PRD alignment
2. **Architecture Diagram** - Mermaid diagrams for system and flows
3. **Technology Stack** - Frontend, backend, database, infrastructure, DevOps
4. **System Components** - Modular design with interfaces and dependencies
5. **Data Architecture** - Schema, models, flows, storage
6. **Infrastructure** - Hosting, environments, scaling, CI/CD, monitoring
7. **Security** - Auth, authorization, data protection, API security
8. **Performance** - Targets, optimization strategies, caching
9. **Development** - Environment setup, project structure, testing, deployment
10. **Risks** - Risk matrix with mitigations
11. **Appendix** - Research insights, alternatives, costs, glossary

See [references/tad-template.md](references/tad-template.md) for full template structure.

### Phase 6: Output

1. Write `tad.md` to project folder
2. Summarize architecture decisions
3. Highlight modular design benefits
4. List cost estimates by phase
5. Suggest next steps (setup dev environment, create tasks)

## Modification Mode

For existing TAD changes:
1. Create timestamped backup
2. Ask what to modify (stack, infrastructure, security, data, scaling)
3. Apply changes preserving structure
4. Update revision history

## Guidelines

- **Practical**: Implementable solutions for startups
- **Cost-conscious**: Consider budget implications
- **Modular**: Emphasize separation of concerns
- **Specific**: Concrete technology choices
- **Visual**: Include mermaid diagrams
