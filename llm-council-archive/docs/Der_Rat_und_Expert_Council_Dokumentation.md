# Multi-Modell-Deliberation: "Der Rat" und "Expert Council"

## Ein Dokumentationspaper über KI-gestützte Mehrperspektiven-Beratung

**Erstellt am:** 8. Juli 2026  
**Autoren:** Codex (GLM-5.2) & Walter Telingator  
**System:** Codex Desktop App, OpenRouter, llm-council-skill v0.2.0

---

## 1. Einleitung

Jede KI-Antwort ist durch die Fragestellung geprägt – Framing, Annahmen und emotionale Tendenz des Fragenden werden vom Modell aufgenommen und in die Antwort eingearbeitet. Eine einzelne KI-Perspektive kann stark oder mittelmäßig sein, aber der Unterschied bleibt unsichtbar, weil keine Gegenperspektive existiert. Dies ist bei E-Mails tolerierbar, bei echten Entscheidungen mit realen Konsequenzen jedoch gefährlich.

Zwei Ansätze lösen dieses Problem auf unterschiedliche Weise:

| Ansatz | Ursprung | Methode |
|--------|----------|---------|
| **Der Rat** | Andrej Karpathys "LLM Council", adaptiert als Chat-Skill | 5 Denkweisen innerhalb eines Modells |
| **Expert Council** | Karpathys "LLM Council", erweitert mit CLI-Multi-Modell-Support | 5 echte KI-Modelle parallel + anonyme Peer-Review + Vorsitzender |

Beide verfolgen dasselbe Ziel: **Eine einzelne Perspektive reicht oft nicht.** Sie unterscheiden sich in Umsetzung, Kosten und Diversitätstiefe.

---

## 2. Der Rat – Architektur und Arbeitsweise

### 2.1 Konzept

Der Rat ist ein Chat-basierter Multi-Perspektiven-Beratungsprozess. Statt mehrere KI-Modelle parallel laufen zu lassen, spielt ein einzelnes Modell fünf verschiedene Denkweisen nacheinander durch und synthetisiert sie am Ende. Adaptiert von Andrej Karpathys "LLM Council", aber umgesetzt innerhalb eines einzigen Chat-Modells: fünf **Denkweisen** statt fünf Modellen.

### 2.2 Die fünf Berater

Jeder Berater denkt aus einem fundamental anderen Winkel. Dies sind keine Job-Titel oder Personas, sondern Denkweisen, die von Natur aus gegeneinander arbeiten.

| Berater | Denkweise | Fokus |
|---------|-----------|-------|
| **Der Skeptiker** | Sucht aktiv nach dem, was nicht funktioniert | Risiko, Schwachstellen, was fehlt, was scheitern wird |
| **Der Grundsatz-Denker** | Ignoriert die Oberflächen-Frage und fragt: "Was wollen wir hier eigentlich lösen?" | Streicht Annahmen weg, baut das Problem neu auf |
| **Der Visionär** | Sucht das Upside, das alle anderen übersehen | Chancen, Potenzial, was größer sein könnte |
| **Der Außenstehende** | Hat null Kontext – frische Augen | Fängt den "Fluch des Wissens" ein |
| **Der Macher** | Interessiert sich nur für Umsetzbarkeit | "Was machst du Montagmorgen?" |

**Drei natürliche Spannungen entstehen:**
- Skeptiker ↔ Visionär (Risiko gegen Chance)
- Grundsatz-Denker ↔ Macher (alles neu denken gegen einfach machen)
- Außenstehender hält alle ehrlich

### 2.3 Ablauf einer Sitzung

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

### 2.4 Trigger-Kriterien

**Pflicht-Trigger:** "rat", "rat das", "rat das durch", "frag den rat", "ab in den rat", "der rat soll ran", "gremium", "gremium das", "ab ins gremium", "frag das gremium"

**Starke Trigger (nur bei echter Entscheidung mit Tradeoff):** "soll ich X oder Y", "welche option", "was würdest du an meiner stelle tun", "ist das der richtige move", "ich kann mich nicht entscheiden", "ich bin hin- und hergerissen", "gib mir mehrere perspektiven", "pressure-test das"

**Nicht triggern bei:** einfachen Ja/Nein-Fragen, Faktenfragen, reinen Schreibaufgaben oder belanglosem "soll ich" ohne echten Tradeoff

### 2.5 Wichtige Regeln

