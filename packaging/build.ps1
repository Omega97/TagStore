# Build dist\TagStore\ and dist\TagStore-Setup-<version>.exe
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

$python = Join-Path $Root ".venv\Scripts\python.exe"
$pyinstaller = Join-Path $Root ".venv\Scripts\pyinstaller.exe"

if (-not (Test-Path $python)) {
    python -m venv (Join-Path $Root ".venv")
}

& $python -m pip install --upgrade pip
& $python -m pip install -r (Join-Path $Root "requirements-dev.txt")

if (Test-Path (Join-Path $Root "dist\TagStore")) {
    Remove-Item -Recurse -Force (Join-Path $Root "dist\TagStore")
}
if (Test-Path (Join-Path $Root "build")) {
    Remove-Item -Recurse -Force (Join-Path $Root "build")
}

& $pyinstaller --noconfirm --distpath (Join-Path $Root "dist") --workpath (Join-Path $Root "build") (Join-Path $Root "packaging\tagstore.spec")
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

$isccCandidates = @(
    "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe",
    "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe",
    "$env:ProgramFiles\Inno Setup 6\ISCC.exe"
)
$iscc = $isccCandidates | Where-Object { $_ -and (Test-Path $_) } | Select-Object -First 1
if (-not $iscc) {
    $cmd = Get-Command ISCC.exe -ErrorAction SilentlyContinue
    if ($cmd) { $iscc = $cmd.Source }
}
if (-not $iscc) {
    Write-Error "Inno Setup 6 (ISCC.exe) was not found. The folder dist\TagStore is ready. Install Inno Setup 6 and rerun packaging\build.ps1." -ErrorAction Continue
    exit 1
}

& $iscc (Join-Path $Root "packaging\installer.iss")
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
