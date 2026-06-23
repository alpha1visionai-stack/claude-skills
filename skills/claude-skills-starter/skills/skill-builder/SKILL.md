---
name: skill-builder
description: Erstellt neue Skills und verbessert bestehende. Nutze diesen Skill wenn du einen neuen Skill bauen, einen bestehenden optimieren, oder das Skill-Format verstehen willst.

---

# Skill Builder

Baut maßgeschneiderte Skills – Schritt für Schritt, durch gezielte Fragen.

## Wann nutzen

- "Neuen Skill erstellen" / "Skill bauen" / "Ich brauche einen Skill für..."
- "Skill verbessern" / "Skill optimieren" / "Der Skill funktioniert nicht gut"
- "Wie ist das Skill-Format?" / "Skill-Architektur erklären"

---

## Kontext: Was ist ein Skill?

Ein Skill ist ein Ordner mit einer `SKILL.md`-Datei. Diese Markdown-Datei enthält Anweisungen, die der KI sagen, **was sie tun soll, wann, und wie**. Im Prinzip eine Checkliste für einen digitalen Mitarbeiter.

### Wo leben Skills?
```
~/.claude/skills/skill-name/     → Global: Funktioniert in jedem Projekt
.claude/skills/skill-name/       → Lokal: Nur in diesem Projekt verfügbar
```

### Ordnerstruktur eines Skills
```
skill-name/
├── SKILL.md              ← Pflicht: Hauptdatei mit Anweisungen
├── references/           ← Optional: Vorlagen, Beispiele, Doku
└── scripts/              ← Optional: Ausführbare Skripte
```

Die meisten Skills brauchen NUR die `SKILL.md`. Unterordner erst anlegen, wenn die SKILL.md über 300 Zeilen geht oder externe Logik gebraucht wird.

---

## Anweisungen: Neuen Skill erstellen

### Schritt 1: Bedarf klären

Stelle diese Fragen (nacheinander, nicht alle auf einmal):

1. **Was soll der Skill tun?** – Das Ziel in einem Satz.
2. **Wann nutzt du ihn?** – In welchen Situationen? Wie oft?
3. **Was sagst du, um ihn auszulösen?** – Natürliche Sätze sammeln.
4. **Wie sieht ein gutes Ergebnis aus?** – Konkretes Beispiel oder Format.
5. **Welche Infos braucht der Skill?** – Dateien, APIs, Kontext?
6. **Was darf NICHT passieren?** – Harte Regeln, Einschränkungen.

### Schritt 2: SKILL.md schreiben

Nutze dieses Format:

```markdown
---
name: [skill-name]                     # Kleinbuchstaben, Bindestriche
description: [Was + Wann in 1-2 Sätzen]  # Entscheidend für Skill-Erkennung!
user-invocable: true
---

# [Skill Name]

[Was macht der Skill? Ein Satz.]

## Wann nutzen

- [Trigger-Satz 1]
- [Trigger-Satz 2]
- [Trigger-Satz 3]

## Kontext

[Hintergrundwissen das die KI jedes Mal braucht]

## Anweisungen

1. [Erster Schritt – klar und konkret]
2. [Zweiter Schritt]
3. [Dritter Schritt]
...

## Regeln

- [Harte Regel 1]
- [Harte Regel 2]

## Output-Format

[Wie soll das Ergebnis aussehen? Template zeigen.]
```

### Schritt 3: Skill-Ordner anlegen

```bash
mkdir -p skills/[skill-name]
```

Die SKILL.md dort ablegen.

### Schritt 4: Testen

- Skill direkt in der Session testen
- Output mit dem Nutzer abgleichen
- Feedback einarbeiten

### Schritt 5: Installieren

Für globale Verfügbarkeit (funktioniert in jedem Projekt):
```bash
ln -sf "$(pwd)/skills/[skill-name]" ~/.claude/skills/[skill-name]
```

### Schritt 6: In CLAUDE.md eintragen

Den neuen Skill in die Skills-Tabelle in der CLAUDE.md einfügen.

---

## Anweisungen: Bestehenden Skill verbessern

1. SKILL.md des Ziel-Skills lesen
2. Fragen: Was funktioniert nicht? Was fehlt? Was ist zu langsam?
3. Gezielt anpassen:
   - **Falscher Output** → Anweisungen präzisieren, Beispiel ergänzen
   - **Falscher Ton/Stil** → Referenzdatei mit echten Beispielen erstellen
   - **Gleicher Fehler wiederholt** → Explizite Regel hinzufügen
   - **Zu langsam / zu viele Tokens** → Konstante Werte hardcoden, Referenzdateien statt API-Calls
   - **Triggert nicht** → Description im Frontmatter konkreter machen
   - **Triggert zu oft** → Description eingrenzen

---

## Best Practices

### Die Beschreibung entscheidet alles
Die `description` im Frontmatter ist das Wichtigste am ganzen Skill. Claude liest NUR Name und Beschreibung beim ersten Scan. Wenn die Beschreibung unklar ist, wird der Skill nie gefunden.

**Schlecht**: `description: Hilft bei Content`
**Gut**: `description: Erstellt YouTube-Titel, Thumbnails und Beschreibungen aus einem Video-Transkript. Nutze wenn ein fertiges Video optimiert werden soll.`

### Schritte statt Prosa
Nummerierte Schritte statt Fließtext. Die KI arbeitet Checklisten sauberer ab als Absätze.

### Verweise statt Wiederholung
Wenn Wissen schon in einer Datei existiert (z.B. Schreibstil in `docs/STIL.md`), dort verlinken statt kopieren:
```markdown
Beachte den Schreibstil aus [docs/STIL.md](../../docs/STIL.md)
```

### Beispiele schlagen Regeln
Ein konkretes Beispiel (Input → Output) ist effektiver als zehn abstrakte Regeln.

### SKILL.md unter 500 Zeilen halten
Wenn es mehr wird: Auslagern in `references/` Unterordner. Die KI verliert bei zu langen Dateien den Fokus.

### Kein Overengineering
Ein Skill muss nicht alles abdecken. Lieber drei fokussierte Skills als ein Monster-Skill.

### Der Feedback-Loop
Kein Skill ist beim ersten Mal perfekt. Der Ablauf:
1. Skill bauen → testen → beobachten was die KI macht
2. Feedback geben → Skill anpassen
3. Wiederholen bis das Ergebnis stimmt
4. Nach 5-10 Durchläufen ist der Skill richtig gut