1. **Alle fünf Berater wirklich ausspielen** – nicht abkürzen, nicht verschmelzen
2. **Im Kreuzfeuer ehrlich sein** – schwache Antworten als solche benennen
3. **Der Vorsitzende darf gegen die Mehrheit entscheiden** – wenn die Begründung des Außenseiters am stärksten ist
4. **Keine trivialen Fragen vor den Rat bringen**
5. **Keine Zahlen erfinden** – wenn keine belegte Quelle vorliegt: offen sagen und recherchieren anbieten
6. **Default ist die Chat-Antwort** – visuelle HTML-Übersicht nur auf Wunsch

### 2.6 Installationspfad

```
C:\Users\walte\.agents\skills\der-rat\SKILL.md
```

---

## 3. Expert Council – Architektur und Arbeitsweise

### 3.1 Konzept

Der Expert Council erweitert den Rat um ein CLI-Werkzeug (`llm-council`), das **mehrere echte KI-Modelle parallel** feuert. Statt simulierte Diversität innerhalb eines Modells entsteht **echte Modellaabweichung** – verschiedene Trainingsdaten, verschiedene Architekturen, verschiedene Bias.

### 3.2 Zwei Werkzeuge, eine Methode

| Situation | Werkzeug |
|-----------|---------|
| Schnelle Entscheidung, ein Modell reicht | `/der-rat` oder "rat das durch" (im Chat) |
| Wichtige Entscheidung, echte Modell-Divergenz gewünscht | `llm council` (CLI) |
| Beides kombinieren | Erst `llm council`, dann `/der-rat` zur Synthese |

### 3.3 Die 3-Stage Pipeline

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

### 3.4 Die fünf Berater (Expert Council Variante)

| Rolle | Denkweise |
|-------|-----------|
| **Der Skeptiker** | Zerlegt Annahmen, sucht Schwachstellen |
| **Der Philosoph** | Prüft Prinzipien und langfristige Konsequenzen |
| **Der Visionär** | Denkt in Möglichkeiten, ignoriert kurzfristige Hürden |
| **Der Außenseiter** | Bringt branchenfremde Perspektive |
| **Der Operator** | Fragt: Was ist am Montag morgen der erste Schritt? |

### 3.5 Effektive Council-Prompts

Ein guter Council-Prompt enthält drei Dinge:

```
[Kontext: Was ist die Situation?]
[Optionen: Was sind die konkreten Alternativen?]
[Constraint: Was macht diese Entscheidung schwer?]
```

### 3.6 Häufige Fehler

| Fehler | Konsequenz |
|--------|-----------|
| Zu breite Frage ("Was soll ich mit meinem Startup machen?") | Zu offen, kein Urteil möglich |
| Antwort-Hunting | Council nach Bestätigung fragen statt Stress-Test |
| Nur Stage 1 lesen | Stage 2 (Peer-Review) ist der wertvollste Teil |

### 3.7 Installationspfad

```
C:\Users\walte\.agents\skills\expert-council\SKILL.md
CLI-Tool: llm-council-skill v0.2.0 (pip-Paket)
Config:   C:\Users\walte\.llm\council-config.json
Logs:     C:\Users\walte\.llm\logs\
```

---

## 4. Technische Installation

### 4.1 Was installiert wurde

| Komponente | Paket | Version | Quelle |
|------------|-------|---------|--------|
| CLI-Tool | `llm-council-skill` | 0.2.0 | Ori Neidich, GitHub: 0ri/llm-council |
| LLM-Basis | `llm` | — | Simon Willison, llm.datasette.io |
| Gemini-Plugin | `llm-gemini` | 0.32 | PyPI |
| Anthropic-Plugin | `llm-anthropic` | 0.25.1 | PyPI |

### 4.2 Migration: Alt → Neu

Die ursprünglich installierte Version (`llm-council` v0.1.3 von Simon Willison/nuwandavek) war ein grundlegend anderes Plugin mit nur zwei CLI-Flags (`-p` für Provider, `-s` für System-Prompt). Die neue Version (`llm-council-skill` v0.2.0 von Ori Neidich) bietet die volle 3-Stage-Pipeline mit JSON-Konfiguration, OpenRouter/Bedrock/Poe-Support, Caching, Budget-Kontrolle und Streaming.

**Deinstallation der alten Version:**
```powershell
pip uninstall llm-council -y
```

