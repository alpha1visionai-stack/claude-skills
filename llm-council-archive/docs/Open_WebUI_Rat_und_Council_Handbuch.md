# Open WebUI Integration: \"Der Rat\" und \"Expert Council\"

## Handbuch für die Implementierung von KI-Mehrperspektiven-Beratung in Open WebUI

**Erstellt am:** 8. Juli 2026
**Basiert auf:** Open WebUI Dokumentation (docs.openwebui.com) & Pipe Function API
**System:** Open WebUI, OpenRouter, Multi-Model Chat, Skills, Pipe Functions

---

## 1. Einleitung

Jede KI-Antwort ist durch die Fragestellung geprägt. Eine einzelne Perspektive reicht oft nicht — besonders bei strategischen Entscheidungen. Dieses Handbuch beschreibt, wie sich die Multi-Perspektiven-Beratungssysteme **\"Der Rat\"** und **\"Expert Council\"** in **Open WebUI** realisieren lassen.

Drei Implementierungsebenen stehen zur Verfügung:

| Ebene | Feature | Aufwand | Ergebnis |
|-------|---------|---------|----------|
| **1. Schnell** | Multi-Model Chats + MOA Merge | 5 Min | Parallelantworten + Synthese |
| **2. Mittel** | Skills + Slash-Commands | 30 Min | Chat-basierter Rat |
| **3. Voll** | Pipe Function | 2–4 Std | Vollständige 3-Stage-Pipeline |

---

## 2. Grundlagen: Open WebUI Features

### 2.1 Multi-Model Chats

Open WebUI hat eingebauten Support für parallele Multi-Modell-Antworten:

- **Modellauswahl**: Im Chat-Header auf **+** klicken und bis zu 5 Modelle auswählen
- **Parallelantworten**: Alle Modelle antworten gleichzeitig, side-by-side
- **MOA Merge (Mixture-of-Agents)**: Ein Synthesizer-Modell erzeugt eine finale Antwort aus allen Einzelantworten

