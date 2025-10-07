from abc import ABC, abstractmethod

class INotificacion(ABC):
    @abstractmethod
    def enviar(self, mensaje: str, destino: str):
        pass


class EmailNotificacion(INotificacion):
    def enviar(self, mensaje: str, destino: str):
        print(f"📧 Enviando email a {destino}: {mensaje}")


class SMSNotificacion(INotificacion):
    def enviar(self, mensaje: str, destino: str):
        print(f"📱 Enviando SMS a {destino}: {mensaje}")


class PushNotificacion(INotificacion):
    def enviar(self, mensaje: str, destino: str):
        print(f"🚀 Enviando notificación push a {destino}: {mensaje}")