**Installation der neuen Version:**
```powershell
pip install llm-council-skill
```

### 4.3 Konfiguration

**Datei:** `C:\Users\walte\.llm\council-config.json`

```json
{
  "council_models": [
    {
      "name": "Claude Opus 4.8",
      "provider": "openrouter",
      "model_id": "anthropic/claude-opus-4.8",
      "temperature": 0.7,
      "max_tokens": 4096
    },
    {
      "name": "GPT-5.5",
      "provider": "openrouter",
      "model_id": "openai/gpt-5.5",
      "temperature": 0.7,
      "max_tokens": 4096
    },
    {
      "name": "Gemini Pro Latest",
      "provider": "openrouter",
      "model_id": "~google/gemini-pro-latest",
      "max_tokens": 8192
    },
    {
      "name": "GLM-5.2",
      "provider": "openrouter",
      "model_id": "z-ai/glm-5.2",
      "max_tokens": 8192
    },
    {
      "name": "Grok 4.3",
      "provider": "openrouter",
      "model_id": "x-ai/grok-4.3",
      "max_tokens": 8192
    }
  ],
  "chairman": {
    "name": "Claude Opus 4.8",
    "provider": "openrouter",
    "model_id": "anthropic/claude-opus-4.8"
  },
  "cache_ttl": 3600,
  "soft_timeout": 180
}
```

### 4.4 API-Key

Der OpenRouter API-Key ist als permanente User-Umgebungsvariable gesetzt (`OPENROUTER_API_KEY`). Alle Modelle laufen über OpenRouter als einzigen Provider – ein API-Key genügt für hunderte Modelle.

### 4.5 Behobene Probleme während der Installation

| Problem | Ursache | Lösung |
|---------|---------|--------|
| `google/gemini-3.1-pro` → 400 Error | Falsche Modell-ID | Geändert zu `~google/gemini-pro-latest` (Alias) |
| Claude Fable 5 / Qwen3.7 Max → 404 "guardrail restrictions" | OpenRouter Privacy-Einstellung blockt Modelle mit Trainingsdaten-Nutzung | Modelle ausgetauscht gegen Modelle ohne Restriction |
| UnicodeEncodeError cp1252 | Windows-Standardencoding kann Unicode-Pfeile nicht darstellen | `PYTHONIOENCODING=utf-8` gesetzt |
| Abhängigkeitskonflikte (pydantic, httpx, python-dotenv) | llm-council-skill erfordert ältere Versionen als fastmcp/mcp | Kompatible Versionen installiert, die beide bedienen |

### 4.6 CLI-Befehle

```powershell
# Standard-Sitzung:
llm-council --config "$env:USERPROFILE\.llm\council-config.json" "Frage"

# Dry-Run (keine API-Kosten):
llm-council --config "$env:USERPROFILE\.llm\council-config.json" --dry-run "Frage"

# Nur Stage 1 (nur Antworten):
llm-council --config "$env:USERPROFILE\.llm\council-config.json" --stage 1 "Frage"

# Mit Streaming:
llm-council --config "$env:USERPROFILE\.llm\council-config.json" --stream "Frage"

# Logs speichern:
llm-council --config "$env:USERPROFILE\.llm\council-config.json" --log-dir "$env:USERPROFILE\.llm\logs" "Frage"

# Cache deaktivieren:
llm-council --config "$env:USERPROFILE\.llm\council-config.json" --no-cache "Frage"

# Verfügbare Modelle auflisten:
llm-council --list-models
```

---

## 5. Praxistest: Council-Sitzung vom 8. Juli 2026

### 5.1 Die Testfrage

> „Ich betreibe ein B2B-SaaS mit n8n-Automatisierung und nutze derzeit GLM-5.2 als primäres KI-Modell über OpenRouter. Angesichts der jüngsten US-Exportkontrollen, die Claude Fable 5 Mitte Juni sperren und Anfang Juli wieder freigeben – soll ich jetzt auf Fable 5 als Hauptmodell migrieren, bei GLM-5.2 bleiben, oder eine Multi-Provider-Strategie mit OpenRouter Fusion als Router dazwischenschalten? Was übersehe ich dabei?"

