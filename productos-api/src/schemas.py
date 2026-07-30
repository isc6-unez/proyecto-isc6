from datetime import date
from typing import Optional
from pydantic import BaseModel


class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    unidad_medida: str
    cantidad: float
    precio_unitario: float
    estado: str = "disponible"
    fecha_produccion: Optional[date] = None


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(ProductoBase):
    pass