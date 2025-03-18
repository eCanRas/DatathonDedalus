
import chainlit as cl
import httpx # cliente HTTP para enviar solicitudes a la API
import asyncio

# Variable para almacenar el asistente (pero sin instanciarlo aún)
asistente = None  

API_URL = "http://127.0.0.1:5000/asistente"

async def send_request(client, message, conversation_id):
    response = await client.post(API_URL,
                                 json={
                                     "message": message.content,
                                     "user_id": conversation_id,},
                                 timeout=100)
    return response

async def show_waiting(stop_event, respuesta_asistente):
    while not stop_event.is_set():
        respuesta_asistente.content = "🛑 **Procesando**"
        await respuesta_asistente.update()
        await asyncio.sleep(0.5)
        for i in range(5):
            puntos = "🛑 **Procesando"
            for j in range(i):
                puntos += "."
            puntos += "**"
            respuesta_asistente.content = puntos
            await respuesta_asistente.update()
            await asyncio.sleep(0.5)


@cl.on_chat_start
async def welcome():
    await cl.Message(content="Hola, soy Castor, tu asistente médico. ¿En qué puedo ayudarte?").send()


@cl.on_message
async def main(message: cl.Message):
    # Enviar mensaje de estado mientras se procesa la solicitud
    respuesta_asistente = cl.Message(content="🛑 **Procesando...**", author="Asistente")
    await respuesta_asistente.send()

    # Obtener el ID de la conversación (sesión del usuario)
    conversation_id = cl.user_session.get("id")

    respuesta = ""
    url_imagen = ""

    try:
        async with httpx.AsyncClient() as client:

            stop_event = asyncio.Event()  # Evento para detener el mensaje de espera

            # Iniciar la tarea de espera y la solicitud en paralelo
            waiting_task = asyncio.create_task(show_waiting(stop_event, respuesta_asistente))
            response_task = asyncio.create_task(send_request(client, message, conversation_id))

            response = await response_task

            response.raise_for_status()  # Lanza un error si la respuesta no es 200 OK

            # Convertir la respuesta a JSON
            data = response.json()
            respuesta = data.get("message", "⚠️ Error en la respuesta de la API")
            url_imagen = data.get("url_imagen", "")

    except httpx.HTTPStatusError as http_err:
        respuesta = f"❌ Error HTTP {http_err.response.status_code}: {http_err}"
    except httpx.RequestError as req_err:
        respuesta = f"⚠️ Error de conexión: {req_err}"
    except Exception as e:
        respuesta = f"⚠️ Error inesperado: {e}"

    # Detener el mensaje de espera
    stop_event.set()
    await waiting_task  # Asegurar que la tarea se cierre limpiamente

    # Enviar la respuesta final
    respuesta_asistente.content = ""
    for char in respuesta:
        respuesta_asistente.content += char  # Añadimos letra por letra al mensaje
        await respuesta_asistente.update()  # Actualizamos el mensaje en la interfaz
        await asyncio.sleep(0.001)  # Pequeña pausa para simular el efecto de escritura

    if url_imagen != "":
        elements = [cl.Image(name="Ejemplo", path=f".\\{url_imagen}", display="inline")]
        await cl.Message(content="Imagen:", elements=elements).send()

    # respuesta_asistente.content += "\n\n🦫 ¿En qué más puedo ayudarte?"
    # await respuesta_asistente.update()

@cl.on_chat_end
async def goodbye():
    await cl.Message(content="Gracias por usar Castor. ¡Hasta luego!").send()