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
    response = cl.Message(content= "🛑 **Procesando...**", author="Asistente")    
    await response.send()

    
        # crea un cliente http asincrono
    async with httpx.AsyncClient() as client:
        # Mensaje de procesamiento
        processing_message = cl.Message(content="🛑 **Procesando...**", author="Asistente")    
        await processing_message.send()

        try:
            # Cliente HTTP asincrónico
            async with httpx.AsyncClient() as client:
                # Enviar la petición a la API Flask
                response = await client.post(API_URL, json={"message": message.content})
                response.raise_for_status()  # Lanza un error si la respuesta no es 200 OK

            # Convertir la respuesta a JSON
            data = response.json()
            respuesta_asistente = data.get("message", "Error en la respuesta")

        except Exception as e:
            respuesta_asistente = f"Error en la petición: {e}"

        # Crear el mensaje de respuesta con la respuesta del asistente
        respuesta_final = cl.Message(content=respuesta_asistente, author="Asistente")
        await respuesta_final.send()

    """
    global asistente
    if asistente is None:  # Solo se instancia cuando se recibe el primer mensaje
        asistente = Asistente()
    
    if message.content in ['salir', 'exit', 'quitar', 'adiós']:
        await cl.Message(content="Si necesitas más infomación, aquí estará Castor para ayudarle en investigación").send()
        exit()
    
    
    response = cl.Message(content= "🛑 **Procesando...**", author="Asistente")    
    await response.send()

    response.content = asistente.assistant(message.content)
    print("RESPUESTA: ", response.content)
    
    await response.update()
    """

@cl.on_chat_end
async def goodbye():
    await cl.Message(content="Gracias por usar Castor. ¡Hasta luego!").send()