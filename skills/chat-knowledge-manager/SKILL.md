---
name: chat-knowledge-manager
description: Verarbeitung von Chat-Exporten zur Erstellung und Pflege einer "Collective Memory". Extrahiert Fakten, Namen und strategische Nuancen aus Nutzer-Prompts und erstellt sowohl konsolidierte Master-Dokumente als auch isolierte Einzel-Extraktionen.
---

# Chat Knowledge Manager

Dieser Skill unterstützt den Workflow zur Extraktion von Wissen aus großen Chat-Historien (z.B. JSON-Exporte). Er folgt der "Knowledge Builder v5.1" Logik für maximale Detailtiefe.

## Workflows

### 1. Master Knowledge Document Rebuild
Erstellt ein konsolidiertes Wissensdokument aus einer Liste von Prompts.
- **Input**: Eine Liste von Prompts (z.B. `extracted_prompts.txt`).
- **Prozess**: Iteratives Mergen (Prompt für Prompt) in ein zentrales Dokument.
- **Ziel**: Eine strukturierte Übersicht (Vision, Board, MD-Ebene, Recruiting, etc.).

### 2. Isolated Fact Extraction
Verarbeitet jeden Prompt einzeln, um die Verfälschung durch Merging zu verhindern.
- **Input**: Eine Liste von Prompts.
- **Output**: Für jeden Prompt eine separate Datei (`Prompt_N_Knowledge.md`) mit:
    - # Original Prompt N
    - # Extrahierte Fakten & Wissen

## Knowledge Builder v5.1 Logik
Beim Extrahieren von Fakten gelten folgende Regeln (siehe [references/knowledge-builder-logic.md](references/knowledge-builder-logic.md)):
- **Keine Kompression**: Granulare Details (Namen, Vorfälle, Zitate) haben Vorrang vor Kürze.
- **Kontext-Bewahrung**: "France Factor" (Sicherheitslage, Kultur, Recht) explizit markieren.
- **Iteratives Mergen**: Immer nur einen Prompt nach dem anderen in das Master-Dokument einarbeiten, um Detailverlust zu minimieren.

## Bundled Resources
- **Scripts**: `scripts/extract_prompts.py` - Extrahiert Nutzer-Prompts aus großen JSON-Exporten (umgeht 20MB Limits).
- **References**: `references/knowledge-builder-logic.md` - Detaillierte Anleitung zur Fakten-Extraktion.
- **Assets**: `assets/master-template.md` - Struktur-Vorlage für das Master-Dokument.
