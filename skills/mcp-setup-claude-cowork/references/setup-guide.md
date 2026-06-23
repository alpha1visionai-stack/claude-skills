# MCP Setup for Claude CoWork (Windows MSIX)

## Config Reference
The Claude Desktop (MSIX/3P) configuration is located at:
`C:\Users\walte\AppData\Local\Claude-3p\claude_desktop_config.json`

### Template Structure
```json
{
  "mcpServers": {
    "server-name": {
      "command": "C:\\Program Files\\nodejs\\node.exe",
      "args": [
        "C:\\absolute\\path\\to\\entrypoint.js"
      ],
      "env": {
        "KEY": "VALUE"
      }
    }
  }
}
```

## Patching Rules
To prevent `stdout` corruption (which crashes the MCP connection), all non-JSON output MUST be redirected to `stderr`.

### Patterns
1. **console.log replacement:**
   Search for `console.log` and replace with `console.error` in the entry point and dependencies.
2. **Third-party noise:**
   For libraries like `dotenv`, use `DOTENVX_QUIET=1` or patch the source to suppress startup banners.

## Verification Workflow
1. **Check Entry Point:** Verify the file exists at the absolute path.
2. **Isolated Test:** Run the server manually in PowerShell with env vars:
   ```powershell
   $env:VAR="VAL"; node "C:\path\to\index.js"
   ```
   Ensure no "junk" (symbols, banners) appears before the first JSON-RPC message.
3. **Chat-ID (Telegram):** For bots, use an echo-loop script to capture the user's numeric Chat-ID.
