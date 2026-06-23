---
name: mcp-setup-claude-cowork
description: Workflow for installing, patching, and stabilizing MCP servers on Windows (Claude Desktop 3P/MSIX). Use when adding new tools like Telegram, Gmail, or Playwright to Claude.
---

# MCP Setup Claude CoWork

This skill provides a specialized workflow for managing MCP servers in the Windows MSIX environment of Claude Desktop.

## Core Mandates
- **Absolute Paths Only:** Never use relative paths or short names (like `node`). Always use full paths (e.g., `C:\Program Files\nodejs\node.exe`).
- **Stdout Purity:** Ensure the MCP server output is pure JSON. Any logging must go to `stderr`.

## Workflow

### 1. Research & Installation
- Locate the npm package entry point (usually `dist/index.js` or `cli.js`).
- Identify required environment variables (API keys, tokens).

### 2. Stabilization (Patching)
- **Log Redirect:** If the server logs to `stdout`, patch it using `replace` to use `console.error`.
- **Suppress Noise:** Set `DOTENVX_QUIET=1` for servers using dotenv-expand or similar to avoid startup banners.

### 3. Configuration
- Update `C:\Users\walte\AppData\Local\Claude-3p\claude_desktop_config.json`.
- Use the structure defined in [setup-guide.md](references/setup-guide.md).

### 4. Verification
- Test the server logic in isolation via PowerShell.
- For interactive services (like Telegram), verify connectivity and retrieve necessary IDs (e.g., Chat-ID).

## Resources
- [Setup Guide](references/setup-guide.md): Detailed configuration and patching patterns.
