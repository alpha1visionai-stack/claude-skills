# Management-Guide: KI-Mehrmodell-Beratung

## "Der Rat" und "Expert Council" — Entscheidungen absichern durch multiple Perspektiven

**Erstellt am:** 8. Juli 2026  
**Autoren:** Codex (GLM-5.2) & Walter Telingator  

---

## 1. Warum eine einzelne KI-Antwort nicht reicht

Jede KI-Antwort ist durch die Fragestellung geprägt — Framing, Annahmen und emotionale Tendenz des Fragenden werden vom Modell aufgenommen und in die Antwort eingearbeitet. Eine einzelne KI-Perspektive kann stark oder mittelmäßig sein, aber der Unterschied bleibt unsichtbar, weil keine Gegenperspektive existiert.

Das ist bei einer E-Mail tolerierbar. Bei echten Entscheidungen mit realen Konsequenzen ist es gefährlich.

Zwei Werkzeuge lösen dieses Problem auf unterschiedliche Weise:

| Werkzeug | Methode | Einsatzgebiet |
|----------|---------|---------------|
| **Der Rat** | 5 Denkweisen innerhalb eines Modells, im Chat | Alltägliche Entscheidungen, schnell und kostenlos |
| **Expert Council** | 5 echte KI-Modelle parallel + anonyme Peer-Review + Vorsitzender | Strategische Schlüsselentscheidungen, maximale Absicherung |

Beide verfolgen dasselbe Ziel: **Eine einzelne Perspektive reicht oft nicht.**

---

## 2. Der Rat — Fünf Perspektiven im Chat

### Konzept

Der Rat ist ein Chat-basierter Beratungsprozess. Ein einzelnes Modell spielt fünf verschiedene Denkweisen nacheinander durch und synthetisiert sie am Ende. Fünf Denkweisen statt fünf Modelle — schnell, kostenlos, sofort im Gespräch verfügbar.

### Die fünf Berater

Jeder Berater denkt aus einem fundamental anderen Winkel. Dies sind keine Job-Titel, sondern Denkweisen, die von Natur aus gegeneinander arbeiten.

| Berater | Denkweise | Fokus |
|---------|-----------|-------|
| **Der Skeptiker** | Sucht aktiv nach dem, was nicht funktioniert | Risiko, Schwachstellen, was fehlt, was scheitern wird |
| **Der Grundsatz-Denker** | Ignoriert die Oberflächen-Frage und fragt: "Was wollen wir hier eigentlich lösen?" | Streicht Annahmen weg, baut das Problem neu auf |
| **Der Visionär** | Sucht das Upside, das alle anderen übersehen | Chancen, Potenzial, was größer sein könnte |
| **Der Außenstehende** | Hat null Kontext — frische Augen | Fängt den "Fluch des Wissens" ein |
| **Der Macher** | Interessiert sich nur für Umsetzbarkeit | "Was machst du Montagmorgen?" |

**Drei natürliche Spannungen entstehen:**
- Skeptiker ↔ Visionär (Risiko gegen Chance)
- Grundsatz-Denker ↔ Macher (alles neu denken gegen einfach machen)
- Außenstehender hält alle ehrlich

### Ablauf einer Sitzung

```
Schritt 1: Frage einrahmen (Kontext sammeln, neutrale Frage formulieren)
    ↓
Schritt 2: Fünf Berater antworten (je 60–120 Wörter, einseitig, committed)
    ↓
Schritt 3: Kreuzfeuer (Was ist am stärksten? Größter blinder Fleck? Was haben alle übersehen?)
    ↓
Schritt 4: Urteil des Vorsitzenden
    ├── Worüber sich der Rat einig ist
    ├── Worüber der Rat streitet
    ├── Was der Rat fast übersehen hätte
    ├── Die Empfehlung (klar, direkt, kein Hedging)
    └── Der erste Schritt (ein konkreter nächster Schritt)
```

### Wann der Rat einspringt

