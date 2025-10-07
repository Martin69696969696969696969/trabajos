from abc import ABC, abstractmethod

class IObservador(ABC):
    @abstractmethod
    def actualizar(self, mensaje: str):
        pass


class NotificacionSubject:
    """Clase Sujeto (Subject) del patrón Observer"""

    def __init__(self):
        self._observadores = []

    def agregar_observador(self, observador: IObservador):
        if observador not in self._observadores:
            self._observadores.append(observador)

    def eliminar_observador(self, observador: IObservador):
        if observador in self._observadores:
            self._observadores.remove(observador)

    def notificar_observadores(self, mensaje: str):
        for observador in self._observadores:
            observador.actualizar(mensaje)
