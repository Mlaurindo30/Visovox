@echo off
REM =============================================
REM Script de testes para ambiente Docker VisioVox Fusion
REM - NÃO faz rebuild das imagens nem reinicia containers se já estiverem rodando
REM - Apenas executa os testes nos containers em execução
REM =============================================

REM Suba os containers manualmente se ainda não estiverem rodando:
REM docker-compose up -d

docker ps

docker exec visiovox_api_gpu poetry run pytest --cov=src --cov-report=term --cov-report=html:coverage_html

docker exec visiovox_celery_gpu poetry run pytest tests/apis/test_celery_task.py

docker exec visiovox_api_gpu poetry run pytest tests/apis/test_router.py

docker exec visiovox_api_gpu poetry run pytest tests/apis/test_schemas.py

docker exec visiovox_api_gpu poetry run pytest tests/apis/test_pipeline_stub.py

docker exec visiovox_api_gpu poetry run pytest --benchmark-only

docker exec visiovox_celery_gpu nvidia-smi

docker exec visiovox_celery_gpu poetry run python -c "import torch; print('CUDA disponível:', torch.cuda.is_available())"

echo Relatório de cobertura gerado em coverage_html/index.html (dentro do container)
docker cp visiovox_api_gpu:/app/coverage_html ./coverage_html
start coverage_html\index.html
echo TODOS OS TESTES EXECUTADOS!
pause

docker logs visiovox_api_gpu
docker logs visiovox_celery_gpu