**Immer (Pflicht-Trigger):** "rat das durch", "frag den rat", "ab in den rat", "gremium das", "ab ins gremium"

**Bei echten Entscheidungen mit Tradeoff:** "soll ich X oder Y", "welche option", "ist das der richtige move", "ich kann mich nicht entscheiden", "pressure-test das"

**Nicht bei:** einfachen Ja/Nein-Fragen, Faktenfragen, reinen Schreibaufgaben oder belanglosem "soll ich" ohne echten Tradeoff

---

## 3. Expert Council — Fünf echte Modelle parallel

### Konzept

Der Expert Council erweitert den Rat um ein CLI-Werkzeug, das **mehrere echte KI-Modelle parallel** feuert. Statt simulierte Diversität innerhalb eines Modells entsteht **echte Modellabweichung** — verschiedene Trainingsdaten, verschiedene Architekturen, verschiedene Bias.

### Die 3-Stage Pipeline

```
Stage 1: Modelle antworten parallel
    ├── Modell A beantwortet die Frage
    ├── Modell B beantwortet die Frage
    ├── Modell C beantwortet die Frage
    ├── Modell D beantwortet die Frage
    └── Modell E beantwortet die Frage

Stage 2: Anonyme Peer-Review
    ├── Modell A bewertet alle 5 Antworten (anonymisiert)
    ├── Modell B bewertet alle 5 Antworten (anonymisiert)
    ├── Modell C bewertet alle 5 Antworten (anonymisiert)
    ├── Modell D bewertet alle 5 Antworten (anonymisiert)
    └── Modell E bewertet alle 5 Antworten (anonymisiert)

Stage 3: Vorsitzender synthetisiert
    └── Chairman-Modell erstellt finales Urteil aus:
        ├── Konsens (wo sind sich alle einig?)
        ├── Dissens (wo streiten sie?)
        ├── Blinde Flecken (was haben alle übersehen?)
        └── Empfehlung + erster Schritt
```

### Die konfigurierten Modelle

| Rolle | Modell | Provider |
|-------|--------|----------|
| Berater 1 | Claude Opus 4.8 | OpenRouter |
| Berater 2 | GPT-5.5 | OpenRouter |
| Berater 3 | Gemini Pro Latest | OpenRouter |
| Berater 4 | GLM-5.2 | OpenRouter |
| Berater 5 | Grok 4.3 | OpenRouter |
| Vorsitzender | Claude Opus 4.8 | OpenRouter |

Pro Council-Sitzung: 11 API-Calls (5 Antworten + 5 Bewertungen + 1 Synthese)  
Geschätzte Kosten: ~0,10–0,15 USD pro Sitzung

### Was ein guter Council-Prompt braucht

Ein guter Council-Prompt enthält drei Dinge:

```
[Kontext: Was ist die Situation?]
[Optionen: Was sind die konkreten Alternativen?]
[Constraint: Was macht diese Entscheidung schwer?]
```

### Häufige Fehler

| Fehler | Konsequenz |
|--------|-----------|
| Zu breite Frage ("Was soll ich mit meinem Startup machen?") | Zu offen, kein Urteil möglich |
| Antwort-Hunting | Council nach Bestätigung fragen statt Stress-Test |
| Nur Stage 1 lesen | Stage 2 (Peer-Review) ist der wertvollste Teil |

---

## 4. Vergleich: Wann welches Werkzeug?

| Aspekt | Der Rat (Chat) | Expert Council (CLI) |
|--------|----------------|----------------------|
| **Modelle** | 1 Modell, 5 Perspektiven | 5 echte Modelle parallel |
| **Kosten** | ~0 $ (im laufenden Chat) | ~0,10–0,15 $ pro Sitzung |
| **Zeit** | ~30 Sekunden | ~72 Sekunden |
| **Divergenz** | Simuliert (ein Modell spielt alle) | Echte Divergenz zwischen Modellen |
| **Peer-Review** | Kreuzfeuer (intern) | Anonyme Peer-Review zwischen Modellen |
| **Logs** | Keine | JSONL-Logs speicherbar |
| **Einsatz** | Alltägliche Entscheidungen | Strategische Schlüsselentscheidungen |

