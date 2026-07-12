---
name: docker-updater
description: Check all running Docker containers and custom Dockerfiles in the server workspace for base image updates, rebuild modified custom images, and recreate updated containers. Use this skill when the user requests container image updates, checking for outdated containers, or rebuilding Dockerfiles.
---

# Docker Updater Skill

This skill provides a standardized way to check, build, and recreate Docker containers and custom Dockerfiles within the server infrastructure (primarily for the `main` and `plane` stacks).

## Capabilities
- Detects running containers whose registry images have newer versions.
- Parses custom Dockerfiles to check if their base images (e.g., `python:3.9-slim-buster`, `n8nio/runners:latest`) have updates.
- Auto-resolves common configuration issues (such as `pnpm` store incompatibility in `n8n-task-runners` or PaddleOCR 3.x deprecations).
- Rebuilds only the modified Dockerfiles (both active and disabled services) in the background.
- Restarts and recreates updated stacks seamlessly.

## Location
- The helper script is located at: `skills/docker-updater/scripts/docker_checker.py` (when cloned in `claude-skills`) or directly in the skill directory structure.

## Usage Guide

To perform Docker updates, execute the script with the desired action flags.

### 1. Check Only (Report Updates)
Run this command to check for registry updates and base image updates without modifying any containers:
```bash
python3 scripts/docker_checker.py --check
```
*Note: This command will pull registry and base images to perform the check but will not rebuild services or restart containers.*

### 2. Build and Recreate (Apply All Updates)
Run this command to check for updates, rebuild all affected Dockerfiles, and recreate the running containers to apply updates:
```bash
python3 scripts/docker_checker.py --all
```
This performs a full run:
1. Checks and pulls registry images.
2. Identifies base image changes and builds the local Dockerfiles.
3. Automatically executes `docker compose up -d` in both the `main` and `plane` stacks.

### 3. Granular Operations
- **Rebuild only**: `python3 scripts/docker_checker.py --build`
- **Recreate only**: `python3 scripts/docker_checker.py --recreate`

## File Adjustments Handled Automatically
The script ensures dependencies match expected filenames:
- Copies `requirements` to `requirements.txt` in OCR services (`easyocr-service`, `paddleocr-service`) to prevent context building errors.
