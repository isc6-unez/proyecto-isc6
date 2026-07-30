from typing import Optional
from database import get_cursor
from schemas import ProductoCreate, ProductoUpdate


def listar_productos(busqueda: Optional[str] = None, estado: Optional[str] = None):
    query = "SELECT * FROM productos_terminados WHERE 1=1"
    params = []

    if busqueda:
        query += " AND nombre ILIKE %s"
        params.append(f"%{busqueda}%")

    if estado:
        query += " AND estado = %s"
        params.append(estado)

    query += " ORDER BY id_producto DESC"

    with get_cursor() as cur:
        cur.execute(query, params)
        return cur.fetchall()


def obtener_producto(id_producto: int):
    with get_cursor() as cur:
        cur.execute(
            "SELECT * FROM productos_terminados WHERE id_producto = %s",
            (id_producto,),
        )
        return cur.fetchone()


def crear_producto(producto: ProductoCreate):
    with get_cursor() as cur:
        cur.execute(
            """
            INSERT INTO productos_terminados
                (nombre, descripcion, unidad_medida, cantidad,
                 precio_unitario, estado, fecha_produccion)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING *;
            """,
            (
                producto.nombre,
                producto.descripcion,
                producto.unidad_medida,
                producto.cantidad,
                producto.precio_unitario,
                producto.estado,
                producto.fecha_produccion,
            ),
        )
        return cur.fetchone()


def actualizar_producto(id_producto: int, producto: ProductoUpdate):
    with get_cursor() as cur:
        cur.execute(
            """
            UPDATE productos_terminados
               SET nombre = %s,
                   descripcion = %s,
                   unidad_medida = %s,
                   cantidad = %s,
                   precio_unitario = %s,
                   estado = %s,
                   fecha_produccion = %s
             WHERE id_producto = %s
            RETURNING *;
            """,
            (
                producto.nombre,
                producto.descripcion,
                producto.unidad_medida,
                producto.cantidad,
                producto.precio_unitario,
                producto.estado,
                producto.fecha_produccion,
                id_producto,
            ),
        )
        return cur.fetchone()


def eliminar_producto(id_producto: int) -> bool:
    with get_cursor() as cur:
        cur.execute(
            "DELETE FROM productos_terminados WHERE id_producto = %s RETURNING id_producto;",
            (id_producto,),
        )
        return cur.fetchone() is not None