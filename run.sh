#!/bin/bash
# ButanolPathOptimizer — скрипт запуска для Linux/macOS
# Запуск: bash run.sh

echo ""
echo "================================================="
echo "   ButanolPathOptimizer — автозапуск"
echo "================================================="
echo ""

# Проверка Docker
if ! command -v docker &> /dev/null; then
    echo "ОШИБКА: Docker не установлен."
    echo "Скачайте Docker Desktop: https://www.docker.com/products/docker-desktop/"
    exit 1
fi

# Проверка что Docker запущен
if ! docker info > /dev/null 2>&1; then
    echo "ОШИБКА: Docker не запущен."
    echo "Запустите Docker Desktop и дождитесь загрузки."
    exit 1
fi

echo "[1/3] Docker найден и запущен."

# Сборка образа
echo "[2/3] Сборка образа (первый раз займет ~2 минуты)..."
docker build -t butanol-pipeline .
if [ $? -ne 0 ]; then
    echo "ОШИБКА: сборка образа не удалась."
    exit 1
fi
echo "[2/3] Образ собран."

# Создание папки output
mkdir -p output

# Запуск контейнера
echo "[3/3] Запуск пайплайна..."
docker run --rm -v "${PWD}/output:/app/output" butanol-pipeline
if [ $? -ne 0 ]; then
    echo "ОШИБКА: пайплайн завершился с ошибкой."
    exit 1
fi

echo ""
echo "================================================="
echo "   Готово! Отчет сохранен в папке output/"
echo "================================================="
echo ""

# Открыть папку output
if [[ "$OSTYPE" == "darwin"* ]]; then
    open output/
else
    xdg-open output/ 2>/dev/null || echo "Откройте папку output/ вручную."
fi
