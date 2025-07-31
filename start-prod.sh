#!/bin/bash
set -e

# No Render, as migrações são melhores como um Build Command
# Mas se não for possível, esta é a segunda melhor opção.
echo "==> Aplicando migrações (produção)..."
alembic upgrade head

echo "==> Iniciando Gunicorn..."
gunicorn -c /code/gunicorn_conf.py app.main:app