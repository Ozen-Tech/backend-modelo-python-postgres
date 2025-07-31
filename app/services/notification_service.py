# app/services/notification_service.py
import uuid
import firebase_admin
from firebase_admin import credentials, messaging
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.notification.model import Notification

try:
    cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)
    print("✅ Firebase Admin SDK inicializado com sucesso.")
except Exception as e:
    print(f"❌ ATENÇÃO: Erro ao inicializar o Firebase Admin SDK: {e}")

def send_push_notification(device_token: str, title: str, body: str, data: dict = None):
    # ... (código existente)
    pass

def get_notifications_by_user(db: Session, *, user_id: uuid.UUID) -> list[Notification]:
    return db.query(Notification).filter(Notification.user_id == user_id).order_by(Notification.created_at.desc()).limit(50).all()

def mark_all_as_read(db: Session, *, user_id: uuid.UUID) -> int:
    num_updated = db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.is_read == False
    ).update({"is_read": True})
    db.commit()
    return num_updated