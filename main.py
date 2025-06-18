from flask import Flask, jsonify, request
import os # Importamos 'os' para posibles usos futuros con variables de entorno

app = Flask(__name__)

# CUANDO RECIBAMOS LAS PETICIONES EN ESTA RUTA
@app.route("/webhook/", methods=["POST", "GET"])
def webhook_whatsapp():
    # SI HAY DATOS RECIBIDOS VIA GET
    if request.method == "GET":
        # SI EL TOKEN ES IGUAL AL QUE RECIBIMOS
        # Es buena práctica obtener el token de verificación de una variable de entorno en producción
        # Si no quieres complicarte ahora, puedes dejar "HolaNovato" directamente.
        # verify_token = os.getenv("VERIFY_TOKEN", "HolaNovato") # Ejemplo con variable de entorno
        verify_token = "HolaNovato" # Usando el valor directamente como lo tienes

        if request.args.get('hub.verify_token') == verify_token:
            # ESCRIBIMOS EN EL NAVEGADOR EL VALOR DEL RETO RECIBIDO DESDE FACEBOOK
            return request.args.get('hub.challenge')
        else:
            # SI NO SON IGUALES RETORNAMOS UN MENSAJE DE ERROR
            return "Error de autentificacion."

    # RECIBIMOS TODOS LOS DATOS ENVIADOS VIA JSON
    data = request.get_json()

    # **ADVERTENCIA IMPORTANTE:**
    # La lógica para acceder a los datos como data['entry'][0]['changes'][0]['value']['messages'][0]['from']
    # puede fallar si la estructura JSON esperada no viene exactamente así.
    # Es crucial añadir manejo de errores (try-except) y validaciones para evitar crasheos.
    # Además, escribir directamente a 'texto.txt' en un entorno de Render (o cualquier PaaS)
    # no es persistente y no es una buena práctica. Los archivos se pierden cuando el contenedor
    # se reinicia o se escala. Para almacenar datos, necesitas una base de datos o un servicio de almacenamiento en la nube.
    # Por ahora, dejo la lógica tal cual para que veas el despliegue, pero ten esto en cuenta.

    try:
        # EXTRAEMOS EL NUMERO DE TELEFONO Y EL MENSAJE
        # Se asume una estructura de datos muy específica aquí.
        # Considera usar librerías como Pydantic o validación más robusta.
        phone_number = data['entry'][0]['changes'][0]['value']['messages'][0]['from']
        message_body = data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
        
        mensaje = f"Telefono:{phone_number}|Mensaje:{message_body}"

        # **ESTO NO ES PERSISTENTE EN RENDER (o la mayoría de los servicios PaaS)**
        # Si realmente necesitas registrar esto, considera usar una base de datos (SQL, NoSQL),
        # un servicio de logs o un almacenamiento de objetos (ej. AWS S3).
        with open("texto.txt", "w") as f:
            f.write(mensaje)
        
        print(f"Webhook recibido y procesado: {mensaje}") # Para ver en los logs de Render

        # RETORNAMOS EL STATUS EN UN JSON
        return jsonify({"status": "success"}, 200)

    except KeyError as e:
        print(f"Error al procesar el JSON recibido: Falta la clave {e}. Datos recibidos: {data}")
        return jsonify({"status": "error", "message": f"Error en la estructura del JSON: {e}"}, 400)
    except Exception as e:
        print(f"Un error inesperado ocurrió: {e}. Datos recibidos: {data}")
        return jsonify({"status": "error", "message": f"Error interno del servidor: {e}"}, 500)

# No se necesita el bloque if __name__ == "__main__": app.run(debug=True)
# Gunicorn se encargará de iniciar la aplicación.