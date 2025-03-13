from idlelib.run import print_exception

import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_experimental.agents.agent_toolkits.csv.base import create_pandas_dataframe_agent
from langchain.schema import StrOutputParser

import os
from dotenv import load_dotenv

class Asistente:

    """Lee el prompt para el asistente desde un archivo de texto."""
    def cargar_prompt(self, archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            return f.read()

    """Función para obtener el historial de una sesión"""
    def get_session_history(self):
        return self.memory

    """Constructor de la clase"""
    def __init__(self):
        # Ubicacion del prompt
        archivo_prompt = "Prompt.txt"
        #Carga el prompt
        self.promptAssistant = self.cargar_prompt(archivo_prompt)

        # Cargar las variables de entorno desde .env
        load_dotenv()
        api_key=os.getenv("api_key","")
        base_url=os.getenv("base_url", "")
        model=os.getenv("model", "")

        # Instancia el modelo
        llm = ChatOpenAI(
            api_key=api_key,
            base_url=base_url,
            model=model
        )

        # Memoria de historial de conversación
        self.memory = ChatMessageHistory()

        # Crea el agente para cargar el csv
        agent_executor = create_pandas_dataframe_agent(
            llm,
            # Carga los ficheros
            [pd.read_csv("..\\DATA\\cohorte_alegias.csv"),
            pd.read_csv("..\\DATA\\cohorte_condiciones.csv"),
            pd.read_csv("..\\DATA\\cohorte_encuentros.csv"),
            pd.read_csv("..\\DATA\\cohorte_medicationes.csv"),
            pd.read_csv("..\\DATA\\cohorte_pacientes.csv"),
            pd.read_csv("..\\DATA\\cohorte_procedimientos.csv")],
            verbose=True,
            allow_dangerous_code=True,
            # handle_parsing_errors=True
        )

        # Definir un Runnable con historial de mensajes
        self.chat = RunnableWithMessageHistory(
            agent_executor, # | StrOutputParser(),
            get_session_history=self.get_session_history,
            # handle_parsing_errors=True
        )

        # Función que llama al asistente e inyecta los datos del CSV
    def assitant(self, user_input):
        try:
            response = self.chat.invoke(
                [
                    # Prompt del sistema
                    SystemMessage(content=f"{self.promptAssistant}"), # \n\n{contexto_csv}
                    # Prompt del usuario
                    HumanMessage(content=user_input)
                ],
            )
            print(response)
            return response["output"]
        except Exception as e:
            print(f"\033[91mError: {e}\033[0m")
            return "Se ha producido un error, vuelva a intentarlo"

Asistente = Asistente()

# Bucle para conversación
while True:
    # Pregunta al usuario
    user_input = input("Tú: ")
    # Permite salir del bucle
    if user_input.lower() in ['salir', 'exit', 'quitar', 'adiós']:
        print("Asistente: ¡Hasta luego!")
        break
    # Obtener respuesta del asistente
    bot_response = Asistente.assitant(user_input)
    # Imprimir respuesta del asistente
    print("Asistente:", bot_response)
