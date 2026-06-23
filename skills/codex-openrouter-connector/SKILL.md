---
name: codex-openrouter-connector
description: Configure the Codex CLI or desktop app to use OpenRouter. Use this skill when you want to connect Codex to OpenRouter models on a Windows machine.
---

# Codex OpenRouter Connector Setup

This skill automates the configuration of the Codex CLI / desktop application to allow OpenRouter models as AI models on a Windows machine.

## Workflow

1.  **Retrieve OpenRouter API Key**: Obtain a valid API key from [OpenRouter](https://openrouter.ai/).
2.  **Run the Configuration Script**: Run the included PowerShell script to update the `config.toml` file, set the permanent environment variable, and verify the setup.

## Usage

To configure OpenRouter for Codex on a new Windows computer, open a PowerShell terminal and run:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\walte\.gemini\skills\codex-openrouter-connector\scripts\configure_openrouter.ps1" -ApiKey "YOUR_OPENROUTER_API_KEY" -Model "google/gemini-2.5-pro"
```

*Note: Replace `YOUR_OPENROUTER_API_KEY` with your actual OpenRouter API key. You can also specify a different model name with the `-Model` parameter (e.g., `"anthropic/claude-3.5-sonnet"`).*

### Crucial Post-Setup Step
After running the script, **you must restart your active terminal, IDE (e.g. VS Code), or the Codex Desktop App** so that they can load the new `OPENROUTER_API_KEY` environment variable.

## What this skill does:
- Sets the `OPENROUTER_API_KEY` environment variable permanently for the current user.
- Configures `config.toml` at `~/.codex/config.toml` to:
  - Use `openrouter` as the `model_provider`.
  - Use `apikey` as `preferred_auth_method`.
  - Set the default active `model` to your chosen model.
  - Define the OpenRouter API endpoint, `wire_api = "responses"`, and key reference.
- Runs `codex doctor` to verify that Codex successfully parses the configuration and connects to OpenRouter.
