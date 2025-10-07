from observador import IObservador

class Usuario(IObservador):
    """Clase que representa al usuario suscrito al sistema"""

    def __init__(self, nombre: str, email: str, telefono: str):
        self.nombre = nombre
        self.email = email
        self.telefono = telefono

    def actualizar(self, mensaje: str):
        print(f"🔔 {self.nombre} ha recibido una notificación: {mensaje}")
