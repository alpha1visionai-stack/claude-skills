---
name: agy-installer
description: Install the Antigravity CLI (agy) on a Windows machine. Use this skill when you need to set up the 'agy' command and its environment variables on a new Windows computer.
---

# Antigravity CLI (agy) Installer

This skill automates the setup of the Antigravity CLI (`agy`) on Windows systems.

## Workflow

1.  **Prepare the environment**: Ensure you are running on a Windows machine.
2.  **Run the installation script**: Execute the bundled PowerShell script to copy the binary, update the PATH, and optionally set the API key.

## Usage

To install `agy`, run the following command in PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\walte\agy-installer\scripts\install_agy.ps1" -ApiKey "YOUR_API_KEY_HERE"
```

*Note: Replace `YOUR_API_KEY_HERE` with your actual Google AI Studio API key if you want it to be configured during installation.*

## What the script does:
- Creates the directory `AppData\Local\agy\bin`.
- Copies `agy.exe` from the skill assets to the installation directory.
- Adds the installation directory to the user's `PATH` environment variable.
- Sets the `GOOGLE_API_KEY` environment variable (if provided).

## Post-Installation
After running the script, you **must restart your terminal** for the changes to take effect. You can then verify the installation by running:

```powershell
agy models
```
