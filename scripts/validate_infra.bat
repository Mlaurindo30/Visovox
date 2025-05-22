@echo off
REM =============================================
REM Validação completa da Infraestrutura VisioVox Fusion (Windows)
REM =============================================

REM 1. Subir ambiente Docker Compose
echo Subindo containers Docker Compose...
docker-compose up -d

REM 2. Esperar containers subirem
timeout /t 10

REM 3. Rodar todos os testes automatizados
echo Executando testes automatizados...
docker exec visiovox_api_gpu poetry run pytest --cov=src --cov-report=term --cov-report=html:coverage_html
docker exec visiovox_celery_gpu poetry run pytest tests/apis/test_celery_task.py
docker exec visiovox_api_gpu poetry run pytest tests/apis/test_router.py
docker exec visiovox_api_gpu poetry run pytest tests/apis/test_schemas.py
docker exec visiovox_api_gpu poetry run pytest tests/apis/test_pipeline_stub.py

REM 4. Copiar e abrir relatório de cobertura
docker cp visiovox_api_gpu:/app/coverage_html ./coverage_html
start coverage_html\index.html

REM 5. Checar /docs e /healthz
echo Abra http://localhost:8000/docs no navegador para validar a documentação.
curl http://localhost:8000/healthz

REM 6. Rodar frontend exemplo
echo Rode o frontend_example manualmente: cd frontend_example && npm start

REM 7. Validar logs
docker logs visiovox_api_gpu > logs_api.txt
docker logs visiovox_celery_gpu > logs_celery.txt

echo =============================
echo Checklist de validação concluído!
echo - Verifique /docs, /healthz, frontend e logs.
echo - Consulte o coverage_html para cobertura de código.
echo - Veja logs_api.txt e logs_celery.txt para detalhes.
echo - Atualize README.md se necessário.
echo - Sinalize OK se tudo estiver funcionando!
pause 