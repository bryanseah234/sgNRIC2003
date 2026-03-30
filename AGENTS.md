---
description: Central configuration and documentation for all AI coding agents across repositories
---

# AI Agents Configuration

This file defines how AI coding agents (Cursor, Antigravity, Claude Code, GitHub Copilot, etc.) should behave across all repositories in this workspace.

## Agent Types and Roles

### 1. Primary Coding Agent (Cursor/Claude Code)
**Purpose**: Main development assistant for code changes
**Capabilities**: Full codebase access, file editing, terminal commands
**Behavior**: Follows all conventions in this file

### 2. Review Agent (GitHub PR Review)
**Purpose**: Automated code review on pull requests
**Capabilities**: Read-only access to PR changes
**Behavior**: Strict adherence to coding standards

### 3. Documentation Agent
**Purpose**: Maintains and updates documentation
**Capabilities**: Can modify markdown files
**Behavior**: Never creates new docs without explicit request

### 4. Security Agent (TruffleHog, CodeQL)
**Purpose**: Security scanning and vulnerability detection
**Capabilities**: Full codebase scan
**Behavior**: Blocks PRs on security issues

## Universal Rules (Apply to All Agents)

### 1. File Operations
- **NEVER** create new markdown files without explicit user request
- **ALWAYS** update existing documentation when possible
- **NEVER** delete files without confirmation
- **ALWAYS** preserve file history and git history

### 2. Code Style
- Follow language-specific conventions (see skill files)
- Use consistent naming patterns
- Keep functions small and focused
- Add type hints for Python, TypeScript interfaces for JS

### 3. Git Conventions
- Commit messages: `type: description`
- Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `perf`, `style`
- Keep commits atomic and focused
- Never force push to main branches

### 4. Communication
- Be concise and direct
- Explain complex changes briefly
- Admit uncertainty when present
- Ask for clarification when requirements are ambiguous

## Repository-Specific Overrides

### source-repo-code (Template/Source)
- **Purpose**: Source of truth for shared configurations
- **Special Rules**: Changes here should be synced to all repos

## Skill System

Skills are modular documentation files that teach agents specific patterns for each repository. They are located in `.github/skills/` folders.

### Available Skills
1. **flask-service**: REST endpoint patterns
2. **database-models**: SQLAlchemy and migration conventions
3. **grpc-service**: gRPC proto and stub management
4. **orchestrator-flow**: Saga pattern and multi-step flows
5. **qr-encryption**: QR generation and verification
6. **error-handling**: Error response patterns
7. **vercel-deployment**: Vercel configuration and edge function patterns
8. **shell-scripting**: Bash, sh, and PowerShell best practices
9. **ai-agent-interaction**: Guidelines for AI Coding Agents
10. **git-best-practices**: Universal Git workflows, Conventional Commits, and branch management
11. **clean-code-principles**: Language-agnostic principles for writing maintainable code
12. **multi-agent-orchestration**: Delegating tasks to specialized sub-agents (Explorer, Oracle, Designer, Builder)
13. **mcp-tool-integration**: Best practices for using Model Context Protocol (MCP) servers and external tools

### Skill Format
Each skill file follows this structure:
```markdown
---
name: skill-name
description: Brief description of what this skill teaches
---

# Skill Title

## When to Use
[Context for when this skill applies]

## Step-by-Step
[Detailed instructions with code examples]

## References
[Links to related documentation]
```

## Agent Workflows

Agent workflows are step-by-step instructions for common tasks. They are located in `.agents/workflows/` folders.

### Available Workflows
- **start-backend.md**: How to start the ticketremaster-b backend stack
- **system.md**: DejaVista system initialization
- **standard-pr-process.md**: Standard process for creating, reviewing, and merging Pull Requests

### Workflow Format
```markdown
---
description: Brief description of the workflow
---

// workflow-command-or-tag

## Steps
1. [Step-by-step instructions]
2. [Include verification steps]
3. [Include troubleshooting if needed]
```

## Syncing Strategy

### Source of Truth
- **Primary**: `source-repo-code` repository for shared configurations (`agents.md`, `.github/skills/`, `.agents/workflows/`)
- **Secondary**: Individual repository overrides

### Sync Process
1. Changes to shared configurations should be made in `source-repo-code`
2. Pushing to `main` in `source-repo-code` will trigger a GitHub Action to propagate changes to all repositories
3. The sync workflow automatically updates all configuration files across the workspace

### New Repository Setup
When creating a new repository:
1. Copy `.github/skills/` from `source-repo-code`
2. Copy `.agents/workflows/` if applicable
3. Add repository-specific overrides if needed
4. Run sync verification

## Maintenance

### Quarterly Reviews
- Review and update skill files
- Check for outdated action versions
- Verify agent behavior consistency
- Update this configuration as needed

### Automated Monitoring
- Use Dependabot for dependency updates
- Use TruffleHog for secret scanning
- Use custom scripts to detect outdated GitHub Actions

## Troubleshooting

### Agent Not Following Conventions
1. Check repository-specific overrides in this file
2. Verify skill files are present and up-to-date
3. Review recent changes to conventions
4. Re-sync configurations from source

### Sync Failures
1. Run sync script with `--dry-run` flag
2. Check for git conflicts in target repositories
3. Verify file permissions
4. Review sync logs for specific errors

## References

- [GitHub Skills Documentation](https://docs.github.com/en/contributing/collaborating-with-github-docs/using-skills)
- [Cursor AI Documentation](https://docs.cursor.com/)
- [Claude Code Documentation](https://docs.anthropic.com/claude/code)
- [Dependabot Configuration](https://docs.github.com/en/code-security/dependabot)
