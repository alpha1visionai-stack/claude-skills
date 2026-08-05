---
name: luminar-preset-converter
description: >
  Durchsucht das aktuelle Projektverzeichnis oder einen angegebenen Ordner nach alten Luminar *.lmp Preset-Dateien (XML Plist) und konvertiert sie automatisch direkt in das native Luminar Neo Format (.lnp Ordner mit lesbarem template.lmps JSON) im Root-Verzeichnis von Presets/Users.
  Verwenden, wenn der Benutzer in natürlicher Sprache sagt: "Konvertiere alle lmp dateien im Projektverzeichnis", "Suche und konvertiere alte lmp Presets", "Wandle meine Luminar Presets um" oder ähnliches.
---

# Luminar Preset Converter Skill

Konvertiert legacy Luminar `*.lmp` Presets (XML Apple Plist Format) direkt in das native Luminar Neo Format (`.lnp` Ordner mit `template.lmps` JSON-Dateien) im Root-Verzeichnis `Presets\Users\`.

## Ordnerstruktur in Luminar Neo

- **Import-Mechanismus**: Luminar Neo scannt Benutzer-Presets ausschließlich direkt auf der obersten Ebene des Ordners `AppData\Roaming\Luminar Neo\Data\Presets\Users\`.
- **Wichtig**: Verschachtelte Unterordner werden von Luminar Neo nicht eingelesen. Daher werden alle `.lnp`-Ordner direkt im Root-Verzeichnis von `Users\` angelegt.

---

## Auslöser in natürlicher Sprache

- *"Konvertiere alle .lmp Dateien im Projektverzeichnis."*
- *"Suche nach alten lmp Presets und wandle sie für Luminar Neo um."*
- *"Wandle meine Luminar Presets um."*

---

## Ausführungsanweisungen für den Agenten

1. **Skript ausführen**:
   ```bash
   python "C:\Users\walte\.gemini\config\skills\luminar-preset-converter\convert_lmp.py" "<PFAD_ZUM_ORDNER_ODER_PROJEKT>" [--out "<ZIEL_PFAD>"]
   ```

2. **Ergebnis**:
   Luminar Neo liest die `.lnp`-Ordner im Root-Verzeichnis `Presets/Users/` beim nächsten Start automatisch unter **Meine Voreinstellungen** / **Eigene Voreinstellungen** ein.
