from flask import Blueprint, request, jsonify
from trycourier import Courier
from app.config import Config

backend_bp = Blueprint('backend', __name__)

@backend_bp.route('/sendmail', methods=['POST'])
def sendmail():
    data = request.get_json()

    client = Courier(auth_token=Config.COURIER_AUTH_TOKEN)

    resp = client.send_message(
        message={
            "to": [{
                "email": Config.EMAIL_ADMIN,
            },
            {
                "email": data['email'],
            }],
            "template": "DMH73AJG2HM5E1NGKYFASDA8ESH0",
            "data": {
                "nombre": data['nombre'],
                "email": data['email'],
                "mensaje": data['mensaje'],
                "subject": "Solicitud de Trailers",
            },
        }
    )
    return jsonify(resp)
