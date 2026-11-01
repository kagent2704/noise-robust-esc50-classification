$ErrorActionPreference = "Stop"

$projectRoot = $PSScriptRoot
$dataDirectory = Join-Path $projectRoot "data"
$datasetDirectory = Join-Path $dataDirectory "ESC-50"
$zipPath = Join-Path $dataDirectory "ESC-50-master.zip"
$downloadUrl = "https://github.com/karolpiczak/ESC-50/archive/refs/heads/master.zip"

if (Test-Path -LiteralPath (Join-Path $datasetDirectory "meta\esc50.csv")) {
    Write-Host "ESC-50 is already available at $datasetDirectory"
    exit 0
}

New-Item -ItemType Directory -Force -Path $dataDirectory | Out-Null
Write-Host "Downloading ESC-50 (approximately 600 MB)..."
Invoke-WebRequest -Uri $downloadUrl -OutFile $zipPath

Write-Host "Extracting dataset..."
Expand-Archive -LiteralPath $zipPath -DestinationPath $dataDirectory -Force

$extractedDirectory = Join-Path $dataDirectory "ESC-50-master"
if (-not (Test-Path -LiteralPath $extractedDirectory)) {
    throw "The downloaded archive did not contain the expected ESC-50-master folder."
}

Move-Item -LiteralPath $extractedDirectory -Destination $datasetDirectory
Remove-Item -LiteralPath $zipPath
Write-Host "ESC-50 is ready at $datasetDirectory"

