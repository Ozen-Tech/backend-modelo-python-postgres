# gunicorn_conf.py (Versão Segura para Produção)
import os
import multiprocessing

# Endereço e porta em que o Gunicorn vai escutar
bind = "0.0.0.0:8000"

# --- A CORREÇÃO ESTÁ AQUI ---
# Pega o número de workers da variável de ambiente GUNICORN_WORKERS.
# Se a variável não estiver definida, usa um padrão seguro de '3'.
# Isso nos dá controle total sobre o consumo de memória no Render.
workers = int(os.environ.get('GUNICORN_WORKERS', '3'))
# -----------------------------

# A classe do worker que o Gunicorn deve usar
worker_class = "uvicorn.workers.UvicornWorker"