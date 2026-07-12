---
name: n8n-sandbox-manager
description: Install, configure, and manage the official self-hosted n8n-sandbox-service to enable the n8n AI Assistant (Preview) workflow builder without external cloud dependencies.
---

# n8n Sandbox Manager Skill

This skill provides a standardized way to set up, configure, verify, and uninstall the official **n8n Sandbox Service** (Docker-in-Docker) to enable the native AI Assistant workflow builder on self-hosted n8n instances.

## Capabilities
- **Automated setup**: Injects the required Docker-in-Docker sandbox containers (`n8n-sandbox-api`, `n8n-sandbox-runner`, and `tls-init`) into `docker-compose.yml`.
- **API and token generation**: Automatically generates secure 24-character random API keys and mTLS authentication tokens and saves them in the `.env` file.
- **mTLS Bootstrap**: Automatically configures the certificate generation (`tls-init`) for secure communication between n8n, the sandbox API, and the runner.
- **Status check**: Inspects container states and verifies gRPC registration heartbeat logs.
- **Clean uninstallation**: Removes all injected variables, containers, and volume definitions safely.

## Location
- The script is located at: `skills/n8n-sandbox-manager/scripts/sandbox_setup.py` (when cloned in `claude-skills`) or directly in the skill directory structure.

## Usage Guide

Run the python manager script to manage the sandbox lifecycle.

### 1. Set Up the Sandbox
Run this command to automatically generate keys, update `.env` and `docker-compose.yml`, pull required images, and restart the stack:
```bash
python3 scripts/sandbox_setup.py --setup
```
*(By default, this will set the AI Assistant model to `openai/gpt-4o-mini` with a placeholder key. You can specify a custom model and API key during setup:)*
```bash
python3 scripts/sandbox_setup.py --setup --model openrouter/z-ai/glm-5.2 --key YOUR_API_KEY
```

### 2. Verify Sandbox Status
Run this command to inspect the state of the sandbox containers and check runner-to-API registration:
```bash
python3 scripts/sandbox_setup.py --status
```
*Expected Output:*
```
=== Checking Sandbox Service Status ===
Container 'n8n-sandbox-api': RUNNING
Container 'n8n-sandbox-runner': RUNNING
Container 'n8n': RUNNING

Checking runner registration logs...
[SUCCESS] Sandbox runner registration stream established with API.
```

### 3. Uninstall/Remove Sandbox
To clean up the sandbox configuration and return the stack to a standard setup, run:
```bash
python3 scripts/sandbox_setup.py --remove
```
*Note: This stops the containers, cleans up the injected sections from both `docker-compose.yml` and `.env`, and restarts the remaining services.*
