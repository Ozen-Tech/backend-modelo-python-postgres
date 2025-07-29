# gunicorn_conf.py
import multiprocessing

# Endereço e porta em que o Gunicorn vai escutar
# 0.0.0.0 significa que ele aceitará conexões de qualquer IP (essencial para Docker)
bind = "0.0.0.0:8000"

# O número de workers a serem iniciados.
# A fórmula (2 * número de cores da CPU) + 1 é um bom ponto de partida.
workers = (multiprocessing.cpu_count() * 2) + 1

# A classe do worker que o Gunicorn deve usar.
# UvicornWorker permite que o Gunicorn rode aplicações ASGI como o FastAPI.
worker_class = "uvicorn.workers.UvicornWorker"