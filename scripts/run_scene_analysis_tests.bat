@echo off
REM Executa todos os testes do módulo scene_analysis
poetry run pytest tests/apis/test_scene_analysis.py --cov=src --disable-warnings --maxfail=2
pause 