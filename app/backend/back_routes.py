from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from trycourier import Courier
from app.config import Config
import psycopg2
from passlib.context import CryptContext

backend_bp = Blueprint('backend', __name__)

@backend_bp.route('/login', methods=['POST'])
def login():
    conn = psycopg2.connect(Config.DB_CONFIG)
    cursor = conn.cursor()
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    query = "SELECT password_hash, salt FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    if result:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        stored_password_hash = result[0]
        salt = result[1]

        if pwd_context.verify(password + salt, stored_password_hash):
            cursor.close()
            conn.close()
            # Si las credenciales son válidas, emite un token JWT
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token), 200
        else:
            cursor.close()
            conn.close()
            return jsonify({'message': 'Credenciales inválidas'}), 401
    else:
        cursor.close()
        conn.close()
        return jsonify({'message': 'User not found'}), 401
    


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

        elif data['currentPage'] == 'peliculas':

            query = "SELECT video_id, link_img, name_pelicula, details FROM peliculas"
            cursor.execute(query)
            peliculas_data = transformar_datos(cursor.fetchall())

            cursor.close()
            conn.close()

            return jsonify({'moviesData': peliculas_data})
        
        elif data['currentPage'] == 'series':

            query = "SELECT video_id, link_img, name_serie, details FROM series"
            cursor.execute(query)
            series_data = transformar_datos(cursor.fetchall())

            cursor.close()
            conn.close()

            return jsonify({'seriesData': series_data})
        
    except Exception as e:
        return jsonify({'error': str(e)})
    

@backend_bp.route('/add_peliculas_series', methods=['POST'])
@jwt_required()
def add_peliculas_series():
    try:
        conn = psycopg2.connect(Config.DB_CONFIG)
        cursor = conn.cursor()

        data = request.get_json()
        if 'peliculas' in data:
            for data_movie in data['peliculas']:
                query = "INSERT INTO peliculas (video_id, link_img, name_pelicula, details) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (*data_movie,))
        elif 'series' in data:
            for data_serie in data['series']:
                query = "INSERT INTO series (video_id, link_img, name_serie, details) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (*data_serie,))
        else:
            return jsonify({'message': 'No se recibieron datos de películas o series'})

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Películas/Series agregadas correctamente'})
    except Exception as e:
        return jsonify({'error': str(e)})

