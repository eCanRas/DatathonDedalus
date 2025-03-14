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

    response = cl.Message(content= "🛑 **Procesando...**", author="Asistente")    
    await response.send()

    response.content = asistente.assistant(message.content)
    
    await response.update()

