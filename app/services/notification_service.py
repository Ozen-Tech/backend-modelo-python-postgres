import firebase_admin
from firebase_admin import credentials, messaging
from app.core.config import settings

# Esta é uma etapa crucial. O SDK do Firebase deve ser inicializado apenas uma vez.
# Colocá-lo no nível do módulo garante que isso aconteça quando o worker iniciar.
try:
    # O settings.FIREBASE_CREDENTIALS_PATH já aponta para o caminho dentro do container
    cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)
    print("✅ Firebase Admin SDK inicializado com sucesso.")
except Exception as e:
    # Se o arquivo de credenciais não for encontrado, o serviço de notificação não funcionará.
    print(f"❌ ATENÇÃO: Erro ao inicializar o Firebase Admin SDK: {e}")
    print("❌ SERVIÇO DE NOTIFICAÇÃO ESTARÁ INOPERANTE.")

def send_push_notification(device_token: str, title: str, body: str, data: dict = None):
    """
    Envia uma notificação push para um único aparelho via FCM.
    """
    if not firebase_admin._apps:
        print("[FIREBASE] SDK não inicializado. Abortando envio de notificação.")
        return False
        
    message = messaging.Message(
        notification=messaging.Notification(title=title, body=body),
        data=data or {},
        token=device_token,
    )
    
    try:
        response = messaging.send(message)
        print(f"[FIREBASE] Notificação enviada com sucesso para o token: {device_token}, Message ID: {response}")
        return True
    except Exception as e:
        # Erros comuns aqui são "token inválido" ou "serviço indisponível".
        print(f"[FIREBASE] Erro ao enviar notificação para o token {device_token}: {e}")
        return False