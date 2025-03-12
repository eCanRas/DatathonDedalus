import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

"""Carga un archivo CSV y lo convierte en texto estructurado para que el modelo lo use."""
def cargar_csv_como_texto(nombre_archivo, max_filas=100):
    try:
        df = pd.read_csv(nombre_archivo)
        df_texto = df.head(max_filas).to_string(index=False)  # Convertir las primeras filas a texto
        columnas = ", ".join(df.columns)  # Obtener nombres de columnas
        contexto = f"El archivo CSV cargado tiene las siguientes columnas: {columnas}. Aquí tienes una muestra:\n{df_texto}"
        return contexto
    except Exception as e:
        return f"Error al cargar el archivo: {str(e)}"

# Archivo CSV de datos
csv_file = ".\\DATA\\cohorte_alegias.csv"
# Carga el contexto del csv
contexto_csv = cargar_csv_como_texto(csv_file)

"""Lee el prompt para el asistente desde un archivo de texto."""
def cargar_prompt(archivo):
    with open(archivo, "r", encoding="utf-8") as f:
        return f.read()

# Ubicacion del prompt
archivo_prompt = "Prompt.txt"
#Carga el prompt
promptAssistant = cargar_prompt(archivo_prompt)

# Instancia el modelo
llm = ChatOpenAI(
    api_key="sk-KVkLObEvkGRLIQ4Thsoz8w",
    base_url="https://litellm.dccp.pbu.dedalus.com",
    model="bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0"
)

# Memoria de historial de conversación
memory = ChatMessageHistory()

"""Función para obtener el historial de una sesión"""
def get_session_history():
    return memory

# Definir un Runnable con historial de mensajes
chat = RunnableWithMessageHistory(llm, get_session_history=get_session_history)

# Función que llama al asistente e inyecta los datos del CSV
def Assitant(user_input):
    response = chat.invoke(
        [
            # Prompt del sistema
            SystemMessage(content=f"{promptAssistant}\n\n{contexto_csv}"),
            # Prompt del usuario
            HumanMessage(content=user_input)
        ],
    )
    return response.content

# Bucle para conversación
while True:
    # Pregunta al usuario
    user_input = input("Tú: ")
    # Permite salir del bucle
    if user_input.lower() in ['salir', 'exit', 'quitar', 'adiós']:
        print("Asistente: ¡Hasta luego!")
        break
    # Obtener respuesta del asistente
    bot_response = Assitant(user_input)
    # Imprimir respuesta del asistente
    print("Asistente:", bot_response)
