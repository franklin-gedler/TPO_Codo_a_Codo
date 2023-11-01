from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    # La variable SECRET_KEY sigue siendo estática
    EMAIL_ADMIN = os.getenv("EMAIL_ADMIN")

    # Configura el atributo COURIER_AUTH_TOKEN para usar la variable de entorno
    COURIER_AUTH_TOKEN = os.getenv("COURIER_AUTH_TOKEN")

    # Configura el atributo DB_CONFIG para usar la variable de entorno
    DB_CONFIG = os.getenv("DB_CONFIG")

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
