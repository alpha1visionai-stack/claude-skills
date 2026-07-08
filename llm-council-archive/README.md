# llm-council-archive

## Multi-Modell-Deliberation: "Der Rat" und "Expert Council"

Komplettes Archiv zur Installation und Nutzung der Multi-Modell-Beratungssysteme
"Der Rat" (Chat-basiert, 5 Perspektiven in einem Modell) und "Expert Council"
(CLI-basiert, 5 echte Modelle parallel mit anonymer Peer-Review).

---

## Inhalt

```
llm-council-archive/
|
|-- docs/
|   |-- Der_Rat_und_Expert_Council_Dokumentation.md   # Vollstaendige Dokumentation
|   `-- llm-council-handbuch.html                      # HTML-Handbuch
|
|-- skills/
|   |-- der-rat/
|   |   `-- SKILL.md                                   # Rat-Skill (Chat-basiert)
|   `-- expert-council/
|       `-- SKILL.md                                   # Council-Skill (CLI-basiert)
|
|-- config/
|   |-- council-config.json                            # Council-Modellkonfiguration
|   `-- AGENTS.md                                      # Web-Grounding-Pflicht
|
|-- install/
|   |-- ubuntu/
|   |   `-- install_ubuntu.sh                          # Ubuntu-Installer
|   `-- windows/
|       `-- install_windows.ps1                        # Windows-Installer
|
|-- logs/
|   |-- 4b5f9820-*.jsonl                               # Beispiel-Run (vollstaendig)
|   |-- ffbeb073-*.jsonl                               # Beispiel-Run (Stage 1 only)
|   `-- a0497012-*.jsonl                               # Beispiel-Run (erster Test)
`-- README.md                                           # Diese Datei
```

---

## Schnellstart

### Ubuntu / Linux

```bash
# 1. Archiv entpacken
unzip llm-council-archive.zip
cd llm-council-archive

# 2. Installer ausfuehren (ohne API-Key)
chmod +x install/ubuntu/install_ubuntu.sh
./install/ubuntu/install_ubuntu.sh

# 3. Oder mit API-Key:
./install/ubuntu/install_ubuntu.sh "sk-or-v1-dein-openrouter-key"

# 4. Shell neu laden
source ~/.bashrc

# 5. Testen
rat --dry-run "Testfrage"
rat "Soll ich Workshop fuer 97 EUR oder 497 EUR launchen?"
```

### Windows (PowerShell)

```powershell
# 1. Archiv entpacken
Expand-Archive llm-council-archive.zip
cd llm-council-archive

# 2. Installer ausfuehren (ohne API-Key)
.\install\windows\install_windows.ps1

# 3. Oder mit API-Key:
.\install\windows\install_windows.ps1 -ApiKey "sk-or-v1-dein-openrouter-key"

# 4. Terminal neu starten

# 5. Testen
rat --dry-run "Testfrage"
rat "Soll ich Workshop fuer 97 EUR oder 497 EUR launchen?"
```

---

## Was installiert wird

| Komponente | Beschreibung |
|------------|-------------|
| Python 3.11+ | Basis-Laufzeitumgebung |
| llm CLI | Simon Willisons LLM-Command-Line-Tool |
| llm-council-skill v0.2.0 | Ori Neidichs Multi-Modell-Deliberation-CLI |
| llm-gemini | Google Gemini-Plugin fuer llm |
| llm-anthropic | Anthropic Claude-Plugin fuer llm |
| council-config.json | Konfiguration mit 5 Modellen + Vorsitzender |
| AGENTS.md | Globale Web-Grounding-Pflicht fuer KI-Agenten |
| der-rat Skill | Chat-basierte 5-Berater-Perspektiven |
| expert-council Skill | CLI-basierte Multi-Modell-Anleitung |
| Shell-Alias `rat` | Kurzbefehl fuer Council-Aufrufe |

---

## Voraussetzungen

### API-Key

