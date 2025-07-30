#!/bin/bash
set -e
echo "🙏 Aplicando migrações do Alembic..."
alembic upgrade head
echo "👤 Criando superusuário (se não existir)..."
python -m app.scripts.create_superuser
echo "🔥 Iniciando a API FastAPI para desenvolvimento..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload