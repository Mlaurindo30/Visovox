#!/bin/bash
set -e
poetry install
if [ -f .env.example ]; then
  cp .env.example .env
fi
echo "Ambiente instalado. Use: poetry run uvicorn src.visiovox.apis.main:app --reload" 