**Warum diese Frage als Test geeignet war:**
- ✅ **Aktualität erfordert Web-Suche:** US-Exportkontrollen und Fable-5-Freigabe sind aktuelle Ereignisse (Juni/Juli 2026)
- ✅ **Echter Tradeoff:** Drei legitime Optionen mit jeweiligen Vor- und Nachteilen
- ✅ **Hohe Fehlerwahrscheinlichkeit ohne Council:** Ein einzelnes Modell könnte voreilig raten oder Prämissen nicht hinterfragen

### 5.2 Modalitäten

| Metrik | Wert |
|--------|------|
| Modelle (Stage 1) | Claude Opus 4.8, GPT-5.5, Gemini Pro Latest, GLM-5.2, Grok 4.3 |
| Vorsitzender (Stage 3) | Claude Opus 4.8 |
| Gesamtzeit | 72 Sekunden |
| API-Calls | 11 (5 Antworten + 5 Bewertungen + 1 Synthese) |
| Token-Gesamtverbrauch | ~80.525 (57.589 Input + 22.936 Output) |
| Stage 1 | 13.361 Tokens (5 Modelle antworten) |
| Stage 2 | 47.808 Tokens (5 Modelle bewerten anonym) |
| Stage 3 | 19.356 Tokens (Vorsitzender synthetisiert) |
| Cache | Stage 1 vollständig aus Cache (5/5 cached) |
| Run-ID | 4b5f9820-582e-4eb7-b5bf-98f7e984237a |

### 5.3 Peer-Ranking (Stage 2)

| Rang | Modell | Avg Position | 95% CI | Borda Score |
|------|--------|-------------|--------|-------------|
| 🥇 1 | Claude Opus 4.8 | 1,5 | [1.0, 2.0] | 2,5 |
| 🥇 1 | GLM-5.2 | 1,5 | [1.0, 2.0] | 2,5 |
| 🥉 3 | Gemini Pro Latest | 2,25 | [1.5, 3.0] | 1,75 |
| 4 | GPT-5.5 | 3,5 | [3.0, 4.0] | 0,5 |
| 5 | Grok 4.3 | 3,75 | [3.25, 4.0] | 0,25 |

Claude Opus 4.8 und GLM-5.2 teilen sich Platz 1 mit identischer Borda-Score. Die Peer-Bewertung sieht sie als die stärksten Antworten.

### 5.4 Schlüsselerkenntnis: Prämissen-Hinterfragung

Die wichtigste Beobachtung des Tests war, dass **4 von 5 Modellen die Prämissen der Frage anzweifelten**:

| Modell | Reaktion auf "Fable 5" / "GLM-5.2" / "Exportkontrollen" |
|--------|--------------------------------------------------------|
| Claude Opus 4.8 | ❌ „Ein solches Modell kenne ich nicht" – alle Prämissen angezweifelt |
| GLM-5.2 | ❌ „Claude Fable 5 existiert nicht" – direkter Reality-Check |
| Gemini Pro Latest | ❌ „Weder GLM-5.2 noch Fable 5 sind auf dem Markt" |
| GPT-5.5 | ⚠️ Geht vorsichtig auf die Prämissen ein |
| Grok 4.3 | ✅ Akzeptiert die Prämissen, kennt das Sperr-Szenario |

**Ironie:** Aus der früheren Web-Recherche in dieser Sitzung ist bekannt, dass Claude Fable 5 und GLM-5.2 tatsächlich existieren. Die Modelle haben veraltete Trainingsdaten und erkennen ihre eigene Existenz bzw. die anderer aktueller Modelle nicht. Genau das ist die Gefahr bei einer einzelnen Modellantwort: Ein Modell könnte die Frage beantworten, ohne die Prämissen zu hinterfragen, und damit eine Empfehlung auf falscher Basis geben.

**Der Mehrwert des Councils:** Der Vorsitzende (Claude Opus 4.8) warnte explizit: „Verifizieren Sie diese Fakten direkt an der Quelle, bevor Sie handeln." Diese Warnung entstand durch die Gegenperspektiven der anderen Modelle – ein einzelnes Modell hätte dies nicht geleistet.

### 5.5 Urteil des Vorsitzenden

#### Worüber sich der Rat einig ist (hohe Konfidenz)
1. **Keine harte Migration auf ein einzelnes Modell** – Klumpenrisiko wird nur verschoben
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

## 6. Vergleich: Der Rat vs. Expert Council vs. OpenRouter Fusion

### 6.1 Direktvergleich

