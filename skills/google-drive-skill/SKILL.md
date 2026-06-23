---
name: google-drive-skill
description: Use when accessing Google Drive files, listing folders, uploading documents, or searching Drive content programmatically from Codex.
---

# Google Drive Skill

## Overview
Python-based skill for Google Drive API operations using OAuth2 authentication. Direct API integration without MCP overhead.

## When to Use
- List files and folders in Google Drive
- Upload documents to specific folders
- Download files for local processing
- Search Drive content by name or type
- Move or copy files between folders

## Requirements

1. **Google Cloud Project**: https://console.cloud.google.com/
2. **Enable Drive API**: APIs & Services > Library > Google Drive API
3. **OAuth2 Credentials**: APIs & Services > Credentials > Create OAuth 2.0 Client ID
4. **Download credentials.json** and place in project `.credentials/google-drive/`

## Quick Reference

| Operation | Script | Example |
|-----------|--------|---------|
| List files | list_files.py | `--folder-id <id>` |
| Upload | upload_file.py | `--file <path> --folder-id <id>` |
| Download | download_file.py | `--file-id <id> --output <path>` |
| Search | search_files.py | `--query "name contains 'Report'"` |

## Setup

### 1. Environment Variables (.env)
```
GOOGLE_DRIVE_CREDENTIALS_PATH=C:\Users\walte\.credentials\google-drive\credentials.json
GOOGLE_DRIVE_TOKEN_PATH=C:\Users\walte\.credentials\google-drive\token.json
```

### 2. First Run (Authentication)
The first execution opens a browser for OAuth2 consent. Token is saved for subsequent runs.

### 3. Usage
```bash
python scripts/list_files.py --max-results 50
python scripts/upload_file.py --file "document.pdf" --folder-id "ABC123"
```

## Error Handling
- **Token expired**: Script auto-refreshes or re-authenticates
- **Permission denied**: Check sharing settings in Drive
- **Rate limit**: Automatic retry with exponential backoff

## Security Notes
- Never commit `credentials.json` or `token.json`
- Token auto-refresh handled internally
- Scope limited to `drive.readonly` or `drive.file` as configured
