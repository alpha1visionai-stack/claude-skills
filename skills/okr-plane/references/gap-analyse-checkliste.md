# Gap-Analyse Checkliste — Klartext-Compliance

## Prüflogik

Nur **Parent-Tasks** analysieren (Issues ohne `parent`-Feld).
Subtasks (7-Phasen) erben die Auftragskarte — keine eigene Prüfung.

## Feld-Prüfung im Detail

### WAS — Outcome, nicht Output (🔴 KRITISCH wenn fehlt)

**Erkennungsmuster für Output-Formulierungen:**
- Endet auf "-ieren": erstellen, entwickeln, implementieren, erstellen, überarbeiten
- Fängt mit Verb an: "Kap 3 ... Entwurf", "Faktencheck ... durchführen"
- Beschreibt Tätigkeit: "Top 5 Verlage kontaktieren"

**Outcome-Umformulierung:**
- "Kap 3 BODY erstellen" → "Leser kann seinen Top-Energie-Hebel identifizieren und hat First Step"
- "Verlage kontaktieren" → "5 Anschreiben versendet, Tracking aktiv"
- "Feature: Login entwickeln" → "Nutzer kann sich einloggen; DSGVO-konform deployed"

### WOFÜR — Impact 2nd/3rd Order (🟡 MITTEL wenn schwach)

**Zu schwach:** Nur 1st-Order ("damit das Buch fertig wird")
**Stark:** 2nd/3rd-Order ("Ohne Deployment-Pipelines kann kein Feature live gehen — jedes KR 2.x hängt daran")

**Leitfrage:** "Was passiert, wenn wir diesen Task NICHT erledigen?"

### WER: Approver (🔴 KRITISCH wenn fehlt)

**Regel:** Genau EINE Person, nie delegierbar, nie ein Team.
**Labels wie "Mo", "Oliver", "Walter" in Plane = KEIN Approver** — sind nur Hinweise.
**Approver muss explizit in der Beschreibung stehen.**

Standard-Mapping:
- BUCH Kapitel → Oliver
- BUCH Exposé/Verlag → Mo
- NPEA Features (alle Phasen) → Walter
- WS Workshop-Design → Oliver
- WS Sales/Pricing → Mo

### WER: Driver (🟠 HOCH wenn fehlt bei NPEA Features)

Alle 18 NPEA Feature-Parent-Tasks brauchen einen Driver.
Standard: `🤖 Ki-Agent-Briefing-Writer` (Phase 1–3), `🤖 Ki-Agent-Developer` (Phase 6)

### WIE — Non-negotiables (🟡 MITTEL wenn fehlt)

Mindestens:
- Sprachvorgabe (Deutsch/Englisch)
- Stil-Vorgabe (für BUCH: energetisch, kein Akademiker-Deutsch, Hook = Führungskräfte-Beispiel)
- Ausschlüsse ("kein generisches KI-Material")
- Technische Constraints (für NPEA: DSGVO-konform, Magic Link bevorzugt)

### BIS WANN (🟠 HOCH wenn BUCH+WS kein Datum)

Anker für Deadlines:
- **Bits & Pretzels München:** Oktober 2026 (erster WV-Auftritt)
- **Verlagseinreichung:** idealerweise September 2026
- **Erster Pilot Tier-2-Workshop:** Q3 2026

NPEA hat bereits Deadlines — prüfen ob überfällig (target_date < heute).

### FERTIG WENN — DoD binär prüfbar (🔴 KRITISCH wenn fehlt)

**DoD-Templates:**

BUCH Kapitel:
- [ ] .md-Datei in manuskript/teil-X/ gespeichert
- [ ] Alle Fakten mit Quelle oder [FAKTENCHECK]-Marker
- [ ] Hook enthält Führungskräfte-Beispiel
- [ ] 3.000–4.500 Wörter
- [ ] Ping an Approver (Oliver/Mo) gesendet

NPEA Feature:
- [ ] BRD (Phase 3) von Walter freigegeben
- [ ] Tech Spec vollständig
- [ ] Deployed auf Vercel Test-Env
- [ ] Min. 1 E2E-Test grün
- [ ] Walter hat abgenommen (Phase 7 auf Done)

WS Workshop-Material:
- [ ] Als PDF + .pptx in workshops/ gespeichert
- [ ] Oliver hat freigegeben
- [ ] Facilitator-Dry-Run (30 min) absolviert

## Severity-Schema

| 🔴 KRITISCH | Approver fehlt, WAS = Output, kein DoD |
| 🟠 HOCH | Driver fehlt (NPEA), kein Datum (BUCH/WS), überfällig |
| 🟡 MITTEL | WIE fehlt, WOFÜR schwach |

## Output-Format Gap-Bericht

```markdown
## GAP X — [Titel] | [🔴/🟠/🟡 SEVERITY]

**Problem:** [Ein Satz]
**Auswirkung:** [Was bricht wenn nicht behoben]
**Betroffene Issues:** [Anzahl + Beispiele]
**Maßnahme:** [Konkrete Aktion] | **Owner:** [Mo/Oliver/Walter/Claude]
**Zeitaufwand:** [Schätzung]
```

## Maßnahmen-Matrix

| Maßnahme | Owner | Tool |
|---|---|---|
| Approver in Issues setzen | Mo + Oliver | Plane UI |
| Deadlines BUCH+WS setzen | Mo | Plane UI / API |
| Driver NPEA Features setzen | Walter | Plane UI |
| DoD als Kommentar eintragen | Claude Code | Plane API PATCH |
| Outcome-Formulierungen updaten | Claude Code | Plane API PATCH |
| Proaktiv-Regel eintragen | Claude Code | Plane API Kommentar |
