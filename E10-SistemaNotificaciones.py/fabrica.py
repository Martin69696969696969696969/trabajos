from notificaciones import EmailNotificacion, SMSNotificacion, PushNotificacion

class NotificacionFactory:
    """Fábrica que crea objetos de notificación según el tipo."""

    @staticmethod
    def crear_notificacion(tipo: str):
        if tipo.lower() == "email":
            return EmailNotificacion()
        elif tipo.lower() == "sms":
            return SMSNotificacion()
        elif tipo.lower() == "push":
            return PushNotificacion()
        else:
            raise ValueError("Tipo de notificación no soportado.")