### Entscheidungshilfe

| Situation | Empfohlenes Werkzeug | Begründung |
|-----------|---------------------|------------|
| Schnelle Meinung, keine kritische Entscheidung | Der Rat (Chat) | Kostenlos, sofort |
| Wichtige Entscheidung mit echtem Tradeoff | Expert Council (CLI) | Echte Multi-Modell-Diversität |
| Hochkritische strategische Entscheidung | Beides kombiniert | CLI zuerst, dann Chat-Synthese |
| Kein Budget | Der Rat (Chat) | Keine zusätzlichen Kosten |
| Echte Modellabweichung sehen | Expert Council (CLI) | Nur CLI bietet echte Divergenz |
| Logs für spätere Analyse | Expert Council (CLI) | Logs als JSONL speicherbar |

---

## 5. Praxistest: Council-Sitzung vom 8. Juli 2026

### Die Testfrage

> „Ich betreibe ein B2B-SaaS mit n8n-Automatisierung und nutze derzeit GLM-5.2 als primäres KI-Modell über OpenRouter. Angesichts der jüngsten US-Exportkontrollen, die Claude Fable 5 Mitte Juni sperren und Anfang Juli wieder freigeben – soll ich jetzt auf Fable 5 als Hauptmodell migrieren, bei GLM-5.2 bleiben, oder eine Multi-Provider-Strategie mit OpenRouter Fusion als Router dazwischenschalten? Was übersehe ich dabei?"

**Warum diese Frage als Test geeignet war:**
- ✅ **Aktualität erfordert Web-Suche:** US-Exportkontrollen und Fable-5-Freigabe sind aktuelle Ereignisse (Juni/Juli 2026)
- ✅ **Echter Tradeoff:** Drei legitime Optionen mit jeweiligen Vor- und Nachteilen
- ✅ **Hohe Fehlerwahrscheinlichkeit ohne Council:** Ein einzelnes Modell könnte voreilig raten oder Prämissen nicht hinterfragen

### Eckdaten der Sitzung

| Metrik | Wert |
|--------|------|
| Modelle (Stage 1) | Claude Opus 4.8, GPT-5.5, Gemini Pro Latest, GLM-5.2, Grok 4.3 |
| Vorsitzender (Stage 3) | Claude Opus 4.8 |
| Gesamtzeit | 72 Sekunden |
| API-Calls | 11 (5 Antworten + 5 Bewertungen + 1 Synthese) |
| Token-Gesamtverbrauch | ~80.525 (57.589 Input + 22.936 Output) |
| Geschätzte Kosten | ~0,10–0,15 USD |

### Peer-Ranking (Stage 2 — anonyme Bewertung)

| Rang | Modell | Avg Position | Borda Score |
|------|--------|-------------|-------------|
| 🥇 1 | Claude Opus 4.8 | 1,5 | 2,5 |
| 🥇 1 | GLM-5.2 | 1,5 | 2,5 |
| 🥉 3 | Gemini Pro Latest | 2,25 | 1,75 |
| 4 | GPT-5.5 | 3,5 | 0,5 |
| 5 | Grok 4.3 | 3,75 | 0,25 |

Claude Opus 4.8 und GLM-5.2 teilen sich Platz 1 mit identischer Borda-Score. Die anonyme Peer-Bewertung sieht sie als die stärksten Antworten.

### Schlüsselerkenntnis: Prämissen-Hinterfragung

Die wichtigste Beobachtung des Tests: **4 von 5 Modellen haben die Prämissen der Frage angezweifelt.**

