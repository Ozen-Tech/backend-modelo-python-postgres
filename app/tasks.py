# app/tasks.py
from datetime import datetime, timedelta, timezone
from app.worker import celery_app
from app.db.connection import SessionLocal
from app.services import deadline_service
from app.schemas.deadline import DeadlineClassification, DeadlineStatus
from app.services.notification_service import send_push_notification
from app.models.notification.model import Notification
from app.models.deadline.model import Deadline 

@celery_app.task
def classify_deadline(deadline_id: str):
    """
    Busca um prazo no banco, calcula sua classificação e envia notificação se necessário.
    """
    print(f"[CELERY TASK] Iniciando classificação para o prazo: {deadline_id}")
    db = SessionLocal()
    try:
        deadline = deadline_service.get_deadline_by_id(db, deadline_id=deadline_id)
        if not deadline or deadline.status in [DeadlineStatus.CONCLUIDO, DeadlineStatus.CANCELADO]:
            print(f"[CELERY TASK] Prazo {deadline_id} não encontrado ou inativo. Abortando.")
            return

        now = datetime.now(timezone.utc)
        time_left = deadline.due_date - now

        new_classification = DeadlineClassification.NORMAL
        if time_left <= timedelta(days=2):
            new_classification = DeadlineClassification.FATAL
        elif time_left <= timedelta(days=7):
            new_classification = DeadlineClassification.CRITICO
        
        # Se a classificação mudou, atualiza e notifica
        if deadline.classification != new_classification:
            print(f"[CELERY TASK] Classificação do prazo {deadline_id} mudou para {new_classification.value}.")
            deadline.classification = new_classification
            db.commit()
            db.refresh(deadline)
            
            # Lógica para enviar notificação
            responsible_user = deadline.responsible
            if responsible_user and (new_classification in [DeadlineClassification.CRITICO, DeadlineClassification.FATAL]):
                # Verifica se o usuário tem token e se ativou notificações push
                if responsible_user.fcm_token and responsible_user.notification_preferences.get('push', True):
                    title = f"Alerta de Prazo: {new_classification.value.upper()}"
                    body = f"O prazo para '{deadline.task_description[:50]}...' está se aproximando."
                    
                    # Salva a notificação no nosso banco
                    notification = Notification(user_id=responsible_user.id, title=title, body=body, related_deadline_id=deadline.id)
                    db.add(notification)
                    db.commit()
                    
                    # Envia para o Firebase
                    data = {"deadlineId": str(deadline.id), "notificationId": str(notification.id)}
                    send_push_notification(responsible_user.fcm_token, title, body, data)
    finally:
        db.close()

@celery_app.task
def reclassify_all_deadlines_task():
    """
    Tarefa agendada para buscar todos os prazos ativos e enfileirar uma
    tarefa de reclassificação para cada um.
    """
    print(f"[CELERY BEAT] {datetime.now()}: Iniciando tarefa diária: Reclassificar todos os prazos.")
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