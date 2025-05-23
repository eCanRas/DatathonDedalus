# pip install tabulate

import pandas as pd
from flask import jsonify
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_experimental.agents.agent_toolkits.csv.base import create_pandas_dataframe_agent

import os
from dotenv import load_dotenv
import re

class Asistente:

    """Lee el prompt para el asistente desde un archivo de texto."""
    def cargar_prompt(self, archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            return f.read()

    """Función para obtener el historial de una sesión"""
    def get_session_history(self, session_id):
        if session_id not in self.memory:
            self.memory[session_id] = ChatMessageHistory()
        return self.memory[session_id]
                   
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

        # Cargar los ficheros como DataFrames
        dfs = [
            pd.read_csv("..\\DATA\\cohorte_alergias.csv"),
            pd.read_csv("..\\DATA\\cohorte_condiciones.csv"),
            pd.read_csv("..\\DATA\\cohorte_encuentros.csv"),
            pd.read_csv("..\\DATA\\cohorte_medicationes.csv"),
            pd.read_csv("..\\DATA\\cohorte_pacientes.csv"),
            pd.read_csv("..\\DATA\\cohorte_procedimientos.csv"),
        ]

        # Instancia el modelo
        llm = ChatOpenAI(
            api_key=api_key,
            base_url=base_url,
            model=model,
            temperature=0
        )

        # Memoria de historial de conversación
        self.memory = {}

        # Crea el agente para cargar el csv
        agent_executor = create_pandas_dataframe_agent(
            llm,
            # Carga los ficheros
            dfs,
            verbose=True,
            allow_dangerous_code=True,
            handle_parsing_errors=True
        )


        # Definir un Runnable con historial de mensajes
        self.chat = RunnableWithMessageHistory(
            agent_executor,
            get_session_history=self.get_session_history,
            handle_parsing_errors=True
        )

        # Función que llama al asistente e inyecta los datos del CSV
    def assistant(self, user_input, user_id):
        url_grafica = ""
        url_csv = ""
        try:
            response = self.chat.invoke(
                [
                    # Prompt del sistema
                    SystemMessage(content=f"{self.promptAssistant}"), # \n\n{contexto_csv}
                    # Prompt del usuario
                    HumanMessage(content=user_input)
                ],
                config={"configurable": {"session_id": user_id}}  # Pasar identificador de sesión
            )

            # Optiene el nombre de la imagen si se ha generado
            match = re.search(r"([^']+\.png)", response["output"])
            if match and os.path.exists(f".\/{match.group(1)}"):
                url_grafica = match.group(1)

            # Optiene el nombre de la imagen si se ha generado
            match = re.search(r"([^']+\.csv)", response["output"])
            if match and os.path.exists(f".\/{match.group(1)}"):
                url_csv = match.group(1)

            resultado = response["output"]
        
        except Exception as e:
            if " Could not parse LLM output" in str(e):
                resultado = str(e).split("`")[3]
            else:
                print(f"\033[91mError: {e}\033[0m")
                resultado =  "Se ha producido un error, vuelva a intentarlo"

        data = {
            "message": resultado,
            "url_imagen": f"{url_grafica}",
            "url_csv": f"{url_csv}"
        }

        json_string = jsonify(data)

        return json_string