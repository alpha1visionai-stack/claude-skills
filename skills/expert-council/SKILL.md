---
name: expert-council
description: "Use when facing a high-stakes decision, architectural choice, or strategic question with real tradeoffs — pricing, build-vs-buy, hiring, technical direction — that has been circling without resolution. Triggers: 'ich kann mich nicht entscheiden', 'pressure-test das', 'was würdest du tun', 'welche option', 'rat das durch', 'council this', 'mehrere perspektiven'. Do NOT trigger for simple yes/no questions, pure fact lookups, or writing tasks."
---

# Expert Council

Jede KI-Antwort ist durch deine Fragestellung geprägt. Dein Framing, deine Annahmen, deine emotionale Tendenz — das Modell nimmt das auf und liefert dir eine Version von dem, was du schon geglaubt hast. Gut für E-Mails. Gefährlich bei echten Entscheidungen.

Der Expert Council löst das: Deine Frage wird durch **fünf unabhängige Berater** mit fundamental verschiedenen Denkweisen geführt, die sich danach anonym gegenseitig prüfen. Ein Vorsitzender fasst zusammen — mit einem klaren Urteil und einem konkreten ersten Schritt.

---

## Zwei Werkzeuge, eine Methode

| Situation | Werkzeug |
|---|---|
| Schnelle Entscheidung, ein Modell reicht | `/der-rat` oder "rat das durch" |
| Wichtige Entscheidung, echte Modell-Divergenz gewünscht | `llm council` (CLI) |
| Beides kombinieren | Erst `llm council`, dann `/der-rat` zur Synthese |

**`llm council` starten (Terminal):**
```bash
llm council -p openai -p anthropic -p google "Deine Frage"

# Mit fokussiertem System-Prompt:
llm council -s "Sei direkt. Maximal 150 Wörter. Nenn den stärksten Gegenargument." "Deine Frage"
```

**`/der-rat` starten (Claude Chat):**
Schreib einfach: `rat das durch: [Deine Frage]`

---

## Wann tagt der Council

**Gute Council-Fragen** (echter Einsatz + mehrere Optionen):
- Preisgestaltung / Monetarisierung
- Build vs. Buy vs. Partner
- Hiring-Entscheidungen
- Technische Architektur mit langfristiger Bindung
- Strategische Richtungswechsel

**Keine Council-Fragen:**
- Faktenfragen ("Wann erschien Paper X?")
- Offensichtliche Entscheidungen, bei denen du nur Bestätigung suchst
- Schreibaufgaben ohne echten Tradeoff

---

## Effektive Council-Prompts

Ein guter Council-Prompt enthält drei Dinge:

```
[Kontext: Was ist die Situation?]
[Optionen: Was sind die konkreten Alternativen?]
[Constraint: Was macht diese Entscheidung schwer?]
```

**Beispiel:**
> "Wir bauen ein B2B-SaaS. Option A: Flat-Rate 99€/Monat. Option B: Usage-Based Pricing. Wir haben 12 Piloten, kein Churn-Datum. Was spricht für welche Richtung — und was übersehen wir?"

---

## Die fünf Berater (`/der-rat`)

| Rolle | Denkweise |
|---|---|
| **Der Skeptiker** | Zerlegt Annahmen, sucht Schwachstellen |
| **Der Philosoph** | Prüft Prinzipien und langfristige Konsequenzen |
| **Der Visionär** | Denkt in Möglichkeiten, ignoriert kurzfristige Hürden |
| **Der Außenseiter** | Bringt branchenfremde Perspektive |
| **Der Operator** | Fragt: Was ist am Montag morgen der erste Schritt? |

Nach der ersten Runde: anonyme Peer-Review. Der Vorsitzende benennt Konsens, Dissens und die blinde Stelle — das, was alle fünf fast übersehen hätten.

---

## Ergebnis weiterverarbeiten

Nach einer `llm council`-Session Logs abrufen:
```bash
llm logs --json   # Alle Antworten als JSON
llm logs -n 1     # Letzte Session
```

Typische Nachfrage an Claude nach dem Council:
> "Hier sind drei Council-Antworten. Wo sind sie sich einig? Wo streiten sie? Was fehlt in allen drei?"

---

## Häufige Fehler

- **Zu breite Frage**: "Was soll ich mit meinem Startup machen?" → Zu offen, kein Urteil möglich. Eingrenzen auf eine spezifische Weggabel.
- **Antwort-Hunting**: Den Council nach Bestätigung fragen, nicht nach Stress-Test. Der Council erkennt das und sagt es dir.
- **Nur Stage 1 lesen**: Bei `/der-rat` ist Stage 2 (Peer-Review) der wertvollste Teil — dort fallen die blinden Flecken auf.
