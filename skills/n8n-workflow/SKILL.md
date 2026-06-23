---
name: n8n-workflow
description: Analysiert und erklärt n8n Workflows. Verwenden bei JSON Workflow-Dateien im N8N/ Ordner, um Knoten-Verbindungen, Datenflüsse und Trigger zu verstehen.
---

# n8n Workflow Analyse

Bei der Analyse von n8n Workflows:

## 1. Workflow-Struktur verstehen
- Identifiziere den **Trigger-Knoten** (z.B. Google Drive Trigger, Schedule)
- Verfolge den **Datenfluss** von links nach rechts durch die Knoten
- Erkenne **Verzweigungen** (Filter-Knoten, IF-Bedingungen)

## 2. Knoten-Typen analysieren

### Trigger-Knoten
- `googleDriveTrigger` - Überwacht Google Drive auf neue Dateien
- `scheduleTrigger` - Zeitgesteuerte Ausführung

### Verarbeitungs-Knoten
- `filter` - Bedingte Weiterleitung basierend auf mimeType etc.
- `code` - JavaScript-Code für benutzerdefinierte Logik
- `extractFromFile` - PDF/Text-Extraktion
- `merge` - Mehrere Eingaben zusammenführen

### AI/KI-Knoten
- `embeddingsOpenAi` - OpenAI Embeddings generieren
- `textSplitterRecursiveCharacterTextSplitter` - Text in Chunks aufteilen
- `documentDefaultDataLoader` - Dokumente für Vector Stores laden
- `vectorStorePinecone` - In Pinecone speichern/abfragen
- `chainSummarization` - Zusammenfassungs-Ketten

### Utility-Knoten
- `stickyNote` - Dokumentation/Notizen im Workflow

## 3. Verbindungen analysieren
- `main` - Standard-Datenfluss zwischen Knoten
- `ai_embedding` - Embeddings zu Vector Store
- `ai_document` - Dokumente zu Vector Store
- `ai_textSplitter` - Text Splitter zu Data Loader

## 4. Projekt-spezifische Konventionen

### Knowledge Pipeline Workflow
- **Trigger**: Google Drive (neue PDF/Text-Dateien)
- **Filter**: mimeType enthält "pdf" oder "text"
- **Extraktion**: PDF → Text, Text → Download
- **Bereinigung**: JavaScript-Code entfernt Timestamps/Formatierungen
- **Dual-Path**:
  - Path A: Full Document → Recursive Splitter → Pinecone (`growth-mindset`)
  - Path B: Summarization Chain → Token Splitter → Pinecone (`sum-growth-mindset`)
- **Cleanup**: Dateien werden nach `loaded` Ordner verschoben

### Wichtige IDs im Projekt
- Pinecone Index `growth-mindset` - Volle Dokumente
- Pinecone Index `sum-growth-mindset` - Zusammengefasste Dokumente
- OpenAI Embeddings: `text-embedding-3-small`
- Google Drive Ordner IDs sind in den Workflow-JSONs hinterlegt

## 5. Fehlerbehebung

Wenn Workflows nicht funktionieren:
1. Prüfe Credentials (Google Drive, OpenAI, Pinecone)
2. Verifiziere Knoten-Verbindungen (richtige Handles)
3. Checke Filter-Bedingungen (mimeType, etc.)
4. Teste JavaScript-Code im Code-Knoten separat
5. Prüfe Pinecone Index-Namen und Namespaces
