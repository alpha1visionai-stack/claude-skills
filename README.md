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

## Skills nach Kategorie

### Entscheidung & Strategie
| Skill | Install | Beschreibung |
|---|---|---|
| `expert-council` | `npx skills add alpha1visionai-stack/claude-skills@expert-council -g -y` | Multi-Perspektiven-Entscheidungsframework mit llm-council CLI und /der-rat |
| `der-rat` | `npx skills add alpha1visionai-stack/claude-skills@der-rat -g -y` | 5 unabhängige KI-Berater prüfen Entscheidungen und liefern klares Urteil (Deutsch) |
| `brainstorming` | `npx skills add alpha1visionai-stack/claude-skills@brainstorming -g -y` | Strukturiertes Brainstorming vor kreativen oder Planungsaufgaben |
| `prd` | `npx skills add alpha1visionai-stack/claude-skills@prd -g -y` | Product Requirements Documents erstellen |

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
