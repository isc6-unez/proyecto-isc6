from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import os
from dotenv import load_dotenv

# Cargar las credenciales del archivo .env
load_dotenv()

app = FastAPI(title="Modulo de Logistica - CRUD Vehiculos")

# Función centralizada para conectar a la BD
def obtener_conexion():
    try:
        conexion = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        return conexion
    except Exception as e:
        print(f"❌ Error crítico de conexión a PostgreSQL: {e}")
        return None

# Mapeo exacto de las columnas de tu vehiculos.sql
class Vehiculo(BaseModel):
    placa: str                  # VARCHAR(10) - Cambiado a singular según tu SQL
    marca: str                  # VARCHAR(50)
    modelo: str                 # VARCHAR(50) en tu SQL (Texto)
    capacidad_carga: float      # DECIMAL(10,2)
    estado: str = "Disponible"  # VARCHAR(30) - Por defecto 'Disponible' en tu SQL

# 1. RUTA PARA REGISTRAR (POST -> INSERT)
@app.post("/vehiculos")
def registrar_vehiculo(vehiculo: Vehiculo):
    conexion = obtener_conexion()
    if not conexion:
        raise HTTPException(status_code=500, detail="Error de conexión con el servidor de BD")
    
    cursor = conexion.cursor()
    try:
        # id_vehiculo se genera automáticamente en PostgreSQL por ser IDENTITY
        cursor.execute(
            "INSERT INTO dpt.vehiculos (placa, marca, modelo, capacidad_carga, estado) VALUES (%s, %s, %s, %s, %s);",
            (vehiculo.placa, vehiculo.marca, vehiculo.modelo, vehiculo.capacidad_carga, vehiculo.estado)
        )
        conexion.commit()
        cursor.close()
        conexion.close()
        return {"mensaje": f"Vehiculo con placa [{vehiculo.placa}] registrado con exito en PostgreSQL"}
    except Exception as e:
        conexion.rollback()
        cursor.close()
        conexion.close()
        raise HTTPException(status_code=400, detail=f"Error al registrar en BD: {str(e)}")

# 2. RUTA PARA MOSTRAR TODOS LOS VEHICULOS (GET -> SELECT)
@app.get("/vehiculos")
def mostrar_vehiculos():
    conexion = obtener_conexion()
    if not conexion:
        raise HTTPException(status_code=500, detail="Error de conexión con el servidor de BD")
    
    cursor = conexion.cursor()
    cursor.execute("SELECT placa, marca, modelo, capacidad_carga, estado FROM dpt.vehiculos;")
    filas = cursor.fetchall()
    
    vehiculos = []
    for fila in filas:
        vehiculos.append({
            "placa": fila[0],
            "marca": fila[1],
            "modelo": fila[2],
            "capacidad_carga": float(fila[3]),
            "estado": fila[4]
        })
        
    cursor.close()
    conexion.close()
    return vehiculos

# 3. RUTA PARA ACTUALIZAR UN VEHÍCULO POR PLACA (PUT -> UPDATE)
@app.put("/vehiculos/{placa}")
def actualizar_vehiculo(placa: str, vehiculo_actualizado: Vehiculo):
    conexion = obtener_conexion()
    if not conexion:
        raise HTTPException(status_code=500, detail="Error de conexión con el servidor de BD")
    
    cursor = conexion.cursor()
    try:
        cursor.execute(
            "UPDATE dpt.vehiculos SET marca = %s, modelo = %s, capacidad_carga = %s, estado = %s WHERE placa = %s;",
            (vehiculo_actualizado.marca, vehiculo_actualizado.modelo, vehiculo_actualizado.capacidad_carga, vehiculo_actualizado.estado, placa)
        )
        conexion.commit()
        
        if cursor.rowcount == 0:
            cursor.close()
            conexion.close()
            return {"error": f"Vehiculo con placa [{placa}] no encontrado en la base de datos"}
            
        cursor.close()
        conexion.close()
        return {"mensaje": f"Vehiculo con placa [{placa}] actualizado con exito en PostgreSQL"}
    except Exception as e:
        conexion.rollback()
        cursor.close()
        conexion.close()
        raise HTTPException(status_code=400, detail=f"Error al actualizar en BD: {str(e)}")

# 4. RUTA PARA ELIMINAR UN VEHÍCULO POR PLACA (DELETE -> DELETE)
@app.delete("/vehiculos/{placa}")
def eliminar_vehiculo(placa: str):
    conexion = obtener_conexion()
    if not conexion:
        raise HTTPException(status_code=500, detail="Error de conexión con el servidor de BD")
    
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM dpt.vehiculos WHERE placa = %s;", (placa,))
    conexion.commit()
    
    if cursor.rowcount == 0:
        cursor.close()
        conexion.close()
        return {"error": f"Vehiculo con placa [{placa}] no encontrado en la base de datos"}
        
    cursor.close()
    conexion.close()
    return {"mensaje": f"Vehiculo con placa [{placa}] eliminado con exito en PostgreSQL"}