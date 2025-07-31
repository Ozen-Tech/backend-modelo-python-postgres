#!/bin/bash

# Faz o script parar imediatamente se qualquer comando falhar
set -e

# 1. Aplica as migrações do banco de dados antes de iniciar
echo "==> [START-PROD] Executando migrações do banco de dados..."
alembic upgrade head

# 2. Inicia o servidor Gunicorn para produção
echo "==> [START-PROD] Iniciando o servidor Gunicorn na porta 8000..."
gunicorn -c gunicorn_conf.py app.main:app