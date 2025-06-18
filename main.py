from flask import Flask, jsonify, request

app = Flask(__name__)
#CUANDO RECIBAMOS LAS PETICIONES EN ESTA RUTA
@app.route("/webhook/", methods=["POST", "GET"])
def webhook_whatsapp():
    #SI HAY DATOS RECIBIDOS VIA GET
    if request.method == "GET":
        #SI EL TOKEN ES IGUAL AL QUE RECIBIMOS
        if request.args.get('hub.verify_token') == "HolaNovato":
            #ESCRIBIMOS EN EL NAVEGADOR EL VALOR DEL RETO RECIBIDO DESDE FACEBOOK
            return request.args.get('hub.challenge')
        else:
            #SI NO SON IGUALES RETORNAMOS UN MENSAJE DE ERROR
            return "Error de autentificacion."
    #RECIBIMOS TODOS LOS DATOS ENVIADO VIA JSON
    data=request.get_json()
    #EXTRAEMOS EL NUMERO DE TELEFONO Y EL MANSAJE
    mensaje="Telefono:"+data['entry'][0]['changes'][0]['value']['messages'][0]['from']
    mensaje=mensaje+"|Mensaje:"+data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
    #ESCRIBIMOS EL NUMERO DE TELEFONO Y EL MENSAJE EN EL ARCHIVO TEXTO
    f = open("texto.txt", "w")
    f.write(mensaje)
    f.close()
    #RETORNAMOS EL STATUS EN UN JSON
    return jsonify({"status": "success"}, 200)

#INICIAMSO FLASK
if __name__ == "__main__":
    app.run(debug=True)