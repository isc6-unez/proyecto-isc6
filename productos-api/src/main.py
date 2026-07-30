from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import psycopg2
import os
from dotenv import load_dotenv

# Cargar las credenciales del archivo .env
load_dotenv()

app = FastAPI(title="Modulo de Inventario - CRUD Productos")

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

# Mapeo exacto de las columnas de tu productos.sql
class Producto(BaseModel):
    nombre: str                         # VARCHAR(150) NOT NULL
    descripcion: Optional[str] = None   # TEXT
    categoria: Optional[str] = None     # VARCHAR(100)
    unidad_medida: str                  # VARCHAR(50) NOT NULL
    peso: Optional[float] = None        # DECIMAL(10,2)
    dimensiones: Optional[str] = None   # VARCHAR(100)
    estado: str = "Activo"              # VARCHAR(20) - Por defecto 'Activo' en tu SQL

# 1. RUTA PARA REGISTRAR (POST -> INSERT)
@app.post("/productos")
def registrar_producto(producto: Producto):
    conexion = obtener_conexion()
    if not conexion:
        raise HTTPException(status_code=500, detail="Error de conexión con el servidor de BD")

    cursor = conexion.cursor()
    try:
        # id_producto se genera automáticamente en PostgreSQL por ser IDENTITY
        cursor.execute(
            "INSERT INTO dpt.productos (nombre, descripcion, categoria, unidad_medida, peso, dimensiones, estado) VALUES (%s, %s, %s, %s, %s, %s, %s);",
            (producto.nombre, producto.descripcion, producto.categoria, producto.unidad_medida, producto.peso, producto.dimensiones, producto.estado)
        )
        conexion.commit()
        cursor.close()
        conexion.close()
        return {"mensaje": f"Producto [{producto.nombre}] registrado con exito en PostgreSQL"}
    except Exception as e:
        conexion.rollback()
        cursor.close()
        conexion.close()
        raise HTTPException(status_code=400, detail=f"Error al registrar en BD: {str(e)}")

# 2. RUTA PARA MOSTRAR TODOS LOS PRODUCTOS (GET -> SELECT)
@app.get("/productos")
def mostrar_productos():
    conexion = obtener_conexion()
    if not conexion:
        raise HTTPException(status_code=500, detail="Error de conexión con el servidor de BD")

    cursor = conexion.cursor()
    cursor.execute("SELECT nombre, descripcion, categoria, unidad_medida, peso, dimensiones, estado FROM dpt.productos;")
    filas = cursor.fetchall()

    productos = []
    for fila in filas:
        productos.append({
            "nombre": fila[0],
            "descripcion": fila[1],
            "categoria": fila[2],
            "unidad_medida": fila[3],
            "peso": float(fila[4]) if fila[4] is not None else None,
            "dimensiones": fila[5],
            "estado": fila[6]
        })

    cursor.close()
    conexion.close()
    return productos

# 3. RUTA PARA ACTUALIZAR UN PRODUCTO POR NOMBRE (PUT -> UPDATE)
@app.put("/productos/{nombre}")
def actualizar_producto(nombre: str, producto_actualizado: Producto):
    conexion = obtener_conexion()
    if not conexion:
        raise HTTPException(status_code=500, detail="Error de conexión con el servidor de BD")

    cursor = conexion.cursor()
    try:
        cursor.execute(
            "UPDATE dpt.productos SET descripcion = %s, categoria = %s, unidad_medida = %s, peso = %s, dimensiones = %s, estado = %s WHERE nombre = %s;",
            (producto_actualizado.descripcion, producto_actualizado.categoria, producto_actualizado.unidad_medida, producto_actualizado.peso, producto_actualizado.dimensiones, producto_actualizado.estado, nombre)
        )
        conexion.commit()

        if cursor.rowcount == 0:
            cursor.close()
            conexion.close()
            return {"error": f"Producto [{nombre}] no encontrado en la base de datos"}

        cursor.close()
        conexion.close()
        return {"mensaje": f"Producto [{nombre}] actualizado con exito en PostgreSQL"}
    except Exception as e:
        conexion.rollback()
        cursor.close()
        conexion.close()
        raise HTTPException(status_code=400, detail=f"Error al actualizar en BD: {str(e)}")

# 4. RUTA PARA ELIMINAR UN PRODUCTO POR NOMBRE (DELETE -> DELETE)
@app.delete("/productos/{nombre}")
def eliminar_producto(nombre: str):
    conexion = obtener_conexion()
    if not conexion:
        raise HTTPException(status_code=500, detail="Error de conexión con el servidor de BD")

    cursor = conexion.cursor()
    cursor.execute("DELETE FROM dpt.productos WHERE nombre = %s;", (nombre,))
    conexion.commit()

    if cursor.rowcount == 0:
        cursor.close()
        conexion.close()
        return {"error": f"Producto [{nombre}] no encontrado en la base de datos"}

    cursor.close()
    conexion.close()
    return {"mensaje": f"Producto [{nombre}] eliminado con exito en PostgreSQL"}
