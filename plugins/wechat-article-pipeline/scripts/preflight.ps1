param(
  [string]$ProjectRoot = (Resolve-Path "."),
  [switch]$TestSsh
)

$ErrorActionPreference = "Stop"
$HadWarning = $false
$Root = Resolve-Path -LiteralPath $ProjectRoot

function Write-Check {
  param([bool]$Ok, [string]$Name, [string]$Detail = "")
  $status = if ($Ok) { "[OK]" } else { "[WARN]" }
  if (-not $Ok) { $script:HadWarning = $true }
  if ($Detail) { Write-Output "$status $Name - $Detail" } else { Write-Output "$status $Name" }
}

function Test-Command {
  param([string]$Name)
  $cmd = Get-Command $Name -ErrorAction SilentlyContinue
  Write-Check ([bool]$cmd) $Name ($(if ($cmd) { $cmd.Source } else { "not found in PATH" }))
}

Push-Location $Root
try {
  Write-Output "Project: $Root"

  foreach ($cmd in @("bun", "node", "python", "ssh")) {
    Test-Command $cmd
  }

  $publishWrapper = Join-Path $Root "tools\github-to-wechat\publish-markdown-to-wechat.ps1"
  Write-Check (Test-Path -LiteralPath $publishWrapper) "project publish wrapper" $publishWrapper

  $apiScript = Join-Path $Root ".codex\skills\baoyu-post-to-wechat\scripts\wechat-api.ts"
  Write-Check (Test-Path -LiteralPath $apiScript) "baoyu wechat-api.ts" $apiScript

  $envFile = Join-Path $Root ".baoyu-skills\.env"
  if (Test-Path -LiteralPath $envFile) {
    $envText = Get-Content -LiteralPath $envFile -Raw
    Write-Check ($envText -match "(?m)^WECHAT_APP_ID=.+") "wechat app id" ".baoyu-skills/.env"
    Write-Check ($envText -match "(?m)^WECHAT_APP_SECRET=.+") "wechat app secret" ".baoyu-skills/.env"
  } else {
    Write-Check $false "wechat credentials" ".baoyu-skills/.env missing"
  }

  $extendPath = Join-Path $Root ".baoyu-skills\baoyu-post-to-wechat\EXTEND.md"
  if (Test-Path -LiteralPath $extendPath) {
    $extendText = Get-Content -LiteralPath $extendPath -Raw
    $method = [regex]::Match($extendText, "(?m)^default_publish_method:\s*(.+?)\s*$")
    Write-Check $method.Success "wechat publish method" ($(if ($method.Success) { $method.Groups[1].Value.Trim() } else { "missing" }))

    $keyMatch = [regex]::Match($extendText, "(?m)^remote_publish_identity_file:\s*(.+?)\s*$")
    if ($keyMatch.Success) {
      $keyPath = $keyMatch.Groups[1].Value.Trim() -replace "^~", $env:USERPROFILE
      Write-Check (Test-Path -LiteralPath $keyPath) "remote ssh key" $keyPath

      if ($TestSsh -and (Test-Path -LiteralPath $keyPath)) {
        $hostMatch = [regex]::Match($extendText, "(?m)^remote_publish_host:\s*(.+?)\s*$")
        $userMatch = [regex]::Match($extendText, "(?m)^remote_publish_user:\s*(.+?)\s*$")
        $hostName = if ($hostMatch.Success) { $hostMatch.Groups[1].Value.Trim() } else { "" }
        $userName = if ($userMatch.Success) { $userMatch.Groups[1].Value.Trim() } else { "root" }
        $sshOut = & ssh -i $keyPath -o StrictHostKeyChecking=accept-new "$userName@$hostName" "echo OK" 2>&1
        Write-Check ($LASTEXITCODE -eq 0) "remote ssh login" ($(if ($LASTEXITCODE -eq 0) { "OK" } else { ($sshOut -join " ") }))
      }
    }
  } else {
    Write-Check $false "wechat extend" $extendPath
  }

  if ($HadWarning) { exit 1 }
} finally {
  Pop-Location
}
