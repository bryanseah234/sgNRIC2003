---
name: ai-agent-interaction
description: Rules and capabilities for AI Coding Agents operating within this workspace
---

# AI Agent Interaction Guidelines

## When to Use
This skill dictates how AI Coding Agents (such as Cursor, Trae, GitHub Copilot, Claude Code, etc.) should behave, read context, and modify code within any repository synced with `source-repo-code`.

## Core Principles
1. **Context First**: Agents must always search the codebase (`SearchCodebase`, `Grep`, `Glob`) to understand existing patterns before proposing or implementing changes.
2. **Minimal Invasiveness**: Prefer editing existing files (`SearchReplace`) over creating new ones. Do not delete files without explicit user permission.
3. **Proactive Verification**: Whenever code is changed, the agent should attempt to verify the change (e.g., running tests, type checking, or building) if the tools are available.

## Step-by-Step Execution Patterns

### 1. Task Management
- For any task requiring more than 2 steps, agents must use a Todo or Task management tool to outline the plan.
- Update the status of tasks (`in_progress`, `completed`) in real-time.

### 2. File Operations
- **Reading**: Use line limits when reading large files. Do not dump thousands of lines into context unnecessarily.
- **Writing**: Use surgical search-and-replace tools rather than overwriting entire files, to avoid accidentally stripping out unread code.
- **Documentation**: **NEVER** proactively create `.md` or `README.md` files unless the user explicitly requests it. Always update existing documentation instead.

### 3. Executing Commands
- Always ensure commands are cross-platform compatible or specifically tailored to the user's OS (e.g., using PowerShell syntax on Windows).
- Use non-blocking execution for long-running processes (like dev servers).
- Never run interactive commands that require manual CLI input from the user unless strictly necessary.

### 4. Following Repository Rules
- Agents must adhere to the `AGENTS.md` file located at the root of the repository.
- Agents must look for and follow framework-specific skills located in `.github/skills/` (e.g., `vue3-composition`, `flask-api`).

## References
- [Cursor Documentation](https://docs.cursor.com/)
- `AGENTS.md` (Root of the repository)