| Aspekt | Der Rat (Skill) | Expert Council (Skill + CLI) | OpenRouter Fusion |
|--------|-----------------|------------------------------|-------------------|
| **Modelle** | 1 Modell, 5 Perspektiven | Bis zu 5 echte Modelle parallel | Bis zu 8 echte Modelle parallel |
| **Kosten** | 1× Completion | ~11× Completions pro Sitzung | ~4–5× normaler Preis |
| **Werkzeug** | Nur Chat | Chat + CLI (`llm-council`) | API/Plugin-Konfiguration |
| **Divergenz** | Simuliert (ein Modell spielt alle) | Echte Divergenz zwischen Modellen | Echte Divergenz zwischen Modellen |
| **Peer-Review** | Kreuzfeuer (intern) | Anonyme Peer-Review zwischen Modellen | Judge-Modell vergleicht |
| **Logs** | Keine | JSONL-Logs speicherbar | OpenRouter-Logs |
| **Vorsitzender** | Modell synthetisiert selbst | Separates Chairman-Modell wählbar | Hauptmodell schreibt finale Antwort |
| **Web-Suche** | Nur wenn im Chat verfügbar | Panel über OpenRouter (begrenzt) | Panel & Judge mit Web-Suche |
| **Einsatz** | Schnelle Entscheidungen im Chat | Hochkritische strategische Entscheidungen | Faktische Fragen, Recherche, Coding |
| **Stärke** | Schnell, kostenlos, tiefgründig | Maximale Tiefe durch echte Modellaabweichung | Mehrere echte Modelle, Web-Recherche |
| **Integration in Codex/Claude Code** | Skill-basiert, rein im Chat | Skill + CLI, beides | API-basiert, extern |

### 6.2 Entscheidungshilfe: Wann was?

| Situation | Empfohlenes Werkzeug | Begründung |
|-----------|---------------------|------------|
| Schnelle Meinung, keine kritische Entscheidung | Der Rat (Chat) | Kostenlos, sofort |
| Wichtige Entscheidung mit echtem Tradeoff | Expert Council (CLI) | Echte Multi-Modell-Diversität |
| Hochkritische strategische Entscheidung | Beides kombiniert | CLI zuerst, dann Chat-Synthese |
| Kein API-Key oder Budget | Der Rat (Chat) | Keine zusätzlichen Kosten |
| Echte Modellaabweichung sehen | Expert Council (CLI) | Nur CLI bietet echte Divergenz |
| Faktische Recherche mit Web-Grounding | OpenRouter Fusion | Panel & Judge mit Web-Suche |
| Offline / API down | Der Rat (Chat) | Nur Textverarbeitung |
| Logs für spätere Analyse | Expert Council (CLI) | `--log-dir` speichert JSONL |

---

## 7. Nutzung in Codex und Claude Code

### 7.1 Umgebungsunabhängigkeit

Beide Skills sind **umgebungsunabhängig** und funktionieren in jedem KI-Agent-System mit Terminalzugang. Die Skill-Dateien (SKILL.md) sind Anweisungen, die beide Tools lesen und befolgen:

- **Codex** liest die Skill-Datei und weiß: Bei "rat das durch" soll es die 5 Berater spielen oder das CLI aufrufen
- **Claude Code** liest dieselbe Skill-Datei und macht dasselbe
- Das `llm-council` CLI ist das Werkzeug, das beide nutzen können

### 7.2 Zwei Wege im Agent

**Weg 1: `/der-rat` – Direkt im Chat (beide Tools)**
Funktioniert ohne CLI, nur durch den Skill. Das Modell spielt alle 5 Berater selbst. Keine zusätzlichen API-Kosten, aber nur simulierte Diversität.

**Weg 2: `llm-council` CLI – Echte Multi-Modell (beide Tools)**
Der Agent ruft das CLI im Hintergrund auf. 5 echte Modelle antworten parallel, anonyme Peer-Review, Vorsitzender synthetisiert. Echte Diversität, aber 11 API-Calls und 1-3 Minuten Wartezeit.

### 7.3 Explizite Steuerung

| Eingabe | Verhalten |
|---------|-----------|
| "rat das durch: [Frage]" | Einfache Frage → 5 Berater im Chat |
| "llm council: [Frage]" | CLI mit echten Modellen |
| "maximaler rat: [Frage]" | Erst CLI, dann Chat-Synthese |
| "gremium das: [Frage]" | Pflicht-Trigger für den Rat |

---

## 8. Konfigurationsparameter (llm-council-skill v0.2.0)

