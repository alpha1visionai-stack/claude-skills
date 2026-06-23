# Claude Skills Starter – Schnellstart

Du hast dir gerade ein Framework runtergeladen, mit dem du dir einen Personal Assistant in Claude Code baust.

## Was ist das hier?

Ein vorgefertigtes System aus Ordnern und Dateien, das Claude Code sofort versteht. Du füllst deine Infos ein, und hast einen Assistenten der dich kennt und für dich arbeitet.

## Was ist drin?

```
claude-skills-starter/
│
├── START-HIER.md          ← Du bist hier
├── CLAUDE.md              ← Das Herzstück: Dein Profil + Skills-Register
│
├── docs/                  ← Dein Kontext
│   ├── PROFIL.md          ← Wer du bist (ausführlich)
│   ├── WORKFLOWS.md       ← Deine wiederkehrenden Abläufe
│   └── STIL.md            ← Wie du schreibst
│
├── skills/                ← Deine Skills
│   └── skill-builder/     ← Der mitgelieferte Meta-Skill
│       ├── SKILL.md       ← Baut neue Skills für dich
│       └── references/    ← Technische Skill-Dokumentation
│
├── ideas/                 ← Ideen-Sammlung
│   └── BACKLOG.md         ← Bewertetes Ideen-Board
│
├── projects/              ← Projekt-Tracking
│   └── AKTIV.md           ← Was gerade läuft
│
└── research/              ← Gespeicherte Ergebnisse (füllt sich automatisch)
```

## Setup in 4 Schritten

### Schritt 1: Ordner in Claude Code öffnen
Öffne Visual Studio Code (oder dein IDE), navigiere zu diesem Ordner und starte Claude Code.

### Schritt 2: CLAUDE.md ausfüllen
Öffne `CLAUDE.md` und ersetze alle `[Platzhalter]` mit deinen echten Daten.
Das ist das Minimum – damit funktioniert der Assistant bereits.

### Schritt 3: docs/ ausfüllen (optional, aber empfohlen)
Je mehr Kontext du in `PROFIL.md`, `WORKFLOWS.md` und `STIL.md` einträgst,
desto bessere Ergebnisse bekommst du. Du musst nicht alles auf einmal ausfüllen.

### Schritt 4: Ersten Skill bauen
Tippe in Claude Code:
```
/skill-builder
```
oder sag einfach: "Ich brauche einen Skill der [dein Wunsch]."
Der Skill Builder fragt dich alles was er wissen muss und erstellt den Skill für dich.

## Tipps

- **Fang mit EINEM Skill an.** Nicht fünf gleichzeitig planen, sondern einen bauen und testen.
- **Beobachte den Agent.** Die ersten Male zuschauen, was er macht. Dann Feedback geben.
- **Skills werden besser.** Kein Skill ist beim ersten Mal perfekt. Nach 5-10 Durchläufen sitzt er.
- **Alles sind nur Textdateien.** Keine Angst – du kannst nichts kaputt machen. Wenn was nicht passt, einfach die Datei bearbeiten.
- **Skill Builder nutzen.** Der hilft dir nicht nur beim Bauen, sondern auch beim Verbessern bestehender Skills.

## Ideen für erste Skills

Falls du nicht weißt wo du anfangen sollst:

- **Morgen-Briefing**: Kalender + Projekte + Prioritäten zusammenfassen
- **Content-Ersteller**: Social Media Posts, Blogposts, Newsletter in deinem Stil
- **Recherche-Skill**: Themen recherchieren und strukturiert zusammenfassen
- **E-Mail-Verfasser**: E-Mails nach deinem Schema vorformulieren
- **Meeting-Vorbereitung**: Vor Calls alles Wichtige zusammentragen
