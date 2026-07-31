from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from crud_clientes import (
    crear_cliente,
    obtener_clientes,
    obtener_cliente_por_id,
    actualizar_cliente,
    eliminar_cliente
)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# ---------- ENDPOINTS DE LA API ----------

@app.get("/api/clientes")
def api_obtener_clientes():
    clientes = obtener_clientes()
    resultado = []
    for c in clientes:
        resultado.append({
            "id_cliente": c[0],
            "nombre": c[1],
            "telefono": c[2],
            "correo": c[3],
            "direccion": c[4],
            "ciudad": c[5],
            "estado": c[6],
            "fecha_registro": str(c[7])
        })
    return resultado

@app.get("/api/clientes/{id_cliente}")
def api_obtener_cliente(id_cliente: int):
    c = obtener_cliente_por_id(id_cliente)
    if c is None:
        return JSONResponse(status_code=404, content={"error": "Cliente no encontrado"})
    return {
        "id_cliente": c[0],
        "nombre": c[1],
        "telefono": c[2],
        "correo": c[3],
        "direccion": c[4],
        "ciudad": c[5],
        "estado": c[6],
        "fecha_registro": str(c[7])
    }

@app.post("/api/clientes")
async def api_crear_cliente(request: Request):
    datos = await request.json()
    nuevo_id = crear_cliente(
        datos.get("nombre"),
        datos.get("telefono"),
        datos.get("correo"),
        datos.get("direccion"),
        datos.get("ciudad"),
        datos.get("estado")
    )
    return JSONResponse(status_code=201, content={"mensaje": "Cliente creado", "id_cliente": nuevo_id})

@app.put("/api/clientes/{id_cliente}")
async def api_actualizar_cliente(id_cliente: int, request: Request):
    datos = await request.json()
    filas = actualizar_cliente(
        id_cliente,
        datos.get("nombre"),
        datos.get("telefono"),
        datos.get("correo"),
        datos.get("direccion"),
        datos.get("ciudad"),
        datos.get("estado")
    )
    if filas == 0:
        return JSONResponse(status_code=404, content={"error": "Cliente no encontrado"})
    return {"mensaje": "Cliente actualizado"}

@app.delete("/api/clientes/{id_cliente}")
def api_eliminar_cliente(id_cliente: int):
    filas = eliminar_cliente(id_cliente)
    if filas == 0:
        return JSONResponse(status_code=404, content={"error": "Cliente no encontrado"})
    return {"mensaje": "Cliente eliminado"}

# ---------- VISTAS HTML ----------

@app.get("/clientes", response_class=HTMLResponse)
def vista_clientes(request: Request):
    clientes = obtener_clientes()
    return templates.TemplateResponse(request, "clientes.html", {"clientes": clientes})

@app.get("/clientes/nuevo", response_class=HTMLResponse)
def nuevo_cliente_form(request: Request):
    return templates.TemplateResponse(request, "form_cliente.html", {"cliente": None})

@app.post("/clientes/nuevo")
def nuevo_cliente_guardar(
    nombre: str = Form(...),
    telefono: str = Form(""),
    correo: str = Form(""),
    direccion: str = Form(""),
    ciudad: str = Form(""),
    estado: str = Form("")
):
    crear_cliente(nombre, telefono, correo, direccion, ciudad, estado)
    return RedirectResponse(url="/clientes", status_code=303)

@app.get("/clientes/editar/{id_cliente}", response_class=HTMLResponse)
def editar_cliente_form(request: Request, id_cliente: int):
    cliente = obtener_cliente_por_id(id_cliente)
    return templates.TemplateResponse(request, "form_cliente.html", {"cliente": cliente})

@app.post("/clientes/editar/{id_cliente}")
def editar_cliente_guardar(
    id_cliente: int,
    nombre: str = Form(...),
    telefono: str = Form(""),
    correo: str = Form(""),
    direccion: str = Form(""),
    ciudad: str = Form(""),
    estado: str = Form("")
):
    actualizar_cliente(id_cliente, nombre, telefono, correo, direccion, ciudad, estado)
    return RedirectResponse(url="/clientes", status_code=303)

@app.get("/clientes/eliminar/{id_cliente}")
def eliminar_cliente_web(id_cliente: int):
    eliminar_cliente(id_cliente)
    return RedirectResponse(url="/clientes", status_code=303)

@app.get("/clientes-prueba", response_class=HTMLResponse)
def vista_clientes_prueba(request: Request):
    clientes_falsos = [
        (1, "Juan Pérez", "8119205176", "juan@mail.com", "Calle Falsa 123", "Puebla", "Puebla", "2026-01-15"),
        (2, "Ana López", "7316908897", "ana@mail.com", "Av. Reforma 45", "CDMX", "CDMX", "2026-02-20"),
        (3, "Carlos Ruiz", "8125361300", "carlos@mail.com", "Blvd. Norte 789", "Monterrey", "Nuevo León", "2026-03-05"),
    ]
    return templates.TemplateResponse(request, "clientes.html", {"clientes": clientes_falsos})
