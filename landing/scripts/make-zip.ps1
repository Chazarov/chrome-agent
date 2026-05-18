$ErrorActionPreference = "Stop"
$root = Split-Path $PSScriptRoot -Parent
Set-Location -LiteralPath $root

$public = Join-Path $root "public"
if (-not (Test-Path -LiteralPath $public)) {
  New-Item -ItemType Directory -Path $public | Out-Null
}

$zip = Join-Path $public "GigaBrowserAgent.zip"
if (Test-Path -LiteralPath $zip) {
  Remove-Item -LiteralPath $zip -Force
}

$temp = Join-Path $env:TEMP ("gigabrowser_zip_" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $temp | Out-Null

$excludeTop = @("node_modules", "dist", ".git")
Get-ChildItem -LiteralPath $root -Force | Where-Object { $excludeTop -notcontains $_.Name } | ForEach-Object {
  $dest = Join-Path $temp $_.Name
  Copy-Item -LiteralPath $_.FullName -Destination $dest -Recurse -Force
}

$zipInside = Join-Path $temp "public/GigaBrowserAgent.zip"
if (Test-Path -LiteralPath $zipInside) {
  Remove-Item -LiteralPath $zipInside -Force
}

Compress-Archive -Path (Join-Path $temp "*") -DestinationPath $zip -Force
Remove-Item -LiteralPath $temp -Recurse -Force

Write-Host "Created $zip"
