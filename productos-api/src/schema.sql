CREATE SCHEMA IF NOT EXISTS dpt;

CREATE TABLE IF NOT EXISTS dpt.productos_terminados (
    id_producto      SERIAL PRIMARY KEY,
    nombre           VARCHAR(150) NOT NULL,
    descripcion      TEXT,
    unidad_medida    VARCHAR(30)  NOT NULL DEFAULT 'pieza',
    cantidad         INTEGER      NOT NULL DEFAULT 0 CHECK (cantidad >= 0),
    precio_unitario  NUMERIC(10,2) NOT NULL DEFAULT 0 CHECK (precio_unitario >= 0),
    estado           VARCHAR(20)  NOT NULL DEFAULT 'disponible'
                     CHECK (estado IN ('disponible', 'agotado', 'descontinuado')),
    fecha_produccion DATE,
    creado_en        TIMESTAMP NOT NULL DEFAULT NOW(),
    actualizado_en   TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE OR REPLACE FUNCTION dpt.set_actualizado_en()
RETURNS TRIGGER AS $$
BEGIN
    NEW.actualizado_en = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_productos_terminados_actualizado ON dpt.productos_terminados;
CREATE TRIGGER trg_productos_terminados_actualizado
    BEFORE UPDATE ON dpt.productos_terminados
    FOR EACH ROW
    EXECUTE FUNCTION dpt.set_actualizado_en();