> **Quelle:** [Open WebUI Multi-Model Chats](https://docs.openwebui.com/features/chat-conversations/chat-features/multi-model-chats/)

### 2.2 Skills

Skills sind Markdown-Dateien, die dem Modell beibringen, wie es eine Aufgabe strukturiert angehen soll:

`
Workspace → Skills → Neuer Skill
`

### 2.3 Slash-Commands (Prompts)

Wiederverwendbare Prompt-Templates mit Slash-Command-Kürzel:

`
Workspace → Prompts → Neuer Prompt
`

### 2.4 Pipe Functions

Pipe Functions sind Python-Funktionen, die sich als eigenes \"Modell\" in Open WebUI registrieren. Sie können beliebige API-Orchestrierung, Logik und Multi-Step-Pipelines ausführen.

`
Admin Panel → Workspace → Functions → New Function
`

> **Quelle:** [Pipe Function API](https://docs.openwebui.com/features/extensibility/plugin/functions/pipe/)

### 2.5 Task Model (Vorsitzenden-Modell)

`
Admin Panel → Settings → Tasks → Task Model
`

Hier wird das Modell für den Vorsitzenden / Synthesizer eingestellt (z. B. anthropic/claude-opus-4.8).

### 2.6 Web Search

Open WebUI hat eingebautes Web Search — löst das Web-Grounding-Problem, das in reinen CLI-Implementationen auftritt.

---

## 3. Ebene 1: Multi-Model Chats + MOA Merge (5 Minuten)

Die schnellste Implementierung — kein Code, nur UI-Konfiguration.

### 3.1 Konfiguration

1. **Task Model setzen**: Admin Panel → Settings → Tasks → Task Model
   - Empfohlen: anthropic/claude-opus-4.8 oder ein leistungsstarkes Synthesizer-Modell
2. **Chat starten**: Neuen Chat öffnen
3. **Modelle hinzufügen**: Im Chat-Header auf **+** klicken
   - 5 Modelle auswählen (z. B. GPT-4o, Claude 3.5 Sonnet, Gemini 2.0, Llama 3.1, Mistral Large)
4. **Prompt senden**: Die Frage eingeben — alle 5 Modelle antworten parallel
5. **MOA Merge**: Auf den Merge-Button klicken → Synthesizer erzeugt finale Antwort

### 3.2 Mapping zum Expert Council

| Council-Stage | Open WebUI Feature |
|---------------|-------------------|
| Stage 1: 5 Modelle parallel | Multi-Model Chat (eingebaut) |
| Stage 2: Anonyme Peer-Review | Nicht eingebaut |
| Stage 3: Vorsitzender synthetisiert | MOA Merge-Button (eingebaut) |

### 3.3 Vorteile und Grenzen

**Vorteile:**
- Kein Code nötig
- Alle Modelle feuern gleichzeitig
- Sofort nutzbar

**Grenzen:**
- Keine anonyme Peer-Review
- MOA-Synthese ist allgemeine Zusammenfassung, kein strukturiertes Urteil mit Konsens/Dissens

---

## 4. Ebene 2: Der Rat als Skill + Slash-Command (30 Minuten)

### 4.1 Skill anlegen

`
Workspace → Skills → Neuer Skill → \"Der Rat\"
`

Inhalt (die 5 Berater-Rollen, Trigger-Kriterien und Ablauf):

`markdown
# Der Rat

Du bist ein erfahrener Vorsitzender eines KI-Beratergremiums.

## Trigger
- \"rat das durch\"
- \"hol den rat\"
- \"berater\"
- \"council\"
- \"mehrere perspektiven\"

## Die 5 Berater
1. **Der Realist**: Was sind die Fakten, harte Grenzen, Risiken?
2. **Der Stratege**: Welches Problem wollen wir hier eigentlich lösen?
3. **Der Visionär**: Sucht das Upside, das alle übersehen
4. **Der Außenstehende**: Frische Augen, kein Kontext
5. **Der Macher**: Was machst du Montagmorgen?

## Ablauf
1. 5 Berater antworten (je 60–120 Wörter, bewusst einseitig)
2. Kreuzfeuer: Was ist am stärksten? Großer blinder Fleck?
3. Urteil: Konsens, Dissens, Blinde Flecken, Empfehlung, Erster Schritt
`

### 4.2 Slash-Command anlegen

`
Workspace → Prompts → Neuer Prompt
`

| Feld | Wert |
|------|------|
| Command | /rat |
| Beschreibung | \"Frage durch 5 Berater prüfen\" |
| Template | Siehe Skill-Inhalt oben (5 Berater + Kreuzfeuer + Urteil) |

### 4.3 Nutzung

Im Chat einfach eingeben:

`
/rat Soll ich X oder Y?
`

→ Das Modell spielt die 5 Berater-Rollen durch und liefert ein strukturiertes Urteil.

---

## 5. Ebene 3: Expert Council als Pipe Function (vollständig)

Die mächtigste Implementierung. Eine Pipe Function registriert sich als neues \"Modell\" in Open WebUI — sobald der Nutzer es auswählt, führt die Python-Funktion die komplette 3-Stage-Pipeline aus.

### 5.1 Architektur

`
Nutzer wählt \"Expert Council\" im Model-Selector
    ↓
pipe() wird aufgerufen
    ↓
Stage 1: 5 API-Calls parallel (async) → 5 Antworten
    ↓
Stage 2: 5 API-Calls parallel → jede bewertet alle 5 Antworten (anonymisiert)
    ↓
Stage 3: 1 API-Call → Vorsitzender synthetisiert strukturiertes Urteil
    ↓
Streaming-Antwort an den Nutzer
`

### 5.2 Pipe Function Code

Die vollständige Pipe Function wird in Open WebUI unter Admin Panel → Workspace → Functions → New Function eingefügt:

`python
\"\"\"
title: Expert Council
author: alpha1visionai
version: 1.0
\"\"\"
from pydantic import BaseModel, Field
from typing import Optional, Generator
import httpx
import asyncio
import json

class Pipe:
    class Valves(BaseModel):
        OPENROUTER_API_KEY: str = Field(
            default=\"\",
            description=\"OpenRouter API Key\"
        )
        BASE_URL: str = Field(
            default=\"https://openrouter.ai/api/v1\",
            description=\"OpenRouter Base URL\"
        )
        CHAIRMAN_MODEL: str = Field(
            default=\"anthropic/claude-opus-4.8\",
            description=\"Vorsitzenden-Modell für Stage 3\"
        )

    def __init__(self):
        self.valves = self.Valves()
        self.type = \"manifold\"

    def pipes(self):
        return [
            {\"id\": \"council\", \"name\": \"Expert Council\"},
        ]

    async def pipe(
        self,
        body: dict,
        __event_emitter__: Optional[callable] = None,
        __user__: Optional[dict] = None,
    ) -> Generator[str, None, None]:
        council_models = [
            \"openai/gpt-4o\",
            \"anthropic/claude-3.5-sonnet\",
            \"google/gemini-2.0-flash-001\",
            \"meta-llama/llama-3.1-70b-instruct\",
            \"mistralai/mistral-large-2407\",
        ]

        question = body[\"messages\"][-1][\"content\"]

        # Stage 1: 5 Modelle parallel
        await self._emit_status(__event_emitter__, \"Stage 1/3: 5 Berater befragen...\")
        responses = await self._call_models_parallel(
            council_models, question, body[\"messages\"][:-1]
        )

        # Stage 2: Anonyme Peer-Review
        await self._emit_status(__event_emitter__, \"Stage 2/3: Peer-Review läuft...\")
        review_prompt = self._build_review_prompt(responses, question)
        reviews = await self._call_models_parallel(
            council_models, review_prompt, []
        )

        # Stage 3: Synthese
        await self._emit_status(__event_emitter__, \"Stage 3/3: Vorsitzender synthetisiert...\")
        synthesis_prompt = self._build_synthesis_prompt(
            question, responses, reviews
        )
        final = await self._call_model(
            self.valves.CHAIRMAN_MODEL,
            synthesis_prompt,
            []
        )

        yield final

    async def _emit_status(self, emitter, message: str):
        if emitter:
            await emitter({
                \"type\": \"status\",
                \"data\": {\"description\": message, \"done\": False},
            })

    async def _call_model(self, model: str, prompt: str, context: list) -> str:
        headers = {
            \"Authorization\": f\"Bearer {self.valves.OPENROUTER_API_KEY}\",
            \"Content-Type\": \"application/json\",
        }
        payload = {
            \"model\": model,
            \"messages\": [
                *context,
                {\"role\": \"user\", \"content\": prompt},
            ],
            \"max_tokens\": 4096,
        }
        async with httpx.AsyncClient(timeout=120) as client:
            r = await client.post(
                f\"{self.valves.BASE_URL}/chat/completions\",
                json=payload, headers=headers
            )
            r.raise_for_status()
            return r.json()[\"choices\"][0][\"message\"][\"content\"]

    async def _call_models_parallel(
        self, models: list, prompt: str, context: list
    ) -> list:
        async def call(m):
            try:
                resp = await self._call_model(m, prompt, context)
                return {\"model\": m, \"response\": resp}
            except Exception as e:
                return {\"model\": m, \"error\": str(e)}

        return await asyncio.gather(*[call(m) for m in models])

    def _build_review_prompt(self, responses: list, question: str) -> str:
        answers = []
        valid = [r for r in responses if \"error\" not in r]
        for i, resp in enumerate(valid):
            answers.append(f\"--- Antwort {chr(65+i)} ---\\n{resp['response']}\\n\")
        return (
            f\"Frage: {question}\\n\\n\"
            f\"Bewerte die folgenden {len(answers)} Antworten anonym.\\n\"
            f\"Vergib Ränge 1 (beste) bis {len(answers)} (schlechteste).\\n\"
            f\"Begründe kurz.\\n\\n\" + \"\\n\".join(answers)
        )

    def _build_synthesis_prompt(
        self, question: str, responses: list, reviews: list
    ) -> str:
        valid_responses = [r for r in responses if \"error\" not in r]
        valid_reviews = [r for r in reviews if \"error\" not in r]

        resp_text = \"\\n\\n\".join([
            f\"**{r['model']}**:\\n{r['response']}\" for r in valid_responses
        ])
        review_text = \"\\n\\n\".join([str(r) for r in valid_reviews])

        return (
            f\"## Originalfrage\\n{question}\\n\\n\"
            f\"## Antworten der 5 Berater\\n{resp_text}\\n\\n\"
            f\"## Anonyme Peer-Reviews\\n{review_text}\\n\\n\"
            f\"Erstelle jetzt das strukturierte Urteil:\\n\"
            f\"1. Konsens: Wo sind sich alle einig?\\n\"
            f\"2. Dissens: Wo gibt es echte Meinungsverschiedenheiten?\\n\"
            f\"3. Blinde Flecken: Was wurde übersehen?\\n\"
            f\"4. Empfehlung: Konkrete Handlungsoption\\n\"
            f\"5. Erster Schritt: Was ist die unmittelbare Aktion?\"
        )
`

### 5.3 Installation

1. **Function anlegen**: Admin Panel → Workspace → Functions → New Function
2. **Code einfügen**: Obigen Code in den Editor kopieren
3. **Speichern**: Function speichern
4. **Valves konfigurieren**: OpenRouter API Key eintragen
5. **Modell auswählen**: \"Expert Council\" erscheint im Model-Selector

### 5.4 Konfiguration

| Valve | Beschreibung | Default |
|-------|-------------|---------|
| OPENROUTER_API_KEY | OpenRouter API Key | (leer) |
| BASE_URL | OpenRouter Base URL | https://openrouter.ai/api/v1 |
| CHAIRMAN_MODEL | Vorsitzenden-Modell | anthropic/claude-opus-4.8 |

---

## 6. Vergleich: CLI vs. Open WebUI

| Aspekt | CLI (llm-council) | Open WebUI Pipe |
|--------|-------------------|-----------------|
| Nutzung | Terminal-Befehl (rat \"Frage\") | Chat-UI, Modell auswählen |
| Streaming | Terminal-Output | Chat-Streaming |
| Logs | JSONL auf Festplatte | Im Chat-Verlauf gespeichert |
| Konfiguration | JSON-Datei | Valves in der UI |
| Multi-User | Ein Nutzer | Mehrere Nutzer gleichzeitig |
| Authentifizierung | API-Key als Env-Var | API-Key in Valves |
| Web-Grounding | Nur über AGENTS.md-Anweisung | Open WebUI Web Search (eingebaut) |
| Peer-Review | Eingebaut (Stage 2) | Custom Pipe (oben implementiert) |
| Kosten | ~0,10–0,15 $/Sitzung | Gleich (11 API-Calls) |

---

## 7. Open WebUI Zusatzfeatures

| Feature | Nutzen für Rat/Council |
|---------|----------------------|
| **Web Search** (eingebaut) | Löst das Web-Grounding-Problem — Modelle recherchieren live |
| **Memory** | Rat kann sich an frühere Urteile erinnern |
| **Automations** | Council-Sitzungen zeitlich planen (z. B. wöchentlicher Check) |
| **Tools** | Python-Tools im Chat für Erweiterungen |
| **MCP Support** | Externe Tool-Server einbinden |
| **Folders/Tags** | Council-Sitzungen organisieren |
| **User Permissions** | Rat/Council nur für bestimmte Nutzer |

---

## 8. Empfohlene Implementierungs-Reihenfolge

1. **Ebene 1** (5 Min): Multi-Model Chat mit 5 Modellen aktivieren + MOA Merge-Button testen → Sofortiger Nutzen, kein Code

2. **Ebene 2** (30 Min): /rat als Slash-Command + Der-Rat-Skill importieren → Für alltägliche Entscheidungen im Chat

3. **Ebene 3** (2–4 Std): Pipe Function installieren → Vollständige 3-Stage-Pipeline mit Peer-Review

---

## 9. Fehlerbehebung

### Pipe Function startet nicht
- **API Key prüfen**: OpenRouter API Key in Valves eingetragen?
- **Modelle verfügbar**: Alle 5 Modelle über OpenRouter erreichbar?
- **Timeout**: Bei großen Antworten das 120s-Timeout erhöhen

### Rat-Antworten sind schwach
- **Task Model prüfen**: Ist ein leistungsstarkes Modell eingestellt?
- **Skill-Inhalt prüfen**: Sind die 5 Berater-Rollen klar definiert?
- **Web Search aktivieren**: Für aktuelle Fakten

### MOA Merge liefert keine gute Synthese
- **Task Model wechseln**: Ein stärkeres Synthesizer-Modell wählen
- **Manuelle Synthese**: Antworten selbst lesen und bewerten

---

## 10. Referenzen

- [Open WebUI Features](https://docs.openwebui.com/features/)
- [Pipe Function API](https://docs.openwebui.com/features/extensibility/plugin/functions/pipe/)
- [Multi-Model Chats](https://docs.openwebui.com/features/chat-conversations/chat-features/multi-model-chats/)
- [Open WebUI Prompts](https://docs.openwebui.com/features/)
- [OpenRouter API](https://openrouter.ai/docs)
- [alpha1visionai Claude Skills](https://github.com/alpha1visionai-stack/claude-skills)

---

*Dieses Handbuch wurde am 8. Juli 2026 erstellt. Alle Informationen basieren auf der aktuellen Open WebUI-Dokumentation und wurden durch Web-Recherche verifiziert.*
