from flask import Flask, request, jsonify
from Asistente import  Asistente

# Instancia de FastAPI
app = Flask(__name__)

# Instanciar el asistente
asistente = Asistente()


# Endpoint para recibir peticiones
@app.route("/asistente", methods=["POST"])
def asistente_endpoint():
    data = request.get_json()  # recibe el JSON enviado por interfaz
    user_message = data.get("message", "")  # obtiene el mensaje del usuario
    user_id = data.get("user_id", "")

    if not user_message:
        return jsonify({"message": "No se ha enviado un mensaje"})

    response = asistente.assistant(user_message, user_id)
    response = jsonify({"message": response})
    return response


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)