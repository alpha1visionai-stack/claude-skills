# alpha1visionai Claude Skills

Shared Claude Code skills for the alpha1visionai team. Install any skill globally with one command:

```bash
npx skills add alpha1visionai-stack/claude-skills@<skill-name> -g -y
```

---

## Quick Start

```bash
# Einzelnen Skill installieren
npx skills add alpha1visionai-stack/claude-skills@expert-council -g -y

# Alle Skills auf einmal installieren (PowerShell)
@("expert-council","der-rat","n8n-workflow","karpathy-guidelines","brainstorming") | ForEach-Object {
    npx skills add alpha1visionai-stack/claude-skills@$_ -g -y
}
```

---

## llm-council-archive

Komplettes Archiv zur Installation und Nutzung der Multi-Modell-Beratungssysteme
**"Der Rat"** (Chat-basiert, 5 Perspektiven in einem Modell) und **"Expert Council"**
(CLI-basiert, 5 echte Modelle parallel mit anonymer Peer-Review).

### Inhalt

```
llm-council-archive/
├── README.md                              # Anleitung + Schnellstart
├── docs/
│   ├── Der_Rat_und_Expert_Council_Dokumentation.md   # Vollständige Doku (559 Zeilen)
│   └── llm-council-handbuch.html                      # HTML-Handbuch
├── skills/
│   ├── der-rat/SKILL.md                   # Rat-Skill (Chat-basiert)
│   └── expert-council/SKILL.md            # Council-Skill (CLI-basiert)
├── config/
│   ├── council-config.json                # 5-Modell-Konfiguration
│   └── AGENTS.md                          # Web-Grounding-Pflicht
├── install/
│   ├── ubuntu/install_ubuntu.sh           # Ubuntu-Installer
│   └── windows/install_windows.ps1        # Windows-Installer
└── logs/
    └── 3 Beispiel-Runs (*.jsonl)          # Live Council-Sitzungen
```

### Ein-Klick-Installation

```bash
# Ubuntu / Linux
cd llm-council-archive
chmod +x install/ubuntu/install_ubuntu.sh
./install/ubuntu/install_ubuntu.sh "sk-or-v1-dein-openrouter-key"

# Windows (PowerShell)
cd llm-council-archive
.\install\windows\install_windows.ps1 -ApiKey "sk-or-v1-dein-openrouter-key"
```

Der Installer richtet automatisch: Python 3.11+, llm CLI, llm-council-skill,
LLM-Plugins (Gemini, Anthropic), Konfiguration, Shell-Alias `rat` und beide Skills.