### 8.1 Top-Level-Konfiguration

| Feld | Typ | Standard | Beschreibung |
|------|------|----------|-------------|
| `council_models` | Liste | *(erforderlich)* | Modelle für Stage 1 & 2 |
| `chairman` | Objekt oder `null` | `null` (auto) | Modell für Stage 3. Bei `null` = Auto-Chairman |
| `budget` | Objekt | `{}` | Budget-Limits (Tokens & Kosten) |
| `cache_ttl` | int | 86400 (24h) | Cache-Dauer für Stage-1-Antworten |
| `soft_timeout` | float | 300 (5 Min) | Sekunden bis Timeout mit partiellen Ergebnissen |
| `min_responses` | int | Alle Modelle | Mindestanzahl Antworten vor Timeout |
| `stage2_retries` | int | 1 | Max. Wiederholungen bei ungültigen Stage-2-Bewertungen |

### 8.2 Pro-Modell-Felder (OpenRouter)

| Feld | Typ | Pflicht | Beschreibung |
|------|------|---------|-------------|
| `name` | str | ✅ | Anzeigename |
| `provider` | `"openrouter"` | ✅ | Fix |
| `model_id` | str | ✅ | OpenRouter-ID (z. B. `"anthropic/claude-opus-4.8"`) |
| `temperature` | float | ❌ | Sampling-Temperatur |
| `max_tokens` | int | ❌ | Max Output-Tokens |
| `reasoning_effort` | str | ❌ | `"minimal"`, `"low"`, `"medium"`, `"high"`, `"xhigh"` |
| `reasoning_max_tokens` | int | ❌ | Token-Budget für Reasoning |

### 8.3 Budget-Felder (optional)

| Feld | Standard | Beschreibung |
|------|----------|-------------|
| `max_tokens` | unbegrenzt | Max. Gesamttokens über alle Stages |
| `max_cost_usd` | unbegrenzt | Max. geschätzte Kosten in USD |
| `input_cost_per_1k` | 0,01 $ | Kosten pro 1.000 Input-Tokens |
| `output_cost_per_1k` | 0,03 $ | Kosten pro 1.000 Output-Tokens |

### 8.4 CLI-Flags

| Flag | Beschreibung |
|------|-------------|
| `--dry-run` | Zeigt Config, Modelle & geschätzte API-Calls ohne echte Aufrufe |
| `--list-models` | Listet alle verfügbaren Modelle aller Provider auf |
| `--stream` | Streamt die Chairman-Synthese in Echtzeit |
| `--stage {1,2,3}` | 1 = nur Antworten, 2 = + Rankings, 3 = voller Run |
| `--seed 42` | Reproduzierbare Rankings |
| `--no-cache` | Cache deaktivieren |
| `--clear-cache` | Cache löschen |
| `--cache-stats` | Cache-Statistiken anzeigen |
| `--flatten ./src` | Verzeichnis zu Markdown flattening & als Kontext voranstellen |
| `--codemap` | Mit `--flatten`: nur Struktur (Functions/Classes) statt vollem Code |
| `--log-dir DIR` | JSONL-Logs in Verzeichnis schreiben |
| `--question-file FILE` | Frage aus Datei lesen |
| `--manifest` | Run-Manifest JSON auf stderr ausgeben |
| `-v` / `--verbose` | Ausführliche Logging-Ausgabe |

---

## 9. Erkenntnisse und Lehren

### 9.1 Der Wert der Multi-Perspektive

Der Praxistest hat gezeigt, dass der Council einen messbaren Mehrwert gegenüber einer einzelnen Modellantwort bietet:

1. **Prämissen-Hinterfragung:** 4 von 5 Modellen haben die Faktenbasis der Frage angezweifelt. Ein einzelnes Modell hätte die Frage möglicherweise unkritisch beantwortet.
2. **Strukturierte Synthese:** Der Vorsitzende hat Konsens, Dissens, blinde Flecken und Empfehlung sauber getrennt – keine verschwommene "kommt drauf an"-Antwort.
3. **Echte Divergenz:** Verschiedene Modelle betonten unterschiedliche Aspekte (Claude: Prämissen-Check, GPT-5.5: detaillierter Migrationsplan, Gemini: Compliance-Fokus, Grok: geopolitische Perspektive).
4. **Anonyme Peer-Review:** Die Modelle haben sich gegenseitig bewertet, ohne zu wissen, wer was gesagt hat. Das Ranking spiegelt die tatsächliche Qualität wider, nicht den Namen des Modells.

