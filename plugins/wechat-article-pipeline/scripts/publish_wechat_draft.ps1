param(
  [string]$ProjectRoot = (Resolve-Path "."),

  [Parameter(Mandatory = $true)]
  [string]$Article,

  [string]$Cover,
  [string]$Title,
  [string]$Summary,
  [string]$SourceUrl,
  [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$Root = Resolve-Path -LiteralPath $ProjectRoot

Push-Location $Root
try {
  $wrapper = Join-Path $Root "tools\github-to-wechat\publish-markdown-to-wechat.ps1"
  if (Test-Path -LiteralPath $wrapper) {
    $args = @("-ExecutionPolicy", "Bypass", "-File", $wrapper, "-Article", $Article)
    if ($Cover) { $args += @("-Cover", $Cover) }
    if ($Title) { $args += @("-Title", $Title) }
    if ($Summary) { $args += @("-Summary", $Summary) }
    if ($SourceUrl) { $args += @("-SourceUrl", $SourceUrl) }
    if ($DryRun) { $args += "-DryRun" }
    & powershell @args
    exit $LASTEXITCODE
  }

  $apiScript = Join-Path $Root ".codex\skills\baoyu-post-to-wechat\scripts\wechat-api.ts"
  if (-not (Test-Path -LiteralPath $apiScript)) {
    throw "No project publish wrapper and no baoyu wechat-api.ts found."
  }

  $articlePath = Resolve-Path -LiteralPath $Article
  $cmdArgs = @($apiScript, $articlePath.Path, "--theme", "default", "--color", "blue")
  if ($Cover) {
    $coverPath = Resolve-Path -LiteralPath $Cover
    $cmdArgs += @("--cover", $coverPath.Path)
  }
  if ($Title) { $cmdArgs += @("--title", $Title) }
  if ($Summary) { $cmdArgs += @("--summary", $Summary) }
  if ($SourceUrl) { $cmdArgs += @("--source-url", $SourceUrl) }

  if ($DryRun) {
    Write-Output (("bun " + ($cmdArgs -join " ")))
    return
  }

  & bun @cmdArgs
  exit $LASTEXITCODE
} finally {
  Pop-Location
}
