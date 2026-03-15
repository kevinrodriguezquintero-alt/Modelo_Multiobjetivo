# Inicia la API (puerto 8000) y el frontend (puerto 3000)

$ROOT = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "Iniciando API en http://localhost:8000 ..."
$api = Start-Process -FilePath "$ROOT\02-api-model\venv\Scripts\uvicorn.exe" `
    -ArgumentList "api.main:app", "--reload", "--port", "8000" `
    -WorkingDirectory "$ROOT\02-api-model" `
    -PassThru -NoNewWindow

Write-Host "Iniciando frontend en http://localhost:3000 ..."
$web = Start-Process -FilePath "python" `
    -ArgumentList "-m", "http.server", "3000" `
    -WorkingDirectory "$ROOT\03-web-model" `
    -PassThru -NoNewWindow

Write-Host ""
Write-Host "API PID:      $($api.Id)"
Write-Host "Frontend PID: $($web.Id)"
Write-Host ""
Write-Host "Presiona Ctrl+C para detener ambos servidores."

try {
    Wait-Process -Id $api.Id, $web.Id
} finally {
    Stop-Process -Id $api.Id, $web.Id -Force -ErrorAction SilentlyContinue
    Write-Host "Servidores detenidos."
}
