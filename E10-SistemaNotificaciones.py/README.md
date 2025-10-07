# 🧩 Sistema de Notificaciones con Patrones de Diseño

## 📘 Descripción
Este proyecto implementa un **Sistema de Notificaciones** que puede enviar mensajes a los usuarios mediante **correo electrónico, SMS o notificaciones push**, aplicando los patrones de diseño **Observer** y **Factory Method**, junto con los **principios SOLID**.

## 🎯 Objetivo
Fortalecer la comprensión del diseño orientado a objetos, el uso de patrones y las buenas prácticas de desarrollo profesional.

---

## 🧱 Patrones Aplicados

### 🔹 Patrón Observer
Permite que los usuarios (observadores) sean notificados automáticamente cuando el sistema (sujeto) envía un nuevo mensaje.
- `NotificacionSubject`: mantiene y notifica a los observadores.
- `Usuario`: implementa la interfaz `IObservador` para recibir notificaciones.

### 🔹 Patrón Factory Method
Encapsula la creación de distintos tipos de notificaciones.
- `INotificacion`: interfaz base.
- `EmailNotificacion`, `SMSNotificacion`, `PushNotificacion`: implementaciones concretas.
- `NotificacionFactory`: crea el tipo de notificación según el parámetro recibido.

---

## 🧩 Principios SOLID Aplicados

| Principio | Aplicación |
|------------|-------------|
| **S - Responsabilidad Única** | Cada clase tiene una única función (Usuario, Fábrica, Notificación, etc.). |
| **O - Abierto/Cerrado** | Se pueden agregar nuevos tipos de notificación sin modificar el código existente. |
| **L - Sustitución de Liskov** | Las subclases de `INotificacion` pueden sustituir a su clase base sin alterar el comportamiento. |
| **I - Segregación de Interfaces** | Se usan interfaces específicas (`IObservador`, `INotificacion`). |
| **D - Inversión de Dependencias** | El código depende de abstracciones (interfaces), no de implementaciones concretas. |

---

## 🚀 Ejecución

```bash
python main.py
