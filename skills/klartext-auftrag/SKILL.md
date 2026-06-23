---
name: klartext-auftrag
description: This skill should be used when the user is delegating a task to a colleague, assigning work to a team member or KI-agent, writing a task description or briefing, asking to "schreib einen task für", "beauftrage X mit", "erstell eine Auftragskarte", "assign this to", "briefing schreiben", "task anlegen", "delegiere das an", "wer macht das?", or invokes "/klartext-auftrag". Also applies proactively whenever a task is being created and no Klartext structure is present yet. Turns any delegation intent into a complete, unambiguous 6-field Klartext card (WAS/WOFÜR/WER-DACI/WIE/BIS WANN/FERTIG WENN + Proaktiv-Regel).
version: 1.0.0
---

# /klartext-auftrag — Delegation Quality Gate

Dieses Skill ist ein **Qualitäts-Gate für Delegation**. Es greift proaktiv immer dann, wenn eine Aufgabe an eine Person oder einen KI-Agenten übergeben wird — ob der Nutzer explizit darum bittet oder nicht.

**Kernprinzip:** Delegiere Outcomes, nicht Outputs. Wer, Was und Wann müssen so klar sein, dass der Driver ohne Rückfragen starten kann.

Framework Source of Truth: `/home/mo/Dokumente/ai-clients/frameworks/klartext-auftrag/Klartext-Auftrag_Framework.md`

## Arbeitsablauf

### Schritt 1 — Kontext segmentieren

Jede Information aus dem Nutzer-Input einem der 6 Felder zuordnen. Ampel setzen:
- 🟢 klar und explizit vorhanden
- 🟡 vorhanden aber mehrdeutig
- 🔴 fehlt komplett

### Schritt 2 — Nur Lücken fragen

Gebündelt, nummeriert, max. 5 Fragen. Plausible Defaults als Ja/Nein anbieten.
- Niemals nach 🟢-Feldern fragen.
- Kein Approver erkennbar → immer Pflichtfrage.
- Selbst getroffene Annahmen mit **(Annahme)** markieren.

### Schritt 3 — Auftragskarte ausgeben

Vollständige Karte im Standardformat. Danach: versandfertige Kurzfassung (4–5 Zeilen direkt an den Driver).

### Schritt 4 — Ablage anbieten

Wenn Projektkontext erkennbar: anbieten, die Karte in Plane anzulegen oder als `.md` zu speichern.

## Die 6 Felder + Proaktiv-Regel

### 1. WAS — Outcome, nicht Output

**Regel:** Das WAS beschreibt die Veränderung beim Empfänger — nicht die Tätigkeit.

| ❌ Output (falsch) | ✅ Outcome (richtig) |
|---|---|
| Präsentation erstellen | Oliver kann das Erstgespräch ohne weitere Vorbereitung führen |
| Code implementieren | Nutzer kann sich einloggen; Feature ist deployed und getestet |
| Kap 3 schreiben | Leser versteht seinen Top-Energie-Hebel und hat einen First Step |
| Verlage kontaktieren | 5 Anschreiben versendet, Tracking aktiv |

Erkennungsmuster für falsche Formulierungen: endet auf „-ieren", „erstellen", „durchführen", „entwickeln", oder startet mit Infinitiv ohne Ergebnis.

### 2. WOFÜR — Impact 2nd/3rd Order

Nicht nur „damit das Projekt weitergeht". Die Leitfrage: *Was passiert, wenn wir diesen Task NICHT erledigen?*

Stark: „Ohne Deployment-Pipelines kann kein Feature live gehen — jedes weitere KR hängt daran."
Schwach: „Damit die App fertig wird."

### 3. WER — DACI-Modell

| Rolle | Regel |
|---|---|
| **Driver** | Genau 1 Person/Agent, führt aus, trägt operationale Verantwortung |
| **Approver** | Genau 1 Person, nie delegierbar, entscheidet final über Abnahme |
| Contributor | Optional, liefert Input |
| Informed | Bekommt Ping bei Fertigstellung |

**Kritisch:** Wenn zwei Personen als Approver vorgeschlagen werden → nachfragen, wer final entscheidet. Nie ein Team als Approver.

### 4. WIE — Leitplanken

Drei Bereiche:
- **Non-negotiable:** Was nicht verhandelbar ist (Sprache, Standards, Compliance)
- **Ausschlüsse:** Was explizit NICHT getan werden soll
- **Agency Space:** Wo der Driver eigenständig entscheiden darf

### 5. BIS WANN — Konkretes Datum

Kein „asap", kein „bald". Immer: `YYYY-MM-DD`. Optional: Zwischencheck-Datum.

### 6. FERTIG WENN — DoD, binär prüfbar

Jedes Kriterium muss mit Ja/Nein beantwortet werden können. Templates:

**Content/Buch:**
- [ ] Datei liegt in Pfad X gespeichert
- [ ] Alle Fakten haben Quellenangabe oder [FAKTENCHECK]-Marker
- [ ] Approver hat explizit freigegeben

**Tech/Software:**
- [ ] Feature deployed auf Test-Env
- [ ] Min. 1 automatisierter Test grün
- [ ] Approver (CTO) hat abgenommen

**Workshop/Sales:**
- [ ] Als PDF gespeichert unter [Pfad]
- [ ] Dry-Run absolviert
- [ ] Approver hat freigegeben

### ⚡ Proaktiv-Regel (immer hinzufügen)

> Driver meldet sich beim Approver **bevor** die Deadline reißt — Was hakt · Auswirkung · Vorschlag.

## Ausgabeformat

```
📋 KLARTEXT-AUFTRAG — [Kurztitel]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WAS          [Outcome — Veränderung beim Empfänger]

WOFÜR        [Impact 2nd/3rd Order — was passiert wenn nicht getan?]

WER          Driver: [Name/Agent]
             Approver: [Genau 1 Person]
             Contributor: [optional]
             Informed: [optional]

WIE          Non-negotiable: [...]
             Nicht: [Ausschlüsse]
             Frei: [Agency Space]

BIS WANN     [YYYY-MM-DD]  (Check-Point: [YYYY-MM-DD])

FERTIG WENN  • [Kriterium 1]
             • [Kriterium 2]
             • Approver hat freigegeben

⭐ AWESOME   [optional — was wäre ein echtes Wow?]

🔴 PROAKTIV  Driver meldet sich beim Approver bevor Deadline reißt
             — Was hakt · Auswirkung · Vorschlag
```

**Kurzfassung (direkt an Driver):**
```
[CTA → bis DATUM]: [Kurztitel]
[2–3 Sätze: Was genau, bis wann, woran erkennst du dass du fertig bist]
Fragen? Meld dich bei [Approver] bevor die Deadline reißt.
```

## Eiserne Regeln

- **Niemals erfinden.** Keine Namen, Zahlen oder Termine hinzudichten. Annahmen mit **(Annahme)** kennzeichnen.
- **Genau 1 Approver.** Bei zwei Kandidaten: nachfragen.
- **WAS muss beobachtbar sein.** Tätigkeit → nach Resultat fragen.
- **Proaktiv-Regel immer einfügen** — keine Ausnahme.
- **Sprache:** Deutsch, Du-Form, energetisch-professionell.

## Referenz

Vollständiges Framework (ORAA, IOOI, Value Chain, DoA):
`references/framework-kern.md`

Für Plane-Integration im NPE-Projekt: Skill `/okr-plane`
