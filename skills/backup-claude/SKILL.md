---
name: backup-claude
description: |
  Backup meiner Claude‑Code‑Daten, Claude‑Einstellungen sichern, Claude‑Daten nach OneDrive exportieren, MCP‑Server‑Konfiguration sichern.
  Trigger‑Phrasen: "Backup meiner Claude‑Code‑Daten", "Claude‑Einstellungen sichern", "Claude‑Daten nach OneDrive exportieren", "MCP‑Server‑Konfiguration sichern".
  Optionales Argument `target` ermöglicht das Angeben eines alternativen Ziel‑Verzeichnisses, z. B. `backup-claude target=D:\MeinBackup\Claude`.
---

# Backup‑Claude‑Skill

<!-- TODO: Bei Bedarf weitere Optionen hinzufügen (z. B. Ausschluss‑/Einbeziehungs‑Muster) -->

Dieses Skill führt das PowerShell‑Skript `backup_claude.ps1` aus, das das komplette Verzeichnis `~/.claude` (inkl. Plugins, Skills, MCP‑Server‑Konfiguration) in ein ZIP‑Archiv packt und im Ziel‑Ordner speichert.

**Ausführung**

```bash
powershell -ExecutionPolicy Bypass -File C:\Users\walte\.claude\scripts\backup_claude.ps1
```

Falls ein alternatives Ziel angegeben wird, wird das Skript über das Argument `target` auf das PowerShell‑Skript weitergeleitet (das Skript kann bei Bedarf angepasst werden).
