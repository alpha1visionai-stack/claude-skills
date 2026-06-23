# Skill-Referenz

> Diese Datei enthält technisches Hintergrundwissen über Claude Code Skills.
> Der Skill Builder greift bei Bedarf darauf zu, damit er nicht jedes Mal das Web durchsuchen muss.

## Frontmatter-Optionen (YAML-Header)

| Feld | Pflicht | Beschreibung |
|---|---|---|
| `name` | Ja | Skill-Name (Kleinbuchstaben, Bindestriche) |
| `description` | Ja | Was der Skill tut + wann er genutzt wird |
| `user-invocable` | Nein | `true` = per /slash-command aufrufbar |
| `model-invocable` | Nein | `false` = NUR per Slash-Command, nicht automatisch |
| `allowed-tools` | Nein | Welche Tools der Skill nutzen darf |
| `agent` | Nein | Dedizierter Sub-Agent für den Skill |

## Progressive Context Loading

So entscheidet Claude, welchen Skill er lädt:

**Level 1 – Scan**: Nur `name` und `description` werden gelesen (~100 Tokens). Passiert bei JEDER Anfrage.
**Level 2 – Match**: Wenn der Skill passt, wird die komplette SKILL.md gelesen (~1.000-3.000 Tokens).
**Level 3 – Referenzen**: Nur wenn die Aufgabe es erfordert, werden Dateien aus `references/` oder `scripts/` geladen.

→ Das bedeutet: Die `description` muss perfekt sein, weil sie der einzige Filter ist.

## Skill-Speicherorte

```
~/.claude/skills/         → Global: Funktioniert überall
.claude/skills/           → Projekt-lokal: Nur in diesem Ordner
```

Globale Skills eignen sich für: Schreibstil, Firmenkontext, persönliche Workflows.
Lokale Skills eignen sich für: Projektspezifische Aufgaben, Team-Skills.

## Symlinks erstellen

Skill lokal entwickeln, global verfügbar machen:
```bash
# Linux/Mac
ln -sf /pfad/zu/skills/skill-name ~/.claude/skills/skill-name

# Windows (PowerShell als Admin)
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\skills\skill-name" -Target "C:\pfad\zu\skills\skill-name"
```

## Typische Skill-Größen

| Typ | Zeilen | Beispiel |
|---|---|---|
| Einfach | 30-80 | Schreibstil-Checker, Format-Konverter |
| Mittel | 80-200 | Content-Ersteller, Recherche-Skill |
| Komplex | 200-500 | Orchestrator (ruft andere Skills auf), Multi-Step-Workflows |

## Häufige Fehler

1. **Description zu vage** → Skill wird nie gefunden
2. **Zu viele Schritte in einer SKILL.md** → KI verliert Fokus
3. **Keine Beispiele** → Inkonsistente Ergebnisse
4. **Alles in einem Skill** → Lieber aufteilen
5. **Referenzdateien nicht verlinkt** → KI weiß nicht dass sie existieren
