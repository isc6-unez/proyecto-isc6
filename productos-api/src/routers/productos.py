import os
from typing import Optional

from fastapi import APIRouter, Request, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

import crud
from schemas import ProductoCreate, ProductoUpdate

templates = Jinja2Templates(
    directory=os.path.join(os.path.dirname(__file__), "..", "templates")
)

router = APIRouter(tags=["Productos Terminados"])
api_router = APIRouter(prefix="/api/productos", tags=["API Productos Terminados"])

# ---------------------------------------------------------------
# Vistas HTML
# ---------------------------------------------------------------

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return RedirectResponse(url="/productos")


@router.get("/productos", response_class=HTMLResponse)
def vista_lista(request: Request, q: Optional[str] = None, estado: Optional[str] = None):
    productos = crud.listar_productos(busqueda=q, estado=estado)
    return templates.TemplateResponse(
        request=request,
        name="list.html",
        context={"productos": productos, "q": q or "", "estado": estado or ""},
    )


@router.get("/productos/nuevo", response_class=HTMLResponse)
def vista_nuevo(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="form.html",
        context={"producto": None, "modo": "crear"},
    )


@router.post("/productos/nuevo")
def crear_producto_form(
    nombre: str = Form(...),
    descripcion: str = Form(""),
    unidad_medida: str = Form(...),
    cantidad: float = Form(...),
    precio_unitario: float = Form(...),
    estado: str = Form("disponible"),
    fecha_produccion: Optional[str] = Form(None),
):
    producto = ProductoCreate(
        nombre=nombre, descripcion=descripcion, unidad_medida=unidad_medida,
        cantidad=cantidad, precio_unitario=precio_unitario, estado=estado,
        fecha_produccion=fecha_produccion or None,
    )
    crud.crear_producto(producto)
    return RedirectResponse(url="/productos", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/productos/{id_producto}/editar", response_class=HTMLResponse)
def vista_editar(request: Request, id_producto: int):
    producto = crud.obtener_producto(id_producto)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return templates.TemplateResponse(
        request=request,
        name="form.html",
        context={"producto": producto, "modo": "editar"}
    )


@router.post("/productos/{id_producto}/editar")
def actualizar_producto_form(
    id_producto: int,
    nombre: str = Form(...),
    descripcion: str = Form(""),
    unidad_medida: str = Form(...),
    cantidad: float = Form(...),
    precio_unitario: float = Form(...),
    estado: str = Form("disponible"),
    fecha_produccion: Optional[str] = Form(None),
):
    producto = ProductoUpdate(
        nombre=nombre, descripcion=descripcion, unidad_medida=unidad_medida,
        cantidad=cantidad, precio_unitario=precio_unitario, estado=estado,
        fecha_produccion=fecha_produccion or None,
    )
    crud.actualizar_producto(id_producto, producto)
    return RedirectResponse(url="/productos", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/productos/{id_producto}/eliminar")
def eliminar_producto_form(id_producto: int):
    crud.eliminar_producto(id_producto)
    return RedirectResponse(url="/productos", status_code=status.HTTP_303_SEE_OTHER)


# ---------------------------------------------------------------
# API JSON
# ---------------------------------------------------------------

@api_router.get("/")
def api_listar(q: Optional[str] = None, estado: Optional[str] = None):
    return crud.listar_productos(busqueda=q, estado=estado)


@api_router.get("/{id_producto}")
def api_obtener(id_producto: int):
    producto = crud.obtener_producto(id_producto)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@api_router.post("/", status_code=status.HTTP_201_CREATED)
def api_crear(producto: ProductoCreate):
    return crud.crear_producto(producto)


@api_router.put("/{id_producto}")
def api_actualizar(id_producto: int, producto: ProductoUpdate):
    actualizado = crud.actualizar_producto(id_producto, producto)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return actualizado


@api_router.delete("/{id_producto}")
def api_eliminar(id_producto: int):
    eliminado = crud.eliminar_producto(id_producto)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"ok": True}