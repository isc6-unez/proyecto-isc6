from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Form
from fastapi.responses import RedirectResponse

from conexion import obtener_conexion

app = FastAPI(title="CRUD Productos")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def inicio(request: Request):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos ORDER BY id_producto")
    productos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"productos": productos}
    )


@app.get("/agregar", response_class=HTMLResponse)
def formulario_agregar(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="agregar.html",
        context={}
    )


@app.post("/agregar")
def guardar_producto(
    nombre: str = Form(...),
    descripcion: str = Form(""),
    categoria: str = Form(""),
    unidad_medida: str = Form(...),
    peso: float = Form(None),
    dimensiones: str = Form(""),
    estado: str = Form("Activo")
):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    sql = """
    INSERT INTO productos
    (nombre, descripcion, categoria, unidad_medida, peso, dimensiones, estado)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (
        nombre, descripcion, categoria, unidad_medida, peso, dimensiones, estado
    ))
    conexion.commit()
    cursor.close()
    conexion.close()
    return RedirectResponse(url="/", status_code=303)


@app.get("/editar/{id_producto}", response_class=HTMLResponse)
def formulario_editar(request: Request, id_producto: int):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM productos WHERE id_producto = %s",
        (id_producto,)
    )
    producto = cursor.fetchone()
    cursor.close()
    conexion.close()
    return templates.TemplateResponse(
        request=request,
        name="editar.html",
        context={"producto": producto}
    )


@app.post("/editar/{id_producto}")
def actualizar_producto(
    id_producto: int,
    nombre: str = Form(...),
    descripcion: str = Form(""),
    categoria: str = Form(""),
    unidad_medida: str = Form(...),
    peso: float = Form(None),
    dimensiones: str = Form(""),
    estado: str = Form("Activo")
):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    sql = """
    UPDATE productos
    SET nombre = %s, descripcion = %s, categoria = %s, unidad_medida = %s,
        peso = %s, dimensiones = %s, estado = %s
    WHERE id_producto = %s
    """
    cursor.execute(sql, (
        nombre, descripcion, categoria, unidad_medida, peso, dimensiones,
        estado, id_producto
    ))
    conexion.commit()
    cursor.close()
    conexion.close()
    return RedirectResponse(url="/", status_code=303)


@app.get("/eliminar/{id_producto}")
def eliminar_producto(id_producto: int):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "DELETE FROM productos WHERE id_producto = %s",
        (id_producto,)
    )
    conexion.commit()
    cursor.close()
    conexion.close()
    return RedirectResponse(url="/", status_code=303)
