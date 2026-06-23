# Claude Code Skills (Global)

This directory contains shared skills available across all your Claude Code projects.

## Available Skills

| Skill | Description | Location |
|-------|-------------|----------|
| `brainstorming` | Explores user intent and design before implementation. | `brainstorming/` |
| `alpha-inspiration-design` | Style web projects in the Alpha Inspiration look and feel. | `alpha-inspiration-design/` |
| `document-consolidation` | Extract, categorize and archive documents (PDF, Word, etc.). | `document-consolidation/` |
| `executing-plans` | Execute implementation plans with batch checkpoints. | `executing-plans/` |
| `frontend-design` | Create production-grade, high-quality frontend interfaces. | `frontend-design/` |
| `receiving-code-review` | Process technical feedback with verification and rigor. | `receiving-code-review/` |
| `requesting-code-review` | Dispatch code-reviewer subagent to verify work. | `requesting-code-review/` |
| `writing-plans` | Design detailed implementation plans. | `writing-plans/` |
| `writing-skills` | Create and verify skills using TDD principles. | `writing-skills/` |
| `n8n-mcp-tools-expert` | Guide for using n8n-mcp MCP tools effectively. | `n8n-mcp-tools-expert/` |
| `n8n-workflow` | Analyze and explain n8n workflows from JSON files. | `n8n-workflow/` |
| `n8n-workflow-patterns` | Best practices for n8n workflow architecture. | `n8n-workflow-patterns/` |
| `n8n-node-configuration` | Detailed guidance for configuring n8n nodes. | `n8n-node-configuration/` |
| `n8n-validation-expert` | Interpret and fix n8n node/workflow validation errors. | `n8n-validation-expert/` |
| `n8n-code-javascript` | Write and fix JavaScript in n8n Code nodes. | `n8n-code-javascript/` |
| `n8n-code-python` | Write and fix Python in n8n Code nodes. | `n8n-code-python/` |
| `n8n-expression-syntax` | Fix and optimize n8n expression syntax. | `n8n-expression-syntax/` |
| `notebooklm` | Query Google NotebookLM source-grounded answers. | `notebooklm.md` |
| `linkedin-automation` | Automate LinkedIn posts via Rube MCP. | `linkedin-automation.md` |
| `skill-creator` | Guide for creating effective Claude skills. | `skill-creator.md` |
| `skill-share` | Create and share skills via Slack (Legacy). | `skill-share.md` |

## Skill Creator Tools

Located in `skill-creator-scripts/`:
- `init_skill.py`, `package_skill.py`, `quick_validate.py`

## Structure & Usage

Claude Code loads skills from `~/.claude/skills/` (Global) and `./.claude/skills/` (Local).
For new skills, use the directory-based structure with `SKILL.md`.
