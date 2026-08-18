$ErrorActionPreference = "Stop"

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "Docker Desktop が必要です。先にインストールして起動してください。"
    exit 1
}

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host ".env を作成しました。AI APIを使う段階で UPSTREAM_API_KEY を設定します。"
}

docker compose up -d --build
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Start-Process "http://localhost:3000"
Write-Host "Raphael を開きました: http://localhost:3000"
