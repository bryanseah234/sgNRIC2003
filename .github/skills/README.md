---
description: Central skills documentation for AI agents across all repositories
---

# AI Agent Skills Documentation

This folder contains comprehensive skill documentation that teaches AI coding agents how to work with each repository's specific patterns, conventions, and technologies.

## What Are Skills?

Skills are modular markdown files that provide step-by-step guidance for AI agents on:
- Repository-specific coding patterns
- Technology stack conventions
- Common workflows and operations
- Error handling and debugging
- Best practices and anti-patterns

## Skill Structure

Each skill follows this format:

```markdown
---
name: skill-name
description: Brief description of what this skill teaches
technologies: [list, of, technologies]
repositories: [repo1, repo2]
---

# Skill Title

## When to Use
[Context for when this skill applies]

## Prerequisites
[Any required knowledge or setup]

## Step-by-Step Instructions
1. [Detailed step with code examples]
2. [Include verification steps]
3. [Include troubleshooting if needed]

## Common Pitfalls
[Things to avoid]

## References
[Links to related documentation]
```

## Available Skills

### Core Development Skills

#### 1. Python Development
- `python-flask-api.md` - Building REST APIs with Flask
- `python-type-hints.md` - Type annotations and mypy
- `python-async-patterns.md` - Async/await patterns
- `python-testing-pytest.md` - Testing with pytest

#### 2. JavaScript/TypeScript Development
- `javascript-vue3-composition.md` - Vue 3 Composition API
- `typescript-best-practices.md` - TypeScript conventions
- `javascript-react-patterns.md` - React hooks and patterns
- `javascript-vite-build.md` - Vite build configuration

#### 3. Database Skills
- `database-sqlalchemy-patterns.md` - SQLAlchemy ORM patterns
- `database-migrations.md` - Database migration strategies
- `database-postgresql-optimization.md` - PostgreSQL performance
- `database-redis-caching.md` - Redis caching patterns

#### 4. Infrastructure Skills
- `docker-compose-patterns.md` - Docker Compose best practices
- `kubernetes-deployment.md` - K8s deployment patterns
- `github-actions-ci.md` - CI/CD with GitHub Actions
- `terraform-infrastructure.md` - Infrastructure as Code

#### 5. Security Skills
- `security-secret-management.md` - Handling secrets securely
- `security-auth-patterns.md` - Authentication and authorization
- `security-input-validation.md` - Input validation and sanitization
- `security-trufflehog-scanning.md` - Secret scanning with TruffleHog

#### 6. gRPC and Microservices
- `grpc-protobuf-patterns.md` - Protocol Buffers and gRPC
- `microservices-saga-pattern.md` - Distributed transaction patterns
- `microservices-event-driven.md` - Event-driven architecture
- `microservices-api-gateway.md` - API Gateway patterns

#### 7. Frontend Skills
- `frontend-component-design.md` - Component design patterns
- `frontend-state-management.md` - State management strategies
- `frontend-form-validation.md` - Form validation patterns
- `frontend-accessibility.md` - Accessibility best practices

### Repository-Specific Skills

#### TicketRemaster Backend
- `ticketremaster-flask-service.md` - Flask service patterns
- `ticketremaster-database-models.md` - Database model conventions
- `ticketremaster-grpc-service.md` - gRPC service patterns
- `ticketremaster-orchestrator-flow.md` - Orchestrator saga patterns
- `ticketremaster-qr-encryption.md` - QR generation and verification
- `ticketremaster-error-handling.md` - Error handling patterns

#### TicketRemaster Frontend
- `ticketremaster-vue-components.md` - Vue component patterns
- `ticketremaster-api-integration.md` - API integration patterns
- `ticketremaster-state-management.md` - State management
- `ticketremaster-testing-playwright.md` - E2E testing with Playwright

#### DejaVista Chrome Extension
- `dejavista-extension-architecture.md` - Chrome extension patterns
- `dejavista-react-components.md` - React component patterns
- `dejavista-supabase-integration.md` - Supabase integration
- `dejavista-vercel-functions.md` - Serverless function patterns

## How to Use Skills

### For AI Agents

1. **Automatic Loading**: Skills are automatically loaded by AI agents when working in a repository
2. **Context-Aware**: Agents select relevant skills based on the task and repository
3. **Step-by-Step**: Follow skill instructions precisely for best results
4. **Cross-Reference**: Skills reference each other for related patterns

### For Developers

1. **Learning Resource**: Use skills to understand repository conventions
2. **Onboarding**: New team members can quickly learn patterns
3. **Reference**: Quick lookup for common tasks
4. **Consistency**: Ensure all code follows the same patterns

## Creating New Skills

### When to Create a Skill

- New technology stack introduced
- Complex pattern that needs documentation
- Repository-specific convention
- Common mistake or anti-pattern
- Best practice that should be followed

### Skill Creation Process

1. **Identify Pattern**: Document the pattern or convention
2. **Write Draft**: Create skill markdown following the template
3. **Add Examples**: Include concrete code examples
4. **Cross-Reference**: Link to related skills and documentation
5. **Test with Agent**: Verify AI agent follows the skill correctly
6. **Sync to Repos**: Deploy skill to all relevant repositories

### Skill Maintenance

- **Quarterly Review**: Check skills for outdated information
- **Update Examples**: Keep code examples current
- **Add Pitfalls**: Document new common mistakes
- **Sync Changes**: Propagate updates to all repositories

## Syncing Skills Across Repositories

### Source of Truth

- **Primary**: `.codeflicker/skills/` in workspace root
- **Secondary**: `source-repo-code/.github/skills/` for shared patterns
- **Tertiary**: Repository-specific `.github/skills/` folders

### Sync Process

1. **Update Source**: Make changes to skills in source location
2. **Run Sync Script**: `python sync_repos.py --skills`
3. **Verify Changes**: Check diff across repositories
4. **Commit Changes**: `git commit -m "chore: sync skills documentation"`

### New Repository Setup

When creating a new repository:

1. **Copy Base Skills**: Copy relevant skills from source
2. **Add Repository-Specific**: Create custom skills for repo patterns
3. **Register in agents.md**: Add repository to agents configuration
4. **Test with Agent**: Verify AI agent loads skills correctly

## Skill Categories

### By Technology

- **Python**: Flask, FastAPI, Django, SQLAlchemy, gRPC
- **JavaScript**: Vue, React, Node.js, Express, Vite
- **TypeScript**: Type safety, interfaces, generics
- **Database**: PostgreSQL, MySQL, Redis, MongoDB
- **Infrastructure**: Docker, Kubernetes, Terraform, GitHub Actions
- **Security**: Authentication, authorization, encryption, scanning

### By Complexity

- **Beginner**: Basic patterns and conventions
- **Intermediate**: Complex workflows and integrations
- **Advanced**: Distributed systems and optimization

### By Purpose

- **Development**: Day-to-day coding tasks
- **Testing**: Unit, integration, and E2E testing
- **Deployment**: CI/CD and infrastructure
- **Maintenance**: Debugging and troubleshooting

## References

- [GitHub Skills Documentation](https://docs.github.com/en/contributing/collaborating-with-github-docs/using-skills)
- [Cursor AI Documentation](https://docs.cursor.com/)
- [Claude Code Documentation](https://docs.anthropic.com/claude/code)
- [AI Agent Configuration](../agents.md)
