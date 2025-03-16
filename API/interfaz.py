import chainlit as cl
import httpx # cliente HTTP para enviar solicitudes a la API

# Variable para almacenar el asistente (pero sin instanciarlo aún)
asistente = None  

API_URL = "http://127.0.0.1:5000/asistente"

@cl.on_chat_start
async def welcome():
    await cl.Message(content="Hola, soy Castor, tu asistente médico. ¿En qué puedo ayudarte?").send()


@cl.on_message
async def main(message: cl.Message):
    # Enviar mensaje de estado mientras se procesa la solicitud
    respuesta_asistente = cl.Message(content="🛑 **Procesando...**", author="Asistente")
    await respuesta_asistente.send()

    try:
        async with httpx.AsyncClient() as client:
            # Enviar la petición a la API Flask
            response = await client.post(API_URL, json={"message": message.content}, timeout=100)
            response.raise_for_status()  # Lanza un error si la respuesta no es 200 OK

            # Convertir la respuesta a JSON
            data = response.json()
            respuesta = data.get("message", "⚠️ Error en la respuesta de la API")

    except httpx.HTTPStatusError as http_err:
        respuesta = f"❌ Error HTTP {http_err.response.status_code}: {http_err}"
    except httpx.RequestError as req_err:
        respuesta = f"⚠️ Error de conexión: {req_err}"
    except Exception as e:
        respuesta = f"⚠️ Error inesperado: {e}"

    # Enviar la respuesta final
    respuesta_asistente.content = respuesta
    await respuesta_asistente.update()

@cl.on_chat_end
async def goodbye():
    await cl.Message(content="Gracias por usar Castor. ¡Hasta luego!").send()