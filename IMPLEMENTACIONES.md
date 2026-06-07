# Agente de Voz Local Inteligente (Pipeline NLP & Actuadores Asíncronos)

Este repositorio contiene la arquitectura completa de un **Agente de Voz Local Inteligente** desarrollado en Python. El sistema implementa el ciclo clásico de la Inteligencia Artificial: **Percibir, Interpretar y Actuar**, abstrayendo el flujo de audio analógico hacia un pipeline de procesamiento lingüístico formal y ejecutando efectos secundarios de manera concurrente en el sistema operativo y en dispositivos móviles.

---

## 🛠️ Nuevas Implementaciones y Arquitectura de Valor Añadido

El proyecto original ha sido drásticamente expandido e interconectado mediante la adición de nuevas reglas sintácticas, controladores nativos de bajo nivel y protocolos abiertos de red. A continuación, se documentan las características integradas de nivel de producción:

### 1. Actuador de Persistencia Local (Módulo de Notas Rápidas)
* **Verbos Sintácticos:** `anota`, `recuerda`
* **Estructura del Comando:** *"[Wake Word] + anota/recuerda + [Texto de Dictado Libre]"*
* **Mecanismo Técnico:** Captura de forma asíncrona la cola completa del comando lingüístico (`cola`), importa el módulo nativo `datetime` para inyectar una estampa de tiempo formateada con precisión (`%Y-%m-%d %H:%M:%S`), y garantiza la persistencia mediante un manejador seguro de archivos (`with open()`) escribiendo de manera incremental en un archivo físico denominado `notas.txt`.

### 2. Regla de Consulta de Estado (Fecha y Hora Dinámica)
* **Verbos Sintácticos:** `dime`, `da`
* **Estructura del Comando:** *"[Wake Word] + dime/da + la hora / la fecha / el tiempo"*
* **Mecanismo Técnico:** Un analizador lógico discrimina los tokens terminales de la cola para identificar si la solicitud requiere la fecha larga en español (mapeada dinámicamente mediante vectores de strings para los meses) o la hora en formato legible de 12 horas (`%I:%M %p`). El resultado se compila en una cadena estructurada que se despacha directamente hacia el motor de síntesis de voz (TTS).

### 3. Actuador del Sistema Operativo de Bajo Nivel (Bloqueo de Equipo)
* **Verbos Sintácticos:** `bloquea`
* **Estructura del Comando:** *"[Wake Word] + bloquea + la computadora / el equipo / la pc"*
* **Mecanismo Técnico:** Para mitigar la latencia y evitar la apertura de subtareas pesadas en la consola de comandos, se importó la librería nativa `ctypes` para interactuar directamente con el *kernel* y el subsistema de ventanas de Windows. El controlador realiza una invocación limpia y directa a la API de Win32 mediante `ctypes.windll.user32.LockWorkStation()`, suspendiendo de forma inmediata la sesión activa del usuario (equivalente a *Win + L*).

### 4. Actuador de Red e Interconectividad Móvil (PC a iPhone en Tiempo Real)
* **Verbos Sintácticos:** `envia`, `manda`
* **Estructura del Comando:** *"[Wake Word] + envia/manda + [Mensaje Push Personalizado]"*
* **Mecanismo Técnico:** Integración de conectividad multiplataforma asíncrona mediante el módulo de red nativo `urllib.request`. El sistema codifica los tokens libres en un búfer UTF-8 y despacha una petición de red asíncrona de tipo `HTTP POST` hacia los servidores del protocolo abierto **NTFY**, enlazándose a un identificador único de tópicos (`NTFY_TOPIC`). El iPhone del usuario, suscrito de forma nativa a dicho canal a través de la app de iOS, recibe e intercepta una notificación push flotante al milisegundo de completarse la orden.

---

## 📐 Pipeline de Procesamiento Lingüístico (Filtros de Datos)

El agente procesa cada señal de audio entrante a través de un esquema rígido y modular de transformación secuencial:

```
[ Entrada de Audio Analógico ]
              │
              ▼ (Librería speech_recognition)
[ API de Google Speech-to-Text (es-MX) ] -> String Crudo
              │
              ▼ (Módulo texto.py -> normalize())
[ Limpieza y Sanitización de Caracteres ] -> Minúsculas, sin acentos ni puntuación
              │
              ▼ (Módulo texto.py -> poner_wake_word_primera())
[ Reordenamiento Sintáctico Dinámico ] -> Garantiza Wake Word en Índice Cero
              │
              ▼ (Módulo texto.py -> tokenizar())
[ Vector de Tokens Terminales ] -> Separación por espacios en Lista de Python
              │
              ▼ (Módulo gramatica.py -> _tokens_para_parser())
[ Inyección de Token Comodín __objeto__ ] -> Encapsulamiento de colas abiertas
              │
              ▼ (Módulo gramatica.py -> ChartParser)
[ Gramática Libre de Contexto NLTK (CFG) ] -> Verificación del Árbol de Derivación
              │
              ▼  (Si el Árbol Sintáctico es Válido -> True)
[ Despachador de Acciones en agente.py ]
              │
              ▼ (Módulo acciones.py -> threading.Thread)
[ Actuador Concurrente (Hilos Demonio) ] -> Efecto secundario web, local o móvil
```

---

## 🚀 Resolución de Retos Técnicos y Dificultades

* **Inestabilidad de Dispositivos de Captura:** El enumerador de hardware de audio en Windows tendía a reorganizar aleatoriamente los índices lógicos de los micrófonos, causando caídas del hilo de escucha. Se solucionó implementando un parámetro de anulación explícito (`MIC_DEVICE_INDEX_OVERRIDE = 1`) en `config.py` para anclar estáticamente el sistema al hardware de alta definición.
* **Rigidez del Parser de NLTK:** Las gramáticas formales CFG restringen las entradas a un vocabulario previamente declarado, haciendo imposible validar dictados abiertos (búsquedas o notas libres). El reto se superó mediante un filtro de sustitución sintáctica intermedio en `_tokens_para_parser` que recorta la cola de la oración y la enmascara temporalmente bajo el token no-terminal `__objeto__`, permitiendo al `ChartParser` validar la estructura de la oración (`S -> AV VP`) en milisegundos sin corromper la información dictada.
* **Restricciones del Entorno iOS:** Ante las limitaciones y retiro de librerías comerciales como Pushbullet de la tienda de aplicaciones de Apple, la infraestructura de red fue rediseñada utilizando peticiones web nativas asíncronas dirigidas al protocolo abierto de NTFY, permitiendo la comunicación libre de costes e instantánea hacia dispositivos iOS.

---

## 🛠️ Tecnologías e Importaciones Clave
* **NLTK (Natural Language Toolkit):** Motor para la definición y análisis sintáctico de la Gramática Libre de Contexto (CFG).
* **SpeechRecognition (Google STT API):** Transcriptor acústico y conversión de ondas analógicas a strings estables.
* **pyttsx3:** Sintetizador de voz local (TTS) para el retorno auditivo de eventos.
* **ctypes:** Interfaz de funciones foráneas nativas para la comunicación con las DLLs del kernel de Windows (`user32.dll`).
* **urllib.request:** Cliente HTTP nativo para la inyección asíncrona de peticiones web (POST) sin dependencias externas pesadas.
* **threading:** Motor de concurrencia para el despacho de hilos tipo Demonio, aislando los efectos secundarios del bucle principal de interfaz.
