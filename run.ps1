# ButanolPathOptimizer — скрипт запуска для Windows
# Запуск: .\run.ps1

Write-Host ""
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "   ButanolPathOptimizer — автозапуск" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""

# Проверка Docker
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "ОШИБКА: Docker не установлен." -ForegroundColor Red
    Write-Host "Скачайте Docker Desktop: https://www.docker.com/products/docker-desktop/" -ForegroundColor Yellow
    exit 1
}

# Проверка что Docker запущен
docker info > $null 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ОШИБКА: Docker Desktop не запущен." -ForegroundColor Red
    Write-Host "Откройте Docker Desktop и дождитесь загрузки." -ForegroundColor Yellow
    exit 1
}

Write-Host "[1/3] Docker найден и запущен." -ForegroundColor Green

# Сборка образа
Write-Host "[2/3] Сборка образа (первый раз займет ~2 минуты)..." -ForegroundColor Yellow
docker build -t butanol-pipeline .
if ($LASTEXITCODE -ne 0) {
    Write-Host "ОШИБКА: сборка образа не удалась." -ForegroundColor Red
    exit 1
}
Write-Host "[2/3] Образ собран." -ForegroundColor Green

# Создание папки output
New-Item -ItemType Directory -Force -Path "output" > $null

# Запуск контейнера
Write-Host "[3/3] Запуск пайплайна..." -ForegroundColor Yellow
docker run --rm -v "${PWD}/output:/app/output" butanol-pipeline
if ($LASTEXITCODE -ne 0) {
    Write-Host "ОШИБКА: пайплайн завершился с ошибкой." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=================================================" -ForegroundColor Green
Write-Host "   Готово! Отчет сохранен в папке output/" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green
Write-Host ""

# Открыть папку output в проводнике
Start-Process explorer.exe -ArgumentList "output"
