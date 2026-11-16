param([string]$Message = 'Publish Guia Canada classroom presentation')
$ErrorActionPreference = 'Stop'
$workspace = [System.IO.Path]::GetFullPath((Split-Path -Parent $PSScriptRoot))
$checkout = [System.IO.Path]::GetFullPath((Join-Path $workspace '.presentation-checkout'))
$dist = Join-Path $workspace 'dist'
if (-not $checkout.StartsWith($workspace + [System.IO.Path]::DirectorySeparatorChar)) { throw 'Unexpected checkout path' }
if (-not (Test-Path -LiteralPath (Join-Path $checkout '.git'))) { throw 'Publication checkout is missing' }
if (-not (Test-Path -LiteralPath (Join-Path $dist 'index.html'))) { throw 'Build the site before publishing' }
$remote = & git -C $checkout remote get-url origin
$branch = & git -C $checkout branch --show-current
if ($remote -ne 'https://github.com/RaphaelPhillipe07/canada-developer-immigration-dw.git' -or $branch -ne 'apresentacao') { throw 'Unexpected publication repository or branch' }
$docs = Join-Path $checkout 'docs'
$source = Join-Path $checkout 'apresentacao'
New-Item -ItemType Directory -Path $docs,$source -Force | Out-Null
$historical = Join-Path $docs 'entrega-1.html'
$oldIndex = Join-Path $docs 'index.html'
if (-not (Test-Path -LiteralPath $historical) -and (Test-Path -LiteralPath $oldIndex)) {
  $oldContent = Get-Content -Raw -Encoding utf8 -LiteralPath $oldIndex
  if (-not $oldContent.Contains('id="root"')) { Copy-Item -LiteralPath $oldIndex -Destination $historical }
}
Get-ChildItem -LiteralPath $dist -Force | ForEach-Object { Copy-Item -LiteralPath $_.FullName -Destination $docs -Recurse -Force }
foreach ($directory in @('src','public','scripts')) {
  $target = Join-Path $source $directory
  New-Item -ItemType Directory -Path $target -Force | Out-Null
  Get-ChildItem -LiteralPath (Join-Path $workspace $directory) -Force | ForEach-Object { Copy-Item -LiteralPath $_.FullName -Destination $target -Recurse -Force }
}
foreach ($file in @('package.json','package-lock.json','tsconfig.json','vite.config.mjs','vitest.config.mjs','index.html','components.json','.gitignore','README.md','DESIGN_SYSTEM.md','PRESENTER_GUIDE.md','MAP_ASSETS.md','THIRD_PARTY_NOTICES.txt','ATIVAR_PAGES.md')) {
  if (Test-Path -LiteralPath (Join-Path $workspace $file)) { Copy-Item -LiteralPath (Join-Path $workspace $file) -Destination (Join-Path $source $file) -Force }
}
[System.IO.File]::WriteAllText((Join-Path $docs '.nojekyll'),'',(New-Object System.Text.UTF8Encoding($false)))
$meta = @{ presentation='Guia Canada'; slides=14; published_at=[DateTime]::UtcNow.ToString('o'); source_path='apresentacao'; branch='apresentacao' } | ConvertTo-Json
[System.IO.File]::WriteAllText((Join-Path $docs 'build-info.json'),$meta,(New-Object System.Text.UTF8Encoding($false)))
& git -C $checkout -c core.autocrlf=false add -- docs apresentacao
if ($LASTEXITCODE -ne 0) { throw 'Could not stage site files' }
& git -C $checkout diff --cached --stat
& git -C $checkout commit -m $Message
if ($LASTEXITCODE -ne 0) { throw 'Could not commit site files' }
& git -C $checkout -c credential.helper= -c 'credential.helper=!gh auth git-credential' push origin apresentacao
if ($LASTEXITCODE -ne 0) { throw 'Could not push publication branch' }
& git -C $checkout rev-parse HEAD


