from database import get_connection

def crear_cliente(nombre, telefono, correo, direccion, ciudad, estado):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO clientes (nombre, telefono, correo, direccion, ciudad, estado)
           VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_cliente""",
        (nombre, telefono, correo, direccion, ciudad, estado)
    )
    nuevo_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return nuevo_id

def obtener_clientes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM clientes ORDER BY id_cliente")
    resultados = cur.fetchall()
    cur.close()
    conn.close()
    return resultados

def obtener_cliente_por_id(id_cliente):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM clientes WHERE id_cliente = %s", (id_cliente,))
    resultado = cur.fetchone()
    cur.close()
    conn.close()
    return resultado

def actualizar_cliente(id_cliente, nombre, telefono, correo, direccion, ciudad, estado):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """UPDATE clientes SET nombre=%s, telefono=%s, correo=%s,
           direccion=%s, ciudad=%s, estado=%s WHERE id_cliente=%s""",
        (nombre, telefono, correo, direccion, ciudad, estado, id_cliente)
    )
    conn.commit()
    filas_afectadas = cur.rowcount
    cur.close()
    conn.close()
    return filas_afectadas

def eliminar_cliente(id_cliente):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM clientes WHERE id_cliente = %s", (id_cliente,))
    conn.commit()
    filas_afectadas = cur.rowcount
    cur.close()
    conn.close()
    return filas_afectadas