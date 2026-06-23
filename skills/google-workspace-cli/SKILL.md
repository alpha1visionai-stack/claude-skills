---
name: google-workspace-cli
description: CLI tool for Google Workspace APIs including Drive, Gmail, Calendar, Sheets, Docs, and Chat
---

# Google Workspace CLI Skill

This skill provides guidance for working with Google Workspace services programmatically using the `gws` command-line tool.

## Installation

Install the CLI globally:
```bash
npm install -g @googleworkspace/cli
```

## Authentication

Set up authentication with Google Workspace:
```bash
gws auth setup    # Configure GCP project + OAuth client (requires gcloud)
gws auth login    # Authenticate via OAuth2 (opens browser)
```

## Core Commands

### Service Discovery
- `gws <service> <resource> <method>` - Execute API methods
- `gws schema <service.resource.method>` - View API schema

### Common Services
- **Drive**: `gws drive files list` - List files
- **Gmail**: `gws gmail users messages list` - List emails
- **Calendar**: `gws calendar events list` - List events
- **Sheets**: `gws sheets spreadsheets get` - Get spreadsheet
- **Docs**: `gws docs documents get` - Get document
- **Chat**: `gws chat spaces messages list` - List chat messages

## Command Structure

All commands follow this pattern:
```bash
gws <service> <resource> [sub-resource] <method> [flags]
```

### Available Services
- `drive` - Manage files, folders, and shared drives
- `sheets` - Read and write spreadsheets
- `gmail` - Send, read, and manage email
- `calendar` - Manage calendars and events
- `admin-reports` - Audit logs and usage reports
- `docs` - Read and write Google Docs
- `slides` - Read and write presentations
- `tasks` - Manage task lists and tasks
- `people` - Manage contacts and profiles
- `chat` - Manage Chat spaces and messages
- `classroom` - Manage classes, rosters, and coursework
- `forms` - Read and write Google Forms
- `keep` - Manage Google Keep notes
- `meet` - Manage Google Meet conferences
- `events` - Subscribe to Google Workspace events
- `modelarmor` - Filter user-generated content for safety
- `workflow` - Cross-service productivity workflows
- `script` - Manage Google Apps Script projects

## Common Flags

- `--params <JSON>` - URL/Query parameters as JSON
- `--json <JSON>` - Request body as JSON (POST/PATCH/PUT)
- `--upload <PATH>` - Upload local file as media content
- `--output <PATH>` - Output file path for binary responses
- `--format <FMT>` - Output format: json (default), table, yaml, csv
- `--page-all` - Auto-paginate, one JSON line per page
- `--page-limit <N>` - Max pages to fetch

## Common Workflows

### List Drive Files
```bash
gws drive files list --params '{"pageSize": 10}'
```

### Get Specific File
```bash
gws drive files get --params '{"fileId": "abc123"}'
```

### List Gmail Messages
```bash
gws gmail users messages list --params '{"userId": "me"}'
```

### Get Spreadsheet Data
```bash
gws sheets spreadsheets get --params '{"spreadsheetId": "..."}'
```

### Upload File to Drive
```bash
gws drive files create --upload ./file.txt --json '{"name": "file.txt"}'
```

## Environment Variables

- `GOOGLE_WORKSPACE_CLI_TOKEN` - Pre-obtained OAuth2 access token
- `GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE` - Path to OAuth credentials JSON
- `GOOGLE_WORKSPACE_CLI_CLIENT_ID` - OAuth client ID
- `GOOGLE_WORKSPACE_CLI_CLIENT_SECRET` - OAuth client secret
- `GOOGLE_WORKSPACE_CLI_CONFIG_DIR` - Override config directory

## Error Handling

### Exit Codes
- `0` - Success
- `1` - API error (Google returned an error response)
- `2` - Auth error (credentials missing or invalid)
- `3` - Validation (bad arguments or input)
- `4` - Discovery (could not fetch API schema)
- `5` - Internal (unexpected failure)

### Common Issues
- **Auth errors**: Run `gws auth login` to re-authenticate
- **Validation errors**: Check command syntax and parameters
- **API errors**: Verify permissions and resource existence

## Dynamic API Discovery

The CLI dynamically generates commands from Google's Discovery Service at runtime, automatically picking up new endpoints when Google adds them.

## Integration with Codex

When working with Google Workspace in Codex projects:

1. Use structured JSON output for parsing responses
2. Handle pagination with `--page-all` flag for large datasets
3. Use `--format table` for human-readable output
4. Handle authentication tokens securely
5. Use appropriate error handling for API responses

## Important Notes

- This is not an officially supported Google product
- Uses Google's Discovery Service for dynamic command generation
- All responses return as valid JSON, ideal for scripting and AI integration
- Supports multiple authentication methods
- Includes 40+ helper commands for common workflows