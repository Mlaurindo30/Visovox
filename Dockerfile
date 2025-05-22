# Dockerfile (GPU-ready, multi-stage)
FROM nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04 AS base

ENV DEBIAN_FRONTEND=noninteractive

# Python e dependências básicas
RUN apt-get update && apt-get install -y \
    python3.10 python3.10-dev python3-pip git ffmpeg libsm6 libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Poetry
RUN pip3 install --upgrade pip
RUN pip3 install poetry

# Copia arquivos do projeto
WORKDIR /app
ENV PYTHONPATH=/app
COPY . /app

# Instala dependências com poetry
RUN poetry install --no-root --no-interaction --no-ansi

# Fix para PyTorch CUDA (opcional):
# RUN poetry run pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

EXPOSE 8000

# Entrypoint padrão (uvicorn API)
CMD ["poetry", "run", "uvicorn", "src.visiovox.apis.main:app", "--host", "0.0.0.0", "--port", "8000"] 