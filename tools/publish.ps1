# Builds dist/ from apps.json (tools/make_catalog.py) and uploads it as the assets of the GitHub release
# tagged `catalog`, creating that release the first time. Old assets that are no longer listed are deleted.
#   powershell -File tools\publish.ps1
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$gh = (Get-Command gh -ErrorAction SilentlyContinue).Source
if (-not $gh) { $gh = 'C:\Program Files\GitHub CLI\gh.exe' }
Set-Location $root

python -I tools/make_catalog.py
if ($LASTEXITCODE -ne 0) { throw 'make_catalog.py failed' }
$files = Get-ChildItem dist -File | ForEach-Object { $_.FullName }

# (a list, not `release view`: its "release not found" on stderr stops Windows PowerShell 5.1 here)
$tags = @(& $gh release list --limit 100 --json tagName --jq '.[].tagName')
if ($LASTEXITCODE -ne 0) { throw 'gh release list failed' }
if ($tags -notcontains 'catalog') {
    & $gh release create catalog --title 'Store catalog' --notes 'The MGU Store reads catalog.json from this release. Add the source 7amoody1985/mgu-apps:releases in the Store.' $files
    if ($LASTEXITCODE -ne 0) { throw 'gh release create failed' }
} else {
    & $gh release upload catalog $files --clobber
    if ($LASTEXITCODE -ne 0) { throw 'gh release upload failed' }
    $keep = Get-ChildItem dist -File | ForEach-Object { $_.Name }
    $have = & $gh release view catalog --json assets --jq '.assets[].name'
    foreach ($a in $have) { if ($keep -notcontains $a) { & $gh release delete-asset catalog $a --yes } }
}
Write-Host 'published: the Store sees it at its next check (Settings > Check now)'
