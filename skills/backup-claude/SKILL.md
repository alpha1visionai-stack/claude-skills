---
name: backup-Codex
description: |
  Backup meiner Codex‑Code‑Daten, Codex‑Einstellungen sichern, Codex‑Daten nach OneDrive exportieren, MCP‑Server‑Konfiguration sichern.
  Trigger‑Phrasen: "Backup meiner Codex‑Code‑Daten", "Codex‑Einstellungen sichern", "Codex‑Daten nach OneDrive exportieren", "MCP‑Server‑Konfiguration sichern".
  Optionales Argument `target` ermöglicht das Angeben eines alternativen Ziel‑Verzeichnisses, z. B. `backup-Codex target=D:\MeinBackup\Codex`.
---

# Backup‑Codex‑Skill

<!-- TODO: Bei Bedarf weitere Optionen hinzufügen (z. B. Ausschluss‑/Einbeziehungs‑Muster) -->

Dieses Skill führt das PowerShell‑Skript `backup_claude.ps1` aus, das das komplette Verzeichnis `~/.Codex` (inkl. Plugins, Skills, MCP‑Server‑Konfiguration) in ein ZIP‑Archiv packt und im Ziel‑Ordner speichert.

**Ausführung**

```bash
powershell -ExecutionPolicy Bypass -File C:\Users\walte\.Codex\scripts\backup_claude.ps1
```

Falls ein alternatives Ziel angegeben wird, wird das Skript über das Argument `target` auf das PowerShell‑Skript weitergeleitet (das Skript kann bei Bedarf angepasst werden).
