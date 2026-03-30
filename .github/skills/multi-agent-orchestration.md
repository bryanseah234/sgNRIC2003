---
name: multi-agent-orchestration
description: Guidelines for orchestrating multiple specialized AI sub-agents to complete complex tasks
---

# Multi-Agent Orchestration

## When to Use
Apply these patterns when an AI agent needs to delegate complex, multi-step, or specialized tasks (like deep research, architectural design, or background processing) to other specialized sub-agents. Inspired by frameworks like "oh-my-openagent" (formerly oh-my-opencode).

## Core Principles
1. **Separation of Concerns**: Do not rely on one monolithic agent to do everything. Delegate to specialized sub-agents (e.g., Explorer, Oracle, Designer, Builder).
2. **Context Persistence**: Ensure long-term context is retained across sessions or sub-agent handoffs.
3. **Async Delegation**: Use background processes for long-running tasks like deep codebase scans or test suite executions, allowing the main agent to remain responsive.

## Step-by-Step Patterns

### 1. The Sub-Agent Roles
When breaking down a task, classify the required work into these roles:
- **Explorer**: Analyzes the current codebase structure, reads files, and builds a map of dependencies.
- **Oracle / Librarian**: Searches external documentation, reads `AGENTS.md` and `.github/skills/`, and retrieves required knowledge (e.g., via WebSearch or Docs MCP).
- **Designer**: Proposes the architectural changes, API contracts, and data structures.
- **Builder**: Executes the code changes based on the Designer's plan.

### 2. Task Handoff Protocol
When delegating from one role/agent to another, always provide a "Handoff Summary":
1. **Goal**: What the sub-agent needs to achieve.
2. **Context**: Relevant files, gathered knowledge, and constraints.
3. **Expected Output**: Exactly what the sub-agent must return (e.g., a specific file edit, a JSON schema, a test report).

### 3. Background Task Management
For tasks that take significant time (running test suites, compiling builds):
- Do not block the main conversation thread.
- Spawn a background terminal/process.
- Implement a "Ralph Loop" or monitoring loop to periodically check the status of the background task and report back only when completed or failed.

### 4. Memory and Context Retention
- Summarize findings into project-level memory or specific markdown files (e.g., `.code-context.md`) rather than keeping them exclusively in the short-term chat history.
- When starting a new feature, explicitly instruct the agent to "Read previous architectural decisions from `.github/skills/` and past PR summaries."

## References
- `ai-agent-interaction.md`
- [oh-my-openagent concepts](https://github.com/code-yeongyu/oh-my-openagent)