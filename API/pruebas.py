from Asistente import Asistente

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
    bot_response = Asistente.assistant(user_input, "0")
    # Imprimir respuesta del asistente
    print("Asistente:", bot_response)