| Modell | Reaktion auf "Fable 5" / "GLM-5.2" / "Exportkontrollen" |
|--------|--------------------------------------------------------|
| Claude Opus 4.8 | ❌ „Ein solches Modell kenne ich nicht" — alle Prämissen angezweifelt |
| GLM-5.2 | ❌ „Claude Fable 5 existiert nicht" — direkter Reality-Check |
| Gemini Pro Latest | ❌ „Weder GLM-5.2 noch Fable 5 sind auf dem Markt" |
| GPT-5.5 | ⚠️ Geht vorsichtig auf die Prämissen ein |
| Grok 4.3 | ✅ Akzeptiert die Prämissen, kennt das Sperr-Szenario |

**Ironie:** Aus der Web-Recherche in derselben Sitzung ist bekannt, dass Claude Fable 5 und GLM-5.2 tatsächlich existieren. Die Modelle haben veraltete Trainingsdaten und erkennen ihre eigene Existenz bzw. die anderer aktueller Modelle nicht. Genau das ist die Gefahr bei einer einzelnen Modellantwort: Ein Modell könnte die Frage beantworten, ohne die Prämissen zu hinterfragen, und damit eine Empfehlung auf falscher Basis geben.

**Der Mehrwert des Councils:** Der Vorsitzende (Claude Opus 4.8) warnte explizit: „Verifizieren Sie diese Fakten direkt an der Quelle, bevor Sie handeln." Diese Warnung entstand durch die Gegenperspektiven der anderen Modelle — ein einzelnes Modell hätte dies nicht geleistet.

### Urteil des Vorsitzenden

#### Worüber sich der Rat einig ist (hohe Konfidenz)
1. **Keine harte Migration auf ein einzelnes Modell** — Klumpenrisiko wird nur verschoben
2. **Multi-Provider-Architektur mit Router-Schicht** ist die richtige Antwort
3. **Router wegen genereller Robustheit**, nicht wegen eines einzelnen Regulierungsereignisses
4. **Verhaltensunterschiede zwischen Modellen** sind das größte Risiko für n8n-Workflows

#### Die 5 kritischen blinden Flecken

| # | Blinder Fleck | Konsequenz |
|---|---------------|------------|
| 1 | Router löst Verfügbarkeit, nicht Verhaltensunterschiede | JSON/Tool-Calling bricht bei Modellwechsel → n8n-Flow stirbt |
| 2 | OpenRouter wird selbst zum Single Point of Failure | Was wenn OpenRouter down ist oder Provider entfernt? |
| 3 | Compliance & Datenhoheit | DPA/AVV, DSGVO, chinesische vs. US-Provider |
| 4 | Latenz & Timeouts | p95/p99, kaskadierte Fallbacks addieren sich |
| 5 | Kosten pro Task ≠ Kosten pro Token | Verschiedene Tokenizer, teurere Fallbacks |

#### Konkreter 5-Phasen-Plan

| Phase | Maßnahme |
|-------|----------|
| **Phase 1** | Keine Vollmigration. Bestehendes Modell bleibt primär. Neues Modell als Shadow-Test. Router für unkritische Workflows evaluieren. |
| **Phase 2** | Eval-Set bauen: 100–500 echte anonymisierte Prompts aus Workflows mit erwarteten JSON-Strukturen und Edge Cases. |
| **Phase 3** | Canary Deployment: ~5% der Workflows auf neues Modell umleiten, Metriken messen. |
| **Phase 4** | Policy Routing nach Risikoklassen: Niedrigrisiko (günstigstes Modell), Mittleres Risiko (Preis-Leistungs + Schema-Validierung), Hohes Risiko (Allowlist + Human-in-the-Loop). |
| **Phase 5** | Anbieterunabhängigkeit: Capability-Aliase statt harter Modellnamen (`llm.fast_cheap`, `llm.structured_json`, `llm.high_reasoning`). |

#### Der erste Schritt
> Baue ein Eval-Set mit 100–500 echten anonymisierten Prompts aus deinen n8n-Workflows und teste GLM-5.2 vs. Fable 5 vs. Fusion gegeneinander. Ohne Eval-Set migrierst du blind.

