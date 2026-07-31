from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import os
from dotenv import load_dotenv

# Cargar las credenciales del archivo .env
load_dotenv()

app = FastAPI(title="Modulo de Productos Terminados - CRUD Productos")


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
    nombre: str
    descripcion: str
    categoria: str
    unidad_medida: str
    peso: float
    dimensiones: str
    estado: str = "Activo"


@app.post("/productos")
def registrar_producto(producto: Producto):
    conexion = obtener_conexion()
    if not conexion:
        raise HTTPException(status_code=500, detail="Error de conexión con el servidor de BD")

    cursor = conexion.cursor()
    try:
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


@app.get("/productos")
def mostrar_productos():
    conexion = obtener_conexion()
    if not conexion:
        raise HTTPException(status_code=500, detail="Error de conexión con el servidor de BD")

    cursor = conexion.cursor()
    cursor.execute("SELECT id_producto, nombre, descripcion, categoria, unidad_medida, peso, dimensiones, estado FROM dpt.productos;")
    filas = cursor.fetchall()

    productos = []
    for fila in filas:
        productos.append({
            "id_producto": fila[0],
            "nombre": fila[1],
            "descripcion": fila[2],
            "categoria": fila[3],
            "unidad_medida": fila[4],
            "peso": float(fila[5]),
            "dimensiones": fila[6],
            "estado": fila[7]
        })

    cursor.close()
    conexion.close()
    return productos


@app.put("/productos/{id_producto}")
def actualizar_producto(id_producto: int, producto_actualizado: Producto):
    conexion = obtener_conexion()
    if not conexion:
        raise HTTPException(status_code=500, detail="Error de conexión con el servidor de BD")

    cursor = conexion.cursor()
    try:
        cursor.execute(
            "UPDATE dpt.productos SET nombre = %s, descripcion = %s, categoria = %s, unidad_medida = %s, peso = %s, dimensiones = %s, estado = %s WHERE id_producto = %s;",
            (producto_actualizado.nombre, producto_actualizado.descripcion, producto_actualizado.categoria, producto_actualizado.unidad_medida, producto_actualizado.peso, producto_actualizado.dimensiones, producto_actualizado.estado, id_producto)
        )
        conexion.commit()

        if cursor.rowcount == 0:
            cursor.close()
            conexion.close()
            return {"error": f"Producto con id [{id_producto}] no encontrado en la base de datos"}

        cursor.close()
        conexion.close()
        return {"mensaje": f"Producto con id [{id_producto}] actualizado con exito en PostgreSQL"}
    except Exception as e:
        conexion.rollback()
        cursor.close()
        conexion.close()
        raise HTTPException(status_code=400, detail=f"Error al actualizar en BD: {str(e)}")


@app.delete("/productos/{id_producto}")
def eliminar_producto(id_producto: int):
    conexion = obtener_conexion()
    if not conexion:
        raise HTTPException(status_code=500, detail="Error de conexión con el servidor de BD")

    cursor = conexion.cursor()
    cursor.execute("DELETE FROM dpt.productos WHERE id_producto = %s;", (id_producto,))
    conexion.commit()

    if cursor.rowcount == 0:
        cursor.close()
        conexion.close()
        return {"error": f"Producto con id [{id_producto}] no encontrado en la base de datos"}

    cursor.close()
    conexion.close()
    return {"mensaje": f"Producto con id [{id_producto}] eliminado con exito en PostgreSQL"}
