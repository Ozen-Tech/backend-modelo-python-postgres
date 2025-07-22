#!/bin/bash
# start.sh

echo "🚀 Esperando o banco de dados iniciar..."
sleep 5

echo "🙏 Aplicando migrações do Alembic..."
alembic upgrade head

echo "👤 Criando superusuário (se não existir)..."
python -m app.scripts.create_superuser

echo "🔥 Iniciando a API FastAPI..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload