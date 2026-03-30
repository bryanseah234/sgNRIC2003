---
name: mcp-tool-integration
description: Best practices for leveraging Model Context Protocol (MCP) servers and external tools
---

# MCP & Tool Integration

## When to Use
Apply this skill when the AI agent needs to interact with external services, databases, or specialized local tools that are not part of the standard built-in IDE capabilities.

## Core Principles
1. **Tool Over Emulation**: If an MCP tool exists for a task (e.g., executing a SQL query or searching GitHub), use the tool rather than trying to write a one-off python script to do it.
2. **Graceful Degradation**: If an MCP server is unavailable or fails, fallback to standard CLI tools or inform the user clearly.

## Key Tool Categories & Usage

### 1. Web and Documentation Context
- **Tool**: WebSearch / Exa / Context7
- **Usage**: When asked about a new library version or an unknown error code, immediately invoke the web search tool to pull in the latest documentation before guessing.
- **Pattern**: `Search query -> Read top 2 results -> Synthesize -> Implement`.

### 2. Deep Codebase Analysis (LSP/AST)
- **Tool**: Grep App / LSP Tools
- **Usage**: Use AST/LSP-aware tools to find *references* to a function, rather than relying on dumb text search which might return false positives in comments or unrelated files.

### 3. Session and History Tools
- **Usage**: When picking up a task from a previous session, use session-history tools to read the last few actions, errors, or summaries to re-establish context instantly.

### 4. Productivity Enforcers
Inspired by productivity loops (like Todo Enforcers or Comment Checkers):
- Before marking a task complete, the agent must autonomously invoke a tool (like `TodoWrite` or a linter) to verify that all checkboxes in the original request were met.
- **"Think Mode"**: Before writing complex code, write out the thought process in a `<thought>` or `// THINKING:` block to ensure logical consistency.

## References
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io)