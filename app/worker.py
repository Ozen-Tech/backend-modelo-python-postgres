# app/worker.py
from celery import Celery
from app.core.config import settings
from celery.schedules import crontab
from .db import base


# Cria a instância do Celery
# O primeiro argumento 'tasks' é o nome tradicional para a instância.
# A variável 'broker' diz ao Celery para usar o Redis que configuramos no .env.
# 'include' diz ao Celery para procurar por tarefas no arquivo 'app/tasks.py'.
celery_app = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND, # Opcional, para armazenar resultados
    include=["app.tasks"]
)

# --- AGENDAMENTO DE TAREFAS (CELERY BEAT) ---
celery_app.conf.beat_schedule = {
    # Executa a tarefa todos os dias às 3 da manhã
    'reclassify-deadlines-daily': {
        'task': 'app.tasks.reclassify_all_deadlines_task',
        'schedule': crontab(hour=3, minute=0),
    },
}