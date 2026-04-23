# Skills Manifest

本仓库使用 `npx skills` 安装公开 skills，并将安装结果同步到所有项目仓库。

## 已安装 Skills 来源（全量）

| 来源仓库 | 已安装技能数 | 主要类别 |
|---|---|---|
| `vercel-labs/agent-skills` | 5 | React/Vercel 最佳实践 |
| `rlespinasse/agent-skills` | 5 | Git 工作流、CI/CD |
| `anthropics/skills` | 15+ | Claude API、文档、设计 |
| `supabase/agent-skills` | 2 | Supabase/Postgres |
| `microsoft/azure-skills` | 25+ | Azure 全栈服务 |
| `JuliusBrussee/caveman` | 6 | Caveman 编码规范 |
| `JuliusBrussee/cavekit` | 4 | Spec/Build/Check/Backprop |
| `softaworks/agent-toolkit` | 40+ | 开发工具、生产力 |
| `inference-sh/skills` | 60+ | AI/媒体生成、工具链 |
| `shadcn/ui` | 1 | shadcn 组件 |
| `mcp-use/skills` | 1 | MCP Builder |

**总计：175+ skills**

## 目标 Agents（全覆盖）

已针对以下 agents 执行安装：

`amp`, `antigravity`, `cline`, `codex`, `cursor`, `deepagents`, `firebender`, `gemini-cli`, `github-copilot`, `kimi-cli`, `opencode`, `warp`, `bob`, `claude-code`, `openclaw`, `codebuddy`, `command-code`, `continue`, `cortex`, `crush`, `droid`, `goose`, `junie`, `iflow-cli`, `kilo`, `kiro-cli`, `kode`, `mcpjam`, `mistral-vibe`, `mux`, `openhands`, `pi`, `qoder`, `qwen-code`, `roo`, `trae`, `trae-cn`, `windsurf`, `zencoder`, `neovate`, `pochi`, `adal`, `augment`

## 安装原则

- 一律在 `sourcerepo` 中 project-level 安装，不使用 `-g`
- 优先使用 `--copy`，避免 symlink 进入 Git
- 由本仓库保存安装结果，再同步到其他仓库
- 不只同步 `.agents/skills/` 与 `.claude/skills/`，还同步 `npx skills add` 实际生成的根目录 `skills/`、`skills-lock.json` 与 agent 专属目录
- 对目标仓库中可能被 `.gitignore` 忽略的 skills 路径，sync 脚本使用强制暂存以确保这些目录和文件仍可被提交

## 多 Agent 同步范围

当前纳入同步的 skills 相关路径包括：

- `.agents/skills/`
- `.claude/skills/`
- `skills/`
- `skills-lock.json`
- `.adal/`
- `.augment/`
- `.bob/`
- `.codebuddy/`
- `.commandcode/`
- `.factory/`
- `.continue/`
- `.cortex/`
- `.crush/`
- `.goose/`
- `.iflow/`
- `.junie/`
- `.kilocode/`
- `.kiro/`
- `.kode/`
- `.mcpjam/`
- `.mux/`
- `.neovate/`
- `.openhands/`
- `.pi/`
- `.pochi/`
- `.qoder/`
- `.qwen/`
- `.roo/`
- `.trae/`
- `.vibe/`
- `.windsurf/`
- `.zencoder/`

## 同步触发

- 每 3 小时自动同步
- 手动触发：`workflow_dispatch`
- 推送触发：skills 相关文件变更时
