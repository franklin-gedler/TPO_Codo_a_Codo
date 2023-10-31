from flask import Blueprint, request, jsonify
from trycourier import Courier
from app.config import Config
import psycopg2

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
    try:
        conn = psycopg2.connect(Config.DB_CONFIG)
        cursor = conn.cursor()
        data = request.get_json()

        transformar_datos = lambda rows: [{'video': row[0], 'img': row[1], 'alt': row[2], 'details': row[3].replace('\n', '')} for row in rows]

        if data['currentPage'] == 'inicio':

            '''# Realiza la consulta para obtener las últimas 4 películas
            cursor = conn.cursor()
            cursor.execute("SELECT video_id, link_img, name_pelicula FROM peliculas ORDER BY id DESC LIMIT 4")
            peliculas_data = [{'video': row[0], 'img': row[1], 'alt': row[2]} for row in cursor.fetchall()]
            cursor.close()

            # Realiza la consulta para obtener las últimas 4 series
            cursor = conn.cursor()
            cursor.execute("SELECT video_id, link_img, name_serie FROM series ORDER BY id DESC LIMIT 4")
            series_data = [{'video': row[0], 'img': row[1], 'alt': row[2]} for row in cursor.fetchall()]
            cursor.close()'''

            query_base = "SELECT columns FROM table ORDER BY id DESC LIMIT 4"
            common_columns_name = ['video_id', 'link_img']
            
            # Obtengo las últimas 4 películas de la base de datos
            query_peliculas = query_base.replace('columns', f"{', '.join(common_columns_name)}, name_pelicula, details").replace('table', 'peliculas')
            cursor.execute(query_peliculas)
            peliculas_data = transformar_datos(cursor.fetchall())

            # Obtengo las últimas 4 series de la base de datos
            query_series = query_base.replace('columns', f"{', '.join(common_columns_name)}, name_serie, details").replace('table', 'series')
            cursor.execute(query_series)
            series_data = transformar_datos(cursor.fetchall())

            cursor.close()
            conn.close()

            return jsonify({'moviesData': peliculas_data, 'seriesData': series_data})

            '''movies_data = list(
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
            return jsonify({'moviesData': movies_data, 'seriesData': series_data})'''
        
        elif data['currentPage'] == 'peliculas':

            query = "SELECT video_id, link_img, name_pelicula, details FROM peliculas"
            cursor.execute(query)
            peliculas_data = transformar_datos(cursor.fetchall())

            cursor.close()
            conn.close()

            '''movies_data = list(
                10*(
                    { 'video': 'S7jL176VXNA?si=j5Ti7yLxdDzpubjl', 'img': '/static/image/juegos_prohibidos.webp', 'alt': 'Pelicula 1' },
                    { 'video': 'jzQn0-WH4WM?si=Dzw8wuuFtZTt628r', 'img': '/static/image/retribucion.jpg', 'alt': 'Pelicula 2' },
                )
            )'''

            return jsonify({'moviesData': peliculas_data})
        
        elif data['currentPage'] == 'series':

            query = "SELECT video_id, link_img, name_serie, details FROM series"
            cursor.execute(query)
            series_data = transformar_datos(cursor.fetchall())

            cursor.close()
            conn.close()

            '''series_data = list(
                10*(
                    { 'video': 'S7jL176VXNA?si=j5Ti7yLxdDzpubjl', 'img': '/static/image/juegos_prohibidos.webp', 'alt': 'Serie 1' },
                    { 'video': 'jzQn0-WH4WM?si=Dzw8wuuFtZTt628r', 'img': '/static/image/retribucion.jpg', 'alt': 'Serie 2' },
                )
            )'''

            return jsonify({'seriesData': series_data})
        
    except Exception as e:
        return jsonify({'error': str(e)})
    

@backend_bp.route('/add_peliculas_series', methods=['POST'])
def add_peliculas_series():
    try:
        conn = psycopg2.connect(Config.DB_CONFIG)
        cursor = conn.cursor()

        data = request.get_json()
        if 'peliculas' in data:
            for data_movie in data['peliculas']:
                query = "INSERT INTO peliculas (video_id, link_img, name_pelicula, details) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (*data_movie,))
        else:
            for data_serie in data['series']:
                query = "INSERT INTO series (video_id, link_img, name_serie, details) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (*data_serie,))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Películas/Series agregadas correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)})

    '''data = request.get_json()

    conn = psycopg2.connect(Config.DB_CONFIG)
    cur = conn.cursor()

    if data['type'] == 'pelicula':
        cur.execute(
            "INSERT INTO peliculas (nombre, descripcion, imagen, video) VALUES (%s, %s, %s, %s)",
            (data['nombre'], data['descripcion'], data['imagen'], data['video'])
        )
    elif data['type'] == 'serie':
        cur.execute(
            "INSERT INTO series (nombre, descripcion, imagen, video) VALUES (%s, %s, %s, %s)",
            (data['nombre'], data['descripcion'], data['imagen'], data['video'])
        )
    
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({'status': 'ok'})'''

