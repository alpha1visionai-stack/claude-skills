---
name: skill-manager
description: Use when the user asks to MANAGE the existing skill system ("liste alle skills", "audit skills", "junction pruefen", "skills verlinken", "skill-system verwalten", "link skills", "symlink anlegen", "show skill structure") OR asks about the cross-agent skill governance protocol. Do NOT use for the act of creating a new skill's content â€” that is the skill-creator's job.
---

# Skill-Manager â€” Protokoll

## Single Source of Truth

**Canonical Store:** `C:\Users\walte\.agents\skills\`

| Agent | Sicht | Mechanismus |
|---|---|---|
| PI              | direkt | liest `.agents/skills/` |
| Claude Code     | via Junction | `.claude/skills/` â†’ `.agents/skills/` |
| Codex           | per Skill | `.codex/skills/<name>` â†’ Symlink |
| Antigravity     | per Skill | `.antigravity/skills/<name>` â†’ Symlink |

**Andere Skill-Ordner sind Sichten, keine Speicherorte.** Niemals direkt reinschreiben.

## Erstellen â€” Schritt fÃ¼r Schritt

### 1. Skill-Name bestimmen
- kebab-case, eindeutig, prÃ¤gnant
- Beispiele: `pdf-extractor`, `n8n-workflow-patterns`

### 2. Verzeichnis + SKILL.md schreiben
```
C:\Users\walte\.agents\skills\<name>\
   SKILL.md          â† Pflicht
   (weitere Assets)  â† optional
```

### 3. Frontmatter (verbindlich)
```markdown
---
name: <name>
description: Use when the user asks to MANAGE the existing skill system ("liste alle skills", "audit skills", "junction pruefen", "skills verlinken", "skill-system verwalten", "link skills", "symlink anlegen", "show skill structure") OR asks about the cross-agent skill governance protocol. Do NOT use for the act of creating a new skill's content â€” that is the skill-creator's job.
---

# <Titel>

<Inhalt>
```

Wichtig:
- `description` MUSS mit "Use when" oder "Trigger when" beginnen
- Trigger mÃ¼ssen **prÃ¤zise** und **exklusiv** sein (keine Konflikte mit anderen Skills)
- Auf negativen Abgrenzungen ("Nicht fÃ¼r X, Y") achten

### 4. Sichtbarkeit erweitern (optional)
Nur falls der Skill auch fÃ¼r Codex/Antigravity gewÃ¼nscht ist, **Per-Skill-Symlink** anlegen:

```powershell
# Codex
New-Item -ItemType SymbolicLink `
  -Path "C:\Users\walte\.codex\skills\<name>" `
  -Target "C:\Users\walte\.agents\skills\<name>"

# Antigravity
New-Item -ItemType SymbolicLink `
  -Path "C:\Users\walte\.antigravity\skills\<name>" `
  -Target "C:\Users\walte\.agents\skills\<name>"
```

**Claude Code braucht keinen Symlink** â€” Junction zeigt bereits auf den Store.

### 5. Audit
```powershell
pwsh C:\Users\walte\.agents\hooks\audit-skills.ps1
```

## NIEMALS

- âŒ Direkt nach `.claude/skills/<name>/` schreiben (Junction, wÃ¼rde sie verstummen lassen)
- âŒ Direkt nach `.codex/skills/<name>/` schreiben (auÃŸer Symlink-Setup)
- âŒ Direkt nach `.antigravity/skills/<name>/` schreiben (auÃŸer Symlink-Setup)
- âŒ Skill ohne prÃ¤zise `description` anlegen
- âŒ Skill mit `description` anlegen, die andere Skills Ã¼berlappt

## Audit-Outputs verstehen

| Status | Bedeutung | Aktion |
|---|---|---|
| `[OK] .claude/skills ist eine Junction` | Struktur intakt | â€” |
| `[OK-SYMLINK]` | Per-Skill-Symlink korrekt | â€” |
| `[ORPHAN]` in Codex/Antigravity | Skill dort, aber nicht im Store | Symlink prÃ¼fen oder lÃ¶schen |
| `[FAIL] .claude/skills ist KEINE Junction` | Drift | `setup-junction.ps1` neu ausfÃ¼hren |
| `[FAIL] Store-Skills fehlen via Junction` | Junction kaputt | `setup-junction.ps1` neu ausfÃ¼hren |

## Hook-Verhalten (Claude Code)

`C:\Users\walte\.claude\settings.json` enthÃ¤lt einen PreToolUse-Hook, der Writes nach
`.codex/skills/` oder `.antigravity/skills/` blockiert mit Exit-Code 2.
Writes in den canonical store via Junction (`.claude/skills/`) sind erlaubt und
landen korrekt im Store.

## Wenn der User "erstelle einen Skill fÃ¼r X" sagt

1. Skill-Name ableiten
2. `C:\Users\walte\.agents\skills\<name>\SKILL.md` mit Frontmatter schreiben
3. Trigger prÃ¼fen â€” keine Konflikte mit anderen Skills
4. Falls Sichtbarkeit erweitert werden soll: Symlinks anlegen
5. `audit-skills.ps1` laufen lassen und Ergebnis zeigen
6. Skill ausgeben mit Pfad und "Use when â€¦"-Trigger

