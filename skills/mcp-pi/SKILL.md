---
name: mcp-pi
description: Use when the user wants to set up, configure, or use MCP (Model Context Protocol) servers inside PI.dev. Triggers on phrases like "MCP in PI", "MCP-Server hinzufügen", "MCP-Bridge", "MCP konfigurieren", "MCP server starten", or when adding tools from MCP servers to a PI session. Do NOT use for general web search or HTTP — that's the webfetch/websearch tools from the webfetch extension.
---

# MCP in PI.dev

PI hat **keinen nativen MCP-Support** — er wird absichtlich weggelassen (siehe `docs/usage.md`). Die `mcp-bridge.ts` Extension schließt diese Lücke, indem sie MCP-Server als Subprozesse startet und ihre Tools als native PI-Tools registriert.

## Schnellstart

### 1. Extension installieren (bereits geschehen)
```powershell
Copy-Item "C:\Users\walte\AppData\Roaming\npm\node_modules\@earendil-works\pi-coding-agent\examples\extensions\permission-gate.ts" "C:\Users\walte\.pi\agent\extensions\"
Copy-Item "C:\Users\walte\AppData\Roaming\npm\node_modules\@earendil-works\pi-coding-agent\examples\extensions\protected-paths.ts" "C:\Users\walte\.pi\agent\extensions\"
# plus webfetch.ts und mcp-bridge.ts (custom)
```

### 2. MCP-Server konfigurieren

`C:\Users\walte\.pi\agent\mcp_servers.json`:

```json
{
  "filesystem": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:/Users/walte/dokumentation"],
    "env": {}
  },
  "github": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-github"],
    "env": { "GITHUB_TOKEN": "ghp_..." }
  }
}
```

Hinweise:
- Schlüssel mit führendem `_` werden ignoriert (für Kommentare/Beispiele).
- Server werden beim PI-Start geladen.
- Jedes MCP-Tool wird als `mcp_<servername>_<toolname>` registriert.

### 3. Pi starten / reload
```
/reload
```
Beim `session_start` zeigt eine Notification, wieviele Server geladen wurden.

## Was die mcp-bridge kann

| Feature | Status |
|---|---|
| MCP-Server via stdio (JSON-RPC) | ✅ |
| Auto-discovery aus `mcp_servers.json` | ✅ |
| Tools als native PI-Tools | ✅ |
| Multi-Server parallel | ✅ |
| Tool-Aufrufe weiterleiten | ✅ |
| Auth via env vars | ✅ |
| Auto-Reconnect bei Server-Crash | ❌ (Neustart von PI nötig) |
| Sampling/Roots/Prompts | ❌ (nur tools) |

## Bekannte MCP-Server

| Server | Zweck | Paket |
|---|---|---|
| Filesystem | Dateien lesen/schreiben mit Sandbox-Pfaden | `@modelcontextprotocol/server-filesystem` |
| GitHub | Issues, PRs, Repos | `@modelcontextprotocol/server-github` |
| Brave Search | Web-Suche mit API-Key | `@modelcontextprotocol/server-brave-search` |
| SQLite | SQL-Datenbanken abfragen | `@modelcontextprotocol/server-sqlite` |
| Postgres | PostgreSQL-Datenbanken | `@modelcontextprotocol/server-postgres` |
| Puppeteer | Browser-Automation | `@modelcontextprotocol/server-puppeteer` |
| Memory | Knowledge-Graph (persistent) | `@modelcontextprotocol/server-memory` |

Offizielle Liste: https://github.com/modelcontextprotocol/servers

## Troubleshooting

**Server startet nicht:**
- Prüfe `command` und Pfad — `npx -y <paket>` funktioniert in der Regel
- Console zeigt `[mcp-bridge] Failed to start server 'xyz'`
- Test manuell: `npx -y @modelcontextprotocol/server-filesystem C:/temp`

**Tool nicht sichtbar:**
- Tools heißen `mcp_<server>_<tool>`, z. B. `mcp_filesystem_read_file`
- `/tools` zeigt alle verfügbaren Tools

**Authentifizierung:**
- Tokens kommen aus `env`-Block in `mcp_servers.json`
- NIEMALS Token in die Config hardcoden und in git committen
- Besser: aus Environment-Variable laden via `"env": { "GITHUB_TOKEN": "${env:GITHUB_TOKEN}" }` (TODO: mcp-bridge unterstützt das noch nicht)

## Architektur

```
┌──────────────┐    JSON-RPC    ┌──────────────────┐
│  PI Session  │◄──────────────►│  MCP Server #1   │
│              │   (stdio)      │  (filesystem)    │
│  mcp-bridge  │                └──────────────────┘
│  .ts         │    JSON-RPC    ┌──────────────────┐
│              │◄──────────────►│  MCP Server #2   │
│              │   (stdio)      │  (github)        │
└──────────────┘                └──────────────────┘

Tools werden mit Praefix mcp_<server>_<tool> registriert,
damit keine Namenskollisionen mit nativen PI-Tools entstehen.
```
