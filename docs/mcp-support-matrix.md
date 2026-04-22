# MCP Support Matrix

本阶段策略：先传播 MCP 配置模板与说明文档，不承诺所有 IDE / Agent 都会自动读取同一份配置。

## 目标

- 让每个项目仓库拥有统一的 MCP 配置模板
- 为未来按 agent 分化配置预留位置
- 避免把 MCP 和 Skills 强耦合

## 支持策略

| Agent / IDE | 项目级配置 | 当前策略 | 说明 |
|---|---|---|---|
| Claude Code | 部分支持，需按实际版本确认 | 文档 + 预留模板 | 后续单独验证 |
| Cursor | 常见为项目级配置/本地规则配合 | 文档 + 预留模板 | 需以实际产品行为验证 |
| Cline | 常见支持项目级配置 | 文档 + 预留模板 | 后续增加示例 |
| Codex / GitHub Copilot / Gemini CLI | 行为不完全一致 | 仅记录支持矩阵 | 暂不强制同步单一文件 |

## 推荐目录策略

- `docs/mcp-support-matrix.md`：说明支持状态
- `templates/mcp/`：未来存放按 agent 分类的模板

## 第一阶段结论

- 先把 MCP 相关同步独立为单独 workflow
- 先同步文档与模板目录
- 等验证具体 agent 行为后，再把对应模板加入默认传播范围
