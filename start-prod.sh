#!/bin/bash
set -e
echo "🙏 Aplicando migrações do Alembic..."
alembic upgrade head
echo "👤 Criando superusuário (se não existir)..."
echo "🔥 Iniciando a API em modo de produção com Gunicorn..."
gunicorn -c /code/gunicorn_conf.py app.main:app