---

## 6. Erkenntnisse und Lehren

### Der Wert der Multi-Perspektive

Der Praxistest hat gezeigt, dass der Council einen messbaren Mehrwert gegenüber einer einzelnen Modellantwort bietet:

1. **Prämissen-Hinterfragung:** 4 von 5 Modellen haben die Faktenbasis der Frage angezweifelt. Ein einzelnes Modell hätte die Frage möglicherweise unkritisch beantwortet.
2. **Strukturierte Synthese:** Der Vorsitzende hat Konsens, Dissens, blinde Flecken und Empfehlung sauber getrennt — keine verschwommene "kommt drauf an"-Antwort.
3. **Echte Divergenz:** Verschiedene Modelle betonten unterschiedliche Aspekte (Claude: Prämissen-Check, GPT-5.5: detaillierter Migrationsplan, Gemini: Compliance-Fokus, Grok: geopolitische Perspektive).
4. **Anonyme Peer-Review:** Die Modelle haben sich gegenseitig bewertet, ohne zu wissen, wer was gesagt hat. Das Ranking spiegelt die tatsächliche Qualität wider, nicht den Namen des Modells.

### Die Gefahr der einzelnen Perspektive

Ohne Council hätte ein einzelnes Modell die Frage beantwortet mit:
- Möglicherweise halluzinierten Details über Fable 5 (wenn das Modell die Prämissen akzeptiert)
- Einer Empfehlung auf potenziell falscher Faktenbasis
- Keiner Gegenperspektive oder Warnung
- Keiner strukturierten Trennung von Konsens und Dissens

### Web-Grounding als Ergänzung

Der Test hat auch eine Grenze des Councils gezeigt: Die Modelle haben veraltete Trainingsdaten und erkennen aktuelle Ereignisse (Fable-5-Freigabe, GLM-5.2-Existenz) nicht. **Web-Grounding ist daher eine notwendige Ergänzung**, nicht ein Ersatz. Die globale Web-Grounding-Pflicht stellt sicher, dass faktische Aussagen immer per Web-Suche verifiziert werden, bevor sie kommuniziert werden.

### Kosten-Nutzen-Abwägung

| Aspekt | Der Rat (Chat) | Expert Council (CLI) |
|--------|----------------|----------------------|
| Kosten pro Sitzung | ~0 $ (im laufenden Chat) | ~0,10–0,15 $ (80.525 Tokens via OpenRouter) |
| Zeit | ~30 Sekunden (im Chat) | ~72 Sekunden (CLI) |
| Diversitätstiefe | Simuliert (1 Modell, 5 Perspektiven) | Echt (5 Modelle, anonyme Peer-Review) |
| Empfohlen für | Alltägliche Entscheidungen | Strategische Schlüsselentscheidungen |

---

## 7. Fazit

Der Rat und der Expert Council sind zwei komplementäre Werkzeuge für dieselbe Herausforderung: **Entscheidungen unter Unsicherheit besser abzusichern.** Der Rat ist der schnelle, kostenlose Allrounder für den Chat-Alltag. Der Expert Council ist die schwere Artillerie für Entscheidungen, bei denen Falschliegen teuer wird.

Der Praxistest hat überzeugend demonstriert, dass die Multi-Modell-Deliberation einen echten Mehrwert bietet: Prämissen werden hinterfragt, blinde Flecken aufgedeckt, und die Synthese liefert eine klare, handlungsfähige Empfehlung statt einer vagen "kommt drauf an"-Antwort.

Die Kombination aus **Web-Grounding-Pflicht** und **Multi-Modell-Deliberation** (Rat/Council) stellt ein robustes Framework dar, um die Schwächen einzelner KI-Antworten systematisch auszugleichen.

---

*Erstellt am 8. Juli 2026 von Codex (GLM-5.2) & Walter Telingator*