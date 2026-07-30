import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def obtener_conexion():
    conexion = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"),
        options=f"-c search_path={os.getenv('DB_SCHEMA')}"
    )
    return conexion
