# Agente de Voz Local - Nuevas Implementaciones

Este documento detalla exclusivamente las funciones añadidas al asistente de voz original, las librerías incorporadas para su ejecución y los comandos exactos para probarlas.

---

## 🛠️ Nuevas Funcionalidades e Integraciones

### 1. Guardar Notas Rápidas (`notas.txt`)
* **Librería añadida:** `datetime` (Nativa de Python).
* **Qué hace:** Captura el texto dictado después del verbo, le añade la fecha y hora actual, y lo escribe al final de un archivo de texto local.
* **Comandos de demostración:**
  * `alexa anota terminar la tarea de inteligencia artificial`
  * `google recuerda revisar el repositorio de github esta noche`
* **Resultado:** Se genera o actualiza el archivo `notas.txt` en la raíz con el formato: `[2026-06-06 21:56:00] terminar la tarea de...`

### 2. Consulta de Fecha y Hora por Voz
* **Librería añadida:** `datetime` (Nativa de Python).
* **Qué hace:** Lee el reloj del sistema operativo, discrimina si pediste hora, fecha o ambas, y genera una respuesta natural para que el asistente la hable.
* **Comandos de demostración:**
  * `siri dime la hora`
  * `cortana da la fecha`
  * `google dime la hora y la fecha`
* **Resultado:** El asistente responde por los altavoces: *"Son las 09:56 PM"* o *"Hoy es 6 de junio del 2026"*.

### 3. Bloqueo de Pantalla de Windows
* **Librería añadida:** `ctypes` (Nativa de Python).
* **Qué hace:** Llama directamente a la API de desarrollo de Windows (`user32.dll`) para suspender la sesión del usuario al instante, sin abrir ventanas de consola.
* **Comandos de demostración:**
  * `google bloquea la computadora`
  * `alexa bloquea el equipo`
* **Resultado:** La computadora se bloquea inmediatamente (pantalla de bloqueo de Windows, equivalente a presionar *Win + L*).

### 4. Notificaciones Push al iPhone
* **Librerías añadidas:** `urllib.request` y `threading` (Nativas de Python). App móvil **NTFY** (iOS).
* **Qué hace:** Envía un paquete de datos HTTP POST en segundo plano con el texto dictado hacia un canal público de NTFY. El iPhone recibe la notificación flotante al milisegundo.
* **Comandos de demostración:**
  * `alexa envia sacar la basura en diez minutos`
  * `siri manda revisar el horno`
* **Resultado:** El iPhone vibra y muestra una notificación flotante en la pantalla con el texto dictado.
