param (
    [Parameter(Mandatory=$true)]
    [string]$ApiKey,
    
    [Parameter(Mandatory=$false)]
    [string]$Model = "google/gemini-2.5-pro"
)

# 1. Resolve Codex Home directory
$codexHome = Join-Path $env:USERPROFILE ".codex"
$configPath = Join-Path $codexHome "config.toml"

if (-not (Test-Path $codexHome)) {
    New-Item -ItemType Directory -Path $codexHome -Force | Out-Null
}

# 2. Set Environment Variable permanently for the User
[System.Environment]::SetEnvironmentVariable("OPENROUTER_API_KEY", $ApiKey, "User")
# Also set in the current session so doctor can use it immediately
$env:OPENROUTER_API_KEY = $ApiKey

# 3. Read or create config.toml
if (Test-Path $configPath) {
    $content = Get-Content $configPath -Raw
} else {
    $content = ""
}

# We want to insert or update the model, model_provider, preferred_auth_method
# Let's remove any existing global definition of model, model_provider, preferred_auth_method to avoid duplicates
$lines = $content -split "`r?`n"
$newLines = @()
$skipHeaderKeys = @("model", "model_provider", "preferred_auth_method")
$inProviderBlock = $false

foreach ($line in $lines) {
    $trimmed = $line.Trim()
    
    # Identify if we enter a table block
    if ($trimmed.StartsWith("[")) {
        if ($trimmed -eq "[model_providers.openrouter]") {
            $inProviderBlock = $true
            continue
        } else {
            $inProviderBlock = $false
        }
    }
    
    if ($inProviderBlock) {
        # Skip lines in the old openrouter block
        continue
    }
    
    # Check if it's one of our global keys before any block
    # (Only matches keys at the root, before any table `[` is defined)
    $isRootKey = $false
    foreach ($key in $skipHeaderKeys) {
        if ($trimmed -match "^$key\s*=") {
            # Check if we have seen a table block yet
            # Since root keys must be defined before any table, we only skip if we are at the root
            $hasSeenTable = $false
            for ($i = 0; $i -lt $newLines.Count; $i++) {
                if ($newLines[$i].Trim().StartsWith("[")) {
                    $hasSeenTable = $true
                    break
                }
            }
            if (-not $hasSeenTable) {
                $isRootKey = $true
            }
        }
    }
    
    if ($isRootKey) {
        continue
    }
    
    $newLines += $line
}

# Construct the new configuration
$header = @"
model = "$Model"
model_provider = "openrouter"
preferred_auth_method = "apikey"
"@

$providerBlock = @"
[model_providers.openrouter]
name = "OpenRouter"
base_url = "https://openrouter.ai/api/v1"
wire_api = "responses"
env_key = "OPENROUTER_API_KEY"
"@

# Combine them
$finalContent = $header + "`r`n`r`n" + $providerBlock + "`r`n`r`n" + ($newLines -join "`r`n")
# Clean up multiple empty lines
$finalContent = $finalContent -replace "(?:\r?\n){3,}", "`r`n`r`n"

Set-Content -Path $configPath -Value $finalContent -Encoding utf8

Write-Host "Config.toml updated successfully!" -ForegroundColor Green

# 4. Try to find and run codex doctor
$codexPath = $null
# Check on PATH first
$whereCodex = Get-Command codex -ErrorAction SilentlyContinue
if ($whereCodex) {
    $codexPath = $whereCodex.Source
} else {
    # Check in AppData\Local\OpenAI\Codex\bin
    $localBin = Join-Path $env:LOCALAPPDATA "OpenAI\Codex\bin"
    if (Test-Path $localBin) {
        $executables = Get-ChildItem -Path $localBin -Filter "codex.exe" -Recurse
        if ($executables) {
            $codexPath = $executables[0].FullName
        }
    }
}

if ($codexPath) {
    Write-Host "Running codex doctor to verify setup..." -ForegroundColor Cyan
    & $codexPath doctor
} else {
    Write-Host "Codex CLI executable not found on PATH or in local AppData. Please verify manually." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "IMPORTANT: Please restart your terminal, IDE (e.g., VS Code), or the Codex Desktop App so that they can load the new OPENROUTER_API_KEY environment variable." -ForegroundColor Yellow