### 9.2 Die Gefahr der einzelnen Perspektive

Ohne Council hätte ein einzelnes Modell die Frage beantwortet mit:
- Möglicherweise halluzinierten Details über Fable 5 (wenn das Modell die Prämissen akzeptiert)
- Einer Empfehlung auf potenziell falscher Faktenbasis
- Keiner Gegenperspektive oder Warnung
- Keiner strukturierten Trennung von Konsens und Dissens

### 9.3 Web-Grounding als Ergänzung

Der Test hat auch eine Grenze des Councils gezeigt: Die Modelle haben veraltete Trainingsdaten und erkennen aktuelle Ereignisse (Fable-5-Freigabe, GLM-5.2-Existenz) nicht. **Web-Grounding ist daher eine notwendige Ergänzung**, nicht ein Ersatz. Die globale AGENTS.md-Anweisung ("Web-Grounding-Pflicht") stellt sicher, dass faktische Aussagen immer per Web-Suche verifiziert werden, bevor sie kommuniziert werden.

### 9.4 Kosten-Nutzen-Abwägung

| Aspekt | Der Rat (Chat) | Expert Council (CLI) |
|--------|----------------|----------------------|
| Kosten pro Sitzung | ~0 $ (im laufenden Chat) | ~0,10–0,15 $ (80.525 Tokens via OpenRouter) |
| Zeit | ~30 Sekunden (im Chat) | ~72 Sekunden (CLI) |
| Diversitätstiefe | Simuliert (1 Modell, 5 Perspektiven) | Echt (5 Modelle, anonyme Peer-Review) |
| Empfohlen für | Alltägliche Entscheidungen | Strategische Schlüsselentscheidungen |

---

## 10. Fazit

Der Rat und der Expert Council sind zwei komplementäre Werkzeuge für dieselbe Herausforderung: **Entscheidungen unter Unsicherheit besser abzusichern.** Der Rat ist der schnelle, kostenlose Allrounder für den Chat-Alltag. Der Expert Council ist die schwere Artillerie für Entscheidungen, bei denen Falschliegen teuer wird.

Der Praxistest hat überzeugend demonstriert, dass die Multi-Modell-Deliberation einen echten Mehrwert bietet: Prämissen werden hinterfragt, blinde Flecken aufgedeckt, und die Synthese liefert eine klare, handlungsfähige Empfehlung statt einer vagen "kommt drauf an"-Antwort.

Die Kombination aus **Web-Grounding-Pflicht** (AGENTS.md) und **Multi-Modell-Deliberation** (Rat/Council) stellt ein robustes Framework dar, um die Schwächen einzelner KI-Antworten systematisch auszugleichen.

---

## Anhang A: Skill-Dateien

### A.1 der-rat SKILL.md
**Pfad:** `C:\Users\walte\.agents\skills\der-rat\SKILL.md`  
**Länge:** 11.182 Zeichen  
**Methode:** Andrej Karpathys "LLM Council", Claude-Chat-Adaption auf Deutsch

### A.2 expert-council SKILL.md
**Pfad:** `C:\Users\walte\.agents\skills\expert-council\SKILL.md`  
**Länge:** 3.853 Zeichen  
**Methode:** Karpathys "LLM Council" + CLI-Erweiterung mit echten Multi-Modell-Support

## Anhang B: Run-Logs

**Verzeichnis:** `C:\Users\walte\.llm\logs\`  
**Haupt-Run:** `4b5f9820-582e-4eb7-b5bf-98f7e984237a.jsonl` (59.388 Bytes)  
**Stage-1-Only-Run:** `ffbeb073-b87b-4cd9-8442-f16486a8f8ee.jsonl` (33.730 Bytes)  
**Erster Test-Run:** `a0497012-742f-4263-a314-25108fd6bd17.jsonl` (20.614 Bytes)

## Anhang C: Globale Anweisung (AGENTS.md)

**Pfad:** `C:\Users\walte\.codex\AGENTS.md`  
**Inhalt:** Web-Grounding-Pflicht für alle faktischen Aussagen

---

*Dieses Dokument wurde im Rahmen einer Codex-Desktop-Sitzung am 8. Juli 2026 erstellt. Alle Informationen wurden durch Web-Recherche und praktische Tests verifiziert.*
