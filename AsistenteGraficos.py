from idlelib.run import print_exception

import pandas as pd
import io
import matplotlib.pyplot as plt
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_experimental.agents.agent_toolkits.csv.base import create_pandas_dataframe_agent

import os
from dotenv import load_dotenv

from langchain_core.callbacks import CallbackManager, BaseCallbackHandler

class CodeCaptureCallback(BaseCallbackHandler):
    """Intercepta el código Python generado por el agente"""
    def __init__(self):
        self.code_snippets = []  # Lista para almacenar los códigos generados

    def on_tool_start(self, serialized, input_str, **kwargs):
        if "python_repl_ast" in serialized["name"]:
            self.code_snippets.append(input_str)  # Guarda el código generado


class AsistenteGraficos:

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
        archivo_prompt = "API/prompt.txt"
        #Carga el prompt
        self.promptAssistant = self.cargar_prompt(archivo_prompt)

        self.capture_callback = CodeCaptureCallback()

        # Cargar las variables de entorno desde .env
        load_dotenv(dotenv_path="API/.env")
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

        self.df_alergias = pd.read_csv(".\\DATA\\cohorte_alegias.csv")
        self.df_condiciones = pd.read_csv(".\\DATA\\cohorte_condiciones.csv")
        self.df_encuentros = pd.read_csv(".\\DATA\\cohorte_encuentros.csv")
        self.df_medicaciones = pd.read_csv(".\\DATA\\cohorte_medicationes.csv")
        self.df_pacientes = pd.read_csv(".\\DATA\\cohorte_pacientes.csv")
        self.df_procedimientos = pd.read_csv(".\\DATA\\cohorte_procedimientos.csv")
        self.dataframes = {
            "df1": self.df_pacientes,
            "df2": self.df_alergias,
            "df3": self.df_condiciones,
            "df4": self.df_encuentros,
            "df5": self.df_medicaciones,
            "df6": self.df_procedimientos
        }
        # Crear el callback
        capture_callback = CodeCaptureCallback()
        # Crea el agente para cargar el csv
        agent_executor = create_pandas_dataframe_agent(
            llm,
            # Carga los ficheros
            [pd.read_csv(".\\DATA\\cohorte_alegias.csv"),
            pd.read_csv(".\\DATA\\cohorte_condiciones.csv"),
            pd.read_csv(".\\DATA\\cohorte_encuentros.csv"),
            pd.read_csv(".\\DATA\\cohorte_medicationes.csv"),
            pd.read_csv(".\\DATA\\cohorte_pacientes.csv"),
            pd.read_csv(".\\DATA\\cohorte_procedimientos.csv")],
            verbose=True,
            allow_dangerous_code=True,
            # handle_parsing_errors=True
            callback_manager = CallbackManager([capture_callback])
        )

        # Definir un Runnable con historial de mensajes
        self.chat = RunnableWithMessageHistory(
            agent_executor,
            get_session_history=self.get_session_history,
            # handle_parsing_errors=True
        )

    def generar_grafica(self, code):
        """Ejecuta código generado dinámicamente para crear una gráfica."""
        try:
            local_vars = {"plt": plt, "pd": pd, **self.dataframes}  # Variables disponibles

            exec(code, {}, local_vars)  # Ejecutamos el código generado
            plt.close() # cierra gráfica anterior

            plt.show()
            # Guardar la imagen si se generó una figura
            if plt.gcf().get_axes():  # ✅ Si hay una gráfica activa
                img_bytes = io.BytesIO()
                plt.savefig(img_bytes, format="png")
                #plt.close()  # Cerrar la figura
                img_bytes.seek(0)
                return img_bytes
            else:
                print("⚠️ No se generó ninguna gráfica.")
                return None

        except Exception as e:
            print(f"❌ ERROR AL GENERAR LA GRÁFICA: {e}")
            return None

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


            return response["output"]
        except Exception as e:
            print(f"\033[91mError: {e}\033[0m")
            return "Se ha producido un error, vuelva a intentarlo"

Asistente = AsistenteGraficos()

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

    # Verificar si el callback ha capturado código
    if Asistente.capture_callback.code_snippets and ["gráfica", "gráfico"] in user_input:
        # Obtener el último código generado
        generated_code = Asistente.capture_callback.code_snippets[-1]

        # Ejecutar el código y generar la gráfica
        image_bytes = Asistente.generar_grafica(generated_code)

        if image_bytes:
            with open("grafica.png", "wb") as f:
                f.write(image_bytes.getbuffer())  # Guardar la imagen
            print("📊 Gráfica generada y guardada como 'grafica.png'.")