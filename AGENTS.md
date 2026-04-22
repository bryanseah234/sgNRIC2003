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

Skills 是由 `npx skills` 工具安装的 Agent Skills，用于向 Agent 传授特定模式的指令。在 sourcerepo 中以 project-level 方式安装，并同步到所有项目仓库。

### 安装来源

Skills 通过 `npx skills add` 从公开仓库安装，支持 Claude Code、Cursor、Cline、Codex、GitHub Copilot、Gemini CLI 等多个 Agent。完整清单与命令参见仓库中的 [`docs/skills-manifest.md`](<kfile name="skills-manifest.md" path="docs/skills-manifest.md">docs/skills-manifest.md</kfile>)。

### 项目级 Skills 目录

- `.agents/skills/`：通用 project-level skills（适合 Cursor/Cline/Codex/GitHub Copilot/OpenCode 等广泛兼容）
- `.claude/skills/`：Claude Code 专属项目级目录

### MCP 配置

MCP（Model Context Protocol）配置模板与支持策略见 [`docs/mcp-support-matrix.md`](<kfile name="mcp-support-matrix.md" path="docs/mcp-support-matrix.md">docs/mcp-support-matrix.md</kfile>)。当前阶段以文档与模板传播为主，不承诺所有 IDE/Agent 自动读取同一文件。

## Syncing Strategy

### Source of Truth
- **Primary**: sourcerepo 仓库作为唯一真源（Skills、MCP、通用配置、仓库设置）
- **Secondary**: 目标仓库保留仓库特定覆盖（需在 sync 后自行维护）

### Sync Workflows
- **Skills 同步**：[`sync-skills.yml`](<kfile name="sync-skills.yml" path=".github/workflows/sync-skills.yml">.github/workflows/sync-skills.yml</kfile>) 负责传播 `.agents/skills/`、`.claude/skills/` 和 `docs/skills-manifest.md`
- **MCP 同步**：[`sync-mcp.yml`](<kfile name="sync-mcp.yml" path=".github/workflows/sync-mcp.yml">.github/workflows/sync-mcp.yml</kfile>) 负责传播 MCP 模板与支持文档
- **仓库设置与通用配置**：[`sync-repo-settings.yml`](<kfile name="sync-repo-settings.yml" path=".github/workflows/sync-repo-settings.yml">.github/workflows/sync-repo-settings.yml</kfile>) 负责传播 GitHub Actions、Dependabot、labels、`AGENTS.md` 等

### Sync Process
1. 在 sourcerepo 中修改 Skills、MCP 或通用配置
2. 推送到 `main` 分支自动触发相应 workflow
3. workflow 会遍历所有非 archive/fork 仓库，复制变更并提交/开 PR
4. 定时任务每日/每日执行，覆盖未来新仓库

### New Repository Setup
当创建新仓库时：
1. 将 sourcerepo 中的配置同步过去（由定时任务或手动触发完成）
2. 如需仓库特定覆盖，同步后手动维护
3. Skills 已通过同步自动到位，无需手动安装

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
1. 检查仓库特定覆盖在 AGENTS.md 中
2. 验证 `.agents/skills/` 与 `.claude/skills/` 中的 skills 文件存在且最新
3. 审阅近期约定变更
4. 从源重新同步配置

### Sync Failures
1. 使用相应 workflow 的 `workflow_dispatch` 手动触发以观察日志
2. 检查目标仓库中的 git 冲突
3. 验证文件权限
4. 查看同步日志中的具体错误

## References

- [GitHub Skills Documentation](https://docs.github.com/en/contributing/collaborating-with-github-docs/using-skills)
- [Cursor AI Documentation](https://docs.cursor.com/)
- [Claude Code Documentation](https://docs.anthropic.com/claude/code)
- [Dependabot Configuration](https://docs.github.com/en/code-security/dependabot)
