---
name: notebooklm-py
description: Python API and CLI tool for Google NotebookLM automation
---

# NotebookLM-py Skill

This skill provides guidance for working with Google NotebookLM programmatically using the `notebooklm-py` Python library.

## Installation

Install the library globally:
```bash
pip install notebooklm-py
```

For browser-based authentication:
```bash
pip install "notebooklm-py[browser]"
```

## Authentication

Authenticate with Google NotebookLM:
```bash
notebooklm login
```

## Core Commands

### Notebook Management
- `notebooklm list` - List all notebooks
- `notebooklm create "Notebook Name"` - Create a new notebook
- `notebooklm show <notebook-id>` - Show notebook details

### Source Management
- `notebooklm add <notebook-id> <url>` - Add URL source
- `notebooklm add <notebook-id> <pdf-file>` - Add PDF source
- `notebooklm add <notebook-id> <youtube-url>` - Add YouTube video

### Content Generation
- `notebooklm generate audio <notebook-id> "prompt"` - Generate audio podcast
- `notebooklm generate video <notebook-id> "prompt"` - Generate video
- `notebooklm generate slides <notebook-id> "prompt"` - Generate slide deck

### Querying
- `notebooklm ask <notebook-id> "question"` - Ask questions about sources
- `notebooklm chat <notebook-id>` - Interactive chat session

## Important Notes

- Uses undocumented Google APIs that can change without notice
- Rate limiting applies to audio/video generation
- Processing times vary: sources (30s-10min), audio (10-20min), video (15-45min)
- Language setting is global (override with `--language` flag)

## Common Workflows

### Research → Podcast
1. Create notebook: `notebooklm create "Research Topic"`
2. Add sources: `notebooklm add <id> <url1> <url2>`
3. Generate audio: `notebooklm generate audio <id> "Create podcast about topic"`
4. Download when complete

### Document Analysis
1. Create notebook with documents
2. Use `notebooklm ask` to query content
3. Save answers as notes

## Integration with Claude Code

When working with NotebookLM in Claude Code projects:

1. Use explicit notebook IDs (`-n` flag) for parallel workflows
2. Check processing status with `notebooklm show <id>`
3. Download artifacts in preferred formats (MP3, MP4, PDF, JSON, etc.)
4. Handle rate limiting with appropriate delays

## Troubleshooting

- Authentication issues: Run `notebooklm login` again
- RPC errors: API may have changed - check repository for updates
- Rate limiting: Wait between resource-intensive operations