# Klartext-Auftrag Framework — Kern-Konzepte

Source of Truth (vollständig):
`/home/mo/Dokumente/ai-clients/frameworks/klartext-auftrag/Klartext-Auftrag_Framework.md`

---

## O-R-A-A — Die Haltung hinter dem Framework

| Buchstabe | Bedeutung |
|---|---|
| **O** — Ownership | Der Driver übernimmt echte Verantwortung — nicht nur Ausführung |
| **R** — Responsibility | Der Approver ist verantwortlich für die Entscheidung, nicht die Tätigkeit |
| **A** — Accountability | Klare Rechenschaftspflicht — wer muss wem für was Rede stehen? |
| **A** — Authority | Driver hat Entscheidungsfreiheit im definierten Agency Space |

ORAA verhindert das häufigste Delegations-Antipattern: Aufgabe übergeben ohne Verantwortung zu übergeben.

---

## IOOI — Value Ladder (für das WAS-Feld)

```
Input → Output → Outcome → Impact
```

| Stufe | Definition | Beispiel |
|---|---|---|
| Input | Ressourcen, die reinfließen | 20 Stunden Arbeit |
| Output | Was produziert wird | Präsentation mit 15 Folien |
| **Outcome** | Veränderung beim Empfänger | Oliver kann Erstgespräch ohne Vorbereitung führen |
| Impact | Langfristige Wirkung | Pilot-Kunde gewonnen, Revenue generiert |

**WAS im Klartext-Auftrag = immer Outcome, idealerweise mit Blick auf Impact.**

---

## DACI — Rollen im Detail

**Driver (D):**
- Führt aus, koordiniert, kommuniziert Fortschritt
- Darf und soll im Agency Space selbst entscheiden
- Meldet proaktiv wenn Deadline oder Scope in Gefahr

**Approver (A):**
- Genau eine Person — die finale Entscheidungsinstanz
- Kann nicht delegiert werden
- Bei BUCH: Oliver (Inhalt) oder Mo (Business) — nie beide gleichzeitig
- Bei Tech-Features: immer CTO/Walter

**Contributor (C):**
- Liefert Input, Reviews, Expertise
- Keine Entscheidungsverantwortung
- Beispiele: Researcher, Reviewer, Subject Matter Expert

**Informed (I):**
- Bekommt Ergebnis nach Fertigstellung
- Keine aktive Rolle im Prozess
- Beispiele: Stakeholder, die auf dem Laufenden bleiben sollen

---

## Häufige Fehler bei der Delegation

| Fehler | Symptom | Fix |
|---|---|---|
| Output statt Outcome | „Erstelle eine Präsentation" | Frag: was ändert sich beim Empfänger wenn die Präsentation fertig ist? |
| Zwei Approver | „Mo und Oliver müssen beide abnehmen" | Entscheide wer final ist — der andere wird Informed oder Contributor |
| Kein Datum | „Asap", „bald", „diese Woche" | Konkretes YYYY-MM-DD, abgeleitet von Meilensteinen |
| Fehlende Leitplanken | Driver interpretiert Qualität anders als gedacht | Non-negotiables explizit machen: Sprache, Stil, Format |
| Kein DoD | „Fertig" bleibt subjektiv | Mindestens 2 binär prüfbare Kriterien + Approver-Freigabe |
| Proaktiv-Regel fehlt | Driver meldet erst wenn Deadline verpasst | Immer explizit formulieren: „bevor die Deadline reißt" |

---

## AWESOME WENN (DoA — Definition of Awesome)

Optional-Feld, das über die Pflicht-DoD hinausgeht. Zweck: dem Driver zeigen, was ein „Wow"-Ergebnis ausmacht. Nie erzwingen, nie als Mindeststandard formulieren.

Beispiel:
- FERTIG WENN: Kap 3 ist in manuskript/ gespeichert, Fakten belegt, Oliver hat freigegeben
- AWESOME WENN: Oliver sagt spontan „das ist das stärkste Kapitel des Buches"

---

## Versandfertige Kurzfassung — Muster

```
[CTA → bis 2026-08-15]: Kap 3 BODY — Leser-Energie-Hebel klar machen

Bitte schreib Kap 3 so, dass ein Leser nach der Lektüre seinen
persönlichen Top-Energie-Hebel (Schlaf / Bewegung / Erholung) kennt
und einen konkreten ersten Schritt hat.
Deadline: 15. August. Fakten brauchen Quelle oder [FAKTENCHECK].
Hook = Führungskräfte-Beispiel, nicht abstrakt.

Fertig wenn: Datei in manuskript/teil-1/kap-03.md · alle Fakten belegt
· Hook enthält Beispiel · 3.000–4.500 Wörter · Ping an Oliver.

Fragen? Meld dich bei Oliver bevor der 15. reißt.
```
