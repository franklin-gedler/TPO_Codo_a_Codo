from flask import Blueprint, request, jsonify, url_for, current_app
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

@backend_bp.route('/movies_series_data', methods=['POST'])
def movie_series_data():
    # Este endpoint simula una base de datos
    data = request.get_json()

    if data['currentPage'] == 'inicio':

        movies_data = list(
            2*(
                { 'video': 'S7jL176VXNA?si=j5Ti7yLxdDzpubjl', 'img': '/static/image/juegos_prohibidos.webp', 'alt': 'Pelicula 1' },
                { 'video': 'jzQn0-WH4WM?si=Dzw8wuuFtZTt628r', 'img': '/static/image/retribucion.jpg', 'alt': 'Pelicula 2' },
            )
        )

        series_data = list(
            2*(
                { 'video': 'S7jL176VXNA?si=j5Ti7yLxdDzpubjl', 'img': '/static/image/juegos_prohibidos.webp', 'alt': 'Serie 1' },
                { 'video': 'jzQn0-WH4WM?si=Dzw8wuuFtZTt628r', 'img': '/static/image/retribucion.jpg', 'alt': 'Serie 2' },
            )
        )
        return jsonify({'moviesData': movies_data, 'seriesData': series_data})
    
    elif data['currentPage'] == 'peliculas':

        movies_data = list(
            10*(
                { 'video': 'S7jL176VXNA?si=j5Ti7yLxdDzpubjl', 'img': '/static/image/juegos_prohibidos.webp', 'alt': 'Pelicula 1' },
                { 'video': 'jzQn0-WH4WM?si=Dzw8wuuFtZTt628r', 'img': '/static/image/retribucion.jpg', 'alt': 'Pelicula 2' },
            )
        )

        return jsonify({'moviesData': movies_data})
    
    elif data['currentPage'] == 'series':

        series_data = list(
            10*(
                { 'video': 'S7jL176VXNA?si=j5Ti7yLxdDzpubjl', 'img': '/static/image/juegos_prohibidos.webp', 'alt': 'Serie 1' },
                { 'video': 'jzQn0-WH4WM?si=Dzw8wuuFtZTt628r', 'img': '/static/image/retribucion.jpg', 'alt': 'Serie 2' },
            )
        )

        return jsonify({'seriesData': series_data})
