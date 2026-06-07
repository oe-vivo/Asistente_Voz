"""YouTube, Google y programas (lo que hace el agente en el equipo)."""

from __future__ import annotations

# Cada función recibe la cola del comando (texto tras el verbo) y un callback hablar(msg) que usa el TTS.
# pywhatkit intenta abrir el navegador; si falla, se usa webbrowser como respaldo.
# Para nuevas apps en "abre", amplía resolver_ruta_aplicacion y ALIAS_ETIQUETA en config.py, y detectar_alias_app_en_tokens aquí.

import subprocess
import threading
import time
import webbrowser
from urllib.parse import quote_plus

import pywhatkit

#Nuevas importaciones
import ctypes
from datetime import datetime
import urllib.request
from asistente_voz.config import NTFY_TOPIC

from asistente_voz.config import ALIAS_ETIQUETA, resolver_ruta_aplicacion


def _youtube_url(q: str) -> str:
    return f"https://www.youtube.com/results?search_query={quote_plus(q)}"


def _google_url(q: str) -> str:
    return f"https://www.google.com/search?q={quote_plus(q)}"


def _play_youtube_hilo(q: str) -> None:
    try:
        pywhatkit.playonyt(q)
    except Exception as e:
        print(f"[YouTube] {e} — abriendo búsqueda en el navegador.")
        webbrowser.open(_youtube_url(q))


def _buscar_google_hilo(q: str) -> None:
    try:
        pywhatkit.search(q)
    except Exception as e:
        print(f"[Google] pywhatkit: {e}")
        webbrowser.open(_google_url(q))

def _enviar_ntfy_hilo(mensaje: str) -> None:
    url = f"https://ntfy.sh/{NTFY_TOPIC}"
    datos = mensaje.encode('utf-8')
    
    req = urllib.request.Request(
        url, 
        data=datos, 
        headers={"Title": "Asistente de Voz PC"}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                print(f"[Notificación] Enviada con éxito al Celular.")
    except Exception as e:
        print(f"[Notificación] Error al conectar con ntfy: {e}")


def ejecutar_reproducir_youtube(consulta: str, hablar) -> None:
    q = consulta.strip()
    if not q:
        hablar("Di qué quieres reproducir en YouTube.")
        return
    msg = f"Reproduciendo {q} en YouTube."
    print(msg)
    hablar(msg)
    time.sleep(0.7)
    threading.Thread(target=_play_youtube_hilo, args=(q,), daemon=True, name="yt").start()


def ejecutar_busqueda_google(consulta: str, hablar) -> None:
    q = consulta.strip()
    if not q:
        hablar("Di qué quieres buscar en Google.")
        return
    msg = f"Buscando {q} en Google."
    print(msg)
    hablar(msg)
    time.sleep(0.5)
    threading.Thread(target=_buscar_google_hilo, args=(q,), daemon=True, name="gg").start()


def ejecutar_abrir_aplicacion(alias: str, hablar) -> None:
    alias = alias.lower()
    ruta = resolver_ruta_aplicacion(alias)
    etiqueta = ALIAS_ETIQUETA.get(alias, alias)
    if ruta is None:
        hablar(f"No encontré instalada la aplicación {etiqueta}. Revisa config.py.")
        print(f"No hay ruta para: {alias}")
        return
    msg = f"Abriendo {etiqueta}."
    print(msg)
    hablar(msg)
    time.sleep(0.5)
    try:
        subprocess.Popen([str(ruta)], shell=False)
    except OSError as e:
        hablar("No pude lanzar la aplicación.")
        print(e)


def detectar_alias_app_en_tokens(tokens: list[str]) -> str | None:
    # Primera coincidencia con la lista; debe alinearse con lo que entiende resolver_ruta_aplicacion.
    apps = ("notepad", "word", "edge", "documento")
    found: str | None = None
    for t in tokens:
        if t in apps:
            found = t
    return found

def ejecutar_tomar_nota(texto_nota: str, hablar) -> None:
    nota = texto_nota.strip()
    if not nota:
        hablar("¿Que quieres que anote?")
        return
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea_nota = f"[{ahora}] {nota}"

    try:
        with open("notas.txt","a", encoding="utf-8") as f:
            f.write("\n"+linea_nota)
            msg = f"Anotado en tu bloc de notas: {nota}"
            print(f"[Notas] Guardado: {linea_nota.strip()}")
            hablar(msg)
    except Exception as e:
        print(f"[Notas] Error al escribir archivo: {e}")
        hablar("Lo siento, no pude guardar la nota en el archivo")

def ejecutar_decir_tiempo(tokens_cola: list[str], hablar) -> None:
    frase_cola = " ".join(tokens_cola).lower()
    ahora = datetime.now()

    pedir_fecha = "fecha" in frase_cola
    pedir_hora = "hora" in frase_cola

    if not pedir_fecha and not pedir_hora:
        pedir_hora = True
        pedir_fecha= True

    mensajes= []
    if pedir_fecha:
        meses = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"]
        fecha_str = f"{ahora.day} de {meses[ahora.month-1]} del {ahora.year}"
        mensajes.append(f"Hoy es {fecha_str}")
    if pedir_hora:
        hora_str = ahora.strftime("%I:%M %p")
        mensajes.append(f"Son las {hora_str}")
    
    msg = ", y ".join(mensajes)
    print(f"[Tiempo] {msg}")
    hablar(msg)

def ejecutar_bloquear_equipo(hablar) -> None:
    msg = "Bloqueando computadora."
    print(f"[Sistema] {msg}")
    hablar(msg)
    time.sleep(0.5)
    
    ctypes.windll.user32.LockWorkStation()

def ejecutar_enviar_telefono(texto_notificacion: str, hablar) -> None:
    msg_limpio = texto_notificacion.strip()
    if not msg_limpio:
        hablar("¿Qué mensaje quieres que envíe a tu teléfono?")
        return
        
    msg_confirmacion = f"Enviando mensaje al teléfono: {msg_limpio}."
    print(msg_confirmacion)
    hablar(msg_confirmacion)
    
# Lo lanzamos en un hilo para que la red no congele la voz del asistente
    threading.Thread(
        target=_enviar_ntfy_hilo, 
        args=(msg_limpio,), 
        daemon=True, 
        name="ntfy"
    ).start()