Du benoetigst einen **OpenRouter API-Key** (https://openrouter.ai):
- Erstelle einen Account bei OpenRouter
- Generiere einen API-Key unter https://openrouter.ai/keys
- Der Key ermoeglicht Zugriff auf hunderte Modelle ueber einen einzigen Provider

### Betriebssystem

| System | Mindestversion |
|--------|---------------|
| Ubuntu | 20.04 LTS oder neuer |
| Windows | 10 (mit PowerShell 5.1+) oder Windows 11 |
| Andere Linux | Python 3.11+ verfuegbar |

---

## Konfigurierte Modelle

| Rolle | Modell | Provider |
|-------|--------|----------|
| Berater 1 | Claude Opus 4.8 | OpenRouter |
| Berater 2 | GPT-5.5 | OpenRouter |
| Berater 3 | Gemini Pro Latest | OpenRouter |
| Berater 4 | GLM-5.2 | OpenRouter |
| Berater 5 | Grok 4.3 | OpenRouter |
| Vorsitzender | Claude Opus 4.8 | OpenRouter |

Pro Council-Sitzung: 11 API-Calls (5 Antworten + 5 Bewertungen + 1 Synthese)
Geschaetzte Kosten: ~0,10-0,15 USD pro Sitzung

---

## Nutzung

### Der Rat (Chat-basiert, in Codex/Claude Code)

Schreibe in deinem KI-Agent-Chat:

```
rat das durch: Soll ich X oder Y?
gremium das: Welche Option ist besser?
pressure-test das: Ist das der richtige Move?
```

Der Agent spielt 5 Berater (Skeptiker, Grundsatz-Denker, Visionaer, Aussenstehender, Macher)
und gibt ein strukturiertes Urteil.

### Expert Council (CLI-basiert)

```bash
# Standard-Sitzung
rat "Deine Frage"

# Ohne Cache (immer frische Antworten)
rat --no-cache "Deine Frage"

# Nur Stage 1 (nur Modell-Antworten, keine Peer-Review)
rat --stage 1 "Deine Frage"

# Mit Streaming der Synthese
rat --stream "Deine Frage"

# Logs speichern
rat --log-dir ~/council-logs "Deine Frage"

# Dry-Run (keine API-Kosten)
rat --dry-run "Deine Frage"

# Verfuegbare Modelle auflisten
llm-council --list-models
```

### In Codex / Claude Code

Beide Tools koennen den Council automatisch aufrufen:
- Schreibe "rat das durch: [Frage]" fuer die Chat-Version
- Schreibe "llm council: [Frage]" fuer die CLI-Version
- Schreibe "maximaler rat: [Frage]" fuer beides kombiniert

---

## Architektur

```
Stage 1: 5 Modelle antworten parallel
    |-- Claude Opus 4.8
    |-- GPT-5.5
    |-- Gemini Pro Latest
    |-- GLM-5.2
    `-- Grok 4.3

Stage 2: Anonyme Peer-Review (alle 5 bewerten alle 5)
    |-- Modell A bewertet Antworten anonym
    |-- Modell B bewertet Antworten anonym
    |-- Modell C bewertet Antworten anonym
    |-- Modell D bewertet Antworten anonym
    `-- Modell E bewertet Antworten anonym

Stage 3: Vorsitzender synthetisiert
    `-- Claude Opus 4.8 erstellt finales Urteil:
        |-- Konsens
        |-- Dissens
        |-- Blinde Flecken
        `-- Empfehlung + erster Schritt
```

---

## Fehlerbehebung

### UnicodeEncodeError (Windows)

Setze `PYTHONIOENCODING=utf-8`:
```powershell
[Environment]::SetEnvironmentVariable("PYTHONIOENCODING", "utf-8", "User")
```

### Modell nicht verfuegbar (404)

Manche Modelle werden durch OpenRouter Privacy-Einstellungen blockiert.
Konfiguriere unter https://openrouter.ai/settings/privacy die Datenpolicy
oder waehle andere Modelle in der council-config.json.

### Falsche Modell-ID (400)

Pruefe verfuegbare Modelle mit:
```bash
llm-council --list-models
```

### Abhaengigkeitskonflikte

Falls pip Abhaengigkeitskonflikte meldet:
```bash
pip install --upgrade pydantic httpx python-dotenv
```

---

## Quellen

| Komponente | Quelle |
|------------|--------|
| llm-council-skill | https://github.com/0ri/llm-council |
| llm CLI | https://llm.datasette.io/ |
| llm-gemini | https://pypi.org/project/llm-gemini/ |
| llm-anthropic | https://pypi.org/project/llm-anthropic/ |
| OpenRouter | https://openrouter.ai/ |
| Karpathy LLM Council | Original-Konzept von Andrej Karpathy |

---

## Lizenz

- llm-council-skill: MIT (Ori Neidich)
- llm CLI: Apache 2.0 (Simon Willison)
- Skills (der-rat, expert-council): Eigene, MIT-kompatibel
- Dokumentation: Eigene

---

## Dokumentation

Die vollstaendige Dokumentation befindet sich in:
`docs/Der_Rat_und_Expert_Council_Dokumentation.md`

Sie umfasst 559 Zeilen mit:
- Architektur beider Systeme
- Technischer Installation
- Praxistest mit echten Ergebnissen
- Vergleich Rat vs. Council vs. Fusion
- Konfigurationsparameter-Referenz
- Erkenntnissen und Lehren

---

Erstellt am 8. Juli 2026 von Codex (GLM-5.2) & Walter Telingator
