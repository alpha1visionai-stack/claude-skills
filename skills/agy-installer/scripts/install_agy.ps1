param (
    [string]$ApiKey
)

$InstallPath = "$env:LOCALAPPDATA\agy\bin"
$ExePath = "$InstallPath\agy.exe"
$SourceExe = "C:\Users\walte\AppData\Local\agy\bin\agy.exe" # This assumes the source machine has agy installed here

# 1. Create directory structure
if (-not (Test-Path $InstallPath)) {
    Write-Host "Creating directory: $InstallPath"
    New-Item -ItemType Directory -Path $InstallPath -Force | Out-Null
}

# 2. Copy the executable (this assumes we have it bundled in the skill assets)
$BundledExe = "$PSScriptRoot\..\assets\agy.exe"
if (Test-Path $BundledExe) {
    Write-Host "Installing agy.exe from bundled assets..."
    Copy-Item -Path $BundledExe -Destination $ExePath -Force
} elseif (Test-Path $SourceExe) {
    Write-Host "Installing agy.exe from local source..."
    Copy-Item -Path $SourceExe -Destination $ExePath -Force
} else {
    Write-Error "agy.exe not found! Please ensure it is in assets or the source path is correct."
    exit 1
}

# 3. Add to User PATH
$UserPath = [System.Environment]::GetEnvironmentVariable("Path", "User")
if ($UserPath -notlike "*$InstallPath*") {
    Write-Host "Adding $InstallPath to User PATH..."
    $NewPath = "$UserPath;$InstallPath"
    [System.Environment]::SetEnvironmentVariable("Path", $NewPath, "User")
} else {
    Write-Host "Path already exists."
}

# 4. Set API Key if provided
if ($ApiKey) {
    Write-Host "Setting GOOGLE_API_KEY..."
    [System.Environment]::SetEnvironmentVariable("GOOGLE_API_KEY", $ApiKey, "User")
    # Also set for current session
    $env:GOOGLE_API_KEY = $ApiKey
}

Write-Host "Installation complete! Please restart your terminal."
