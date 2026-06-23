---
name: document-consolidation
description: Use when you encounter binary documents (PDF, Word, Excel, PPTX) or cloud shortcuts (.gdoc, .gsheet) that need to be text-extracted, categorized into standard Markdown files, and archived.
---

# Document Consolidation Workflow

This skill automates the extraction, categorization, and archiving of documents according to the project's standards.

## When to Use

Trigger this skill when:
- The user provides new documents (PDF, Docx, etc.)
- You find un-consolidated files in a directory
- The user specifically asks to "consolidate documents" or "run markitdown"

## Core Workflow

1.  **Identify Documents**: Locate PDF, DOCX, XLSX, PPTX, or Google Cloud shortcuts.
2.  **Execute Consolidation**: Run the provided Python script to handle extraction and archiving.
3.  **Review Prompts**: Specifically look for system prompts or personas in the extracted content and ensure they are added to `system_prompts.md`.

## Execution

Run the consolidation script on a directory or a specific file:

```bash
# Process all documents in current directory
python d:/OneDrive/Dokumente/Codex/.Codex/skills/document-consolidation/scripts/consolidate_docs.py .

# Process a specific file
python d:/OneDrive/Dokumente/Codex/.Codex/skills/document-consolidation/scripts/consolidate_docs.py path/to/document.pdf
```

## Standard Mapping

Contents are automatically sorted into these files:
- `Angebote_Konzepte.md`: Proposals, pitches, and concepts.
- `Analysen_UseCases.md`: Detailed analyses and use cases.
- `Automatisierung_n8n.md`: n8n specific workflows and logic.
- `Kalkulationen_Kosten.md`: Budgets, prices, and calculations.
- `Meetings_Protokolle.md`: Meeting minutes and notes.
- `Manifest_Vision.md`: Strategic goals and manifestos.
- `Compliance_GDPR.md`: Legal and data protection info.
- `system_prompts.md`: **IMPORTANT** - All LLM instructions, personas, and /CMD lists.

## Post-Processing

After the script runs:
1. Verify the additions in the target Markdown files.
2. If the script missed a specific prompt extraction for `system_prompts.md`, manually refine it.
3. Inform the user which documents were processed and where the content went.
