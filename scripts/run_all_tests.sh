#!/bin/bash
set -e

# Função para detectar ambiente Windows (Git Bash/WSL)
IS_WINDOWS=false
case "$(uname -s)" in
    MINGW*|MSYS*|CYGWIN*) IS_WINDOWS=true;;
    *) IS_WINDOWS=false;;
esac

# Helper para abrir HTML de cobertura no Windows
open_html() {
    if $IS_WINDOWS; then
        explorer.exe $(wslpath -w "$1")
    else
        xdg-open "$1" || open "$1" || echo "Abra manualmente: $1"
    fi
}

echo "🟢 Subindo ambiente Docker Compose..."
docker-compose up -d --build

echo "⏳ Aguardando containers subirem..."
sleep 10

echo "🔍 Validando containers..."
docker ps

echo "🧪 Rodando TODOS os testes automatizados (unitários, integração, domínios)..."
docker exec visiovox_api_gpu poetry run pytest --cov=src --cov-report=term --cov-report=html:coverage_html

echo "🧪 Rodando testes Celery (stub, unitários)..."
docker exec visiovox_celery_gpu poetry run pytest tests/apis/test_celery_task.py

echo "🧪 Rodando testes de integração (TestClient, mocks, outros domínios)..."
docker exec visiovox_api_gpu poetry run pytest tests/apis/test_router.py
# Adicione aqui outros arquivos de teste de domínios, ex:
# docker exec visiovox_api_gpu poetry run pytest tests/apis/test_scene_analysis_router.py
# docker exec visiovox_api_gpu poetry run pytest tests/apis/test_facial_processing_router.py

echo "🧪 Rodando testes de schemas e pipeline stub..."
docker exec visiovox_api_gpu poetry run pytest tests/apis/test_schemas.py
docker exec visiovox_api_gpu poetry run pytest tests/apis/test_pipeline_stub.py

echo "🧪 Rodando testes de performance (pytest-benchmark, se disponível)..."
docker exec visiovox_api_gpu poetry run pytest --benchmark-only || echo "pytest-benchmark não instalado ou sem benchmarks."

echo "🟢 Validando GPU no Celery..."
docker exec visiovox_celery_gpu nvidia-smi

echo "🟢 Validando PyTorch CUDA no Celery..."
docker exec visiovox_celery_gpu poetry run python -c "import torch; print('CUDA disponível:', torch.cuda.is_available())"

echo "📊 Gerando relatório de cobertura HTML..."
echo "Abra o arquivo coverage_html/index.html no seu navegador para visualizar o relatório."

# Tenta abrir automaticamente no Windows
if $IS_WINDOWS; then
    open_html "coverage_html/index.html"
fi

echo '✅ Todos os testes, validações e benchmarks executados!' 