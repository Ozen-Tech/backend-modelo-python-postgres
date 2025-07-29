# app/tasks.py
from datetime import datetime, timedelta
from .worker import celery_app
from .db.connection import SessionLocal
from .services import deadline_service
from .schemas.deadline import DeadlineClassification, DeadlineStatus
from .services.notification_service import send_push_notification
from .models.notification.model import Notification
from .models.deadline.model import Deadline 

@celery_app.task
def classify_deadline(deadline_id: str):
    print(f"[CELERY TASK] Classificando prazo: {deadline_id}")
    db = SessionLocal()
    # ... (lógica existente para buscar prazo, calcular tempo, etc.)
    try:
        deadline = deadline_service.get_deadline_by_id(db, deadline_id=deadline_id)
        # ...
        if deadline.classification != new_classification:
            deadline.classification = new_classification
            db.commit()
            db.refresh(deadline)
            
            if deadline.responsible and (new_classification in [DeadlineClassification.CRITICO, DeadlineClassification.FATAL]):
                if deadline.responsible.fcm_token and deadline.responsible.notification_preferences.get('push', False):
                    title = f"Alerta de Prazo: {new_classification.value.upper()}"
                    body = f"O prazo para '{deadline.task_description[:50]}...' está se aproximando."
                    
                    # Salva a notificação no banco de dados ANTES de enviar
                    notification = Notification(user_id=deadline.responsible.id, title=title, body=body, related_deadline_id=deadline.id)
                    db.add(notification)
                    db.commit()
                    
                    # Envia a notificação push
                    data = {"deadlineId": str(deadline.id), "notificationId": str(notification.id)}
                    send_push_notification(deadline.responsible.fcm_token, title, body, data)
    finally:
        db.close()

@celery_app.task
def reclassify_all_deadlines_task():
    print("[CELERY BEAT] Iniciando tarefa diária: Reclassificar todos os prazos.")
    db = SessionLocal()
    try:
        active_deadlines = db.query(Deadline).filter(
            Deadline.status.notin_([DeadlineStatus.CONCLUIDO, DeadlineStatus.CANCELADO])
        ).all()
        
        print(f"[CELERY BEAT] Encontrados {len(active_deadlines)} prazos ativos para reclassificar.")
        for deadline in active_deadlines:
            classify_deadline.delay(str(deadline.id))
    finally:
        db.close()
