import sys
import os

try:
    import chainlit as cl
    from Asistente import Asistente  # Asegura que el nombre del módulo sea correcto y en minúsculas
except ModuleNotFoundError as e:
    print(f"Error: {e}. Asegúrate de que el módulo está instalado y accesible.")
    sys.exit(1)

@cl.on_message
async def main(message: cl.Message):
    try:
        # Obtener respuesta del asistente
        bot_response = Asistente.assitant(message.content)
        
        # Enviar respuesta con color verde
        await cl.Message(content=bot_response, author="Asistente").send()
    except Exception as e:
        await cl.Message(content=f"Error procesando el mensaje: {str(e)}", author="Asistente").send()
