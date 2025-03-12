import openai
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

# Configurar el modelo con LiteLLM a través de OpenAI
llm = ChatOpenAI(
    api_key="sk-KVkLObEvkGRLIQ4Thsoz8w",
    base_url="https://litellm.dccp.pbu.dedalus.com",
    model="bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0"
)

# Memoria de historial de conversación
memory = ChatMessageHistory()

# Función para obtener el historial de una sesión (simulada aquí)
def get_session_history(session_id: str):
    return memory  # En una implementación real, usarías una DB o Redis

# Definir un Runnable con historial de mensajes
chat = RunnableWithMessageHistory(llm, get_session_history=get_session_history)

# Interacción con el agente
session_id = "usuario_123"  # ID de sesión ficticio

# Funcion que llama al asistente
def Assitant(user_input):
    response = chat.invoke(
        [HumanMessage(content=user_input)],
        config={"configurable": {"session_id": session_id}}
    )
    return response.content

# Bucle para preguntar continuamente
while True:
    user_input = input("Tú: ")  # Pregunta al usuario
    if user_input.lower() in ['salir', 'exit', 'quitar', 'adiós']:  # Permite salir del bucle
        print("Asistente: ¡Hasta luego!")
        break
    bot_response = Assitant(user_input)  # Obtener respuesta del asistente
    print("Asistente:", bot_response)  # Imprimir respuesta del asistente