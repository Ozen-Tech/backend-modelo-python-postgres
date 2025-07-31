

#!/bin/bash

# 1. Parar o script se qualquer comando falhar
set -e

# 2. Aplicar as migrações do banco de dados
# O comando `alembic upgrade head` irá conectar ao seu banco de produção
# (usando a DATABASE_URL do ambiente) e aplicar quaisquer migrações pendentes.
echo "==> Executando migrações do banco de dados..."
alembic upgrade head

# 3. Iniciar o servidor de aplicação Gunicorn
# Este comando iniciará a API para receber requisições da web.
echo "==> Iniciando o servidor Gunicorn..."
gunicorn -c gunicorn_conf.py app.main:app