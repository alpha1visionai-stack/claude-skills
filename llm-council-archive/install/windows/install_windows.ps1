#==============================================================
# llm-council-skill Installer fuer Windows (PowerShell)
#
# Verwendung:
#   .\install_windows.ps1
#   .\install_windows.ps1 -ApiKey "sk-or-v1-xxxxxxxx"
#==============================================================

param(
    [string]$ApiKey = $env:OPENROUTER_API_KEY
)

$ErrorActionPreference = "Stop"

function Write-Info  { Write-Host "[INFO]  $args" -ForegroundColor Blue }
function Write-OK    { Write-Host "[OK]    $args" -ForegroundColor Green }
function Write-Warn2 { Write-Host "[WARN]  $args" -ForegroundColor Yellow }

Write-Host ""
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "  llm-council-skill Installer fuer Windows" -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host ""

# 1. Python pruefen
Write-Info "Python pruefen..."
try {
    $pyVer = python --version 2>&1
    Write-OK "Python gefunden: $pyVer"
} catch {
    Write-Warn2 "Python nicht gefunden. Bitte installiere Python 3.11+ von https://python.org"
    Write-Warn2 "Oder nutze: winget install Python.Python.3.13"
    exit 1
}

# 2. pip aktualisieren
Write-Info "pip aktualisieren..."
python -m pip install --upgrade pip --quiet 2>$null
Write-OK "pip bereit"

# 3. llm CLI installieren
Write-Info "llm CLI installieren..."
python -m pip install llm --quiet 2>$null
Write-OK "llm CLI installiert"

# 4. llm-council-skill installieren
Write-Info "llm-council-skill v0.2.0 installieren..."
python -m pip install llm-council-skill --quiet 2>$null
Write-OK "llm-council-skill installiert"

# 5. Plugins installieren
Write-Info "llm-gemini und llm-anthropic Plugins installieren..."
llm install llm-gemini 2>$null
llm install llm-anthropic 2>$null
Write-OK "Plugins installiert"

# 6. Verzeichnisse erstellen
Write-Info "Verzeichnisse erstellen..."
$dirs = @(
    "$env:USERPROFILE\.llm",
    "$env:USERPROFILE\.llm\logs",
    "$env:USERPROFILE\.codex",
    "$env:USERPROFILE\.agents\skills\der-rat",
    "$env:USERPROFILE\.agents\skills\expert-council"
)
foreach ($d in $dirs) {
    if (!(Test-Path $d)) { New-Item -ItemType Directory -Path $d -Force | Out-Null }
}
Write-OK "Verzeichnisse erstellt"

# 7. Konfiguration installieren
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$baseDir = Split-Path -Parent (Split-Path -Parent $scriptDir)

if (Test-Path "$baseDir\config\council-config.json") {
    Write-Info "council-config.json installieren..."
    Copy-Item "$baseDir\config\council-config.json" "$env:USERPROFILE\.llm\council-config.json" -Force
    Write-OK "Council-Konfiguration installiert"
}

if (Test-Path "$baseDir\config\AGENTS.md") {
    Write-Info "AGENTS.md installieren..."
    Copy-Item "$baseDir\config\AGENTS.md" "$env:USERPROFILE\.codex\AGENTS.md" -Force
    Write-OK "AGENTS.md installiert"
}

# 8. Skills installieren
if (Test-Path "$baseDir\skills\der-rat\SKILL.md") {
    Write-Info "Skill 'der-rat' installieren..."
    Copy-Item "$baseDir\skills\der-rat\SKILL.md" "$env:USERPROFILE\.agents\skills\der-rat\SKILL.md" -Force
    Write-OK "der-rat installiert"
}

if (Test-Path "$baseDir\skills\expert-council\SKILL.md") {
    Write-Info "Skill 'expert-council' installieren..."
    Copy-Item "$baseDir\skills\expert-council\SKILL.md" "$env:USERPROFILE\.agents\skills\expert-council\SKILL.md" -Force
    Write-OK "expert-council installiert"
}

# 9. API-Key setzen
if ($ApiKey -and $ApiKey.Length -gt 10) {
    Write-Info "OPENROUTER_API_KEY setzen..."
    [Environment]::SetEnvironmentVariable("OPENROUTER_API_KEY", $ApiKey, "User")
    $env:OPENROUTER_API_KEY = $ApiKey
    Write-OK "OPENROUTER_API_KEY gesetzt"
} else {
    Write-Warn2 "Kein API-Key uebergeben!"
    Write-Warn2 "Setze ihn: [Environment]::SetEnvironmentVariable('OPENROUTER_API_KEY', 'sk-or-v1-key', 'User')"
}

# 10. PYTHONIOENCODING
[Environment]::SetEnvironmentVariable("PYTHONIOENCODING", "utf-8", "User")
$env:PYTHONIOENCODING = "utf-8"
Write-OK "PYTHONIOENCODING=utf-8 gesetzt"

# 11. PowerShell-Alias
$profilePath = $PROFILE
if (Test-Path $profilePath) {
    $profileContent = Get-Content $profilePath -Raw
    if ($profileContent -notmatch 'function rat') {
        Write-Info "PowerShell-Alias 'rat' erstellen..."
        Add-Content $profilePath "`nfunction rat { llm-council --config `"$env:USERPROFILE\.llm\council-config.json`" @args }"
        Write-OK "Alias 'rat' hinzugefuegt"
    }
} else {
    Write-Info "PowerShell-Profil erstellen..."
    New-Item -ItemType File -Path $profilePath -Force | Out-Null
    Add-Content $profilePath "function rat { llm-council --config `"$env:USERPROFILE\.llm\council-config.json`" @args }"
    Write-OK "PowerShell-Profil mit Alias erstellt"
}

# 12. Verifikation
Write-Host ""
Write-Info "Installation verifizieren..."
Write-Host ""
Write-Host "  llm Version:          $(llm --version 2>$null)"
Write-Host "  llm-council:          $(where.exe llm-council 2>$null | Select-Object -First 1)"
Write-Host "  Council Config:       $(if (Test-Path "$env:USERPROFILE\.llm\council-config.json") {'OK'} else {'FEHLT'})"
Write-Host "  AGENTS.md:            $(if (Test-Path "$env:USERPROFILE\.codex\AGENTS.md") {'OK'} else {'FEHLT'})"
Write-Host "  Skill der-rat:        $(if (Test-Path "$env:USERPROFILE\.agents\skills\der-rat\SKILL.md") {'OK'} else {'FEHLT'})"
Write-Host "  Skill expert-council: $(if (Test-Path "$env:USERPROFILE\.agents\skills\expert-council\SKILL.md") {'OK'} else {'FEHLT'})"
Write-Host "  API-Key:              $(if ($ApiKey) {'gesetzt'} else {'nicht gesetzt'})"

# 13. Dry-Run Test
if ($ApiKey) {
    Write-Host ""
    Write-Info "Dry-Run Test..."
    llm-council --config "$env:USERPROFILE\.llm\council-config.json" --dry-run "Test" 2>&1
}

Write-Host ""
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "  Installation abgeschlossen!" -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Naechste Schritte:"
Write-Host "    1. Terminal neu starten"
Write-Host "    2. Council testen:   rat --dry-run 'Testfrage'"
Write-Host "    3. Echte Frage:      rat 'Soll ich X oder Y?'"
Write-Host ""
