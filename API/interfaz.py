import chainlit as cl
from Asistente import Asistente 

# Variable para almacenar el asistente (pero sin instanciarlo aún)
asistente = None  

@cl.on_message
async def main(message: cl.Message):
    global asistente
    if asistente is None:  # Solo se instancia cuando se recibe el primer mensaje
        asistente = Asistente()
    
    if message.content in ['salir', 'exit', 'quitar', 'adiós']:
        await cl.Message(content="Si necesitas más infomación, aquí estará Castor para ayudarle en investigación").send()
        exit()
    bot_response = asistente.assitant(message.content)
    await cl.Message(content=bot_response, author="Asistente").send()

