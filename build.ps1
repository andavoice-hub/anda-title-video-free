param([Parameter(Mandatory=$true)][string]$FFmpegBin)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$ffmpeg = Join-Path $FFmpegBin 'ffmpeg.exe'
if (-not (Test-Path -LiteralPath $ffmpeg)) { throw '指定資料夾缺少 ffmpeg.exe' }
$version = (& $ffmpeg -version) -join "`n"
if ($version -match '--enable-gpl' -or $version -notmatch '--enable-shared') { throw '只接受 LGPL shared FFmpeg 建置' }
$nsis = 'C:\Program Files (x86)\NSIS\makensis.exe'
if (-not (Test-Path -LiteralPath $nsis)) { throw '找不到 NSIS makensis.exe' }
$stage = Join-Path $root 'stage'
$release = Join-Path $root 'release'
if (Test-Path -LiteralPath $stage) {
    $resolved = (Resolve-Path -LiteralPath $stage).Path
    if ($resolved -ne (Join-Path $root 'stage')) { throw 'stage 路徑檢查失敗' }
    Remove-Item -LiteralPath $resolved -Recurse -Force
}
New-Item -ItemType Directory -Force -Path $stage,$release | Out-Null
Push-Location $root
try {
    pyinstaller --noconfirm --clean --windowed --onedir --name 'AndaTitleVideoFree' --distpath "$root\dist" --workpath "$root\build" title_video.py
    if ($LASTEXITCODE -ne 0) { throw 'PyInstaller 建置失敗' }
    Copy-Item -Path "$root\dist\AndaTitleVideoFree\*" -Destination $stage -Recurse -Force
    $ffstage = Join-Path $stage 'ffmpeg'
    New-Item -ItemType Directory -Force -Path $ffstage | Out-Null
    Copy-Item -Path (Join-Path $FFmpegBin '*') -Destination $ffstage -Force
    $fflicense = Join-Path (Split-Path -Parent $FFmpegBin) 'LICENSE.txt'
    if (-not (Test-Path -LiteralPath $fflicense)) { throw 'FFmpeg 下載包缺少 LICENSE.txt' }
    Copy-Item -LiteralPath $fflicense -Destination $ffstage -Force
    Copy-Item -LiteralPath "$root\LICENSE","$root\THIRD_PARTY.md","$root\COMMERCIAL.md" -Destination $stage -Force
    & $nsis "$root\installer.nsi"
    if ($LASTEXITCODE -ne 0) { throw 'NSIS 建置失敗' }
} finally { Pop-Location }
