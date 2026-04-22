# Skills Manifest

本仓库使用 `npx skills` 安装公开 skills，并将安装结果同步到其他仓库。

## 第一阶段必装 Skills

| 来源 | Skill | 用途 | 安装方式 |
|---|---|---|---|
| `vercel-labs/agent-skills` | `web-design-guidelines` | UI/UX、可访问性、前端审查 | project-level |
| `vercel-labs/agent-skills` | `vercel-react-best-practices` | React/Next.js 性能与最佳实践 | project-level |
| `vercel-labs/agent-skills` | `vercel-composition-patterns` | React 组件组合模式 | project-level |
| `vercel-labs/agent-skills` | `vercel-react-view-transitions` | React 视图过渡动画 | project-level |
| `rlespinasse/agent-skills` | `conventional-commit` | 规范 commit message | project-level |
| `rlespinasse/agent-skills` | `pin-github-actions` | GitHub Actions SHA 固定 | project-level |
| `rlespinasse/agent-skills` | `verify-pr-logs` | CI 日志诊断 | project-level |
| `rlespinasse/agent-skills` | `verify-readme-features` | README 与实现一致性核验 | project-level |
| `rlespinasse/agent-skills` | `diataxis` | 文档体系治理 | project-level |
| `mcp-use/skills` | `mcp-builder` | MCP server 设计与构建 | project-level |

## 目标 Agents

- `claude-code`
- `cursor`
- `cline`
- `codex`
- `github-copilot`
- `gemini-cli`

## 安装原则

- 一律在 `sourcerepo` 中 project-level 安装，不使用 `-g`
- 优先使用 `--copy`，避免 symlink 进入 Git
- 由本仓库保存安装结果，再同步到其他仓库

## 后续扩展

第二阶段再评估领域型技能，例如 Stitch、Base 等，仅在确有普适价值时纳入。
