from usuario import Usuario
from observador import NotificacionSubject
from fabrica import NotificacionFactory

if __name__ == "__main__":
    # Crear el sujeto principal (gestor de notificaciones)
    sistema_notificaciones = NotificacionSubject()

    # Crear usuarios
    usuario1 = Usuario("Martín", "martin@email.com", "555-1234")
    usuario2 = Usuario("Laura", "laura@email.com", "555-5678")

    # Suscribir usuarios al sistema
    sistema_notificaciones.agregar_observador(usuario1)
    sistema_notificaciones.agregar_observador(usuario2)

    # Crear una notificación usando el Factory Method
    fabrica = NotificacionFactory()
    notificador = fabrica.crear_notificacion("email")

    # Enviar mensaje
    mensaje = "Nueva actualización disponible 🎉"
    sistema_notificaciones.notificar_observadores(mensaje)

    # Enviar mensaje real por medio del canal (Factory Method)
    notificador.enviar(mensaje, usuario1.email)
    notificador.enviar(mensaje, usuario2.email)
