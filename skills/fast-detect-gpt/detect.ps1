<#
.SYNOPSIS
    Fast-DetectGPT Starter-Skript für Windows PowerShell
.EXAMPLE
    .\detect.ps1 -Text "Hier steht der Text..."
.EXAMPLE
    .\detect.ps1 -File "aufsatz.txt"
.EXAMPLE
    .\detect.ps1
#>

param(
    [string]$Text = "",
    [string]$File = "",
    [string]$SamplingModel = "gpt-neo-2.7B",
    [string]$ScoringModel = "gpt-neo-2.7B"
)

$RepoDir = $PSScriptRoot

if ($Text -ne "") {
    uv run --directory $RepoDir python detect_text.py --text $Text --sampling_model_name $SamplingModel --scoring_model_name $ScoringModel
}
elseif ($File -ne "") {
    uv run --directory $RepoDir python detect_text.py --file $File --sampling_model_name $SamplingModel --scoring_model_name $ScoringModel
}
else {
    uv run --directory $RepoDir python detect_text.py --sampling_model_name $SamplingModel --scoring_model_name $ScoringModel
}