> 💡 Benötigt wird ein [OpenRouter API-Key](https://openrouter.ai/keys) für den Zugriff auf alle Modelle über einen einzigen Provider.

### Konfigurierte Modelle

| Rolle | Modell | Provider |
|-------|--------|----------|
| Berater 1 | Claude Opus 4.8 | OpenRouter |
| Berater 2 | GPT-5.5 | OpenRouter |
| Berater 3 | Gemini Pro Latest | OpenRouter |
| Berater 4 | GLM-5.2 | OpenRouter |
| Berater 5 | Grok 4.3 | OpenRouter |
| Vorsitzender | Claude Opus 4.8 | OpenRouter |

Geschätzte Kosten: ~0,10–0,15 USD pro Sitzung (11 API-Calls).

→ Vollständige Anleitung: [`llm-council-archive/README.md`](llm-council-archive/README.md)

---

## Skills nach Kategorie

### Entscheidung & Strategie
| Skill | Install | Beschreibung |
|---|---|---|
| `expert-council` | `npx skills add alpha1visionai-stack/claude-skills@expert-council -g -y` | Multi-Perspektiven-Entscheidungsframework: 5 echte Modelle parallel mit anonymer Peer-Review via llm-council CLI |
| `der-rat` | `npx skills add alpha1visionai-stack/claude-skills@der-rat -g -y` | 5 unabhängige KI-Berater prüfen Entscheidungen und liefern klares Urteil (Chat-basiert, Deutsch) |
| `brainstorming` | `npx skills add alpha1visionai-stack/claude-skills@brainstorming -g -y` | Strukturiertes Brainstorming vor kreativen oder Planungsaufgaben |
| `klartext-auftrag` | `npx skills add alpha1visionai-stack/claude-skills@klartext-auftrag -g -y` | Aufträge und Anforderungen in Klartext-Format strukturieren (Deutsch) |
| `prd` | `npx skills add alpha1visionai-stack/claude-skills@prd -g -y` | Product Requirements Documents erstellen |

### OKR-Planung & Ziele
| Skill | Install | Beschreibung |
|---|---|---|
| `brainstorm-okrs` | `npx skills add alpha1visionai-stack/claude-skills@brainstorm-okrs -g -y` | OKR-Brainstorming und Ideensammlung für Ziele |
| `okr-plane` | `npx skills add alpha1visionai-stack/claude-skills@okr-plane -g -y` | OKRs mit Plane-Integration planen und verwalten |
| `foundation-okr-writer` | `npx skills add alpha1visionai-stack/claude-skills@foundation-okr-writer -g -y` | Foundation OKRs schreiben und validieren |
| `setting-okrs-goals` | `npx skills add alpha1visionai-stack/claude-skills@setting-okrs-goals -g -y` | OKRs und Ziele für Teams definieren und setzen |
| `team-okrs` | `npx skills add alpha1visionai-stack/claude-skills@team-okrs -g -y` | Team-OKRs erstellen und visualisieren |

### n8n & Automatisierung
| Skill | Install | Beschreibung |
|---|---|---|
| `n8n-workflow` | `npx skills add alpha1visionai-stack/claude-skills@n8n-workflow -g -y` | n8n Workflow-Analyse und -Erklärung |
| `n8n-workflow-patterns` | `npx skills add alpha1visionai-stack/claude-skills@n8n-workflow-patterns -g -y` | Bewährte Workflow-Architekturmuster |
| `n8n-code-javascript` | `npx skills add alpha1visionai-stack/claude-skills@n8n-code-javascript -g -y` | JavaScript in n8n Code-Nodes schreiben |
| `n8n-code-python` | `npx skills add alpha1visionai-stack/claude-skills@n8n-code-python -g -y` | Python in n8n Code-Nodes schreiben |
| `n8n-expression-syntax` | `npx skills add alpha1visionai-stack/claude-skills@n8n-expression-syntax -g -y` | n8n Expressions validieren und Fehler beheben |
| `n8n-node-configuration` | `npx skills add alpha1visionai-stack/claude-skills@n8n-node-configuration -g -y` | Node-Konfiguration und Operation-Guidance |
| `n8n-validation-expert` | `npx skills add alpha1visionai-stack/claude-skills@n8n-validation-expert -g -y` | Validierungsfehler interpretieren und beheben |
| `n8n-mcp-tools-expert` | `npx skills add alpha1visionai-stack/claude-skills@n8n-mcp-tools-expert -g -y` | n8n MCP-Tools effektiv einsetzen |

### Frontend & Design
| Skill | Install | Beschreibung |
|---|---|---|
| `alpha-inspiration-design` | `npx skills add alpha1visionai-stack/claude-skills@alpha-inspiration-design -g -y` | Web-UIs und Komponenten im alpha1visionai Designstil |
| `frontend-design` | `npx skills add alpha1visionai-stack/claude-skills@frontend-design -g -y` | Produktionsreife Frontend-Interfaces mit hoher Designqualität |
| `shadcn-ui` | `npx skills add alpha1visionai-stack/claude-skills@shadcn-ui -g -y` | shadcn/ui Komponenten integrieren und aufbauen |
| `vercel-react-best-practices` | `npx skills add alpha1visionai-stack/claude-skills@vercel-react-best-practices -g -y` | React & Next.js Performance-Optimierung nach Vercel-Standard |
| `vercel-react-view-transitions` | `npx skills add alpha1visionai-stack/claude-skills@vercel-react-view-transitions -g -y` | Smooth Animationen mit React View Transitions |
| `react-components` | `npx skills add alpha1visionai-stack/claude-skills@react-components -g -y` | Stitch-Designs in Vite/React-Komponenten konvertieren |
| `remotion` | `npx skills add alpha1visionai-stack/claude-skills@remotion -g -y` | Walkthrough-Videos mit Remotion generieren |

### Stitch (Design-System)
| Skill | Install | Beschreibung |
|---|---|---|
| `stitch-generate-design` | `npx skills add alpha1visionai-stack/claude-skills@stitch-generate-design -g -y` | Designs in Stitch generieren |
| `stitch-loop` | `npx skills add alpha1visionai-stack/claude-skills@stitch-loop -g -y` | Websites iterativ mit Stitch aufbauen |
| `stitch-code-to-design` | `npx skills add alpha1visionai-stack/claude-skills@stitch-code-to-design -g -y` | Code in Stitch-Design umwandeln |
| `stitch-extract-design-md` | `npx skills add alpha1visionai-stack/claude-skills@stitch-extract-design-md -g -y` | Design-System aus Stitch extrahieren |
| `stitch-extract-static-html` | `npx skills add alpha1visionai-stack/claude-skills@stitch-extract-static-html -g -y` | Statisches HTML aus Stitch exportieren |
| `stitch-manage-design-system` | `npx skills add alpha1visionai-stack/claude-skills@stitch-manage-design-system -g -y` | Design-System in Stitch verwalten |
| `stitch-react-native` | `npx skills add alpha1visionai-stack/claude-skills@stitch-react-native -g -y` | Stitch-Designs in React Native konvertieren |
| `stitch-upload-to-stitch` | `npx skills add alpha1visionai-stack/claude-skills@stitch-upload-to-stitch -g -y` | Designs zu Stitch hochladen |
| `taste-design` | `npx skills add alpha1visionai-stack/claude-skills@taste-design -g -y` | Semantisches Design-System für Stitch |
| `design-md` | `npx skills add alpha1visionai-stack/claude-skills@design-md -g -y` | Design-System in DESIGN.md dokumentieren |
| `enhance-prompt` | `npx skills add alpha1visionai-stack/claude-skills@enhance-prompt -g -y` | UI-Ideen in optimierte Stitch-Prompts umwandeln |

### Dokumentation & Wissen
| Skill | Install | Beschreibung |
|---|---|---|
| `document-consolidation` | `npx skills add alpha1visionai-stack/claude-skills@document-consolidation -g -y` | PDF/Word/Excel/PPTX mit markitdown konsolidieren |
| `document-skills` | `npx skills add alpha1visionai-stack/claude-skills@document-skills -g -y` | Spezialisierte Skills für DOCX, PDF, PPTX und XLSX-Verarbeitung |
| `documentation-writer` | `npx skills add alpha1visionai-stack/claude-skills@documentation-writer -g -y` | Technische Dokumentation nach Diátaxis-Standard |
| `doc-coauthoring` | `npx skills add alpha1visionai-stack/claude-skills@doc-coauthoring -g -y` | Strukturierter Workflow für kollaborative Dokumentation |
| `writing-plans` | `npx skills add alpha1visionai-stack/claude-skills@writing-plans -g -y` | Implementierungspläne vor mehrstufigen Aufgaben schreiben |
| `notebooklm` | `npx skills add alpha1visionai-stack/claude-skills@notebooklm -g -y` | Google NotebookLM vollständige API |
| `notebooklm-py` | `npx skills add alpha1visionai-stack/claude-skills@notebooklm-py -g -y` | NotebookLM Python API & CLI |
| `notebooklm-skill` | `npx skills add alpha1visionai-stack/claude-skills@notebooklm-skill -g -y` | NotebookLM direkt aus Claude abfragen |
| `youtube-skill` | `npx skills add alpha1visionai-stack/claude-skills@youtube-skill -g -y` | YouTube-Transkripte und Metadaten extrahieren |

### Code-Qualität & Reviews
| Skill | Install | Beschreibung |
|---|---|---|
| `karpathy-guidelines` | `npx skills add alpha1visionai-stack/claude-skills@karpathy-guidelines -g -y` | Karpathys Richtlinien zur Vermeidung typischer LLM-Coding-Fehler |
| `requesting-code-review` | `npx skills add alpha1visionai-stack/claude-skills@requesting-code-review -g -y` | Code-Reviews richtig anfordern |
| `receiving-code-review` | `npx skills add alpha1visionai-stack/claude-skills@receiving-code-review -g -y` | Code-Review-Feedback umsetzen |
| `executing-plans` | `npx skills add alpha1visionai-stack/claude-skills@executing-plans -g -y` | Implementierungspläne in separater Session ausführen |

### Tools & Infrastruktur
| Skill | Install | Beschreibung |
|---|---|---|
| `mcp-builder` | `npx skills add alpha1visionai-stack/claude-skills@mcp-builder -g -y` | Hochwertige MCP-Server erstellen |
| `mcp-pi` | `npx skills add alpha1visionai-stack/claude-skills@mcp-pi -g -y` | MCP einrichten, konfigurieren und nutzen |
| `google-drive-skill` | `npx skills add alpha1visionai-stack/claude-skills@google-drive-skill -g -y` | Google Drive Dateien und Ordner verwalten |
| `google-workspace-cli` | `npx skills add alpha1visionai-stack/claude-skills@google-workspace-cli -g -y` | Google Workspace CLI (Drive, Gmail, Calendar, Sheets) |
| `file-organizer` | `npx skills add alpha1visionai-stack/claude-skills@file-organizer -g -y` | Dateien und Ordner intelligent organisieren |
| `invoice-organizer` | `npx skills add alpha1visionai-stack/claude-skills@invoice-organizer -g -y` | Rechnungen und Belege für die Steuer organisieren |

### Skills & Skill-Management
| Skill | Install | Beschreibung |
|---|---|---|
| `skill-creator` | `npx skills add alpha1visionai-stack/claude-skills@skill-creator -g -y` | Effektive Skills erstellen |
| `claude-skills-starter` | `npx skills add alpha1visionai-stack/claude-skills@claude-skills-starter -g -y` | Starter-Template für Claude-Skills und Workflows |
| `skill-manager` | `npx skills add alpha1visionai-stack/claude-skills@skill-manager -g -y` | Bestehendes Skill-System verwalten |
| `find-skills` | `npx skills add alpha1visionai-stack/claude-skills@find-skills -g -y` | Skills im Open-Agent-Ökosystem entdecken |
| `writing-skills` | `npx skills add alpha1visionai-stack/claude-skills@writing-skills -g -y` | Skills erstellen, bearbeiten und testen (TDD-Ansatz) |
| `site-builder` | `npx skills add alpha1visionai-stack/claude-skills@site-builder -g -y` | Websites aufbauen |
| `backup-claude` | `npx skills add alpha1visionai-stack/claude-skills@backup-claude -g -y` | Claude-Konfiguration sichern |
| `lead-research-assistant` | `npx skills add alpha1visionai-stack/claude-skills@lead-research-assistant -g -y` | Hochwertige Leads durch Zielgruppen-Analyse identifizieren |
| `meeting-insights-analyzer` | `npx skills add alpha1visionai-stack/claude-skills@meeting-insights-analyzer -g -y` | Meeting-Transkripte auf Muster und Insights analysieren |

---

## Neuen Skill hinzufügen

1. Ordner `skills/<skill-name>/` anlegen
2. `SKILL.md` mit YAML-Frontmatter erstellen:
   ```markdown
   ---
   name: skill-name
   description: "Use when ..."
   ---
   ```
3. PR erstellen → nach Merge sofort installierbar:
   ```bash
   npx skills add alpha1visionai-stack/claude-skills@skill-name -g -y
   ```

---

## Empfohlene Skills für neue Teammitglieder

```bash
npx skills add alpha1visionai-stack/claude-skills@expert-council -g -y
npx skills add alpha1visionai-stack/claude-skills@der-rat -g -y
npx skills add alpha1visionai-stack/claude-skills@karpathy-guidelines -g -y
npx skills add alpha1visionai-stack/claude-skills@n8n-workflow -g -y
npx skills add alpha1visionai-stack/claude-skills@brainstorming -g -y
```

### Kreativ & Medien
| Skill | Install | Beschreibung |
|---|---|---|
| `ascii-video` | `npx skills add alpha1visionai-stack/claude-skills@ascii-video -g -y` | ASCII-Art Videos generieren |
| `manim-video` | `npx skills add alpha1visionai-stack/claude-skills@manim-video -g -y` | Mathematische Animationen mit Manim erstellen |
| `popular-web-designs` | `npx skills add alpha1visionai-stack/claude-skills@popular-web-designs -g -y` | Bekannte Web-Designs nachbauen und analysieren |
| `songwriting-and-ai-music` | `npx skills add alpha1visionai-stack/claude-skills@songwriting-and-ai-music -g -y` | Songwriting und KI-Musik-Generierung |
| `youtube-content` | `npx skills add alpha1visionai-stack/claude-skills@youtube-content -g -y` | YouTube-Content-Strategie und -Analyse |
| `powerpoint` | `npx skills add alpha1visionai-stack/claude-skills@powerpoint -g -y` | PowerPoint-Präsentationen erstellen und bearbeiten |
| `gopro-exif-injector` | `npx skills add alpha1visionai-stack/claude-skills@gopro-exif-injector -g -y` | GoPro EXIF-Injektion, Sensor-Realismus, DxO Nik 7 Color Efex ('Ai-gen-2') & Silver Efex ('019 - Fine Art Process') |
| `luminar-preset-converter` | `npx skills add alpha1visionai-stack/claude-skills@luminar-preset-converter -g -y` | Lightroom & Luminar Presets (.xmp/.lmp) in Luminar Neo Format konvertieren |
| `instagram-publisher` | `npx skills add alpha1visionai-stack/claude-skills@instagram-publisher -g -y` | Automatisiertes Veröffentlichen von Bildern, Bildunterschriften und Hashtags auf Instagram via Playwright |

### Textprüfung & Qualität
| Skill | Install | Beschreibung |
|---|---|---|
| `ki-text-check` | `npx skills add alpha1visionai-stack/claude-skills@ki-text-check -g -y` | Deutsche Texte auf KI-Erzeugung prüfen — Indizienbefund mit Fundstellen statt Blackbox-Prozentzahl, vollständig offline |
| `ki-text-umschreiben` | `npx skills add alpha1visionai-stack/claude-skills@ki-text-umschreiben -g -y` | Maschinell klingende Texte überarbeiten — gezielt gegen die Befunde aus ki-text-check, ohne Fakten zu erfinden |

### Research & Data
| Skill | Install | Beschreibung |
|---|---|---|
| `huggingface-hub` | `npx skills add alpha1visionai-stack/claude-skills@huggingface-hub -g -y` | HuggingFace Hub — Modelle, Datasets, Spaces verwalten |
| `polymarket` | `npx skills add alpha1visionai-stack/claude-skills@polymarket -g -y` | Polymarket Prediction Markets analysieren |

### Tools & Integrationen (aus Gemini/Codex)
| Skill | Install | Beschreibung |
|---|---|---|
| `agy-installer` | `npx skills add alpha1visionai-stack/claude-skills@agy-installer -g -y` | AGY-Installer-Workflow |
| `chat-knowledge-manager` | `npx skills add alpha1visionai-stack/claude-skills@chat-knowledge-manager -g -y` | Chat-Wissen strukturiert verwalten |
| `codex-openrouter-connector` | `npx skills add alpha1visionai-stack/claude-skills@codex-openrouter-connector -g -y` | Codex mit OpenRouter verbinden |
| `mcp-setup-claude-cowork` | `npx skills add alpha1visionai-stack/claude-skills@mcp-setup-claude-cowork -g -y` | MCP-Setup für Claude Co-Working |
| `tax-automation-consultant` | `npx skills add alpha1visionai-stack/claude-skills@tax-automation-consultant -g -y` | Steuererfassung (EÜR/USt) automatisieren |
| `playwright` | `npx skills add alpha1visionai-stack/claude-skills@playwright -g -y` | Browser-Automatisierung via Playwright CLI |
| `codex-primary-runtime` | `npx skills add alpha1visionai-stack/claude-skills@codex-primary-runtime -g -y` | Codex Primary Runtime Konfiguration |
